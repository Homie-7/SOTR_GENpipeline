"""The court's fragment edge: the paper screen BURNING AWAY at both sides (edge effect v3, Homie 2026-09-25).

WHY: the torn-paper edge read as "paper shreds", and masonry blocks belong to the rooms (salon, studio),
not to a lit paper screen (Homie: the rooms break like concrete because they are physical spaces; the
court's screen is not). Paper disintegrates by burning, so the screen smoulders at its left and right
edges and flakes away as ash, ONE WAY, for the whole appearance: nothing ever comes back.

v2 of this module (same day, Homie: "still looks pretty fake and low-poly-ish"). What read as fake, and
what replaced it:
- a burn line that was a function of height only (a sawtooth edge, horizontal streaks in the scorch)
  -> the line is warped by 2D noise, so the edge is lacy and irregular at every scale;
- one uniform orange line -> real burnt-paper layering: brown scorch soaking into the paper, a black
  char band of varying width, a pale ash lip, and the glow in patches: hot spots that crawl along the
  edge, glowing veins inside the char;
- flat single-tone polygon flakes -> soft, textured, ragged flakes that tumble (their width swings as
  they turn), cooling from ember to grey; a few sparks rising with short trails;
- faint smoke rising out of the burn into the dark.

- THE BURN LINE creeps slowly inward and never retreats: about 5% of the width at the start of beat 3,
  about 9% at the end of beat 7 (the three appearances share one timeline via --t0, so beat 5 starts
  where beat 3 stopped). A pixel that has burned stays burned.
- The judge is laid over this by render_court.py, so he never burns (LOOK D7/D15). The impact shudder
  moves everything together.

Used by: python tools/render_court.py OUT.mov --beat 3 --scrim --burn [--t0 FRAMES]
"""
import cv2
import numpy as np

FPS = 24
TOTAL = 3864          # frames across beats 3 + 5 + 7 (960 + 2424 + 480): the burn's whole run
BEAT_T0 = {3: 0, 5: 960, 7: 3384}
EMBER = np.array([1.0, 0.42, 0.10], np.float32)
EMBER_HOT = np.array([1.0, 0.78, 0.40], np.float32)
BROWN = np.array([0.50, 0.30, 0.14], np.float32)


def _noise1d(n, rng, octaves=((1, 1.0), (2, 0.6), (4, 0.35), (9, 0.18), (23, 0.08))):
    y = np.linspace(0, 1, n)
    out = np.zeros(n)
    for f, amp in octaves:
        out += amp * np.sin(2 * np.pi * (f * y + rng.uniform())) + amp * 0.5 * np.sin(2 * np.pi * (f * 1.7 * y + rng.uniform()))
    return out / np.abs(out).max()


def fractal(h, w, rng, scales=(160, 64, 24, 9, 4), gains=(1.0, 0.55, 0.3, 0.16, 0.08)):
    """Smooth 2D fractal noise in about -1..1 (bicubic-upsampled random grids)."""
    out = np.zeros((h, w), np.float32)
    for s, g in zip(scales, gains):
        gh, gw = max(2, int(np.ceil(h / s)) + 2), max(2, int(np.ceil(w / s)) + 2)
        grid = rng.normal(0, 1, (gh, gw)).astype(np.float32)
        up = cv2.resize(grid, ((gw - 1) * s, (gh - 1) * s), interpolation=cv2.INTER_CUBIC)[:h, :w]
        out += g * up
    return out / (np.abs(out).max() + 1e-6)


class BurnEdges:
    def __init__(self, W, H, d0=0.05, d1=0.09, seed=1817, flakes=120, sparks=30, band=0.2):
        self.W, self.H = W, H
        rng = np.random.default_rng(seed)
        self.d0, self.d1 = d0 * W, d1 * W
        self.bw = bw = int(band * W)
        self.shape, self.creep, self.warp, self.wmod, self.fib = {}, {}, {}, {}, {}
        for s in ('left', 'right'):
            self.shape[s] = _noise1d(H, rng)
            self.creep[s] = np.clip(_noise1d(H, rng) * 0.5 + 0.5, 0, 1)
            # the edge's own shape at every scale, fixed in the PAPER, so the advancing line eats into it
            self.warp[s] = 13 * fractal(H, bw, rng) + 3.5 * fractal(H, bw, rng, scales=(6, 3, 2), gains=(1, 0.6, 0.4))
            self.wmod[s] = fractal(H, bw, rng) * 0.5 + 0.5            # char and scorch widths vary
            self.fib[s] = fractal(H, bw, rng, scales=(5, 2), gains=(1, 0.7))
        # moving fields, tall so they can scroll: hot spots crawl along the edge; smoke rises
        self.hot = {s: fractal(3 * H, bw, rng, scales=(70, 28, 10), gains=(1, 0.6, 0.35)) for s in ('left', 'right')}
        self.smoke = {s: fractal(3 * H, bw, rng, scales=(90, 40, 16), gains=(1, 0.5, 0.25)) for s in ('left', 'right')}
        self.xs = np.arange(bw, dtype=np.float32)[None, :]
        self.flakes, self.sparks, self.seed = flakes, sparks, seed
        self.life, self.slife = 7 * FPS, 1.6 * FPS
        self.dt, self.sdt = self.life / flakes, self.slife / sparks
        self.cache, self.scache = {}, {}
        self.grain = fractal(64, 64, rng, scales=(6, 3), gains=(1, 0.6)) * 0.5 + 0.5

    def line(self, side, t):
        """Burn depth (px from the frame edge) per row at flow frame t. Non-decreasing in t."""
        k = np.clip(t / TOTAL, 0, 1)
        D = self.d0 + (self.d1 - self.d0) * k
        return D * (1 + 0.32 * self.shape[side]) + 14 * self.creep[side] * k

    # ------------------------------------------------------------------ ash and sparks
    def _flake(self, j):
        if j in self.cache:
            return self.cache[j]
        r = np.random.default_rng([self.seed, j & 0xFFFFFFFF])
        k = int(r.integers(9, 15))
        ang = np.sort(r.uniform(0, 2 * np.pi, k))
        size = r.uniform(2.5, 11) * (1.8 if r.uniform() < 0.12 else 1.0)
        rad = size * np.clip(r.normal(1, 0.28, k), 0.35, 1.5)
        poly = np.stack([np.cos(ang) * rad, np.sin(ang) * rad * r.uniform(0.5, 1.0)], 1)
        s = dict(side='left' if r.uniform() < 0.5 else 'right', y=r.uniform(0, self.H), poly=poly, size=size,
                 jit=r.uniform(-0.5, 0.5) * self.dt, life=self.life * r.uniform(0.6, 1.3),
                 vx=r.uniform(6, 22), vy=-r.uniform(5, 18), spin=r.uniform(-2.2, 2.2), tumble=r.uniform(0.6, 2.5),
                 wob=r.uniform(2, 8), wf=r.uniform(0.25, 0.8), ph=r.uniform(0, 6.3),
                 hot=r.uniform(0.3, 1.8), grey=r.uniform(0.16, 0.36), gx=int(r.integers(0, 40)), gy=int(r.integers(0, 40)))
        if len(self.cache) > 8192:
            self.cache.clear()
        self.cache[j] = s
        return s

    def _spark(self, j):
        if j in self.scache:
            return self.scache[j]
        r = np.random.default_rng([self.seed + 7, j & 0xFFFFFFFF])
        s = dict(side='left' if r.uniform() < 0.5 else 'right', y=r.uniform(0, self.H),
                 jit=r.uniform(-0.5, 0.5) * self.sdt, life=self.slife * r.uniform(0.5, 1.4),
                 vx=r.uniform(15, 50), vy=-r.uniform(40, 110), curve=r.uniform(-20, 20), b=r.uniform(0.5, 1.0))
        if len(self.scache) > 8192:
            self.scache.clear()
        self.scache[j] = s
        return s

    def _alive(self, t, dt, life, get):
        lo = int(np.floor((t - 1.4 * life) / dt)) - 1
        for j in range(lo, int(np.floor(t / dt)) + 2):
            s = get(j)
            age = t - (j * dt + s['jit'])
            if 0 <= age < s['life']:
                yield s, age

    # ------------------------------------------------------------------ one frame
    def frame(self, lit, t):
        """lit: the lit screen (H, W, 3, 0..1). Returns it burning at flow frame t."""
        W, H, bw = self.W, self.H, self.bw
        out = lit.copy()
        light = np.zeros((H, W, 3), np.float32)          # emitted light (embers), added at the end
        for side in ('left', 'right'):
            sl = np.s_[:, :bw] if side == 'left' else np.s_[:, W - bw:]
            flip = (lambda a: a) if side == 'left' else (lambda a: a[:, ::-1])
            v = self.xs - self.line(side, t).astype(np.float32)[:, None] + self.warp[side]   # px into the paper
            wm = self.wmod[side]
            charw = 3 + 9 * wm
            alive = np.clip((v + 0.8) / 1.6, 0, 1)
            char = 1 - np.clip(v / charw, 0, 1) ** 0.7                                      # black crust
            scorch = np.exp(-np.clip(v, 0, None) / (14 + 34 * wm)) * (0.75 + 0.25 * self.fib[side])
            lip = np.exp(-np.clip(v, 0, None) / 1.3) * (0.45 + 0.55 * np.clip(self.fib[side] + 0.4, 0, 1)) * alive
            paper = flip(out[sl])
            lum_p = paper.mean(-1, keepdims=True)
            col = paper * (1 - 0.7 * scorch[..., None]) + BROWN * 1.25 * lum_p * 0.7 * scorch[..., None]   # scorched brown
            col = col * (1 - 0.93 * char[..., None]) + 0.02 * char[..., None]
            col = col + lip[..., None] * 0.10 * np.array([0.9, 0.88, 0.85], np.float32)   # pale ash on the lip
            out[sl] = flip(col * alive[..., None])
            # glow: hot spots crawling along the edge, flickering; veins inside the char
            sc = int(t * 1.7) % H
            hot = self.hot[side][H - sc:2 * H - sc]
            flick = 0.8 + 0.2 * np.sin(t * 0.7 + self.fib[side] * 6)
            heat = np.clip((hot + 0.15) * 1.6, 0, 1) ** 1.5 * flick
            rim = np.exp(-np.abs(v - 0.6) / 1.5) * (0.38 + 0.9 * heat)      # a thin glow all along, hotter in patches
            veins = char * alive * np.clip((hot - 0.35) * 3, 0, 1) * 0.55 * (0.5 + 0.5 * self.fib[side])
            g = np.clip(rim + veins, 0, 1.6)[..., None]
            emit = g * EMBER + np.clip(g - 0.8, 0, None) * (EMBER_HOT - EMBER) * 1.2
            # smoke: faint, rising out of the burn into the dark, thinning as it goes
            ss = int(t * 1.1) % H
            smk = np.clip(self.smoke[side][ss:ss + H] * 0.8 + 0.25, 0, 1)
            smk = smk * np.exp(-np.clip(-v, 0, None) / 55) * (v < 4) * 0.075
            emit = emit + smk[..., None] * np.array([0.62, 0.58, 0.54], np.float32)
            light[sl] = flip(emit)
        # ash flakes: soft, textured, tumbling; hot when they leave the edge, grey as they cool
        lines = {s: self.line(s, t) for s in ('left', 'right')}
        ash_a = np.zeros((H, W), np.float32)
        ash_c = np.zeros((H, W), np.float32)
        for s, age in self._alive(t, self.dt, self.life, self._flake):
            a_s, u = age / FPS, age / s['life']
            y0 = int(np.clip(s['y'], 0, H - 1))
            dx = s['vx'] * a_s + s['wob'] * np.sin(2 * np.pi * s['wf'] * a_s + s['ph'])
            x = lines[s['side']][y0] - dx if s['side'] == 'left' else W - 1 - lines[s['side']][y0] + dx
            y = s['y'] + s['vy'] * a_s
            th = s['spin'] * a_s
            R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
            turn = 0.25 + 0.75 * abs(np.cos(s['tumble'] * a_s + s['ph']))           # its width swings as it tumbles
            pts = s['poly'] * [turn, 1] @ R.T * (1 - 0.3 * u) + [x, y]
            x0, y0b = int(pts[:, 0].min()) - 3, int(pts[:, 1].min()) - 3
            x1, y1b = int(pts[:, 0].max()) + 4, int(pts[:, 1].max()) + 4
            if x1 <= 0 or y1b <= 0 or x0 >= W or y0b >= H:
                continue
            m = np.zeros((y1b - y0b, x1 - x0), np.uint8)
            cv2.fillPoly(m, [np.round((pts - [x0, y0b]) * 4).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=2)
            m = cv2.GaussianBlur(m.astype(np.float32) / 255, (0, 0), 0.7)
            gy, gx = s['gy'], s['gx']
            tex = cv2.resize(self.grain[gy:gy + 24, gx:gx + 24], m.shape[::-1])
            fade = min(1.0, (1 - u) / 0.3, a_s / 0.25)
            cx0, cy0, cx1, cy1 = max(x0, 0), max(y0b, 0), min(x1, W), min(y1b, H)
            mm = m[cy0 - y0b:cy1 - y0b, cx0 - x0:cx1 - x0] * fade
            tt = tex[cy0 - y0b:cy1 - y0b, cx0 - x0:cx1 - x0]
            np.maximum(ash_a[cy0:cy1, cx0:cx1], mm * (0.55 + 0.45 * tt), out=ash_a[cy0:cy1, cx0:cx1])
            ash_c[cy0:cy1, cx0:cx1] = np.where(mm > 0.05, s['grey'] * (0.6 + 0.6 * tt), ash_c[cy0:cy1, cx0:cx1])
            heat = np.exp(-a_s / s['hot'])
            if heat > 0.03:
                core = np.clip(mm * (tt * 1.4 - 0.2), 0, 1) * heat
                light[cy0:cy1, cx0:cx1] += core[..., None] * (EMBER * 1.1)
        out = out * (1 - ash_a[..., None]) + (ash_a * ash_c)[..., None] * np.array([1.0, 0.96, 0.9], np.float32)
        # sparks: tiny bright points flying up with short trails
        for s, age in self._alive(t, self.sdt, self.slife, self._spark):
            a_s, u = age / FPS, age / s['life']
            y0 = int(np.clip(s['y'], 0, H - 1))
            def pos(a):
                dx = s['vx'] * a + s['curve'] * a * a
                xx = lines[s['side']][y0] - dx if s['side'] == 'left' else W - 1 - lines[s['side']][y0] + dx
                return int(xx), int(s['y'] + s['vy'] * a)
            p1, p0 = pos(a_s), pos(max(a_s - 0.07, 0))
            b = s['b'] * (1 - u) ** 1.5
            cv2.line(light, p0, p1, (float(EMBER_HOT[0] * b), float(EMBER_HOT[1] * b), float(EMBER_HOT[2] * b)), 1, cv2.LINE_AA)
        for sl in (np.s_[:, :bw], np.s_[:, W - bw:]):          # bloom, only where there is light
            li = light[sl]
            light[sl] = li + 0.45 * cv2.GaussianBlur(li, (0, 0), 5) + 0.25 * cv2.GaussianBlur(li, (0, 0), 16)
        return np.clip(out + light, 0, 1)
