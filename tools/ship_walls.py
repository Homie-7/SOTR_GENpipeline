"""Cut ONE wide deck plate into the three walls, 4 : 5 : 4 (LEFT 1440, CENTRE 1800, RIGHT 1440 at 1080 high).

  python tools/ship_walls.py PLATE.png OUTDIR [--band 0.5] [--scale 1080] [--preview]

The plate is scaled so that the 4680 x 1080 canvas fits its width; --band picks which horizontal strip is kept
(0 = the top, 1 = the bottom, 0.5 = the middle). If the plate is too SHORT for its width at 4.33:1 nothing is lost
sideways; if it is too NARROW (the usual case: NBP's widest is 21:9 = 2.33:1 against the stage's 4.33:1) the tool says
how many pixels each side must be OUTPAINTED first, and stops (it never stretches).
Writes <stem>_LEFT.png, _CENTRE.png, _RIGHT.png and, with --preview, <stem>_walls.jpg (the three side by side, with
the two seams marked).

WHY (2026-10-05, docs/PLAN-SHIP-INTRO.md, after Sahaj's 4D-viewer capture): one image = one light, one horizon and
one ship; the rails carry across both seams by construction, and the walls drop straight into Sahaj's layout.
"""
import argparse
import os

import cv2
import numpy as np

CANVAS_W, CANVAS_H = 4680, 1080
WALLS = (('LEFT', 0, 1440), ('CENTRE', 1440, 3240), ('RIGHT', 3240, 4680))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plate')
    ap.add_argument('outdir')
    ap.add_argument('--band', type=float, default=0.5, help='0 top .. 1 bottom: which strip of the plate is kept')
    ap.add_argument('--preview', action='store_true')
    a = ap.parse_args()
    im = cv2.imread(a.plate, cv2.IMREAD_UNCHANGED)
    h, w = im.shape[:2]
    need_w = h * CANVAS_W / CANVAS_H          # width the plate would need to fill the canvas at its full height
    s = CANVAS_W / w
    if h * s < CANVAS_H:                      # too short: impossible without stretching
        add = int(np.ceil((CANVAS_H / s - h) / 2))
        raise SystemExit(f'plate too short for 4.33:1 by {2 * add} px of height: outpaint {add} px top and bottom')
    kept = CANVAS_H / s                       # plate rows that survive
    print(f'plate {w}x{h}: keeps {kept:.0f} of {h} rows ({kept / h:.0%}); full height would need '
          f'{need_w:.0f} px wide = outpaint {max(0, (need_w - w) / 2):.0f} px each side')
    big = cv2.resize(im, (CANVAS_W, int(round(h * s))), interpolation=cv2.INTER_LANCZOS4)
    y0 = int(round((big.shape[0] - CANVAS_H) * min(max(a.band, 0), 1)))
    canvas = big[y0:y0 + CANVAS_H]
    os.makedirs(a.outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(a.plate))[0]
    for name, x0, x1 in WALLS:
        cv2.imwrite(os.path.join(a.outdir, f'{stem}_{name}.png'), canvas[:, x0:x1])
    if a.preview:
        pv = canvas[..., :3].copy()
        for x in (1440, 3240):
            pv[:, x - 2:x + 2] = (0, 200, 255)
        cv2.imwrite(os.path.join(a.outdir, f'{stem}_walls.jpg'), cv2.resize(pv, (2340, 540)),
                    [cv2.IMWRITE_JPEG_QUALITY, 88])
    print('walls written to', a.outdir)


if __name__ == '__main__':
    main()
