"""Build one LIGHT STATE of the ship's three walls on the DAY walls' exact geometry.

  python tools/ship_states.py DAY_DIR --c C_TAKE.png --l L_TAKE.png --r R_TAKE.png OUTDIR

DAY_DIR = assembled_v1/ (S7-SHIP-<WALL>_1080.png, the approved day geometry). Each raw NBP state take is warped onto
its day wall by tools/ship_align.py (SIFT similarity, missing edge strips filled), written as S7-SHIP-<WALL>_1080.png,
plus S7-SHIP_walls_preview.jpg (4680 wide at half size, seams in yellow, the day horizon in red) and a log of each
wall's measured scale/shift.

WHY (2026-10-06): states are crossfaded by script on one geometry. ship_assemble.py's scale-and-crop kept NBP's
reframing (NIGHT CENTRE 7.5% off), so a light change would jump. This replaces it for states; ship_assemble.py stays
the tool for the day set itself.
"""
import argparse
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from ship_align import similarity, fill_from_day  # noqa: E402

HZ = 0.387


def align(day, take):
    h, w = day.shape[:2]
    f = h / take.shape[0]
    small = cv2.resize(take, (int(round(take.shape[1] * f)), h), interpolation=cv2.INTER_AREA)
    M, inl, n = similarity(day, small)
    Mf = M / f
    out = cv2.warpAffine(take, Mf, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LANCZOS4, borderValue=(0, 0, 0))
    inside = cv2.warpAffine(np.full(take.shape[:2], 255, np.uint8), Mf, (w, h),
                            flags=cv2.WARP_INVERSE_MAP | cv2.INTER_NEAREST, borderValue=0) > 0
    miss = 1 - inside.mean()
    if miss > 0:
        refl = cv2.warpAffine(take, Mf, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LANCZOS4,
                              borderMode=cv2.BORDER_REFLECT_101).astype(np.float32)
        out = fill_from_day(out, day, inside, refl)
    return out, f'scale {np.hypot(M[0, 0], M[1, 0]):.4f} shift {M[0, 2]:.1f},{M[1, 2]:.1f} inliers {inl}/{n} filled {miss * 100:.2f}%'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('day_dir'); ap.add_argument('outdir')
    ap.add_argument('--c', required=True); ap.add_argument('--l', required=True); ap.add_argument('--r', required=True)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    walls, log = [], []
    for name, take in (('LEFT', a.l), ('CENTRE', a.c), ('RIGHT', a.r)):
        day = cv2.imread(os.path.join(a.day_dir, f'S7-SHIP-{name}_1080.png'))
        out, msg = align(day, cv2.imread(take))
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{name}_1080.png'), out)
        walls.append(out)
        log.append(f'{name}: {os.path.basename(take)}  {msg}')
        print(log[-1])
    pv = np.concatenate(walls, axis=1)
    for x in (1440, 3240):
        pv[:, x - 2:x + 2] = (0, 200, 255)
    pv[int(HZ * 1080), :, :] = (0, 0, 255)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_preview.jpg'), cv2.resize(pv, (2340, 540)), [cv2.IMWRITE_JPEG_QUALITY, 88])
    with open(os.path.join(a.outdir, 'ALIGN_LOG.txt'), 'w') as fh:
        fh.write('tools/ship_states.py onto ' + a.day_dir + '\n' + '\n'.join(log) + '\n')


if __name__ == '__main__':
    main()
