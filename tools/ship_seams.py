"""Make the ship's three walls meet at both seams, for every light state, so the room reads as ONE scene.

  python tools/ship_seams.py STATE_DIR OUTDIR [--masks 5_layers/day] [--check]

STATE_DIR = an aligned state set (3_walls/assembled_<state>/, made by ship_states.py on the day geometry). CENTRE is the
anchor (it holds the mast, the sun and the moon) and is copied untouched. Each SIDE wall gets two corrections:

1. GEOMETRY (the same for every state, because every state sits on the day geometry): the bulwark rail meets CENTRE's
   rail at the seam. Measured on the day walls at 4x (2026-10-06): the rail-cap top at the seam is LEFT 519 / CENTRE 591
   and CENTRE 587 / RIGHT 476, so the sides are moved DOWN by 72 and 111 px at the seam. A vertical displacement field:
   dy = D * s(x) * w(y), s = smoothstep from the outer quarter of the wall (0) to the seam (1), w = smoothstep from the
   horizon (0, pinned at 0.387) to the side's own rail row at the seam (1) and 1 below. The sea between the horizon and the
   rail stretches; everything below moves rigidly; the outer edge never moves.
2. LIGHT (per state): row by row, the side's colour at the seam matches CENTRE's. In Lab, the per-row mean of a 48 px strip
   either side of the seam is measured separately on the SEA/SKY layer and the SHIP layer (the day masks, warped with the
   wall), smoothed down the rows; the side is shifted by (CENTRE - side) * f(x), f = 1 at the seam fading to 0 over
   --band px (default 700). So a sunset glow that pooled at a side wall's inner edge meets CENTRE's sky, and the bulwark
   planks meet in brightness.

Writes S7-SHIP-<WALL>_1080.png, a preview (seams yellow, horizon red) and SEAMS_LOG.txt (seam mismatch before/after:
mean Lab distance over the strips, sky and ship).

WHY (Homie, 2026-10-06, on the light-arc preview): "This is a complete cohesive single scene, so they all need to align…
while they are animated, it all looks like a single scene. At the moment your composite shows me they are not aligned."
The horizon was already one line; the rail stepped 72/111 px at the seams and the sunset sky jumped in brightness.
"""
import argparse
import os

import cv2
import numpy as np

HZ = 0.387
RAIL = {'LEFT': (519, 591), 'RIGHT': (476, 587)}   # (side's rail-cap top at the seam, CENTRE's), day geometry


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


CATHEAD = (432, 478, 0, 52, 56)   # RIGHT: rows, cols of the half cathead cut by the seam; sea copied from col 56 on


def clear_cathead(img, mask):
    """RIGHT's inner edge shows half a cathead (a beam + block jutting over the sea) cut by the seam: an object across a
    seam (CLAUDE.md: every object lives whole on one wall), and the rail warp stretched it into a white smear. It is
    replaced by the open sea right beside it (same rows), feathered; the mask marks it as sea."""
    y0, y1, x0, x1, sx = CATHEAD
    img = img.copy(); mask = mask.copy()
    src = img[y0:y1, sx:sx + (x1 - x0)].astype(np.float32)
    dst = img[y0:y1, x0:x1].astype(np.float32)
    a = np.ones((y1 - y0, x1 - x0), np.float32)
    a[:4] = np.linspace(0, 1, 4)[:, None]; a[:, -6:] *= np.linspace(1, 0, 6)[None, :]
    img[y0:y1, x0:x1] = (src * a[..., None] + dst * (1 - a[..., None])).astype(np.uint8)
    mask[y0:y1, x0:x1] = True
    return img, mask


def warp_side(img, wall, interp=cv2.INTER_LANCZOS4):
    """dest = src + D*s(x)*w(src): monotonic down every column, so it is inverted exactly per column (np.interp)."""
    h, w = img.shape[:2]
    side_y, c_y = RAIL[wall]
    D = c_y - side_y
    xs = np.arange(w, dtype=np.float32)
    s = smoothstep(0.25 * w, w - 1, xs) if wall == 'LEFT' else smoothstep(0.75 * w, 0, xs)
    src = np.arange(h, dtype=np.float32)
    wy = smoothstep(HZ * h, side_y, src)
    mapy = np.empty((h, w), np.float32)
    for x in range(w):
        dest = src + D * s[x] * wy
        mapy[:, x] = np.interp(src, dest, src)           # for each dest row, the src row that lands there
    mapx = np.tile(xs, (h, 1))
    return cv2.remap(img, mapx, mapy, interp, borderMode=cv2.BORDER_REPLICATE)


def row_means(lab, mask, cols):
    """Per-row mean Lab over `cols` where mask is set; rows with too few pixels are filled from neighbours."""
    sub, m = lab[:, cols], mask[:, cols]
    cnt = m.sum(1)
    tot = (sub * m[..., None]).sum(1)
    out = np.full((lab.shape[0], 3), np.nan, np.float32)
    ok = cnt >= 6
    out[ok] = tot[ok] / cnt[ok, None]
    idx = np.arange(len(out))
    for c in range(3):
        good = ~np.isnan(out[:, c])
        if good.sum() < 2:
            return None
        out[:, c] = np.interp(idx, idx[good], out[good, c])
    return cv2.GaussianBlur(out.reshape(-1, 1, 3), (1, 61), 0).reshape(-1, 3)


def zone_gain(side, c, side_m, c_m, side_cols, c_cols, lo=0.4, hi=2.0):
    """CENTRE/side RGB gain down the rows from FOUR robust zone medians (upper sky, lower sky, far sea, near sea), each taken
    over the OPEN sky/sea of a 600 px band beside the seam, linearly interpolated (log) between the zone centres. CENTRE's
    edge strips are dense with shrouds: per-row means there banded the sky and lit the sea from rope and rail-cap pixels."""
    h = side.shape[0]; hz = int(HZ * h)
    zones = ((0, hz // 2), (hz // 2, hz), (hz, hz + 70), (hz + 70, hz + 200))
    ys, gs = [], []
    for a, b in zones:
        ps = side[a:b, side_cols][side_m[a:b, side_cols]]
        pc = c[a:b, c_cols][c_m[a:b, c_cols]]
        if len(ps) < 200 or len(pc) < 200:
            continue
        gs.append(np.log(np.maximum(np.median(pc, 0), 1) / np.maximum(np.median(ps, 0), 1)))
        ys.append((a + b) / 2)
    out = np.ones((h, 3), np.float32)
    if len(ys) >= 1:
        ys, gs = np.array(ys), np.array(gs)
        for ch in range(3):
            out[:, ch] = np.exp(np.interp(np.arange(h), ys, gs[:, ch]))
    return np.clip(out, lo, hi)


def mismatch(side_lab, c_lab, side_m, c_m, side_cols, c_cols):
    """Seam mismatch as reported in SEAMS_LOG: mean Lab distance between zone MEDIANS of the side and CENTRE, over the 600 px
    band beside the seam: the four sky/sea zones of zone_gain(), and the ship below the horizon."""
    h = side_lab.shape[0]; hz = int(HZ * h)
    d = []
    for a, b in ((0, hz // 2), (hz // 2, hz), (hz, hz + 70), (hz + 70, hz + 200)):
        ps = side_lab[a:b, side_cols][side_m[a:b, side_cols]]; pc = c_lab[a:b, c_cols][c_m[a:b, c_cols]]
        if len(ps) > 200 and len(pc) > 200:
            d.append(np.abs(np.median(ps, 0) - np.median(pc, 0)).sum())
    ps = side_lab[hz:, side_cols][~side_m[hz:, side_cols]]; pc = c_lab[hz:, c_cols][~c_m[hz:, c_cols]]
    return [float(np.mean(d)) if d else float('nan'), float(np.abs(np.median(ps, 0) - np.median(pc, 0)).sum())]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('state_dir'); ap.add_argument('outdir')
    ap.add_argument('--masks', default=None, help='dir with the DAY walls\' _bgmask.png (default: ../../5_layers/day)')
    ap.add_argument('--band', type=int, default=700)
    ap.add_argument('--strip', type=int, default=140)
    ap.add_argument('--colour-only', action='store_true',
                    help='no rail warp, no cathead patch: for walls whose geometry already continues CENTRE '
                         '(tools/ship_buildout.py, 7 Oct); only the per-state light match at the seams')
    a = ap.parse_args()
    masks = a.masks or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(a.state_dir))), '5_layers', 'day')
    os.makedirs(a.outdir, exist_ok=True)
    img = {k: cv2.imread(os.path.join(a.state_dir, f'S7-SHIP-{k}_1080.png')) for k in ('LEFT', 'CENTRE', 'RIGHT')}
    msk = {k: cv2.imread(os.path.join(masks, f'S7-SHIP-{k}_1080_bgmask.png'), 0) > 127 for k in img}
    c_lab = cv2.cvtColor(img['CENTRE'], cv2.COLOR_BGR2LAB).astype(np.float32)
    S = a.strip
    log, out = [], {'CENTRE': img['CENTRE']}
    for wall in ('LEFT', 'RIGHT'):
        w = img[wall].shape[1]
        side_cols = slice(w - 600, w) if wall == 'LEFT' else slice(0, 600)
        c_cols = slice(0, 600) if wall == 'LEFT' else slice(1200, 1800)
        before = mismatch(cv2.cvtColor(img[wall], cv2.COLOR_BGR2LAB).astype(np.float32), c_lab, msk[wall], msk['CENTRE'],
                          side_cols, c_cols)
        if a.colour_only:
            wi, wm = img[wall], msk[wall]
        else:
            if wall == 'RIGHT':
                img[wall], msk[wall] = clear_cathead(img[wall], msk[wall])
            wi = warp_side(img[wall], wall)
            wm = warp_side(msk[wall].astype(np.uint8) * 255, wall, cv2.INTER_LINEAR) > 127
        xs = np.arange(w, dtype=np.float32)
        dist = (w - 1 - xs) if wall == 'LEFT' else xs
        f = (1 - smoothstep(0, a.band, dist))[None, :, None]
        res = wi.astype(np.float32)
        cimg = img['CENTRE'].astype(np.float32)
        soft_bg = cv2.GaussianBlur(wm.astype(np.float32), (7, 7), 0)[..., None]
        # SKY/SEA: per-row RGB gain (CENTRE / side) at the seam, smoothed down the rows, clamped, fading into the wall
        g = zone_gain(res, cimg, wm, msk['CENTRE'], side_cols, c_cols)
        lum = (g * np.array([0.114, 0.587, 0.299], np.float32)).sum(1, keepdims=True)   # BGR weights
        g = (lum * np.sqrt(g / lum))[:, None, :]   # brightness in full, colour shift halved (a dimmed sun glow went cyan)
        res = res * (1 + (g - 1) * f * soft_bg)
        # SHIP: one gain per channel over the whole seam strip (rows below the horizon), fading into the wall
        hzr = int(HZ * res.shape[0])
        sm_, cm_ = ~wm, ~msk['CENTRE']
        sm_[:hzr] = False; cm_[:hzr] = False
        a1 = res[:, side_cols][sm_[:, side_cols]].mean(0); b1 = cimg[:, c_cols][cm_[:, c_cols]].mean(0)
        g2 = np.clip(b1 / np.maximum(a1, 1), 0.75, 1.33)[None, None, :]
        res = res * (1 + (g2 - 1) * f * (1 - soft_bg))
        res = np.clip(res, 0, 255).astype(np.uint8)
        after = mismatch(cv2.cvtColor(res, cv2.COLOR_BGR2LAB).astype(np.float32), c_lab, wm, msk['CENTRE'], side_cols, c_cols)
        out[wall] = res
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{wall}_1080_bgmask.png'), wm.astype(np.uint8) * 255)
        log.append(f'{wall}: ' + ('colour only' if a.colour_only else f'rail {RAIL[wall][0]}->{RAIL[wall][1]} at the seam') + '; seam mismatch (Lab dist of zone medians, sky/sea | ship) '
                   f'before {before[0]:.1f} | {before[1]:.1f}  after {after[0]:.1f} | {after[1]:.1f}')
        print(log[-1])
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP-CENTRE_1080_bgmask.png'), msk['CENTRE'].astype(np.uint8) * 255)
    for k, im in out.items():
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{k}_1080.png'), im)
    pv = np.concatenate([out['LEFT'], out['CENTRE'], out['RIGHT']], axis=1)
    pv2 = pv.copy()
    for x in (1440, 3240):
        pv2[:, x - 2:x + 2] = (0, 200, 255)
    pv2[int(HZ * 1080), :, :] = (0, 0, 255)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_preview.jpg'), cv2.resize(pv2, (2340, 540)), [cv2.IMWRITE_JPEG_QUALITY, 88])
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_clean_2340.png'), cv2.resize(pv, (2340, 540), interpolation=cv2.INTER_AREA))
    with open(os.path.join(a.outdir, 'SEAMS_LOG.txt'), 'w') as fh:
        fh.write(f'tools/ship_seams.py {a.state_dir}' + (' --colour-only' if a.colour_only else '') + '\n' + '\n'.join(log) + '\n')


if __name__ == '__main__':
    main()
