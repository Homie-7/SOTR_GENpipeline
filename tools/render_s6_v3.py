"""Scene 6 animatic v3 (kept so v3 can be rebuilt; v4 is render_s6.py). Original docstring follows.

Scene 6 (The Napoleonic Wars): the ANIMATIC, v3, across all three walls, from one 4680x1080 timeline.

WHY: Scene 6 is floating imagery over a movement piece (client, 2026-09-28). The animatic lets Homie and
the client judge the whole scene before any credit is spent. v1 = `render_s6_v1.py`, v2 = `render_s6_v2.py`.
v3 answers Homie's five notes on v2 (LOOK.md Scene 6, the v3 to-do list; plan in docs/S6-V3-PLAN.md):
  1. the flag is a real cloth (ClothFlag): the cloth itself is displaced by waves running hoist -> fly,
     harder at the fly; the outline, the stripes, the tear, the bleach and the burn all live in CLOTH
     coordinates (inverse-mapped each frame), so they ripple and travel with the folds. Crisp stripe seams;
  2. one picture, one word, never overlapping: the battles take turns (the flag leaves CENTRE at 0:40,
     Iéna takes it), every word sits in the dark below its own picture, 1816 sits in the open Atlantic;
     `--check` measures every picture/picture and word/picture overlap across the whole timeline;
  3. nothing is ever static: every picture scales at a constant, linear rate for its whole life (words too,
     the colour walls' mottling drifts, the map pans, the ship approaches);
  4. a physical, consistent burn (PaperBurn): court_burn.py's layering (approved by Homie), in 2D: scorch,
     char, ash lip, a thin sharp rim with crawling hot spots. The front moves at constant speed away from an
     ignition point on the side facing the stage centre, and the ash (Ash) leaves the rim in the SAME
     direction the front travels, and rises;
  5. the map (MapJourney): cropped to the Atlantic coast, France to Senegal; it pans south the whole time
     while the Medusa's course draws down the coast at a constant speed, a glowing point at its head.

Rules kept from LOOK.md "Scene 6": colour only in the flag and the fire; fields (smoke, embers, ash,
haze, coloured light, the Liberté colour walls) may cross the seams; objects never do: every picture,
flag, flake and word fades out inside a 300 mm (90 px) guard at each wall edge (Ctx.guard).
Our picture leads the timing (~2:45); the caption strip under the picture is for review only.

  python tools/render_s6.py OUT.mp4 [--scale 0.5] [--start S --end S] [--stills DIR --at 3,14,...]
  python tools/render_s6.py - --check [--scale 0.25]      (overlap report, no movie)
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
F32 = np.float32

PAPER = np.array([0.66, 0.60, 0.49], F32)
PAPER_GREY = np.array([0.55, 0.54, 0.52], F32)
INK = np.array([0.05, 0.04, 0.03], F32)
EMBER = np.array([1.0, 0.45, 0.12], F32)
EMBER_HOT = np.array([1.0, 0.78, 0.40], F32)
BROWN = np.array([0.50, 0.30, 0.14], F32)
ASH = np.array([0.42, 0.40, 0.37], F32)
BLUE = np.array([0.11, 0.18, 0.46], F32)
WHITE = np.array([0.80, 0.78, 0.72], F32)
RED = np.array([0.64, 0.10, 0.12], F32)
AMBER = np.array([0.98, 0.66, 0.28], F32)

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
# the map's journey: a frame MAP_SPAN degrees of latitude high, centred on MAP_LON, panning south at a constant speed
MAP_SPAN, MAP_LON = 32.0, -18.0
MAP_T0, MAP_LAT0, MAP_SPEED = 147.5, 39.4, 1.82          # s, deg, deg/s
ROUTE_T0, ROUTE_T1 = 149.0, 157.5

LINES = [
    (18.0, 'AGNÈS', "Après vingt-trois années de guerre -"), (20.5, 'AMINA', "After 23 years of war -"),
    (23.5, 'AGNÈS', "J'ai appris à être forte. À être utile. Comme les hommes -"),
    (28.0, 'AMINA', "I learned to be strong. To be useful. Like the men."),
    (32.0, 'AGNÈS', "Pour nos braves, nos glorieux soldats."), (35.0, 'AMINA', "For our brave ones. Our glorious soldiers."),
    (38.0, 'AGNÈS', "Nous avons connu la victoire."), (41.0, 'AGNÈS', "Austerlitz."), (43.5, 'AGNÈS', "Wagram."),
    (46.0, 'AGNÈS', "Iéna."), (50.0, 'AGNÈS', "Eylau."), (52.5, 'AGNÈS', "Friedland."),
    (55.0, 'AMINA', "We fought for France."), (57.0, 'AGNÈS', "Nous avons cru à la victoire -"),
    (58.5, 'AMINA', "We believed in victory."),
    (59.5, 'AGNÈS', "Et puis il y a eu la famine -"), (61.5, 'AMINA', "Famine."),
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

REC = None                       # --check: every tagged blit appends (tag, y0, y1, x0, x1, mask) here


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0 + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


def ssf(e0, e1, x):
    return float(ss(e0, e1, x))


def lin(t0, t1, t):
    return float(np.clip((t - t0) / (t1 - t0), 0, 1))


class Ctx:
    def __init__(self, scale):
        self.s = scale
        self.q = max(0.6, scale)                            # full-res px -> canvas px, never thinner than ~1 px
        self.W, self.H = int(round(FULL_W * scale)), int(round(FULL_H * scale))
        self.rng = np.random.default_rng(1816)
        xs = (np.arange(self.W) + 0.5) / scale
        g = np.zeros(self.W, F32)
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
    g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY).astype(F32) / 255
    lo, hi = np.percentile(g, lo_p), np.percentile(g, hi_p)
    t = np.clip((g - lo) / (hi - lo + 1e-6), 0, 1) ** gamma
    return ink[None, None] * (1 - t[..., None]) + paper[None, None] * t[..., None], t


def blit(canvas, rgb, alpha, ox, oy, add=None, guard=None, mode='over', tag=None):
    """Composite at a sub-pixel position. guard (1D, canvas width) fades objects out at the wall edges."""
    H, W = canvas.shape[:2]
    ix, iy = int(np.floor(ox)), int(np.floor(oy))
    h, w = alpha.shape
    M = np.float32([[1, 0, ox - ix], [0, 1, oy - iy]])
    stack = np.dstack([rgb, alpha[..., None]] + ([add] if add is not None else [])).astype(F32)
    sh = cv2.warpAffine(stack, M, (w + 2, h + 2), flags=cv2.INTER_LINEAR, borderValue=0)
    x0, y0 = max(0, ix), max(0, iy)
    x1, y1 = min(W, ix + w + 2), min(H, iy + h + 2)
    if x1 <= x0 or y1 <= y0:
        return
    sub = sh[y0 - iy:y1 - iy, x0 - ix:x1 - ix]
    a = sub[..., 3:4]
    if guard is not None:
        a = a * guard[None, x0:x1, None]
    if REC is not None and tag:
        REC.append((tag, y0, y1, x0, x1, a[..., 0] > 0.2))
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


def scaled(arr, sc, ow, oh):
    """arr scaled by sc about its centre into an (oh, ow) buffer, the centres aligned exactly."""
    h, w = arr.shape[:2]
    M = np.float32([[sc, 0, (ow - sc * w) / 2], [0, sc, (oh - sc * h) / 2]])
    return cv2.warpAffine(np.ascontiguousarray(arr, F32), M, (ow, oh), flags=cv2.INTER_LINEAR, borderValue=0)


# --------------------------------------------------------------------------- the burn (court_burn.py, in 2D)
class PaperBurn:
    """A burn front crossing paper or cloth at constant speed, away from an ignition point p0.
    Layering from court_burn.py v2 (Homie-approved): brown scorch soaking ahead of the front, a black char
    band of varying width, a pale ash lip, a thin sharp glowing rim with hot spots crawling along it and
    veins in the char. The front's shape (distance + a lacy warp) is FIXED IN THE PAPER, so the advancing
    line eats into it rather than wobbling. (ux, uy) is the direction the front travels at each point:
    the ash leaves that way."""

    def __init__(self, ctx, h, w, p0, seed, valid=None):
        self.ctx, q = ctx, ctx.q
        rng = np.random.default_rng(seed)
        yy, xx = np.mgrid[0:h, 0:w].astype(F32)
        dx, dy = xx - p0[0], yy - p0[1]
        dist = np.sqrt(dx * dx + dy * dy) + 1e-3
        L = float(max(h, w))
        big = fractal(h, w, rng, scales=(max(3, int(L / 3)), max(2, int(L / 9)), max(2, int(L / 22))), gains=(1, 0.5, 0.3))
        mid = fractal(h, w, rng, scales=(max(2, int(40 * q)), max(2, int(16 * q)), max(2, int(6 * q))), gains=(1, 0.55, 0.3))
        fine = fractal(h, w, rng, scales=(max(2, int(5 * q)), 2), gains=(1, 0.6))
        D = dist + 0.11 * L * big + 13 * q * mid + 3.5 * q * fine
        hs = (max(3, int(70 * q)), max(2, int(28 * q)), max(2, int(10 * q)))
        self.F = dict(D=D.astype(F32), ux=(dx / dist).astype(F32), uy=(dy / dist).astype(F32),
                      wm=(fractal(h, w, rng, scales=(max(3, int(60 * q)), max(2, int(20 * q))), gains=(1, 0.5)) * 0.5 + 0.5).astype(F32),
                      fib=fractal(h, w, rng, scales=(max(2, int(5 * q)), 2), gains=(1, 0.7)),
                      h1=fractal(h, w, rng, scales=hs, gains=(1, 0.6, 0.35)), h2=fractal(h, w, rng, scales=hs, gains=(1, 0.6, 0.35)))
        m = np.ones((h, w), bool) if valid is None else valid > 0.05
        Dm = self.F['D'][m]
        self.R0, self.R1 = float(Dm.min()) - 8 * q, float(Dm.max()) + 30 * q

    def sample(self, mx, my):
        return {k: cv2.remap(v, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT) for k, v in self.F.items()}

    def apply(self, rgb, alpha, k, t, F=None):
        """k: 0..1, linear in time (constant speed). Returns rgb, alpha, emitted light, rim (0..1)."""
        F = self.F if F is None else F
        q = self.ctx.q
        v = (F['D'] - (self.R0 + (self.R1 - self.R0) * k)) / q          # full-res px into the paper
        wm, fib = F['wm'], F['fib']
        alive = np.clip((v + 0.8) / 1.6, 0, 1)
        char = 1 - np.clip(v / (3 + 9 * wm), 0, 1) ** 0.7
        scorch = np.exp(-np.clip(v, 0, None) / (14 + 34 * wm)) * (0.75 + 0.25 * fib)
        lip = np.exp(-np.clip(v, 0, None) / 1.3) * (0.45 + 0.55 * np.clip(fib + 0.4, 0, 1)) * alive
        lum = rgb.mean(-1, keepdims=True)
        col = rgb * (1 - 0.7 * scorch[..., None]) + BROWN * 1.25 * lum * 0.7 * scorch[..., None]
        col = col * (1 - 0.93 * char[..., None]) + 0.02 * char[..., None]
        col = col + lip[..., None] * 0.10 * np.array([0.9, 0.88, 0.85], F32)
        hot = F['h1'] * np.cos(t * 0.9) + F['h2'] * np.sin(t * 0.9)
        heat = np.clip((hot + 0.15) * 1.6, 0, 1) ** 1.5 * (0.8 + 0.2 * np.sin(t * 0.7 + fib * 6))
        rim = np.exp(-np.abs(v - 0.6) / 1.5) * (0.38 + 0.9 * heat)
        veins = char * alive * np.clip((hot - 0.35) * 3, 0, 1) * 0.55 * (0.5 + 0.5 * fib)
        g = (np.clip(rim + veins, 0, 1.6) * np.clip(alpha * 1.5, 0, 1))[..., None]
        emit = g * EMBER + np.clip(g - 0.8, 0, None) * (EMBER_HOT - EMBER) * 1.2
        emit = emit + 0.35 * cv2.GaussianBlur(emit, (0, 0), 3 * q)                  # a little bloom, only where lit
        return col.astype(F32), (alpha * alive).astype(F32), emit.astype(F32), (rim * alpha).astype(F32)

    def spawn(self, ash, rim, F, to_canvas, rate, dt):
        """Ash leaves the rim the way the front travels. to_canvas maps local (x, y) -> canvas (x, y)."""
        k = self.ctx.rng.poisson(rate * dt)
        if not k:
            return
        pts = np.argwhere(rim > 0.55)
        if not len(pts):
            return
        for i in self.ctx.rng.integers(0, len(pts), size=min(k, len(pts))):
            y, x = pts[i]
            cx, cy = to_canvas(x, y)
            ash.spawn(cx, cy, float(F['ux'][y, x]), float(F['uy'][y, x]))


class Ash:
    """Burnt flakes off a burn front (court_burn.py's): soft, ragged, textured, tumbling (their width swings
    as they turn), hot when they leave, grey as they cool. They carry on the way the front was travelling,
    slow down, and rise."""

    def __init__(self, ctx, seed=77, cap=700):
        self.ctx, self.rng, self.items, self.cap = ctx, np.random.default_rng(seed), [], cap
        self.grain = fractal(64, 64, np.random.default_rng(seed + 1), scales=(6, 3), gains=(1, 0.6)) * 0.5 + 0.5

    def spawn(self, x, y, ux, uy):
        if len(self.items) >= self.cap:
            return
        r, q, s = self.rng, self.ctx.q, self.ctx.s
        k = int(r.integers(9, 15))
        ang = np.sort(r.uniform(0, 2 * np.pi, k))
        size = r.uniform(2.5, 9) * q * (1.8 if r.uniform() < 0.12 else 1.0)
        rad = size * np.clip(r.normal(1, 0.28, k), 0.35, 1.5)
        poly = np.stack([np.cos(ang) * rad, np.sin(ang) * rad * r.uniform(0.5, 1.0)], 1)
        spd = r.uniform(18, 55) * s
        v = np.array([ux * spd + r.normal(0, 4) * s, uy * spd - r.uniform(6, 20) * s])
        self.items.append(dict(poly=poly, x=float(x), y=float(y), v=v, spin=r.uniform(-2.2, 2.2), tumble=r.uniform(0.6, 2.5),
                               ph=r.uniform(0, 6.3), hot=r.uniform(0.3, 1.8), grey=r.uniform(0.16, 0.36),
                               life=r.uniform(2.5, 5.0), age=0.0, gx=int(r.integers(0, 40)), gy=int(r.integers(0, 40))))

    def draw(self, canvas, dt):
        H, W = canvas.shape[:2]
        s, guard = self.ctx.s, self.ctx.guard
        keep = []
        for f in self.items:
            f['age'] += dt
            if f['age'] >= f['life']:
                continue
            f['v'] *= (1 - 0.25 * dt)
            f['v'][1] -= 5 * s * dt
            f['x'] += f['v'][0] * dt
            f['y'] += f['v'][1] * dt
            a_s = f['age']
            u = a_s / f['life']
            th = f['spin'] * a_s
            R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
            turn = 0.25 + 0.75 * abs(np.cos(f['tumble'] * a_s + f['ph']))
            pts = f['poly'] * [turn, 1] @ R.T * (1 - 0.3 * u) + [f['x'], f['y']]
            x0, y0 = int(pts[:, 0].min()) - 3, int(pts[:, 1].min()) - 3
            x1, y1 = int(pts[:, 0].max()) + 4, int(pts[:, 1].max()) + 4
            if x1 <= 0 or y1 <= 0 or x0 >= W or y0 >= H:
                continue
            keep.append(f)
            m = np.zeros((y1 - y0, x1 - x0), np.uint8)
            cv2.fillPoly(m, [np.round((pts - [x0, y0]) * 4).astype(np.int32)], 255, lineType=cv2.LINE_AA, shift=2)
            m = cv2.GaussianBlur(m.astype(F32) / 255, (0, 0), 0.7)
            tex = cv2.resize(self.grain[f['gy']:f['gy'] + 24, f['gx']:f['gx'] + 24], m.shape[::-1])
            fade = min(1.0, (1 - u) / 0.3, a_s / 0.25)
            cx0, cy0, cx1, cy1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
            mm = m[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0] * fade * guard[None, cx0:cx1]
            tt = tex[cy0 - y0:cy1 - y0, cx0 - x0:cx1 - x0]
            reg = canvas[cy0:cy1, cx0:cx1]
            aa = (mm * (0.55 + 0.45 * tt))[..., None]
            reg[:] = reg * (1 - aa) + aa * (f['grey'] * (0.6 + 0.6 * tt))[..., None] * np.array([1.0, 0.96, 0.9], F32)
            heat = np.exp(-a_s / f['hot'])
            if heat > 0.03:
                reg += (np.clip(mm * (tt * 1.4 - 0.2), 0, 1) * heat)[..., None] * (EMBER * 1.1)
        self.items = keep


# --------------------------------------------------------------------------- the paper fragments that break off
class Flakes:
    """Torn pieces of a picture, cut from its eroding edge, drifting off (while it lives; a burn sheds Ash)."""

    def __init__(self, ctx):
        self.ctx, self.rng, self.items = ctx, np.random.default_rng(44), []

    def spawn(self, src, sx, sy, cx, cy, out):
        if len(self.items) > 420:
            return
        r = self.rng
        sz = max(6, int(r.uniform(8, 26) * self.ctx.s * 2))
        h, w = src.shape[:2]
        if h <= sz or w <= sz:
            return
        x0, y0 = int(np.clip(sx - sz / 2, 0, w - sz)), int(np.clip(sy - sz / 2, 0, h - sz))
        patch = np.ascontiguousarray(src[y0:y0 + sz, x0:x0 + sz], F32)
        n = r.integers(5, 9)
        ang = np.sort(r.uniform(0, 2 * np.pi, n))
        rad = r.uniform(0.25, 0.5, n) * sz
        poly = np.stack([sz / 2 + rad * np.cos(ang), sz / 2 + rad * np.sin(ang)], 1).astype(np.int32)
        m = np.zeros((sz, sz), F32)
        cv2.fillPoly(m, [poly], 1.0)
        m = cv2.GaussianBlur(m, (0, 0), 0.6)
        spd = r.uniform(14, 34) * self.ctx.s
        vel = np.array(out, F32) * spd + np.array([r.normal(0, 4), -r.uniform(4, 14)], F32) * self.ctx.s
        self.items.append(dict(p=patch, m=m, x=cx, y=cy, v=vel, a=r.uniform(0, 360), va=r.uniform(-70, 70),
                               life=r.uniform(2.5, 5.5), age=0.0))

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
            blit(canvas, col, m * (1 - k) ** 1.1, f['x'] - sz / 2, f['y'] - sz / 2, guard=self.ctx.guard)
            keep.append(f)
        self.items = keep


# --------------------------------------------------------------------------- a picture, washed in, no frame
def ignition(wall, w, h):
    """Burns start on the side facing the stage centre (as the colour walls Homie liked): LEFT from its right,
    RIGHT from its left, CENTRE from its middle. The front, and the ash, travel outward from there."""
    return {'L': (w * 1.06, h * 0.5), 'R': (-w * 0.06, h * 0.5), 'C': (w * 0.5, h * 0.55)}[wall]


class Wash:
    """A print as an atmospheric wash: big, organic breathing edges that erode and flake off; it arrives as
    an ink bloom, keeps scaling at a constant rate for its whole life, and leaves by burning (or, for the
    ghosts in the haze, by dissolving)."""

    def __init__(self, ctx, rgb, wall, cx, cy, h_full, t_in, t_out, in_dur=3.0, out_dur=3.5, drift=(0.0, -2.5),
                 grow=0.010, seed=0, flake_rate=7.0, mode='over', name='', exit='burn'):
        self.ctx, self.wall, self.t_in, self.t_out, self.in_dur, self.out_dur = ctx, wall, t_in, t_out, in_dur, out_dur
        self.drift, self.grow, self.flake_rate, self.mode, self.name, self.exit = drift, grow, flake_rate, mode, name, exit
        x0, x1 = WALLS[wall]
        smax = 1 + max(0.0, grow) * (t_out + out_dur - t_in)
        max_w = (x1 - x0 - 2 * MARGIN - 140) / smax                     # full-res px: never nearer a seam than the guard
        h_full = min(h_full, max_w * rgb.shape[0] / rgb.shape[1])
        hh = max(8, ctx.px(h_full))
        ww = max(8, int(round(rgb.shape[1] * hh / rgb.shape[0])))
        self.rgb = np.ascontiguousarray(cv2.resize(rgb, (ww, hh), interpolation=cv2.INTER_AREA), F32)
        self.h, self.w = hh, ww
        self.cx, self.cy = ctx.wall_xy(wall, cx, cy)
        rng = np.random.default_rng(seed + 3)
        yy, xx = np.mgrid[0:hh, 0:ww].astype(F32)
        ex, ey = np.abs(xx - ww / 2) / (ww / 2), np.abs(yy - hh / 2) / (hh / 2)
        r = (ex ** 2.2 + ey ** 2.2) ** (1 / 2.2)
        self.base = 1 - r
        sc = max(3, hh // 4)
        self.big = fractal(hh + 80, ww + 160, rng, scales=(sc, max(3, sc // 3), max(2, sc // 8)), gains=(1, 0.5, 0.25))
        self.fine = fractal(hh, ww, np.random.default_rng(seed + 9), scales=(max(2, sc // 6), max(2, sc // 16)), gains=(1, 0.5))
        n = fractal(hh, ww, np.random.default_rng(seed + 7), scales=(sc, max(2, sc // 3)), gains=(1, 0.45))
        self.n_in = np.clip(0.55 * (n * 0.5 + 0.5) + 0.45 * np.clip(r, 0, 1), 0, 1)
        mott = fractal(hh, ww, np.random.default_rng(seed + 11), scales=(sc, max(2, sc // 5)), gains=(1, 0.4))
        if mode == 'over':
            self.rgb *= (1 + 0.07 * mott)[..., None]
        self.burn = PaperBurn(ctx, hh, ww, ignition(wall, ww, hh), seed + 50, valid=self.base) if exit == 'burn' else None

    def active(self, t):
        return self.t_in <= t <= self.t_out + self.out_dur

    def draw(self, t, canvas, flakes, ash, dt):
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
        rgb = self.rgb * (1 - 0.6 * front)[..., None] if self.mode == 'over' else self.rgb
        alpha = (shape * rev).astype(F32)
        emit = rim = None
        burning = t > self.t_out
        if burning:
            k = lin(self.t_out, self.t_out + self.out_dur, t)
            if self.burn is not None:
                rgb, alpha, emit, rim = self.burn.apply(rgb, alpha, k, t)
            else:                                                      # a ghost dissolves back into the haze
                alpha = alpha * np.clip(((1 - ss(0, 1, k)) * 1.25 - self.n_in) / 0.07, 0, 1)
        sc = 1 + self.grow * tt                                         # constant, linear: nice clean motion
        ow, oh = int(np.ceil(self.w * sc)) + 4, int(np.ceil(self.h * sc)) + 4
        ox = self.cx + self.drift[0] * tt * self.ctx.s
        oy = self.cy + self.drift[1] * tt * self.ctx.s
        blit(canvas, scaled(rgb, sc, ow, oh), scaled(alpha, sc, ow, oh), ox - ow / 2, oy - oh / 2,
             None if emit is None else scaled(emit, sc, ow, oh), guard=self.ctx.guard, mode=self.mode, tag='pic:' + self.name)

        def to_canvas(x, y):
            return ox + (x - self.w / 2) * sc, oy + (y - self.h / 2) * sc
        if rim is not None:
            self.burn.spawn(ash, rim, self.burn.F, to_canvas, 30 * self.ctx.s * 2, dt)
        if self.mode != 'over' or burning:
            return
        rng = self.ctx.rng                                             # fragments break off the eroding edge
        k = rng.poisson(self.flake_rate * dt * min(1.0, tt / 1.5))
        if k:
            band = np.argwhere((alpha > 0.25) & (alpha < 0.65))
            if len(band):
                for i in rng.integers(0, len(band), size=min(k, len(band))):
                    y, x = band[i]
                    o = np.array([x - self.w / 2, y - self.h / 2], F32)
                    o /= np.linalg.norm(o) + 1e-6
                    flakes.spawn(self.rgb, x, y, *to_canvas(x, y), o)


# --------------------------------------------------------------------------- the flag: a real cloth
def periodic_x(f):
    """Make a (h, 2P) noise wrap seamlessly at P along x."""
    P = f.shape[1] // 2
    w = (np.arange(P, dtype=F32) / P)[None, :]
    return np.ascontiguousarray((1 - w) * f[:, P:2 * P] + w * f[:, :P], F32)


class ClothFlag:
    """PLACEHOLDER for S6-FLAG, v3 (Homie: "a real cloth, not shadows animating on a flat").
    The CLOTH moves: a displacement D(u, v, t) of waves running from the hoist to the fly, the fly flapping
    harder (amp ~ u^1.3), swaying along its length (the stripes bend) and fluttering up and down (the
    outline ripples). Each frame is inverse-mapped (c = s - D(c), fixed-point) so the stripes, the weave,
    the outline, the tear, the bleach and the burn all live on the cloth and travel with its folds. Crisp
    seams between the stripes. The hoist dissolves into the smoke (no pole); the fly end frays."""

    def __init__(self, ctx, wall, kind='tri', box=(0.07, 0.05, 0.93, 0.74), seed=0):
        self.ctx, self.wall, self.kind = ctx, wall, kind
        x0, x1 = ctx.wall_px(wall)
        self.x0, self.w, self.h = x0, x1 - x0, ctx.H
        w, h = self.w, self.h
        self.CX0, self.CY0 = box[0] * w, box[1] * h
        CW, CH = (box[2] - box[0]) * w, (box[3] - box[1]) * h
        self.CW, self.CH = CW, CH
        pad = self.pad = int(0.15 * CW)
        tw, th = int(CW) + 2 * pad, int(CH) + 2 * pad
        yy, xx = np.mgrid[0:th, 0:tw].astype(F32)
        cu, cv = xx - pad, yy - pad
        rng = np.random.default_rng(seed)
        if kind == 'tri':
            e = 0.9
            wb = ss(CW / 3 - e, CW / 3 + e, cu)[..., None]
            wr = ss(2 * CW / 3 - e, 2 * CW / 3 + e, cu)[..., None]
            cloth = BLUE * (1 - wb) + WHITE * (wb - wr) + RED * wr
        else:
            cloth = np.ones((th, tw, 3), F32) * WHITE * 0.95
        weave = fractal(th, tw, rng, scales=(max(3, th // 6), max(2, th // 30), 2), gains=(1, 0.35, 0.12))
        self.cloth = np.ascontiguousarray(cloth * 0.92 * (1 + 0.06 * weave[..., None]), F32)
        self.whiteC = np.ascontiguousarray(np.ones((th, tw, 3), F32) * WHITE * (1 + 0.06 * weave[..., None]), F32)
        n = fractal(th, tw, rng, scales=(ctx.px(200), ctx.px(60)), gains=(1, 0.4)) * 0.5 + 0.5
        ex, ey = np.abs(cu / CW - 0.5) * 2, np.abs(cv / CH - 0.5) * 2
        r = (np.clip(ex, 0, 2) ** 3 + np.clip(ey, 0, 2) ** 3) ** (1 / 3)
        n_in = np.clip(0.5 * n + 0.5 * np.clip(r, 0, 1), 0, 1)
        E = fractal(th, tw, rng, scales=(ctx.px(160), ctx.px(50), max(2, ctx.px(14))), gains=(1, 0.5, 0.25))
        self.aux = np.ascontiguousarray(np.dstack([n_in, E, n]), F32)
        self.P = tw
        self.turb = periodic_x(fractal(th, 2 * tw, rng, scales=(ctx.px(420), ctx.px(160), ctx.px(60)), gains=(1, 0.45, 0.15)))
        self.wspd = 0.30 * CW                                      # the wind's pattern speed along the cloth, px/s
        self.tearn = fractal(th, 8, rng, scales=(ctx.px(240), ctx.px(80), max(2, ctx.px(26))), gains=(1, 0.4, 0.12))[:, 0]
        self.fray = fractal(th, 8, rng, scales=(max(2, ctx.px(12)), 2), gains=(1, 0.5))[:, 0]
        p0 = {'C': (pad + CW / 2, pad + CH / 2), 'L': (pad + CW * 1.25, pad + CH / 2), 'R': (pad - CW * 0.25, pad + CH / 2)}[wall]
        inside = ((cu >= 0) & (cu <= CW) & (cv >= 0) & (cv <= CH)).astype(F32)
        self.burnf = PaperBurn(ctx, th, tw, p0, seed + 40, valid=inside)
        gy, gx = np.mgrid[0:h, 0:w].astype(F32)
        self.Xs, self.Ys = gx - self.CX0, gy - self.CY0

    def disp(self, cu, cv, t, side=0.0, tear=0.0):
        CW, CH = self.CW, self.CH
        u, v = cu / CW, cv / CH
        uc = np.clip(u, 0, 1.15)
        T = cv2.remap(self.turb, (cu + self.pad - self.wspd * t) % self.P, cv + self.pad, cv2.INTER_LINEAR,
                      borderMode=cv2.BORDER_REFLECT)
        ph1 = 2 * np.pi * (1.15 * u + 0.30 * v - 0.42 * t) + 0.9 * T
        ph2 = 2 * np.pi * (2.2 * u - 0.45 * v - 0.71 * t) + 1.3 + 0.6 * T
        amp = 0.18 + 0.82 * uc ** 1.3                              # the fly flaps harder than the hoist
        z = amp * (np.sin(ph1) + 0.6 * np.sin(ph2) + 0.3 * T)
        dy = 0.085 * CH * z * (0.25 + 0.75 * uc)
        dx = 0.04 * CW * amp * np.sin(ph1 + 0.7) - 0.025 * CW * amp * (1 + np.sin(ph1)) * uc
        if side:                                                   # torn: the halves pull apart and sag
            dx = dx + side * tear * 0.05 * CW
            dy = dy + tear * 0.035 * CH * np.clip(np.abs(u - 0.5) * 2, 0, 1)
        return dx.astype(F32), dy.astype(F32), z.astype(F32)

    def solve(self, t, side=0.0, tear=0.0):
        cu, cv = self.Xs, self.Ys
        for _ in range(3):
            dx, dy, z = self.disp(cu, cv, t, side, tear)
            cu, cv = self.Xs - dx, self.Ys - dy
        return cu, cv, z

    def render_side(self, t, side, reveal, burn, tear, bleach, grey):
        CW, CH, pad, q = self.CW, self.CH, self.pad, self.ctx.q
        cu, cv, z = self.solve(t, side, tear)
        mx, my = (cu + pad).astype(F32), (cv + pad).astype(F32)
        tex = cv2.remap(self.cloth, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        aux = cv2.remap(self.aux, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        n_in, E, bn = aux[..., 0], aux[..., 1], aux[..., 2]
        u, v = cu / CW, cv / CH
        a = (ss(0, 0.16, u + 0.10 * E) * ss(0, 0.07, (1 - u) + 0.05 * E)
             * ss(0, 0.022, v + 0.008 * E) * ss(0, 0.022, (1 - v) + 0.008 * E))
        a = a * np.clip((reveal * 1.25 - n_in) / 0.12, 0, 1)
        iy = np.clip(my.astype(np.int32), 0, len(self.tearn) - 1)
        tl = 0.5 + 0.035 * self.tearn[iy]
        if bleach > 0:                                              # the Restoration: the right half drains to white
            fr = ss(0, 0.12, bleach * 1.3 - (1 - np.clip((u - 0.5) * 2, 0, 1)) * 0.6 - bn * 0.4) * (u >= tl)
            wimg = cv2.remap(self.whiteC, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            tex = tex * (1 - fr[..., None]) + wimg * fr[..., None]
        if tear > 0:                                                # a torn edge: frayed, a little paler, no fire
            d = (u - tl) * CW * (1 if side > 0 else -1) + 2.5 * q * self.fray[iy]
            a = a * ss(0, 2.0 * q, d)
            tex = tex * (1 + 0.14 * np.exp(-np.clip(d, 0, None) / (3 * q)))[..., None]
        gx = np.gradient(z, axis=1)
        gy = np.gradient(z, axis=0)
        g = (0.8 * gx + 0.5 * gy) * CW / (2 * np.pi * 1.15)
        shade = np.clip(0.93 - 0.42 * g, 0.40, 1.28) * np.clip(0.86 + 0.12 * z, 0.66, 1.06)
        img = tex * shade[..., None] + (np.clip(shade - 1.1, 0, 1)[..., None] * 0.25) * np.array([0.9, 0.88, 0.85], F32)
        if grey > 0:
            img = img * (1 - grey) + img.mean(2, keepdims=True) * 0.55 * grey
        emit = rim = F = None
        if burn > 0:
            F = self.burnf.sample(mx, my)
            img, a, emit, rim = self.burnf.apply(img, a.astype(F32), burn, t, F)
        return img.astype(F32), a.astype(F32), emit, rim, F

    def draw(self, canvas, t, ash=None, dt=0.0, strength=1.0, reveal=1.0, burn=0.0, tear=0.0, bleach=0.0, grey=0.0):
        sides = [0.0] if tear <= 0 else [-1.0, 1.0]
        img = np.zeros((self.h, self.w, 3), F32)
        a = np.zeros((self.h, self.w), F32)
        emit = None
        for side in sides:
            i2, a2, e2, rim, F = self.render_side(t, side, reveal, burn, tear, bleach, grey)
            img += i2 * a2[..., None]
            a += a2
            if e2 is not None:
                emit = e2 if emit is None else emit + e2
                if ash is not None:
                    self.burnf.spawn(ash, rim, F, lambda x, y: (self.x0 + x, y), 45 * self.ctx.s * 2, dt)
        img = img / np.maximum(a, 1e-4)[..., None]
        a = np.clip(a, 0, 1)
        blit(canvas, img, a * strength, self.x0, 0, None if emit is None else emit * strength,
             guard=self.ctx.guard, tag='pic:flag' + self.wall)


# --------------------------------------------------------------------------- the map and the journey
def lonlat_to_bellin(lon, lat, W, H):
    fx = BELLIN_FX[0] * lon + BELLIN_FX[1] * lat + BELLIN_FX[2]
    fy = BELLIN_FY[0] * lon + BELLIN_FY[1] * lat + BELLIN_FY[2]
    return fx * W, fy * H


def map_lat(t):
    return MAP_LAT0 - MAP_SPEED * (t - MAP_T0)


class MapJourney:
    """The Atlantic coast from France to Senegal (Homie's v2 note 5: tighter, always moving, the journey).
    Africa glows like old paper held to a lamp (Bellin's 1740s map inside Natural Earth's outline); Europe
    and the islands are ghosted; the sea keeps Bellin's lettering near the coasts and falls to dark in the
    open ocean, where 1816 sits. The frame pans south at a constant speed the whole time, and the Medusa's
    course draws itself down the coast at a constant speed, a glowing point at its head."""

    def __init__(self, ctx):
        self.ctx = ctx
        x0, x1 = ctx.wall_px('C')
        self.x0, self.w, self.h = x0, x1 - x0, ctx.H
        im = cv2.imread(os.path.join(SRC, 'map_africa_Bellin_1740s.jpg'))
        BH, BW = im.shape[:2]
        self.BW, self.BH = BW, BH
        im = self._inpaint(im)
        self.ppd = self.h / MAP_SPAN                                   # canvas px per degree of latitude
        sc = self.ppd / (-BELLIN_FY[1] * BH)
        bx0, by0 = lonlat_to_bellin(-52, 62, BW, BH)
        bx1, by1 = lonlat_to_bellin(26, -6, BW, BH)
        self.sc, self.bx0, self.by0 = sc, bx0, by0
        CWm, CHm = int((bx1 - bx0) * sc), int((by1 - by0) * sc)
        M = np.float32([[sc, 0, -sc * bx0], [0, sc, -sc * by0]])
        warped = cv2.warpAffine(im, M, (CWm, CHm), flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=(150, 150, 150))
        gj = json.load(open(os.path.join(SRC, 'naturalearth_50m_countries.geojson'), encoding='utf-8'))
        land = np.zeros((CHm, CWm), F32)
        other = np.zeros((CHm, CWm), F32)
        for f in gj['features']:
            cont = f['properties'].get('CONTINENT')
            geom = f['geometry']
            polys = [geom['coordinates']] if geom['type'] == 'Polygon' else geom['coordinates']
            for poly in polys:
                ring = np.array(poly[0])
                if ring[:, 0].max() < -52 or ring[:, 0].min() > 26 or ring[:, 1].max() < -6 or ring[:, 1].min() > 62:
                    continue
                if ring[:, 0].max() < -20 and ring[:, 1].min() > 30:           # the Azores: off the course, in 1816's sea
                    continue
                P = np.c_[self.to_canvas(ring[:, 0], ring[:, 1])]
                cv2.fillPoly(land if cont == 'Africa' else other, [np.int32(P * 4)], 1.0, cv2.LINE_AA, shift=2)
        land = cv2.GaussianBlur(land, (0, 0), 0.8)
        g = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY).astype(F32) / 255
        lo, hi = np.percentile(g, 2), np.percentile(g, 90)
        tt = np.clip((g - lo) / (hi - lo), 0, 1)[..., None]
        land_rgb = np.array([0.20, 0.09, 0.03], F32) * (1 - tt) + AMBER * 0.92 * tt
        sea_rgb = np.array([0.05, 0.05, 0.06], F32) * (1 - tt) + np.array([0.30, 0.29, 0.29], F32) * tt
        oth = cv2.GaussianBlur(other, (0, 0), 0.8)[..., None]
        sea_rgb = sea_rgb * (1 - 0.35 * oth) + land_rgb * 0.35 * oth                      # Europe, the islands: ghosted
        anyland = np.maximum(land, oth[..., 0])
        dist = cv2.distanceTransform((land < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        u = ctx.s * 2
        wl = sum(wgt * np.exp(-((dist - d0 * u) / (0.9 * u)) ** 2) for d0, wgt in ((4, 0.55), (9, 0.35), (15, 0.22), (23, 0.12)))
        coast = np.exp(-((dist - 0.5) / (1.1 * u)) ** 2)
        halo = cv2.GaussianBlur(land, (0, 0), ctx.px(28))
        L = land[..., None]
        img = sea_rgb * (1 - L) + land_rgb * L
        img = img + (wl * (1 - land))[..., None] * np.array([0.40, 0.36, 0.30], F32) * 0.5
        img = img * (1 - 0.55 * coast[..., None]) + (halo * (1 - land))[..., None] * AMBER * 0.28
        self.img = np.ascontiguousarray(img, F32)
        dsea = cv2.distanceTransform((anyland < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        vn = fractal(CHm, CWm, np.random.default_rng(77), scales=(ctx.px(260), ctx.px(80)), gains=(1, 0.4))
        sea_a = np.clip(np.exp(-dsea / (3.5 * self.ppd)) * (0.9 + 0.25 * vn), 0, 1) * 0.8   # dark in the open ocean
        nn = fractal(CHm, CWm, np.random.default_rng(78), scales=(ctx.px(180), ctx.px(50)), gains=(1, 0.45)) * 0.5 + 0.5
        sx, sy = self.to_canvas(MAP_LON, MAP_LAT0)
        yy, xx = np.mgrid[0:CHm, 0:CWm].astype(F32)
        ds = np.sqrt((xx - sx) ** 2 + (yy - sy) ** 2) / self.w
        n_land = np.clip(0.45 * ds * 1.4 + 0.35 * nn, 0, 1)
        n_sea = np.clip(0.35 + 0.35 * ds * 1.2 + 0.3 * nn, 0, 1)
        self.fld = np.ascontiguousarray(np.dstack([land, sea_a, n_land, n_sea]), F32)
        R = np.array([self.to_canvas(lon, lat) for lon, lat in ROUTE_LONLAT], F32)
        self.route = R
        seg = np.sqrt(((R[1:] - R[:-1]) ** 2).sum(1))
        self.seg, self.cum = seg, np.r_[0, np.cumsum(seg)]
        yv, xv = np.mgrid[0:self.h, 0:self.w].astype(F32)
        rr = np.sqrt(((xv - self.w / 2) / (self.w * 0.58)) ** 2 + ((yv - self.h / 2) / (self.h * 0.64)) ** 2)
        self.vig = np.clip(1.25 - rr, 0, 1).astype(F32)
        # the continent dissolves before any frame edge (no hard edge, no rectangle): east, top and bottom
        rl = np.sqrt(((xv - self.w * 0.5) / (self.w * 0.42)) ** 2 + ((yv - self.h * 0.42) / (self.h * 0.5)) ** 2)
        ln = fractal(self.h, self.w, np.random.default_rng(79), scales=(ctx.px(220), ctx.px(70)), gains=(1, 0.45))
        self.lvig = (np.clip((1.12 - rl) * 2.5 + 0.3 * ln, 0, 1) * ss(0, 0.12 * self.h, yv)).astype(F32)

    def to_canvas(self, lon, lat):
        bx, by = lonlat_to_bellin(lon, lat, self.BW, self.BH)
        return (bx - self.bx0) * self.sc, (by - self.by0) * self.sc

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

    def origin(self, t):
        cx, cy = self.to_canvas(MAP_LON, map_lat(t))
        return cx - self.w / 2, cy - self.h / 2                        # canvas px at the frame's top-left

    def draw(self, canvas, t, t_in, wash):
        ox, oy = self.origin(t)
        M = np.float32([[1, 0, -ox], [0, 1, -oy]])
        img = cv2.warpAffine(self.img, M, (self.w, self.h), flags=cv2.INTER_LINEAR, borderValue=0)
        fld = cv2.warpAffine(self.fld, M, (self.w, self.h), flags=cv2.INTER_LINEAR, borderValue=0)
        land, sea_a, n_land, n_sea = fld[..., 0], fld[..., 1], fld[..., 2], fld[..., 3]
        a = ssf(t_in, t_in + 5.0, t) * 1.2
        rl = np.clip((a - n_land) / 0.08, 0, 1)
        rs = np.clip((a - 0.35 - n_sea) / 0.1, 0, 1)
        alpha = (land * rl * self.lvig + (1 - land) * sea_a * rs * self.vig) * (1 - wash)
        img = img * (1 + 0.05 * np.sin(t * 1.3))
        blit(canvas, img, alpha.astype(F32), self.x0, 0, guard=self.ctx.guard, tag='pic:map')
        self.draw_route(canvas, t, wash, ox, oy)

    def at(self, s):
        i = int(np.clip(np.searchsorted(self.cum, s) - 1, 0, len(self.seg) - 1))
        return self.route[i] + (self.route[i + 1] - self.route[i]) * float(np.clip((s - self.cum[i]) / self.seg[i], 0, 1))

    def draw_route(self, canvas, t, wash, ox, oy):
        k = lin(ROUTE_T0, ROUTE_T1, t)                                  # constant speed down the coast
        if k <= 0 or wash >= 1:
            return
        q = self.ctx.q
        off = np.array([ox - self.x0, oy], F32)
        layer = np.zeros(canvas.shape[:2], F32)
        Lk = self.cum[-1] * k
        per = 14 * q
        s0 = 0.0
        while s0 < Lk:                                                  # dashes fixed on the map: they travel with it
            p0, p1 = self.at(s0) - off, self.at(min(s0 + per * 0.55, Lk)) - off
            cv2.line(layer, (int(p0[0] * 4), int(p0[1] * 4)), (int(p1[0] * 4), int(p1[1] * 4)), 1.0,
                     max(2, int(4 * q)), cv2.LINE_AA, shift=2)
            s0 += per
        layer = cv2.GaussianBlur(layer, (0, 0), 0.7) * self.ctx.guard[None, :]
        a = layer[..., None] * 0.95 * (1 - wash)
        canvas[:] = canvas * (1 - a) + np.array([0.62, 0.08, 0.05], F32) * a
        head = 1 - ssf(ROUTE_T1, ROUTE_T1 + 1.5, t)                     # the ship's point, glowing at the head
        if head > 0:
            hx, hy = self.at(Lk) - off
            gy, gx = np.ogrid[0:canvas.shape[0], 0:canvas.shape[1]]
            r2 = (gx - hx) ** 2 + (gy - hy) ** 2
            fl = 0.85 + 0.15 * np.sin(t * 11)
            g = (np.exp(-r2 / (2 * (2.2 * q) ** 2)) + 0.45 * np.exp(-r2 / (2 * (12 * q) ** 2))) * head * fl * (1 - wash)
            g = (g * self.ctx.guard[None, :])[..., None]
            canvas += g * np.array([1.0, 0.55, 0.35], F32)


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
    """A word, alone in the dark (never on a picture): it arrives out of blur and keeps growing at a slow,
    constant rate for as long as it is up (note 3: nothing is ever static)."""

    def __init__(self, ctx, text, wall, fx, fy, size_full, t_in, t_out, font='GFSDidot-Regular.ttf',
                 colour=np.array([0.90, 0.86, 0.76], np.float32), tracking=0.14, fade=1.2, shadow=0.75, grow=0.005):
        self.rgb, self.a = text_layer(ctx, text, font, size_full, colour, tracking)
        self.sh = cv2.GaussianBlur(self.a, (0, 0), max(1.5, ctx.px(size_full) * 0.18)) * shadow
        self.x, self.y = ctx.wall_xy(wall, fx, fy)
        self.t_in, self.t_out, self.fade, self.ctx, self.grow, self.text = t_in, t_out, fade, ctx, grow, text
        self.blur_max = max(1.0, 6 * ctx.s)

    def draw(self, canvas, t):
        if not (self.t_in <= t <= self.t_out + self.fade):
            return
        k = ssf(self.t_in, self.t_in + self.fade, t) * (1 - ssf(self.t_out, self.t_out + self.fade, t))
        a = self.a
        if k < 0.999:
            a = cv2.GaussianBlur(a, (0, 0), self.blur_max * (1 - k) + 0.01)
        sc = 1 + self.grow * (t - self.t_in)
        h, w = a.shape
        ow, oh = int(np.ceil(w * sc)) + 4, int(np.ceil(h * sc)) + 4
        ox, oy = self.x - ow / 2, self.y - oh / 2
        if self.sh.max() > 0:
            blit(canvas, np.zeros((oh, ow, 3), np.float32), scaled(self.sh, sc, ow, oh) * k, ox, oy, guard=self.ctx.guard)
        blit(canvas, scaled(self.rgb, sc, ow, oh), scaled(a, sc, ow, oh) * k, ox, oy, guard=self.ctx.guard,
             tag='word:' + self.text)


# --------------------------------------------------------------------------- Liberté, Égalité, Fraternité
def colour_wall(ctx, wall, col, seed):
    x0, x1 = ctx.wall_px(wall)
    w, h = x1 - x0, ctx.H
    n = fractal(h, w, np.random.default_rng(seed), scales=(max(2, h // 3), max(2, h // 12), max(2, h // 40)), gains=(1, 0.4, 0.15))
    yy, xx = np.mgrid[0:h, 0:w].astype(F32)
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.42) / (h / 2)) ** 2)
    img = col[None, None] * np.clip(1.15 - 0.45 * r, 0.35, 1.1)[..., None]
    n_in = np.clip(0.5 * (n * 0.5 + 0.5) + 0.5 * np.clip(r / 1.4, 0, 1), 0, 1)
    mot = fractal(h + ctx.px(400), w + ctx.px(900), np.random.default_rng(seed + 2),
                  scales=(max(2, h // 3), max(2, h // 12), max(2, h // 40)), gains=(1, 0.4, 0.15))
    burn = PaperBurn(ctx, h, w, {'L': (w * 1.05, h * 0.5), 'R': (-w * 0.05, h * 0.5), 'C': (w * 0.5, h * 0.5)}[wall], seed + 60)
    return dict(img=img.astype(F32), n_in=n_in, mot=mot, burn=burn, x=x0, w=w, h=h, wall=wall)


def draw_colour_wall(ctx, canvas, cw, t, t_in, t_out, ash, dt, dim=1.0, burn_dur=6.0):
    """A field of colour; its mottling drifts the whole time; it burns from the stage centre outward."""
    if t < t_in:
        return
    w, h = cw['w'], cw['h']
    a_in = ssf(t_in, t_in + 2.6, t) * 1.2
    rev = np.clip((a_in - cw['n_in']) / 0.08, 0, 1)
    mot = slide(cw['mot'], w, h, w / 2 + ctx.px(900) - 20 * ctx.s * (t - t_in), h / 2 + ctx.px(200) + 4 * ctx.s * (t - t_in))
    img = cw['img'] * (1 + 0.10 * mot[..., None]) * dim
    a = rev.astype(F32)
    emit = None
    if t > t_out:
        img, a, emit, rim = cw['burn'].apply(img.astype(F32), a, lin(t_out, t_out + burn_dur, t), t)
        cw['burn'].spawn(ash, rim, cw['burn'].F, lambda x, y: (cw['x'] + x, y), 60 * ctx.s * 2, dt)
    reg = canvas[:, cw['x']:cw['x'] + w]
    reg[:] = reg * (1 - a[..., None]) + img * a[..., None] + (0 if emit is None else emit)


# --------------------------------------------------------------------------- the scene
def build(ctx):
    S = {}

    def pr(name, grey=False):
        return tone(load(name), paper=PAPER_GREY if grey else PAPER)[0]

    def gy(name):                                    # an engraving as a multiplier: paper 1, ink ~0
        return np.clip(tone(load(name), paper=np.ones(3, F32), ink=np.full(3, 0.04, F32), hi_p=85)[0], 0, 1)

    def wash(name, wall, cx, cy, h, t_in, t_out, seed, grey=False, **kw):
        return Wash(ctx, pr(name, grey), wall, cx, cy, h, t_in, t_out, seed=seed, name=name, **kw)

    W = []
    # M2: the five battles TAKE TURNS, one picture and one word each, high on the wall, the word in the dark below
    W.append(wash('battle_austerlitz_DuplessiBertaux', 'L', 0.50, 0.36, 540, 41.0, 46.0, 1))
    W.append(wash('battle_wagram_estampe', 'R', 0.50, 0.36, 560, 43.5, 48.5, 2))
    W.append(wash('battle_iena_DuplessiBertaux', 'C', 0.50, 0.37, 620, 46.0, 53.0, 3))
    W.append(wash('battle_eylau_estampe', 'L', 0.50, 0.36, 560, 50.0, 55.5, 4))
    W.append(wash('battle_friedland_1808', 'R', 0.50, 0.36, 560, 52.5, 57.5, 5))
    # M3: Goya, grey, big (no words)
    W.append(wash('goya_p50_famine_MadreInfeliz', 'L', 0.50, 0.42, 800, 60.5, 72.0, 6, grey=True, grow=0.008, out_dur=4.0))
    W.append(wash('goya_p15_execution_YnoHaiRemedio', 'R', 0.50, 0.42, 800, 64.5, 73.5, 7, grey=True, grow=0.008, out_dur=4.0))
    W.append(wash('goya_p18_death_EnterraryCallar', 'C', 0.50, 0.42, 820, 68.5, 75.0, 8, grey=True, grow=0.008, out_dur=4.0))
    # M5: Waterloo on CENTRE (its word below it), the field after it on LEFT, the ravages on RIGHT
    W.append(wash('battle_waterloo_MontStJean_1815', 'C', 0.50, 0.36, 640, 104.0, 112.0, 9, out_dur=4.0))
    W.append(wash('battle_waterloo_field_Jazet_1816', 'L', 0.50, 0.40, 760, 107.5, 116.5, 10, grey=True, grow=0.008, out_dur=4.0))
    W.append(wash('goya_p30_ravages_Estragos', 'R', 0.50, 0.40, 780, 110.0, 117.5, 11, grey=True, grow=0.008, out_dur=4.0))
    # M7: they escape through the flames (CENTRE, once the flags have burnt)...
    W.append(wash('goya_p41_fleeing_EscapanLlamas', 'C', 0.50, 0.42, 820, 136.5, 143.5, 12, grey=True, grow=0.008))
    # ...then the fleeing families ghost into the dawn haze on LEFT and RIGHT, receding toward the ship
    W.append(Wash(ctx, gy('goya_p44_fleeing_YoLoVi'), 'L', 0.46, 0.50, 760, 138.0, 157.0, seed=13, drift=(9, 1.0), grow=-0.008,
                  in_dur=4.0, out_dur=5.0, mode='multiply', name='goya_p44', exit='fade'))
    W.append(Wash(ctx, gy('goya_p45_fleeing_YestoTambien'), 'R', 0.54, 0.50, 760, 140.0, 157.0, seed=14, drift=(-9, 1.0),
                  grow=-0.008, in_dur=4.0, out_dur=5.0, mode='multiply', name='goya_p45', exit='fade'))
    S['washes'] = W
    S['flakes'] = Flakes(ctx)
    S['ash'] = Ash(ctx)
    S['words'] = [
        Word(ctx, 'AUSTERLITZ', 'L', 0.50, 0.80, 46, 41.4, 46.0),
        Word(ctx, 'WAGRAM', 'R', 0.50, 0.80, 46, 43.9, 48.5),
        Word(ctx, 'IÉNA', 'C', 0.50, 0.82, 52, 46.4, 53.0),
        Word(ctx, 'EYLAU', 'L', 0.50, 0.80, 46, 50.4, 55.5),
        Word(ctx, 'FRIEDLAND', 'R', 0.50, 0.80, 46, 52.9, 57.5),
        Word(ctx, 'LIBERTÉ', 'L', 0.50, 0.40, 110, 82.4, 100.0),
        Word(ctx, 'ÉGALITÉ', 'C', 0.50, 0.40, 110, 84.4, 100.0, colour=np.array([0.10, 0.10, 0.16], F32), shadow=0),
        Word(ctx, 'FRATERNITÉ', 'R', 0.50, 0.40, 96, 86.4, 100.0),
        Word(ctx, 'WATERLOO', 'C', 0.50, 0.83, 60, 105.5, 111.0),
        Word(ctx, 'MONARCHISTES', 'R', 0.50, 0.82, 58, 124.2, 130.5),
        Word(ctx, 'NAPOLÉONISTES', 'L', 0.50, 0.82, 58, 126.2, 130.5),
        Word(ctx, '1816', 'C', 0.26, 0.28, 230, 150.0, 156.5, font='PinyonScript-Regular.ttf',
             colour=np.array([0.95, 0.92, 0.86], F32), tracking=0.02, fade=2.0),
    ]
    S['cwalls'] = [colour_wall(ctx, 'L', BLUE, 21), colour_wall(ctx, 'C', WHITE, 22), colour_wall(ctx, 'R', RED, 23)]
    S['flagC'] = ClothFlag(ctx, 'C', 'tri', seed=30)
    S['flagL'] = ClothFlag(ctx, 'L', 'tri', box=(0.10, 0.06, 0.90, 0.62), seed=31)
    S['flagR'] = ClothFlag(ctx, 'R', 'white', box=(0.10, 0.06, 0.90, 0.62), seed=32)
    S['smoke'] = Smoke(ctx)
    S['fore'] = Smoke(ctx, seed=16, speed=1.6)
    S['embers'] = Particles(ctx, EMBER)
    S['ashp'] = Particles(ctx, ASH, rise=(-12, 10), seed=5, blur=1.2, gain=0.9)
    S['map'] = MapJourney(ctx)
    ship = cv2.imread(os.path.join(SRC, 'medusa_frigate_Baugean.jpg'))
    g = cv2.cvtColor(ship, cv2.COLOR_BGR2GRAY).astype(F32) / 255
    sh_h = ctx.px(430)
    S['ship'] = cv2.resize(g, (int(g.shape[1] * sh_h / g.shape[0]), sh_h), interpolation=cv2.INTER_AREA)
    hz = np.linspace(0, 1, ctx.H, dtype=F32)
    hn = fractal(ctx.H, ctx.W, np.random.default_rng(56), scales=(ctx.px(500), ctx.px(160)), gains=(1, 0.4))
    S['horizon_y'] = 0.56
    S['haze'] = np.exp(-((hz[:, None] - 0.56 - 0.02 * hn) / 0.12) ** 2) * (0.75 + 0.25 * hn)
    S['sky'] = (np.clip(1 - np.abs(hz - 0.56) / 0.40, 0, 1) ** 2)[:, None]
    gy_, gx_ = np.mgrid[0:ctx.H, 0:ctx.W].astype(F32)
    glowLR = np.zeros((ctx.H, ctx.W), F32)
    for wall in ('L', 'R'):
        x, y = ctx.wall_xy(wall, 0.5, 0.54)
        glowLR += np.exp(-(((gx_ - x) / ctx.px(560)) ** 2 + ((gy_ - y) / ctx.px(300)) ** 2))
    S['glowLR'] = glowLR
    return S


def render_frame(ctx, S, t, dt):
    W, H = ctx.W, ctx.H
    c = np.zeros((H, W, 3), F32)
    # the smoke field: coloured by the flag's light in M1-M2, cold and grey in M3, back to fire in M5
    dens = 0.95 * (1 - ssf(12, 24, t)) + 0.55 * ssf(12, 24, t) * (1 - ssf(74, 80, t)) \
        + 0.55 * ssf(98, 104, t) * (1 - ssf(132, 140, t))
    warm = 1.0 * (1 - ssf(20, 60, t)) + 0.35 + 0.45 * ssf(98, 104, t) * (1 - ssf(118, 126, t))
    spill = ssf(8, 16, t) * (1 - ssf(38, 44, t)) * 0.9 + 0.6 * ssf(120, 124, t) * (1 - ssf(130, 135, t))
    cold = ssf(56, 64, t) * (1 - ssf(96, 102, t))
    S['smoke'].draw(t, c, dens, warm, spill=spill, cold=cold)
    # M7 dawn haze (a field) and the light behind the exiles
    hz = ssf(135, 141, t)
    if hz > 0:
        c += S['haze'][..., None] * np.array([0.42, 0.44, 0.48], F32) * 0.7 * hz
        c += S['sky'][..., None] * np.array([0.07, 0.08, 0.11], F32) * hz
        c += (S['glowLR'] * (ssf(137, 142, t) * (1 - 0.7 * ssf(155, 161, t))))[..., None] * np.array([0.55, 0.55, 0.57], F32)
    ash = S['ash']
    # M1-M2: the tricolour cloth fills CENTRE through the glory lines, then goes back into the smoke for the battles
    if 7 <= t <= 42.6:
        S['flagC'].draw(c, t, ash, dt, reveal=ssf(7, 16, t) * (1 - ssf(38.5, 42.5, t)))
    # M4-M5: the three colour walls, burning from the stage centre outward into Waterloo
    if 79 <= t <= 110:
        dim = 1 - 0.25 * ssf(96, 101, t)
        for cw, ti in zip(S['cwalls'], (81.0, 83.0, 85.0)):
            draw_colour_wall(ctx, c, cw, t, ti, 101.5, ash, dt, dim)
    # M6: France divided: the CENTRE tricolour tears, its right half bleaches white; LEFT tricolour, RIGHT white; all burn
    if 119.5 <= t <= 136.5:
        S['flagC'].draw(c, t, ash, dt, reveal=ssf(119.5, 122.5, t), tear=ssf(121.5, 125.5, t), bleach=ssf(124, 127.5, t),
                        burn=lin(130.5, 135.5, t))
        S['flagR'].draw(c, t + 3, ash, dt, strength=0.85, reveal=ssf(124, 127, t), burn=lin(131.0, 136.0, t))
        S['flagL'].draw(c, t + 7, ash, dt, strength=0.85, reveal=ssf(126, 129, t), burn=lin(131.3, 136.3, t))
    # the pictures, and the fragments that break off them
    for wsh in S['washes']:
        if wsh.active(t):
            wsh.draw(t, c, S['flakes'], ash, dt)
    S['flakes'].draw(c, dt)
    ash.draw(c, dt)
    # M7: the coast, the course, 1816; it washes into the dawn; the frigate
    if t >= MAP_T0:
        S['map'].draw(c, t, MAP_T0, ssf(157, 159.8, t))
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
    S['ashp'].step(t, dt, 60 * ssf(60, 64, t) * (1 - ssf(74, 78, t)) + 70 * ssf(106, 110, t) * (1 - ssf(118, 124, t)))
    S['ashp'].draw(c, t)
    return np.clip(c, 0, 1)


def ship(ctx, c, S, t):
    """The Medusa on the horizon: it keeps coming, slowly, and rides the swell."""
    k = ssf(159.8, 164.0, t)
    x, y = ctx.wall_xy('C', 0.5, S['horizon_y'])
    g0 = S['ship']
    gy, gx = np.mgrid[0:c.shape[0], 0:c.shape[1]].astype(F32)
    glow = np.exp(-(((gx - x) / (g0.shape[1] * 0.75)) ** 2 + ((gy - y) / (g0.shape[0] * 0.55)) ** 2))
    c += glow[..., None] * np.array([0.55, 0.55, 0.56], F32) * ssf(156.5, 162, t)
    if k <= 0:
        return
    sc = 1 + 0.008 * (t - 159.8)
    h0, w0 = g0.shape
    ow, oh = int(np.ceil(w0 * sc)) + 4, int(np.ceil(h0 * sc)) + 4
    g = scaled(g0, sc, ow, oh)
    yy, xx = np.mgrid[0:h0, 0:w0].astype(F32)
    edge = np.clip(np.minimum(np.minimum(xx, w0 - xx), np.minimum(yy, h0 - yy)) / (h0 * 0.18), 0, 1)
    edge = scaled(edge, sc, ow, oh)
    rgb = np.repeat((0.08 + 0.92 * g)[..., None], 3, 2).astype(F32)
    bob = 1.5 * ctx.s * np.sin(t * 1.1)
    blit(c, rgb, (edge * k).astype(F32), x - ow / 2, y - oh * 0.84 + bob, guard=ctx.guard, mode='multiply', tag='pic:ship')


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


def check(ctx, S, step=0.25):
    """Note 2, measured: at every step, does any picture overlap another picture, or any word a picture?"""
    global REC
    bad = {}
    n = int(DUR / step)
    for i in range(n + 1):
        t = i * step
        REC = []
        render_frame(ctx, S, t, step)
        recs = REC
        REC = None
        for a in range(len(recs)):
            for b in range(a + 1, len(recs)):
                ta, tb = recs[a][0], recs[b][0]
                if ta == tb or (ta.startswith('word:') and tb.startswith('word:')):
                    continue
                y0, y1 = max(recs[a][1], recs[b][1]), min(recs[a][2], recs[b][2])
                x0, x1 = max(recs[a][3], recs[b][3]), min(recs[a][4], recs[b][4])
                if y1 <= y0 or x1 <= x0:
                    continue
                ma = recs[a][5][y0 - recs[a][1]:y1 - recs[a][1], x0 - recs[a][3]:x1 - recs[a][3]]
                mb = recs[b][5][y0 - recs[b][1]:y1 - recs[b][1], x0 - recs[b][3]:x1 - recs[b][3]]
                px = int((ma & mb).sum())
                if px > 4:
                    key = tuple(sorted((ta, tb)))
                    lo, hi, mx = bad.get(key, (t, t, 0))
                    bad[key] = (min(lo, t), max(hi, t), max(mx, px))
    if not bad:
        print('CHECK: no picture/picture or word/picture overlap anywhere in 0-%.0f s' % DUR)
    for (ta, tb), (lo, hi, mx) in sorted(bad.items(), key=lambda kv: kv[1][0]):
        print(f'OVERLAP {ta} x {tb}: {lo:.2f}-{hi:.2f} s, up to {mx} px (at scale {ctx.s})')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=0.5)
    ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--end', type=float, default=DUR)
    ap.add_argument('--stills', default=None, help='write PNGs at --at seconds instead of a movie')
    ap.add_argument('--at', type=str, default='')
    ap.add_argument('--check', action='store_true', help='report picture/word overlaps instead of rendering')
    a = ap.parse_args()
    ctx = Ctx(a.scale)
    S = build(ctx)
    dt = 1 / FPS
    if a.check:
        check(ctx, S)
        return
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
