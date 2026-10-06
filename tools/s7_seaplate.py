"""The ship-free SEA PLATE per light state, registered onto the deck canvas (9 Oct, Homie: "I can very clearly see the
lines of what was erased").

  python tools/s7_seaplate.py STATE PLATE.png

PLATE = the Nano Banana edit of 7_canvas21/S7-SHIP-CANVAS21_<state>.png with the whole ship removed
(prompts/S7-SEA-PLATE.txt). It comes back reframed a little (3168x1344, not the canvas's 2.296:1), so:
1. ECC (affine) onto the canvas, on the open sky and sea at both ends of the frame, outside the shrouds (the plate keeps
   the canvas's clouds), from a scale + shift first guess;
2. its low-frequency colour is matched to the canvas's own sea and sky (a smooth per-channel gain, measured on the
   canvas's world pixels: the walls band's _bgmask_v2 plus the outer sky), so the still ship's edges sit on the same
   colour they were painted against;
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


def world_mask(st):
    """canvas pixels that are sea/sky: the band from the bgmask_v2, above it the outer sky (no rigging there)"""
    m = np.zeros((CH, CW), bool)
    bg = np.hstack([cv2.imread(T + f'5_layers/seamed_v2/{st}/S7-SHIP-{x}_1080_bgmask_v2.png', 0) for x in WALLS])
    m[B0:B0 + 1080] = bg > 127
    m[:B0, :1050] = True
    m[:B0, 3700:] = True
    return m


def main():
    st, src = sys.argv[1], sys.argv[2]
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
    W = np.eye(2, 3, dtype=np.float32)               # canvas coords -> pre-scaled plate coords
    for blur in (9, 5, 1.5):
        best, W = cv2.findTransformECC(cv2.GaussianBlur(g0, (0, 0), blur), cv2.GaussianBlur(g1, (0, 0), blur), W,
                                       cv2.MOTION_AFFINE, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 400, 1e-7),
                                       em, 5)
    reg = cv2.warpAffine(pre, W, (CW, CH), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP,
                         borderMode=cv2.BORDER_REFLECT_101).astype(np.float32)
    Mi = W
    # the HORIZON wins over the clouds: the plate's horizon line is put exactly on the canvas's (a vertical shear + shift;
    # the clouds move a few px, invisible), measured as tools/s7_worldfill.horizon_cols does for the idles
    still = np.hstack([cv2.imread(T + f'3_walls/seamed_v2/{st}/S7-SHIP-{x}_1080.png') for x in WALLS])
    bgb = np.where(wm[B0:B0 + 1080], 255, 0).astype(np.uint8)
    _, Hc = horizon_cols(still, bgb)
    _, Hp = horizon_cols(reg[B0:B0 + 1080].astype(np.uint8), np.full((1080, CW), 255, np.uint8))
    xs = np.arange(CW)
    ac, bc = np.polyfit(xs, Hc.astype(float), 1); ap, bp = np.polyfit(xs, Hp.astype(float), 1)
    S = np.float32([[1, 0, 0], [ap - ac, 1, bp - bc]])   # canvas y -> plate y: y + (Hp(x) - Hc(x))
    reg = cv2.warpAffine(reg, S, (CW, CH), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT_101)
    print(f'{st}: horizon canvas {Hc[0]}..{Hc[-1]}, plate {Hp[0]}..{Hp[-1]} (band rows) -> moved onto the canvas')
    # low-frequency colour match: gain = blur(canvas) / blur(plate) on world pixels, filled smoothly elsewhere
    cf = can.astype(np.float32)
    # sea/sky colour goes by distance to the horizon (rows) and only slowly sideways: an anisotropic masked blur
    # (200 px across, 6 px down) keeps the haze band and the sun side, and copies no local detail of the canvas
    wg = cv2.erode(wm.astype(np.uint8), np.ones((15, 15), np.uint8)).astype(np.float32)
    def ablur(x):
        return cv2.GaussianBlur(x, (0, 0), sigmaX=200, sigmaY=6)
    den = ablur(wg)
    mc = ablur(cf * wg[..., None]) / np.maximum(den, 1e-4)[..., None]
    mp = ablur(reg * wg[..., None]) / np.maximum(den, 1e-4)[..., None]
    gain = np.clip(mc / np.maximum(mp, 1), 0.75, 1.33)
    gain[den < 0.05] = 1.0                            # no world pixels near (under the deck): no correction
    gain = cv2.GaussianBlur(gain, (0, 0), sigmaX=60, sigmaY=4)
    out = np.clip(reg * gain, 0, 255).astype(np.uint8)
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
