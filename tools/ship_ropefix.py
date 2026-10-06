"""Remove the rope ZIG-ZAG at the top of the ship's CENTRE wall (Homie, 7 Oct: "the ropes on top aren't aligned").

CAUSE: tools/ship_align.py warped each state onto the day wall and filled the missing top strip with the take reflected at
its edge (BORDER_REFLECT_101), so every SLANTED shroud folds back into a V at row K. Seen in NIGHT (K=34); MAGIC and SUNSET
are clean (checked 7 Oct); WRECK unchecked. The mast and the vertical ropes are unharmed by a mirror and are kept.

FIX (script, 0 cr): in the two shroud fans only (x < 450 and x > 1350 of CENTRE), rows 0..K+FEATHER are rebuilt from the
DAY wall's real ropes (day and night ropes measured within 2-4 px; a horizontal scale about the mast takes the residual
out), painted in the state's own rope colour (median of its rope pixels below K) over the state's own sky (the mirrored
ropes inpainted away). Joined over FEATHER rows inside the true part.
(Tried first, FAILED: carrying the state's ropes upward along their own slope smeared them and doubled the mast wrap.)

  python tools/ship_ropefix.py STATE.png DAY.png OUT.png K [--check CHECK.jpg]   # night (K=34): day ropes recoloured
  python tools/ship_ropefix.py STATE.png DAY.png OUT.png K --stretch             # wreck (K=13): see stretch()

STRETCH (wreck, 7 Oct): the day ropes did NOT line up rope for rope near the wreck's top (ghost stubs), so the wreck's OWN
true rows K..K+60 are spread up over rows 0..K+60 (quadratic map: s(0)=K, s(m)=m, s'(m)=1), fans only: the fold becomes
a slight bend, no join.
"""
import argparse

import cv2
import numpy as np

FEATHER = 16
FANS = ((0, 450), (1350, 1800))


def blackhat(img, k=31):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.float32)
    return cv2.morphologyEx(g, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))


def shift_at(day_bh, st_bh, y0, x0, x1):
    a = day_bh[y0:y0 + 20, x0:x1].mean(0); b = st_bh[y0:y0 + 20, x0:x1].mean(0)
    a = a - a.mean(); b = b - b.mean()
    return int(np.argmax(np.correlate(b, a, 'full')) - (len(a) - 1))


def fix(st, day, K):
    H, W = st.shape[:2]
    dbh, sbh = blackhat(day), blackhat(st)
    # horizontal scale about the mast (x ~ 900) from the fans' shifts just below K
    sl = shift_at(dbh, sbh, K + 10, 0, 400); sr = shift_at(dbh, sbh, K + 10, 1400, 1800)
    sx = 1.0 - (sl / 700.0 - sr / 700.0) / 2.0
    M = np.float32([[sx, 0, 900 * (1 - sx)], [0, 1, 0]])
    dayw = cv2.warpAffine(day, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    md = np.clip((blackhat(dayw, 21) - 12) / 14.0, 0, 1)                  # day ropes (thin dark lines only)
    ms = np.clip((sbh - 4) / 14.0, 0, 1)                                  # the state's own (mirrored) ropes
    Y = K + FEATHER
    # the sky above K: a smooth fit across the whole width (cubic in x per channel) to the clean sky in rows K..K+100
    # (rope pixels and their halo left out), carried straight up, + the open sky's own grain
    band = st[K:K + 100].astype(np.float32)
    bh = cv2.GaussianBlur(sbh[K:K + 100], (0, 0), 2); ok = cv2.erode((bh < np.percentile(bh, 50)).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    yy, xx = np.nonzero(ok); xs = np.arange(W)
    col = np.stack([np.polyval(np.polyfit(xx / W, band[yy, xx, c], 3), xs / W) for c in range(3)], 1)
    hp = (band - cv2.GaussianBlur(band, (0, 0), 3))[:, 450:1350][ok[:, 450:1350]]
    gs = float(1.4826 * np.median(np.abs(hp)))           # the open sky's grain (robust: stars ignored)
    sky = np.repeat(col[None], Y, 0) + np.random.default_rng(7).normal(0, gs, (Y, W, 1))
    below = st[K:K + 80].reshape(-1, 3); belm = ms[K:K + 80].ravel() > 0.6
    sel = below[belm]; rope = (sel[np.argsort(sel.sum(1))[:max(1, len(sel) // 10)]].mean(0).astype(np.float32) if belm.sum() > 50 else np.float32([20, 20, 20]))  # the darkest 10%
    a = md[:Y, :, None]
    new = sky * (1 - a) + rope * a
    out = st.astype(np.float32).copy()
    wy = np.ones(Y, np.float32); wy[K:Y] = np.linspace(1, 0, Y - K)        # 1 above K, fading out inside the true part
    wx = np.zeros(W, np.float32)
    for x0, x1 in FANS:
        wx[x0:x1] = 1
    wx = cv2.GaussianBlur(wx.reshape(1, -1), (0, 0), 20).ravel()
    w = (wy[:, None] * wx[None, :])[..., None]
    out[:Y] = out[:Y] * (1 - w) + new * w
    return np.clip(out, 0, 255).astype(np.uint8), (sl, sr, sx, rope)


def stretch(st, K, R=60):
    H, Wd = st.shape[:2]; m = K + R - 1
    c = K / m ** 2; b = 1 - 2 * K / m
    y = np.arange(m + 1, dtype=np.float32); s = K + b * y + c * y * y
    mapy = np.repeat(s[:, None], Wd, 1).astype(np.float32)
    mapx = np.repeat(np.arange(Wd, dtype=np.float32)[None, :], m + 1, 0)
    sm = cv2.remap(st, mapx, mapy, cv2.INTER_CUBIC).astype(np.float32)
    fan = np.zeros(Wd, np.float32)
    for x0, x1 in FANS:
        fan[x0:x1] = 1
    fan = cv2.GaussianBlur(fan.reshape(1, -1), (0, 0), 20).ravel()[None, :, None]
    out = st.astype(np.float32).copy(); out[:m + 1] = out[:m + 1] * (1 - fan) + sm * fan
    return np.clip(out, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('state'); ap.add_argument('day'); ap.add_argument('out')
    ap.add_argument('K', type=int); ap.add_argument('--check'); ap.add_argument('--stretch', action='store_true')
    a = ap.parse_args()
    st, day = cv2.imread(a.state), cv2.imread(a.day)
    if a.stretch:
        cv2.imwrite(a.out, stretch(st, a.K)); print('stretch K', a.K); return
    res, info = fix(st, day, a.K)
    cv2.imwrite(a.out, res)
    print('K', a.K, 'fan shifts L/R', info[0], info[1], 'sx %.4f' % info[2], 'rope bgr', info[3])
    if a.check:
        top = 2 * a.K + 140
        cv2.imwrite(a.check, np.vstack([st[:top], np.full((6, st.shape[1], 3), (0, 0, 255), np.uint8), res[:top]]))


if __name__ == '__main__':
    main()
