"""The fragment edge, flowing ONE WAY for the whole file (replaces break_strip.py's ping-pong).

Built 2026-09-25 (Claude). WHY (Homie, on the v2 edge files): "the loops are running forward and
backward… it just looks like a cheap loop. We want this breaking/disintegration to just continue
throughout the video in a single way." He likes the LOOK of the generated breaks ("fantastic,
especially the studio"), so the look is kept and only the motion is rebuilt:

1. KIT (from the generated break clip and the clip it was edited from, no credits):
   - FOOTPRINT: the pixels the edit changed (as break_strip.py), limited to the breaking side.
   - FRONT: the broken wall edge and its cracks. The blocks move and the edge doesn't, so the
     per-pixel temporal median, with every pixel that is ever dark and restless set to the void,
     is the edge alone: the model's own ragged line and cracks, frozen, blocks removed.
   - SPRITES: the floating blocks themselves, cut out of several frames of the clip (islands of
     lit pixels in the void). Each keeps the model's own shading and thickness.
2. RENDER over a finished clean file:
   - the front replaces the footprint, lit every frame by the base (blur(base now) / blur(the lit
     reference)), so it dims with the snuff and warms with the reveal; pixels the edit never
     touched (the salon's left sconce) come from the base.
   - a CONVEYOR of blocks: each one slides out from behind the broken edge, drifts outward, turns
     slowly, recedes (shrinks and darkens) and is gone. Every block moves one way only, from its
     birth to its death; new ones keep coming, so the break never settles and never reverses.
     Blocks are lit by the base at the place they are now, so they also follow the room's light.
   - --period N makes the whole thing exactly periodic in N frames (spawn slots repeat), so a
     HOLD piece still loops seamlessly while every block moves one way (a waterfall loop).
   - --t0 sets where in the flow the file starts (in frames), so IN / HOLD / OUT pieces join.

  python tools/edge_flow.py kit BREAK.mp4 EDITED_FROM.mp4 KIT.npz --side left --max-x 0.24
  python tools/edge_flow.py render BASE.mov KIT.npz OUT.mov [--seconds 12] [--period 193 --t0 0]

The base is never modified; OUT is a separate effect file and refuses to overwrite. .mov = ProRes
422 HQ 10-bit with the base's audio copied; anything else = H.264 preview. Needs ffmpeg, numpy, OpenCV.
"""
import argparse
import json
import os
import subprocess

import cv2
import numpy as np

FPS = 24


def info(p):
    s = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height', '-of', 'json', p]))['streams'][0]
    return s['width'], s['height']


def read_all(p, w, h):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt',
                          'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114


# ---------------------------------------------------------------------------------------------- kit

def build_kit(a):
    W, H = a.size if a.size else info(a.brk)
    brk = read_all(a.brk, W, H)
    src = read_all(a.edited_from, W, H)
    n = len(brk)

    foot = np.zeros((H, W), np.uint8)
    for k in range(n):
        j = min(round(k * (len(src) - 1) / max(n - 1, 1)), len(src) - 1)
        d = np.abs(cv2.GaussianBlur(lum(brk[k].astype(np.float32)), (0, 0), 3) -
                   cv2.GaussianBlur(lum(src[j].astype(np.float32)), (0, 0), 3))
        foot |= (d > a.thresh).astype(np.uint8)
    if a.side == 'left':
        foot[:, int(a.max_x * W):] = 0
    else:
        foot[:, :int((1 - a.max_x) * W)] = 0
    foot = cv2.morphologyEx(foot, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15)))
    foot = cv2.dilate(foot, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    foot_all = foot.copy()  # before --protect: blocks are collected from the model's whole void
    if a.protect:
        x0, y0, x1, y1 = [float(v) for v in a.protect.split(',')]
        foot[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 0

    L = np.stack([lum(f.astype(np.float32)) for f in brk])
    med = np.median(brk, axis=0).astype(np.float32)
    mlum, lmin, lstd = lum(med), L.min(0), L.std(0)

    def void_of(fp):
        # the void: dark in the median, or ever dark and restless (a block passing through);
        # 'min': ever dark (blocks that move less than their own size, the studio)
        if a.void_rule == 'min':
            v = (lmin < a.void_lum) & (fp > 0)
        else:
            v = ((mlum < a.void_lum) | ((lmin < a.void_lum) & (lstd > a.restless))) & (fp > 0)
        v = cv2.morphologyEx(v.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        # cracks are thin void inside the wall: they stay part of the (opaque) front; only the big
        # void is where blocks may show. Keep the big void connected to the breaking frame edge.
        b = cv2.morphologyEx(v, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (a.crack_w, a.crack_w)))
        nlab, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
        keep = np.zeros_like(b)
        for i in range(1, nlab):
            x, y, w, h, area = st[i]
            if (a.side == 'left' and x <= 2) or (a.side == 'right' and x + w >= W - 2) or area > 0.02 * W * H:
                keep[lab == i] = 1
        return v, keep

    void, big = void_of(foot)
    _, big_all = void_of(foot_all)
    front = med * (1 - void[..., None])
    wall = 1 - cv2.GaussianBlur(big.astype(np.float32), (0, 0), 1.0)  # opaque wall incl. cracks

    # the front line per row: where the big void meets the wall
    fx = np.full(H, -1, np.int32)
    for y in range(H):
        xs = np.nonzero(big[y])[0]
        if len(xs):
            fx[y] = xs.max() if a.side == 'left' else xs.min()

    # sprites: lit islands inside the big void, from several frames
    sprites = []
    for k in np.linspace(0, n - 1, a.sprite_frames).round().astype(int):
        f = brk[k].astype(np.float32)
        # a block must sit wholly in the void (clear of the wall and of the void's own limits), or
        # it would carry a cut, straight side
        lit = ((lum(f) > a.block_lum) & (foot_all > 0)).astype(np.uint8)
        lit = cv2.morphologyEx(lit, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
        nl, lb, stt, cen = cv2.connectedComponentsWithStats(lit, 8)
        wall_near = cv2.dilate((big_all == 0).astype(np.uint8), np.ones((9, 9), np.uint8))
        for i in range(1, nl):
            x, y, w, h, area = stt[i]
            if area < a.min_area or x <= 1 or y <= 1 or x + w >= W - 1 or y + h >= H - 1:
                continue
            m = (lb[y:y + h, x:x + w] == i).astype(np.uint8)
            if (wall_near[y:y + h, x:x + w] * m).sum() > 0.04 * area:
                continue  # still attached to the edge: cut off, would show a straight side
            p = 4
            y0, y1, x0, x1 = max(y - p, 0), min(y + h + p, H), max(x - p, 0), min(x + w + p, W)
            mm = np.zeros((y1 - y0, x1 - x0), np.float32)
            mm[y - y0:y - y0 + h, x - x0:x - x0 + w] = m
            mm = cv2.dilate(mm, np.ones((3, 3), np.uint8))
            rgb = f[y0:y1, x0:x1]
            alpha = np.clip((lum(rgb) - 6) / 28, 0, 1) * cv2.GaussianBlur(mm, (0, 0), 0.8)
            sprites.append(dict(rgb=rgb.astype(np.float16), alpha=alpha.astype(np.float16),
                                cx=float(cen[i][0]), cy=float(cen[i][1]), w=int(w), h=int(h)))
    np.savez_compressed(a.kit, W=W, H=H, side=a.side, foot=foot, front=front.astype(np.float16),
                        wall=wall.astype(np.float16), fx=fx, ref=cv2.GaussianBlur(src.astype(np.float32).mean(0), (0, 0), W / 30),
                        sprites=np.array(sprites, dtype=object))
    print(f'kit {a.kit}: {W}x{H}, footprint {foot.mean():.3f}, void {big.mean():.3f}, '
          f'rows with a front {(fx >= 0).sum()}, {len(sprites)} sprites')


# ------------------------------------------------------------------------------------ court kit

def block_front(field, side, rng, depth=0.07, wander=0.035, cell=(58, 112), zone=0.16):
    """A Control-style broken edge built from the wall's own picture (the court's lit screen, whose
    generated take drew a hard straight edge): rows of blocks stepping in and out, a few blocks near
    the edge loosened (a dark gap round them, nudged outward), straight cracks running in along the
    block lines, a little shade on the wall at the break. Returns (front, wall alpha, fx, footprint)."""
    H, W = field.shape[:2]
    front = field.copy()
    wall = np.ones((H, W), np.float32)
    crack = np.ones((H, W), np.float32)
    fx = np.zeros(H, np.int32)
    ys, y = [], 0
    while y < H:
        h = int(rng.uniform(*cell))
        ys.append((y, min(y + h, H)))
        y += h
    d = depth * W
    rows = []
    for (y0, y1) in ys:
        d = np.clip(d + rng.normal(0, 0.45) * wander * W, (depth - wander) * W, (depth + wander) * W)
        rows.append((y0, y1, int(d)))
    for (y0, y1, dd) in rows:
        x_in = dd if side == 'left' else W - 1 - dd  # the wall's edge on this row
        fx[y0:y1] = x_in
        if side == 'left':
            wall[y0:y1, :dd] = 0
        else:
            wall[y0:y1, W - dd:] = 0
        # a crack along the row's top boundary, running in from the edge
        L = int(rng.uniform(25, 170))
        xa, xb = (dd, min(dd + L, W)) if side == 'left' else (max(W - dd - L, 0), W - dd)
        crack[max(y0 - 1, 0):y0 + 1, xa:xb] = 0.35
        # a loosened block at the edge: a gap round it, nudged out into the dark
        if rng.uniform() < 0.45:
            bw = int(rng.uniform(40, 95))
            by0, by1 = y0 + 3, y1 - 3
            nud = int(rng.uniform(4, 12))
            if side == 'left':
                bx0, bx1 = dd, dd + bw
                src = field[by0:by1, bx0:bx1]
                front[by0:by1, bx0 - nud:bx1 - nud] = src
                wall[by0:by1, bx0 - nud:bx0] = 1
                crack[by0 - 2:by0, bx0 - nud:bx1] = 0.2
                crack[by1:by1 + 2, bx0 - nud:bx1] = 0.2
                crack[by0:by1, bx1 - nud:bx1] = 0.12
            else:
                bx1, bx0 = W - dd, W - dd - bw
                src = field[by0:by1, bx0:bx1]
                front[by0:by1, bx0 + nud:bx1 + nud] = src
                wall[by0:by1, bx1:bx1 + nud] = 1
                crack[by0 - 2:by0, bx0:bx1 + nud] = 0.2
                crack[by1:by1 + 2, bx0:bx1 + nud] = 0.2
                crack[by0:by1, bx0:bx0 + nud] = 0.12
        # now and then a vertical crack along a block line
        if rng.uniform() < 0.35:
            cx = dd + int(rng.uniform(50, 140)) if side == 'left' else W - dd - int(rng.uniform(50, 140))
            crack[y0:y1, max(cx - 1, 0):cx + 1] = np.minimum(crack[y0:y1, max(cx - 1, 0):cx + 1], 0.4)
    crack = cv2.GaussianBlur(crack, (0, 0), 0.6)
    edge = cv2.GaussianBlur((1 - wall), (0, 0), 5)                 # shade on the wall at the break
    front = front * (crack * (1 - 0.35 * np.clip(edge * 2, 0, 1)))[..., None] * wall[..., None]
    foot = np.zeros((H, W), np.uint8)
    if side == 'left':
        foot[:, :int(zone * W)] = 1
    else:
        foot[:, W - int(zone * W):] = 1
    return front, wall, fx, foot


def court_sprites(brk, zones, lum_lo=38, min_area=1500, frames=5):
    """The generated cubes from the court's take, cut from the dark panels beside its (straight-edged)
    screen: islands above lum_lo in each zone. zones: {'left': (x0, x1), 'right': (x0, x1)}."""
    out = []
    n = len(brk)
    for k in np.linspace(0, n - 1, frames).round().astype(int):
        f = brk[k].astype(np.float32)
        L = lum(f)
        for sd, (zx0, zx1) in zones.items():
            m = np.zeros(L.shape, np.uint8)
            m[:, zx0:zx1] = (L[:, zx0:zx1] > lum_lo)
            m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
            nl, lb, st, cen = cv2.connectedComponentsWithStats(m, 8)
            for i in range(1, nl):
                x, y, w, h, area = st[i]
                if area < min_area or y <= 1 or y + h >= L.shape[0] - 1:
                    continue
                p = 4
                y0, y1, x0, x1 = max(y - p, 0), y + h + p, max(x - p, 0), x + w + p
                mm = (lb[y0:y1, x0:x1] == i).astype(np.float32)
                mm = cv2.dilate(mm, np.ones((3, 3), np.uint8))
                rgb = f[y0:y1, x0:x1]
                alpha = np.clip((lum(rgb) - 22) / 25, 0, 1) * cv2.GaussianBlur(mm, (0, 0), 0.8)
                out.append(dict(rgb=rgb.astype(np.float16), alpha=alpha.astype(np.float16), side=sd,
                                cx=float(cen[i][0]), cy=float(cen[i][1]), w=int(w), h=int(h)))
    return out


def build_court_kit(a):
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from render_court_v2 import field_static, OW, OH
    base, lamp = field_static()
    field = (base * lamp[..., None]) * 255.0      # the screen as lit on average (lamp_gain averages 1)
    rng = np.random.default_rng(a.seed)
    fl, wl, fxl, footl = block_front(field, 'left', rng, depth=a.depth, zone=a.zone)
    fr, wr, fxr, footr = block_front(field, 'right', rng, depth=a.depth, zone=a.zone)
    left = np.zeros((OH, OW, 1), np.float32)
    left[:, :OW // 2] = 1
    front = fl * left + fr * (1 - left)
    wall = wl * left[..., 0] + wr * (1 - left[..., 0])
    foot = np.maximum(footl, footr)
    brk = read_all(a.brk, OW, OH)
    zl, zr = [int(v) for v in a.zones.split(',')]
    sprites = court_sprites(brk, {'left': (0, zl), 'right': (zr, OW)})
    np.savez_compressed(a.kit, W=OW, H=OH, side='both', foot=foot, front=front.astype(np.float16),
                        wall=wall.astype(np.float16), fx_left=fxl, fx_right=fxr,
                        ref=cv2.GaussianBlur(field, (0, 0), OW / 30), sprites=np.array(sprites, dtype=object))
    print(f'court kit {a.kit}: {OW}x{OH}, {len(sprites)} sprites '
          f'({sum(s["side"] == "left" for s in sprites)} left), edge depth {fxl.mean() / OW:.3f} / {1 - fxr.mean() / OW:.3f}')


# ------------------------------------------------------------------------------ studio canvas chips

def build_chips(a):
    """Homie 2026-09-25: "shouldn't we make the painting frame fragment instead of just the wall behind
    it?… I want most of the painting canvas to be visible… a little bit of the canvas being chipped
    away, I don't mind." So the canvas's RIGHT edge chips too: small rectangular notches knocked out of
    the edge (deepest in the sky, shallow at the bottom, where the lying figure's drapery comes within
    ~30 px of the edge; the figures and the apex are 60 px+ inside and never touched), fine cracks in
    the paint at the notches, and pieces of the painted canvas drifting away with the plaster. The
    canvas wall stays LIVE (it shows the painting as it grows); the pieces are cut from the live
    picture too, so a chip always carries the paint that is there now."""
    kit = dict(np.load(a.kit, allow_pickle=True))
    W, H = int(kit['W']), int(kit['H'])
    rng = np.random.default_rng(a.seed)
    (tx, ty), (bx, by) = [float(v) for v in a.top.split(',')], [float(v) for v in a.bottom.split(',')]
    edge_x = lambda y: tx + (y - ty) * (bx - tx) / (by - ty)

    def max_depth(y):
        v = (y - ty) / (by - ty)
        if v < 0.12:
            return a.depth * 1.3            # the top corner
        if v < 0.45:
            return a.depth
        if v < 0.72:
            return a.depth * 0.58
        return a.depth * 0.29

    foot = kit['foot'].astype(np.uint8)
    wall = kit['wall'].astype(np.float32)
    front = kit['front'].astype(np.float32)
    fx = kit['fx'].copy()
    live = np.zeros((H, W), np.float32)
    crack = np.ones((H, W), np.float32)
    y = int(ty)
    notch = []
    while y < H:
        h = int(rng.uniform(18, 62))
        y1 = min(y + h, H)
        md = max_depth((y + y1) / 2)
        d = 0 if rng.uniform() < 0.18 else int(md * rng.uniform(0.2, 1.0))
        notch.append((y, y1, d))
        y = y1
    for (y0, y1, d) in notch:
        for yy in range(y0, y1):
            ex = int(round(edge_x(yy)))
            x0 = ex - int(max_depth(yy)) - 10           # the live zone: from inside the canvas to its edge,
            live[yy, x0 - 14:ex + 2] = 1                # starting before the footprint so its feathered
            foot[yy, x0:] = 1                           # edge blends the live picture, not the front
            wall[yy, x0 - 14:ex + 2] = 1
            if d:
                wall[yy, ex - d:] = 0                   # knocked out: the void shows
                front[yy, ex - d:] = 0
            fx[yy] = ex - d if d else min(fx[yy], ex + 2) if fx[yy] >= 0 else ex + 2
        if d:  # hairline cracks in the paint from the notch's inner corners
            for yc in (y0, y1 - 1):
                L = int(rng.uniform(8, 30))
                ex = int(round(edge_x(yc)))
                crack[max(yc - 1, 0):yc + 1, ex - d - L:ex - d] = 0.45
    crack = cv2.GaussianBlur(crack, (0, 0), 0.5)
    # cracks are applied to the live canvas through the wall alpha (it multiplies the live picture)
    wall_live = wall * np.where(live > 0, crack, 1.0)
    # pieces of painted canvas: cut from the band being chipped, drifting away with the plaster
    pieces = []
    for _ in range(a.pieces):
        yc = rng.uniform(ty + 10, H - 30)
        md = max_depth(yc)
        w, h = int(rng.uniform(14, max(16, md * 0.9))), int(rng.uniform(14, 48))
        ex = edge_x(yc)
        x0 = int(ex - md * rng.uniform(0.3, 1.0))
        y0 = int(yc - h / 2)
        x0, y0 = max(min(x0, int(ex) - w), 0), max(min(y0, H - h), 0)
        alpha = np.ones((h, w), np.float32)
        # a slightly broken outline, not a perfect rectangle
        for side_ in range(4):
            k = int(rng.uniform(0, 3))
            if k:
                if side_ == 0:
                    alpha[:k, :int(w * rng.uniform(0.2, 0.7))] = 0
                elif side_ == 1:
                    alpha[-k:, int(w * rng.uniform(0.3, 0.8)):] = 0
                elif side_ == 2:
                    alpha[int(h * rng.uniform(0.2, 0.7)):, :k] = 0
                else:
                    alpha[:int(h * rng.uniform(0.3, 0.8)), -k:] = 0
        alpha = cv2.GaussianBlur(alpha, (0, 0), 0.6)
        shade = np.ones((h, w), np.float32)
        shade[:, -3:] *= 0.45                    # the torn canvas's thickness, in shadow
        shade[-2:, :] *= 0.6
        pieces.append(dict(live=(x0, y0, x0 + w, y0 + h), alpha=alpha, shade=shade, side='right',
                           cx=float(x0 + w / 2), cy=float(y0 + h / 2), w=w, h=h))
    kit.update(foot=foot, wall=wall_live.astype(np.float16), front=front.astype(np.float16), fx=fx,
               live_wall=live.astype(np.float16), live_sprites=np.array(pieces, dtype=object))
    np.savez_compressed(a.out, **kit)
    print(f'chips kit {a.out}: {sum(1 for n in notch if n[2])} notches, {len(pieces)} canvas pieces, '
          f'deepest {max(n[2] for n in notch)} px')


# ------------------------------------------------------------------------------------------- render

class Flow:
    """A conveyor of blocks off one broken edge. Slot j is born at j*dt (+ jitter); its look and path
    come from slot j (or j mod slots when periodic), so the flow is deterministic and, with a period,
    exactly cyclic."""

    def __init__(self, a, W, H, side, fx, sprites, seed, count):
        self.a, self.W, self.H, self.side, self.fx = a, W, H, side, fx
        self.sprites = sprites
        self.rows = np.nonzero(fx >= 0)[0]
        self.seed = seed
        self.life = a.life * FPS
        self.dt = self.life / count  # frames between births: ~count blocks alive at once
        if a.period:
            self.slots = max(1, round(a.period / self.dt))
            self.dt = a.period / self.slots
        self.cache = {}

    def slot(self, j):
        key = j % self.slots if self.a.period else j
        if key in self.cache:
            return self.cache[key]
        r = np.random.default_rng([self.seed, key & 0xFFFFFFFF])
        sp = self.sprites[r.integers(len(self.sprites))]
        y = float(self.rows[r.integers(len(self.rows))])
        out = -1 if self.side == 'left' else 1
        s = dict(sp=sp, y=y, jit=r.uniform(-0.45, 0.45) * self.dt,
                 life=self.life * r.uniform(0.75, 1.25),
                 v=self.a.speed * r.uniform(0.6, 1.4) * out, vy=self.a.speed * r.uniform(-0.35, 0.35),
                 rot0=r.uniform(-12, 12) * sp.get('rot_ok', 1.0), vrot=r.uniform(-1, 1) * self.a.spin,
                 s0=r.uniform(0.8, 1.1), s_end=r.uniform(0.3, 0.55))
        if sp.get('live') is not None:  # a live piece is born where it was cut from
            s['y'] = sp['cy']
        if len(self.cache) > 4096:
            self.cache.clear()
        self.cache[key] = s
        return s

    def draw(self, img, gain_img, base, f, vis):
        """img: float RGB 0-255 (void already black where blocks may show); f: flow frame number."""
        W, H, a = self.W, self.H, self.a
        lo = int(np.floor((f - 1.3 * self.life) / self.dt)) - 1
        hi = int(np.floor(f / self.dt)) + 1
        alive = []
        for j in range(lo, hi + 1):
            s = self.slot(j)
            age = f - (j * self.dt + s['jit'])
            if 0 <= age < s['life']:
                alive.append((age / s['life'], s))
        # oldest (furthest back) first, so newer, nearer blocks cover them
        for u, s in sorted(alive, key=lambda t: -t[0]):
            sp = s['sp']
            live = sp.get('live')
            if live is not None:  # the face is the base as it is NOW at the place it was cut from
                lx0, ly0, lx1, ly1 = live
                rgb_src = base[ly0:ly1, lx0:lx1] * sp['shade'][..., None]
                lit = 1.0
            else:
                rgb_src = sp['rgb'].astype(np.float32)
            age_s = u * s['life'] / FPS
            # pulled out of the edge (velocity eases up from 0 over ~pull s), then gliding one way
            dist = s['v'] * (age_s - a.pull * (1 - np.exp(-age_s / a.pull)))
            scale = s['s0'] * (1 - (1 - s['s_end']) * u ** 1.1)
            x_edge = self.fx[int(s['y'])]
            # born just behind the broken edge (the wall hides it), then out into the dark
            x0_ = x_edge + (sp['w'] * a.hide * scale) * (1 if self.side == 'left' else -1)
            x = x0_ + dist
            y = s['y'] + s['vy'] * age_s
            ang = s['rot0'] + s['vrot'] * age_s
            hh, ww = rgb_src.shape[:2]
            M = cv2.getRotationMatrix2D((ww / 2, hh / 2), ang, scale)
            M[:, 2] += [x - ww / 2, y - hh / 2]
            ext = int(max(hh, ww) * scale * 0.75) + 3
            x0, x1, y0, y1 = max(int(x) - ext, 0), min(int(x) + ext, W), max(int(y) - ext, 0), min(int(y) + ext, H)
            if x1 <= x0 or y1 <= y0:
                continue
            M[:, 2] -= [x0, y0]
            rgb = cv2.warpAffine(rgb_src, M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
            al = cv2.warpAffine(sp['alpha'].astype(np.float32), M, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
            # light: the base's light where the block is now / where it was made; darker as it recedes
            if live is None:
                lit = gain_img[int(np.clip(y, 0, H - 1)), int(np.clip(x, 0, W - 1))] * a.layer_gain
            depth = (scale / s['s0']) ** a.depth_dark
            fade = min(1.0, (1 - u) / 0.12, age_s / a.fade_in)
            al = al * fade * vis[y0:y1, x0:x1]
            reg = img[y0:y1, x0:x1]
            reg[:] = reg * (1 - al[..., None]) + rgb * (lit * depth) * al[..., None]


class EdgeRenderer:
    """The break over one frame: the static front (lit by the frame), the live-wall zone, the flows."""

    def __init__(self, kit, a):
        self.a = a
        W, H = self.W, self.H = int(kit['W']), int(kit['H'])
        self.foot = kit['foot'].astype(np.float32)
        self.mask = cv2.GaussianBlur(self.foot, (0, 0), 4)[..., None]
        self.front = kit['front'].astype(np.float32)
        self.wall = kit['wall'].astype(np.float32)
        self.live = kit['live_wall'].astype(np.float32)[..., None] if 'live_wall' in kit else None
        self.ref = kit['ref'] + 2.0
        ramp = np.ones((H, 1), np.float32)
        f0 = int(H * (1 - a.floor_frac))
        if a.floor_frac > 0:
            ramp[f0:, 0] = np.linspace(1, 0, H - f0) ** 1.5
        self.ramp = ramp
        # where blocks may show: the void (not the wall, not outside the footprint), floor faded
        self.vis = ((1 - self.wall) * self.foot) * ramp
        side = str(kit['side'])
        sprites = list(kit['sprites'])
        live = list(kit['live_sprites']) if 'live_sprites' in kit else []
        self.flows = []
        for n, sd in enumerate(['left', 'right'] if side == 'both' else [side]):
            fx = kit['fx_' + sd] if side == 'both' else kit['fx']
            sps = [s for s in sprites if s.get('side', sd) == sd]
            self.flows.append(Flow(a, W, H, sd, fx, sps, a.seed + n, a.count))
            lv = [s for s in live if s.get('side', sd) == sd]
            if lv:
                self.flows.append(Flow(a, W, H, sd, fx, lv, a.seed + 100 + n, a.live_count))

    def frame(self, base, i):
        """base: float RGB 0-255, the clean picture; i: the flow frame. Returns the picture with the break."""
        a = self.a
        gain = np.clip((cv2.GaussianBlur(base, (0, 0), self.W / 30) + 2.0) / self.ref, 0, 1.5)
        layer = self.front * gain * a.front_gain
        if self.live is not None:  # the wall here is the live picture (the painted canvas), cut by the break
            layer = layer * (1 - self.live) + base * self.wall[..., None] * self.live
        layer = layer * self.ramp[..., None]
        for fl in self.flows:
            fl.draw(layer, gain, base, i, self.vis)
        return base * (1 - self.mask) + layer * self.mask


def smoke_layer(path, at, length, xmax, W, H, win=18):
    """The snuffed wicks' smoke, pulled out of the clean file (Homie 2026-09-25: the smoke vanished where
    the wall is broken, because the break shows a frozen copy of the wall and the dark). The wall behind
    is static and the smoke moves, so for each pixel the wall is the darkest value within +-win frames;
    smoke is what is brighter than that, high-passed so the snuff's own dimming is not taken for smoke.
    Returns {base frame: smoke RGB (H, xmax, 3)} for the frames of the snuff."""
    f0 = max(at - win, 0)
    n = length + 2 * win
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{f0 / FPS:.4f}', '-i', path, '-frames:v', str(n),
                          '-vf', f'crop={xmax}:{H}:0:0', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    B = np.frombuffer(raw, np.uint8).reshape(-1, H, xmax, 3).astype(np.float32)
    L = lum(B)
    tint = B[-1].reshape(-1, 3).mean(0)
    tint = tint / max(lum(tint[None])[0], 1e-3)          # the smoke takes the room's light colour
    out = {}
    for i in range(len(B)):
        lo, hi = max(0, i - win), min(len(B), i + win + 1)
        d = L[i] - L[lo:hi].min(0)
        d = d - cv2.GaussianBlur(d, (0, 0), 30)
        d = np.clip(d - 1.5, 0, None)                    # below this it is grain, not smoke
        if d.max() > 1:
            out[f0 + i] = (d[..., None] * tint[None, None]).astype(np.float32)
    return out


def render(a):
    kit = dict(np.load(a.kit, allow_pickle=True))
    W, H = info(a.base)
    assert (W, H) == (int(kit['W']), int(kit['H'])), 'kit and base sizes differ'
    if os.path.exists(a.out):
        raise SystemExit(f'refusing: {a.out} exists')
    er = EdgeRenderer(kit, a)
    smoke = {}
    if a.smoke_at is not None:
        xmax = (int(np.nonzero(kit['foot'].any(0))[0].max()) + 9) // 2 * 2   # even: 4:2:2 crops round
        smoke = smoke_layer(a.base, a.smoke_at, a.smoke_len, xmax, W, H)
        sm_mask = er.mask[:, :xmax] * (1 + 1.0 * (1 - er.wall[:, :xmax, None]))   # brighter against the dark
        print(f'smoke on {len(smoke)} frames')
    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '17', '-pix_fmt', 'yuv420p']
    cmd_in = ['ffmpeg', '-v', 'error']
    if a.start:
        cmd_in += ['-ss', str(a.start)]
    if a.loops > 1:
        cmd_in += ['-stream_loop', str(a.loops - 1)]
    cmd_in += ['-i', a.base]
    if a.seconds:
        cmd_in += ['-t', str(a.seconds)]
    rd = subprocess.Popen(cmd_in + ['-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'], stdout=subprocess.PIPE)
    aud = (['-ss', str(a.start)] if a.start else []) + (['-stream_loop', str(a.loops - 1)] if a.loops > 1 else [])
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-'] + aud + ['-i', a.base, '-map', '0:v', '-map', '1:a?', '-c:a', 'copy',
                          '-shortest'] + enc + [a.out], stdin=subprocess.PIPE)
    size = W * H * 6
    i = 0
    while True:
        buf = rd.stdout.read(size)
        if len(buf) < size:
            break
        base = np.frombuffer(buf, '<u2').reshape(H, W, 3).astype(np.float32) / 257.0
        out = er.frame(base, a.t0 + i)
        k = i + int(round(a.start * FPS))
        if k in smoke:
            sm = smoke[k]
            out[:, :sm.shape[1]] += sm * sm_mask
        wr.stdin.write((np.clip(out, 0, 255) * 257).astype('<u2').tobytes())
        i += 1
    wr.stdin.close()
    wr.wait()
    rd.wait()
    print(f'{i} frames -> {a.out}')


def flow_args(r):
    """The flow's settings (shared by the render command and render_court.py)."""
    r.add_argument('--t0', type=int, default=0, help='flow frame the file starts on (IN/HOLD/OUT joins)')
    r.add_argument('--period', type=int, help='make the flow exactly cyclic in this many frames (a HOLD loop)')
    r.add_argument('--seed', type=int, default=1819)
    r.add_argument('--count', type=float, default=50, help='blocks alive at once, about (per edge)')
    r.add_argument('--live-count', type=float, default=10, help='live pieces (cut from the picture) alive at once')
    r.add_argument('--life', type=float, default=32, help='seconds from leaving the edge to gone')
    r.add_argument('--speed', type=float, default=6.5, help='outward drift, px per second')
    r.add_argument('--spin', type=float, default=3, help='max turn, degrees per second')
    r.add_argument('--pull', type=float, default=3, help='seconds to ease out of the edge')
    r.add_argument('--hide', type=float, default=0.55, help='how far behind the edge a block is born, x its width')
    r.add_argument('--fade-in', type=float, default=1.5, help='seconds')
    r.add_argument('--depth-dark', type=float, default=0.6)
    r.add_argument('--layer-gain', type=float, default=1.0, help='block brightness (studio blocks came back ~3x the plaster)')
    r.add_argument('--front-gain', type=float, default=1.0)
    r.add_argument('--floor-frac', type=float, default=0.05)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    k = sub.add_parser('kit')
    k.add_argument('brk')
    k.add_argument('edited_from')
    k.add_argument('kit')
    k.add_argument('--side', choices=['left', 'right'], default='left')
    k.add_argument('--max-x', type=float, default=0.24)
    k.add_argument('--thresh', type=float, default=18)
    k.add_argument('--protect', help='x0,y0,x1,y1 fractions never taken from the break (the studio canvas)')
    k.add_argument('--size', type=int, nargs=2)
    k.add_argument('--void-lum', type=float, default=22)
    k.add_argument('--void-rule', choices=['median', 'min'], default='median')
    k.add_argument('--restless', type=float, default=10)
    k.add_argument('--crack-w', type=int, default=9, help='void thinner than this (px) is a crack, part of the wall')
    k.add_argument('--block-lum', type=float, default=26)
    k.add_argument('--min-area', type=int, default=140)
    k.add_argument('--sprite-frames', type=int, default=6)
    c = sub.add_parser('kit-court', help="the court: a block front built from its own screen + the take's cubes")
    c.add_argument('brk', help='the generated court break take (S9-CRT-BREAK)')
    c.add_argument('kit')
    c.add_argument('--seed', type=int, default=1817)
    c.add_argument('--depth', type=float, default=0.07, help='mean depth of the break each side (fraction of width)')
    c.add_argument('--zone', type=float, default=0.16, help='the band each side the break may use')
    c.add_argument('--zones', default='288,1512', help="x limits of the take's cube columns (at 1800 wide)")
    ch = sub.add_parser('chips', help='the studio: chip the canvas right edge too (live pieces of the painting)')
    ch.add_argument('kit', help='the studio kit')
    ch.add_argument('out')
    ch.add_argument('--top', default='1503,229', help="the canvas's top-right corner (x,y) in the 1664x1248 frame")
    ch.add_argument('--bottom', default='1525,1248', help="its bottom-right corner")
    ch.add_argument('--depth', type=float, default=55, help='deepest notch in the sky, px (less lower down)')
    ch.add_argument('--pieces', type=int, default=40)
    ch.add_argument('--seed', type=int, default=1819)
    r = sub.add_parser('render')
    r.add_argument('base')
    r.add_argument('kit')
    r.add_argument('out')
    r.add_argument('--start', type=float, default=0, help='preview: start this many seconds into the base')
    r.add_argument('--seconds', type=float, help='preview: render only this long')
    r.add_argument('--loops', type=int, default=1, help='play a seamless base (a HOLD loop) this many times')
    r.add_argument('--smoke-at', type=int, help='base frame where the snuff starts: carry its smoke over the break')
    r.add_argument('--smoke-len', type=int, default=120)
    flow_args(r)
    a = ap.parse_args()
    {'kit': build_kit, 'kit-court': build_court_kit, 'chips': build_chips, 'render': render}[a.cmd](a)


if __name__ == '__main__':
    main()
