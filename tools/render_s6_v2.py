"""Scene 6 animatic v2 (kept so v2 can be rebuilt; v3 is render_s6.py). Original docstring follows.

Scene 6 (The Napoleonic Wars): the ANIMATIC, v2, across all three walls, from one 4680x1080 timeline.

WHY: Scene 6 is floating imagery over a movement piece (client, 2026-09-28). The animatic lets Homie and
the client judge the whole scene before any credit is spent. v1 (`render_s6_v1.py`) worked as a flow;
Homie's notes on it (2026-09-28) are what v2 answers:
  1. the flag is not an illustration in the middle of CENTRE: a cloth with the physical properties of a
     flag, flowy and atmospheric, covering the wall, its edges dissolving (AtmoFlag);
  2/7. no rectangular "image stamps", no frames anywhere: every picture washes in large with organic,
     breathing edges that slowly flake away into drifting paper fragments, one way (Wash + Flakes, the
     Scene 9 edge idea for paper); the ink-in and the burn stay (he liked them);
  3. "France divided" reads: the tricolour TEARS down the middle of CENTRE and its right half bleaches
     white; the tricolour on LEFT, the white Bourbon flag on RIGHT; then all three burn;
  4. no stick figures: Goya's fleeing families (Disasters of War 41, 44, 45, 1810) ghost into the dawn
     haze and recede toward the ship;
  5. the map is the SHAPE of the continent, glowing, floating in a faded sea of the old map with its
     lettering and islands (Homie's 2022 Slide 6 mock-up), not a framed print;
  6. far less negative space: pictures are big and layered; smoke, ash and coloured light fill the rest.

Rules kept from LOOK.md "Scene 6": colour only in the flag and the fire; fields (smoke, embers, ash,
haze, coloured light, the Liberté colour walls) may cross the seams; objects never do: every picture,
flag, flake and word fades out inside a 300 mm (90 px) guard at each wall edge (Ctx.guard).
Our picture leads the timing (~2:45); the caption strip under the picture is for review only.

  python tools/render_s6.py OUT.mp4 [--scale 0.5] [--start S --end S] [--stills DIR --at 3,14,...]
"""
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from court_burn import fractal  # noqa: E402

FPS = 24
DUR = 165.0
FULL_W, FULL_H = 4680, 1080
WALLS = {'L': (0, 1440), 'C': (1440, 3240), 'R': (3240, 4680)}
MARGIN = 90                      # 300 mm on a 4800 mm / 1440 px flat
SRC = r'C:\Users\Homie\Documents\SOTR_MEDIA\02_APPROVED_BUILDING_BLOCKS\S6_public_domain'
FONTS = os.path.join(os.path.dirname(__file__), 'fonts')

PAPER = np.array([0.66, 0.60, 0.49], np.float32)
PAPER_GREY = np.array([0.55, 0.54, 0.52], np.float32)
INK = np.array([0.05, 0.04, 0.03], np.float32)
EMBER = np.array([1.0, 0.45, 0.12], np.float32)
ASH = np.array([0.42, 0.40, 0.37], np.float32)
BLUE = np.array([0.11, 0.18, 0.46], np.float32)
WHITE = np.array([0.80, 0.78, 0.72], np.float32)
RED = np.array([0.64, 0.10, 0.12], np.float32)
AMBER = np.array([0.98, 0.66, 0.28], np.float32)

CROPS = {
    'battle_austerlitz_DuplessiBertaux': (0.07, 0.10, 0.93, 0.54),
    'battle_wagram_estampe': (0.19, 0.09, 0.82, 0.60),
    'battle_iena_DuplessiBertaux': (0.04, 0.04, 0.97, 0.72),
    'battle_eylau_estampe': (0.19, 0.16, 0.80, 0.67),
    'battle_friedland_1808': (0.04, 0.11, 0.96, 0.62),
    'goya_p50_famine_MadreInfeliz': (0.245, 0.22, 0.73, 0.71),
    'goya_p15_execution_YnoHaiRemedio': (0.27, 0.21, 0.725, 0.76),
    'goya_p18_death_EnterraryCallar': (0.21, 0.205, 0.76, 0.705),
    'goya_p30_ravages_Estragos': (0.265, 0.25, 0.735, 0.81),
    'goya_p41_fleeing_EscapanLlamas': (0.205, 0.205, 0.755, 0.715),
    'goya_p44_fleeing_YoLoVi': (0.205, 0.205, 0.745, 0.67),
    'goya_p45_fleeing_YestoTambien': (0.235, 0.215, 0.77, 0.725),
    'battle_waterloo_MontStJean_1815': (0.10, 0.16, 0.90, 0.76),
    'battle_waterloo_field_Jazet_1816': (0.12, 0.13, 0.86, 0.72),
}
# Bellin's Carte de l'Afrique (1740s): lon/lat -> image fraction, least-squares fit on 7 capes (2026-09-28)
BELLIN_FX = (8.24193980e-03, -8.60414514e-05, 3.66176906e-01)
BELLIN_FY = (4.08052042e-05, -7.61695559e-03, 4.75185211e-01)
# the Medusa's course: off the top (from Rochefort), Madeira, Tenerife, Cap Blanc / Arguin, Saint-Louis
ROUTE_LONLAT = [(-9.5, 47.0), (-13.0, 38.5), (-16.9, 32.7), (-16.4, 28.3), (-17.4, 21.5), (-17.2, 19.5), (-16.5, 16.0)]
SENEGAL = (-16.5, 16.0)

LINES = [
    (18.0, 'AGNÈS', "Après vingt-trois années de guerre -"), (20.5, 'AMINA', "After 23 years of war -"),
    (23.5, 'AGNÈS', "J'ai appris à être forte. À être utile. Comme les hommes -"),
    (28.0, 'AMINA', "I learned to be strong. To be useful. Like the men."),
    (32.0, 'AGNÈS', "Pour nos braves, nos glorieux soldats."), (35.0, 'AMINA', "For our brave ones. Our glorious soldiers."),
    (38.0, 'AGNÈS', "Nous avons connu la victoire."), (41.0, 'AGNÈS', "Austerlitz."), (43.5, 'AGNÈS', "Wagram."),
    (46.0, 'AGNÈS', "Iéna."), (48.5, 'AGNÈS', "Eylau."), (51.0, 'AGNÈS', "Friedland."),
    (53.0, 'AMINA', "We fought for France."), (55.0, 'AGNÈS', "Nous avons cru à la victoire -"),
    (57.0, 'AMINA', "We believed in victory."),
    (59.0, 'AGNÈS', "Et puis il y a eu la famine -"), (61.0, 'AMINA', "Famine."),
    (63.0, 'AGNÈS', "Les exécutions -"), (65.0, 'AMINA', "Executions."), (67.0, 'AGNÈS', "La mort -"),
    (69.0, 'AMINA', "Death!"),
    (79.0, 'AGNÈS', "Et malgré tout, nous avons parlé de Liberté, d'Égalité, de Fraternité."),
    (88.0, '', "(Silence)"),
    (96.0, 'AGNÈS', "Il fallait continuer à se battre pour Napoléon."), (99.0, 'AMINA', "We fought for France."),
    (101.0, 'AGNÈS', "Jusqu'à Waterloo -"), (103.0, 'AMINA', "Waterloo."),
    (105.0, 'AGNÈS', "Là où Napoléon est vaincu -"), (107.5, 'AMINA', "Defeated. Banished."),
    (110.0, 'AGNÈS', "Humilié ! Exilé ! Après vingt-trois ans, je ne reconnais plus mon pays."),
    (121.0, 'AMINA', "France is divided."), (124.0, 'AGNÈS', "Monarchistes !"), (126.0, 'AGNÈS', "Napoléonistes !"),
    (128.0, 'AGNÈS', "La France est dangereuse pour moi."), (131.0, 'AMINA', "Oui."),
    (137.0, 'AGNÈS', "Alors... je pars."), (139.0, 'AMINA', "You are leaving France?"),
    (141.0, 'AGNÈS', "Oui. Je dois partir. Recommencer ailleurs. Loin de tout ça."),
    (145.0, 'SARAH/AMINA', "Where are you going?"), (147.0, 'AGNÈS', "Loin !"), (157.0, 'AMINA', "Away from here!"),
    (160.0, '', "(The Medusa appears on the horizon.)"),
]
MOVES = [(0, 'M1 · smoke, the march'), (18, 'M2 · glory, the five battles'), (58, 'M3 · famine, executions, death'),
         (78, 'M4 · Liberté, Égalité, Fraternité'), (96, 'M5 · Waterloo'), (120, 'M6 · France divided'),
         (136, 'M7 · je pars… the Medusa')]


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def ssf(e0, e1, x):
    return float(ss(e0, e1, x))


class Ctx:
    def __init__(self, scale):
        self.s = scale
        self.W, self.H = int(round(FULL_W * scale)), int(round(FULL_H * scale))
        self.rng = np.random.default_rng(1816)
        xs = (np.arange(self.W) + 0.5) / scale
        g = np.zeros(self.W, np.float32)
        for x0, x1 in WALLS.values():
            inside = (xs >= x0) & (xs < x1)
            d = np.minimum(xs - x0, x1 - xs)
            g[inside] = ss(MARGIN, MARGIN + 110, d[inside])
        self.guard = g                                       # 0 within 300 mm of any wall edge

    def px(self, v):
        return int(round(v * self.s))

    def wall_xy(self, wall, fx, fy):
        x0, x1 = WALLS[wall]
        return (x0 + fx * (x1 - x0)) * self.s, fy * FULL_H * self.s

    def wall_px(self, wall):
        x0, x1 = WALLS[wall]
        return self.px(x0), self.px(x1)


def load(name):
    im = cv2.imread(os.path.join(SRC, name + '.jpg'))
    if name in CROPS:
        h, w = im.shape[:2]
        x0, y0, x1, y1 = CROPS[name]
        im = im[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    return im


def tone(im, paper=PAPER, ink=INK, lo_p=1.5, hi_p=92, gamma=0.9):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    lo, hi = np.percentile(g, lo_p), np.percentile(g, hi_p)
    t = np.clip((g - lo) / (hi - lo + 1e-6), 0, 1) ** gamma
    return ink[None, None] * (1 - t[..., None]) + paper[None, None] * t[..., None], t


def blit(canvas, rgb, alpha, ox, oy, add=None, guard=None, mode='over'):
    """Composite at a sub-pixel position. guard (1D, canvas width) fades objects out at the wall edges."""
    H, W = canvas.shape[:2]
    ix, iy = int(np.floor(ox)), int(np.floor(oy))
    h, w = alpha.shape
    M = np.float32([[1, 0, ox - ix], [0, 1, oy - iy]])
    stack = np.dstack([rgb, alpha[..., None]] + ([add] if add is not None else [])).astype(np.float32)
    sh = cv2.warpAffine(stack, M, (w + 2, h + 2), flags=cv2.INTER_LINEAR, borderValue=0)
    x0, y0 = max(0, ix), max(0, iy)
    x1, y1 = min(W, ix + w + 2), min(H, iy + h + 2)
    if x1 <= x0 or y1 <= y0:
        return
    sub = sh[y0 - iy:y1 - iy, x0 - ix:x1 - ix]
    a = sub[..., 3:4]
    if guard is not None:
        a = a * guard[None, x0:x1, None]
    region = canvas[y0:y1, x0:x1]
    if mode == 'multiply':                                   # engraving on haze: paper -> the light, ink -> dark
        region[:] = region * (1 - a) + region * sub[..., :3] * a
    else:
        region[:] = region * (1 - a) + sub[..., :3] * a
    if add is not None:
        g = sub[..., 4:7] if guard is None else sub[..., 4:7] * guard[None, x0:x1, None]
        region[:] += g


def slide(field, w, h, cx, cy):
    return cv2.getRectSubPix(field, (int(w), int(h)), (float(cx), float(cy)))


# --------------------------------------------------------------------------- the paper fragments that break off
class Flakes:
    """Torn pieces of a picture, cut from its edge, drifting off one way: ember while it burns, then ash."""

    def __init__(self, ctx):
        self.ctx, self.rng, self.items = ctx, np.random.default_rng(44), []

    def spawn(self, src, sx, sy, cx, cy, out, ember=False):
        if len(self.items) > 420:
            return
        r = self.rng
        sz = max(6, int(r.uniform(8, 26) * self.ctx.s * 2))
        h, w = src.shape[:2]
        if h <= sz or w <= sz:
            return
        x0, y0 = int(np.clip(sx - sz / 2, 0, w - sz)), int(np.clip(sy - sz / 2, 0, h - sz))
        patch = np.ascontiguousarray(src[y0:y0 + sz, x0:x0 + sz], np.float32)
        n = r.integers(5, 9)
        ang = np.sort(r.uniform(0, 2 * np.pi, n))
        rad = r.uniform(0.25, 0.5, n) * sz
        poly = np.stack([sz / 2 + rad * np.cos(ang), sz / 2 + rad * np.sin(ang)], 1).astype(np.int32)
        m = np.zeros((sz, sz), np.float32)
        cv2.fillPoly(m, [poly], 1.0)
        m = cv2.GaussianBlur(m, (0, 0), 0.6)
        spd = r.uniform(14, 34) * self.ctx.s * (1.6 if ember else 1)
        vel = np.array(out, np.float32) * spd + np.array([r.normal(0, 4), -r.uniform(4, 14) * (2 if ember else 1)], np.float32) * self.ctx.s
        self.items.append(dict(p=patch, m=m, x=cx, y=cy, v=vel, a=r.uniform(0, 360), va=r.uniform(-70, 70),
                               life=r.uniform(2.5, 5.5), age=0.0, ember=ember))

    def draw(self, canvas, dt):
        keep = []
        for f in self.items:
            f['age'] += dt
            if f['age'] >= f['life']:
                continue
            f['x'] += f['v'][0] * dt
            f['y'] += f['v'][1] * dt
            f['v'][1] -= 3 * self.ctx.s * dt
            f['a'] += f['va'] * dt
            k = f['age'] / f['life']
            sz = f['m'].shape[0]
            M = cv2.getRotationMatrix2D((sz / 2, sz / 2), f['a'], 1 - 0.45 * k)
            p = cv2.warpAffine(f['p'], M, (sz, sz), borderValue=0)
            m = cv2.warpAffine(f['m'], M, (sz, sz), borderValue=0)
            col = p * (1 - 0.7 * k) + ASH[None, None] * 0.7 * k * 0.6
            add = None
            if f['ember']:
                edge = np.clip(m - cv2.erode(m, np.ones((3, 3), np.uint8)), 0, 1)
                add = (edge * (1 - k) ** 1.5)[..., None] * EMBER[None, None] * 1.4
                col = col * (1 - 0.6 * min(1.0, k * 2))
            blit(canvas, col, m * (1 - k) ** 1.1, f['x'] - sz / 2, f['y'] - sz / 2, add, guard=self.ctx.guard)
            keep.append(f)
        self.items = keep


# --------------------------------------------------------------------------- a picture, washed in, no frame
class Wash:
    """A print as an atmospheric wash: big, organic breathing edges that erode one way and flake off;
    it arrives as an ink bloom and leaves by burning."""

    def __init__(self, ctx, rgb, wall, cx, cy, h_full, t_in, t_out, in_dur=3.0, out_dur=4.0, drift=(0.0, -2.0),
                 grow=0.004, seed=0, flake_rate=7.0, mode='over', name=''):
        self.ctx, self.wall, self.t_in, self.t_out, self.in_dur, self.out_dur = ctx, wall, t_in, t_out, in_dur, out_dur
        self.drift, self.grow, self.flake_rate, self.mode, self.name = drift, grow, flake_rate, mode, name
        hh = max(8, ctx.px(h_full))
        ww = max(8, int(round(rgb.shape[1] * hh / rgb.shape[0])))
        self.rgb = np.ascontiguousarray(cv2.resize(rgb, (ww, hh), interpolation=cv2.INTER_AREA), np.float32)
        self.h, self.w = hh, ww
        self.cx, self.cy = ctx.wall_xy(wall, cx, cy)
        rng = np.random.default_rng(seed + 3)
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        ex, ey = np.abs(xx - ww / 2) / (ww / 2), np.abs(yy - hh / 2) / (hh / 2)
        r = (ex ** 2.2 + ey ** 2.2) ** (1 / 2.2)
        self.base = 1 - r
        sc = max(3, hh // 4)
        self.big = fractal(hh + 80, ww + 160, rng, scales=(sc, max(3, sc // 3), max(2, sc // 8)), gains=(1, 0.5, 0.25))
        self.fine = fractal(hh, ww, np.random.default_rng(seed + 9), scales=(max(2, sc // 6), max(2, sc // 16)), gains=(1, 0.5))
        n = fractal(hh, ww, np.random.default_rng(seed + 7), scales=(sc, max(2, sc // 3)), gains=(1, 0.45))
        self.n_in = np.clip(0.55 * (n * 0.5 + 0.5) + 0.45 * np.clip(r, 0, 1), 0, 1)
        side = 'R' if wall == 'L' else 'L' if wall == 'R' else 'B'
        grad = {'L': xx / ww, 'R': 1 - xx / ww, 'B': 1 - np.abs(xx / ww - 0.5) * 2}[side]
        n2 = fractal(hh, ww, np.random.default_rng(seed + 99), scales=(sc, max(2, sc // 3), max(2, sc // 8)), gains=(1, 0.5, 0.25))
        self.n_out = np.clip(0.5 * grad + 0.5 * (n2 * 0.5 + 0.5), 0, 1)
        mott = fractal(hh, ww, np.random.default_rng(seed + 11), scales=(sc, max(2, sc // 5)), gains=(1, 0.4))
        if mode == 'over':
            self.rgb *= (1 + 0.07 * mott)[..., None]

    def active(self, t):
        return self.t_in <= t <= self.t_out + self.out_dur

    def draw(self, t, canvas, flakes, dt):
        tt = t - self.t_in
        life = max(1e-3, self.t_out - self.t_in)
        br = slide(self.big, self.w, self.h, self.w / 2 + 80 + 9 * self.ctx.s * np.sin(t * 0.21 + self.cx),
                   self.h / 2 + 40 + 5 * self.ctx.s * np.cos(t * 0.17))
        m = self.base + 0.30 * br + 0.08 * self.fine
        thr = 0.10 + 0.12 * min(1.0, tt / life)                     # the edges erode, one way
        shape = ss(thr - 0.06, thr + 0.34, m)
        a_in = ssf(0, 1, tt / self.in_dur) * 1.25
        rev = np.clip((a_in - self.n_in) / 0.07, 0, 1)
        front = np.clip(1 - np.abs(a_in - self.n_in - 0.03) / 0.05, 0, 1) * (a_in < 1.2)
        b = ssf(0, 1, (t - self.t_out) / self.out_dur) * 1.15 if t > self.t_out else 0.0
        rgb = self.rgb
        if self.mode == 'over':
            rgb = rgb * (1 - 0.6 * front)[..., None]
        glow = None
        rim = None
        alive = 1.0
        if b > 0:
            d = self.n_out - b
            alive = np.clip(d / 0.012, 0, 1)
            char = np.clip(1 - d / 0.07, 0, 1) * (d > 0)
            if self.mode == 'over':
                rgb = rgb * (1 - 0.85 * char[..., None])
            rim = np.clip(1 - np.abs(d - 0.006) / 0.012, 0, 1) * (b < 1.12)
            rim = rim * np.clip(np.sin(self.n_in * 55 + t * 1.3) * 0.9 + 0.35, 0, 1)
            if self.mode == 'over':
                glow = (rim * (0.75 + 0.25 * np.sin(t * 13 + self.n_in * 40)))[..., None] * EMBER[None, None] * 1.5
        alpha = (shape * rev * alive).astype(np.float32)
        scale = 1 + self.grow * tt
        ox = self.cx + self.drift[0] * tt * self.ctx.s
        oy = self.cy + self.drift[1] * tt * self.ctx.s
        if abs(scale - 1) > 1e-3:
            M = np.float32([[scale, 0, (1 - scale) * self.w / 2], [0, scale, (1 - scale) * self.h / 2]])
            rgb = cv2.warpAffine(np.ascontiguousarray(rgb, np.float32), M, (self.w, self.h))
            alpha = cv2.warpAffine(alpha, M, (self.w, self.h))
            if glow is not None:
                glow = cv2.warpAffine(np.ascontiguousarray(glow, np.float32), M, (self.w, self.h))
        blit(canvas, rgb, alpha, ox - self.w / 2, oy - self.h / 2, glow, guard=self.ctx.guard, mode=self.mode)
        if self.mode != 'over':
            return
        # fragments break off the eroding edge (and, while it burns, off the burning rim as embers)
        rng = self.ctx.rng
        k = rng.poisson(self.flake_rate * dt * min(1.0, tt / 1.5))
        if k:
            band = np.argwhere((alpha > 0.25) & (alpha < 0.65))
            if len(band):
                for i in rng.integers(0, len(band), size=min(k, len(band))):
                    y, x = band[i]
                    o = np.array([x - self.w / 2, y - self.h / 2], np.float32)
                    o /= np.linalg.norm(o) + 1e-6
                    flakes.spawn(self.rgb, x, y, ox - self.w / 2 + x, oy - self.h / 2 + y, o)
        if rim is not None:
            kk = rng.poisson(18 * dt)
            if kk:
                pts = np.argwhere(rim > 0.6)
                if len(pts):
                    for i in rng.integers(0, len(pts), size=min(kk, len(pts))):
                        y, x = pts[i]
                        o = np.array([x - self.w / 2, y - self.h / 2], np.float32)
                        o /= np.linalg.norm(o) + 1e-6
                        flakes.spawn(self.rgb, x, y, ox - self.w / 2 + x, oy - self.h / 2 + y, o, ember=True)


# --------------------------------------------------------------------------- the flag as a cloth, not a picture
class AtmoFlag:
    """PLACEHOLDER for S6-FLAG: a cloth filling a wall, folding in the wind, its edges dissolving into smoke."""

    def __init__(self, ctx, wall, kind='tri', seed=0):
        self.ctx, self.wall, self.kind = ctx, wall, kind
        x0, x1 = ctx.wall_px(wall)
        self.x0, self.w, self.h = x0, x1 - x0, ctx.H
        w, h = self.w, self.h
        pad = ctx.px(160)
        self.pad = pad
        cw, ch = w + 2 * pad, h + 2 * pad
        xx = np.arange(cw, dtype=np.float32)
        cloth = np.zeros((ch, cw, 3), np.float32)
        if kind == 'tri':
            b1, b2 = pad + w / 3, pad + 2 * w / 3
            soft = ctx.px(40)
            wb = ss(b1 - soft, b1 + soft, xx)[None, :, None]
            wr = ss(b2 - soft, b2 + soft, xx)[None, :, None]
            cloth[:] = BLUE * (1 - wb) + WHITE * (wb - wr) + RED * wr
        else:
            cloth[:] = WHITE * 0.95
        weave = fractal(ch, cw, np.random.default_rng(seed + 12), scales=(max(3, ch // 6), max(2, ch // 30)), gains=(1, 0.35))
        self.cloth = np.ascontiguousarray(cloth * 0.9 * (1 + 0.07 * weave[..., None]), np.float32)
        self.whiteC = np.ascontiguousarray(np.ones_like(cloth) * WHITE * (1 + 0.07 * weave[..., None]), np.float32)
        self.turb = fractal(h + ctx.px(700), w + ctx.px(2400), np.random.default_rng(seed + 5),
                            scales=(ctx.px(420), ctx.px(160), ctx.px(60)), gains=(1, 0.45, 0.15))
        self.edge = fractal(h + ctx.px(400), w + ctx.px(400), np.random.default_rng(seed + 6),
                            scales=(ctx.px(260), ctx.px(90), ctx.px(30)), gains=(1, 0.5, 0.2))
        yy, xx2 = np.mgrid[0:h, 0:w].astype(np.float32)
        self.X, self.Y = xx2, yy
        ex, ey = np.abs(xx2 - w / 2) / (w / 2), np.abs(yy - h * 0.44) / (h * 0.52)
        self.r = (ex ** 3 + ey ** 3) ** (1 / 3)
        n = fractal(h, w, np.random.default_rng(seed + 8), scales=(ctx.px(200), ctx.px(60)), gains=(1, 0.4)) * 0.5 + 0.5
        self.n_in = np.clip(0.5 * n + 0.5 * np.clip(self.r, 0, 1), 0, 1)
        g = {'L': xx2 / w, 'R': 1 - xx2 / w, 'C': 1 - np.abs(xx2 / w - 0.5) * 2}[wall]
        n2 = fractal(h, w, np.random.default_rng(seed + 9), scales=(ctx.px(220), ctx.px(70), ctx.px(24)), gains=(1, 0.5, 0.2)) * 0.5 + 0.5
        self.n_out = np.clip(0.55 * g + 0.45 * n2, 0, 1)
        self.tearn = fractal(h, 8, np.random.default_rng(seed + 10), scales=(ctx.px(240), ctx.px(80), ctx.px(26)), gains=(1, 0.4, 0.12))[:, 0]
        self.bleachn = n

    def render(self, t, reveal=1.0, grey=0.0, burn=0.0, tear=0.0, bleach=0.0, amp=1.0):
        s, w, h = self.ctx.s, self.w, self.h
        T = slide(self.turb, w, h, w / 2 + self.ctx.px(2400) - 70 * s * t, h / 2 + self.ctx.px(350) + 20 * s * np.sin(t * 0.21))
        X, Y = self.X, self.Y
        A = 46 * s * amp
        k1, k2 = 2 * np.pi / (w * 0.42), 2 * np.pi / (w * 0.27)
        Hf = A * (np.sin(k1 * X - 1.7 * t + 1.1 * T + 0.004 * Y / s) + 0.45 * np.sin(k2 * (0.8 * X + 0.6 * Y) - 1.15 * t + 0.8 * T)
                  + 0.5 * T)
        Hf = Hf.astype(np.float32)
        gx = cv2.Sobel(Hf, cv2.CV_32F, 1, 0, ksize=3) / 8
        gy = cv2.Sobel(Hf, cv2.CV_32F, 0, 1, ksize=3) / 8
        shade = np.clip(0.88 - 0.95 * (0.75 * gx + 0.45 * gy) / (A * k1 + 1e-6), 0.5, 1.22)
        shade *= np.clip(0.88 + 0.2 * (Hf / (A * 2.0) + 0.5), 0.72, 1.08)          # folds that recede go dark
        u = (X + self.pad + 0.9 * Hf).astype(np.float32)
        v = (Y + self.pad + 0.45 * Hf).astype(np.float32)
        img = cv2.remap(self.cloth, u, v, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        if bleach > 0:                                                         # the Restoration: colour drains to white
            front = ss(0, 0.12, bleach * 1.3 - (1 - np.clip((X / w - 0.5) * 2, 0, 1)) * 0.6 - self.bleachn * 0.4)
            front = front * (X > w * 0.5 - 2)
            wimg = cv2.remap(self.whiteC, u, v, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            img = img * (1 - front[..., None]) + wimg * front[..., None]
        img = img * shade[..., None]
        sheen = np.clip(shade - 1.1, 0, 1)[..., None] * 0.25
        img = img + sheen * np.array([0.9, 0.88, 0.85], np.float32)
        if grey > 0:
            gg = img.mean(2, keepdims=True)
            img = img * (1 - grey) + gg * 0.55 * grey
        E = slide(self.edge, w, h, w / 2 + self.ctx.px(200) - 25 * s * t, h / 2 + self.ctx.px(200) - 6 * s * t)
        edge = ss(0.02, 0.30, (1 - self.r) + 0.32 * E)
        rev = np.clip((reveal * 1.25 - self.n_in) / 0.12, 0, 1)
        alpha = edge * rev
        glow = None
        if tear > 0:
            cxl = w / 2 + self.tearn[:, None] * self.ctx.px(110)
            d = np.abs(X - cxl)
            tw = tear * w * 0.16
            alpha = alpha * ss(tw, tw + self.ctx.px(24), d)
            rim = np.clip(1 - np.abs(d - tw - self.ctx.px(8)) / max(1, self.ctx.px(9)), 0, 1) * np.clip(np.sin(Y * 0.05 + self.tearn[:, None] * 9 + t * 1.3) * 0.9 + 0.2, 0, 1)
            glow = rim[..., None] * EMBER[None, None] * 0.9
            img = img * (ss(tw, tw + self.ctx.px(26), d) ** 0.5)[..., None]
        if burn > 0:
            dd = self.n_out - burn
            alpha = alpha * np.clip(dd / 0.012, 0, 1)
            char = np.clip(1 - dd / 0.08, 0, 1) * (dd > 0)
            img = img * (1 - 0.85 * char[..., None])
            rim = np.clip(1 - np.abs(dd - 0.006) / 0.012, 0, 1) * (burn < 1.1)
            rim = rim * np.clip(np.sin(self.n_in * 60 + t * 1.2) * 0.9 + 0.3, 0, 1)
            g2 = rim[..., None] * EMBER[None, None] * 1.4
            glow = g2 if glow is None else glow + g2
        return img.astype(np.float32), alpha.astype(np.float32), None if glow is None else glow.astype(np.float32)

    def draw(self, canvas, t, strength=1.0, **kw):
        img, a, glow = self.render(t, **kw)
        blit(canvas, img, a * strength, self.x0, 0, None if glow is None else glow * strength, guard=self.ctx.guard)


# --------------------------------------------------------------------------- the continent
def lonlat_to_bellin(lon, lat, W, H):
    fx = BELLIN_FX[0] * lon + BELLIN_FX[1] * lat + BELLIN_FX[2]
    fy = BELLIN_FY[0] * lon + BELLIN_FY[1] * lat + BELLIN_FY[2]
    return fx * W, fy * H


class ContinentMap:
    """Africa's own shape, glowing like old paper held to a lamp, floating in a faded sea of Bellin's
    1740s map (its lettering, islands and lines in the negative space). After Homie's 2022 Slide 6."""

    def __init__(self, ctx):
        self.ctx = ctx
        x0, x1 = ctx.wall_px('C')
        self.x0, self.w, self.h = x0, x1 - x0, ctx.H
        im = cv2.imread(os.path.join(SRC, 'map_africa_Bellin_1740s.jpg'))
        BH, BW = im.shape[:2]
        im = self._inpaint(im)
        sc = 0.94 * self.h / (0.55 * BH)                      # Africa's height (fy 0.195..0.745) fills 94% of the wall
        cxb, cyb = 0.505 * BW, 0.47 * BH
        self.M = np.float32([[sc, 0, self.w / 2 - sc * cxb], [0, sc, self.h * 0.50 - sc * cyb]])
        warped = cv2.warpAffine(im, self.M, (self.w, self.h), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_REPLICATE)
        gj = json.load(open(os.path.join(SRC, 'naturalearth_50m_countries.geojson'), encoding='utf-8'))
        land = np.zeros((self.h, self.w), np.float32)
        other = np.zeros((self.h, self.w), np.float32)
        for f in gj['features']:
            cont = f['properties'].get('CONTINENT')
            geom = f['geometry']
            polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
            for poly in polys:
                ring = np.array(poly[0])
                if ring[:, 0].max() < -40 or ring[:, 0].min() > 75 or ring[:, 1].max() < -45 or ring[:, 1].min() > 55:
                    continue
                bx, by = lonlat_to_bellin(ring[:, 0], ring[:, 1], BW, BH)
                P = np.c_[bx * sc + self.M[0, 2], by * sc + self.M[1, 2]]
                cv2.fillPoly(land if cont == 'Africa' else other, [np.int32(P * 4)], 1.0, cv2.LINE_AA, shift=2)
        self.land = cv2.GaussianBlur(land, (0, 0), 0.8)
        g = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
        lo, hi = np.percentile(g, 2), np.percentile(g, 90)
        tt = np.clip((g - lo) / (hi - lo), 0, 1)[..., None]
        land_rgb = np.array([0.20, 0.09, 0.03], np.float32) * (1 - tt) + AMBER * 0.92 * tt
        sea_rgb = np.array([0.05, 0.05, 0.06], np.float32) * (1 - tt) + np.array([0.30, 0.29, 0.29], np.float32) * tt
        oth = cv2.GaussianBlur(other, (0, 0), 0.8)[..., None]
        sea_rgb = sea_rgb * (1 - 0.35 * oth) + land_rgb * 0.35 * oth                      # Europe, Arabia: ghosted, not lit
        dist = cv2.distanceTransform((self.land < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        u = ctx.s * 2
        wl = sum(wgt * np.exp(-((dist - d0 * u) / (0.9 * u)) ** 2) for d0, wgt in ((4, 0.55), (9, 0.35), (15, 0.22), (23, 0.12)))
        coast = np.exp(-((dist - 0.5) / (1.1 * u)) ** 2)
        halo = cv2.GaussianBlur(self.land, (0, 0), ctx.px(28))
        L = self.land[..., None]
        img = sea_rgb * (1 - L) + land_rgb * L
        img = img + (wl * (1 - self.land))[..., None] * np.array([0.40, 0.36, 0.30], np.float32) * 0.5
        img = img * (1 - 0.55 * coast[..., None]) + (halo * (1 - self.land))[..., None] * AMBER * 0.28
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        rr = np.sqrt(((xx - self.w / 2) / (self.w * 0.55)) ** 2 + ((yy - self.h / 2) / (self.h * 0.62)) ** 2)
        vn = fractal(self.h, self.w, np.random.default_rng(77), scales=(ctx.px(260), ctx.px(80)), gains=(1, 0.4))
        self.sea_a = np.clip(1.15 - rr + 0.25 * vn, 0, 1) ** 1.3 * 0.8
        self.img = img.astype(np.float32)
        sx, sy = lonlat_to_bellin(*SENEGAL, BW, BH)
        self.sen = (sx * sc + self.M[0, 2], sy * sc + self.M[1, 2])
        ds = np.sqrt((xx - self.sen[0]) ** 2 + (yy - self.sen[1]) ** 2) / self.w
        nn = fractal(self.h, self.w, np.random.default_rng(78), scales=(ctx.px(180), ctx.px(50)), gains=(1, 0.45)) * 0.5 + 0.5
        self.n_in_land = np.clip(0.45 * ds * 1.4 + 0.35 * nn, 0, 1)
        self.n_in_sea = np.clip(0.35 + 0.35 * rr + 0.3 * nn, 0, 1)
        self.route = []
        for lon, lat in ROUTE_LONLAT:
            bx, by = lonlat_to_bellin(lon, lat, BW, BH)
            self.route.append((bx * sc + self.M[0, 2], by * sc + self.M[1, 2]))

    @staticmethod
    def _inpaint(im):
        h, w = im.shape[:2]
        b, g, r = [im[..., i].astype(int) for i in range(3)]
        col = ((b - r > 14) | (r - g > 40))
        box = np.zeros((h, w), bool)
        box[int(0.76 * h):int(0.88 * h), int(0.22 * w):int(0.40 * w)] = True
        box[int(0.64 * h):int(0.75 * h), int(0.74 * w):int(0.88 * w)] = True
        m = cv2.dilate((col & box).astype(np.uint8) * 255, np.ones((11, 11), np.uint8))
        return cv2.inpaint(im, m, 9, cv2.INPAINT_TELEA)

    def draw(self, canvas, t, t_in, wash):
        a = ssf(t_in, t_in + 5.0, t) * 1.2
        rl = np.clip((a - self.n_in_land) / 0.08, 0, 1)
        rs = np.clip((a - 0.35 - self.n_in_sea) / 0.1, 0, 1)
        alpha = (self.land * rl + (1 - self.land) * self.sea_a * rs) * (1 - wash)
        img = self.img * (1 + 0.05 * np.sin(t * 1.3))
        blit(canvas, img, alpha.astype(np.float32), self.x0, 0, guard=self.ctx.guard)
        self.draw_route(canvas, t, wash)

    def draw_route(self, canvas, t, wash):
        k = ssf(149.5, 154.5, t)
        if k <= 0 or wash >= 1:
            return
        P = np.array(self.route, np.float32) + np.array([self.x0, 0], np.float32)
        seg = np.sqrt(((P[1:] - P[:-1]) ** 2).sum(1))
        L = seg.sum() * k
        layer = np.zeros(canvas.shape[:2], np.float32)
        acc = 0
        for (a, b), l in zip(zip(P[:-1], P[1:]), seg):
            if acc >= L:
                break
            f = min(1, (L - acc) / l)
            e = a + (b - a) * f
            n = max(2, int(l * f / max(3, 10 * self.ctx.s)))
            for i in range(n):
                if i % 2 == 0:
                    p0, p1 = a + (e - a) * i / n, a + (e - a) * (i + 1) / n
                    cv2.line(layer, tuple(int(v) for v in p0), tuple(int(v) for v in p1), 1.0, max(2, int(6 * self.ctx.s)), cv2.LINE_AA)
            acc += l
        layer = cv2.GaussianBlur(layer, (0, 0), 0.7) * self.ctx.guard[None, :]
        a = layer[..., None] * 0.95 * (1 - wash)
        canvas[:] = canvas * (1 - a) + np.array([0.62, 0.08, 0.05], np.float32) * a


# --------------------------------------------------------------------------- fields
class Smoke:
    """Battle smoke across all three walls (a FIELD: it may cross the seams). Placeholder for S6-SMOKE."""

    def __init__(self, ctx, seed=6, speed=1.0):
        self.ctx = ctx
        H, W, s = ctx.H, ctx.W, ctx.s
        self.va, self.vb = (22 * s * speed, 9 * s * speed), (9 * s * speed, 4 * s * speed)
        pa = (int(W + DUR * self.va[0]) + 8, int(H + DUR * self.va[1]) + 8)
        pb = (int(W + DUR * self.vb[0]) + 8, int(H + DUR * self.vb[1]) + 8)
        self.a = fractal(pa[1], pa[0], np.random.default_rng(seed),
                         scales=(int(260 * s), int(110 * s), int(44 * s), max(3, int(16 * s))), gains=(1, 0.6, 0.3, 0.12))
        self.b = fractal(pb[1], pb[0], np.random.default_rng(seed + 1), scales=(int(400 * s), int(160 * s), int(60 * s)),
                         gains=(1, 0.5, 0.25))
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        self.under = np.clip(yy * 1.3 - 0.2, 0, 1)
        xs = (np.arange(W) + 0.5) / s
        blue = np.clip(1 - np.abs(xs - 1440) / 900, 0, 1) * (xs < 1440)
        red = np.clip(1 - np.abs(xs - 3240) / 900, 0, 1) * (xs >= 3240)
        white = np.clip(1 - np.abs(xs - 2340) / 1400, 0, 1) * ((xs >= 1440) & (xs < 3240)) * 0.35
        self.spill = (blue[None, :, None] * BLUE * 2.2 + red[None, :, None] * RED * 1.6
                      + white[None, :, None] * WHITE * 0.5).astype(np.float32)

    def draw(self, t, canvas, dens, warm, spill=0.0, cold=0.0):
        if dens <= 0.001:
            return
        W, H = self.ctx.W, self.ctx.H
        a = slide(self.a, W, H, (DUR - t) * self.va[0] + W / 2 + 2, t * self.va[1] + H / 2 + 2)
        b = slide(self.b, W, H, (DUR - t) * self.vb[0] + W / 2 + 2, t * self.vb[1] + H / 2 + 2)
        d = np.clip((0.55 * a + 0.45 * b) * 0.9 + 0.25, 0, 1) ** 1.6 * dens
        dark = np.array([0.055, 0.045, 0.04], np.float32) * (1 - cold) + np.array([0.06, 0.06, 0.065], np.float32) * cold
        lit = np.array([0.42, 0.17, 0.07], np.float32) * warm * (1 - cold) + np.array([0.20, 0.20, 0.21], np.float32) * cold * warm
        col = dark + lit[None, None] * self.under[..., None]
        if spill > 0:
            col = col + self.spill * spill
        canvas[:] = canvas * (1 - d[..., None] * 0.92) + col * d[..., None]


class Particles:
    def __init__(self, ctx, colour, rise=(25, 70), seed=3, blur=1.6, gain=1.4):
        self.ctx, self.rng, self.col, self.rise, self.blur, self.gain = ctx, np.random.default_rng(seed), colour, rise, blur, gain
        self.p = np.zeros((0, 6), np.float32)

    def step(self, t, dt, rate):
        k = self.rng.poisson(rate * dt) if rate > 0 else 0
        if k:
            r = self.rng
            new = np.stack([r.uniform(0, self.ctx.W, k), r.uniform(self.ctx.H * 0.2, self.ctx.H * 1.05, k),
                            r.normal(6, 10, k) * self.ctx.s, -r.uniform(*self.rise, k) * self.ctx.s,
                            r.uniform(2.5, 6, k), r.uniform(0.8, 2.2, k) * max(1, self.ctx.s * 2)], 1)
            self.p = np.concatenate([self.p, new.astype(np.float32)])
        p = self.p
        if len(p):
            p[:, 0] += (p[:, 2] + 14 * self.ctx.s * np.sin(t * 1.7 + p[:, 1] * 0.03)) * dt
            p[:, 1] += p[:, 3] * dt
            p[:, 4] -= dt
            self.p = p[(p[:, 4] > 0) & (p[:, 1] > -10) & (p[:, 1] < self.ctx.H + 10)]

    def draw(self, canvas, t):
        if not len(self.p):
            return
        layer = np.zeros(canvas.shape[:2], np.float32)
        for x, y, vx, vy, life, sz in self.p:
            tw = 0.55 + 0.45 * np.sin(t * 9 + x)
            cv2.circle(layer, (int(x), int(y)), max(1, int(sz)), float(min(1, life / 2) * tw), -1)
        layer = cv2.GaussianBlur(layer, (0, 0), max(0.8, self.blur * self.ctx.s))
        canvas += layer[..., None] * self.col[None, None] * self.gain


# --------------------------------------------------------------------------- type
def text_layer(ctx, text, font, size_full, colour, tracking=0.08):
    size = max(6, ctx.px(size_full))
    f = ImageFont.truetype(os.path.join(FONTS, font), size)
    chars = list(text)
    widths = [f.getbbox(ch)[2] - f.getbbox(ch)[0] if ch.strip() else size * 0.3 for ch in chars]
    track = size * tracking
    W = int(sum(widths) + track * len(chars) + size)
    H = int(size * 1.6)
    im = Image.new('L', (W, H), 0)
    d = ImageDraw.Draw(im)
    x = size * 0.5
    for ch, w in zip(chars, widths):
        d.text((x, size * 0.2), ch, font=f, fill=255)
        x += w + track
    a = np.asarray(im, np.float32) / 255
    ys, xs = np.nonzero(a > 0.02)
    pad = max(4, size // 3)
    a = np.pad(a[ys.min():ys.max() + 1, xs.min():xs.max() + 1], pad)
    rgb = np.ones(a.shape + (3,), np.float32) * colour[None, None]
    return rgb, a


class Word:
    def __init__(self, ctx, text, wall, fx, fy, size_full, t_in, t_out, font='GFSDidot-Regular.ttf',
                 colour=np.array([0.90, 0.86, 0.76], np.float32), tracking=0.14, fade=1.2, shadow=0.75):
        self.rgb, self.a = text_layer(ctx, text, font, size_full, colour, tracking)
        self.sh = cv2.GaussianBlur(self.a, (0, 0), max(1.5, ctx.px(size_full) * 0.18)) * shadow
        x, y = ctx.wall_xy(wall, fx, fy)
        self.ox, self.oy = x - self.a.shape[1] / 2, y - self.a.shape[0] / 2
        self.t_in, self.t_out, self.fade, self.ctx = t_in, t_out, fade, ctx
        self.blur_max = max(1.0, 6 * ctx.s)

    def draw(self, canvas, t):
        if not (self.t_in <= t <= self.t_out + self.fade):
            return
        k = ssf(self.t_in, self.t_in + self.fade, t) * (1 - ssf(self.t_out, self.t_out + self.fade, t))
        a = self.a
        if k < 0.999:
            a = cv2.GaussianBlur(a, (0, 0), self.blur_max * (1 - k) + 0.01)
        if self.sh.max() > 0:
            blit(canvas, np.zeros_like(self.rgb), self.sh * k, self.ox, self.oy, guard=self.ctx.guard)
        blit(canvas, self.rgb, a * k, self.ox, self.oy, guard=self.ctx.guard)


# --------------------------------------------------------------------------- Liberté, Égalité, Fraternité (as v1)
def colour_wall(ctx, wall, col, seed):
    x0, x1 = ctx.wall_px(wall)
    w, h = x1 - x0, ctx.H
    n = fractal(h, w, np.random.default_rng(seed), scales=(max(2, h // 3), max(2, h // 12), max(2, h // 40)), gains=(1, 0.4, 0.15))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.42) / (h / 2)) ** 2)
    img = col[None, None] * (1 + 0.10 * n[..., None]) * np.clip(1.15 - 0.45 * r, 0.35, 1.1)[..., None]
    n_in = np.clip(0.5 * (n * 0.5 + 0.5) + 0.5 * np.clip(r / 1.4, 0, 1), 0, 1)
    g = xx / w if wall == 'L' else (1 - xx / w if wall == 'R' else 1 - np.abs(xx / w - 0.5) * 2)
    n2 = fractal(h, w, np.random.default_rng(seed + 1), scales=(max(2, h // 4), max(2, h // 14)), gains=(1, 0.5))
    n_out = np.clip(0.6 * (1 - g) + 0.4 * (n2 * 0.5 + 0.5), 0, 1)
    return dict(img=img.astype(np.float32), n_in=n_in, n_out=n_out, x=x0, w=w)


def draw_colour_wall(canvas, cw, t, t_in, t_out, dim=1.0):
    if t < t_in:
        return
    a_in = ssf(t_in, t_in + 2.6, t) * 1.2
    rev = np.clip((a_in - cw['n_in']) / 0.08, 0, 1)
    b = ssf(t_out, t_out + 6.0, t) * 1.12 if t > t_out else 0
    alive = np.clip((cw['n_out'] - b) / 0.01, 0, 1) if b > 0 else 1
    img = cw['img'] * dim
    glow = 0
    if b > 0:
        d = cw['n_out'] - b
        char = np.clip(1 - d / 0.06, 0, 1) * (d > 0)
        img = img * (1 - 0.9 * char[..., None])
        rim = np.clip(1 - np.abs(d - 0.005) / 0.01, 0, 1) * (b < 1.1)
        rim = rim * np.clip(np.sin(cw['n_in'] * 60 + t * 1.1) * 0.9 + 0.3, 0, 1)
        glow = rim[..., None] * EMBER[None, None] * 1.3
    a = (rev * alive)[..., None]
    reg = canvas[:, cw['x']:cw['x'] + cw['w']]
    reg[:] = reg * (1 - a) + img * a + glow


# --------------------------------------------------------------------------- the scene
def build(ctx):
    S = {}

    def pr(name, grey=False):
        return tone(load(name), paper=PAPER_GREY if grey else PAPER)[0]

    def gy(name):                                    # an engraving as a multiplier: paper 1, ink ~0
        return np.clip(tone(load(name), paper=np.ones(3, np.float32), ink=np.full(3, 0.04, np.float32), hi_p=85)[0], 0, 1)

    W = []
    # M2: the five battles, washed in large and layered (double exposures), one per name
    W.append(Wash(ctx, pr('battle_austerlitz_DuplessiBertaux'), 'L', 0.50, 0.26, 500, 41.0, 58.5, seed=1, drift=(0, -1.5)))
    W.append(Wash(ctx, pr('battle_wagram_estampe'), 'R', 0.50, 0.31, 680, 43.5, 59.5, seed=2, drift=(0, -1.5)))
    W.append(Wash(ctx, pr('battle_iena_DuplessiBertaux'), 'L', 0.52, 0.56, 640, 46.0, 60.5, seed=3, drift=(0, -2.0)))
    W.append(Wash(ctx, pr('battle_eylau_estampe'), 'R', 0.48, 0.59, 600, 48.5, 61.5, seed=4, drift=(0, -2.0)))
    W.append(Wash(ctx, pr('battle_friedland_1808'), 'C', 0.50, 0.44, 880, 51.0, 62.5, seed=5, drift=(0, -1.5)))
    # M3: Goya, grey, big
    W.append(Wash(ctx, pr('goya_p50_famine_MadreInfeliz', True), 'L', 0.50, 0.45, 960, 60.5, 72.0, seed=6, drift=(0, -1.5)))
    W.append(Wash(ctx, pr('goya_p15_execution_YnoHaiRemedio', True), 'R', 0.50, 0.45, 960, 64.5, 73.5, seed=7, drift=(0, -1.5)))
    W.append(Wash(ctx, pr('goya_p18_death_EnterraryCallar', True), 'C', 0.50, 0.46, 1000, 68.5, 75.0, seed=8, drift=(0, -1.0)))
    # M5: Waterloo on CENTRE, the field after it on LEFT, the ravages on RIGHT
    W.append(Wash(ctx, pr('battle_waterloo_MontStJean_1815'), 'C', 0.50, 0.44, 940, 103.0, 112.0, seed=9, drift=(0, -1.5)))
    W.append(Wash(ctx, pr('battle_waterloo_field_Jazet_1816', True), 'L', 0.50, 0.44, 820, 107.5, 116.5, seed=10, drift=(0, -1.0)))
    W.append(Wash(ctx, pr('goya_p30_ravages_Estragos', True), 'R', 0.50, 0.44, 900, 110.0, 117.5, seed=11, drift=(0, -1.0)))
    # M7: they escape through the flames (CENTRE, as the flags burn)...
    W.append(Wash(ctx, pr('goya_p41_fleeing_EscapanLlamas', True), 'C', 0.50, 0.45, 980, 135.5, 145.0, seed=12, drift=(0, -1.5),
                  out_dur=3.5))
    # ...then the fleeing families ghost into the dawn haze on LEFT and RIGHT, receding toward the ship
    W.append(Wash(ctx, gy('goya_p44_fleeing_YoLoVi'), 'L', 0.46, 0.50, 760, 138.0, 157.0, seed=13, drift=(9, 1.0), grow=-0.008,
                  in_dur=4.0, out_dur=5.0, mode='multiply'))
    W.append(Wash(ctx, gy('goya_p45_fleeing_YestoTambien'), 'R', 0.54, 0.50, 760, 140.0, 157.0, seed=14, drift=(-9, 1.0),
                  grow=-0.008, in_dur=4.0, out_dur=5.0, mode='multiply'))
    S['washes'] = W
    S['flakes'] = Flakes(ctx)
    S['words'] = [
        Word(ctx, 'AUSTERLITZ', 'L', 0.50, 0.44, 46, 41.4, 57.5),
        Word(ctx, 'WAGRAM', 'R', 0.50, 0.50, 46, 43.9, 58.5),
        Word(ctx, 'IÉNA', 'L', 0.50, 0.78, 46, 46.4, 59.5),
        Word(ctx, 'EYLAU', 'R', 0.50, 0.79, 46, 48.9, 60.5),
        Word(ctx, 'FRIEDLAND', 'C', 0.50, 0.78, 52, 51.4, 61.5),
        Word(ctx, 'LIBERTÉ', 'L', 0.50, 0.40, 110, 82.4, 100.0),
        Word(ctx, 'ÉGALITÉ', 'C', 0.50, 0.40, 110, 84.4, 100.0, colour=np.array([0.10, 0.10, 0.16], np.float32), shadow=0),
        Word(ctx, 'FRATERNITÉ', 'R', 0.50, 0.40, 96, 86.4, 100.0),
        Word(ctx, 'WATERLOO', 'C', 0.50, 0.80, 60, 103.4, 110.5),
        Word(ctx, 'MONARCHISTES', 'R', 0.50, 0.76, 58, 124.2, 131.0),
        Word(ctx, 'NAPOLÉONISTES', 'L', 0.50, 0.76, 58, 126.2, 131.0),
        Word(ctx, '1816', 'C', 0.66, 0.26, 230, 150.0, 156.5, font='PinyonScript-Regular.ttf',
             colour=np.array([0.95, 0.92, 0.86], np.float32), tracking=0.02, fade=2.0),
    ]
    S['cwalls'] = [colour_wall(ctx, 'L', BLUE, 21), colour_wall(ctx, 'C', WHITE, 22), colour_wall(ctx, 'R', RED, 23)]
    S['flagC'] = AtmoFlag(ctx, 'C', 'tri', seed=30)
    S['flagL'] = AtmoFlag(ctx, 'L', 'tri', seed=31)
    S['flagR'] = AtmoFlag(ctx, 'R', 'white', seed=32)
    S['smoke'] = Smoke(ctx)
    S['fore'] = Smoke(ctx, seed=16, speed=1.6)
    S['embers'] = Particles(ctx, EMBER)
    S['ash'] = Particles(ctx, ASH, rise=(-12, 10), seed=5, blur=1.2, gain=0.9)
    S['map'] = ContinentMap(ctx)
    ship = cv2.imread(os.path.join(SRC, 'medusa_frigate_Baugean.jpg'))
    g = cv2.cvtColor(ship, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    sh_h = ctx.px(430)
    S['ship'] = cv2.resize(g, (int(g.shape[1] * sh_h / g.shape[0]), sh_h), interpolation=cv2.INTER_AREA)
    hz = np.linspace(0, 1, ctx.H, dtype=np.float32)
    hn = fractal(ctx.H, ctx.W, np.random.default_rng(56), scales=(ctx.px(500), ctx.px(160)), gains=(1, 0.4))
    S['horizon_y'] = 0.56
    S['haze'] = np.exp(-((hz[:, None] - 0.56 - 0.02 * hn) / 0.12) ** 2) * (0.75 + 0.25 * hn)
    S['sky'] = (np.clip(1 - np.abs(hz - 0.56) / 0.40, 0, 1) ** 2)[:, None]
    gy_, gx_ = np.mgrid[0:ctx.H, 0:ctx.W].astype(np.float32)
    glowLR = np.zeros((ctx.H, ctx.W), np.float32)
    for wall in ('L', 'R'):
        x, y = ctx.wall_xy(wall, 0.5, 0.54)
        glowLR += np.exp(-(((gx_ - x) / ctx.px(560)) ** 2 + ((gy_ - y) / ctx.px(300)) ** 2))
    S['glowLR'] = glowLR
    return S


def render_frame(ctx, S, t, dt):
    W, H = ctx.W, ctx.H
    c = np.zeros((H, W, 3), np.float32)
    # the smoke field: coloured by the flag's light in M1-M2, cold and grey in M3, back to fire in M5
    dens = 0.95 * (1 - ssf(12, 24, t)) + 0.55 * ssf(12, 24, t) * (1 - ssf(74, 80, t)) \
        + 0.55 * ssf(98, 104, t) * (1 - ssf(132, 140, t))
    warm = 1.0 * (1 - ssf(20, 60, t)) + 0.35 + 0.45 * ssf(98, 104, t) * (1 - ssf(118, 126, t))
    spill = ssf(8, 16, t) * (1 - ssf(50, 58, t)) * 0.9 + 0.6 * ssf(120, 124, t) * (1 - ssf(131, 136, t))
    cold = ssf(56, 64, t) * (1 - ssf(96, 102, t))
    S['smoke'].draw(t, c, dens, warm, spill=spill, cold=cold)
    # M7 dawn haze (a field) and the light behind the exiles
    hz = ssf(135, 141, t)
    if hz > 0:
        c += S['haze'][..., None] * np.array([0.42, 0.44, 0.48], np.float32) * 0.7 * hz
        c += S['sky'][..., None] * np.array([0.07, 0.08, 0.11], np.float32) * hz
        c += (S['glowLR'] * (ssf(137, 142, t) * (1 - 0.7 * ssf(155, 161, t))))[..., None] * np.array([0.55, 0.55, 0.57], np.float32)
    # M1-M3: the tricolour cloth on CENTRE, behind Friedland, greying with famine, dissolving at death
    if 7 <= t <= 71:
        S['flagC'].draw(c, t, strength=1 - 0.55 * ssf(50, 54, t), reveal=ssf(7, 16, t), grey=ssf(58, 66, t),
                        burn=ssf(66, 71, t) * 1.12)
    # M4-M5: the three colour walls, burning from the inner edges into Waterloo
    if 79 <= t <= 110:
        dim = 1 - 0.25 * ssf(96, 101, t)
        for cw, ti in zip(S['cwalls'], (81.0, 83.0, 85.0)):
            draw_colour_wall(c, cw, t, ti, 101.5, dim)
    # M6: France divided
    if 119.5 <= t <= 137:
        S['flagC'].draw(c, t, reveal=ssf(119.5, 122.5, t), tear=ssf(121.5, 125.5, t), bleach=ssf(124, 127.5, t),
                        burn=ssf(131, 136.5, t) * 1.12)
        S['flagR'].draw(c, t + 3, strength=0.8, reveal=ssf(124, 127, t), burn=ssf(131.5, 137, t) * 1.12)
        S['flagL'].draw(c, t + 7, strength=0.8, reveal=ssf(126, 129, t), burn=ssf(132, 137, t) * 1.12)
    # the pictures, and the fragments that break off them
    for wsh in S['washes']:
        if wsh.active(t):
            wsh.draw(t, c, S['flakes'], dt)
    S['flakes'].draw(c, dt)
    # M7: the continent, 1816, the route; it washes into the dawn; the frigate
    if t >= 147:
        S['map'].draw(c, t, 147.0, ssf(157, 161.5, t))
    if t >= 156:
        ship(ctx, c, S, t)
    for wd in S['words']:
        wd.draw(c, t)
    # a thin smoke in FRONT of everything
    fd = 0.22 * ssf(10, 20, t) * (1 - ssf(74, 80, t)) + 0.22 * ssf(100, 106, t) * (1 - ssf(128, 136, t))
    S['fore'].draw(t, c, fd, warm * 0.8, cold=cold)
    rate = 90 * (1 - ssf(14, 30, t)) + 22 * ssf(14, 30, t) * (1 - ssf(58, 70, t)) + 55 * ssf(100, 104, t) * (1 - ssf(118, 125, t)) \
        + 30 * ssf(131, 133, t) * (1 - ssf(137, 140, t))
    S['embers'].step(t, dt, rate)
    S['embers'].draw(c, t)
    S['ash'].step(t, dt, 60 * ssf(60, 64, t) * (1 - ssf(74, 78, t)) + 70 * ssf(106, 110, t) * (1 - ssf(118, 124, t)))
    S['ash'].draw(c, t)
    return np.clip(c, 0, 1)


def ship(ctx, c, S, t):
    k = ssf(158.5, 163.5, t)
    if k <= 0:
        return
    g = S['ship']
    h, w = g.shape
    x, y = ctx.wall_xy('C', 0.5, S['horizon_y'])
    gy, gx = np.mgrid[0:c.shape[0], 0:c.shape[1]].astype(np.float32)
    glow = np.exp(-(((gx - x) / (w * 0.75)) ** 2 + ((gy - y) / (h * 0.55)) ** 2))
    c += glow[..., None] * np.array([0.55, 0.55, 0.56], np.float32) * ssf(156.5, 162, t)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    edge = np.clip(np.minimum(np.minimum(xx, w - xx), np.minimum(yy, h - yy)) / (h * 0.18), 0, 1)
    rgb = np.repeat((0.08 + 0.92 * g)[..., None], 3, 2).astype(np.float32)
    blit(c, rgb, (edge * k).astype(np.float32), x - w / 2, y - h * 0.84, guard=ctx.guard, mode='multiply')


def caption(ctx, frame, t):
    W, H = frame.shape[1], frame.shape[0]
    sh = max(40, int(H * 0.11)) // 2 * 2
    strip = Image.new('RGB', (W, sh), (18, 18, 20))
    d = ImageDraw.Draw(strip)
    f = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(12, int(sh * 0.36)))
    fs = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(10, int(sh * 0.26)))
    mv = [m for m in MOVES if m[0] <= t][-1][1]
    d.text((10, sh * 0.08), f'{int(t // 60)}:{t % 60:04.1f}   {mv}', font=fs, fill=(150, 150, 150))
    cur = [ln for ln in LINES if ln[0] <= t < ln[0] + 4.5]
    if cur:
        sp, tx = cur[-1][1], cur[-1][2]
        d.text((10, sh * 0.48), (sp + ':  ' if sp else '') + tx, font=f, fill=(230, 225, 210))
    for wall, (x0, x1) in WALLS.items():
        d.text((ctx.px((x0 + x1) / 2) - 20, sh * 0.08), {'L': 'LEFT', 'C': 'CENTRE', 'R': 'RIGHT'}[wall], font=fs, fill=(90, 90, 90))
    img = frame.copy()
    for xs in (1440, 3240):
        x = ctx.px(xs)
        img[:, max(0, x - 1):x + 1] = (70, 70, 70)
    return np.vstack([img, np.asarray(strip)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=0.5)
    ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--end', type=float, default=DUR)
    ap.add_argument('--stills', default=None, help='write PNGs at --at seconds instead of a movie')
    ap.add_argument('--at', type=str, default='')
    a = ap.parse_args()
    ctx = Ctx(a.scale)
    S = build(ctx)
    dt = 1 / FPS
    if a.stills:
        os.makedirs(a.stills, exist_ok=True)
        for ts in [float(v) for v in a.at.split(',')]:
            for i in range(int(3 * FPS), 0, -1):               # run 3 s up to it so particles and fragments exist
                render_frame(ctx, S, max(0.0, ts - i * dt), dt)
            fr = (render_frame(ctx, S, ts, dt) * 255).astype(np.uint8)
            cv2.imwrite(os.path.join(a.stills, f's6_{ts:06.1f}.png'), cv2.cvtColor(caption(ctx, fr, ts), cv2.COLOR_RGB2BGR))
            print('still', ts, flush=True)
        return
    n0, n1 = int(a.start * FPS), int(a.end * FPS)
    sh = max(40, int(ctx.H * 0.11)) // 2 * 2
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{ctx.W}x{ctx.H + sh}',
           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p',
           '-movflags', '+faststart', a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n0, n1):
        t = i / FPS
        fr = (render_frame(ctx, S, t, dt) * 255).astype(np.uint8)
        p.stdin.write(caption(ctx, fr, t).tobytes())
        if i % (FPS * 10) == 0:
            print(f'{t:6.1f} s', flush=True)
    p.stdin.close()
    p.wait()
    print('wrote', a.out)


if __name__ == '__main__':
    main()
