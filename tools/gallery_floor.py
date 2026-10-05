"""The Louvre gallery FLOOR (Scenes 1 + 10): the oak floor in the room's light, and the puddle as the script tells it.

Built 2026-10-05 (Homie: "we also need a floor version of it where the water puddle is… based on however the script
says it should be"). Follows docs/FLOOR-PLAN.md: floor as floor, top-down, orthographic, true scale, no pre-warp, the
mapping guy fits it; a 16:9 frame with the floor envelope 10,057 x 4,350 mm centred full width (top = upstage, the
CENTRE wall), soft fade outside the wedge between the flats; brightness capped below the walls; the floor never breaks.

THE PUDDLE, from the script (workshop draft V1, pp. 3-8):
  "a recent spill of water… AMINA… mopping the floor in front of… The Raft"   -> SPILL: an ordinary wet spill
  "The water disappears."                                                   -> VANISH: it dries away, rim inward
  "Then it mysteriously returns, glowing."                                    -> RETURN: it wells up from the centre, glowing
  (Martin seats the group away from it; the BLACKOUT; Sarah slips on it)    -> GLOW_LIT / GLOW_DARK loops
  Scene 10: "Light is suddenly restored"                                     -> DRY (no puddle)
THE WATER IS DRAWN, NOT GENERATED (2026-10-05): an NBP edit adding the spill redrew the planks around it (finding 4a),
so a dry/wet difference can't cut it out; the spill is a procedural shape (organic outline, droplets, a trickle along a
plank joint) rendered as thin water on the oak: meniscus rim, a thin highlight, a soft sheen of the laylight, a slight
darkening. That also makes the vanish (rim inward) and the return (from the centre) exact.
The glow is the sea-teal of the painting-melt render (Scene 2), so the puddle is the first drop of that sea.
The loops cycle cleanly (every motion is periodic over --loop seconds). Silent picture (scratch sound is the
sound designer's; Final Animations/Puddle/PUDDLE_audio.wav exists).

  python tools/gallery_floor.py --dry DRY.png --outdir DIR [--size 1920x1080] [--stills] [--clips]
Needs numpy, Pillow, opencv, ffmpeg.
"""
import argparse, os, subprocess
import numpy as np
from PIL import Image
import cv2

ENV_W, ENV_H = 10.057, 4.35          # floor envelope, metres (FLOOR-PLAN.md)
BACK_HALF = 3.0                      # CENTRE wall base, half-width (6.0 m)
FRONT_HALF = ENV_W / 2               # audience edge, half-width
TEAL = np.float32([0.16, 0.78, 0.70])  # the melt render's sea (sampled by eye from paintingMelt_1109)
# where each painting stands on the plan: (wall, from_m, to_m) along that wall's own width, as on the finished walls
PAINTINGS = [('L', 0.68, 1.87), ('L', 2.51, 4.12), ('C', 1.13, 5.01), ('R', 1.55, 3.06)]


def load(p):
    return np.asarray(Image.open(p).convert('RGB'), dtype=np.float32) / 255.0


def save(a, p):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p)


class Floor:
    def __init__(self, dry, size, pad_m=0.35, seed=4, wet_gain=1.0):
        self.W, self.H = size
        self.ppm = self.W / ENV_W
        self.eh = int(round(ENV_H * self.ppm))
        self.y0 = (self.H - self.eh) // 2
        yy, xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        self.x_m = (xx + 0.5) / self.ppm - ENV_W / 2       # metres from the centre line
        self.d_m = (yy + 0.5 - self.y0) / self.ppm          # metres downstage from the CENTRE wall
        self.rng = np.random.default_rng(seed)
        self.wet_gain = wet_gain             # the water's reflections (laylight panes, sheen, meniscus line); 1 = pale oak v1
        self.dry = self._fit(dry)
        self.wedge = self._wedge(pad_m)
        self.light = self._light()
        self.sd = self._puddle_sdf()          # metres: >0 inside the water, <0 outside
        self.depth = np.clip(self.sd, 0, None)
        self.waves = [(self.rng.uniform(0, 2 * np.pi), self.rng.uniform(26, 44), int(self.rng.integers(1, 3)) * self.rng.choice([-1, 1]),
                       self.rng.uniform(0, 2 * np.pi)) for _ in range(7)]

    def _fit(self, img):
        """Cover the envelope with the plate (top-down, true scale), flatten its generated lighting."""
        h, w = img.shape[:2]
        s = max(self.W / w, self.eh / h)
        r = cv2.resize(img, (int(round(w * s)), int(round(h * s))), interpolation=cv2.INTER_AREA)
        oy, ox = (r.shape[0] - self.eh) // 2, (r.shape[1] - self.W) // 2
        r = r[oy:oy + self.eh, ox:ox + self.W]
        flat = cv2.GaussianBlur(r, (0, 0), self.ppm * 0.8)
        r = r / (flat + 1e-4) * flat.reshape(-1, 3).mean(0)
        out = np.zeros((self.H, self.W, 3), np.float32)
        out[self.y0:self.y0 + self.eh] = r
        return out

    def _wedge(self, pad_m):
        """1 inside the floor between the flats' bases, soft to 0 within pad_m outside it."""
        half = BACK_HALF + (FRONT_HALF - BACK_HALF) * np.clip(self.d_m / ENV_H, 0, 1)
        side = half - np.abs(self.x_m)                     # >0 inside
        out_side = np.clip(1 + side / pad_m, 0, 1)
        out_back = np.clip(1 + self.d_m / pad_m, 0, 1)
        out_front = np.clip(1 + (ENV_H - self.d_m) / pad_m, 0, 1)
        m = out_side * out_back * out_front
        return (m * m * (3 - 2 * m))[..., None]

    def _wall_dist(self):
        half = BACK_HALF + (FRONT_HALF - BACK_HALF) * np.clip(self.d_m / ENV_H, 0, 1)
        cos = np.cos(np.radians(25))
        return {'C': np.maximum(self.d_m, 0), 'L': np.maximum((self.x_m + half) * cos, 0),
                'R': np.maximum((half - self.x_m) * cos, 0)}

    def _light(self, contact=0.12, contact_k=0.18, pool_k=(0.20, 0.15, 0.08), pool_reach=0.7):
        """The room's light on the floor: even laylight, contact shadow at every wall foot, warm spill under each painting."""
        dist = self._wall_dist()
        L = np.ones((self.H, self.W, 3), np.float32)
        for k in dist:
            L *= (1 - contact_k * np.exp(-dist[k] / contact))[..., None]
        # position along each wall (metres from that wall's left edge, as the wall files are laid out)
        half = BACK_HALF + (FRONT_HALF - BACK_HALF) * np.clip(self.d_m / ENV_H, 0, 1)
        flat_len = np.hypot(FRONT_HALF - BACK_HALF, ENV_H)
        along = {'C': self.x_m + BACK_HALF,
                 'L': (ENV_H - self.d_m) / ENV_H * flat_len,       # LEFT wall: its left edge is downstage
                 'R': self.d_m / ENV_H * flat_len}                 # RIGHT wall: its left edge is the corner
        pool = np.zeros((self.H, self.W), np.float32)
        for wall, a, b in PAINTINGS:
            u = along[wall]
            span = np.clip(np.minimum(u - a, b - u) / 0.35 + 0.5, 0, 1)
            pool = np.maximum(pool, span * np.exp(-dist[wall] / (pool_reach / 2)))
        L *= 1 + pool[..., None] * np.float32(pool_k)
        # the room's warm cast (the walls' plaster is warm; the flattened oak plate came out cool-grey)
        return L * np.float32([1.05, 1.0, 0.92])

    def _puddle_sdf(self, cx=0.0, cd=1.0, rx=0.78, ry=0.46):
        """An organic spill in front of the Raft: a wobbly pool, three droplets, a trickle down a plank joint."""
        th = np.arctan2((self.d_m - cd) / ry, (self.x_m - cx) / rx)
        wob = np.zeros_like(th)
        for k in range(2, 14):
            wob += self.rng.uniform(0.02, 0.07) / k ** 0.75 * np.cos(k * th + self.rng.uniform(0, 6.3))
        r = np.hypot((self.x_m - cx) / rx, (self.d_m - cd) / ry)
        inside = (r < 1 + wob).astype(np.uint8)
        for dx, dd, rx_, ry_ in [(-0.93, 1.28, 0.05, 0.035), (-0.84, 1.40, 0.025, 0.02), (0.90, 0.80, 0.03, 0.04),
                                 (0.34, 1.52, 0.02, 0.015), (-0.30, 1.55, 0.035, 0.022)]:
            inside[np.hypot((self.x_m - dx) / rx_, (self.d_m - dd) / ry_) < 1] = 1
        din = cv2.distanceTransform(inside, cv2.DIST_L2, 5) / self.ppm
        dout = cv2.distanceTransform(1 - inside, cv2.DIST_L2, 5) / self.ppm
        return cv2.GaussianBlur((din - dout).astype(np.float32), (0, 0), 1.0)

    def water(self, level, t=0.0, loop=10.0, s=None, ghost=None, thin=0.0):
        """level: metres the waterline has moved IN from the rim (0 = the full spill; grows to dry it away).
        s / ghost / thin: the dewetting vanish (see dewet()) passes its own waterline field, damp ghost and thinning.
        Returns (alpha, look-multiplier, look-add) for thin water on the lit oak."""
        if s is None:
            s = self.sd - level
        a = np.clip(s / 0.004 + 0.5, 0, 1)                         # the water's footprint, crisp
        rim = np.exp(-np.maximum(s, 0) / 0.010) * a                 # meniscus band just inside the edge
        ph = 2 * np.pi * t / loop
        shimmer = 0.5 + 0.5 * np.sin(14 * self.x_m + 9 * self.d_m + ph) * np.sin(-11 * self.x_m + 13 * self.d_m + 2 * ph)
        sheen = np.exp(-((self.x_m - 0.15) ** 2 / 0.20 + (self.d_m - 0.85) ** 2 / 0.06)) * (0.75 + 0.25 * shimmer)
        hl = np.exp(-np.abs(s - 0.006) / 0.0025) * a                # thin bright line on the meniscus
        # the laylight's panes mirrored in the water (soft: the water is thin and slightly rippled)
        pane = 1.2
        gx = np.abs(((self.x_m + 0.02 * shimmer) / pane) % 1 - 0.5) * 2
        gy = np.abs(((self.d_m + 0.3 + 0.02 * shimmer) / pane) % 1 - 0.5) * 2
        panes = np.clip((0.92 - np.maximum(gx, gy)) / 0.18, 0, 1)
        mul = 1 - a * 0.07 - rim * 0.28
        add = ((sheen * 0.08 + panes * 0.04) * a * (1 - 0.5 * thin) + hl * 0.12)[..., None] \
            * np.float32([0.97, 1.0, 1.03]) * self.wet_gain
        if ghost is None:
            damp = np.clip(1 - np.maximum(-s, 0) / 0.05, 0, 1) * (level > 0)   # a faint damp ghost where it has dried
            mul = mul - damp * (1 - a) * 0.04
        else:
            mul = mul - ghost * (1 - a) * 0.22                                  # wet wood, darker, drying off
        return a, mul[..., None], add

    def dewet(self, p, ghost_m=0.08):
        """THE VANISH, v2 (Homie 2026-10-05: the rim-inward vanish "looks like a cheap animation scaling back").
        Real thin water doesn't shrink evenly: it DEWETS. The outline frays where the film is thinnest, dry holes punch
        through the shallow middle, the pool breaks into islands, the last beads go, and the wood stays dark and damp
        for a moment where each part has just dried. p: 0 (the full spill, identical to SPILL) .. 1 (dry floor).
        Returns (s, ghost, thin) for water()."""
        if not hasattr(self, '_dw'):
            rng = np.random.default_rng(11)
            def field(sig_m):
                f = cv2.GaussianBlur(rng.standard_normal(self.sd.shape).astype(np.float32), (0, 0), self.ppm * sig_m)
                return f / (f.std() + 1e-6)
            n = 0.75 * field(0.20) + 0.45 * field(0.06)          # big shallow areas + a fine fray
            n = np.clip(n / 1.6, -1, 1)
            h = np.minimum(self.sd, 0.025) + 0.08 * (n + 1)      # the film's "height above drying": a flat spill is about
            #                                                       equally thin everywhere, so thin spots open all over at once
            self._dw = np.minimum(self.sd, h)                    # >= 0 inside the spill; at p = 0, s = this (= SPILL)
            self._dw_end = float(self._dw.max()) + ghost_m + 0.01
        thr = self._dw_end * p
        s = np.where(self.sd > 0, self._dw, self.sd) - thr     # the soft edge outside the outline dries too
        inside = np.clip(self.sd / 0.003 + 0.5, 0, 1)            # the spill's own footprint (the ghost lives there)
        dried = np.clip(thr - self._dw, 0, None)
        ghost = np.clip(1 - dried / ghost_m, 0, 1) * (thr > self._dw) * inside
        return s, ghost, p

    # ------------------------------------------------------------------ pictures
    def base(self, level=0.72):
        """Floor brightness capped below the walls (FLOOR-PLAN: mostly dark, capped)."""
        return level

    def lit(self, level=None, glow=0.0, t=0.0, loop=10.0, dark=False, dewet=None):
        """level: None = dry floor, else the waterline (see water()); glow 0..1; dark = the blackout.
        dewet: 0..1, the dewetting vanish instead of a level (see dewet())."""
        fl = self.dry
        img = fl * self.base() * (0.035 * np.float32([0.8, 0.9, 1.0]) if dark else self.light)
        if level is None and dewet is None:
            return np.clip(img, 0, 1) * self.wedge
        if dewet is not None:
            s, ghost, thin = self.dewet(dewet)
            level = 0.0
            a, mul, add = self.water(0.0, t, loop, s=s, ghost=ghost, thin=thin)
        else:
            a, mul, add = self.water(level, t, loop)
        img = img * mul + (0 if dark else add * self.base())
        if glow > 0:
            img = img + self._glow(t, loop, level) * glow * a[..., None]
            spill = cv2.GaussianBlur(a, (0, 0), self.ppm * 0.30)[..., None]
            img = img + spill * TEAL * (0.28 if dark else 0.08) * glow
        return np.clip(img, 0, 1) * self.wedge

    def _glow(self, t, loop, level=0.0):
        """Light from inside the water: an organic caustic web (7 random wave directions, periodic over `loop`),
        a brighter core, slow ripple rings from the middle, one breath per loop."""
        ph = 2 * np.pi * t / loop
        v = np.zeros_like(self.x_m)
        for ang, k, n, off in self.waves:
            v += np.cos(k * (np.cos(ang) * self.x_m + np.sin(ang) * self.d_m) + n * ph + off)
        web = np.clip(1 - np.abs(v) / 2.2, 0, 1) ** 5
        depth = np.clip(self.sd - level, 0, None)
        core = np.clip(depth / 0.30, 0, 1)
        r = np.hypot(self.x_m / 1.0, (self.d_m - 1.0) / 0.6)
        rings = 0.5 + 0.5 * np.cos(2 * np.pi * (r / 0.22) - 3 * ph)
        breathe = 0.88 + 0.12 * np.sin(ph)
        e = (0.30 + 0.30 * core + 0.40 * web * (0.6 + 0.4 * rings)) * breathe
        return e[..., None] * TEAL


def ease(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def write_clip(frames_fn, n, path, size, fps=24):
    W, H = size
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                          '-r', str(fps), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2',
                          '-pix_fmt', 'yuv422p10le', path], stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write((np.clip(frames_fn(i), 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    p.stdin.close()
    p.wait()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--size', default='1920x1080')
    ap.add_argument('--loop', type=float, default=10.0)
    ap.add_argument('--stills', action='store_true')
    ap.add_argument('--clips', action='store_true')
    ap.add_argument('--vanish', choices=['erode', 'dewet'], default='erode',
                    help='erode = v1 (the waterline moves in evenly); dewet = v2 (frays, holes, islands, a damp ghost)')
    ap.add_argument('--vanish-s', type=float, default=3.0, help='length of the vanish, seconds')
    ap.add_argument('--wet-gain', type=float, default=1.0,
                    help='strength of the water\'s reflections; 1 = pale oak v1. A dark floor shows water by its mirror of the laylight')
    a = ap.parse_args()
    size = tuple(map(int, a.size.split('x')))
    os.makedirs(a.outdir, exist_ok=True)
    F = Floor(load(a.dry), size, wet_gain=a.wet_gain)
    tag = f'{size[0]}x{size[1]}'
    if a.stills:
        save(F.lit(None), f'{a.outdir}/S1-GAL-FLOOR_DRY_{tag}.png')
        save(F.lit(0.0), f'{a.outdir}/S1-GAL-FLOOR_SPILL_{tag}.png')
        save(F.lit(0.0, glow=1.0), f'{a.outdir}/S1-GAL-FLOOR_GLOW-LIT_{tag}.png')
        save(F.lit(0.0, glow=1.0, dark=True), f'{a.outdir}/S1-GAL-FLOOR_GLOW-DARK_{tag}.png')
        print('stills written')
    if a.clips:
        fps, L = 24, a.loop
        n_loop = int(round(L * fps))
        deep = float(F.sd.max()) + 0.01
        nv = int(round(a.vanish_s * fps))
        def vanish(i):   # erode: it dries from the rim inward and is gone; dewet: it breaks up and dries off (v2)
            k = ease(i / (nv - 1))
            if a.vanish == 'dewet':
                return F.lit(dewet=i / (nv - 1), t=i / fps, loop=L)
            return F.lit(k * deep, t=i / fps, loop=L)
        def ret(i):      # 4 s: it wells up from the centre outward, glowing as it comes
            k = ease(i / (4 * fps - 1))
            return F.lit((1 - k) * deep, glow=ease(k * 1.4), t=i / fps, loop=L)
        jobs = [('SPILL_HOLD', lambda i: F.lit(0.0, t=i / fps, loop=L), n_loop),
                ('VANISH', vanish, nv),
                ('RETURN_GLOW', ret, 4 * fps),
                ('GLOW-LIT_LOOP', lambda i: F.lit(0.0, glow=1.0, t=(i + 4 * fps) / fps, loop=L), n_loop),
                ('GLOW-DARK_LOOP', lambda i: F.lit(0.0, glow=1.0, t=(i + 4 * fps) / fps, loop=L, dark=True), n_loop),
                ('DRY_HOLD', lambda i: F.lit(None), n_loop)]
        for name, fn, n in jobs:
            out = f'{a.outdir}/S1-GAL-FLOOR_{name}_{tag}.mov'
            write_clip(fn, n, out, size)
            print('wrote', out)


if __name__ == '__main__':
    main()
