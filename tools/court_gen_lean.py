"""Scene 9 court beats, LEAN judge (M9s, 2026-11-20): the APPROVED strike unchanged, the v6 READ / v7 STILL takes around
it, steady middle blur, flow-eased shape match at every join. REVIEW only, 0 credits.

NEW FILE beside court_gen_approved.py (imported, never changed), so the shipped beats and the M9o review stay
bit-identical. Plan: docs/S9-JUDGE-VO-PLAN.md (REVISED), docs/HANDOFF-2026-11-20-M9r.md Next 2. Homie (M9p): no sharp nod,
no leg shift, still when the dialogue is over, seamless strike <-> idle on giant screens, no quality drop gavel -> idle.

SOURCES: A approved fig_SOTR_judge_strike_s9_v1 (frames untouched) · T v4 RETURN · U v5 RAISE (rigid corrections as
court_gen_approved) · R6 v6 READ (bc52970f, 481 f; head-lifts to the court f104-160 and f248-305) · R7 v7 STILL.
PERFORMANCE (docs/S9-JUDGE-LINES.md): while Darren speaks = R6; after a dialogue end = R7 (breathing only).
  b3 speak 225-706 = R6 whole (lifts land on his reading), still 706-960.
  b5cut: R6 lift 1 placed on "Order! Order!" (867), lift 2 on "Get the traitors out" (957); still from 1010 to the
  RAISE and after the last "Order!" (1358).
BLUR (compose_opaque closeness, 0 = far blur, 1 = sharp): every generated frame CL_MID = 0.48 (= approved f67); RETURN
eases 1 -> CL_MID over its first 24 f; RAISE eases CL_MID -> 0 (= approved f40) over its last 24 f. Approved frames keep
their own closeness.
JOINS: no crossfades. At each source change / idle cut the generated side is warped by optical flow onto the frame it
joins, the warp easing out (or in, before an approved frame) over EASE frames. Approved frames are never warped.

  python tools/court_gen_lean.py plan --beat 3|5cut|7
  python tools/court_gen_lean.py render OUT.mp4 --beat 3|5cut|7
"""
import argparse
import glob
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
import court_gen as cg  # noqa: E402
import court_gen_approved as ga  # noqa: E402
from court_burn import BEAT_T0  # noqa: E402
from court_behind_paper import compose_opaque, closeness as a_closeness  # noqa: E402

GEN = cg.GEN
OW, OH, FPS = rc.OW, rc.OH, rc.FPS
IMPACT_A = ga.IMPACT_A
CL_MID = 0.48
EASE_CL = 24
EASE = 14
LIFT_ONSET = {'L1': 104, 'L2': 248}
STILL = {3: [(706, 10 ** 9)], '5cut': [(1010, 1168), (1358, 10 ** 9)], 7: []}
CUES = {3: [], '5cut': [(867, 'L1'), (957, 'L2')], 7: []}


def take_path(tag):
    if tag in 'TU':
        return ga.take_path(tag)
    pat = {'R6': 'S9-CRT-IDLE_v6_read_*.mp4', 'R7': 'S9-CRT-IDLE_v7_still_*.mp4'}[tag]
    p = sorted(glob.glob(os.path.join(GEN, pat)))
    assert len(p) == 1, (tag, p)
    return p[0]


def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


class Pieces:
    """R6 rest cut points and its two lift pieces."""

    def __init__(self, R6):
        self.j = cg.Joins(R6)
        cuts = self.j.cuts
        self.n = len(R6)
        self.lift = {}
        for k, on in LIFT_ONSET.items():
            a = max(c for c in cuts if c <= on - 4)
            b = min(c for c in cuts if c >= on + 60)
            self.lift[k] = (a, b, on - a)


class Line(ga.Line):
    def __init__(self, n, NT, NU, beat, pcs, n7):
        self.n, self.NT, self.NU, self.beat, self.p, self.n7 = n, NT, NU, beat, pcs, n7
        self.seq = []

    def add(self, src, frames, size):
        for f in frames:
            self.seq.append(dict(src=src, f=f, size=size, impact=False, warp=None))

    def speak(self, o0, o1, size):
        pos = o0
        for t, L in CUES[self.beat]:
            if not (o0 <= t < o1):
                continue
            a, b, d = self.p.lift[L]
            s = max(pos, t - d)
            self.quiet(s - pos, size)
            self.add('R6', range(a, b), size)
            pos = s + (b - a)
        self.quiet(o1 - pos, size)

    def quiet(self, gap, size):
        if gap <= 0:
            return
        segs = [(0, gap)] if gap <= self.p.n else self.p.j.fill(gap, np.random.default_rng(1820))
        for a, b in segs:
            self.add('R6', range(a, b), size)

    def still(self, gap, size):
        while gap > 0:
            k = min(gap, self.n7)
            self.add('R7', range(k), size)
            gap -= k

    def idle(self, gap, size, to_end=False):
        o0, o1 = len(self.seq), len(self.seq) + gap
        cuts = sorted([o0, o1] + [x for s in STILL[self.beat] for x in s if o0 < x < o1])
        for a, b in zip(cuts, cuts[1:]):
            is_still = any(s0 <= a and b <= s1 for s0, s1 in STILL[self.beat])
            (self.still if is_still else self.speak)(a, b, size) if is_still else self.speak(a, b, size)
            if is_still:
                pass
        assert len(self.seq) == o1, (self.beat, len(self.seq), o1)


def _idle(self, gap, size, to_end=False):
    o0, o1 = len(self.seq), len(self.seq) + gap
    pts = sorted(set([o0, o1] + [x for s in STILL[self.beat] for x in s if o0 < x < o1]))
    for a, b in zip(pts, pts[1:]):
        if any(s0 <= a and b <= s1 for s0, s1 in STILL[self.beat]):
            self.still(b - a, size)
        else:
            self.speak(a, b, size)
    assert len(self.seq) == o1, (self.beat, len(self.seq), o1)


Line.idle = _idle


def timeline(beat, NT, NU, pcs, n7):
    """court_gen_approved.timeline with the lean idle (same strikes, RETURNs, RAISEs, capper)."""
    n = ga.LENGTH[beat]
    L = Line(n, NT, NU, beat, pcs, n7)
    knocks = ga.KNOCKS[beat]
    size = ga.FIRST[beat]
    imp0 = knocks[0][0]
    size = L.hit(IMPACT_A - imp0, size, knocks[0][1])
    L.ret(size)
    for imp, q in knocks[1:]:
        u0 = imp - (IMPACT_A - 40) - NU
        L.idle(u0 - len(L.seq), size)
        L.raise_(size)
        if q == 'Q5':
            L.add('A', range(40, 47), size)
            L.add('A', range(47, 60), 'Q5')
            L.add('A', [96] * 36, 'Q5')
            L.seq += [dict(src=None, f=None, size=None, impact=False, warp=None) for _ in range(n - len(L.seq))]
            break
        size = L.hit(40, size, q)
        L.ret(size)
    else:
        L.idle(n - len(L.seq), size)
    seq = L.seq[:n]
    assert len(seq) == n
    for imp, _ in knocks:
        assert seq[imp]['src'] == 'A' and seq[imp]['f'] == IMPACT_A, (beat, imp)
        seq[imp]['impact'] = True
    add_warps(seq)
    return seq


def add_warps(seq):
    """At every discontinuity: warp the generated side onto the frame across the join, easing over EASE frames."""
    rep = []
    for j in range(1, len(seq)):
        p, q = seq[j - 1], seq[j]
        if not p['src'] or not q['src']:
            continue
        if p['src'] == q['src'] and q['f'] in (p['f'], p['f'] + 1):
            continue
        if p['src'] == 'A' and q['src'] == 'A':
            continue
        if q['src'] != 'A':          # warp the next frames onto the previous frame, easing out
            for i in range(EASE):
                k = j + i
                if k >= len(seq) or seq[k]['src'] != q['src'] or seq[k]['warp']:
                    break
                seq[k]['warp'] = (p['src'], p['f'], 1 - smooth((i + 1) / (EASE + 1)))
            rep.append((j, f"{p['src']}->{q['src']}", 'out'))
        else:                        # generated -> approved: warp the last frames onto the approved frame, easing in
            for i in range(EASE):
                k = j - 1 - i
                if k < 0 or seq[k]['src'] != p['src']:
                    break
                seq[k]['warp'] = (q['src'], q['f'], 1 - smooth((i + 1) / (EASE + 1)))
            rep.append((j, f"{p['src']}->{q['src']}", 'in'))
    seq_rep[id(seq)] = rep


seq_rep = {}


class Scene(ga.Scene):
    def __init__(self, fitd):
        from render_court_v2 import SIZES as V2, field_static
        from court_burn import BurnEdges
        from court_behind_paper import fibre
        for q in ('Q1', 'Q2', 'Q3'):
            rc.SIZES[q] = V2[q]
        self.base, self.lamp, self.plain, self.far, self.near = field_static(layers=True)
        self.burn = BurnEdges(OW, OH)
        self.fib = fibre()
        self.src = rc.load_source()
        self.gbox = rc.gavel_box(self.src[rc.HELD])
        self.takes = {k: cg.load_take(take_path(k)) for k in ('T', 'U', 'R6', 'R7')}
        self.fitd = fitd
        self.cache = {}

    def mask(self, src, f, size):
        key = (src, f, size)
        if key not in self.cache:
            if len(self.cache) > 16:
                self.cache.clear()
            if src in ('R6', 'R7'):
                self.cache[key] = cg.place(cg.prep(self.takes[src][f]), size)
            else:
                return ga.Scene.mask(self, src, f, size)
        return self.cache[key]

    def cl(self, src, f, size):
        if size == 'Q5':
            return 1.0
        if src == 'A':
            return a_closeness(f)
        if src == 'T':
            return 1 + (CL_MID - 1) * smooth(f / EASE_CL)
        if src == 'U':
            n = len(self.takes['U'])
            return CL_MID * (1 - smooth((f - (n - 1 - EASE_CL)) / EASE_CL))
        return CL_MID


def flow_warp(cur, target, w):
    """Warp mask `cur` (grey, 1 = field, 0 = figure) toward `target` by weight w (1 = target's shape)."""
    if w <= 0.001:
        return cur
    s = 0.5
    a = cv2.GaussianBlur(cv2.resize(target, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), (0, 0), 2)
    b = cv2.GaussianBlur(cv2.resize(cur, None, fx=s, fy=s, interpolation=cv2.INTER_AREA), (0, 0), 2)
    fl = cv2.calcOpticalFlowFarneback((a * 255).astype(np.uint8), (b * 255).astype(np.uint8), None,
                                      0.5, 5, 25, 5, 7, 1.5, 0)
    fl = cv2.resize(fl, (cur.shape[1], cur.shape[0]), interpolation=cv2.INTER_LINEAR) / s
    h, wd = cur.shape[:2]
    gx, gy = np.meshgrid(np.arange(wd, dtype=np.float32), np.arange(h, dtype=np.float32))
    return cv2.remap(cur, gx + w * fl[..., 0], gy + w * fl[..., 1], cv2.INTER_LINEAR,
                     borderMode=cv2.BORDER_CONSTANT, borderValue=1.0)


def build_seq(beat, sc=None):
    fitd = ga.load_fit()
    R6 = sc.takes['R6'] if sc else cg.load_take(take_path('R6'))
    n7 = len(sc.takes['R7']) if sc else len(cg.load_take(take_path('R7')))
    return timeline(beat, fitd['frames']['T'], fitd['frames']['U'], Pieces(R6), n7)


def frames(beat, clean=False):
    sc = Scene(ga.load_fit())
    seq = build_seq(beat, sc)
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
            m = flow_warp(m.astype(np.float32), sc.mask(ws, wf, s['size']).astype(np.float32), w)
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
    print(k, 'frames ->', out, flush=True)


def plan(beat):
    seq = build_seq(beat)
    print(f'beat {beat}: {len(seq)} frames')
    for r in ga.describe(seq):
        print(f"  out {r['o0']:5d}-{r['o1']:5d} ({r['o0'] / FPS:6.2f} s)  {r['src']} f{r['f0']}-{r['f1']}  {r['q']}")
    for j, k, d in seq_rep[id(seq)]:
        print(f'  join out {j:5d} {k} warp {d}')
    print('  impacts at out', [i for i, s in enumerate(seq) if s['impact']])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['plan', 'render'])
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--clean', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'plan':
        plan(a.beat)
    else:
        render(a.out, a.beat, a.clean)
