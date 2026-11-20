"""Scene 9 court beats: the APPROVED gavel strike, unchanged, inside the GENERATED judge idle. REVIEW only, 0 credits.

Built 2026-11-20 (Claude, worker for the M9 live chat). Plan: SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review/
_PLAN_approved_strike.md section 4. Homie (M9o): "make sure it's not changing, we are just adding things around it" /
"I just don't want you to change the animation of the guy hitting the gavel" / "Yes, both (63 cr)".

NEW CODE BESIDE the shipped path and beside court_gen.py: render_court / court_behind_paper / court_gen are imported,
never changed, so the shipped beats and the v2-strike review build stay bit-identical.

FOUR SOURCES, one opaque judge (court_behind_paper.compose_opaque, 'front': windows < railing < judge):
  A  fig_SOTR_judge_strike_s9_v1 (approved, 1080x1920, f0-96, impact f53, held f96). Frames UNCHANGED: rc.load_source
     (epaulette fill < 600 px keeps the keyline ring) + rc.place (V2 Q1-Q3, rc Q4, Q5 = the gavel box), A2 closeness
     court_behind_paper.closeness(f). Exactly the shipped hit path.
  R  S9-CRT-IDLE_v3 reading idle (720p), rest-to-rest segments (court_gen.Joins), court_gen.prep/place.
  T  S9-CRT-IDLE_v4 RETURN bridge (approved f96 -> rest), court_gen.prep/place + a rigid correction.
  U  S9-CRT-IDLE_v5 RAISE bridge (rest -> approved f40), same.
RIGID CORRECTION (scale + shift only, NO warp): measured per bridge END against the frame it joins (A f96 / A f40 in the
generated source frame for 'floor' sizes and for Q4; R f0 at the rest end), uniform scale about the feet point
(540, court_gen.FEET_Y) + shift, by IoU of the black masks. Ramped over the take with a smoothstep from one end's value
to the other's. A join whose IoU after correction is < 0.97 gets a short crossfade of the two masks (2-4 frames by
IoU), always on the bridge's side, so approved frames stay pure from f40 (or the beat start) to f96.

  python tools/court_gen_approved.py fit                       measure the corrections + IoUs (json beside the takes)
  python tools/court_gen_approved.py plan --beat 3|5cut|7      print the timeline runs and joins
  python tools/court_gen_approved.py render OUT.mp4 --beat 3|5cut|7
  python tools/court_gen_approved.py sheets VIDEO.mp4 --beat B --prefix OUTPREFIX   joins / strikes / overview
"""
import argparse
import glob
import json
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
import court_gen as cg  # noqa: E402
from render_court_v2 import SIZES as V2  # noqa: E402
from court_burn import BEAT_T0  # noqa: E402
from court_behind_paper import compose_opaque, closeness as a_closeness  # noqa: E402

GEN = cg.GEN
OW, OH, FPS = rc.OW, rc.OH, rc.FPS
SW, SH = 1080, 1920
IMPACT_A = 53
FIT_JSON = os.path.join(GEN, '_bridge_fit_approved_strike.json')


def take_path(tag):
    pat = {'R': 'S9-CRT-IDLE_v3_read_*.mp4', 'T': 'S9-CRT-IDLE_v4_return_*.mp4', 'U': 'S9-CRT-IDLE_v5_raise_*.mp4'}[tag]
    p = sorted(glob.glob(os.path.join(GEN, pat)))
    assert len(p) == 1, (tag, p)
    return p[0]


def kind(size):
    return 'Q4' if size == 'Q4' else 'floor'


def a_to_gen(a, k):
    """An approved 1080x1920 grey frame mapped into the generated takes' source frame, so that court_gen.place(result,
    size) puts it exactly where rc.place(a, size) does (floor sizes share one map, Q4 has its own)."""
    K = cg.K
    if k == 'floor':
        cx_a, cy_a, cx_g, cy_g = SW / 2, rc.FEET_Y, SW / 2, cg.FEET_Y
    else:
        cx_a, cy_a, cx_g, cy_g = rc.SIZES['Q4']['cx'], rc.SIZES['Q4']['cy'], cg.SIZES['Q4']['cx'], cg.SIZES['Q4']['cy']
    M = np.float32([[K, 0, cx_g - K * cx_a], [0, K, cy_g - K * cy_a]])
    return cv2.warpAffine(a, M, (SW, SH), flags=cv2.INTER_CUBIC, borderValue=1.0)


def corr_matrix(c):
    s, dx, dy = c
    ax, ay = SW / 2, cg.FEET_Y
    return np.float32([[s, 0, ax - s * ax + dx], [0, s, ay - s * ay + dy]])


def apply_corr(g, c, scale=1.0):
    if c == (1.0, 0.0, 0.0):
        return g
    M = corr_matrix(c)
    if scale != 1.0:
        M = M.copy()
        M[:, 2] *= scale
        w, h = int(round(SW * scale)), int(round(SH * scale))
        return cv2.warpAffine(g, M, (w, h), flags=cv2.INTER_LINEAR, borderValue=1.0)
    return cv2.warpAffine(g, M, (SW, SH), flags=cv2.INTER_CUBIC, borderValue=1.0)


def iou(a, b):
    return float(np.logical_and(a, b).sum() / max(np.logical_or(a, b).sum(), 1))


def fit(moving, target):
    """Best (s, dx, dy) putting `moving` (generated grey) on `target` (grey, same frame), by IoU of black. Coarse at
    1/4 size, then refined at full size."""
    q = 0.25
    tq = cv2.resize(target, None, fx=q, fy=q, interpolation=cv2.INTER_AREA) < 0.5
    mq = cv2.resize(moving, None, fx=q, fy=q, interpolation=cv2.INTER_AREA)
    best = (-1, (1.0, 0.0, 0.0))
    for s in np.arange(0.90, 1.1001, 0.005):
        for dx in range(-60, 61, 4):
            for dy in range(-60, 61, 4):
                c = (float(s), float(dx), float(dy))
                M = corr_matrix(c)
                M[:, 2] *= q
                w = cv2.warpAffine(mq, M, (tq.shape[1], tq.shape[0]), flags=cv2.INTER_LINEAR, borderValue=1.0) < 0.5
                v = iou(w, tq)
                if v > best[0]:
                    best = (v, c)
    t = target < 0.5
    s0, x0, y0 = best[1]
    best = (-1, best[1])
    for s in np.arange(s0 - 0.006, s0 + 0.0061, 0.001):
        for dx in range(int(x0) - 4, int(x0) + 5):
            for dy in range(int(y0) - 4, int(y0) + 5):
                c = (round(float(s), 4), float(dx), float(dy))
                v = iou(apply_corr(moving, c) < 0.5, t)
                if v > best[0]:
                    best = (v, c)
    return best


def measure():
    src = rc.load_source()
    R = cg.load_take(take_path('R'))
    T = cg.load_take(take_path('T'))
    U = cg.load_take(take_path('U'))
    r0 = cg.prep(R[0])
    out = {'files': {k: os.path.basename(take_path(k)) for k in 'RTU'}, 'frames': {'T': len(T), 'U': len(U)}}
    ends = {
        'T_start': (cg.prep(T[0]), {k: a_to_gen(src[96], k) for k in ('floor', 'Q4')}),
        'T_end': (cg.prep(T[-1]), {'rest': r0}),
        'U_start': (cg.prep(U[0]), {'rest': r0}),
        'U_end': (cg.prep(U[-1]), {k: a_to_gen(src[40], k) for k in ('floor', 'Q4')}),
    }
    for name, (mov, tg) in ends.items():
        for k, t in tg.items():
            raw = iou(mov < 0.5, t < 0.5)
            v, c = fit(mov, t)
            out[f'{name}_{k}'] = dict(corr=c, iou_raw=round(raw, 4), iou=round(v, 4))
            print(f'{name:8s} {k:5s}  raw IoU {raw:.4f} -> {v:.4f} after s {c[0]:.4f} dx {c[1]:+.0f} dy {c[2]:+.0f}',
                  flush=True)
    with open(FIT_JSON, 'w') as f:
        json.dump(out, f, indent=1)
    print('->', FIT_JSON)
    return out


def xfade_n(v):
    if v >= 0.97:
        return 0
    if v >= 0.95:
        return 2
    if v >= 0.90:
        return 3
    return 4


# ------------------------------------------------------------------------------------------------ the timeline
def t_closeness(f, n):
    """RETURN: sharp (1) while the gavel is still at the lens, softening to 0 as it lowers (as court_gen's S 213-245)."""
    h0, h1 = T_CL
    return float(np.clip(1 - (f - h0) / (h1 - h0), 0, 1))


T_CL = (22, 34)   # RETURN (b3d7a16d): gavel face-on at the lens to ~f22, swung up and away by ~f32, down at his side by ~f56
KNOCKS = cg.KNOCKS
LENGTH = cg.LENGTH
FIRST = cg.FIRST


class Line:
    """Per output frame: dict(src, f, size, impact, mix=(src, f, w) or None). src None = black."""

    def __init__(self, n, NT, NU, joins, rng):
        self.n, self.NT, self.NU, self.joins, self.rng = n, NT, NU, joins, rng
        self.seq = []

    def add(self, src, frames, size):
        for f in frames:
            self.seq.append(dict(src=src, f=f, size=size, impact=False, mix=None))

    def idle(self, gap, size, to_end=False):
        if gap <= 0:
            return
        if to_end and gap <= 361:
            segs = [(0, gap)]
        else:
            segs = self.joins.fill(gap, self.rng)
        for a, b in segs:
            self.add('R', range(a, b), size)

    def hit(self, f_from, size_pre, size_post=None):
        """Approved f_from..96 (size_post from the impact on), then f96 held 24 frames (as shipped)."""
        size_post = size_post or size_pre
        self.add('A', range(f_from, IMPACT_A), size_pre)
        self.add('A', range(IMPACT_A, 97), size_post)
        self.add('A', [96] * 24, size_post)
        return size_post

    def ret(self, size):
        self.add('T', range(self.NT), size)

    def raise_(self, size):
        self.add('U', range(self.NU), size)


def timeline(beat, NT, NU, R, seed=1820):
    n = LENGTH[beat]
    rng = np.random.default_rng(seed)
    L = Line(n, NT, NU, cg.Joins(R), rng)
    knocks = KNOCKS[beat]
    size = FIRST[beat]
    # 1st strike: the beat opens on contiguous approved frames, impact on the knock
    imp0 = knocks[0][0]
    size = L.hit(IMPACT_A - imp0, size, knocks[0][1])
    L.ret(size)
    for imp, q in knocks[1:]:
        u0 = imp - (IMPACT_A - 40) - NU                    # the RAISE ends on the frame before approved f40
        L.idle(u0 - len(L.seq), size)
        assert len(L.seq) == u0, (beat, len(L.seq), u0)
        L.raise_(size)
        if q == 'Q5':                                       # the capper (render_court): f47-59 at Q5, f96 x36, black
            L.add('A', range(40, 47), size)
            L.add('A', range(47, 60), 'Q5')
            L.add('A', [96] * 36, 'Q5')
            L.seq += [dict(src=None, f=None, size=None, impact=False, mix=None) for _ in range(n - len(L.seq))]
            break
        size = L.hit(40, size, q)
        L.ret(size)
    else:
        L.idle(n - len(L.seq), size, to_end=True)
    seq = L.seq[:n]
    assert len(seq) == n, (beat, len(seq))
    for imp, _ in knocks:
        assert seq[imp]['src'] == 'A' and seq[imp]['f'] == IMPACT_A, (beat, imp, seq[imp])
        seq[imp]['impact'] = True
    return seq


def joins_of(seq):
    """[(out index of the first frame of the next run, prev src, next src)] for every change of source."""
    out = []
    for i in range(1, len(seq)):
        p, q = seq[i - 1]['src'], seq[i]['src']
        if p and q and p != q:
            out.append((i, p, q))
    return out


def add_xfades(seq, fitd):
    """Crossfade masks on the bridge side where the corrected IoU < 0.97. Returns [(join index, kind, IoU, n)]."""
    rep = []
    for j, p, q in joins_of(seq):
        size = seq[j]['size'] if q != 'A' else seq[j - 1]['size']
        k = kind(size)
        if (p, q) == ('A', 'T'):
            v = fitd[f'T_start_{k}']['iou']
            n = xfade_n(v)
            for i in range(n):              # first n RETURN frames, mixed with approved f96 (held) fading out
                seq[j + i]['mix'] = ('A', 96, 1 - (i + 1) / (n + 1))
        elif (p, q) == ('T', 'R'):
            v = fitd['T_end_rest']['iou']
            n = xfade_n(v)
            for i in range(n):              # first n idle frames, mixed with RETURN's last frame
                seq[j + i]['mix'] = ('T', seq[j - 1]['f'], 1 - (i + 1) / (n + 1))
        elif (p, q) == ('R', 'U'):
            v = fitd['U_start_rest']['iou']
            n = xfade_n(v)
            for i in range(n):              # first n RAISE frames, mixed with the idle's last frame
                seq[j + i]['mix'] = ('R', seq[j - 1]['f'], 1 - (i + 1) / (n + 1))
        elif (p, q) == ('U', 'A'):
            v = fitd[f'U_end_{k}']['iou']
            n = xfade_n(v)
            for i in range(n):              # last n RAISE frames, mixed with approved f(40-n)..f39 fading in
                o = j - n + i
                seq[o]['mix'] = ('A', 40 - n + i, (i + 1) / (n + 1))
        else:
            continue
        rep.append((j, f'{p}->{q}', size, v, n))
    return rep


def describe(seq):
    runs = []
    for i, s in enumerate(seq):
        r = runs[-1] if runs else None
        if r and r['src'] == s['src'] and (s['src'] is None or s['f'] in (r['f1'], r['f1'] + 1)):
            r['f1'], r['o1'] = s['f'], i
            if s['size'] not in r['q']:
                r['q'].append(s['size'])
        else:
            runs.append(dict(src=s['src'], f0=s['f'], f1=s['f'], o0=i, o1=i, q=[s['size']]))
    return runs


# ------------------------------------------------------------------------------------------------ the frames
class Scene(cg.GenScene):
    def __init__(self, fitd):
        for q in ('Q1', 'Q2', 'Q3'):
            rc.SIZES[q] = V2[q]          # the approved look's sizes, as court_behind_paper.Scene sets them
        from render_court_v2 import field_static
        from court_burn import BurnEdges
        from court_behind_paper import fibre
        self.base, self.lamp, self.plain, self.far, self.near = field_static(layers=True)
        self.burn = BurnEdges(OW, OH)
        self.fib = fibre()
        self.src = rc.load_source()
        self.gbox = rc.gavel_box(self.src[rc.HELD])
        self.takes = {k: cg.load_take(take_path(k)) for k in 'RTU'}
        self.fitd = fitd
        self.cache = {}

    def corr(self, src, f, size):
        k = kind(size)
        d = self.fitd
        if src == 'T':
            a, b = tuple(d[f'T_start_{k}']['corr']), tuple(d['T_end_rest']['corr'])
            w = f / (len(self.takes['T']) - 1)
        else:
            a, b = tuple(d[f'U_end_{k}']['corr']), tuple(d['U_start_rest']['corr'])
            w = 1 - f / (len(self.takes['U']) - 1)
        w = w * w * (3 - 2 * w)                                   # smoothstep: no sudden drift at either end
        return tuple(float(x * (1 - w) + y * w) for x, y in zip(a, b))

    def mask(self, src, f, size):
        key = (src, f, size)
        if key not in self.cache:
            if len(self.cache) > 10:
                self.cache.clear()
            if src == 'A':
                m = rc.place(self.src[f], size, self.gbox)
            elif src == 'R':
                m = cg.place(cg.prep(self.takes['R'][f]), size)
            else:
                m = cg.place(apply_corr(cg.prep(self.takes[src][f]), self.corr(src, f, size)), size)
            self.cache[key] = m
        return self.cache[key]

    def cl(self, src, f, size):
        if size == 'Q5':
            return 1.0
        if src == 'A':
            return a_closeness(f)
        if src == 'T':
            return t_closeness(f, len(self.takes['T']))
        return 0.0


def load_fit():
    with open(FIT_JSON) as f:
        return json.load(f)


def build_seq(beat, sc=None):
    fitd = load_fit()
    R = sc.takes['R'] if sc else cg.load_take(take_path('R'))
    seq = timeline(beat, fitd['frames']['T'], fitd['frames']['U'], R)
    rep = add_xfades(seq, fitd)
    return seq, rep


def frames(beat, clean=False):
    sc = Scene(load_fit())
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
        if s['mix']:
            ms, mf, w = s['mix']
            m = m * (1 - w) + sc.mask(ms, mf, s['size']) * w
            cl = cl * (1 - w) + sc.cl(ms, mf, s['size']) * w
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
    seq, rep = build_seq(beat)
    print(f'beat {beat}: {len(seq)} frames')
    for r in describe(seq):
        print(f"  out {r['o0']:5d}-{r['o1']:5d} ({r['o0'] / FPS:6.2f} s)  {r['src']} f{r['f0']}-{r['f1']}  {r['q']}")
    for j, k, size, v, n in rep:
        print(f'  join out {j:5d} {k} {size}: IoU {v:.4f} -> crossfade {n} f')
    print('  impacts at out', [i for i, s in enumerate(seq) if s['impact']])
    return seq, rep


# ------------------------------------------------------------------------------------------------ contact sheets
def read_frames(video, idxs, w=360):
    idxs = sorted(set(i for i in idxs if i >= 0))
    p = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0',
                        '-select_streams', 'v:0', video], capture_output=True, text=True).stdout.split(',')
    vw, vh = int(p[0]), int(p[1])
    h = int(round(vh * w / vw))
    raw = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-vf', f'scale={w}:{h}:flags=area', '-f', 'rawvideo',
                            '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    out, i, want = {}, 0, set(idxs)
    last = max(idxs)
    while i <= last:
        b = raw.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        if i in want:
            out[i] = np.frombuffer(b, np.uint8).reshape(h, w, 3).copy()
        i += 1
    raw.kill()
    return out, (w, h)


def sheet(rows, fr, wh, path, title):
    w, h = wh
    lab = 24
    cols = max(len(r[1]) for r in rows)
    img = np.full((40 + len(rows) * (h + lab + 8), 150 + cols * (w + 4), 3), 30, np.uint8)
    cv2.putText(img, title, (8, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (230, 230, 230), 1, cv2.LINE_AA)
    for r, (name, idxs, labels) in enumerate(rows):
        y = 40 + r * (h + lab + 8)
        cv2.putText(img, name, (6, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (230, 230, 120), 1, cv2.LINE_AA)
        for c, (i, lb) in enumerate(zip(idxs, labels)):
            x = 150 + c * (w + 4)
            if i in fr:
                img[y:y + h, x:x + w] = fr[i]
            cv2.putText(img, lb, (x + 2, y + h + 17), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1, cv2.LINE_AA)
    cv2.imwrite(path, img)
    print('sheet ->', path)


def sheets(video, beat, prefix):
    seq, rep = build_seq(beat)
    jrows = []
    for j, k, size, v, n in rep:
        idx = list(range(j - 3, j + 4))
        jrows.append((f'{k} {size} {v:.3f} x{n}', idx,
                      [f'{i} {seq[i]["src"]}{seq[i]["f"]}{"*" if seq[i]["mix"] else ""}' for i in idx]))
    for j in range(1, len(seq)):  # idle-internal cuts (rest-to-rest DP segments), not in rep
        a_, b_ = seq[j - 1], seq[j]
        if a_['src'] == b_['src'] == 'R' and b_['f'] != a_['f'] + 1:
            idx = list(range(j - 3, j + 4))
            jrows.append((f'R cut f{a_["f"]}->f{b_["f"]}', idx,
                          [f'{i} {seq[i]["src"]}{seq[i]["f"]}' for i in idx]))
    srows = []
    for imp, q in KNOCKS[beat]:
        idx = list(range(imp - 6, imp + 7))
        srows.append((f'impact @{imp} {q}', idx, [f'{i - imp:+d} A{seq[i]["f"]}' for i in idx]))
    n = len(seq)
    ov = list(range(0, n, max(1, n // 48)))[:48]
    orows = [(f'{ov[r * 12] / FPS:.1f}s', ov[r * 12:(r + 1) * 12],
              [f'{i} {seq[i]["src"]}{seq[i]["f"]}' for i in ov[r * 12:(r + 1) * 12]]) for r in range(len(ov) // 12)]
    allidx = [i for _, ix, _ in jrows + srows + orows for i in ix]
    fr, wh = read_frames(video, allidx, 240 if jrows and len(jrows) > 6 else 300)
    sheet(jrows, fr, wh, prefix + '_joins.png', f'{os.path.basename(video)}  joins -3..+3 (* = crossfade frame)')
    sheet(srows, fr, wh, prefix + '_strikes.png', f'{os.path.basename(video)}  impacts -6..+6 (Darren knock = 0)')
    fr2, wh2 = read_frames(video, [i for _, ix, _ in orows for i in ix], 200)
    sheet(orows, fr2, wh2, prefix + '_overview.png', f'{os.path.basename(video)}  whole run')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['fit', 'plan', 'render', 'sheets'])
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--clean', action='store_true')
    ap.add_argument('--prefix')
    a = ap.parse_args()
    if a.cmd == 'fit':
        measure()
    elif a.cmd == 'plan':
        plan(a.beat)
    elif a.cmd == 'render':
        render(a.out, a.beat, a.clean)
    else:
        sheets(a.out, a.beat, a.prefix)
