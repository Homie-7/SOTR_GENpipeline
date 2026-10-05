"""Measure a generated puddle take (S1-GAL-PUDDLE-RETURN) before it goes near the comp.

Built 2026-10-05 for v4+ (the dark Versailles floor): Homie's beat is 2-3 drops, a pause, then the water wells up BY
ITSELF to the spill's size (~1.5 x 0.9 m) and stops. So the numbers that matter are: how many drops land, whether
there's a pause, whether the pool grows without impacts, how big it gets, and when it stops. Uses puddle_comp's own
waterline tracer (water_mask), so "the tracer finds it" is measured, not assumed.

Per frame (vs the take's own dry opening frames, as puddle_comp does):
  area_m2     the main pool (water_mask, the largest piece) in m^2, and its bounding box in metres
  any_m2      every wet pixel (beads included)
  drops       new wet blobs that appear away from existing water (an impact), counted with their times
  motion      mean |frame - previous| inside the frame (ripples, impacts): when it falls to grain the water lies still
Then: lock (phase correlation of the outer ring, frames 4 / middle / last vs frame 0, px), framing vs the reference
patch (ECC affine), and --sheet: 12 frames across the take with the traced waterline drawn, brightened x2 for dark oak.

  python tools/puddle_measure.py TAKE.mp4 --ref REF_PATCH.png --patch-geom patch_geom.json [--sheet OUT.jpg]
         [--csv OUT.csv] [--dry-frames 4]
"""
import argparse
import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puddle_comp as pc  # noqa: E402


def gray(a):
    return cv2.cvtColor(a.astype(np.float32), cv2.COLOR_RGB2GRAY)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('--ref', required=True)
    ap.add_argument('--patch-geom', required=True)
    ap.add_argument('--sheet')
    ap.add_argument('--csv')
    ap.add_argument('--dry-frames', type=int, default=4)
    a = ap.parse_args()

    geom = json.load(open(a.patch_geom))
    pw_m, ph_m = geom['patch_m']
    w, h, n = pc.probe(a.take)
    ppm = w / pw_m
    ref = cv2.cvtColor(cv2.imread(a.ref), cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
    ref = cv2.resize(ref, (w, h), interpolation=cv2.INTER_AREA)
    ring = np.ones((h, w), np.uint8)
    ring[int(h * .2):int(h * .8), int(w * .25):int(w * .75)] = 0
    hann = cv2.createHanningWindow((w, h), cv2.CV_32F)

    it = pc.frames(a.take, w, h)
    first = [next(it) for _ in range(a.dry_frames)]
    dry = np.mean(first, 0)
    f0 = gray(first[0])
    try:
        W = pc.align_warp(dry, ref)
        fr = f'ECC take->ref affine sx {W[0, 0]:.3f} sy {W[1, 1]:.3f} dx {W[0, 2]:+.1f} dy {W[1, 2]:+.1f} px'
    except cv2.error:
        fr = 'ECC found no match: the take REDREW the floor'
    print('probe', w, 'x', h, n, 'frames;', fr, flush=True)

    rows, prev, wet_prev, poolf = [], None, np.zeros((h, w), bool), np.zeros((h, w), np.float32)
    drops, lock, sheet_idx = [], {}, set(np.linspace(0, n - 1, 12).astype(int).tolist())
    sheet = []
    for i, f in enumerate(_chain(first, it)):
        ratio, thr = pc.noise_floor((f + 0.01) / (dry + 0.01), 0.03, 3, wet_prev)   # the same noise floor the comp uses
        lum = cv2.GaussianBlur(np.abs(ratio.mean(2) - 1), (0, 0), 3)
        wet = lum > thr
        wet = cv2.morphologyEx(wet.astype(np.uint8), cv2.MORPH_OPEN, np.ones((5, 5), np.uint8)).astype(bool)
        poolf = poolf * 0.7 + pc.water_mask(ratio, thr, 25) * 0.3
        pool = poolf > 0.5
        # a new blob far from any earlier water = an impact
        near = cv2.dilate(wet_prev.astype(np.uint8), np.ones((41, 41), np.uint8)).astype(bool)
        nb, lab, st, cen = cv2.connectedComponentsWithStats((wet & ~near).astype(np.uint8), 8)
        for k in range(1, nb):
            if st[k, cv2.CC_STAT_AREA] > 60 and i >= a.dry_frames:   # the dry frames define 'dry'; skip them
                drops.append((i / 24, cen[k][0] / ppm - pw_m / 2, cen[k][1] / ppm - ph_m / 2))
        wet_prev = wet_prev | wet
        g = gray(f)
        motion = float(np.abs(g - prev).mean()) if prev is not None else 0.0
        prev = g
        ys, xs = np.nonzero(pool)
        bw = (xs.max() - xs.min()) / ppm if len(xs) else 0
        bh = (ys.max() - ys.min()) / ppm if len(ys) else 0
        rows.append((i / 24, pool.sum() / ppm ** 2, wet.sum() / ppm ** 2, bw, bh, motion, thr))
        if i in (4, n // 2, n - 1):
            (dx, dy), _ = cv2.phaseCorrelate(f0 * ring * hann, g * ring * hann)
            lock[i] = (dx, dy)
        if a.sheet and i in sheet_idx:
            vis = cv2.cvtColor((np.clip(f * 2.0, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
            cnt, _ = cv2.findContours(pool.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cv2.drawContours(vis, cnt, -1, (0, 255, 255), 3)
            vis = cv2.resize(vis, (640, 360))
            cv2.putText(vis, f'{i / 24:.2f}s  pool {bw:.2f}x{bh:.2f} m', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, .6,
                        (0, 0, 255), 2)
            sheet.append(vis)

    print('lock (outer ring vs frame 0, px):', {k: (round(v[0], 2), round(v[1], 2)) for k, v in lock.items()})
    # merge impact detections within 3 frames of each other
    merged = []
    for t, x, y in drops:
        if not merged or t - merged[-1][0] > 0.15 or abs(x - merged[-1][1]) > 0.15:
            merged.append((t, x, y))
    print(f'impacts (new wet blobs away from earlier water): {len(merged)}')
    for t, x, y in merged:
        print(f'   {t:5.2f}s at x {x:+.2f} m, y {y:+.2f} m (from patch centre)')
    print(' t(s)  pool_m2  wet_m2   pool_w x h (m)  motion  thr')
    for r in rows[::6]:
        print(f'{r[0]:5.2f}  {r[1]:6.3f}  {r[2]:6.3f}   {r[3]:4.2f} x {r[4]:4.2f}     {r[5]:.4f}  {r[6]:.3f}')
    if a.csv:
        with open(a.csv, 'w') as fh:
            fh.write('t,pool_m2,wet_m2,pool_w,pool_h,motion,thr\n')
            fh.writelines(','.join(f'{v:.4f}' for v in r) + '\n' for r in rows)
    if a.sheet and sheet:
        while len(sheet) % 4:
            sheet.append(np.zeros_like(sheet[0]))
        cv2.imwrite(a.sheet, np.vstack([np.hstack(sheet[r:r + 4]) for r in range(0, len(sheet), 4)]))
        print('sheet ->', a.sheet)


def _chain(first, it):
    yield from first
    yield from it


if __name__ == '__main__':
    main()
