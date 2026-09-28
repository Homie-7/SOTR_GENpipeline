"""Scene 6 (The Napoleonic Wars): the ANIMATIC, across all three walls, from one 4680x1080 timeline.

WHY: Scene 6 is floating imagery over a movement piece (client, 2026-09-28). Before a single credit is
spent, Homie and the client judge the whole scene as a timed animatic: the public-domain engravings,
Goya's etchings, the maps and the frigate, the type, and the scripted effects, in their real places
on the three walls. The generated parts (the flag in smoke, the battle smoke, the fleeing silhouettes)
are PLACEHOLDERS here, drawn by script, and are replaced after the animatic is approved.

The look is LOOK.md "Scene 6" (DRAFT): fragments of paper on black; each one ARRIVES as an ink bloom
and LEAVES by burning (one way, never reversed, D16); colour only in the flag and the fire. The
wall-to-wall rules: fields (smoke, embers, ash, colour, haze) cross the seams, objects never straddle
one; every fragment keeps 300 mm (90 px) clear of its wall's edges.

Timing: our picture leads (~2:45, seven movements, BIBLE.md), the sound designer scores to it.
The review render adds a caption strip under the picture (movement + the spoken line) and marks the
seams; it is not a show file.

  (v1, kept so S6-ANIMATIC_v1 can be rebuilt; v2 is render_s6.py)
  python tools/render_s6_v1.py OUT.mp4 [--scale 0.5] [--start S --end S] [--stills DIR]
"""
import argparse
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

PAPER = np.array([0.80, 0.74, 0.62], np.float32)
PAPER_GREY = np.array([0.66, 0.65, 0.62], np.float32)
INK = np.array([0.09, 0.07, 0.05], np.float32)
EMBER = np.array([1.0, 0.45, 0.12], np.float32)
BLUE = np.array([0.10, 0.17, 0.42], np.float32)
WHITE = np.array([0.80, 0.78, 0.72], np.float32)
RED = np.array([0.60, 0.09, 0.11], np.float32)

# crop boxes, as fractions of each source (x0, y0, x1, y1): the picture only, no margins or titles
CROPS = {
    'battle_austerlitz_DuplessiBertaux': (0.07, 0.10, 0.93, 0.54),
    'battle_wagram_estampe': (0.19, 0.09, 0.82, 0.60),
    'battle_iena_DuplessiBertaux': (0.04, 0.04, 0.97, 0.72),
    'battle_eylau_estampe': (0.19, 0.16, 0.80, 0.67),
    'battle_friedland_1808': (0.04, 0.11, 0.96, 0.62),
    'goya_p50_famine_MadreInfeliz': (0.235, 0.21, 0.74, 0.72),
    'goya_p15_execution_YnoHaiRemedio': (0.26, 0.20, 0.735, 0.77),
    'goya_p18_death_EnterraryCallar': (0.20, 0.195, 0.77, 0.715),
    'battle_waterloo_MontStJean_1815': (0.10, 0.16, 0.90, 0.76),
    'battle_waterloo_field_Jazet_1816': (0.12, 0.13, 0.86, 0.72),
    'map_westafrica_Delisle_1707': (0.15, 0.04, 0.72, 0.62),
    'medusa_frigate_Baugean': (0.0, 0.0, 1.0, 1.0),
}
# the route of the Medusa, in fractions of the WHOLE Delisle map: Cap St-Vincent, Madeira, the Canaries,
# down the coast past Cap Blanc, to the mouth of the Senegal
ROUTE = [(0.355, 0.075), (0.31, 0.19), (0.275, 0.29), (0.235, 0.40), (0.215, 0.47), (0.222, 0.555)]

# the spoken text (script, Scene 6), for the review caption strip only
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

    def px(self, v):
        return int(round(v * self.s))

    def wall_xy(self, wall, fx, fy):
        x0, x1 = WALLS[wall]
        return (x0 + fx * (x1 - x0)) * self.s, fy * FULL_H * self.s


def load_print(name):
    """A source print as warm ink on aged paper (colour prints go monochrome: LOOK Scene 6)."""
    im = cv2.imread(os.path.join(SRC, name + '.jpg'))
    h, w = im.shape[:2]
    x0, y0, x1, y1 = CROPS[name]
    im = im[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
    return im


def tone(im, grey=False, paper=None):
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    lo, hi = np.percentile(g, 1.5), np.percentile(g, 92)
    t = np.clip((g - lo) / (hi - lo + 1e-6), 0, 1) ** 0.9
    pap = paper if paper is not None else (PAPER_GREY if grey else PAPER)
    return INK[None, None] * (1 - t[..., None]) + pap[None, None] * t[..., None]


class Frag:
    """One piece of paper: inks in, drifts slowly toward us, burns away from one side."""

    def __init__(self, ctx, rgb, wall, cx, cy, h_full, t_in, t_out, in_dur=2.4, out_dur=3.2,
                 drift=(0.0, -3.0), burn_from='inner', seed=0, name=''):
        self.ctx, self.wall, self.t_in, self.t_out = ctx, wall, t_in, t_out
        self.in_dur, self.out_dur, self.drift, self.name = in_dur, out_dur, drift, name
        hh = max(8, ctx.px(h_full))
        ww = max(8, int(round(rgb.shape[1] * hh / rgb.shape[0])))
        self.rgb = cv2.resize(rgb, (ww, hh), interpolation=cv2.INTER_AREA).astype(np.float32)
        self.h, self.w = hh, ww
        self.cx, self.cy = ctx.wall_xy(wall, cx, cy)
        rng = np.random.default_rng(seed + 7)
        yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
        r = np.sqrt(((xx - ww / 2) / (ww / 2)) ** 2 + ((yy - hh / 2) / (hh / 2)) ** 2) / 1.42
        sc = max(2, int(hh / 6))
        n = fractal(hh, ww, rng, scales=(sc, max(2, sc // 3), max(2, sc // 9)), gains=(1, 0.45, 0.2))
        self.n_in = np.clip(0.55 * (n * 0.5 + 0.5) + 0.45 * r, 0, 1)            # blooms from the middle
        side = {'inner': ('R' if wall == 'L' else 'L' if wall == 'R' else 'B'), 'left': 'L', 'right': 'R',
                'top': 'T', 'bottom': 'B'}[burn_from]
        grad = {'L': xx / ww, 'R': 1 - xx / ww, 'T': yy / hh, 'B': 1 - yy / hh}[side]
        if side == 'B' and wall == 'C' and burn_from == 'inner':          # CENTRE: from both edges
            grad = 1 - np.abs(xx / ww - 0.5) * 2
        n2 = fractal(hh, ww, np.random.default_rng(seed + 99), scales=(sc, max(2, sc // 3), max(2, sc // 8)),
                     gains=(1, 0.5, 0.25))
        self.n_out = np.clip(0.55 * grad + 0.45 * (n2 * 0.5 + 0.5), 0, 1)
        # torn paper edge: never a clean rectangle
        e = fractal(hh, ww, np.random.default_rng(seed + 5), scales=(max(2, sc // 2), max(2, sc // 6)), gains=(1, 0.5))
        dist = np.minimum(np.minimum(xx, ww - 1 - xx), np.minimum(yy, hh - 1 - yy)) / max(4, hh * 0.035)
        self.edge = np.clip(dist + 0.9 * e - 0.4, 0, 1)
        # aged paper: darker toward the edges, faint mottling
        mott = fractal(hh, ww, np.random.default_rng(seed + 11), scales=(max(2, sc), max(2, sc // 4)), gains=(1, 0.4))
        self.rgb *= (0.86 + 0.14 * np.clip(1.2 - r, 0, 1))[..., None] * (1 + 0.05 * mott)[..., None]
        self.check_margins()

    def check_margins(self):
        x0, x1 = WALLS[self.wall]
        life = self.t_out + self.out_dur - self.t_in
        for t in (0, life):
            cx = self.cx / self.ctx.s + self.drift[0] * t
            lo, hi = cx - self.w / self.ctx.s / 2, cx + self.w / self.ctx.s / 2
            if lo < x0 + MARGIN - 1 or hi > x1 - MARGIN + 1:
                print(f'  WARNING {self.name}: outside the 300 mm margin of {self.wall} ({lo:.0f}-{hi:.0f})')

    def active(self, t):
        return self.t_in <= t <= self.t_out + self.out_dur

    def draw(self, t, canvas, sparks):
        tt = t - self.t_in
        ox = self.cx + self.drift[0] * tt * self.ctx.s - self.w / 2
        oy = self.cy + self.drift[1] * tt * self.ctx.s - self.h / 2
        a_in = ssf(0, 1, (t - self.t_in) / self.in_dur) * 1.25
        rev = np.clip((a_in - self.n_in) / 0.06, 0, 1)
        front = np.clip(1 - np.abs(a_in - self.n_in - 0.03) / 0.05, 0, 1) * (a_in < 1.2)
        b = ssf(0, 1, (t - self.t_out) / self.out_dur) * 1.15 if t > self.t_out else 0.0
        alive = np.clip((self.n_out - b) / 0.012, 0, 1) if b > 0 else 1.0
        rgb = self.rgb * (1 - 0.65 * front)[..., None]                      # ink-soaked bloom front
        if b > 0:
            d = self.n_out - b
            char = np.clip(1 - d / 0.07, 0, 1) * (d > 0)
            rgb = rgb * (1 - 0.85 * char[..., None]) + np.array([0.12, 0.06, 0.02]) * 0.85 * char[..., None] * 0.3
            rim = np.clip(1 - np.abs(d - 0.006) / 0.012, 0, 1) * (b < 1.12)
            rim = rim * np.clip(np.sin(self.n_in * 55 + t * 1.3) * 0.9 + 0.35, 0, 1)
            flick = 0.7 + 0.3 * np.sin(t * 13 + self.n_in * 40)
            glow = (rim * flick)[..., None] * EMBER[None, None] * 1.6
            ys, xs = np.nonzero(rim > 0.7)
            if len(xs):
                k = self.ctx.rng.integers(0, len(xs), size=min(3, len(xs)))
                for i in k:
                    sparks.append((ox + xs[i], oy + ys[i]))
        else:
            glow = None
        alpha = (rev * self.edge * alive).astype(np.float32)
        blit(canvas, rgb, alpha, ox, oy, glow)


def blit(canvas, rgb, alpha, ox, oy, add=None):
    """Composite rgb/alpha at a sub-pixel position (and an additive glow layer)."""
    H, W = canvas.shape[:2]
    ix, iy = int(np.floor(ox)), int(np.floor(oy))
    fx, fy = ox - ix, oy - iy
    h, w = alpha.shape
    M = np.float32([[1, 0, fx], [0, 1, fy]])
    pad = 2
    stack = np.dstack([rgb, alpha[..., None]] + ([add] if add is not None else [])).astype(np.float32)
    sh = cv2.warpAffine(stack, M, (w + pad, h + pad), flags=cv2.INTER_LINEAR, borderValue=0)
    x0, y0 = max(0, ix), max(0, iy)
    x1, y1 = min(W, ix + w + pad), min(H, iy + h + pad)
    if x1 <= x0 or y1 <= y0:
        return
    sub = sh[y0 - iy:y1 - iy, x0 - ix:x1 - ix]
    a = sub[..., 3:4]
    region = canvas[y0:y1, x0:x1]
    region[:] = region * (1 - a) + sub[..., :3] * a
    if add is not None:
        region[:] += sub[..., 4:7]


class Smoke:
    """Battle smoke across all three walls (a FIELD: it may cross the seams). Placeholder for S6-SMOKE."""

    def __init__(self, ctx):
        self.ctx = ctx
        H, W = ctx.H, ctx.W
        s = ctx.s
        self.va, self.vb = (22 * s, 9 * s), (9 * s, 4 * s)                   # px/s: the smoke drifts right and up
        pa = (int(W + DUR * self.va[0]) + 8, int(H + DUR * self.va[1]) + 8)
        pb = (int(W + DUR * self.vb[0]) + 8, int(H + DUR * self.vb[1]) + 8)
        self.a = fractal(pa[1], pa[0], np.random.default_rng(6),
                         scales=(int(260 * s), int(110 * s), int(44 * s), max(3, int(16 * s))), gains=(1, 0.6, 0.3, 0.12))
        self.b = fractal(pb[1], pb[0], np.random.default_rng(7), scales=(int(400 * s), int(160 * s), int(60 * s)),
                         gains=(1, 0.5, 0.25))
        yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
        self.under = np.clip(yy * 1.3 - 0.2, 0, 1)                           # lit from the fires below

    def draw(self, t, canvas, dens, warm, pale=0.0):
        if dens <= 0.001:
            return
        W, H = self.ctx.W, self.ctx.H
        # the window slides left and down over the field, so the smoke moves right and up; never wraps
        a = cv2.getRectSubPix(self.a, (W, H), ((DUR - t) * self.va[0] + W / 2 + 2, t * self.va[1] + H / 2 + 2))
        b = cv2.getRectSubPix(self.b, (W, H), ((DUR - t) * self.vb[0] + W / 2 + 2, t * self.vb[1] + H / 2 + 2))
        d = np.clip((0.55 * a + 0.45 * b) * 0.9 + 0.25, 0, 1) ** 1.6 * dens
        dark = np.array([0.055, 0.045, 0.04], np.float32)
        lit = np.array([0.42, 0.17, 0.07], np.float32) * warm
        pal = np.array([0.36, 0.37, 0.40], np.float32) * pale
        col = dark + (lit[None, None] * self.under[..., None]) + pal
        canvas[:] = canvas * (1 - d[..., None] * 0.92) + col * d[..., None]


class Embers:
    def __init__(self, ctx, n=260):
        self.ctx, self.rng = ctx, np.random.default_rng(3)
        self.p = np.zeros((0, 6), np.float32)            # x, y, vx, vy, life, size
        self.n = n

    def spawn(self, k, x=None, y=None):
        r = self.rng
        xs = r.uniform(0, self.ctx.W, k) if x is None else np.full(k, x) + r.normal(0, 2, k)
        ys = r.uniform(self.ctx.H * 0.55, self.ctx.H * 1.05, k) if y is None else np.full(k, y)
        new = np.stack([xs, ys, r.normal(6, 10, k) * self.ctx.s, -r.uniform(25, 70, k) * self.ctx.s,
                        r.uniform(2.5, 6, k), r.uniform(0.8, 2.2, k) * max(1, self.ctx.s * 2)], 1)
        self.p = np.concatenate([self.p, new.astype(np.float32)])

    def step(self, t, dt, rate):
        k = self.rng.poisson(rate * dt) if rate > 0 else 0
        if k:
            self.spawn(k)
        p = self.p
        if len(p):
            p[:, 0] += (p[:, 2] + 14 * self.ctx.s * np.sin(t * 1.7 + p[:, 1] * 0.03)) * dt
            p[:, 1] += p[:, 3] * dt
            p[:, 4] -= dt
            self.p = p[(p[:, 4] > 0) & (p[:, 1] > -10)]

    def draw(self, canvas, t):
        if not len(self.p):
            return
        layer = np.zeros(canvas.shape[:2], np.float32)
        for x, y, vx, vy, life, sz in self.p:
            tw = 0.55 + 0.45 * np.sin(t * 9 + x)
            cv2.circle(layer, (int(x), int(y)), max(1, int(sz)), float(min(1, life / 2) * tw), -1)
        layer = cv2.GaussianBlur(layer, (0, 0), max(0.8, 1.6 * self.ctx.s))
        canvas += layer[..., None] * EMBER[None, None] * 1.4


class Flag:
    """PLACEHOLDER for S6-FLAG (generated later): a tricolour moving in the wind, pole on the left."""

    def __init__(self, ctx, h_full=520, colours=(BLUE, WHITE, RED)):
        self.ctx = ctx
        self.h = ctx.px(h_full)
        self.w = int(self.h * 1.5)
        cloth = np.zeros((self.h, self.w, 3), np.float32)
        for i, c in enumerate(colours):
            cloth[:, i * self.w // 3:(i + 1) * self.w // 3] = c
        weave = fractal(self.h, self.w, np.random.default_rng(12), scales=(max(2, self.h // 5), max(2, self.h // 20)),
                        gains=(1, 0.4))
        self.cloth = cloth * (1 + 0.06 * weave[..., None])
        yy, xx = np.mgrid[0:self.h, 0:self.w].astype(np.float32)
        self.xx, self.yy = xx, yy
        sc = max(2, self.h // 6)
        nz = fractal(self.h, self.w, np.random.default_rng(31), scales=(sc, sc // 3 + 1), gains=(1, 0.5)) * 0.5 + 0.5
        self.n_out = np.clip(0.7 * (1 - xx / self.w) + 0.3 * nz, 0, 1)      # burns from the fly end toward the pole

    def render(self, t, burn=0.0, grey=0.0):
        k = 2 * np.pi / (self.w * 0.55)
        amp = self.h * 0.045 * (self.xx / self.w) ** 0.8
        ph = k * self.xx - t * 2.6
        dy = amp * np.sin(ph) + amp * 0.35 * np.sin(1.9 * ph + 1.3 + self.yy * 0.01)
        mx = self.xx
        my = self.yy - dy
        img = cv2.remap(self.cloth, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR,
                        borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        alpha = cv2.remap(np.ones((self.h, self.w), np.float32), mx.astype(np.float32), my.astype(np.float32),
                          cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        slope = np.cos(ph) * amp * k
        shade = np.clip(1 + 1.8 * slope, 0.45, 1.35)
        img = img * shade[..., None]
        if grey:
            g = img.mean(2, keepdims=True)
            img = img * (1 - grey) + g * grey * 0.6
        glow = None
        if burn > 0:
            d = self.n_out - burn
            alpha = alpha * np.clip(d / 0.012, 0, 1)
            char = np.clip(1 - d / 0.08, 0, 1) * (d > 0)
            img = img * (1 - 0.85 * char[..., None])
            rim = np.clip(1 - np.abs(d - 0.006) / 0.012, 0, 1) * (burn < 1.1)
            rim = rim * np.clip(np.sin(self.n_out * 70 + t * 1.2) * 0.9 + 0.3, 0, 1)
            glow = rim[..., None] * EMBER[None, None] * 1.4
        # the pole
        pw = max(2, self.h // 70)
        img[:, :pw] = 0.10
        alpha[:, :pw] = 1
        return img, alpha, glow


class Walker:
    """PLACEHOLDER for S6-EXILE: a crude cut-paper figure walking in profile."""

    def __init__(self, kind, x, y, h, speed, t0, direction, fade_x0, fade_x1):
        self.kind, self.x, self.y, self.h, self.v, self.t0 = kind, x, y, h, speed, t0
        self.d, self.f0, self.f1 = direction, fade_x0, fade_x1

    def draw(self, mask, t):
        if t < self.t0:
            return 0
        tt = t - self.t0
        x = self.x + self.d * self.v * tt
        h = self.h
        ph = tt * (2.2 if self.kind != 'child' else 3.0) * 2 * np.pi / 2
        bob = abs(np.sin(ph)) * h * 0.015
        y = self.y - bob
        vis = float(np.clip((self.f1 - x) / (self.f1 - self.f0), 0, 1)) if self.d > 0 else \
            float(np.clip((x - self.f1) / (self.f0 - self.f1), 0, 1))
        if vis <= 0:
            return 0
        c = 1.0
        hr = h * 0.075
        cv2.circle(mask, (int(x), int(y - h + hr)), max(1, int(hr)), c, -1)
        top, hip = y - h + 2 * hr, y - h * 0.47
        sw = h * 0.11
        body = np.array([[x - sw * 0.8, top], [x + sw * 0.8, top], [x + sw, hip], [x - sw, hip]], np.int32)
        if self.kind in ('woman', 'cantiniere'):
            body = np.array([[x - sw * 0.7, top], [x + sw * 0.7, top], [x + sw * 1.8, y - h * 0.05],
                             [x - sw * 1.6, y - h * 0.05]], np.int32)
        cv2.fillPoly(mask, [body], c)
        lw = max(1, int(h * 0.05))
        for s in (1, -1):
            a = s * 0.38 * np.sin(ph)
            kx, ky = x + np.sin(a) * h * 0.47, hip + np.cos(a) * h * 0.47
            cv2.line(mask, (int(x), int(hip)), (int(kx), int(min(ky, y))), c, lw)
            ax = x + np.sin(-a * 0.8) * h * 0.3
            cv2.line(mask, (int(x), int(top + hr)), (int(ax), int(top + h * 0.3)), c, max(1, lw - 1))
        if self.kind == 'soldier':
            cv2.line(mask, (int(x + self.d * sw * 1.5), int(top)), (int(x + self.d * sw * 2.2), int(y)), c, max(1, lw - 1))
        if self.kind in ('woman', 'bundle'):
            cv2.circle(mask, (int(x - self.d * sw * 1.2), int(top + h * 0.12)), max(1, int(h * 0.1)), c, -1)
        if self.kind == 'cantiniere':
            cv2.ellipse(mask, (int(x - self.d * sw * 1.4), int(hip - h * 0.05)), (max(1, int(h * 0.08)), max(1, int(h * 0.1))),
                        0, 0, 360, c, -1)
        return vis


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
    a = a[max(0, ys.min() - 2):ys.max() + 3, max(0, xs.min() - 2):xs.max() + 3]
    rgb = np.ones(a.shape + (3,), np.float32) * colour[None, None]
    return rgb, a


class Word:
    def __init__(self, ctx, text, wall, fx, fy, size_full, t_in, t_out, font='GFSDidot-Regular.ttf',
                 colour=np.array([0.86, 0.82, 0.72], np.float32), tracking=0.12, fade=1.2):
        self.rgb, self.a = text_layer(ctx, text, font, size_full, colour, tracking)
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
        blit(canvas, self.rgb, a * k, self.ox, self.oy)


def colour_wall(ctx, wall, col, seed):
    x0, x1 = WALLS[wall]
    w, h = ctx.px(x1 - x0), ctx.H
    rng = np.random.default_rng(seed)
    n = fractal(h, w, rng, scales=(max(2, h // 3), max(2, h // 12), max(2, h // 40)), gains=(1, 0.4, 0.15))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.42) / (h / 2)) ** 2)
    img = col[None, None] * (1 + 0.10 * n[..., None]) * np.clip(1.15 - 0.45 * r, 0.35, 1.1)[..., None]
    n_in = np.clip(0.5 * (n * 0.5 + 0.5) + 0.5 * np.clip(r / 1.4, 0, 1), 0, 1)
    if wall == 'L':
        g = xx / w
    elif wall == 'R':
        g = 1 - xx / w
    else:
        g = 1 - np.abs(xx / w - 0.5) * 2
    n2 = fractal(h, w, np.random.default_rng(seed + 1), scales=(max(2, h // 4), max(2, h // 14)), gains=(1, 0.5))
    n_out = np.clip(0.6 * (1 - g) + 0.4 * (n2 * 0.5 + 0.5), 0, 1)       # burns from the inner edge(s)
    return dict(img=img.astype(np.float32), n_in=n_in, n_out=n_out, x=ctx.px(x0), w=w)


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


def build(ctx):
    s = {}

    def pr(name, grey=False):
        return tone(load_print(name), grey=grey)
    F = []
    # M2: the five battles, a growing collage; they burn in M3
    F.append(Frag(ctx, pr('battle_austerlitz_DuplessiBertaux'), 'L', 0.40, 0.25, 260, 41.0, 58.5, seed=1, name='Austerlitz',
                  drift=(1.0, -1.5)))
    F.append(Frag(ctx, pr('battle_wagram_estampe'), 'R', 0.62, 0.26, 300, 43.5, 59.5, seed=2, name='Wagram', drift=(-1.0, -1.5)))
    F.append(Frag(ctx, pr('battle_iena_DuplessiBertaux'), 'L', 0.63, 0.60, 320, 46.0, 60.5, seed=3, name='Iéna', drift=(-1.0, -2.0)))
    F.append(Frag(ctx, pr('battle_eylau_estampe'), 'R', 0.38, 0.60, 320, 48.5, 61.5, seed=4, name='Eylau', drift=(1.0, -2.0)))
    F.append(Frag(ctx, pr('battle_friedland_1808'), 'C', 0.50, 0.46, 470, 51.0, 62.5, seed=5, name='Friedland', drift=(0, -2.0)))
    # M3: Goya, in grey
    F.append(Frag(ctx, pr('goya_p50_famine_MadreInfeliz', True), 'L', 0.50, 0.40, 470, 60.5, 72.0, seed=6, name='famine',
                  drift=(0, -2.0)))
    F.append(Frag(ctx, pr('goya_p15_execution_YnoHaiRemedio', True), 'R', 0.50, 0.40, 470, 64.5, 73.5, seed=7,
                  name='executions', drift=(0, -2.0)))
    F.append(Frag(ctx, pr('goya_p18_death_EnterraryCallar', True), 'C', 0.50, 0.44, 500, 68.5, 75.0, seed=8, name='death',
                  drift=(0, -1.5)))
    # M5: Waterloo, then the field after it
    F.append(Frag(ctx, pr('battle_waterloo_MontStJean_1815'), 'C', 0.50, 0.43, 520, 103.0, 110.5, seed=9, name='Waterloo',
                  drift=(0, -2.0)))
    F.append(Frag(ctx, pr('battle_waterloo_field_Jazet_1816', True), 'C', 0.50, 0.46, 400, 111.0, 116.5, seed=10,
                  name='Mont-Saint-Jean after', drift=(0, -1.5), out_dur=4.0))
    s['frags'] = F
    s['words'] = [
        Word(ctx, 'AUSTERLITZ', 'L', 0.40, 0.25 + 0.165, 44, 41.4, 57.5),
        Word(ctx, 'WAGRAM', 'R', 0.62, 0.26 + 0.185, 44, 43.9, 58.5),
        Word(ctx, 'IÉNA', 'L', 0.27, 0.60, 44, 46.4, 59.5),
        Word(ctx, 'EYLAU', 'R', 0.74, 0.60, 44, 48.9, 60.5),
        Word(ctx, 'FRIEDLAND', 'C', 0.50, 0.46 + 0.245, 48, 51.4, 61.5),
        Word(ctx, 'LIBERTÉ', 'L', 0.50, 0.40, 110, 82.4, 100.0),
        Word(ctx, 'ÉGALITÉ', 'C', 0.50, 0.40, 110, 84.4, 100.0, colour=np.array([0.10, 0.10, 0.16], np.float32)),
        Word(ctx, 'FRATERNITÉ', 'R', 0.50, 0.40, 96, 86.4, 100.0),
        Word(ctx, 'WATERLOO', 'C', 0.50, 0.43 + 0.27, 56, 103.4, 109.5),
        Word(ctx, '1816', 'C', 0.62, 0.24, 190, 150.0, 156.5, font='PinyonScript-Regular.ttf',
             colour=np.array([0.90, 0.86, 0.76], np.float32), tracking=0.02, fade=2.0),
    ]
    s['cwalls'] = [colour_wall(ctx, 'L', BLUE, 21), colour_wall(ctx, 'C', WHITE, 22), colour_wall(ctx, 'R', RED, 23)]
    s['flag'] = Flag(ctx, 540)
    s['flag_small'] = Flag(ctx, 430)
    s['flag_white'] = Flag(ctx, 430, colours=(WHITE, WHITE, WHITE))
    s['smoke'] = Smoke(ctx)
    s['embers'] = Embers(ctx)
    # the map, with the route drawn in iron-gall ink
    mp = load_print('map_westafrica_Delisle_1707')
    mp = inpaint_stamps(mp)
    s['map'] = Frag(ctx, tone(mp, paper=np.array([0.78, 0.71, 0.58], np.float32)), 'C', 0.50, 0.45, 900, 147.0, 999,
                    in_dur=3.5, seed=12, name='map', drift=(0, -1.0))
    x0, y0, x1, y1 = CROPS['map_westafrica_Delisle_1707']
    s['route'] = [((u - x0) / (x1 - x0), (v - y0) / (y1 - y0)) for u, v in ROUTE]
    # the frigate
    ship = cv2.imread(os.path.join(SRC, 'medusa_frigate_Baugean.jpg'))
    g = cv2.cvtColor(ship, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255
    sh_h = ctx.px(430)
    sh_w = int(g.shape[1] * sh_h / g.shape[0])
    s['ship'] = cv2.resize(g, (sh_w, sh_h), interpolation=cv2.INTER_AREA)
    # the fleeing silhouettes (placeholders)
    s['walkers'] = walkers(ctx)
    hz = np.linspace(0, 1, ctx.H, dtype=np.float32)
    s['horizon_y'] = 0.56
    hn = fractal(ctx.H, ctx.W, np.random.default_rng(56), scales=(ctx.px(500), ctx.px(160)), gains=(1, 0.4))
    s['haze'] = np.exp(-((hz[:, None] - 0.56 - 0.02 * hn) / 0.12) ** 2) * (0.75 + 0.25 * hn)
    s['sky'] = (np.clip(1 - np.abs(hz - 0.56) / 0.40, 0, 1) ** 2)[:, None]
    return s


def inpaint_stamps(im):
    """Remove the library stamps (blue and red ink) that sit in the map's Atlantic."""
    h, w = im.shape[:2]
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    b, g, r = [im[..., i].astype(int) for i in range(3)]
    col = ((b - r > 18) | (r - g > 45)) & (hsv[..., 1] > 40)
    box = np.zeros((h, w), bool)
    box[int(0.75 * h):int(0.92 * h), :int(0.12 * w)] = True        # the stamps, in crop coordinates
    m = (col & box).astype(np.uint8) * 255
    m = cv2.dilate(m, np.ones((9, 9), np.uint8))
    return cv2.inpaint(im, m, 7, cv2.INPAINT_TELEA)


def walkers(ctx):
    rng = np.random.default_rng(1815)
    W = []
    kinds = ['soldier', 'woman', 'child', 'bundle', 'cantiniere', 'soldier', 'bundle', 'woman']
    hy = 0.56 * ctx.H
    for wall, d in (('L', 1), ('R', -1)):
        x0, x1 = [ctx.px(v) for v in WALLS[wall]]
        for i in range(9):
            t0 = 138 + i * 2.1 + rng.uniform(-0.5, 0.5)
            h = ctx.px(rng.uniform(190, 235)) * (0.62 if kinds[i % 8] == 'child' else 1)
            start = x0 + ctx.px(MARGIN) if d > 0 else x1 - ctx.px(MARGIN)
            inner0 = x1 - ctx.px(MARGIN) - ctx.px(420) if d > 0 else x0 + ctx.px(MARGIN) + ctx.px(420)
            inner1 = x1 - ctx.px(MARGIN) if d > 0 else x0 + ctx.px(MARGIN)
            W.append((wall, Walker(kinds[i % 8], start, hy + ctx.px(rng.uniform(10, 40)), h, ctx.px(rng.uniform(60, 80)),
                                   t0, d, inner0, inner1)))
    return W


def render_frame(ctx, s, t, dt):
    W, H = ctx.W, ctx.H
    c = np.zeros((H, W, 3), np.float32)
    # ---- fields that cross the walls: smoke, embers, haze ----
    dens = 0.95 * (1 - ssf(12, 24, t)) + 0.35 * ssf(12, 24, t) * (1 - ssf(55, 66, t)) \
        + 0.30 * ssf(98, 104, t) * (1 - ssf(118, 126, t))
    warm = 1.0 * (1 - ssf(20, 60, t)) + 0.35 + 0.4 * ssf(98, 104, t) * (1 - ssf(116, 124, t))
    s['smoke'].draw(t, c, dens, warm)
    # M7: the dawn haze band and the sea (fields: they cross)
    hz = ssf(136, 141, t)
    if hz > 0:
        band = s['haze'][..., None] * np.array([0.42, 0.44, 0.48], np.float32) * 0.7 * hz
        sky = s['sky'][..., None] * np.array([0.07, 0.08, 0.11], np.float32) * hz
        c += band + sky
    # ---- M1-M3: the tricolour on CENTRE ----
    if 7 <= t <= 53:
        img, a, glow = s['flag'].render(t)
        k = ssf(8, 15, t) * (1 - ssf(48.5, 52.5, t))
        x, y = ctx.wall_xy('C', 0.5, 0.43)
        blit(c, img, a * k, x - img.shape[1] / 2, y - img.shape[0] / 2, None if glow is None else glow * k)
    # ---- M4-M5: the three colour walls, then they burn from the inner edges ----
    if 79 <= t <= 110:
        dim = 1 - 0.25 * ssf(96, 101, t)
        for cw, ti in zip(s['cwalls'], (81.0, 83.0, 85.0)):
            draw_colour_wall(c, cw, t, ti, 101.5 + (0 if cw['x'] > 0 else 0.6), dim)
    # ---- M6: France divided ----
    if 123 <= t <= 137:
        img, a, glow = s['flag_white'].render(t * 0.8, burn=ssf(132, 136.5, t) * 1.12)
        k = ssf(124, 126, t)
        x, y = ctx.wall_xy('R', 0.52, 0.42)
        blit(c, img, a * k, x - img.shape[1] / 2, y - img.shape[0] / 2, None if glow is None else glow * k)
        img, a, glow = s['flag_small'].render(t * 1.1, burn=0.45 + ssf(132.5, 137, t) * 0.7, grey=0.25)
        k = ssf(126, 128, t)
        x, y = ctx.wall_xy('L', 0.48, 0.42)
        blit(c, img, a * k, x - img.shape[1] / 2, y - img.shape[0] / 2, None if glow is None else glow * k)
    # ---- the paper fragments ----
    sparks = []
    for f in s['frags']:
        if f.active(t):
            f.draw(t, c, sparks)
    # ---- M7: the map, 1816, the route; the map washes into the sea; the frigate ----
    if t >= 147:
        m = s['map']
        wash = ssf(156, 160.5, t)
        if wash < 1:
            before = c.copy()
            m.draw(t, c, sparks)
            route(ctx, c, m, s['route'], t)
            if wash > 0:
                c[:] = c * (1 - wash) + before * wash
    if t >= 156:
        ship(ctx, c, s, t)
    # ---- the silhouettes (placeholders): black against the haze, walking into it ----
    if t >= 138:
        for wall, wk in s['walkers']:
            mask = np.zeros((H, W), np.float32)
            vis = wk.draw(mask, t)
            if vis > 0:
                mask = cv2.GaussianBlur(mask, (0, 0), 0.6)
                k = (mask * vis * ssf(0, 1, (t - wk.t0) / 1.5))[..., None]
                c[:] = c * (1 - k) + np.array([0.02, 0.02, 0.025], np.float32) * k
    for wd in s['words']:
        wd.draw(c, t)
    # ---- embers: rising everywhere in M1 and M5, and from every burning edge ----
    rate = 90 * (1 - ssf(14, 30, t)) + 18 * ssf(14, 30, t) * (1 - ssf(58, 70, t)) + 55 * ssf(100, 104, t) * (1 - ssf(118, 125, t))
    em = s['embers']
    em.step(t, dt, rate)
    for sx, sy in sparks[:40]:                               # sparks off every burning edge
        if em.rng.random() < 0.5:
            em.spawn(1, sx, sy)
    em.draw(c, t)
    return np.clip(c, 0, 1)


def route(ctx, c, m, pts, t):
    k = ssf(151, 156, t)
    if k <= 0:
        return
    tt = t - m.t_in
    ox = m.cx + m.drift[0] * tt * ctx.s - m.w / 2
    oy = m.cy + m.drift[1] * tt * ctx.s - m.h / 2
    P = np.array([(ox + u * m.w, oy + v * m.h) for u, v in pts], np.float32)
    seg = np.sqrt(((P[1:] - P[:-1]) ** 2).sum(1))
    L = seg.sum() * k
    layer = np.zeros(c.shape[:2], np.float32)
    acc = 0
    for (a, b), l in zip(zip(P[:-1], P[1:]), seg):
        if acc >= L:
            break
        f = min(1, (L - acc) / l)
        e = a + (b - a) * f
        n = max(2, int(l * f / max(3, 9 * ctx.s)))
        for i in range(n):                                   # a dashed line, as on a chart
            if i % 2 == 0:
                p0, p1 = a + (e - a) * i / n, a + (e - a) * (i + 1) / n
                cv2.line(layer, tuple(np.int32(p0)), tuple(np.int32(p1)), 1.0, max(2, int(6 * ctx.s)), cv2.LINE_AA)
        acc += l
    layer = cv2.GaussianBlur(layer, (0, 0), 0.7)
    ink = np.array([0.42, 0.05, 0.04], np.float32)
    a = layer[..., None] * 0.9
    c[:] = c * (1 - a) + ink * a


def ship(ctx, c, s, t):
    k = ssf(158.5, 163.5, t)
    if k <= 0:
        return
    g = s['ship']
    h, w = g.shape
    x, y = ctx.wall_xy('C', 0.5, s['horizon_y'])
    ox, oy = int(x - w / 2), int(y - h * 0.84)
    x0, y0 = max(0, ox), max(0, oy)
    x1, y1 = min(c.shape[1], ox + w), min(c.shape[0], oy + h)
    sub = g[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
    # the engraving multiplies onto the dawn haze: its paper becomes the haze, its lines stay ink
    yy, xx = np.mgrid[0:sub.shape[0], 0:sub.shape[1]].astype(np.float32)
    edge = np.clip(np.minimum(np.minimum(xx, sub.shape[1] - xx), np.minimum(yy, sub.shape[0] - yy)) / (sub.shape[0] * 0.18), 0, 1)
    a = (edge * k)[..., None]
    gy, gx = np.mgrid[0:c.shape[0], 0:c.shape[1]].astype(np.float32)
    glow = np.exp(-(((gx - x) / (w * 0.75)) ** 2 + ((gy - y) / (h * 0.55)) ** 2))
    c += glow[..., None] * np.array([0.55, 0.55, 0.56], np.float32) * ssf(156.5, 162, t)
    reg = c[y0:y1, x0:x1]
    mult = reg * (0.08 + 0.92 * sub[..., None])
    reg[:] = reg * (1 - a) + mult * a


def caption(ctx, frame, t):
    """Review strip under the picture: seams marked, movement name, the current line."""
    W, H = frame.shape[1], frame.shape[0]
    sh = max(40, int(H * 0.11)) // 2 * 2                    # even: H.264 4:2:0 needs even sizes
    strip = Image.new('RGB', (W, sh), (18, 18, 20))
    d = ImageDraw.Draw(strip)
    f = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(12, int(sh * 0.36)))
    fs = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(10, int(sh * 0.26)))
    mv = [m for m in MOVES if m[0] <= t][-1][1]
    d.text((10, sh * 0.08), f'{int(t // 60)}:{t % 60:04.1f}   {mv}', font=fs, fill=(150, 150, 150))
    cur = [l for l in LINES if l[0] <= t < l[0] + 4.5]
    if cur:
        sp, tx = cur[-1][1], cur[-1][2]
        d.text((10, sh * 0.48), (sp + ':  ' if sp else '') + tx, font=f, fill=(230, 225, 210))
    for wall, (x0, x1) in WALLS.items():
        d.text((ctx.px((x0 + x1) / 2) - 20, sh * 0.08), {'L': 'LEFT', 'C': 'CENTRE', 'R': 'RIGHT'}[wall], font=fs,
               fill=(90, 90, 90))
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
    ap.add_argument('--stills', help='write one PNG per listed second instead of a movie', default=None)
    ap.add_argument('--at', type=str, default='')
    a = ap.parse_args()
    ctx = Ctx(a.scale)
    s = build(ctx)
    dt = 1 / FPS
    if a.stills:
        os.makedirs(a.stills, exist_ok=True)
        times = [float(v) for v in a.at.split(',')]
        t = 0.0
        # run the particle system forward so embers exist
        for ts in times:
            while t < ts - dt / 2:
                s['embers'].step(t, dt, 0)
                t += dt
            fr = (render_frame(ctx, s, ts, dt) * 255).astype(np.uint8)
            cv2.imwrite(os.path.join(a.stills, f's6_{ts:06.1f}.png'), cv2.cvtColor(caption(ctx, fr, ts), cv2.COLOR_RGB2BGR))
            print('still', ts)
        return
    n0, n1 = int(a.start * FPS), int(a.end * FPS)
    sh = max(40, int(ctx.H * 0.11)) // 2 * 2
    cmd = ['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{ctx.W}x{ctx.H + sh}',
           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p',
           '-movflags', '+faststart', a.out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(n0, n1):
        t = i / FPS
        fr = (render_frame(ctx, s, t, dt) * 255).astype(np.uint8)
        p.stdin.write(caption(ctx, fr, t).tobytes())
        if i % (FPS * 10) == 0:
            print(f'{t:6.1f} s', flush=True)
    p.stdin.close()
    p.wait()
    print('wrote', a.out)


if __name__ == '__main__':
    main()
