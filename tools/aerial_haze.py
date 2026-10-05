"""Physically based distance haze + depth of field on an open-sea plate, focused on a near subject (the intro's gull).

  python tools/aerial_haze.py IN.png OUT.png --subject x,y,w,h [--cam-h 3] [--fov 50] [--vis 9000] [--ship-km 6]
                              [--focus 4] [--fstop 4] [--check]

WHY (Homie, 5 Oct 2026, on S7-INTRO-F1): "volumetric fog in the distance… real life physics… not sure we should be able to
see the ship so clearly if the cam is next to the bird, DOF as well… if that can be done in post, do that." Free, exact,
repeatable, and applied to the START FRAME so the Seedance flight inherits it.

PHYSICS.
- Distance per pixel. Over a flat sea, a camera CAM_H m above the water with focal length f px sees the sea at row y
  (below the horizon row hz) at distance d = CAM_H * f / (y - hz). Everything at or above the horizon band (the ship,
  the far clouds) is put at SHIP_KM.
- Haze (Koschmieder): I = J t + A (1 - t), t = exp(-beta d), beta = 3.912 / VIS (VIS = meteorological visibility, m).
  Above the horizon the haze fades out over SKY_BAND of the height (first run flattened the whole sky: wrong).
  A, the airlight, is sampled from the sky just above the horizon, so the far sea and the ship melt into the real sky.
- Depth of field (thin lens): blur circle c(d) = (f_mm^2 / N) |1/S - 1/d| / (1 - f_mm/S), converted to px; S = the focus
  distance (the gull), N = the f-number. Far objects get c(inf); the near sea under the gull stays sharp. Built from a
  stack of Gaussian blurs blended per pixel.
- The subject (its box, refined by GrabCut) is in focus and close: no haze, no blur; it is laid back on top.
"""
import argparse

import cv2
import numpy as np


def horizon_row(img):
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h = lum.shape[0]
    prof = cv2.GaussianBlur(lum.mean(axis=1).reshape(-1, 1), (1, 9), 0).ravel()
    g = np.abs(np.diff(prof))
    return int(np.argmax(g[h // 8: h * 7 // 8])) + h // 8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--subject', required=True, help='x,y,w,h box around the near subject (px, full size)')
    ap.add_argument('--cam-h', type=float, default=3.0)
    ap.add_argument('--fov', type=float, default=50.0, help='horizontal field of view, degrees')
    ap.add_argument('--vis', type=float, default=25000.0, help='meteorological visibility, metres (25 km: a clear Atlantic day)')
    ap.add_argument('--sky-band', type=float, default=0.06, help='above the horizon, the haze fades out over this fraction of the height')
    ap.add_argument('--ship-km', type=float, default=6.0)
    ap.add_argument('--focus', type=float, default=4.0, help='focus distance, metres (the subject)')
    ap.add_argument('--fstop', type=float, default=4.0)
    ap.add_argument('--sensor-mm', type=float, default=36.0)
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()

    img = cv2.imread(a.inp, cv2.IMREAD_COLOR)
    h, w = img.shape[:2]
    J = img.astype(np.float32) / 255.0
    f_px = (w / 2) / np.tan(np.radians(a.fov / 2))
    hz = horizon_row(img)

    # distance map (m)
    yy = np.arange(h, dtype=np.float32)
    d_row = np.where(yy > hz + 2, a.cam_h * f_px / np.maximum(yy - hz, 1e-3), a.ship_km * 1000.0)
    d_row = np.minimum(d_row, a.ship_km * 1000.0)
    d = np.repeat(d_row[:, None], w, axis=1)

    # airlight from the sky band just above the horizon
    band = J[max(0, hz - h // 20): max(1, hz - 3), :, :].reshape(-1, 3)
    A = np.median(band, axis=0)

    beta = 3.912 / a.vis
    t = np.exp(-beta * d)
    # Above the horizon only the near-horizon band (the ship, the far cloud base) is at SHIP_KM; the open sky above it is
    # already the airlight integrated through the whole atmosphere, so the haze fades out upward (it never flattens the sky).
    fade = np.exp(-np.maximum(hz - yy, 0) / (a.sky_band * h))[:, None]
    t = np.where((yy <= hz + 2)[:, None], 1 - (1 - t) * fade, t)[..., None]
    hazed = J * t + A[None, None, :] * (1 - t)

    # depth of field
    f_mm = (a.sensor_mm / 2) / np.tan(np.radians(a.fov / 2))
    S = a.focus * 1000.0
    dmm = d * 1000.0
    c_mm = (f_mm ** 2 / a.fstop) * np.abs(1.0 / S - 1.0 / dmm) / (1.0 - f_mm / S)
    c_px = c_mm * (w / a.sensor_mm)
    sig = np.clip(c_px / 2.355, 0, 40)            # blur circle -> Gaussian sigma
    levels = [0, 1, 2, 3.5, 5, 7, 10, 14, 20, 28, 40]
    stack = [hazed] + [cv2.GaussianBlur(hazed, (0, 0), s) for s in levels[1:]]
    out = np.zeros_like(hazed)
    for i in range(len(levels) - 1):
        lo, hi = levels[i], levels[i + 1]
        wgt = np.clip((sig - lo) / (hi - lo), 0, 1)
        inside = ((sig >= lo) & (sig < hi))[..., None]
        out = np.where(inside, stack[i] * (1 - wgt[..., None]) + stack[i + 1] * wgt[..., None], out)
    out = np.where((sig >= levels[-1])[..., None], stack[-1], out)

    # the subject: GrabCut inside its box, kept sharp and clear
    x, y, bw, bh = [int(v) for v in a.subject.split(',')]
    mask = np.zeros((h, w), np.uint8)
    bgd, fgd = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, (x, y, bw, bh), bgd, fgd, 6, cv2.GC_INIT_WITH_RECT)
    sub = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 1.0, 0.0).astype(np.float32)
    sub = cv2.GaussianBlur(sub, (0, 0), 1.2)[..., None]
    out = out * (1 - sub) + J * sub

    cv2.imwrite(a.out, np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8))
    print(f'horizon row {hz}/{h}; f {f_px:.0f} px; airlight {np.round(A * 255).astype(int)}; '
          f'ship transmission {np.exp(-beta * a.ship_km * 1000):.2f}; far blur sigma {sig.max():.1f} px; '
          f'subject {sub.mean():.1%} of frame')
    if a.check:
        cv2.imwrite(a.out.rsplit('.', 1)[0] + '_submask.png', (sub[..., 0] * 255).astype(np.uint8))


if __name__ == '__main__':
    main()
