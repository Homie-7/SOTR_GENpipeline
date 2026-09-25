"""The court's fragment edge: the paper screen BURNING AWAY at both sides (edge effect v3, Homie 2026-09-25).

WHY: the torn-paper edge read as "paper shreds", and masonry blocks belong to the rooms (salon, studio),
not to a lit paper screen (Homie: the rooms break like concrete because they are physical spaces; the
court's screen is not). Paper disintegrates by burning, so the screen smoulders at its left and right
edges and flakes away as ash, ONE WAY, for the whole appearance: nothing ever comes back.

- THE BURN LINE creeps slowly inward and never retreats: about 5% of the width at the start of beat 3,
  about 9% at the end of beat 7 (the three appearances share one timeline via --t0, so beat 5 starts
  where beat 3 stopped). Its shape is irregular (layered noise), as a real char line is.
- THE EDGE: a scorched band (browning, then charred dark) on the paper side, and a thin ember rim along
  the line itself that flickers and crawls. Beyond it, the dark.
- ASH: flakes keep breaking off the line and drift outward and a little upward, turning; each starts
  as a glowing ember and cools to grey, then fades. Deterministic slots (same scheme as edge_flow.py).
- The judge is laid over this by render_court.py, so he never burns (LOOK D7/D15). The impact shudder
  moves everything together.

Used by: python tools/render_court.py OUT.mov --beat 3 --scrim --burn [--t0 FRAMES]
"""
import cv2
import numpy as np

FPS = 24
TOTAL = 3864          # frames across beats 3 + 5 + 7 (960 + 2424 + 480): the burn's whole run
BEAT_T0 = {3: 0, 5: 960, 7: 3384}


def _noise1d(n, rng, octaves=((1, 1.0), (2, 0.6), (4, 0.35), (9, 0.18), (23, 0.08), (61, 0.04))):
    y = np.linspace(0, 1, n)
    out = np.zeros(n)
    for f, amp in octaves:
        out += amp * np.sin(2 * np.pi * (f * y + rng.uniform())) + amp * 0.5 * np.sin(2 * np.pi * (f * 1.7 * y + rng.uniform()))
    return out / np.abs(out).max()


class BurnEdges:
    def __init__(self, W, H, d0=0.05, d1=0.09, seed=1817, flakes=110, band=0.2):
        self.W, self.H = W, H
        rng = np.random.default_rng(seed)
        self.d0, self.d1 = d0 * W, d1 * W
        self.shape = {s: _noise1d(H, rng) for s in ('left', 'right')}
        self.creep = {s: np.clip(_noise1d(H, rng) * 0.5 + 0.5, 0, 1) for s in ('left', 'right')}
        self.flick = {s: rng.uniform(0, 100) for s in ('left', 'right')}
        self.bw = int(band * W)
        self.flakes = flakes
        self.seed = seed
        self.life = 7 * FPS
        self.dt = self.life / flakes
        self.cache = {}

    def line(self, side, t):
        """Burn depth (px from the frame edge) per row at flow frame t. Non-decreasing in t."""
        k = np.clip(t / TOTAL, 0, 1)
        D = self.d0 + (self.d1 - self.d0) * k
        return D * (1 + 0.38 * self.shape[side]) + 14 * self.creep[side] * k

    def _slot(self, j):
        if j in self.cache:
            return self.cache[j]
        r = np.random.default_rng([self.seed, j & 0xFFFFFFFF])
        k = int(r.integers(5, 9))
        ang = np.sort(r.uniform(0, 2 * np.pi, k))
        size = r.uniform(3, 13)
        poly = np.stack([np.cos(ang), np.sin(ang)], 1) * (size * r.uniform(0.45, 1.0, k))[:, None]
        s = dict(side='left' if r.uniform() < 0.5 else 'right', y=r.uniform(0, self.H), poly=poly,
                 jit=r.uniform(-0.5, 0.5) * self.dt, life=self.life * r.uniform(0.6, 1.3),
                 vx=r.uniform(7, 24), vy=-r.uniform(4, 16), spin=r.uniform(-2.5, 2.5),
                 wob=r.uniform(2, 7), wf=r.uniform(0.3, 0.9), ph=r.uniform(0, 6.3),
                 hot=r.uniform(0.4, 2.2), grey=r.uniform(0.18, 0.4))
        if len(self.cache) > 8192:
            self.cache.clear()
        self.cache[j] = s
        return s

    def frame(self, lit, t):
        """lit: the lit screen (H, W, 3, 0..1). Returns it burning at flow frame t."""
        W, H, bw = self.W, self.H, self.bw
        out = lit.copy()
        glow = np.zeros((H, W), np.float32)
        xs = np.arange(bw, dtype=np.float32)[None, :]
        for side in ('left', 'right'):
            d_line = self.line(side, t).astype(np.float32)[:, None]
            # distance into the paper from the burn line (px); the band is in edge coordinates
            d = xs - d_line
            sl = np.s_[:, :bw] if side == 'left' else np.s_[:, W - bw:]
            if side == 'right':
                d = d[:, ::-1]
            paper = out[sl]
            scorch = np.clip(np.exp(-np.clip(d, 0, None) / 5.0) * 0.9 + np.exp(-np.clip(d, 0, None) / 28.0) * 0.5, 0, 1)
            brown = np.array([0.55, 0.33, 0.16], np.float32)             # scorched paper browns before it chars
            tint = paper * (1 - 0.5 * scorch[..., None]) * (1 - 0.35 * scorch[..., None]) + \
                paper * brown * 0.35 * scorch[..., None] * (1 - scorch[..., None])
            alive = np.clip(d / 1.2, 0, 1)[..., None]                     # beyond the line: gone
            paper[:] = tint * alive
            # the ember rim: a thin crawling glow along the line, patchy
            yy = np.arange(H, dtype=np.float32)[:, None]
            f = self.flick[side]
            crawl = 0.55 + 0.45 * np.sin(yy * 0.045 + t * 0.09 + f) * np.sin(yy * 0.013 - t * 0.05 + 2 * f)
            crawl = np.clip(crawl + 0.25 * np.sin(yy * 0.31 + t * 0.4), 0, 1)
            rim = np.exp(-np.abs(d + 0.5) / 1.8) * crawl
            g = glow[sl]
            g[:] = np.maximum(g, rim)
        # ash: flakes break off the line and drift out and up, cooling from ember to grey
        ash = np.zeros((H, W), np.float32)
        hot = np.zeros((H, W), np.float32)
        lo = int(np.floor((t - 1.4 * self.life) / self.dt)) - 1
        hi = int(np.floor(t / self.dt)) + 1
        lines = {s: self.line(s, t) for s in ('left', 'right')}
        for j in range(lo, hi + 1):
            s = self._slot(j)
            age = t - (j * self.dt + s['jit'])
            if not 0 <= age < s['life']:
                continue
            a_s = age / FPS
            u = age / s['life']
            y0 = int(np.clip(s['y'], 0, H - 1))
            x_line = lines[s['side']][y0]
            dx = s['vx'] * a_s + s['wob'] * np.sin(2 * np.pi * s['wf'] * a_s + s['ph'])
            x = x_line - dx if s['side'] == 'left' else W - 1 - x_line + dx
            y = s['y'] + s['vy'] * a_s
            th = s['spin'] * a_s
            R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
            sc = 1 - 0.35 * u
            pts = (s['poly'] @ R.T * [1, 0.55 + 0.45 * abs(np.cos(1.3 * th))] * sc + [x, y]).astype(np.int32)
            fade = min(1.0, (1 - u) / 0.25, a_s / 0.3)
            heat = np.exp(-a_s / s['hot'])
            x0, y0b = max(pts[:, 0].min() - 2, 0), max(pts[:, 1].min() - 2, 0)
            x1, y1b = min(pts[:, 0].max() + 3, W), min(pts[:, 1].max() + 3, H)
            if x1 <= x0 or y1b <= y0b:
                continue
            m = np.zeros((y1b - y0b, x1 - x0), np.uint8)
            cv2.fillPoly(m, [pts - [x0, y0b]], 255, lineType=cv2.LINE_AA)
            m = m.astype(np.float32) / 255
            np.maximum(ash[y0b:y1b, x0:x1], m * (s['grey'] * fade), out=ash[y0b:y1b, x0:x1])
            np.maximum(hot[y0b:y1b, x0:x1], m * (heat * fade), out=hot[y0b:y1b, x0:x1])
        ember = np.array([1.0, 0.45, 0.12], np.float32)
        out = out * (1 - np.clip(ash * 2, 0, 1)[..., None]) + ash[..., None] * np.array([0.62, 0.58, 0.52], np.float32)
        light = np.maximum(glow, hot)
        light = light + 0.35 * cv2.GaussianBlur(light, (0, 0), 6)            # a soft halo round the embers
        return np.clip(out + light[..., None] * ember * 0.85, 0, 1)
