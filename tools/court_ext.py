"""Scene 9 court beats, EXT judge (M10g, 2026-11-21): ONE drawing of the judge end to end. REVIEW only.

Homie (M10g): keep the APPROVED strike exactly as it is (fig_SOTR_judge_strike_s9_v1, the step forward, the gavel in
your face) and build the read before it and the return to reading after it with Seedance's extend. Every piece below
is generated FROM the approved strike's own frames, so it is the same figure, the same drawing, the same framing:

  B  v12-BACK   video_extension backward of the approved strike: reads (f0-58), raises (f59-119), runs INTO approved f0
  A  approved   fig_SOTR_judge_strike_s9_v1 f0-96, untouched (impact f53)
  F  v12-FWD    video_extension forward of the approved strike: runs ON from approved f96, holds, steps back
  R  v13-FWD2   video_extension forward of F (steered by B f0 as @Image 1): settles into B's reading pose and reads

Order: [first knock: A from mid-strike] -> F -> R (reading, looped inside itself) -> B f_y.. (raise) -> A f0-96 -> F -> R ...
Three joins are continuous by construction (extensions). Two are chosen, not made: the loop point inside R's reading
(R[q] ~ R[p]) and the exit from R's reading into B's reading (R[x+1] ~ B[y]), each the most similar frame pair of the
same drawing. Where such a pair is not one natural step apart the outgoing frames are flow-warped onto the incoming
frame over EASE frames (same figure, same pose, a few px; never a morph between different drawings). Idles are fitted
by whole loops plus a uniform retime of at most RATE_MAX (frame interpolation between neighbouring frames), never a cut.

  python tools/court_ext.py measure
  python tools/court_ext.py plan --beat 3|5cut|7 [--full]
  python tools/court_ext.py render OUT.mp4 --beat 3|5cut|7 [--full]
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
import court_gen_lean as gl  # noqa: E402
import court_gen_flow as cf  # noqa: E402
from court_burn import BEAT_T0  # noqa: E402
from court_behind_paper import compose_opaque, closeness as a_closeness  # noqa: E402

OW, OH, FPS = rc.OW, rc.OH, rc.FPS
SW, SH = 1080, 1920
GEN = cg.GEN
IMPACT_A = ga.IMPACT_A                      # 53
SIZE = {3: 'Q1', '5cut': 'Q2', 7: 'Q4'}     # one size per file (M9x)
PAT = {'B': 'S9-CRT-IDLE_v12back_*.mp4', 'F': 'S9-CRT-IDLE_v12fwd_*.mp4', 'R': os.environ.get('EXT_R', 'S9-CRT-IDLE_v13fwd3_*.mp4')}
B_READ = 58                                 # B f0-58 reads, f59 on raises
BP = os.environ.get('EXT_BP')               # optional take that leads into B (B's backward extension)
if BP:
    PAT['BP'] = BP
BP2 = os.environ.get('EXT_BP2')             # optional short lead: backward extension of B from f59 (the raise) -> lead 'C'
if BP2:
    PAT['BP2'] = BP2
BP3 = os.environ.get('EXT_BP3')             # optional F-lead: backward extension of B from f59 whose first frame is F's
if BP3:                                     # settled end -> lead 'D', entered straight from F (no R; b7's tight window)
    PAT['BP3'] = BP3
# M10m (Homie M10l: "Do the order-order lookups"): U = v16-FWD, a forward extension of R from R[LOOK_AT] (head lifts
# on "Order! Order!", a gavel thrust, back into the reading pose). b5 only, behind EXT_LOOKUP (path/glob of U): R's
# stream lands exactly on R[LOOK_AT] at out LOOK_OUT (xw 0, no ease), U plays at rate 1, then exits into R or a lead.
LOOKUP = os.environ.get('EXT_LOOKUP')
if LOOKUP:
    PAT['U'] = LOOKUP
LOOK_AT, LOOK_OUT = 147, 858
LOOK_Z0 = 144                               # U from here on is the held reading pose (exit search window)
READ_FROM = int(os.environ.get('EXT_READ_FROM', 60))   # R frames from here on are settled reading (from the take's sheet)
REFRAME = int(os.environ.get('EXT_REFRAME', 96))   # frames over which R's framing eases onto B's before a raise
LOOP_MIN = 72                               # shortest loop inside R's reading (3 s)
EASE = 8                                    # frames of flow-warp ease where neighbours are not one step apart
DUP_IOU = 0.997                             # at or above: the second frame repeats the first (dropped, no hold)
HOLD_IOU, HOLD_MOVE = 0.9985, 0.996            # a generated frame this close to the last while the frames around it move = a hold
SNAP_IOU = 0.985                            # below: not one natural 24 fps step apart -> ease (one step is ~0.99)
RATE_MAX = 0.12                             # idle retime limit (+-12 %)
RATE_MAX_B7 = 0.16                          # b7: barely room to read between its two knocks
# M10i (Homie M10g: "the script just floats in the air while he moves his hand around"): in each read lead the grip
# change (paper from the top grip to the side grip) is drawn slowly, the paper drifting while the hand barely moves.
# The span is played FASTER inside its own take: whole frames only, a smooth speed ramp 1x -> RAMP_K x -> 1x (ease in,
# ease out, like a real hand move), no interpolation, no morph. The frames saved go back to the reading before it.
# Spans in the lead's own indices after the hold-frame drop (measured M10i on the paper/hand crop, every frame eyed).
GRIP = {'C': (16, 79), 'B': (31, 99), 'D': (21, 79)}
RAMP_K = float(os.environ.get('EXT_RAMP_K', 3.0))
RAMP_MODE = os.environ.get('EXT_RAMP_MODE', 'motion')   # M10j: 'motion' (matched) | 'bump' (M10i sin^2)
WRAP_E = 24                                 # loop wrap: the last WRAP_E frames before R[q] ease onto R[p-WRAP_E..p-1]
# M10o (Darren 22 Nov, docs/HANDOFF-2026-11-22-S9darren.md), behind EXT_D22=1 (EXT3 rebuilds unchanged without it):
# b5's last strike 1278 -> 1374 (= 247.0 s, after his last "Order!" which ends 246.22 s); his snip 248.0-290.0 s
# (= b5 out SNIP) is black here and cut in the review; the strike plays through across it (A54.. in the kept frames,
# no jump to a reading frame); b7's Q5 capper ends ON the impact frame (A f0-53), black from the next frame.
D22 = os.environ.get('EXT_D22') == '1'
D22_STRIKE = 1374
SNIP = (1398, 2406)                         # b5 out frames of mix 248.0 s and 290.0 s (b5 starts 189.75 s)
# M10p (Homie on EXT4, 22 Nov: "match the Gavel hit with the sound because we are following the sound here"; b7: "make
# that fade a little bit after the gavel has been hit so that the impact stays ... quite a bit of echo"), behind
# EXT_E5=1 (EXT3 and EXT4 rebuild unchanged without it; never with EXT_D22). b5: the last strike stays ON his gavel
# sound (KNOCKS 1278 -> 1279 with the +1 below = 243.04 s; his transient 243.03 s, ncc 0.60; b7 knock -> 389), and the line is
# built as if the snip were not there (the EXT3 path at 2424 - 1008 frames), so the judge plays straight through the
# splice; black is put back over SNIP (cut in the review). b7: the Q5 capper plays A f0-95 (hit + follow-through),
# then F/R carry on, and the picture fades to black over his echo: gain 1 at out E5_FADE[0] (339.58 s) to 0 at
# E5_FADE[1] (342.0 s, his echo at -39 dB just before his next sound at 342.1 s), smoothstep; black after.
E5 = os.environ.get('EXT_E5') == '1'
assert not (E5 and D22), 'EXT_E5 and EXT_D22 are separate builds'
E5_FADE = (400, 458)
CL_GEN = cf.CL_GEN
GEN_SIGMA = 1.0                             # contour clean-up of the x1.5 upscale (approved frames are native 1080)


def take(tag):
    p = sorted(glob.glob(os.path.join(GEN, PAT[tag])))
    if not p:
        raise SystemExit(f'missing take {tag}: {PAT[tag]}')
    return p[-1]


def grip_motion(fr):
    """Per-step motion of the paper/hand crop (mean abs diff, 0-255), cadence-smoothed over 4 frames."""
    c = fr[:, 250:680, 280:660].astype(np.float32)
    m = np.abs(np.diff(c, axis=0)).mean(axis=(1, 2))
    return np.convolve(np.pad(m, 2, mode='edge'), np.ones(4) / 4, mode='same')[2:-2]


def ramp_play(n, s, e, k, motion=None, edge=8):
    """Indices 0..n-1 with span s..e played faster, whole frames, strictly increasing, s and e kept.
    M10j (Homie: "nice and clean, not fake"): with `motion` the speed is MOTION-MATCHED, not a fixed bump: frames where
    the paper only drifts (little motion) play up to k x, frames where the hand already moves fast stay at 1x, so the
    played span moves evenly like one real hand move instead of whipping the fast part. Speed eases to 1x over `edge`
    frames at both ends and is smoothed, so it never jumps. Without `motion`: the M10i sin^2 bump 1 -> k -> 1."""
    span = np.arange(s, e + 1)
    if motion is None:
        u = (span - s) / (e - s)
        step = 1 + (k - 1) * np.sin(np.pi * u) ** 2
    else:
        m = np.maximum(motion[s:e + 1], 0.05)
        target = np.percentile(m, 90)                     # the take's own fast-move speed
        step = np.clip(target / m, 1, k)
        step = np.convolve(np.pad(step, 4, mode='edge'), np.ones(9) / 9, mode='same')[4:-4]
        ramp = np.clip(np.minimum(span - s, e - span) / edge, 0, 1)
        step = 1 + (step - 1) * (3 * ramp ** 2 - 2 * ramp ** 3)
    idx, t = [], float(s)
    while t < e:
        i = int(round(t))
        if not idx or i > idx[-1]:
            idx.append(i)
        t += float(np.interp(t, span, step))
    if idx[-1] != e:
        idx.append(e)
    return list(range(s)) + idx + list(range(e + 1, n))


def load_gen(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, 1280, 720)


def prep_gen(g720):
    """720x1280 generated frame -> 1080x1920 grey 0..1 in the approved strike's own grid (extensions are its framing x2/3).
    Small white specks enclosed by black are filled (as rc.load_source does for the approved frames)."""
    g = cv2.resize(g720.astype(np.float32), (SW, SH), interpolation=cv2.INTER_CUBIC) / 255.0
    black = (g < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < 600 and not (x == 0 or y == 0 or x + w >= SW or y + h >= SH):
            g[lab == i] = 0.0
    return cv2.GaussianBlur(g, (0, 0), GEN_SIGMA)


# ------------------------------------------------------------------------------------------------ scene
class Scene(gl.Scene):
    def __init__(self):                                   # gl.Scene minus the old takes
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
        self.gen = {k: load_gen(take(k)) for k in PAT if k not in ('BP', 'BP2', 'BP3')}
        self.bp_join = {}
        self.read_max = {'B': B_READ}                     # per lead: last frame an exit may land on
        b = self.gen['B']

        def lead(tag, after):                             # backward extension + the B frames it was extended from
            bp = load_gen(take(tag))
            gs = [prep_gen(fr) for fr in bp]              # drop generator HOLD frames: a frame that repeats its
            st = [iou_grey(gs[k], gs[k + 1]) for k in range(len(gs) - 1)]   # predecessor mid-motion (a stutter)
            hold = [k + 1 for k in range(1, len(st) - 1)
                    if st[k] >= HOLD_IOU and st[k - 1] < HOLD_MOVE and st[k + 1] < HOLD_MOVE]
            if hold:
                print(f'{tag}: dropped hold frames {hold}')
                bp = np.delete(bp, hold, axis=0)
            v = iou_grey(prep_gen(bp[-1]), prep_gen(after[0]))
            if v >= DUP_IOU:
                bp = bp[:-1]
                v = iou_grey(prep_gen(bp[-1]), prep_gen(after[0]))
            return np.concatenate([bp, after]), len(bp), v
        if BP2:
            self.gen['C'], nc, self.bp_join['C'] = lead('BP2', b[B_READ + 1:])
            self.read_max['C'] = nc - 1
        if BP:
            self.gen['B'], nb, self.bp_join['B'] = lead('BP', b)
            self.read_max['B'] = B_READ + nb
        self.leads = sorted(self.read_max)
        self.f_leads = []                                 # leads entered from F, not from R
        if BP3:
            self.gen['D'], nd, self.bp_join['D'] = lead('BP3', b[B_READ + 1:])
            self.read_max['D'] = nd - 1
            self.f_leads = ['D']
        self.slow_end = {}                                # F-leads: last frame of the slow reading before the grip
        self.grip = {}
        for L, (s, e) in GRIP.items():                    # compress the grip change inside each lead's own take
            if L not in self.gen or RAMP_K <= 1:
                continue
            play = ramp_play(len(self.gen[L]), s, e, RAMP_K, None if RAMP_MODE == 'bump' else grip_motion(self.gen[L]))
            self.gen[L] = self.gen[L][play]
            self.read_max[L] = play.index(self.read_max[L])
            self.slow_end[L] = s - 1
            self.grip[L] = (s, play.index(e))
            print(f'{L}: grip change f{s}-{e} ({e - s + 1} f) plays on {play.index(e) - s + 1} f '
                  f'({[i for i in play if s <= i <= e]})')
        self.W = {}
        self.cache = {}

    def n(self, tag):
        return len(self.src) if tag == 'A' else len(self.gen[tag])

    def grey(self, src, f, xw=0.0, xl='B'):
        if src == 'A':
            return self.src[f]
        g = prep_gen(self.gen[src][f])
        return reframe(g, self.W[xl], xw) if (src in ('R', 'F', 'U') and xw > 0) else g

    def raw(self, src, f, size, xw=0.0, xl='B'):
        xw = round(float(xw), 3) if src in ('R', 'F', 'U') else 0.0
        key = (src, f, size, xw, xl if xw else '')
        if key not in self.cache:
            if len(self.cache) > 48:
                self.cache.clear()
            g = self.grey(src, f, xw, xl)
            pad = cf.touches(g)
            m = cf.place_floor(cf.extend(g) if pad else g, rc.SIZES[size], rc.FEET_Y, pad)
            self.cache[key] = cf.drop_blobs(m).astype(np.float32)
        return self.cache[key]

    def mask(self, e, size):
        """e = dict(src, f (float when retimed), snap=(src, f, w) or None)."""
        f = e['f']
        i = int(np.floor(f + 1e-6))
        xw, xl = e.get('xw', 0.0), e.get('xl', 'B')
        m = self.raw(e['src'], i, size, xw, xl)
        if f - i > 1e-3 and i + 1 < self.n(e['src']):
            m = gl.flow_warp(m, self.raw(e['src'], i + 1, size, xw, xl), f - i)
        if e.get('snap'):
            s, sf, w = e['snap']
            m = gl.flow_warp(m, self.raw(s, sf, size, xw, xl), w)
        return cf.drop_blobs(m)

    def cl(self, src, f):
        return max(a_closeness(int(f)), CL_GEN) if src == 'A' else CL_GEN


# ------------------------------------------------------------------------------------------------ joins
def iou_grey(a, b):
    a, b = a < 0.5, b < 0.5
    return float((a & b).sum() / max((a | b).sum(), 1))


def fit_frame(src, dst):
    """Affine W (inverse map, 1080x1920 px) that lays src's figure onto dst's (ECC on the grey frames at half size)."""
    a = cv2.resize(src, (540, 960)).astype(np.float32)
    b = cv2.resize(dst, (540, 960)).astype(np.float32)
    W = np.eye(2, 3, dtype=np.float32)
    _, W = cv2.findTransformECC(b, a, W, cv2.MOTION_AFFINE,
                                (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    W[:, 2] *= 2
    return W


def reframe(g, W, xw):
    """R drifts in framing against B (Seedance extensions each re-frame a little: ~3 % wide, ~1 % tall, a few px).
    xw 0..1 eases R from its own framing onto B's, slowly, over the reading before a raise."""
    Wx = np.eye(2, 3, dtype=np.float32) * (1 - xw) + W * xw
    return cv2.warpAffine(g, Wx, (g.shape[1], g.shape[0]), flags=cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP,
                          borderMode=cv2.BORDER_REPLICATE)


def small(g):
    return cv2.resize(g, (270, 480), interpolation=cv2.INTER_AREA) < 0.5


def iou_b(a, b):
    return float((a & b).sum() / max((a | b).sum(), 1))


class Joins:
    """Measured once: the dup frames to drop at the extension seams, R's loop point and the exits from R into B."""

    def __init__(self, sc):
        g = sc.grey
        nF, nR = sc.n('F'), sc.n('R')
        self.f_start = 1 if iou_grey(g('F', 0), g('A', 96)) >= DUP_IOU else 0
        self.r_start = 1 if iou_grey(g('R', 0), g('F', nF - 1)) >= DUP_IOU else 0
        Rs = [small(g('R', k)) for k in range(nR)]
        best = (-1, 0, 0)                     # loop: play R[p..q-1] then R[p] again -> R[q] must look like R[p]
        for p_ in range(READ_FROM, nR - LOOP_MIN):
            for q_ in range(p_ + LOOP_MIN, nR):
                v = iou_b(Rs[p_], Rs[q_])
                if v > best[0]:
                    best = (v, p_, q_)
        self.loop_iou, self.p, self.q = best
        self.lead = {}
        for L in sc.leads:                        # per lead: R's framing -> the lead's, its exits, its seam into A0
            nL = sc.n(L)
            b_end = nL - 1 if iou_grey(g(L, nL - 1), g('A', 0)) >= DUP_IOU else nL
            fits = []
            for x in range(READ_FROM, nR, 6):
                W = fit_frame(g('R', x), g(L, 0))
                fits.append((iou_grey(reframe(g('R', x), W, 1.0), g(L, 0)), x, W))
            w_iou, w_x, sc.W[L] = max(fits, key=lambda t: t[0])
            Ra = [small(reframe(g('R', k), sc.W[L], 1.0)) for k in range(nR)]
            Ls = [small(g(L, k)) for k in range(sc.read_max[L] + 1)]
            # exits: play R[..x] then L[y..] -> R[x+1] must look like L[y]; every pair, best first
            exits = sorted(((iou_b(Ra[x + 1], Ls[y]), x, y) for x in range(self.r_start, nR - 1)
                            for y in range(sc.read_max[L] + 1)), reverse=True)
            self.lead[L] = dict(b_end=b_end, exits=exits, W=sc.W[L], W_iou=w_iou, W_x=w_x,
                                A0=iou_grey(g(L, b_end - 1), g('A', 0)), into=sc.bp_join.get(L))
        self.flead = {}
        for L in sc.f_leads:                      # F-leads: F's framing -> the lead's, exits F[x] -> L[y]
            nL = sc.n(L)
            b_end = nL - 1 if iou_grey(g(L, nL - 1), g('A', 0)) >= DUP_IOU else nL
            fits = []
            for x in range(nF - 20, nF):
                W = fit_frame(g('F', x), g(L, 0))
                fits.append((iou_grey(reframe(g('F', x), W, 1.0), g(L, 0)), x, W))
            w_iou, w_x, sc.W[L] = max(fits, key=lambda t: t[0])
            Fa = [small(reframe(g('F', k), sc.W[L], 1.0)) for k in range(nF)]
            Ls = [small(g(L, k)) for k in range(sc.read_max[L] + 1)]
            exits = sorted(((iou_b(Fa[x + 1], Ls[y]), x, y) for x in range(nF // 2, nF - 1)
                            for y in range(sc.read_max[L] + 1)), reverse=True)
            self.flead[L] = dict(b_end=b_end, exits=exits, W=sc.W[L], W_iou=w_iou, W_x=w_x,
                                 rm=sc.slow_end.get(L, sc.read_max[L]), slow=L in sc.slow_end,
                                 A0=iou_grey(g(L, b_end - 1), g('A', 0)), into=sc.bp_join.get(L))
        self.nF, self.nR = nF, nR
        self.look = None
        if 'U' in sc.gen:                         # look-up take: seam on R[LOOK_AT], exits U[z] -> R[w] / lead L[y]
            nU = sc.n('U')
            u_start = 1 if iou_grey(g('U', 0), g('R', LOOK_AT)) >= DUP_IOU else 0
            Us = [small(g('U', k)) for k in range(nU)]
            exits = [(iou_b(Us[z + 1], Rs[w]), z, 'R', w) for z in range(LOOK_Z0, nU - 1) for w in range(self.r_start, nR)]
            for L in sc.leads:
                Ua = [small(reframe(g('U', k), sc.W[L], 1.0)) for k in range(LOOK_Z0, nU)]
                Ls = [small(g(L, k)) for k in range(sc.read_max[L] + 1)]
                exits += [(iou_b(Ua[z + 1 - LOOK_Z0], Ls[y]), z, L, y) for z in range(LOOK_Z0, nU - 1)
                          for y in range(sc.read_max[L] + 1)]
            self.look = dict(u_start=u_start, seam=iou_grey(g('R', LOOK_AT), g('U', u_start)),
                             dup=iou_grey(g('U', 0), g('R', LOOK_AT)), exits=sorted(exits, key=lambda t: -t[0]))
        self.seam = dict(A96_F=iou_grey(g('A', 96), g('F', self.f_start)),
                         F_R=iou_grey(g('F', nF - 1), g('R', self.r_start)))

    def report(self):
        print('extension seams IoU:', {k: round(v, 4) for k, v in self.seam.items()},
              f' f_start {self.f_start} r_start {self.r_start}')
        print(f'R loop: R[{self.p}..{self.q - 1}] ({self.q - self.p} f), R[{self.q}] vs R[{self.p}] IoU {self.loop_iou:.4f}')
        for L, d in self.lead.items():
            print(f'lead {L}: b_end {d["b_end"]}, into-B seam {d["into"]}, ->A0 {d["A0"]:.4f}; reframe at R[{d["W_x"]}] '
                  f'(IoU {d["W_iou"]:.4f}) {np.round(d["W"], 4).tolist()}')
            print('   best exits (IoU, x, y):', [(round(v, 4), x, y) for v, x, y in d['exits'][:6]])
        for L, d in self.flead.items():
            print(f'F-lead {L}: b_end {d["b_end"]}, into-B seam {d["into"]}, ->A0 {d["A0"]:.4f}; reframe at F[{d["W_x"]}] '
                  f'(IoU {d["W_iou"]:.4f}) {np.round(d["W"], 4).tolist()}')
            print('   best exits (IoU, x, F->y):', [(round(v, 4), x, y) for v, x, y in d['exits'][:6]])

        if self.look:
            d = self.look
            print(f'look-up U: U0 vs R[{LOOK_AT}] {d["dup"]:.4f} -> u_start {d["u_start"]}, seam R[{LOOK_AT}]->U[{d["u_start"]}] '
                  f'{d["seam"]:.4f}; best exits (IoU, z, ->, w/y):', [(round(v, 4), z, t, w) for v, z, t, w in d['exits'][:8]])

    def stream(self, t):
        """R index at whole stream position t: R[r_start..q-1], then R[p..q-1] again and again."""
        first = self.q - self.r_start
        return self.r_start + t if t < first else self.p + (t - first) % (self.q - self.p)


# ------------------------------------------------------------------------------------------------ timeline
class Line:
    def __init__(self, J):
        self.J = J
        self.seq = []

    def add(self, src, frames):
        for f in frames:
            self.seq.append(dict(src=src, f=f, snap=None, impact=False))

    def snap_into(self, src, f, iou, end=None, floor=0):
        """Warp the EASE frames before position `end` (default: the end so far) onto (src, f), when not one step apart."""
        if iou >= SNAP_IOU:
            return
        end = len(self.seq) if end is None else end
        k = min(EASE, end - floor)
        for j in range(k):
            self.seq[end - k + j]['snap'] = (src, f, cf.smooth((j + 1) / (k + 1)))

    def strike(self, a0, a1=97):
        self.add('A', range(a0, a1))

    def read(self, n, tx=None, t0=0):
        """n frames of R's stream; stream position tx lands on the last frame (uniform retime when tx + 1 != n).
        Fractional frames interpolate R[i] -> R[i+1] (at a wrap R[q-1] -> R[q], and R[q] ~ R[p])."""
        J = self.J
        start = len(self.seq)
        tx = n - 1 if tx is None else tx
        for o in range(n):
            t = t0 + o * (tx - t0) / max(n - 1, 1) if t0 else o * tx / max(n - 1, 1)
            i = int(np.floor(t + 1e-6))
            self.seq.append(dict(src='R', f=J.stream(i) + (t - i), snap=None, impact=False))
        # M10i: R[q] differs from R[p] in the drawing (not the position: an affine fit gains nothing), a small snap
        # at 24 fps. Over the last WRAP_E frames before every wrap, R[q-E+j] eases onto R[p-E+j], the frames of the SAME
        # reading take that lead into R[p] (pairs IoU 0.988-0.994), so the loop reaches R[p] through its own frames.
        for o in range(start, len(self.seq)):
            f = self.seq[o]['f']
            j = f - (J.q - WRAP_E)
            if 0 <= j < WRAP_E and f >= J.p:
                self.seq[o]['snap'] = ('R', int(J.p - WRAP_E + np.floor(j + 1e-6)), cf.smooth((j + 1) / WRAP_E))

    def read_to_raise(self, n, rate_max, t0=0):
        """Fill n frames: R's stream out at an exit R[x] -> L[y] for a lead L (B, or the short lead C), then L to its end
        (the raise, exact into A0). Best-matching exit over all leads that fits with whole loops and the smallest retime.
        Over the last REFRAME reading frames R's framing eases onto the lead's. Returns (lead, iou, x, y, rate)."""
        J = self.J
        best = None
        for L, d in J.lead.items():
            for v, x, y in d['exits']:
                if best and v < best[0] - 0.003:              # sorted: nothing materially better further down
                    break
                nr = n - (d['b_end'] - y)                     # frames for the R part
                if nr < 2:
                    continue
                if J.p <= x < J.q:
                    cands = [x - J.r_start + m * (J.q - J.p) for m in range(60)]
                elif x < J.q:
                    cands = [x - J.r_start]
                else:
                    continue
                for tx in cands:
                    if tx < t0:
                        continue
                    rate = (tx - t0 + 1) / nr
                    if abs(rate - 1) <= rate_max and (best is None or (v, -abs(rate - 1)) > (best[0], -abs(best[6] - 1))):
                        best = (v, L, x, y, tx, nr, rate)
        assert best, f'no exit fits {n} frames'
        v, L, x, y, tx, nr, rate = best
        d = J.lead[L]
        r0 = len(self.seq)
        self.read(nr, tx, t0)
        k = min(REFRAME, nr)                              # ease R's framing onto the lead's over the last k reading frames
        for j in range(k):
            self.seq[r0 + nr - k + j].update(xw=cf.smooth((j + 1) / k), xl=L)
        self.snap_into(L, y, v)
        self.add(L, range(y, d['b_end']))
        self.snap_into('A', 0, d['A0'])
        return L, round(v, 4), x, y, round(rate, 3)

    def f_to_raise(self, m, stretch_max=0.06):
        """Fill m frames straight from the strike: F[f_start..x] then an F-lead L[y..] (the raise, exact into A0).
        Best exit wins; any length gap is taken up by retiming ONLY the lead's slow reading part (same-take frames,
        within stretch_max); the raise plays on whole frames. F's framing eases onto the lead's over F."""
        J = self.J
        best = None
        for L, d in J.flead.items():
            for v, x, y in d['exits']:
                if y > d['rm']:
                    continue
                nread = m - (x + 1 - J.f_start) - (d['b_end'] - d['rm'] - 1)   # output frames for L[y..rm]
                rate = (d['rm'] - y) / max(nread - 1, 1)
                smax = 0.75 if d['slow'] else stretch_max     # M10i: the grip frames saved go to the still reading
                if nread >= 2 and abs(rate - 1) <= smax and (best is None or (v, -abs(rate - 1)) > (best[0], -abs(best[5] - 1))):
                    best = (v, L, x, y, nread, rate)
        if best is None:
            return None
        v, L, x, y, nread, rate = best
        d = J.flead[L]
        f0 = len(self.seq)
        self.add('F', range(J.f_start, x + 1))
        nf = len(self.seq) - f0
        k = min(REFRAME, nf)
        for j in range(k):
            self.seq[f0 + nf - k + j].update(xw=cf.smooth((j + 1) / k), xl=L)
        self.snap_into(L, y, v)
        self.add(L, [y + o * rate for o in range(nread)])
        self.add(L, range(d['rm'] + 1, d['b_end']))
        self.snap_into('A', 0, d['A0'])
        return 'F->' + L, round(v, 4), x, y, round(rate, 3)

    def lookup_to_raise(self, n):
        """Fill n frames (the gap after F) with the look-up: R's stream exactly onto R[LOOK_AT] at out LOOK_OUT, U at
        rate 1, then the best-IoU exit that still fits: into R[w] (then read_to_raise from there) or straight into a
        lead L[y] (y forced by the length; U's framing eases onto the lead's). snap_into where IoU < SNAP_IOU."""
        J, d = self.J, self.J.look
        o0 = len(self.seq)
        end = o0 + n                                      # out frame of A0
        self.read(LOOK_OUT - o0 + 1, LOOK_AT - J.r_start)
        assert self.seq[LOOK_OUT]['f'] == LOOK_AT and not self.seq[LOOK_OUT]['snap'], self.seq[LOOK_OUT]
        for v, z, tgt, w in d['exits']:
            rem = end - (LOOK_OUT + 1) - (z - d['u_start'] + 1)
            trial = Line(J)
            trial.seq = [dict(e) for e in self.seq]
            trial.add('U', range(d['u_start'], z + 1))
            u0 = LOOK_OUT + 1
            if tgt == 'R':
                trial.snap_into('R', w, v)
                try:
                    nxt = trial.read_to_raise(rem, RATE_MAX, t0=w - J.r_start)
                except AssertionError:
                    continue
            else:
                y = J.lead[tgt]['b_end'] - rem
                if y != w:
                    continue
                k = min(REFRAME, z - d['u_start'] + 1)
                for j in range(k):
                    trial.seq[u0 + (z - d['u_start'] + 1) - k + j].update(xw=cf.smooth((j + 1) / k), xl=tgt)
                trial.snap_into(tgt, y, v)
                trial.add(tgt, range(y, J.lead[tgt]['b_end']))
                trial.snap_into('A', 0, J.lead[tgt]['A0'])
                nxt = None
            assert len(trial.seq) == end
            self.seq = trial.seq
            return ('U', round(v, 4), z, tgt, w, nxt)
        raise AssertionError('no look-up exit fits')

    def recover(self):
        J = self.J
        self.add('F', range(J.f_start, J.nF))
        self.snap_into('R', J.r_start, J.seam['F_R'])


def timeline(beat, J, n):
    if E5 and beat == '5cut':                                 # M10p: straight through the snip, black put back over it
        k = SNIP[1] - SNIP[0]
        seq, info = timeline_core(beat, J, n - k)
        blk = [dict(src=None, f=None, snap=None, impact=False) for _ in range(k)]
        return seq[:SNIP[0]] + blk + seq[SNIP[0]:], info
    seq, info = timeline_core(beat, J, n)
    if E5 and beat == 7:                                      # M10p: fade to black over his gavel echo
        f0, f1 = E5_FADE
        for o, s in enumerate(seq):
            if o > f1:
                seq[o] = dict(src=None, f=None, snap=None, impact=False)
            elif o > f0:
                u = (o - f0) / (f1 - f0)
                s['gain'] = 1 - u * u * (3 - 2 * u)
    return seq, info


def timeline_core(beat, J, n):
    knocks = list(ga.KNOCKS[beat])
    if D22 and beat == '5cut':
        knocks[2] = (D22_STRIKE, knocks[2][1])
    if E5:                                                  # M10p audit: A's gavel touches at IMPACT_A - 1, so the knock frame
        k = 2 if beat == '5cut' else (1 if beat == 7 else None)  # goes 1 later: contact lands on his hit (b5 243.0 s vs
        if k is not None:                                   # his 243.03 s; b7 339.083 s vs 339.10 s), sound never before it
            knocks[k] = (knocks[k][0] + 1, knocks[k][1])
    L = Line(J)
    L.strike(IMPACT_A - knocks[0][0])
    info = []
    for kn, (imp, q) in enumerate(knocks[1:]):
        fl = L.f_to_raise(imp - IMPACT_A - len(L.seq)) if (beat == 7 and J.flead) else None
        if beat == '5cut' and J.look and kn == 1:            # M10m: the look-up sits in b5's second gap
            L.recover()
            info.append(L.lookup_to_raise(imp - IMPACT_A - len(L.seq)))
        elif fl:
            info.append(fl)
        else:
            L.recover()
            info.append(L.read_to_raise(imp - IMPACT_A - len(L.seq), RATE_MAX_B7 if beat == 7 else RATE_MAX))
        if D22 and beat == '5cut' and kn == len(knocks) - 2:  # M10o: strike through, black over the snip
            L.strike(0, IMPACT_A + 1)
            tail = iter(range(IMPACT_A + 1, 96))
            while len(L.seq) < n:
                o = len(L.seq)
                if SNIP[0] <= o < SNIP[1]:
                    L.seq.append(dict(src=None, f=None, snap=None, impact=False))
                else:
                    f = next(tail, None)
                    L.seq.append(dict(src=None, f=None, snap=None, impact=False) if f is None else
                                 dict(src='A', f=f, snap=None, impact=False))
            break
        if q == 'Q5' and E5:                                  # M10p: hit + follow-through, then carry on (faded later)
            L.strike(0)
            L.recover()
            if n > len(L.seq):
                L.read(n - len(L.seq))
            break
        if q == 'Q5':                                         # the capper: approved f0-95, black on the old frame
            L.strike(0, IMPACT_A + 1 if D22 else 96)        # M10o: snap to black after the impact frame
            L.seq += [dict(src=None, f=None, snap=None, impact=False) for _ in range(n - len(L.seq))]
            break
        L.strike(0)
    else:
        L.recover()
        L.read(n - len(L.seq))
    seq = L.seq[:n]
    assert len(seq) == n, (beat, len(seq), n)
    for imp, _ in knocks:
        assert seq[imp]['src'] == 'A' and seq[imp]['f'] == IMPACT_A, (beat, imp, seq[imp])
        seq[imp]['impact'] = True
    return seq, info


def length(beat, full):
    return 2424 if (beat == '5cut' and full) else ga.LENGTH[beat]


# ------------------------------------------------------------------------------------------------ render
def frames(sc, seq, beat, clean=False):
    t0 = BEAT_T0[5 if beat == '5cut' else beat]
    size = SIZE[beat]
    rng = np.random.default_rng(1817)
    shake = 0
    for n, s in enumerate(seq):
        if s['src'] is None:
            yield np.zeros((OH, OW, 3), np.float32)
            continue
        m = sc.mask(s, size)
        im = compose_opaque(sc, n, t0, m, sc.cl(s['src'], s['f']), clean)
        if s['impact']:
            shake = 6
        if shake:
            amp = 7 * shake / 6
            dx, dy = rng.integers(-amp, amp + 1, 2)
            im = np.roll(im, (int(dy), int(dx)), (0, 1)) * (1 + 0.05 * shake / 6)
            shake -= 1
        if 'gain' in s:                                       # M10p: b7 fade to black (EXT_E5)
            im = im * s['gain']
        yield im


def render(out, beat, full, clean=False):
    if os.path.exists(out):
        raise SystemExit(f'refusing: {out} exists')
    sc = Scene()
    J = Joins(sc)
    J.report()
    seq, info = timeline(beat, J, length(beat, full))
    print('exits (iou, x, y, rate):', info, flush=True)
    tmp = os.path.join(os.path.dirname(out), '_tmp_' + os.path.basename(out))
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OW}x{OH}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '14',
                          '-pix_fmt', 'yuv420p', tmp], stdin=subprocess.PIPE)
    k = 0
    for im in frames(sc, seq, beat, clean):
        w.stdin.write((np.clip(im, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
        k += 1
        if k % 120 == 0:
            print(f'{k} frames', flush=True)
    w.stdin.close()
    if w.wait() != 0:
        raise SystemExit('ffmpeg failed')
    os.replace(tmp, out)
    print(k, 'frames ->', out, 'DONE', flush=True)


def describe(seq):
    rows = []
    for i, s in enumerate(seq):
        r = rows[-1] if rows else None
        if r and r['src'] == s['src'] and (s['src'] is None or 0 <= s['f'] - r['f1'] <= 1.5):
            r['o1'], r['f1'] = i, s['f']
        else:
            rows.append(dict(src=s['src'], o0=i, o1=i, f0=s['f'], f1=s['f']))
    return rows


def plan(beat, full):
    sc = Scene()
    J = Joins(sc)
    J.report()
    seq, info = timeline(beat, J, length(beat, full))
    print('exits (iou, x, y, rate):', info)
    print(f'beat {beat}: {len(seq)} frames, size {SIZE[beat]}')
    for r in describe(seq):
        f0 = '' if r['f0'] is None else f"{r['f0']:.2f}-{r['f1']:.2f}"
        print(f"  out {r['o0']:5d}-{r['o1']:5d} ({r['o0'] / FPS:6.2f} s)  {r['src']} {f0}")
    sn = [i for i, s in enumerate(seq) if s['snap']]
    print('  eased frames:', sn)
    print('  impacts at out', [i for i, s in enumerate(seq) if s['impact']])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['measure', 'plan', 'render'])
    ap.add_argument('out', nargs='?')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, '5cut', 7])
    ap.add_argument('--full', action='store_true', help="b5 at its full 2424 f (Darren's uncut 21112026 mix)")
    ap.add_argument('--clean', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'measure':
        Joins(Scene()).report()
    elif a.cmd == 'plan':
        plan(a.beat, a.full)
    else:
        render(a.out, a.beat, a.full, a.clean)
