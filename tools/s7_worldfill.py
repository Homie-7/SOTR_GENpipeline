"""The ship's IDLE world layer must hold NO ship (Homie 8 Oct: "the ship's bow moves separately from the ship").

Two defects made ship pixels roll with the sea in tools/s7_idle.py v1:
1. the 5_layers bgmasks marked ship as sea/sky in places (the forecastle gun's barrel, holes in the furled sails, blocks,
   rope edges): those pixels showed the clip's rolling world, so the bow "moved";
2. the rolled world layer was the WHOLE clip frame, ship included: as it rolled (up to ~25 px at the wall ends) the clip's own
   yard, guns and rail slid into view through the mask, doubled beside the still ship.

  refine_mask(still, bg)  -> bg2 (uint8 255 = sea/sky): ship pixels inside the old mask found by colour against a smooth
                             sea/sky model (only near the ship), added to the ship, then the ship dilated by `grow` px.
  fill_world(img, hole, H) -> img with every hole pixel replaced by sea/sky: under the horizon the sea is copied SIDEWAYS
                             from open water in the same row (keeps the haze, wave scale and the clip's wave motion), else
                             mirrored from above; the sky by a push-pull (normalised pyramid) fill from sky only.

  python tools/s7_worldfill.py STATE      writes 5_layers/seamed_v2/<state>/S7-SHIP-<wall>_1080_bgmask_v2.png + _v2check.jpg
"""
import sys

import cv2
import numpy as np

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/'
WALLS = (('LEFT', 0, 1440), ('CENTRE', 1440, 3240), ('RIGHT', 3240, 4680))


def masked_blur(img, m, s):
    m = m.astype(np.float32)
    num = cv2.GaussianBlur(img * m[..., None], (0, 0), s)
    den = cv2.GaussianBlur(m, (0, 0), s)[..., None]
    return num / np.maximum(den, 1e-4), den[..., 0]


def horizon_row(still, bg, cols=None):
    """the sea/sky line, from the outer quarters of the panorama (mostly open sea and sky), or from the given columns"""
    g = cv2.cvtColor(still, cv2.COLOR_BGR2GRAY).astype(np.float32)
    cols = np.r_[0:700, 3980:4680] if cols is None else cols
    m = bg[:, cols] > 127
    prof = np.array([g[y, cols][m[y]].mean() if m[y].sum() > 50 else np.nan for y in range(g.shape[0])])
    prof = np.interp(np.arange(len(prof)), np.flatnonzero(~np.isnan(prof)), prof[~np.isnan(prof)])
    sm = cv2.GaussianBlur(prof.reshape(-1, 1).astype(np.float32), (1, 0), 2).ravel()
    d = np.abs(sm[4:] - sm[:-4])                     # a 4-row step: the sky/sea line, not the wave texture
    d[:150] = 0; d[700:] = 0
    return int(np.argmax(d)) + 2


def horizon_cols(still, bg, step=240, win=360):
    """the horizon row for every column (it is not level across the build-out): measured in windows, smoothed"""
    H0 = horizon_row(still, bg)
    xs, hs = [], []
    for x in range(0, 4680, step):
        c = np.arange(max(0, x - win // 2), min(4680, x + win // 2))
        band = bg[H0 - 40:H0 + 40][:, c] > 127
        if band.mean() < 0.35:
            continue
        hh = horizon_row(still, bg, c)
        if abs(hh - H0) < 30:
            xs.append(x); hs.append(hh)
    if len(xs) < 3:
        return H0, np.full(4680, H0, int)
    # the horizon is a straight line (possibly tilted across the build-out): robust line fit, outliers (moon glitter,
    # sails near the line) dropped
    xs, hs = np.array(xs, float), np.array(hs, float)
    keep = np.ones(len(xs), bool)
    for _ in range(3):
        a, b = np.polyfit(xs[keep], hs[keep], 1)
        r = np.abs(hs - (a * xs + b))
        keep = r < max(3.0, np.median(r[keep]) * 2.5)
    return H0, np.round(a * np.arange(4680) + b).astype(int)


def refine_mask(still, bg, near=48, near_sea=12, t_sky=14.0, t_sea=40.0, grow=2):
    """bg: uint8 255 = sea/sky (the old mask). Returns (bg2 uint8, horizon row)."""
    H, Hc = horizon_cols(still, bg)
    lab = cv2.cvtColor(still, cv2.COLOR_BGR2LAB).astype(np.float32)
    world = bg > 127
    # specks of "ship" alone in the open sea are mask noise: they would freeze bits of sea -> world
    n, cc, stt, _ = cv2.connectedComponentsWithStats((~world).astype(np.uint8), 8)
    rows = np.arange(bg.shape[0])[:, None]
    small = np.flatnonzero((stt[:, cv2.CC_STAT_AREA] < 40) & (stt[:, cv2.CC_STAT_TOP] > H + 8))
    world |= np.isin(cc, small[small > 0])
    ship = ~world
    dist = cv2.distanceTransform(world.astype(np.uint8), cv2.DIST_L2, 5)
    zone = world & (dist < near)
    # smooth sea/sky model from the world pixels only (robust: a first pass, then again without the outliers)
    sky_m = world & (rows < Hc[None, :] - 3)
    sea_m = world & (rows > Hc[None, :] + 3)
    flag = np.zeros_like(world)
    for m, t, s, darkonly, nz in ((sky_m, t_sky, 5, False, near), (sea_m, t_sea, 4, True, near_sea)):
        keep = m.copy()
        for _ in range(2):
            mod, den = masked_blur(lab, keep, s)
            dl = lab[..., 0] - mod[..., 0]
            dist_c = np.sqrt(((lab - mod) ** 2).sum(-1))
            out = (dist_c > t) & m
            if darkonly:                              # the sea's whitecaps are brighter; ship wood and iron are darker
                out &= dl < -t * 0.6
            keep = m & ~out
        flag |= out & zone & (dist < nz)
    flag &= np.abs(rows - Hc[None, :]) > 6             # the horizon line itself is what moves: never freeze it
    # a flagged speck only counts when it touches the ship or other flags (isolated sky noise / whitecaps stay world)
    n, lab_cc, stats, _ = cv2.connectedComponentsWithStats(flag.astype(np.uint8), 8)
    touch = cv2.dilate(ship.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    ok = np.zeros(n, bool)
    ok[np.unique(lab_cc[touch & flag])] = True
    ok[0] = False
    flag = ok[lab_cc]
    ship2 = ship | flag
    # close tiny world slivers (< 3 px wide) trapped inside the ship, then grow the ship a little
    ship2 = cv2.morphologyEx(ship2.astype(np.uint8), cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8)).astype(bool)
    if grow:
        ship2 = cv2.dilate(ship2.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * grow + 1,) * 2)).astype(bool)
    return np.where(ship2, 0, 255).astype(np.uint8), H, Hc


def pushpull(img, valid):
    """fill invalid pixels from valid ones by a normalised Gaussian pyramid (smooth, no seams)"""
    img = img.astype(np.float32); w = valid.astype(np.float32)
    levels = []
    I, W = img * w[..., None], w
    while min(W.shape) > 8:
        levels.append((I, W))
        I = cv2.pyrDown(I); W = cv2.pyrDown(W)
    est = I / np.maximum(W[..., None], 1e-6)
    for I, W in reversed(levels):
        up = cv2.resize(est, (W.shape[1], W.shape[0]), interpolation=cv2.INTER_LINEAR)
        a = np.clip(W * 4, 0, 1)[..., None]
        est = (I / np.maximum(W[..., None], 1e-6)) * a + up * (1 - a)
    return est


def fill_world(img, hole, H, margin=6, tile=96, min_run=24):
    """img HxWx3 (uint8/float), hole bool HxW, H horizon row (int, or one per column). Sea mirrored from above under the
    horizon, sky push-pull."""
    img = img.astype(np.float32)
    valid = ~hole
    h, w = hole.shape
    rows = np.arange(h)[:, None].repeat(w, 1)
    Hb = np.broadcast_to(np.asarray(H).reshape(1, -1) if np.ndim(H) else np.int64(H), (1, w))
    sky = rows < Hb                                  # sky holes from sky only, sea holes from sea only: no pale blur
    out = np.where(sky[..., None], pushpull(img, valid & sky), pushpull(img, valid & ~sky))   # where they meet
    top = Hb + margin
    sea_hole = hole & ~sky & (rows >= top)
    sea_ok = valid & ~sky & (rows >= top)
    # 1) the SEA is copied SIDEWAYS from the same row (same distance to the horizon = same haze and wave scale), translated
    #    from the nearer open water; a mirror (v2 test) copied the hazy band under the horizon downwards as a pale block
    best_d = np.full((h, w), 1 << 30, np.int64); best_x = np.zeros((h, w), np.int64)
    cols = np.arange(w)[None, :].repeat(h, 0)
    for flip in (False, True):
        V = sea_ok[:, ::-1] if flip else sea_ok
        lastc = np.maximum.accumulate(np.where(V, cols, -1), axis=1)
        run = np.zeros((h, w), np.int64); r = np.zeros(h, np.int64)
        for x in range(w):
            r = np.where(V[:, x], r + 1, 0); run[:, x] = r
        lc = np.clip(lastc, 0, w - 1)
        R = np.minimum(np.take_along_axis(run, lc, 1), tile)
        d = cols - lastc
        sx = lc - R + 1 + (d - 1) % np.maximum(R, 1)      # repeat the last `tile` px of open water, in order
        ok = (lastc >= 0) & (R >= min_run)
        if flip:
            sx, ok, d = (w - 1 - sx)[:, ::-1], ok[:, ::-1], d[:, ::-1]
        take = ok & (d < best_d)
        best_d = np.where(take, d, best_d); best_x = np.where(take, sx, best_x)
    side = sea_hole & (best_d < (1 << 30))
    out = np.where(side[..., None], np.take_along_axis(img, np.clip(best_x, 0, w - 1)[..., None].repeat(3, 2), 1), out)
    # 2) what has no open water in its row: mirrored from above (folded inside the sea strip), else the push-pull
    lastv = np.maximum.accumulate(np.where(valid, rows, -1), axis=0)
    S = lastv - top + 1
    d = rows - lastv
    Sp = np.maximum(S, 1)
    k = (d - 1) % (2 * Sp)
    srcc = np.clip(lastv - np.where(k < Sp, k, 2 * Sp - 1 - k), 0, h - 1)
    okm = sea_hole & ~side & (lastv >= top) & (S >= 4) & np.take_along_axis(valid, srcc, 0)
    out = np.where(okm[..., None], np.take_along_axis(img, srcc[..., None].repeat(3, 2), 0), out)
    return np.where(hole[..., None], out, img)


def main():
    st = sys.argv[1]
    still = np.hstack([cv2.imread(T + f'3_walls/seamed_v2/{st}/S7-SHIP-{x}_1080.png') for x, _, _ in WALLS])
    bg = np.hstack([cv2.imread(T + f'5_layers/seamed_v2/{st}/S7-SHIP-{x}_1080_bgmask.png', 0) for x, _, _ in WALLS])
    bg2, H, Hc = refine_mask(still, bg)
    added = (bg > 127) & (bg2 <= 127)
    print(f'{st}: horizon row {H} (columns {Hc.min()}..{Hc.max()}); ship grew by {added.sum()} px ({added.mean() * 100:.2f}% of the frame)')
    for x, a, b in WALLS:
        cv2.imwrite(T + f'5_layers/seamed_v2/{st}/S7-SHIP-{x}_1080_bgmask_v2.png', bg2[:, a:b])
    o = still.copy()
    o[bg2 > 127] = (o[bg2 > 127] * 0.55 + np.array([0, 0, 255]) * 0.45).astype(np.uint8)
    o[added] = (0, 255, 255)
    cv2.imwrite(T + f'5_layers/seamed_v2/{st}/S7-SHIP_1080_bgmask_v2check.jpg', o, [cv2.IMWRITE_JPEG_QUALITY, 92])


if __name__ == '__main__':
    main()
