"""Assemble the ship's three walls at 1080: CENTRE 1800x1080, LEFT/RIGHT 1440x1080, every horizon on ONE line.

  python tools/ship_assemble.py --centre C.png --left L.png --right R.png OUTDIR [--cut-l 0.2] [--cut-r 0.2]

CENTRE is scaled to 1080 high and centre-cropped to 1800 wide. Its horizon row (measured) sets the line. Each side wall
first loses CUT of its width on the side facing CENTRE (NBP's side takes re-show the bow and the mast foot there: they
are not true continuations, LOG 2026-10-05), then is cropped to 4:3 and scaled so its own measured horizon lands on
CENTRE's line. Writes S7-SHIP-<WALL>_1080.png and S7-SHIP_walls_preview.jpg (4680 wide, seams marked).

WHY: one horizon across the three walls is what makes three separate generations read as one ship at sea; the rest of
a seam is hidden by the set itself (the 25° fold and the 830 mm gap, STAGE.md).
"""
import argparse
import os

import cv2
import numpy as np


def horizon(img, edge=0.15):
    lum = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    h, w = lum.shape
    e = max(8, int(w * edge))
    side = np.concatenate([lum[:, :e], lum[:, -e:]], axis=1).mean(axis=1)
    g = np.abs(np.diff(cv2.GaussianBlur(side.reshape(-1, 1), (1, 9), 0).ravel()))
    return int(np.argmax(g[h // 8: h * 7 // 8])) + h // 8


def side_wall(img, cut, cut_side, hz_frac, out_w=1440, out_h=1080):
    h, w = img.shape[:2]
    keep = int(round(w * (1 - cut)))
    img = img[:, :keep] if cut_side == 'right' else img[:, w - keep:]
    crop_h = int(round(keep * out_h / out_w))
    if crop_h > h:                           # too short to keep the full width: narrow it instead
        crop_h, keep2 = h, int(round(h * out_w / out_h))
        img = img[:, :keep2] if cut_side == 'left' else img[:, img.shape[1] - keep2:]
        keep = keep2
    hz = horizon(img)
    y0 = int(round(hz - hz_frac * crop_h))
    y0 = min(max(y0, 0), h - crop_h)
    if abs((hz - y0) / crop_h - hz_frac) > 0.01:
        print(f'  note: horizon lands at {(hz - y0) / crop_h:.3f}, wanted {hz_frac:.3f} (plate too short to shift further)')
    return cv2.resize(img[y0:y0 + crop_h], (out_w, out_h), interpolation=cv2.INTER_AREA)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--centre', required=True); ap.add_argument('--left', required=True); ap.add_argument('--right', required=True)
    ap.add_argument('outdir')
    ap.add_argument('--cut-l', type=float, default=0.2); ap.add_argument('--cut-r', type=float, default=0.2)
    ap.add_argument('--hz-c', type=float, help='CENTRE horizon as a fraction of the height (overrides the measurement:\n'
                    'on a deck plate the detector can lock onto a grating edge instead of the sea line)')
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    c = cv2.imread(a.centre)
    s = 1080 / c.shape[0]
    c = cv2.resize(c, (int(round(c.shape[1] * s)), 1080), interpolation=cv2.INTER_AREA)
    x0 = (c.shape[1] - 1800) // 2
    c = c[:, x0:x0 + 1800]
    hz_frac = a.hz_c if a.hz_c else horizon(c) / 1080
    print(f'CENTRE horizon {hz_frac:.3f}')
    l = side_wall(cv2.imread(a.left), a.cut_l, 'right', hz_frac)      # LEFT faces CENTRE with its right edge
    r = side_wall(cv2.imread(a.right), a.cut_r, 'left', hz_frac)      # RIGHT faces CENTRE with its left edge
    for name, im in (('LEFT', l), ('CENTRE', c), ('RIGHT', r)):
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{name}_1080.png'), im)
    pv = np.concatenate([l, c, r], axis=1)
    for x in (1440, 3240):
        pv[:, x - 2:x + 2] = (0, 200, 255)
    pv[int(hz_frac * 1080), :, :] = (0, 0, 255)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_preview.jpg'), cv2.resize(pv, (2340, 540)), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print('written to', a.outdir)


if __name__ == '__main__':
    main()
