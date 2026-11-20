"""Scene 9 court beats, FLOW judge (M9v, 2026-11-20): Homie's notes on the LEAN review, fixed by script. REVIEW only, 0 cr.

NEW FILE: court_gen_lean / court_gen_approved / court_gen / render_court are imported, never changed, so the LEAN, the
approved-strike review and the shipped beats stay bit-identical. Notes: docs/HANDOFF-2026-11-20-M9t.md (verbatim),
causes: docs/S9-JUDGE-M9u-DIAGNOSIS.md, plan + measurements: docs/HANDOFF-2026-11-20-M9v.md.

WHAT CHANGES AGAINST LEAN (the approved strike's FRAMES stay untouched, never warped):
  1 ONE SIZE PER FILE: b3 Q1, b5cut Q2, b7 Q3. No Q3 jump at slam 3, no Q4 push-in, no Q5 capper cut: the capper plays
    approved f40-95 at Q3 and goes black on the same frame as before.
  2 ONE SHARPNESS: every generated frame at CL_GEN; approved frames at max(their own closeness, CL_GEN), so there is
    no blur dip at the raise -> strike join. Generated masks get a contour clean-up (blur at 1080 before the
    threshold) so the x1.5 upscale doesn't stair-step.
  3 NO HARD CUTS: no 24-frame f96 freeze (f96 runs straight into the RETURN, flow-warped); flow-warp joins EASE_A /
    EASE_I frames long; the idle reads forward from a playhead (no rest-to-rest back-jumps except when a take runs
    out or a cued lift starts, both warped over EASE_I).
  4 CLIPPED EDGES: where the 9:16 source frame cuts the gavel (A f48-50 top, U f32-45 left) or the paper (A f42-48
    right), the frame is padded and the visible part is mirrored across the edge to close the shape, so no straight
    edge shows on the wall.
  5 BREATHING DAMPED: each idle frame is flow-warped DAMP of the way toward its take's f0, torso only (the weight is 0
    on the head), so the head lifts stay whole.

  python tools/court_gen_flow.py plan --beat 3|5cut|7
  python tools/court_gen_flow.py render OUT.mp4 --beat 3|5cut|7
  python tools/court_gen_flow.py sheets VIDEO.mp4 --beat B --prefix OUTPREFIX
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
import court_gen as cg  # noqa: E402
import court_gen_approved as ga  # noqa: E402
import court_gen_lean as gl  # noqa: E402
from court_burn import BEAT_T0  # noqa: E402
from court_behind_paper import compose_opaque, closeness as a_closeness  # noqa: E402

OW, OH, FPS = rc.OW, rc.OH, rc.FPS
SW, SH = 1080, 1920
IMPACT_A = ga.IMPACT_A
SIZE = {3: 'Q1', '5cut': 'Q2', 7: 'Q3'}
CL_GEN = 0.9
EASE_A = 20          # joins with an approved frame
EASE_I = 30          # joins inside the idle
DAMP = 0.5
NECK = (470, 570)    # gen source rows (1080x1920): damping weight 0 above NECK[0], DAMP below NECK[1]
PAD = 360            # source px of canvas added on each side for the mirrored edges
CLEAN_SIGMA = 1.8


def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------------------------------------ clipped edges
def _touch(b, side):
    return {'T': b[0], 'L': b[:, 0], 'R': b[:, -1]}[side]


def extend(g):
    """Pad grey g (1 = field) by PAD on every side; where black touches the top / left / right edge, mirror the strip
    just inside the edge outward to close the shape. Depth = until the black run is under 35 % of its edge width."""
    H, W = g.shape
    out = np.ones((H + 2 * PAD, W + 2 * PAD), np.float32)
    out[PAD:PAD + H, PAD:PAD + W] = g
    b = g < 0.5
    for side in ('T', 'L', 'R'):
        e = np.nonzero(_touch(b, side))[0]
        if len(e) < 3:
            continue
        c0, c1 = max(int(e[0]) - 24, 0), int(e[-1]) + 25
        # work in a "top" frame: rows = depth from the edge, cols = along the edge
        if side == 'T':
            strip = g[:PAD, c0:c1]
        elif side == 'L':
            strip = g[c0:c1, :PAD].T
        else:
            strip = g[c0:c1, ::-1][:, :PAD].T
        w0 = (strip[0] < 0.5).sum()
        wd = (strip < 0.5).sum(1)
        under = np.nonzero(wd < 0.35 * w0)[0]
        D = int(under[0]) if len(under) else PAD
        D = min(D, PAD, 260)
        refl = strip[:D][::-1]                     # row 0 = deepest, row D-1 = the edge row
        if side == 'T':
            reg = out[PAD - D:PAD, PAD + c0:PAD + c1]
            out[PAD - D:PAD, PAD + c0:PAD + c1] = np.minimum(reg, refl)
        elif side == 'L':
            reg = out[PAD + c0:PAD + c1, PAD - D:PAD]
            out[PAD + c0:PAD + c1, PAD - D:PAD] = np.minimum(reg, refl.T)
        else:
            reg = out[PAD + c0:PAD + c1, PAD + W:PAD + W + D]
            out[PAD + c0:PAD + c1, PAD + W:PAD + W + D] = np.minimum(reg, strip[:D].T)
    return out


def touches(g):
    b = g < 0.5
    return any(_touch(b, s).sum() >= 3 for s in 'TLR')


def place_floor(g, s, feet, padded):
    """Floor placement (rc.place / cg.place maths) of a source frame, optionally PAD-padded."""
    M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * feet]])
    if padded:
        M[:, 2] -= s * PAD
    grey = cv2.warpAffine(g, M, (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)


def prep_clean(g720):
    return cv2.GaussianBlur(cg.prep(g720), (0, 0), CLEAN_SIGMA)


# ------------------------------------------------------------------------------------------------ the timeline
class Line(gl.Line):
    def __init__(self, *a):
        super().__init__(*a)
        self.ph = {'R6': 0, 'R7': 0}

    def hit(self, f_from, size):
        self.add('A', range(f_from, 97), size)       # no f96 freeze

    def play(self, tag, gap, size, n):
        while gap > 0:
            if self.ph[tag] >= n:
                self.ph[tag] = 0                     # take ran out: back to its rest f0 (warped)
            k = min(gap, n - self.ph[tag])
            self.add(tag, range(self.ph[tag], self.ph[tag] + k), size)
            self.ph[tag] += k
            gap -= k

    def quiet(self, gap, size):
        self.play('R6', gap, size, self.p.n)

    def still(self, gap, size):
        self.play('R7', gap, size, self.n7)

    def speak(self, o0, o1, size):
        pos = o0
        for t, L in gl.CUES[self.beat]:
            if not (o0 <= t < o1):
                continue
            a, b, d = self.p.lift[L]
            s = max(pos, t - d)
            b = min(b, a + o1 - s)
            self.quiet(s - pos, size)
            self.add('R6', range(a, b), size)
            self.ph['R6'] = b                        # keep reading on from the end of the lift
            pos = s + (b - a)
        self.quiet(o1 - pos, size)


def timeline(beat, NT, NU, pcs, n7):
    n = ga.LENGTH[beat]
    size = SIZE[beat]
    L = Line(n, NT, NU, beat, pcs, n7)
    knocks = ga.KNOCKS[beat]
    L.hit(IMPACT_A - knocks[0][0], size)
    L.ret(size)
    for imp, q in knocks[1:]:
        u0 = imp - (IMPACT_A - 40) - NU
        L.idle(u0 - len(L.seq), size)
        L.raise_(size)
        if q == 'Q5':                                # the capper, one size: approved f40-95, black on the old frame
            L.add('A', range(40, 96), size)
            L.seq += [dict(src=None, f=None, size=None, impact=False, warp=None) for _ in range(n - len(L.seq))]
            break
        L.hit(40, size)
        L.ret(size)
    else:
        L.idle(n - len(L.seq), size)
    seq = L.seq[:n]
    assert len(seq) == n, (beat, len(seq))
    for imp, _ in knocks:
        assert seq[imp]['src'] == 'A' and seq[imp]['f'] == IMPACT_A, (beat, imp, seq[imp])
        seq[imp]['impact'] = True
    return seq, add_warps(seq)


def add_warps(seq):
    """lean.add_warps with longer eases: EASE_A at an approved join, EASE_I inside the idle."""
    rep = []
    for j in range(1, len(seq)):
        p, q = seq[j - 1], seq[j]
        if not p['src'] or not q['src']:
            continue
        if p['src'] == q['src'] and q['f'] in (p['f'], p['f'] + 1):
            continue
        if p['src'] == 'A' and q['src'] == 'A':
            continue
        E = EASE_A if 'A' in (p['src'], q['src']) else EASE_I
        if q['src'] != 'A':
            for i in range(E):
                k = j + i
                if k >= len(seq) or seq[k]['src'] != q['src'] or seq[k]['warp']:
                    break
                seq[k]['warp'] = (p['src'], p['f'], 1 - smooth((i + 1) / (E + 1)))
            rep.append((j, f"{p['src']}{p['f']}->{q['src']}{q['f']}", 'out'))
        else:
            for i in range(E):
                k = j - 1 - i
                if k < 0 or seq[k]['src'] != p['src']:
                    break
                seq[k]['warp'] = (q['src'], q['f'], 1 - smooth((i + 1) / (E + 1)))
            rep.append((j, f"{p['src']}{p['f']}->{q['src']}{q['f']}", 'in'))
    return rep


# ------------------------------------------------------------------------------------------------ the frames
def flow_warp_w(cur, target, wmap):
    """court_gen_lean.flow_warp with a per-pixel weight."""
    s = 0.5
    a = cv2.GaussianBlur(cv2.resize(target, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), (0, 0), 2)
    b = cv2.GaussianBlur(cv2.resize(cur, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), (0, 0), 2)
    fl = cv2.calcOpticalFlowFarneback((a * 255).astype(np.uint8), (b * 255).astype(np.uint8), None,
                                      0.5, 5, 25, 5, 7, 1.5, 0)
    fl = cv2.resize(fl, (cur.shape[1], cur.shape[0]), interpolation=cv2.INTER_LINEAR) / s
    h, wd = cur.shape[:2]
    gx, gy = np.meshgrid(np.arange(wd, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(cur, gx + wmap * fl[..., 0], gy + wmap * fl[..., 1], cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)


class Scene(gl.Scene):
    def __init__(self, fitd):
        super().__init__(fitd)
        self.rest = {}
        self.wmaps = {}

    def wmap(self, size):
        if size not in self.wmaps:
            s = cg.SIZES[size]['s']
            y_src = (np.arange(OH, dtype=np.float32) - (OH - s * cg.FEET_Y)) / s
            w = np.array([DAMP * smooth((y - NECK[0]) / (NECK[1] - NECK[0])) for y in y_src], np.float32)
            self.wmaps[size] = np.repeat(w[:, None], OW, 1)
        return self.wmaps[size]

    def raw(self, src, f, size):
        if src == 'A':
            g = self.src[f]
            pad = touches(g)
            return place_floor(extend(g) if pad else g, rc.SIZES[size]['s'], rc.FEET_Y, pad)
        g = prep_clean(self.takes[src][f])
        if src in 'TU':
            g = ga.apply_corr(g, ga.Scene.corr(self, src, f, size))
        pad = touches(g)
        return place_floor(extend(g) if pad else g, cg.SIZES[size]['s'], cg.FEET_Y, pad)

    def mask(self, src, f, size):
        key = (src, f, size)
        if key not in self.cache:
            if len(self.cache) > 40:
                self.cache.clear()
            m = self.raw(src, f, size).astype(np.float32)
            if src in ('R6', 'R7') and f:
                rk = (src, size)
                if rk not in self.rest:
                    self.rest[rk] = self.raw(src, 0, size).astype(np.float32)
                m = flow_warp_w(m, self.rest[rk], self.wmap(size))
            self.cache[key] = m
        return self.cache[key]

    def cl(self, src, f, size):
        if src == 'A':
            return max(a_closeness(f), CL_GEN)
        return CL_GEN


def build_seq(beat, sc=None):
    fitd = ga.load_fit()
    R6 = sc.takes['R6'] if sc else cg.load_take(gl.take_path('R6'))
    n7 = len(sc.takes['R7']) if sc else len(cg.load_take(gl.take_path('R7')))
    return timeline(beat, fitd['frames']['T'], fitd['frames']['U'], gl.Pieces(R6), n7)


def frames(beat, clean=False):
    sc = Scene(ga.load_fit())
    seq, _ = build_seq(beat, sc)
    t0 = BEAT_T0[5 if beat == '5cut' else beat]
    rng = np.random.default_rng(1817)
    shake = 0
    for n, s in enumerate(seq):
        if s['src'] is None:
            yield np.zeros((OH, OW, 3), np.float32)
            continue
        m = sc.mask(s['src'], s['f'], s['size'])
        cl = sc.cl(s['src'], s['f'], s['size'])
        if s['warp']:
            ws, wf, w = s['warp']
            m = gl.flow_warp(m, sc.mask(ws, wf, s['size']), w)
            cl = cl * (1 - w) + sc.cl(ws, wf, s['size']) * w
        im = compose_opaque(sc, n, t0, m, cl, clean)
        if s['impact']:
            shake = 6
        if shake:
            amp = 7 * shake / 6
            dx, dy = rng.integers(-amp, amp + 1, 2)
            im = np.roll(im, (int(dy), int(dx)), (0, 1)) * (1 + 0.05 * shake / 6)
            shake -= 1
        yield im


def render(out, beat, clean=False):
    if os.path.exists(out):
        raise SystemExit(f'refusing: {out} exists')
    tmp = os.path.join(os.path.dirname(out), '_tmp_' + os.path.basename(out))
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    k = 0
    for im in frames(beat, clean):
        w.stdin.write((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        k += 1
        if k % 120 == 0:
            print(f'{k} frames', flush=True)
    w.stdin.close()
    if w.wait() != 0:
        raise SystemExit('ffmpeg failed')
    os.replace(tmp, out)
    print(k, 'frames ->', out, 'DONE', flush=True)


def plan(beat):
    seq, rep = build_seq(beat)
    print(f'beat {beat}: {len(seq)} frames, size {SIZE[beat]}')
    for r in ga.describe(seq):
        print(f"  out {r['o0']:5d}-{r['o1']:5d} ({r['o0'] / FPS:6.2f} s)  {r['src']} f{r['f0']}-{r['f1']}  {r['q']}")
    for j, k, d in rep:
        print(f'  join out {j:5d} {k} warp {d}')
    print('  impacts at out', [i for i, s in enumerate(seq) if s['impact']])


def sheets(video, beat, prefix):
    """Joins -6..+6 every 2 frames, strikes -6..+6, and the clipped-edge frames, from the rendered video."""
    seq, rep = build_seq(beat)
    rows = [(k, list(range(j - 6, j + 7, 2)), [f'{i} {seq[i]["src"]}{seq[i]["f"]}' for i in range(j - 6, j + 7, 2)])
            for j, k, _ in rep if j + 6 < len(seq)]
    srows = [(f'impact @{imp}', list(range(imp - 12, imp + 1, 2)),
              [f'{i} {seq[i]["src"]}{seq[i]["f"]}' for i in range(imp - 12, imp + 1, 2)]) for imp, _ in ga.KNOCKS[beat]]
    allidx = [i for _, ix, _ in rows + srows for i in ix if 0 <= i < len(seq)]
    fr, wh = ga.read_frames(video, allidx, 260)
    half = (len(rows) + 1) // 2
    ga.sheet(rows[:half], fr, wh, prefix + '_joinsA.png', f'{os.path.basename(video)}  joins -6..+6')
    if rows[half:]:
        ga.sheet(rows[half:], fr, wh, prefix + '_joinsB.png', f'{os.path.basename(video)}  joins -6..+6')
    ga.sheet(srows, fr, wh, prefix + '_strikes.png', f'{os.path.basename(video)}  raise -> impact (clipped edges)')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['plan', 'render', 'sheets'])
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--clean', action='store_true')
    ap.add_argument('--prefix')
    a = ap.parse_args()
    if a.cmd == 'plan':
        plan(a.beat)
    elif a.cmd == 'render':
        render(a.out, a.beat, a.clean)
    else:
        sheets(a.out, a.beat, a.prefix)
