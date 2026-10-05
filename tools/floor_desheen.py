"""Take the baked-in REFLECTIONS out of a generated top-down floor plate, so the floor carries only the room's own
light (gallery_floor.py adds it, from the same model as the walls).

WHY (2026-10-05, S1-GAL-FLOOR v2, the dark Versailles parquet): every NBP take came back with the laylight's sheen
baked in: a top-to-bottom falloff and, along the upstage edge, whole panels ~30% brighter than their neighbours
(take a650a2ac: top-row panels 0.30-0.32 against 0.23-0.25 everywhere else). gallery_floor.py's flatten (a divide by a
0.8 m blur) removes the falloff but not a panel-sized hot spot. Homie: "I'm just concerned that the reflections on the
floor might be problematic."
HOW: glare ADDS white light on top of the wood, so it is SUBTRACTED, not divided: after the same broad flatten, the
local level (a ~0.3 m blur of luminance) is compared with the floor's median; whatever sits above the median by more
than the natural panel-to-panel spread (--tol) is taken off equally from R, G and B. That keeps the lattice's own
contrast and the oak's colour; darker panels are never lifted. The generated source is never modified: this writes a
new plate that every tool (gallery_floor.py, puddle_comp.py, the Seedance patch) is then built from.

  python tools/floor_desheen.py PLATE.png OUT.png [--width-m 10.057] [--tol 0.06] [--report]
Needs numpy, Pillow, opencv.
"""
import argparse
import numpy as np
from PIL import Image
import cv2


def desheen(img, ppm, tol=0.06, local_m=0.3, broad_m=0.8):
    """img float RGB 0..1. Returns (out, excess) where excess is the subtracted luminance field."""
    flat = cv2.GaussianBlur(img, (0, 0), ppm * broad_m)
    img = img / (flat + 1e-4) * flat.reshape(-1, 3).mean(0)          # the broad falloff, as gallery_floor.py does
    lum = img.mean(2)
    local = cv2.GaussianBlur(lum, (0, 0), ppm * local_m)
    target = float(np.median(local))
    excess = np.clip(local - target * (1 + tol), 0, None)
    excess = cv2.GaussianBlur(excess, (0, 0), ppm * 0.1)             # no hard edge where the correction starts
    return np.clip(img - excess[..., None], 0, 1), excess


def cells(lum, ppm, nx=10, ny=4):
    h, w = lum.shape
    cy, cx = h / ny, w / nx
    return [[lum[int(r * cy):int((r + 1) * cy), int(c * cx):int((c + 1) * cx)].mean() for c in range(nx)] for r in range(ny)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plate')
    ap.add_argument('out')
    ap.add_argument('--width-m', type=float, default=10.057, help='metres the plate spans across (the floor envelope)')
    ap.add_argument('--tol', type=float, default=0.06, help='brightness above the median left alone (natural spread)')
    ap.add_argument('--report', action='store_true', help='print panel brightness before/after (~1 m cells)')
    a = ap.parse_args()
    img = np.asarray(Image.open(a.plate).convert('RGB'), dtype=np.float32) / 255.0
    ppm = img.shape[1] / a.width_m
    out, excess = desheen(img, ppm, a.tol)
    Image.fromarray((out * 255 + 0.5).astype(np.uint8)).save(a.out)
    if a.report:
        for name, im in (('before (flattened only)', desheen(img, ppm, tol=1e9)[0]), ('after', out)):
            print(name)
            for row in cells(im.mean(2), ppm):
                print('  ' + ' '.join('%.3f' % v for v in row))
        print('max subtracted %.3f, area touched %.1f%%' % (excess.max(), 100 * (excess > 0.005).mean()))
    print('wrote', a.out)


if __name__ == '__main__':
    main()
