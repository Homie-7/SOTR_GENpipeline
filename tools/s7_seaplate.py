"""The ship-free SEA PLATE per light state, registered onto the deck canvas (9 Oct, Homie: "I can very clearly see the
lines of what was erased").

  python tools/s7_seaplate.py STATE PLATE.png [--harmony 448]

PLATE = the Nano Banana edit of 7_canvas21/S7-SHIP-CANVAS21_<state>.png with the whole ship removed
(prompts/S7-SEA-PLATE.txt). It comes back reframed a little (3168x1344, not the canvas's 2.296:1), so:
1. ECC (affine) onto the canvas, on the open sky and sea at both ends of the frame, outside the shrouds (the plate keeps
   the canvas's clouds), from a scale + shift first guess;
2. its low-frequency colour is matched to the canvas's own sea and sky (a smooth per-channel gain, measured on the
   canvas's world pixels: the walls band's _bgmask_v2 plus the outer sky), so the still ship's edges sit on the same
   colour they were painted against;
   --harmony H (sunset): the sunset canvas predates tools/ship_skyharmony.py, so its side skies keep their own style and
   Nano Banana copied the wall seams (x 1440 / 3240) three times over: the same harmonise (k from the still) is run on
   the plate's sky (a seam blur was tried and read as smoke columns: dropped; the seams sit behind the shroud nets).
3. writes 9_seaplate/S7-SEA-PLATE_<state>_reg.png (4680x2038, canvas pixels) and _upload.png (2480x1080, the start frame
   for prompts/S7-SEA-IDLE.txt) + _check.jpg (canvas | plate, the ship's outline drawn on both).
"""
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s7_worldfill import horizon_cols, masked_blur  # noqa: E402

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/'
WALLS = ('LEFT', 'CENTRE', 'RIGHT')
CW, CH, B0 = 4680, 2038, 479


def horizon_offset(plate, can, wmask, Hc, win=90, srch=40, step=180):
    """how far the plate's horizon sits from the canvas's, per column (9 Oct). Edge hunting failed on the plate (night: a
    dark violet band above the line; sunset: the glow), so the plate's brightness PROFILE across the horizon (sky, haze,
    line, sea) is slid against the canvas's own profile (world pixels only) and the best-correlating shift kept, per
    window; then a robust straight line. Returns the shift per column (plate row = canvas row + shift)."""
    gp = cv2.cvtColor(plate.astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    gc = cv2.cvtColor(can, cv2.COLOR_BGR2GRAY).astype(np.float32)
    xs, ds = [], []
    for x in range(0, CW - step, step):
        c = slice(x, x + step)
        h0 = int(Hc[x + step // 2]) + B0
        m = wmask[h0 - win:h0 + win, c]
        if m.mean() < 0.6:
            continue
        pc = (gc[h0 - win:h0 + win, c] * m).sum(1) / np.maximum(m.sum(1), 1)
        pc = np.diff(pc)
        best, bs = -2, 0
        for sh in range(-srch, srch + 1):
            pp = np.diff(gp[h0 - win + sh:h0 + win + sh, c].mean(1))
            r = np.corrcoef(pc, pp)[0, 1]
            if r > best:
                best, bs = r, sh
        if best > 0.5:
            xs.append(x + step // 2); ds.append(bs)
    xs, ds = np.array(xs, float), np.array(ds, float)
    if len(xs) < 3:                                   # magic: a soft hazy horizon, no confident window: trust the ECC
        print(f'  horizon offset: only {len(xs)} confident windows, no shear (the ECC registration stands)')
        return 0.0, 0.0
    keep = np.ones(len(xs), bool)
    for _ in range(3):
        a1, b1 = np.polyfit(xs[keep], ds[keep], 1)
        r = np.abs(ds - (a1 * xs + b1))
        keep = r < max(2.0, np.median(r[keep]) * 2.5)
    print(f'  horizon offset plate - canvas: {b1:+.1f} px at x=0, {a1 * CW + b1:+.1f} px at x={CW} ({keep.sum()}/{len(xs)} windows)')
    return a1, b1


def world_mask(st):
    """canvas pixels that are sea/sky: the band from the bgmask_v2, above it the outer sky (no rigging there)"""
    m = np.zeros((CH, CW), bool)
    bg = np.hstack([cv2.imread(T + f'5_layers/seamed_v2/{st}/S7-SHIP-{x}_1080_bgmask_v2.png', 0) for x in WALLS])
    m[B0:B0 + 1080] = bg > 127
    m[:B0, :1050] = True
    m[:B0, 3700:] = True
    return m


def main():
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument('state'); ap.add_argument('plate')
    ap.add_argument('--harmony', type=int, default=0, help='sunset: the horizon row (band) for ship_skyharmony')
    a = ap.parse_args()
    st, src = a.state, a.plate
    can = cv2.imread(T + f'7_canvas21/S7-SHIP-CANVAS21_{st}.png')
    pl = cv2.imread(src)
    ph, pw = pl.shape[:2]
    wm = world_mask(st)
    # ECC on the outer sky + sea (the shrouds start ~x 1100 and end ~x 3600 on the canvas), rows above the near swell
    em = np.zeros((CH, CW), np.uint8)
    em[:1150, :1050] = 255; em[:1150, 3700:] = 255
    em &= np.where(wm, 255, 0).astype(np.uint8)
    s = CH / ph                                       # first guess: fill the height, centred
    M = np.float32([[s, 0, (CW - pw * s) / 2], [0, s, 0]])
    pre = cv2.warpAffine(pl, M, (CW, CH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT_101)
    g0 = cv2.cvtColor(can, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g1 = cv2.cvtColor(pre, cv2.COLOR_BGR2GRAY).astype(np.float32)
    # canvas coords -> pre-scaled plate coords. Several starting scales (9 Oct: Nano Banana reframes each run differently,
    # day 1.045, night 0.974; magic's single start ran off to 1.85): the best correlation with a sane scale wins
    best, W = -1.0, None
    for s0 in (1.0, 0.96, 1.04, 0.92, 1.08):
        Wt = np.float32([[s0, 0, CW / 2 * (1 - s0)], [0, s0, CH / 2 * (1 - s0)]])
        try:
            for blur in (9, 5, 1.5):
                cc, Wt = cv2.findTransformECC(cv2.GaussianBlur(g0, (0, 0), blur), cv2.GaussianBlur(g1, (0, 0), blur), Wt,
                                              cv2.MOTION_AFFINE,
                                              (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 400, 1e-7), em, 5)
        except cv2.error:
            continue
        sc = np.hypot(*Wt[:, 0])
        if abs(sc - 1) < 0.15 and cc > best:
            best, W = cc, Wt
    assert W is not None, 'no sane registration found'
    reg = cv2.warpAffine(pre, W, (CW, CH), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP,
                         borderMode=cv2.BORDER_REFLECT_101).astype(np.float32)
    Mi = W
    # the HORIZON wins over the clouds: the plate's horizon line is put exactly on the canvas's (a vertical shear + shift;
    # the clouds move a few px, invisible), measured as tools/s7_worldfill.horizon_cols does for the idles
    still = np.hstack([cv2.imread(T + f'3_walls/seamed_v2/{st}/S7-SHIP-{x}_1080.png') for x in WALLS])
    bgb = np.where(wm[B0:B0 + 1080], 255, 0).astype(np.uint8)
    _, Hc = horizon_cols(still, bgb)
    a1, b1 = horizon_offset(reg, can, wm, Hc)
    S = np.float32([[1, 0, 0], [a1, 1, b1]])          # canvas y -> plate y: y + offset(x)
    reg = cv2.warpAffine(reg, S, (CW, CH), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT_101)
    # low-frequency colour match: gain = blur(canvas) / blur(plate) on world pixels, filled smoothly elsewhere
    cf = can.astype(np.float32)
    # sea/sky colour goes by distance to the horizon (rows) and only slowly sideways: an anisotropic masked blur
    # (200 px across, 6 px down) keeps the haze band and the sun side, and copies no local detail of the canvas
    wb = wm.copy(); wb[:B0] = False                   # the band only: the outer-sky patches made slabs (magic, sunset)
    wg = cv2.erode(wb.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
    def ablur(x):
        return cv2.GaussianBlur(x, (0, 0), sigmaX=200, sigmaY=6)
    den = ablur(wg)
    mc = ablur(cf * wg[..., None]) / np.maximum(den, 1e-4)[..., None]
    mp = ablur(reg * wg[..., None]) / np.maximum(den, 1e-4)[..., None]
    gain = np.clip(mc / np.maximum(mp, 1), 0.75, 1.33)
    gain[den < 0.05] = 1.0                            # no world pixels near (under the deck): no correction
    top = B0 + 40                                     # above the band: the band's top row of gain, carried up unchanged
    gain[:top] = gain[top]
    gain = cv2.GaussianBlur(gain, (0, 0), sigmaX=60, sigmaY=4)
    out = np.clip(reg * gain, 0, 255).astype(np.uint8)
    if a.harmony:
        from ship_skyharmony import harmonise
        kk = np.load(T + f'3_walls/seamed_v2/{st}/SKYHARMONY_k.npy')
        top = out[:B0 + 1080].copy()
        out[:B0 + 1080] = harmonise(top, np.ones(top.shape[:2], np.float32), B0 + a.harmony, k={'L': kk[0], 'R': kk[1]})[0]
    d = T + '9_seaplate/'
    os.makedirs(d, exist_ok=True)
    cv2.imwrite(d + f'S7-SEA-PLATE_{st}_reg.png', out)
    cv2.imwrite(d + f'S7-SEA-PLATE_{st}_upload.png', cv2.resize(out, (2480, 1080), interpolation=cv2.INTER_AREA))
    err = np.abs(out.astype(np.float32) - cf)[wm].mean()
    edge = cv2.morphologyEx(wm.astype(np.uint8), cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(bool)
    a, b = can.copy(), out.copy()
    a[edge] = b[edge] = (0, 0, 255)
    cv2.imwrite(d + f'S7-SEA-PLATE_{st}_check.jpg', cv2.resize(np.vstack([a, b]), (2340, 2038)), [cv2.IMWRITE_JPEG_QUALITY, 90])
    sx = np.hypot(*Mi[:, 0]); print(f'{st}: ECC {best:.4f}, scale {1 / sx:.4f}, gain {gain.min():.2f}..{gain.max():.2f}, '
                                   f'mean |plate - canvas| on world px {err:.1f}')


if __name__ == '__main__':
    main()
