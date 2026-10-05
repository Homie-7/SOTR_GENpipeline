"""Split a generated ship-deck plate into two layers: the SHIP (hull, rails, mast, rigging) and the SEA + SKY behind it.

  python tools/ship_layers.py PLATE.png OUTDIR [--run 14] [--speck 400]

Writes OUTDIR/<stem>_ship.png (RGBA: the ship, alpha 0 where sea or sky shows), <stem>_bgmask.png (255 = sea/sky)
and <stem>_check.jpg (the sea/sky tinted green, for review).

WHY (2026-10-05, docs/PLAN-SHIP-INTRO.md "Designed for destruction"): the deck we land on is the ship that grinds,
tips, loses its foremast and comes apart into the raft. With the sea and sky on their own layer the horizon can tilt
behind a level ship ("tipped over on side", as it looks from on board), the sea can shallow and brighten over the
sandbank, the light can change per state, the rowboats sit on the sea, and the ship can break away to open sea.

HOW (tested on S7-SHIP-ROOM v1 take 82f8306c, 0 credits): a daylight plate's sky and sea are cool (blue > red) or
near-white cloud; the ship is warm (oak, red-ochre bulwarks, hemp) or dark (tarred rope, iron). Pixel class alone also
catches pale blue-grey deck planks, so a SPATIAL rule is added (see split()): the sky (above the horizon) joins the
top edge through a RUN px bridge over the rigging; the sea joins the sky through only 3 px, so a gap in a rail never
reaches the deck. (Earlier rules leaked deck planks on take 087f71a5 or lost the sky between the centre shrouds.) Every
shroud and ratline stays on the ship layer. Background islands smaller than SPECK px are dropped.
Daylight plates only: a dusk or night plate is split from its DAY parent's mask (the geometry is the same plate).
"""
import argparse
import os

import cv2
import numpy as np


def split(path, run=14, speck=400):
    bgr = cv2.imread(path, cv2.IMREAD_COLOR)
    im = bgr.astype(np.float32) / 255.0
    b, g, r = im[..., 0], im[..., 1], im[..., 2]
    h, w = b.shape
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    cls = (((b - r) > 0.02) & (lum > 0.22)) | ((lum > 0.72) & (np.abs(r - b) < 0.08))
    # 1. The horizon row: the strongest step in mean brightness down the outer 15% of the frame (open sea and sky).
    side = np.concatenate([lum[:, :w * 15 // 100], lum[:, -w * 15 // 100:]], axis=1).mean(axis=1)
    hz = int(np.argmax(np.abs(np.diff(cv2.GaussianBlur(side.reshape(-1, 1), (1, 9), 0).ravel()))[h // 8: h * 7 // 8])) + h // 8
    # 2. Seeds = SKY: class pixels above the horizon joined to the top edge through a RUN px bridge (crosses rigging).
    above = cls.copy(); above[hz:, :] = False
    k, lab = cv2.connectedComponents(cv2.dilate(above.astype(np.uint8), np.ones((run, run), np.uint8)), connectivity=4)
    top = np.unique(lab[0, :])
    seeds = above & np.isin(lab, top[top > 0])
    # 3. Grow from the sky into the sea through only a 3 px bridge: a gap in the rail never joins the deck planks.
    k, lab = cv2.connectedComponents(cv2.dilate(cls.astype(np.uint8), np.ones((3, 3), np.uint8)), connectivity=4)
    hit = np.unique(lab[seeds])
    m = (cls & (np.isin(lab, hit[hit > 0]) | seeds)).astype(np.uint8)
    k, lab, stats, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
    small = np.where(stats[:, cv2.CC_STAT_AREA] < speck)[0]
    m[np.isin(lab, small[small > 0])] = 0
    return bgr, m * 255


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plate')
    ap.add_argument('outdir')
    ap.add_argument('--run', type=int, default=14)
    ap.add_argument('--speck', type=int, default=400)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(a.plate))[0]
    bgr, m = split(a.plate, a.run, a.speck)
    rgba = cv2.cvtColor(bgr, cv2.COLOR_BGR2BGRA)
    rgba[..., 3] = 255 - m
    cv2.imwrite(os.path.join(a.outdir, stem + '_ship.png'), rgba)
    cv2.imwrite(os.path.join(a.outdir, stem + '_bgmask.png'), m)
    vis = bgr.copy()
    sel = m > 0
    vis[sel] = (vis[sel] * 0.25 + np.array([0, 255, 0]) * 0.75).astype(np.uint8)
    hh, ww = m.shape
    cv2.imwrite(os.path.join(a.outdir, stem + '_check.jpg'), cv2.resize(vis, (2000, int(2000 * hh / ww))),
                [cv2.IMWRITE_JPEG_QUALITY, 85])
    print(f'{stem}: sea/sky {m.mean() / 255:.1%} of the frame')


if __name__ == '__main__':
    main()
