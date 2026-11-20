"""Scene 9 court beats, FLOW judge (M9v, 2026-11-20): Homie's notes on the LEAN review, fixed by script. REVIEW only, 0 cr.

NEW FILE: court_gen_lean / court_gen_approved / court_gen / render_court are imported, never changed, so the LEAN, the
approved-strike review and the shipped beats stay bit-identical. Notes: docs/HANDOFF-2026-11-20-M9t.md (verbatim),
causes: docs/S9-JUDGE-M9u-DIAGNOSIS.md, plan + measurements: docs/HANDOFF-2026-11-20-M9v.md.

WHAT CHANGES AGAINST LEAN (the approved strike's FRAMES stay untouched, never warped):
  1 ONE SIZE PER FILE: b3 Q1, b5cut Q2, b7 Q4 (M9x, Homie: keep the torso framing at the end; was Q3 in M9v/w).
    No Q3 jump at slam 3, no Q5 capper cut: the capper plays
    approved f40-95 at Q4 and goes black on the same frame as before.
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
import json
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
SIZE = {3: 'Q1', '5cut': 'Q2', 7: 'Q4'}   # M9x (Homie): b7 keeps the torso framing (Q4), whole file
CL_GEN = 0.9
EASE_A = 20          # joins with an approved frame
EASE_I = 30          # joins inside the idle
EASE_UA = 30         # WIDE: v9 RAISE end -> approved f40 (static v9 tail, so nothing freezes)
DAMP = 0.5
NECK = (470, 570)    # gen source rows (1080x1920): damping weight 0 above NECK[0], DAMP below NECK[1]
PAD = 360            # source px of canvas added on each side for the mirrored edges
CLEAN_SIGMA = 1.8
CAP_K = 0.5          # round-cap depth / run width at a clipped edge (M9w)

# ------------------------------------------------------------------------------------------------ M9y: 16:9 takes
# v8 READ SILENT (replaces R6 v6) and v9 RAISE WIDE (replaces U v5) are 1280x720. They are NOT forced through the
# 9:16 source frame: each frame is upscaled x1.5 (1920x1080) and mapped straight onto the wall by one matrix,
# wall = place . corr . MAP, where MAP (fit16) puts the 16:9 rest pose on the v6 rest pose in the old 1080x1920 source
# grid, so FEET_Y / K / the Q sizes / NECK all keep working. Nothing is clipped: the wide frame covers the wall.
# `--legacy` renders the M9x FLOW (v6 + v5) as before.
WIDE = True
W16, H16 = 1280, 720
FIT16_JSON = os.path.join(cg.GEN, '_fit_16x9_v8v9.json')
LIFT16 = {'L1': 68, 'L2': 214}   # v8 head turns to the front (court) start f68 / f214, back by f136 / f281
RAISE_V5 = False                 # M10a: v9 never reaches approved f40 (best IoU 0.71); --raise-v5 = v5 RAISE (0.98 both ends)
DAMP16 = False                   # M10a: the damping flow-warp lumps v8's scroll at Q4 (Homie 4:57); v8 frames play raw
BLOB_FRAC = 0.004                # black pieces smaller than this x the largest are dropped (scroll blobs, M9x)


def take16_path(tag):
    import glob
    pat = {'R6': 'S9-CRT-IDLE_v8_read_*.mp4', 'U': 'S9-CRT-IDLE_v9_raise_*.mp4'}[tag]
    p = sorted(glob.glob(os.path.join(cg.GEN, pat)))
    assert len(p) == 1, (tag, p)
    return p[0]


def load16(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H16, W16)


def prep16(g720, blur=True):
    """1280x720 grey uint8 -> 1920x1080 float 0..1, white specks inside the black filled (as court_gen.prep)."""
    g = cv2.resize(g720.astype(np.float32), (1920, 1080), interpolation=cv2.INTER_CUBIC) / 255.0
    black = (g < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 600 and not (x == 0 or y == 0 or x + w >= 1920 or y + h >= 1080):
            g[lab == i] = 0.0
    return cv2.GaussianBlur(g, (0, 0), CLEAN_SIGMA) if blur else g


def m3(M):
    return np.vstack([np.asarray(M, np.float64), [0, 0, 1]])


def map16(fit16):
    s, tx, ty = fit16['map']
    return np.float64([[s, 0, tx], [0, s, ty], [0, 0, 1]])


def to_src(g16, fit16):
    """A prepped 16:9 frame in the old 1080x1920 source grid (for fitting / measuring only)."""
    return cv2.warpAffine(g16, map16(fit16)[:2].astype(np.float32), (SW, SH), flags=cv2.INTER_CUBIC, borderValue=1.0)


def place16(g16, sz, corr, fit16):
    s = sz['s']
    if sz['floor']:
        P = [[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * cg.FEET_Y]]
    else:
        P = [[s, 0, OW / 2 - s * sz['cx']], [0, s, OH / 2 - s * sz['cy']]]
    M = m3(P) @ m3(ga.corr_matrix(corr)) @ map16(fit16)
    grey = cv2.warpAffine(g16, M[:2].astype(np.float32), (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)


def drop_blobs(m):
    """Drop loose black pieces (under BLOB_FRAC x the largest piece) from a wall mask (1 = field), with their soft rim,
    never touching pixels within 2 px of a kept piece."""
    black = (m < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(black, 8)
    if n <= 2:
        return m
    areas = st[1:, 4]
    small = [i + 1 for i, a in enumerate(areas) if a < BLOB_FRAC * areas.max()]
    if not small:
        return m
    rem = np.isin(lab, small).astype(np.uint8)
    keep = black & (1 - rem)
    near_r = cv2.dilate(rem, np.ones((7, 7), np.uint8)) > 0
    near_k = cv2.dilate(keep, np.ones((5, 5), np.uint8)) > 0
    m = m.copy()
    m[near_r & ~near_k] = 1.0
    return m


def _fit_map(mov, tgt):
    """(s, tx, ty) putting 16:9 prepped `mov` (1080x1920 hxw) on source-grid `tgt` (1920x1080 hxw), IoU of black."""
    def box(b):
        ys, xs = np.nonzero(b)
        return xs.mean(), ys.min(), ys.max()
    mx, my0, my1 = box(mov < 0.5)
    tx_, ty0, ty1 = box(tgt < 0.5)
    s0 = (ty1 - ty0) / (my1 - my0)
    best = (-1, None)
    t = tgt < 0.5
    q = 0.25
    tq = cv2.resize(tgt, None, fx=q, fy=q, interpolation=cv2.INTER_AREA) < 0.5
    mq = cv2.resize(mov, None, fx=q, fy=q, interpolation=cv2.INTER_AREA)
    for s in np.arange(s0 * 0.97, s0 * 1.0301, 0.002):
        bx, by = tx_ - s * mx, ty1 - s * my1
        for dx in range(-24, 25, 3):
            for dy in range(-24, 25, 3):
                M = np.float32([[s, 0, (bx + dx) * q], [0, s, (by + dy) * q]])
                w = cv2.warpAffine(mq, M, (tq.shape[1], tq.shape[0]), flags=cv2.INTER_LINEAR, borderValue=1.0) < 0.5
                v = ga.iou(w, tq)
                if v > best[0]:
                    best = (v, (float(s), float(bx + dx), float(by + dy)))
    s1, x1, y1 = best[1]
    best = (-1, None)
    for s in np.arange(s1 - 0.003, s1 + 0.00301, 0.0005):
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                c = (round(float(s), 5), x1 + dx, y1 + dy)
                M = np.float32([[c[0], 0, c[1]], [0, c[0], c[2]]])
                v = ga.iou(cv2.warpAffine(mov, M, (SW, SH), flags=cv2.INTER_CUBIC, borderValue=1.0) < 0.5, t)
                if v > best[0]:
                    best = (v, c)
    return best


def fit16():
    """MAP: v8 f0 onto v6 f0 (the rest every old fit used). U corrections for v9 as court_gen_approved.measure."""
    R6 = cg.load_take(gl.take_path('R6'))
    r0 = cg.prep(R6[0])
    v8, v9 = load16(take16_path('R6')), load16(take16_path('U'))
    v, c = _fit_map(prep16(v8[0], False), r0)
    print(f'MAP v8 f0 -> v6 f0: s {c[0]:.5f} tx {c[1]:.1f} ty {c[2]:.1f}  IoU {v:.4f}', flush=True)
    out = {'files': {'R6': os.path.basename(take16_path('R6')), 'U': os.path.basename(take16_path('U'))},
           'map': list(c), 'map_iou': round(v, 4), 'frames': {'U': len(v9), 'R6': len(v8)}}
    v9f0 = prep16(v9[0], False)
    v_, c_ = _fit_map(v9f0, r0)
    print(f'(check) v9 f0 own map: s {c_[0]:.5f} tx {c_[1]:.1f} ty {c_[2]:.1f} IoU {v_:.4f}', flush=True)
    src = rc.load_source()
    ends = {'U_start': (to_src(v9f0, out), {'rest': r0}),
            'U_end': (to_src(prep16(v9[-1], False), out), {k: ga.a_to_gen(src[40], k) for k in ('floor', 'Q4')})}
    for name, (mov, tg) in ends.items():
        for k, t in tg.items():
            raw = ga.iou(mov < 0.5, t < 0.5)
            v, c = ga.fit(mov, t)
            out[f'{name}_{k}'] = dict(corr=c, iou_raw=round(raw, 4), iou=round(v, 4))
            print(f'{name:8s} {k:5s}  raw IoU {raw:.4f} -> {v:.4f} after s {c[0]:.4f} dx {c[1]:+.0f} dy {c[2]:+.0f}',
                  flush=True)
    with open(FIT16_JSON, 'w') as f:
        json.dump(out, f, indent=1)
    print('->', FIT16_JSON)


def load_fit16():
    with open(FIT16_JSON) as f:
        return json.load(f)


def smooth(x):
    x = float(np.clip(x, 0, 1))
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------------------------------------ clipped edges
def _touch(b, side):
    return {'T': b[0], 'L': b[:, 0], 'R': b[:, -1]}[side]


def _runs(e, gap=12):
    """Split sorted edge indices into runs (separate shapes touching the same edge)."""
    cut = np.nonzero(np.diff(e) > gap)[0]
    return np.split(e, cut + 1)


def extend(g):
    """Pad grey g (1 = field) by PAD on every side; where black touches the top / left / right edge, close the shape
    OUTSIDE the frame with the visible strip mirrored outward, trimmed by a ROUND CAP (a half-ellipse across the run,
    depth about half the run width). M9w: the plain mirror (M9v) made a straight-ended bar of the paper (A f42-48), so
    every run now ends rounded, like the paper's rolled end. Depth = until the black run is under 35 % of its edge
    width, never more than CAP_K x the run width."""
    H, W = g.shape
    out = np.ones((H + 2 * PAD, W + 2 * PAD), np.float32)
    out[PAD:PAD + H, PAD:PAD + W] = g
    b = g < 0.5
    for side in ('T', 'L', 'R'):
        e_all = np.nonzero(_touch(b, side))[0]
        for e in _runs(e_all):
            if len(e) < 3:
                continue
            c0, c1 = max(int(e[0]) - 24, 0), int(e[-1]) + 25
            # work in a "top" frame: rows = depth from the edge (row 0 = the edge row), cols = along the edge
            if side == 'T':
                strip = g[:PAD, c0:c1]
            elif side == 'L':
                strip = g[c0:c1, :PAD].T
            else:
                strip = g[c0:c1, ::-1][:, :PAD].T
            run = int(e[-1]) - int(e[0]) + 1
            w0 = (strip[0] < 0.5).sum()
            wd = (strip < 0.5).sum(1)
            under = np.nonzero(wd < 0.35 * w0)[0]
            D = int(under[0]) if len(under) else PAD
            dcap = max(6.0, CAP_K * run)
            D = int(min(D, PAD, 260, np.ceil(dcap)))
            u = np.arange(c0, c0 + strip.shape[1], dtype=np.float32)[None, :]
            r = np.arange(D, dtype=np.float32)[:, None] + 0.5
            m, a = (e[0] + e[-1]) / 2.0, run / 2.0 + 2.0
            q = ((u - m) / a) ** 2 + (r / dcap) ** 2
            cap = np.clip((1.0 - q) * min(a, dcap) / 1.5, 0, 1)      # ~1.5 px soft rim
            ef = 1.0 - (1.0 - strip[:D]) * cap                       # edge-first, capped mirror
            if side == 'T':
                reg = out[PAD - D:PAD, PAD + c0:PAD + c1]
                out[PAD - D:PAD, PAD + c0:PAD + c1] = np.minimum(reg, ef[::-1][:, :reg.shape[1]])
            elif side == 'L':
                reg = out[PAD + c0:PAD + c1, PAD - D:PAD]
                out[PAD + c0:PAD + c1, PAD - D:PAD] = np.minimum(reg, ef[::-1].T[:reg.shape[0]])
            else:
                reg = out[PAD + c0:PAD + c1, PAD + W:PAD + W + D]
                out[PAD + c0:PAD + c1, PAD + W:PAD + W + D] = np.minimum(reg, ef.T[:reg.shape[0]])
    return out


def touches(g):
    b = g < 0.5
    return any(_touch(b, s).sum() >= 3 for s in 'TLR')


def place_floor(g, sz, feet, padded):
    """rc.place / cg.place maths for a size dict (floor sizes, or Q4 by its cx/cy), optionally PAD-padded."""
    s = sz['s']
    if sz['floor']:
        M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * feet]])
    else:
        M = np.float32([[s, 0, OW / 2 - s * sz['cx']], [0, s, OH / 2 - s * sz['cy']]])
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
        if WIDE and not RAISE_V5 and (p['src'], q['src']) == ('U', 'A'):
            E = EASE_UA                             # the v9 -> f40 distance-field morph needs room (join_warp)
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


def merged_fit():
    """The approved-strike fit; in WIDE mode its U entries come from the 16:9 fit (v9)."""
    fitd = ga.load_fit()
    if WIDE:
        f16 = load_fit16()
        fitd = dict(fitd)
        if not RAISE_V5:
            fitd['frames'] = dict(fitd['frames'], U=f16['frames']['U'])
            for k in ('U_start_rest', 'U_end_floor', 'U_end_Q4'):
                fitd[k] = f16[k]
        else:
            fitd['frames'] = dict(fitd['frames'])
        fitd['_16'] = f16
    return fitd


class Scene(gl.Scene):
    def __init__(self, fitd):
        super().__init__(fitd)
        self.rest = {}
        self.wmaps = {}
        if WIDE:
            self.f16 = fitd['_16']
            for k in (('R6',) if RAISE_V5 else ('R6', 'U')):
                self.takes[k] = load16(take16_path(k))

    def wmap(self, size):
        if size not in self.wmaps:
            sz = cg.SIZES[size]
            s = sz['s']
            top = OH - s * cg.FEET_Y if sz['floor'] else OH / 2 - s * sz['cy']
            y_src = (np.arange(OH, dtype=np.float32) - top) / s
            w = np.array([DAMP * smooth((y - NECK[0]) / (NECK[1] - NECK[0])) for y in y_src], np.float32)
            self.wmaps[size] = np.repeat(w[:, None], OW, 1)
        return self.wmaps[size]

    def raw(self, src, f, size):
        m = self._raw(src, f, size)
        return drop_blobs(m) if WIDE else m

    def _raw(self, src, f, size):
        if src == 'A':
            g = self.src[f]
            pad = touches(g)
            return place_floor(extend(g) if pad else g, rc.SIZES[size], rc.FEET_Y, pad)
        if WIDE and (src == 'R6' or (src == 'U' and not RAISE_V5)):
            corr = ga.Scene.corr(self, src, f, size) if src == 'U' else (1.0, 0.0, 0.0)
            return place16(prep16(self.takes[src][f]), cg.SIZES[size], corr, self.f16)
        g = prep_clean(self.takes[src][f])
        if src in 'TU':
            g = ga.apply_corr(g, ga.Scene.corr(self, src, f, size))
        pad = touches(g)
        return place_floor(extend(g) if pad else g, cg.SIZES[size], cg.FEET_Y, pad)

    def mask(self, src, f, size):
        key = (src, f, size)
        if key not in self.cache:
            if len(self.cache) > 40:
                self.cache.clear()
            m = self.raw(src, f, size).astype(np.float32)
            if src in ('R6', 'R7') and f and not (WIDE and src == 'R6' and not DAMP16):
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
    fitd = merged_fit()
    if WIDE:
        gl.LIFT_ONSET = LIFT16            # v8's head turns (gl.Pieces reads this module global)
        R6 = sc.takes['R6'] if sc else load16(take16_path('R6'))
    else:
        R6 = sc.takes['R6'] if sc else cg.load_take(gl.take_path('R6'))
    n7 = len(sc.takes['R7']) if sc else len(cg.load_take(gl.take_path('R7')))
    return timeline(beat, fitd['frames']['T'], fitd['frames']['U'], gl.Pieces(R6), n7)


def sdf_morph(cur, target, w):
    """Blend two masks (grey, 1 = field) through their signed distance fields: the figure stays one solid shape
    (no flow tearing) while it changes pose. Edge softness ~1.5 px, like the source masks."""
    if w <= 0.001:
        return cur
    def sdf(m):
        fig = (m < 0.5).astype(np.uint8)
        return (cv2.distanceTransform(1 - fig, cv2.DIST_L2, 5) - cv2.distanceTransform(fig, cv2.DIST_L2, 5))
    d = (1 - w) * sdf(cur) + w * sdf(target)        # > 0 = field
    return np.clip(0.5 + d / 3.0, 0, 1).astype(cur.dtype)


def join_warp(src, cur, ws, target, w):
    """WIDE: v9 RAISE ends off approved f40's pose (IoU ~0.67), too far for Farneback (it tears into blotches), and its
    scroll is drawn unlike v8's (Farneback holes the scroll top and leaves specks at READ -> RAISE). So every join that
    touches v9 morphs by distance field; the others keep the flow warp Homie praised. Specks from any warp are dropped."""
    if WIDE and not RAISE_V5 and 'U' in (src, ws):
        return sdf_morph(cur, target, w)
    m = gl.flow_warp(cur, target, w)
    return drop_blobs(m) if WIDE else m


def frames(beat, clean=False):
    sc = Scene(merged_fit())
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
            m = join_warp(s['src'], m, ws, sc.mask(ws, wf, s['size']), w)
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
    ap.add_argument('cmd', choices=['plan', 'render', 'sheets', 'fit16'])
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--clean', action='store_true')
    ap.add_argument('--prefix')
    ap.add_argument('--raise-v5', action='store_true', help='M10a: v8 READ + the v5 RAISE (pose-matched to approved f40)')
    ap.add_argument('--legacy', action='store_true', help='M9x FLOW: v6 READ + v5 RAISE (9:16), no blob drop')
    a = ap.parse_args()
    WIDE = not a.legacy
    RAISE_V5 = a.raise_v5
    if a.cmd == 'fit16':
        fit16()
    elif a.cmd == 'plan':
        plan(a.beat)
    elif a.cmd == 'render':
        render(a.out, a.beat, a.clean)
    else:
        sheets(a.out, a.beat, a.prefix)
