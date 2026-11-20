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
  python tools/court_behind_paper.py beat OUT.mov --beat 3|5|7        (FINAL show build, A2 level 2, 1800x1080 ProRes, no sound)
  python tools/court_behind_paper.py strike OUT.mov --size Q1|Q2|Q3|Q4  (the operator's single strike, same look)
  ... beat|strike ... --opaque [rail|front]   (M9k TEST: true layers, the judge opaque; compose_opaque())
beat/strike are built like render_court.py --scrim --burn (same timeline, shake, burn t0 per beat); the Q5 capper
(the gavel alone) goes through the same paper/fibre treatment at full sharpness (it is at the lens).
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


def shadow_density(m, level=2, closeness=None):
    """The judge's soft shadow 0..1, exactly as compose() builds it (A1/A2)."""
    sg, keep = LEVELS[level]
    s = 1 - m
    if closeness is not None:
        sh = blur(s, max(sg * 0.35, 1.5))
        so = blur(s, sg * 1.25)
        return so * (1 - closeness) + sh * closeness
    return blur(s, sg)


def compose_opaque(sc, n, t0, m, cl, clean=False, rail_front=False):
    """--opaque (Homie M9k 2026-11-20: "the judge is kind of on top of it... wherever we see the judge silhouette... we
    don't see the other things"). True layers instead of shadows multiplied through each other:
      far   the two arched windows + the wall round them (back)
      judge OPAQUE: under him the windows are not there at all (his tone replaces them, no double darkening)
      near  the bar's balustrade + floor sill (rail at 1.0 m). Default ('front', rail_front=False): the railing is the
            MIDDLE layer, behind the judge (Homie: "windows in the back... the railing in the middle... the judge
            ahead"). rail_front=True ('rail', Q1-Q3 only) lays it over his legs in its own pale tone: tested
            2026-11-20 and rejected by Claude (the pale bars read as holes through his legs).
    The paper's burn, lamp bloom and fibre are applied over the combined result as compose() does."""
    sg, keep = LEVELS[2]
    sb = shadow_density(m, 2, cl)
    lit = sc.plain * (sc.lamp * lamp_gain(n))[..., None]
    burn = (lambda im: im) if clean else (lambda im: sc.burn.frame(im, t0 + n))
    tone = keep * WARM / WARM.max()
    hole = 1 - sb                                                    # where the judge is, nothing behind him shows
    if rail_front:
        bg = burn(lit * (1 - 0.30 * sc.far * hole)[..., None])       # windows behind the judge, no railing yet
    else:
        bg = burn(lit * (1 - (0.30 * sc.far + 0.30 * sc.near) * hole)[..., None])
    out = bg * (1 - sb[..., None] * (1 - tone[None, None, :]))
    lampb = cv2.GaussianBlur(bg.mean(2), (0, 0), 60)
    out = out + (sb * lampb * 0.035)[..., None] * WARM
    if rail_front:                                                   # the railing over him, solid, its own tone
        rail = burn(lit * (1 - 0.30 * sc.far - 0.30 * sc.near)[..., None])
        a = sc.near[..., None]
        out = out * (1 - a) + rail * a
    out = out * (1 + 0.035 * sc.fib[..., None])
    out = out + (sb * 0.018)[..., None] * sc.fib[..., None] * WARM
    return np.clip(out, 0, 1)


class Scene:
    def __init__(self, opaque=False):
        for q in ('Q1', 'Q2', 'Q3'):
            rc.SIZES[q] = V2[q]
        if opaque:
            self.base, self.lamp, self.plain, self.far, self.near = field_static(layers=True)
        else:
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


def frames(beat, strike, clean=False, opaque=None, skip=0):
    """The show build's frames: render_court.py's timeline/shake/burn, with the judge behind the paper (level 2, A2).
    opaque = None (the approved look, bit-identical), 'front' (true layers, judge opaque) or 'rail' (see compose_opaque).
    skip = frames before it are not drawn (yields None; the shake's random draws still run, so later frames match)."""
    sc = Scene(opaque=bool(opaque))
    seq = rc.timeline(beat, strike)
    t0 = BEAT_T0[5 if beat == '5cut' else beat] if beat else 0
    rng = np.random.default_rng(1817)
    shake = 0
    for n, (idx, sz, impact) in enumerate(seq):
        if n < skip:
            if idx is not None:
                if impact:
                    shake = 6
                if shake:
                    amp = 7 * shake / 6
                    rng.integers(-amp, amp + 1, 2)
                    shake -= 1
            yield None
            continue
        if idx is None:
            im = np.zeros((OH, OW, 3), np.float32)
        else:
            if len(sc.cache) > 8:
                sc.cache = {k: v for k, v in sc.cache.items() if k[0] == rc.RAISED}
            cl = 1.0 if sz == 'Q5' else closeness(idx)
            if opaque:
                im = compose_opaque(sc, n, t0, sc.mask(idx, sz), cl, clean,
                                    rail_front=(opaque == 'rail' and sz in ('Q1', 'Q2', 'Q3')))
            else:
                bgi = sc.base * (sc.lamp * lamp_gain(n))[..., None] if clean else sc.bg(n, t0)
                im = compose(bgi, sc.mask(idx, sz), sc.fib, 2, closeness=cl)
            if impact:
                shake = 6
            if shake:
                amp = 7 * shake / 6
                dx, dy = rng.integers(-amp, amp + 1, 2)
                im = np.roll(im, (int(dy), int(dx)), (0, 1)) * (1 + 0.05 * shake / 6)
                shake -= 1
        yield im


def n_frames(beat, strike):
    return len(rc.timeline(beat, strike))


def final(out, beat, strike, clean=False, opaque=None):
    """The show build (ProRes 422 HQ, no sound)."""
    if os.path.exists(out):
        raise SystemExit(f'refusing: {out} exists. Clean renders are never replaced; give the new one a new version')
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{OW}x{OH}',
                          '-r', str(rc.FPS), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2',
                          '-pix_fmt', 'yuv422p10le', out], stdin=subprocess.PIPE)
    k = 0
    for im in frames(beat, strike, clean, opaque):
        w.stdin.write((np.clip(im, 0, 1) * 65535).astype('<u2').tobytes())
        k += 1
    w.stdin.close()
    w.wait()
    print(k, 'frames ->', out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['stills', 'clip', 'beat', 'strike'])
    ap.add_argument('out')
    ap.add_argument('--level', type=int, default=2, choices=[1, 2, 3])
    ap.add_argument('--a2', action='store_true')
    ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--size', default='Q2')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, 5, 7, '5cut'],
                    help="5cut = Darren's cut of b5 (64.25 s, strikes moved; docs/S9-DARREN-CUT.md)")
    ap.add_argument('--clean', action='store_true', help='beat/strike: no burn edge (the _CLEAN master)')
    ap.add_argument('--opaque', nargs='?', const='front', choices=['front', 'rail'],
                    help="beat/strike: TRUE LAYERS (M9k): windows (back) < railing (middle) < the judge, OPAQUE "
                         "(default 'front'). 'rail' = the balustrade solid over his legs (tested 2026-11-20: its pale "
                         "tone reads as see-through legs; not used). Without it: the approved look, bit-identical")
    ap.add_argument('--idle', action='store_true',
                    help='beat: the LIVING judge (tools/court_idle.py: breath, nods, lean + coat, no snap after strikes)')
    a = ap.parse_args()
    if a.cmd == 'stills':
        stills(a.out)
    elif a.cmd == 'beat' and a.idle:
        import court_idle
        court_idle.final(a.out, a.beat, a.clean)
    elif a.cmd == 'beat':
        final(a.out, a.beat, None, a.clean, a.opaque)
    elif a.cmd == 'strike':
        final(a.out, None, a.size, a.clean, a.opaque)
    else:
        clip(a.out, a.level, a.a2, a.smoke, a.size)
