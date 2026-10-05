"""Match a side wall's SKY and SEA to CENTRE's at the seam, row by row, so a light state reads as one sky (7 Oct 2026).

  python tools/ship_skymatch.py STATE_DIR OUTDIR --masks 5_layers/buildout_day [--strip 80] [--band 600]

STATE_DIR = a state set whose geometry continues across the seams (tools/ship_buildout.py walls + ship_states.py +
ship_seams.py --colour-only). CENTRE is copied untouched. For each SIDE wall, per row: the median Lab of the OPEN sky/sea
pixels (the day mask) in a STRIP px band on each side of the seam; rows with fewer than 12 such pixels are filled from
their neighbours; the difference CENTRE - side is smoothed down the rows (Gaussian, 61 rows) and added to the side's
sky/sea layer only, fading out with distance from the seam: exp(-d / BAND). The ship layer is not touched.
Writes the set, a preview and SKYMATCH_LOG.txt (the mean Lab step across each seam on sky/sea rows, before/after).

WHY: on SUNSET the side-wall edits glow hot at the edge facing CENTRE (the sun is in CENTRE; two prompt versions failed on
that defect, LOG 2026-10-07), so at each seam an orange side sky met CENTRE's dark mauve one. ship_seams.py's four zone
medians are too coarse at the horizon glow; a per-row GAIN on thin unmasked strips painted streaks (ropes, clouds).
Masked medians over a wider strip, heavily smoothed, follow the sky's real gradient without picking up the rigging.
"""
import argparse
import os

import cv2
import numpy as np

SPOT_W = 300     # px beside the seam over which a row's normal sky level is measured
SPOT_DL = 12.0   # L above the row's level that counts as glare
SPOT_BAND = 260.0  # px from the seam over which the glare clamp fades
SPOT_ROWS = 110    # rows either side of the horizon where the glare lives (the rail at the seam is ~170 rows below)
HZ_ROW = int(round(0.387 * 1080))


def row_median(lab, mask, cols, min_n=12):
    sub, m = lab[:, cols], mask[:, cols]
    out = np.full((lab.shape[0], 3), np.nan, np.float32)
    for y in range(lab.shape[0]):
        v = sub[y][m[y]]
        if len(v) >= min_n:
            out[y] = np.median(v, 0)
    idx = np.arange(len(out)); good = ~np.isnan(out[:, 0])
    for c in range(3):
        out[:, c] = np.interp(idx, idx[good], out[good, c])
    return out, good


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('state_dir'); ap.add_argument('outdir')
    ap.add_argument('--masks', required=True)
    ap.add_argument('--strip', type=int, default=80)
    ap.add_argument('--band', type=float, default=600.0)
    a = ap.parse_args()
    os.makedirs(a.outdir, exist_ok=True)
    img = {k: cv2.imread(os.path.join(a.state_dir, f'S7-SHIP-{k}_1080.png')) for k in ('LEFT', 'CENTRE', 'RIGHT')}
    msk = {k: cv2.imread(os.path.join(a.masks, f'S7-SHIP-{k}_1080_bgmask.png'), 0) > 127 for k in img}
    cl = cv2.cvtColor(img['CENTRE'], cv2.COLOR_BGR2LAB).astype(np.float32)
    log = [f'tools/ship_skymatch.py {a.state_dir} strip {a.strip} band {a.band}']
    for side in ('LEFT', 'RIGHT'):
        lab = cv2.cvtColor(img[side], cv2.COLOR_BGR2LAB).astype(np.float32)
        h, w = lab.shape[:2]
        scols = slice(w - a.strip, w) if side == 'LEFT' else slice(0, a.strip)
        ccols = slice(0, a.strip) if side == 'LEFT' else slice(1800 - a.strip, 1800)
        cm, cg = row_median(cl, msk['CENTRE'], ccols)
        sm, sg = row_median(lab, msk[side], scols)
        both = cg & sg
        off = cv2.GaussianBlur((cm - sm).reshape(-1, 1, 3), (1, 61), 0).reshape(-1, 3)
        off[:, 0] = np.clip(off[:, 0], -60, 30)
        xs = np.arange(w, dtype=np.float32)
        d = (w - 1 - xs) if side == 'LEFT' else xs
        wt = np.exp(-d / a.band)[None, :] * cv2.GaussianBlur(msk[side].astype(np.float32), (7, 7), 0)
        res = lab + off[:, None, :] * wt[..., None]
        # the hot spot (the side's sun glow): in the rows around the horizon only (HZ_ROW +- SPOT_ROWS, above the rail),
        # pixels near the seam that are much BRIGHTER than their row, or off its colour, are pulled to the row's own level
        # and colour (the row's median over the open sky/sea of the SPOT_W px beside the seam). Not limited to the mask:
        # the layer split leaves small sky pockets between the shrouds on the ship layer. Ropes are darker than the sky,
        # so the brightness test leaves them alone.
        sc2 = slice(w - SPOT_W, w) if side == 'LEFT' else slice(0, SPOT_W)
        rm, _ = row_median(res, msk[side], sc2)
        rm = cv2.GaussianBlur(rm.reshape(-1, 1, 3), (1, 31), 0).reshape(-1, 3)
        rows = np.zeros(h, np.float32)
        rows[max(0, HZ_ROW - SPOT_ROWS):HZ_ROW + SPOT_ROWS] = 1
        rows = cv2.GaussianBlur(rows.reshape(-1, 1), (1, 31), 0).ravel()
        ws = np.exp(-d / SPOT_BAND)[None, :] * rows[:, None]
        exc = np.maximum(res[..., 0] - rm[:, None, 0] - SPOT_DL, 0)
        cdev = np.linalg.norm(res[..., 1:] - rm[:, None, 1:], axis=2)
        bright = res[..., 0] > rm[:, None, 0] - 8                # sky-bright, not a rope
        k = np.clip(np.maximum(exc / 15.0, (cdev - 10) / 15.0), 0, 1) * bright * ws
        res[..., 0] -= exc * 0.9 * ws
        res[..., 1:] = res[..., 1:] * (1 - k[..., None]) + rm[:, None, 1:] * k[..., None]
        spot = int((k > 0.2).sum())
        before = float(np.abs(cm - sm)[both].mean())
        sm2, _ = row_median(res, msk[side], scols)
        after = float(np.abs(cm - sm2)[both].mean())
        log.append(f'{side}: sky/sea step at the seam (mean |dLab| over {both.sum()} rows) {before:.2f} -> {after:.2f}; '
                   f'hot-spot pixels pulled down {spot}')
        img[side] = cv2.cvtColor(np.clip(res, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    for k, im in img.items():
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{k}_1080.png'), im)
    pv = np.concatenate([img['LEFT'], img['CENTRE'], img['RIGHT']], axis=1)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_clean_2340.png'), cv2.resize(pv, (2340, 540), interpolation=cv2.INTER_AREA))
    for x in (1440, 3240):
        pv[:, x - 2:x + 2] = (0, 200, 255)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_preview.jpg'), cv2.resize(pv, (2340, 540)), [cv2.IMWRITE_JPEG_QUALITY, 88])
    with open(os.path.join(a.outdir, 'SKYMATCH_LOG.txt'), 'w') as fh:
        fh.write('\n'.join(log) + '\n')
    print('\n'.join(log))


if __name__ == '__main__':
    main()
