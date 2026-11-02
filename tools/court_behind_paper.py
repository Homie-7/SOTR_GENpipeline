"""Scene 9: the judge BEHIND the parchment (Meeting 6, 31 Oct: "experiment with placing the judge behind the parchment
paper so he is less defined"). Built 2026-11-03 (Claude, delegated by Homie). Script, 0 credits.

Today (render_court.py --scrim --burn) the judge is a hard black silhouette laid ON the lit-scrim field. Here he is a
SHADOW cast through the paper by the lamp behind it:
- soft: his two-tone mask is blurred (a shadow is soft; sharpest where the body is closest to the paper);
- not black: the shadow keeps a share of the paper's own light, tinted warm (light through paper is amber when dim);
- the paper's own fibre runs OVER him (he is behind it, so the paper reads continuous), stronger in the shadow where the
  translucent sheet shows its grain; the lamp's bloom lifts his core a touch;
- A1 = one softness throughout; A2 = he sharpens as he lunges toward us (the blow f40-96) and softens again after;
- B (--smoke) = a figure of smoke: the silhouette's core is kept, only its edges go to rising smoke.
The sanctioned white keyline round the gavel (LOOK World 3) is kept as a thin pale line; it must not glow.

  python tools/court_behind_paper.py stills OUTDIR            (softness levels x raised / strike, + A2 + smoke)
  python tools/court_behind_paper.py clip OUT.mp4 --level 2 [--a2] [--smoke] [--size Q2]
Needs numpy, OpenCV, ffmpeg and render_court.py / render_court_v2.py / court_burn.py beside it.
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
from render_court_v2 import field_static, lamp_gain, SIZES as V2  # noqa: E402
from court_burn import BurnEdges, BEAT_T0  # noqa: E402

OW, OH = rc.OW, rc.OH
WARM = np.float32([1.0, 0.80, 0.56])           # the amber of dim light through paper (RGB)
# softness levels: blur sigma (px at 1080 high), share of the paper's light the shadow keeps
LEVELS = {1: (3.5, 0.26), 2: (8.0, 0.22), 3: (16.0, 0.18)}


def fibre(seed=7):
    """Parchment fibre: fine isotropic grain + longer random strands + slow mottling, mean 0, std ~1."""
    rng = np.random.default_rng(seed)
    a = cv2.GaussianBlur(rng.normal(0, 1, (OH, OW)).astype(np.float32), (0, 0), 0.9)
    b = cv2.GaussianBlur(rng.normal(0, 1, (OH, OW)).astype(np.float32), (0, 0), sigmaX=7, sigmaY=1.1)
    c = cv2.GaussianBlur(rng.normal(0, 1, (OH, OW)).astype(np.float32), (0, 0), 38)
    f = a / a.std() * 0.55 + b / b.std() * 0.55 + c / c.std() * 0.6
    return (f / f.std()).astype(np.float32)


def blur(s, sg):
    return cv2.GaussianBlur(s, (0, 0), sg) if sg > 0.3 else s


def smoke_shadow(s, fib, t):
    """B: keep the silhouette's core, let only its edges go to smoke that drifts up (advected noise)."""
    core = cv2.erode((s > 0.5).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=9).astype(np.float32)
    core = blur(core, 3.0)
    rng = np.random.default_rng(31)
    n = np.zeros((OH, OW), np.float32)
    for sc, g in ((90, 1.0), (40, 0.6), (18, 0.35)):
        w = cv2.GaussianBlur(rng.normal(0, 1, (OH // 4, OW // 4)).astype(np.float32), (0, 0), sc / 4)
        w = cv2.resize(w, (OW, OH), interpolation=cv2.INTER_CUBIC)
        n += g * w / max(w.std(), 1e-6)
    n /= n.std()
    # the smoke rises: sample the noise lower down so wisps stream up; its reach grows with height
    rise = 38 + 22 * np.sin(t * 0.07)
    M = np.float32([[1, 0, 0], [0, 1, -rise]])
    nr = cv2.warpAffine(n, M, (OW, OH), borderMode=cv2.BORDER_REFLECT_101)
    halo = blur(cv2.dilate((s > 0.5).astype(np.uint8), np.ones((3, 3), np.uint8), iterations=22).astype(np.float32), 14)
    halo = np.maximum(halo - blur(core, 8), 0)
    wisp = np.clip(0.55 + 0.55 * nr, 0, 1) * halo
    tail = blur(cv2.warpAffine(halo, np.float32([[1, 0, 0], [0, 1, -70]]), (OW, OH)), 20) * np.clip(0.35 + 0.5 * nr, 0, 1) * 0.55
    return np.clip(np.maximum(core, wisp + tail * (1 - core)), 0, 1)


def compose(bg, m, fib, level=2, closeness=None, smoke=False, t=0):
    """bg = the lit paper (with its burn) 0..1; m = the placed figure mask (0 black, 1 white); returns the frame."""
    sg, keep = LEVELS[level]
    s = 1 - m
    if closeness is not None:                       # A2: soft far, sharp near the lens
        sh = blur(s, max(sg * 0.35, 1.5))
        so = blur(s, sg * 1.25)
        sb = so * (1 - closeness) + sh * closeness
    else:
        sb = blur(s, sg)
    if smoke:
        sb = np.maximum(smoke_shadow(s, fib, t), 0) * 0.92
    # keep a thin pale line where the gavel's sanctioned keyline was, but never a glow: blur already softens it
    tone = keep * WARM / WARM.max()
    trans = 1 - sb[..., None] * (1 - tone[None, None, :])        # light that gets through the paper where the shadow is
    out = bg * trans
    lamp = cv2.GaussianBlur(bg.mean(2), (0, 0), 60)
    out = out + (sb * lamp * 0.035)[..., None] * WARM                # the lamp's bloom lifts the shadow's core a touch
    out = out * (1 + 0.035 * fib[..., None])                          # the paper's own fibre over everything
    out = out + (sb * 0.018)[..., None] * fib[..., None] * WARM       # and stronger in the shadow, where the sheet shows
    return np.clip(out, 0, 1)


class Scene:
    def __init__(self):
        for q in ('Q1', 'Q2', 'Q3'):
            rc.SIZES[q] = V2[q]
        self.base, self.lamp = field_static()
        self.src = rc.load_source()
        self.gbox = rc.gavel_box(self.src[rc.HELD])
        self.burn = BurnEdges(OW, OH)
        self.fib = fibre()
        self.cache = {}

    def mask(self, idx, size):
        k = (idx, size)
        if k not in self.cache:
            self.cache[k] = rc.place(self.src[idx], size, self.gbox)
        return self.cache[k]

    def bg(self, n, t0=BEAT_T0[5]):
        return self.burn.frame(self.base * (self.lamp * lamp_gain(n))[..., None], t0 + n)


def closeness(idx):
    """0 at the raised pose, 1 when the gavel is held at the lens (blow f40-96), back to 0 on the cut to raised."""
    return float(np.clip((idx - rc.BLOW[0]) / (rc.HELD - rc.BLOW[0]), 0, 1))


def save(path, img):
    cv2.imwrite(path, cv2.cvtColor((np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8), cv2.COLOR_RGB2BGR))


def stills(outdir):
    os.makedirs(outdir, exist_ok=True)
    sc = Scene()
    shots = [('raised', 0, 'Q2', 200), ('strike', rc.HELD, 'Q3', 230)]
    rows = []
    for tag, idx, size, n in shots:
        bg = sc.bg(n)
        m = sc.mask(idx, size)
        cur = []
        cur.append(('00_CURRENT', bg * m[..., None]))
        for lv in (1, 2, 3):
            cur.append((f'A1_level{lv}', compose(bg, m, sc.fib, lv)))
        cur.append(('A2_sharp-near', compose(bg, m, sc.fib, 2, closeness=closeness(idx))))
        cur.append(('B_smoke', compose(bg, m, sc.fib, 2, smoke=True, t=n)))
        for name, im in cur:
            save(os.path.join(outdir, f'S9_court_{tag}_{name}.png'), im)
        rows.append(np.hstack([cv2.resize(im, (600, 360), interpolation=cv2.INTER_AREA) for _, im in cur[:3]]))
        rows.append(np.hstack([cv2.resize(im, (600, 360), interpolation=cv2.INTER_AREA) for _, im in cur[3:]]))
    save(os.path.join(outdir, 'sheet.png'), np.vstack(rows))
    print('stills ->', outdir)


def clip(out, level, a2, smoke, size):
    sc = Scene()
    seq = rc.timeline(None, size)
    enc = ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                          '-r', str(rc.FPS), '-i', '-'] + enc + [out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(1817)
    shake = 0
    for n, (idx, sz, impact) in enumerate(seq):
        m = sc.mask(idx, sz)
        im = compose(sc.bg(n), m, sc.fib, level, closeness=closeness(idx) if a2 else None, smoke=smoke, t=n)
        if impact:
            shake = 6
        if shake:
            amp = 7 * shake / 6
            dx, dy = rng.integers(-amp, amp + 1, 2)
            im = np.roll(im, (int(dy), int(dx)), (0, 1))
            shake -= 1
        w.stdin.write((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    w.stdin.close()
    w.wait()
    print(len(seq), 'frames ->', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['stills', 'clip'])
    ap.add_argument('out')
    ap.add_argument('--level', type=int, default=2, choices=[1, 2, 3])
    ap.add_argument('--a2', action='store_true')
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--size', default='Q2')
    a = ap.parse_args()
    if a.cmd == 'stills':
        stills(a.out)
    else:
        clip(a.out, a.level, a.a2, a.smoke, a.size)
