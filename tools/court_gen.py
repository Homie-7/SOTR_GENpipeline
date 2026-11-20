"""Scene 9 court beats with the GENERATED judge (S9-CRT-IDLE v2 strike + v3 reading idle), opaque, for REVIEW.

Built 2026-11-20 (Claude, worker for the M9 live chat; Homie M9m: "I need to see the whole scene 9 run with this new
adjustment and idle animations and everything done properly"). Script, 0 credits. NEW CODE BESIDE the shipped path:
render_court.py / court_behind_paper.py are imported, never changed, so the shipped beats stay bit-identical.

SOURCES (04_WORKING_FILES/S9_judge_generated_idle, 720x1280, 24 fps, 361 frames, both start and end on one rest pose):
  S = S9-CRT-IDLE_v2_strike_91fd62a7.mp4  reads f0-90, raises f90-140, the gavel ARRIVES at the lens on f142 (IMPACT),
      held to ~f213, lowered by ~f245, reads, rest again at f312-321 and f357-360.
      Defect: a thin white horizontal line rows ~374-395 (720 px) through gavel + body, f142-208: repaired per column
      by interpolating across the band (the line is detected per frame: a full-width bright row run).
  R = S9-CRT-IDLE_v3_read_07416a29.mp4    reading idle; near-rest (mask xor vs f0 < ~1100 px of ~225k) at f0-15,
      ~75-105, ~201-225, ~285 and ~345-360. Those are the ONLY join points: every join is rest-to-rest.
Frames are upscaled x1.5 in grey (1080x1920) and go through render_court's placement + the A2/opaque layering
(court_behind_paper.compose_opaque, 'front': windows < railing < the judge, opaque).

MEASURED (2026-11-20) against the approved strike clip: rest pose feet at 1080-row ~1719 (FEET_Y 1732, the same +13
as render_court's 1773 -> 1786); head-top-to-feet 1453 px vs 1483 in the approved clip, so every size scale is / 0.98
(the judge stands the same height on the wall). Q4 centre re-measured on the head/chest (570, 491). Q5 = the gavel's
box at the lens, by hand (1080 px: x 15-533, y 60-1020).

TIMING: each strike's impact frame (S f142) lands on the frame holding Darren's knock onset in his mix (matched filter,
r 0.81-0.93: 78.918 / 190.818 / 212.500 / 243.033 / 287.147 / 302.355 s on the review clock). Q changes only on an
impact (b5 Q2 -> Q3 on strike 2, b7 Q4 -> Q5 on the capper). The capper holds Q5 43 frames after impact, then black,
as render_court's capper. The gaps between strike takes are filled with R segments cut rest-to-rest (a small DP).

  python tools/court_gen.py OUT.mp4 --beat 3|5cut|7 [--clean] [--plan]
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
from render_court_v2 import field_static, SIZES as V2  # noqa: E402
from court_burn import BurnEdges, BEAT_T0  # noqa: E402
from court_behind_paper import compose_opaque, fibre  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
GEN = os.path.join(HERE, '..', '..', 'SOTR_MEDIA', '04_WORKING_FILES', 'S9_judge_generated_idle')
TAKES = {'S': os.path.join(GEN, 'S9-CRT-IDLE_v2_strike_91fd62a7.mp4'),
         'R': os.path.join(GEN, 'S9-CRT-IDLE_v3_read_07416a29.mp4')}
OW, OH, FPS = rc.OW, rc.OH, rc.FPS
GW, GH = 720, 1280
SW, SH = 1080, 1920
FEET_Y = 1732
K = 1453 / 1483                    # new judge height / approved judge height (head top to feet)
SIZES = {
    'Q1': dict(s=V2['Q1']['s'] / K, floor=True),
    'Q2': dict(s=V2['Q2']['s'] / K, floor=True),
    'Q3': dict(s=V2['Q3']['s'] / K, floor=True),
    'Q4': dict(s=1.45 / K, floor=False, cx=570, cy=491),
}
GAVEL = (15, 60, 518, 960)         # x, y, w, h at 1080x1920, by hand on S f145-215
IMPACT = 142                       # S: the gavel arrives at the lens
CAP_HOLD = 43                      # frames of Q5 after the capper's impact, then black (render_court: 6 + 36 + 1)
EXIT_S = [312, 313, 314, 315, 316, 317, 318, 357, 358, 359, 360]   # S frames to leave the strike take (near rest)
# Darren's knocks, in frames from each court file's start on the review clock (s9_darren_review.clips())
KNOCKS = {3: [(37, 'Q1')], '5cut': [(25, 'Q2'), (546, 'Q3'), (1278, 'Q3')], 7: [(23, 'Q4'), (388, 'Q5')]}
LENGTH = {3: 960, '5cut': 1542, 7: 480}
FIRST = {3: 'Q1', '5cut': 'Q2', 7: 'Q4'}


def load_take(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, GH, GW)


def repair_line(g):
    """The S take's white horizontal line (S f142-216): rows in 250-700 that are > 40 brighter than BOTH the rows 6 px
    above and below in >= 300 of 720 columns. Catches the full-width line and its fading, partial tail (f209-216) that
    a plain brightness test missed; no other frame of S or R trips it (max 219 columns). Each column is interpolated
    across the band (+3 px margin each side) from the rows just outside it."""
    gi = g.astype(np.int16)
    nb = np.minimum(gi[244:694], gi[256:706])
    cnt = ((gi[250:700] - nb) > 40).sum(1)
    rows = np.nonzero(cnt >= 300)[0] + 250
    if not len(rows):
        return g, None
    y0, y1 = int(rows[0]) - 3, int(rows[-1]) + 3
    g = g.astype(np.float32).copy()
    a, b = g[y0 - 1], g[y1 + 1]
    t = ((np.arange(y0, y1 + 1) - (y0 - 1)) / (y1 + 2 - y0))[:, None]
    g[y0:y1 + 1] = a[None] * (1 - t) + b[None] * t
    return g, (y0, y1)


def prep(g720):
    """720 grey uint8 -> 1080x1920 float 0..1 grey, line repaired, small white specks inside the black filled."""
    g, _ = repair_line(g720)
    g = cv2.resize(np.asarray(g, np.float32), (SW, SH), interpolation=cv2.INTER_CUBIC) / 255.0
    black = (g < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 600 and not (x == 0 or y == 0 or x + w >= SW or y + h >= SH):
            g[lab == i] = 0.0
    return g


def place(g, size):
    if size == 'Q5':
        x, y, w, h = GAVEL
        s = OH * 1.05 / h
        M = np.float32([[s, 0, OW / 2 - s * (x + w / 2)], [0, s, OH / 2 - s * (y + h / 2)]])
    else:
        sz = SIZES[size]
        s = sz['s']
        if sz['floor']:
            M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * FEET_Y]])
        else:
            M = np.float32([[s, 0, OW / 2 - s * sz['cx']], [0, s, OH / 2 - s * sz['cy']]])
    grey = cv2.warpAffine(g, M, (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)


def closeness(take, f):
    """A2 sharpness: 0 at rest/reading, rising through the raise to 1 at the lens, back to 0 as the gavel lowers."""
    if take != 'S':
        return 0.0
    if f <= IMPACT:
        return float(np.clip((f - 118) / (IMPACT - 118), 0, 1))
    return float(np.clip(1 - (f - 213) / 32, 0, 1))


# ------------------------------------------------------------------------------------------------ the timeline
class Joins:
    def __init__(self, R):
        m = R < 128
        self.m = m
        xr = np.array([np.logical_xor(f, m[0]).sum() for f in m])
        self.cuts = [i for i in range(len(R)) if xr[i] < 1100]

    def fill(self, gap, rng):
        """Rest-to-rest R segments [(a, b)] whose lengths sum to gap: fewest segments, long ones (alive), each join's
        mask difference small. A filler under 16 frames is R[0:g] (its first frames barely move)."""
        if gap <= 0:
            return []
        if gap < 16:
            return [(0, gap)]
        segs = [(a, b) for a in self.cuts for b in self.cuts if b - a >= 48]
        segs += [(0, g) for g in range(1, 16)]
        INF = 1e9
        best = [INF] * (gap + 1)
        how = [None] * (gap + 1)
        best[0] = 0
        jit = {s: rng.random() * 0.01 for s in segs}
        for L in range(1, gap + 1):
            for s in segs:
                n = s[1] - s[0]
                if n <= L and best[L - n] + 1 + jit[s] < best[L]:
                    best[L] = best[L - n] + 1 + jit[s]
                    how[L] = s
        out, L = [], gap
        while L > 0:
            s = how[L]
            out.append(s)
            L -= s[1] - s[0]
        # order: longest first, no identical neighbours where avoidable
        out.sort(key=lambda s: -(s[1] - s[0]))
        return out


def timeline(beat, S, R, seed=1820):
    """[(take, frame, size, impact)] per output frame; take None = black."""
    n = LENGTH[beat]
    rng = np.random.default_rng(seed)
    joins = Joins(R)
    seq = []
    size = FIRST[beat]
    knocks = KNOCKS[beat]
    for k, (imp, q) in enumerate(knocks):
        start = imp - IMPACT
        if k == 0:
            enter = -start if start < 0 else 0
            if start > 0:  # rest before the first strike
                seq += [('R', a + i, size) for a, b in joins.fill(start, rng) for i in range(b - a)]
        else:
            enter = 0
            gap = start - len(seq)
            assert gap >= 0, (beat, k, gap)
            seq += [('R', a + i, size) for a, b in joins.fill(gap, rng) for i in range(b - a)]
        assert len(seq) == max(start, 0), (len(seq), start)
        last = k + 1 == len(knocks)
        if q == 'Q5':      # the capper: the take to the impact at the current size, then Q5 held, then black
            seq += [('S', f, size) for f in range(enter, IMPACT)]
            seq += [('S', f, 'Q5') for f in range(IMPACT, IMPACT + CAP_HOLD)]
            seq += [(None, None, None)] * (n - len(seq))
            break
        if q != size:
            pre = [('S', f, size) for f in range(enter, IMPACT)]
            size = q
        else:
            pre = [('S', f, size) for f in range(enter, IMPACT)]
        seq += pre
        if last:
            tail = [('S', f, size) for f in range(IMPACT, 361)]
            seq += tail[:n - len(seq)]
            rest = n - len(seq)
            if rest > 0:   # the file's end is not a join: one R run from rest, as long as it needs (fill if > 1 take)
                segs = [(0, rest)] if rest <= len(R) else joins.fill(rest, rng)
                seq += [('R', a + i, size) for a, b in segs for i in range(b - a)]
        else:
            # choose the exit frame whose remaining gap fills best (prefer the take's true end)
            nxt = knocks[k + 1][0] - IMPACT
            best = None
            for ex in sorted(EXIT_S, reverse=True):
                gap = nxt - (len(seq) + ex - IMPACT)
                if gap < 0:
                    continue
                segs = joins.fill(gap, np.random.default_rng(seed + k))
                score = len(segs) + (0.5 if any(b - a < 16 for a, b in segs) and gap >= 16 else 0)
                if best is None or score < best[0]:
                    best = (score, ex)
            seq += [('S', f, size) for f in range(IMPACT, best[1])]
    seq = seq[:n]
    out = []
    imps = {imp for imp, _ in knocks}
    for i, (t, f, q) in enumerate(seq):
        out.append((t, f, q, i in imps))
    assert len(out) == n
    return out


def describe(seq):
    """Runs of contiguous frames from one take, for the plan printout and the joins report."""
    runs = []
    for i, (t, f, q, imp) in enumerate(seq):
        if runs and runs[-1]['take'] == t and t is not None and f == runs[-1]['f1'] + 1:
            runs[-1]['f1'] = f
            runs[-1]['o1'] = i
            if q not in runs[-1]['q']:
                runs[-1]['q'].append(q)
        elif runs and t is None and runs[-1]['take'] is None:
            runs[-1]['o1'] = i
        else:
            runs.append(dict(take=t, f0=f, f1=f, o0=i, o1=i, q=[q]))
    return runs


# ------------------------------------------------------------------------------------------------ the frames
class GenScene:
    def __init__(self):
        self.base, self.lamp, self.plain, self.far, self.near = field_static(layers=True)
        self.burn = BurnEdges(OW, OH)
        self.fib = fibre()
        self.takes = {k: load_take(p) for k, p in TAKES.items()}
        self.cache = {}

    def mask(self, take, f, size):
        k = (take, f, size)
        if k not in self.cache:
            if len(self.cache) > 6:
                self.cache.clear()
            self.cache[k] = place(prep(self.takes[take][f]), size)
        return self.cache[k]


def frames_gen(beat, clean=False):
    sc = GenScene()
    seq = timeline(beat, sc.takes['S'], sc.takes['R'])
    t0 = BEAT_T0[5 if beat == '5cut' else beat]
    rng = np.random.default_rng(1817)
    shake = 0
    for n, (take, f, sz, impact) in enumerate(seq):
        if take is None:
            yield np.zeros((OH, OW, 3), np.float32)
            continue
        cl = 1.0 if sz == 'Q5' else closeness(take, f)
        im = compose_opaque(sc, n, t0, sc.mask(take, f, sz), cl, clean)
        if impact:
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
    for im in frames_gen(beat, clean):
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
    S, R = load_take(TAKES['S']), load_take(TAKES['R'])
    seq = timeline(beat, S, R)
    m = {'S': S < 128, 'R': R < 128}
    runs = describe(seq)
    print(f'beat {beat}: {len(seq)} frames')
    for i, r in enumerate(runs):
        j = ''
        if i and r['take'] and runs[i - 1]['take']:
            p = runs[i - 1]
            j = f"  join xor {int(np.logical_xor(m[p['take']][p['f1']], m[r['take']][r['f0']]).sum())} px (720)"
        print(f"  out {r['o0']:5d}-{r['o1']:5d} ({r['o0'] / FPS:6.2f} s)  {r['take']} f{r['f0']}-{r['f1']}  {r['q']}{j}")
    print('  impacts at out', [i for i, s in enumerate(seq) if s[3]], '-> take frames',
          [(s[0], s[1], s[2]) for s in seq if s[3]])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', required=True, type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--clean', action='store_true')
    ap.add_argument('--plan', action='store_true')
    a = ap.parse_args()
    if a.plan:
        plan(a.beat)
    else:
        render(a.out, a.beat, a.clean)
