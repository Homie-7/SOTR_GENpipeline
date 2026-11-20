"""Scene 9: the LIVING judge behind the parchment (Homie, M9k 2026-11-20). Script, 0 credits. TEST stage.

Homie: "breathing and nodding on the stress words... lean in on each order and his coat swinging... his resting position
is a bit of a still... every time he brings down the gavel, he then snaps back to the image... We want it to look like
it's just like a constant video." Options doc: docs/S9-IDLE-JUDGE-OPTIONS.md (A + B, everywhere).

Everything is done on the GREY source (the approved strike, fig_SOTR_judge_strike_s9_v1) BEFORE the threshold, so the
figure stays two-tone; court_behind_paper.compose (A2 level 2) is applied after, as now.
- REST pose = source frame 24 (the coat has fallen closed; frames 17-33 are the clip's own quiet plateau).
- LIFE: a smooth displacement field on the grey frame: breathing (continuous, slower and smaller in silence, plus a
  breath before each line), a slow sway sheared from the pinned feet, a head micro-motion driven by Darren's mix
  (fast-minus-slow loudness), a head dip on each stressed word, and on each "Order" a lean toward the room (upper body
  widens, head forward/down, a touch sharper, A2) while the coat swings: the grey flow-morphs REST -> frame 0 (the
  skirts thrown open) and then source frames 0..24 play FORWARD (the generated cloth falling closed). Never reversed.
- INTO A STRIKE: source frames 24..39 play forward into the blow (f40), the life fading out, the figure's scale
  easing to the strike's size (the hard Q2 -> Q3 jump becomes a step forward).
- OUT OF A STRIKE (the fix for the snap): the held gavel (f96) keeps a small breath; then Recover: the gavel draws
  back from the lens into his chest, the body flow-morphs (DIS both ways, shapes blended as signed distances so the
  two-tone edge never ghosts) to f0, and the raised arm comes up at his side into place; A2 sharpness eases back and
  the source's own frames 1..24 play forward as he settles: one continuous movement.
- The capper (b7 Q5) and the blow frames themselves are untouched.

  python tools/court_idle.py stills OUTDIR --beat 5cut --at 17.4,23.9,25.6
  python tools/court_idle.py review OUT.mp4 --beat 5cut --t0 12 --t1 40 [--compare OLD.mov]   (H.264, Darren's audio)
  python tools/court_behind_paper.py beat OUT.mov --beat 5cut --idle                          (the full beat, ProRes)
Word times are on Darren's mix clock (options doc); BEAT_MIX maps each beat file onto it.
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_court as rc  # noqa: E402
import court_behind_paper as cbp  # noqa: E402

FPS, OW, OH, SW, SH = rc.FPS, rc.OW, rc.OH, rc.SW, rc.SH
MIX = r'G:\SOTR\HF\Final changes\the judge TO BE CUT DOWN 19112026.mov'
BEAT_MIX = {3: 77.375, 5: 189.75, '5cut': 189.75, 7: 322.9166667}   # each beat file's start on his mix clock (s9_animatic.S)

# cues on his mix clock (docs/S9-IDLE-JUDGE-OPTIONS.md, faster-whisper word times)
BREATHS = [92.4, 190.2, 206.6, 211.8, 225.1, 243.6, 323.2]
NODS = [91.5, 190.7, 212.3, 207.1, 225.7, 244.1, 330.9, 333.2, 334.8, 337.3]
ORDERS = [207.1, 225.7, 244.1]

REST = 24
APPROACH = REST, rc.BLOW[0] - 1            # 24..39 forward into the blow
HOLD_N = 24                                # the gavel held at the lens (as render_court)
RETURN_N = 20                              # f96 -> f0 (Recover), eased
FLARE_N = 8                                # REST -> f0 morph (the coat thrown open on the lean)
# landmarks of the REST frame, source px (measured 2026-11-20 on frame 24)
HEAD_C, HEAD_R = (546.0, 380.0), (88.0, 100.0)
NECK_Y, SHOULDER_Y, HIP_Y, FEET_Y = 470.0, 545.0, 1150.0, float(rc.FEET_Y)
BODY_CX = 546.0
LO = 4                                     # warp fields are built at 1/4 res and upsampled (they are smooth)


def smooth(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- the grey source: flow morphs
class Morph:
    def __init__(self, src):
        self.src = src
        self.dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
        self.flows = {}
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        self.xx, self.yy = xx, yy
        self.cache = {}

    def flow(self, a, b):
        if (a, b) not in self.flows:
            def prep(g):
                g = cv2.resize(g, (SW // 2, SH // 2), interpolation=cv2.INTER_AREA)
                return cv2.GaussianBlur((g * 255).astype(np.uint8), (0, 0), 2.5)
            f = self.dis.calc(prep(self.src[a]), prep(self.src[b]), None)
            self.flows[(a, b)] = cv2.resize(f, (SW, SH), interpolation=cv2.INTER_LINEAR) * 2.0
        return self.flows[(a, b)]

    @staticmethod
    def sdf(g):
        black = (g < 0.5).astype(np.uint8)
        return (cv2.distanceTransform(1 - black, cv2.DIST_L2, 5) - cv2.distanceTransform(black, cv2.DIST_L2, 5))

    def frame(self, a, b, t):
        """grey frame between source frames a and b at t (0 = a, 1 = b)"""
        t = float(t)
        key = (a, b, round(t, 4))
        if key in self.cache:
            return self.cache[key]
        if t <= 0:
            return self.src[a]
        if t >= 1:
            return self.src[b]
        fab, fba = self.flow(a, b), self.flow(b, a)
        wa = cv2.remap(self.src[a], self.xx + t * fba[..., 0], self.yy + t * fba[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        wb = cv2.remap(self.src[b], self.xx + (1 - t) * fab[..., 0], self.yy + (1 - t) * fab[..., 1],
                       cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        d = (1 - t) * self.sdf(wa) + t * self.sdf(wb)
        shape = np.clip(0.5 + 0.12 * cv2.GaussianBlur(d, (0, 0), 1.2), 0, 1)
        lin = (1 - t) * wa + t * wb
        k = float(np.clip(4 * t * (1 - t) * 2.5, 0, 1))          # exact grey at the ends, clean shapes in between
        g = (lin * (1 - k) + shape * k).astype(np.float32)
        if len(self.cache) > 64:
            self.cache.clear()
        self.cache[key] = g
        return g


# ---------------------------------------------------------------- out of the strike: he takes the gavel back
class Recover:
    """f96 (the gavel at the lens) -> f0 (raised) without tearing. The two frames share no gavel (the generated clip
    cuts f48 -> f53), so a plain flow morph shreds the arm. Built as three layers on the grey (darkness adds):
    - the gavel at the lens: its keyline ring shrinks toward the chest and darkens into the body (he draws it back);
    - the body: f96 with the gavel filled in as torso, flow-morphed (DIS + SDF, as Morph) to f0 with the arm removed;
    - the raised arm of f0: comes up from in front of the chest (hidden in the black torso), rises and opens out to
      its place, a few degrees of rotation about the shoulder.
    Exact f96 at u=0 and exact f0 at u=1."""
    PIVOT = (390.0, 560.0)                 # f0 shoulder joint (source px)

    def __init__(self, src, morph):
        self.morph = morph
        g96, g0 = src[rc.HELD], src[0]
        d = (g96 < 0.44).astype(np.uint8)
        n, lab, st, cen = cv2.connectedComponentsWithStats(d, 8)
        # the gavel's interior is its own component: the keyline ring cuts it off from the body
        cand = [i for i in range(1, n) if 120000 < st[i, 4] < 320000 and 380 < cen[i][0] < 720 and 500 < cen[i][1] < 900]
        if not cand:
            raise SystemExit('Recover: gavel component not found in f96')
        gv = (lab == cand[0]).astype(np.uint8)
        G = cv2.dilate(gv, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41)))
        Gs = cv2.GaussianBlur(G.astype(np.float32), (0, 0), 2.0)
        self.gc = (float(cen[cand[0]][0]), float(cen[cand[0]][1]))
        self.ring = (g96 * Gs).astype(np.float32)  # light of the gavel region (the ring), added on top
        self.body96 = (g96 * (1 - Gs)).astype(np.float32)   # the gavel filled in as torso
        yy, xx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        arm = ((xx < 395) & (yy < 690)).astype(np.float32)
        As = cv2.GaussianBlur(arm, (0, 0), 3.0) * (yy < 700)
        D0 = 1 - g0
        self.arm = (D0 * As).astype(np.float32)   # darkness of the raised arm + gavel
        self.body0 = (1 - D0 * (1 - As)).astype(np.float32)
        self.xx, self.yy = xx, yy

        def prep(g):
            g = cv2.resize(g, (SW // 2, SH // 2), interpolation=cv2.INTER_AREA)
            return cv2.GaussianBlur((np.clip(g, 0, 1) * 255).astype(np.uint8), (0, 0), 2.5)
        dis = morph.dis
        self.fab = cv2.resize(dis.calc(prep(self.body96), prep(self.body0), None), (SW, SH)) * 2.0
        self.fba = cv2.resize(dis.calc(prep(self.body0), prep(self.body96), None), (SW, SH)) * 2.0
        self.cache = {}

    def body(self, t):
        t = float(t)
        if t <= 0:
            return self.body96
        if t >= 1:
            return self.body0
        wa = cv2.remap(self.body96, self.xx + t * self.fba[..., 0], self.yy + t * self.fba[..., 1], cv2.INTER_LINEAR,
                       borderMode=cv2.BORDER_REPLICATE)
        wb = cv2.remap(self.body0, self.xx + (1 - t) * self.fab[..., 0], self.yy + (1 - t) * self.fab[..., 1],
                       cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        dd = (1 - t) * Morph.sdf(wa) + t * Morph.sdf(wb)
        shape = np.clip(0.5 + 0.12 * cv2.GaussianBlur(dd, (0, 0), 1.2), 0, 1)
        k = float(np.clip(4 * t * (1 - t) * 2.5, 0, 1))
        return ((1 - t) * wa + t * wb) * (1 - k) + shape * k

    def frame(self, u):
        u = float(u)
        key = round(u, 4)
        if key in self.cache:
            return self.cache[key]
        if u >= 1:
            return self.morph.src[0]
        # 1) the ring draws back into the chest: 0 .. 0.45
        k = float(smooth(u / 0.45))
        s = 1 - 0.55 * k
        cx, cy = self.gc
        M = np.float32([[s, 0, cx - s * cx], [0, s, cy - s * cy + 60 * k]])
        ring = cv2.warpAffine(self.ring, M, (SW, SH), flags=cv2.INTER_LINEAR, borderValue=0.0) * (1 - k)
        # 2) the body: 0.1 .. 0.95
        b = self.body(smooth((u - 0.1) / 0.85))
        # 3) the arm rises: 0.25 .. 1
        e = float(smooth((u - 0.25) / 0.75))
        if e > 0:
            ang = 30.0 * (1 - e) ** 1.3          # up at his side, opening out to the raised pose (no pass across the face)
            px, py = self.PIVOT
            R = cv2.getRotationMatrix2D((px, py), ang, 1.0)
            R[0, 2] += 70 * (1 - e)
            R[1, 2] += 400 * (1 - e) ** 1.4
            arm = cv2.warpAffine(self.arm, R, (SW, SH), flags=cv2.INTER_LINEAR, borderValue=0.0)
        else:
            arm = 0.0
        g = np.clip(b + ring - arm, 0, 1).astype(np.float32)
        if e > 0 and e < 1:              # clean the union edge (two-tone)
            g = np.clip(np.minimum(b + ring, 1 - arm), 0, 1).astype(np.float32)
        if len(self.cache) > 64:
            self.cache.clear()
        self.cache[key] = g
        return g


# ---------------------------------------------------------------- life: the displacement field
class Warp:
    def __init__(self):
        yy, xx = np.mgrid[0:SH // LO, 0:SW // LO].astype(np.float32) * LO
        self.X, self.Y = xx, yy
        r = np.sqrt(((xx - HEAD_C[0]) / HEAD_R[0]) ** 2 + ((yy - HEAD_C[1]) / HEAD_R[1]) ** 2)
        self.w_head = smooth((1.75 - r) / 0.9)                        # 1 on the head, 0 by the shoulders
        self.w_up = smooth((HIP_Y - yy) / (HIP_Y - SHOULDER_Y))        # 0 below the hips, 1 shoulders and up
        self.w_feet = np.clip((FEET_Y - yy) / (FEET_Y - 280), 0, 1.1)  # 0 at the pinned feet
        self.chest = np.clip((xx - BODY_CX) / 260, -1.4, 1.4) * self.w_up * (1 - self.w_head) * smooth((1300 - yy) / 400)
        fy, fx = np.mgrid[0:SH, 0:SW].astype(np.float32)
        self.fx, self.fy = fx, fy

    def field(self, p, q=1.0):
        """forward displacement (dx, dy) in source px at low res. p: breath, nod, lean, sway, hx, hy.
        q = how much the pose is the REST pose (1) vs the held lunge (0, landmarks differ: whole-body breath + sway)."""
        X, Y = self.X, self.Y
        if q < 1:
            hdx, hdy = 4.0 * p['sway'] * self.w_feet, -5.0 * p['breath'] * self.w_feet
            if q <= 0:
                return hdx, hdy
            rdx, rdy = self.field(p, 1.0)
            return (1 - q) * hdx + q * rdx, (1 - q) * hdy + q * rdy
        b, n, L = p['breath'], p['nod'], p['lean']
        dy = -8.0 * b * self.w_up
        dx = 3.5 * b * self.chest
        # the nod: the head dips and foreshortens (top comes down more than the chin), a hair of tilt
        dy = dy + self.w_head * (9.0 * n + 0.045 * n * (HEAD_C[1] - Y))
        dx = dx + self.w_head * (-(Y - NECK_Y) * np.sin(np.radians(0.7 * n)))
        # head micro-motion from the voice
        dx = dx + self.w_head * p['hx']
        dy = dy + self.w_head * p['hy']
        # the lean toward the room: upper body widens, head/shoulders forward and down, the head a touch bigger
        dx = dx + L * (0.03 * (X - BODY_CX) * self.w_up + 0.03 * (X - HEAD_C[0]) * self.w_head)
        dy = dy + L * (0.016 * (HIP_Y - Y) * self.w_up + 0.03 * (Y - HEAD_C[1]) * self.w_head)
        # sway from the pinned feet
        dx = dx + 5.0 * p['sway'] * self.w_feet
        return dx, dy

    def apply(self, g, p, q=1.0, amount=1.0):
        if amount <= 1e-3:
            return g
        dx, dy = self.field(p, q)
        dx = cv2.resize(dx * amount, (SW, SH), interpolation=cv2.INTER_CUBIC)
        dy = cv2.resize(dy * amount, (SW, SH), interpolation=cv2.INTER_CUBIC)
        return cv2.remap(g, (self.fx - dx).astype(np.float32), (self.fy - dy).astype(np.float32), cv2.INTER_CUBIC,
                         borderMode=cv2.BORDER_REPLICATE)


# ---------------------------------------------------------------- the mix: loudness envelope on the beat's clock
def envelope(beat, n):
    t0 = BEAT_MIX[beat]
    if not os.path.exists(MIX):
        print('court_idle: mix not found, voice-driven head motion off:', MIX)
        return np.full(n, -60.0, np.float32)
    sr = 8000
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-ss', f'{t0:.4f}', '-t', f'{n / FPS + 1:.4f}', '-i', MIX,
                          '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32)
    hop = sr // FPS
    a = np.pad(a, (0, max(0, n * hop - len(a))))
    rms = np.sqrt(np.mean(a[:n * hop].reshape(n, hop) ** 2, 1) + 1e-12)
    return (20 * np.log10(rms + 1e-9)).astype(np.float32)


def ema(x, sec):
    k = 1 - np.exp(-1 / (sec * FPS))
    y = np.empty_like(x)
    acc = x[0]
    for i, v in enumerate(x):
        acc += k * (v - acc)
        y[i] = acc
    return y


# ---------------------------------------------------------------- the timeline
def plan(beat):
    """Per output frame: dict(base=('src', i) | ('morph', a, b, t) | None, scale=(size, s), cl, life, rest, impact,
    p=life params). Strikes keep render_court's blow (f40-96) + 24 held frames exactly."""
    b = rc.BEATS[beat]
    n = int(b['length'] * FPS)
    cues = sorted(b['cues'])
    fr = [None] * n
    size = cues[0][1]
    for i in range(n):
        fr[i] = dict(base=('src', REST), size=size, cl=0.0, life=1.0, q=1.0, impact=False, busy=False)
    strikes = [(int(t * FPS), sz) for t, sz, k in cues if k == 'strike']
    capper = [(int(t * FPS), sz) for t, sz, k in cues if k == 'capper']
    prev = size
    for start, sz in strikes:
        # approach: 24..39 forward into the blow, life fading, scale easing
        k0 = max(0, start - (APPROACH[1] - APPROACH[0] + 1))
        m = start - k0
        for j, i in enumerate(range(k0, start)):
            u = (j + 1) / max(m, 1)
            fr[i].update(base=('src', APPROACH[1] - (m - 1 - j)), life=1 - smooth(u), busy=True,
                         size=(prev, sz, smooth(u)) if prev != sz else sz)
        k = start
        for idx in range(rc.BLOW[0], rc.BLOW[1] + 1):
            if k < n:
                fr[k].update(base=('src', idx), size=sz, cl=cbp.closeness(idx), life=0.0, q=0.0,
                             impact=idx == 53, busy=True)
            k += 1
        for j in range(HOLD_N):
            if k < n:
                fr[k].update(base=('src', rc.HELD), size=sz, cl=1.0, life=smooth(j / 8) * 0.7, q=0.0, busy=True)
            k += 1
        for j in range(RETURN_N):
            u = smooth((j + 1) / RETURN_N)
            if k < n:
                fr[k].update(base=('recover', u), size=sz, cl=1 - u, life=0.7, q=u, busy=True)
            k += 1
        for idx in range(1, REST + 1):          # the coat settles: the source's own cloth, forward
            if k < n:
                fr[k].update(base=('src', idx), size=sz, life=min(1.0, 0.7 + 0.3 * idx / REST), busy=True)
            k += 1
        for i in range(k, n):
            fr[i]['size'] = sz
        prev = sz
    t_mix0 = BEAT_MIX[beat]
    # "Order": lean + coat (skipped where a strike owns the frames)
    orders = []
    for tw in ORDERS:
        i0 = int(round((tw - t_mix0 - 0.1) * FPS))
        span = range(i0, i0 + FLARE_N + REST + 1)
        if 0 <= i0 and span[-1] < n and not any(fr[i]['busy'] for i in span):
            for j in range(FLARE_N):
                fr[i0 + j]['base'] = ('morph', REST, 0, smooth((j + 1) / FLARE_N))
            for idx in range(0, REST + 1):
                fr[i0 + FLARE_N + idx]['base'] = ('src', idx)
            for i in span:
                fr[i]['busy'] = True
            orders.append(tw)
    for c, sz in capper:                       # render_court's capper, unchanged: f47-59 at Q5, held 36, then black
        k = c
        for idx in range(47, 60):
            if k < n:
                fr[k].update(base=('src', idx), size='Q5', cl=1.0, life=0.0, q=0.0, impact=idx == 53)
            k += 1
        for _ in range(36):
            if k < n:
                fr[k].update(base=('src', rc.HELD), size='Q5', cl=1.0, life=0.0, q=0.0)
            k += 1
        for i in range(k, n):
            fr[i].update(base=None, life=0.0)
        break
    # the life parameters
    env = envelope(beat, n)
    fast, slow = ema(env, 0.12), ema(env, 0.6)
    act = np.clip((ema(env, 2.5) + 50) / 22, 0, 1)                   # 0 in his silence, 1 under speech / crowd
    emph = np.clip((fast - slow) / 7.0, -0.6, 1.5)
    t = np.arange(n) / FPS
    rate = 1 / (5.6 - 1.8 * act)                                     # breaths slow down in the quiet
    phase = np.cumsum(2 * np.pi * rate / FPS)
    breath = (0.30 + 0.25 * act) * (0.5 - 0.5 * np.cos(phase))
    for tb in BREATHS:
        c = tb - t_mix0
        up = smooth((t - (c - 0.6)) / 1.0)
        down = 1 - smooth((t - (c + 0.4)) / 2.0)
        breath = breath + 0.9 * up * down
    nod = np.zeros(n)
    for tw in NODS:
        c = tw - t_mix0
        nod += smooth((t - (c - 0.05)) / 0.15) * (1 - smooth((t - (c + 0.15)) / 0.4))
    lean = np.zeros(n)
    for tw in orders:
        c = tw - t_mix0
        lean += smooth((t - (c - 0.1)) / 0.35) * (1 - smooth((t - (c + 0.9)) / 1.4))
    sway = (0.6 * np.sin(2 * np.pi * t / 7.3 + 0.4) + 0.4 * np.sin(2 * np.pi * t / 11.9 + 1.7)) * (0.55 + 0.45 * act)
    hy = 3.0 * emph
    hx = 1.2 * emph * np.sin(2 * np.pi * t / 3.1)
    for i in range(n):
        fr[i]['p'] = dict(breath=float(min(breath[i], 1.3)), nod=float(min(nod[i], 1.0)), lean=float(min(lean[i], 1)),
                          sway=float(sway[i]), hx=float(hx[i]), hy=float(hy[i]))
        if fr[i]['life'] > 0 and fr[i]['q'] >= 1:
            fr[i]['cl'] = max(fr[i]['cl'], 0.3 * fr[i]['p']['lean'])
    return fr


def place_s(g, s):
    """render_court.place's floor branch at any scale (feet on the floor line)"""
    M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * rc.FEET_Y]])
    grey = cv2.warpAffine(g, M, (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)


class Renderer:
    def __init__(self, beat, clean=False):
        self.beat, self.clean = beat, clean
        self.sc = cbp.Scene()
        self.morph = Morph(self.sc.src)
        self.warp = Warp()
        self.recover = None
        self.plan = plan(beat)
        self.t0 = cbp.BEAT_T0[5 if beat == '5cut' else beat]
        # shake state for every frame, exactly as court_behind_paper.final draws it
        rng = np.random.default_rng(1817)
        shake, self.shake = 0, []
        for f in self.plan:
            if f['base'] is None:
                self.shake.append(None)
                continue
            if f['impact']:
                shake = 6
            if shake:
                amp = 7 * shake / 6
                dx, dy = rng.integers(-amp, amp + 1, 2)
                self.shake.append((int(dx), int(dy), shake))
                shake -= 1
            else:
                self.shake.append(None)

    def grey(self, i):
        f = self.plan[i]
        base = f['base']
        if base[0] == 'src':
            g = self.sc.src[base[1]]
        elif base[0] == 'recover':
            if self.recover is None:
                self.recover = Recover(self.sc.src, self.morph)
            g = self.recover.frame(base[1])
        else:
            g = self.morph.frame(*base[1:])
        return self.warp.apply(g, f['p'], q=f['q'], amount=f['life'])

    def mask(self, i, g):
        sz = self.plan[i]['size']
        if isinstance(sz, tuple):
            a, b, u = sz
            return place_s(g, (1 - u) * rc.SIZES[a]['s'] + u * rc.SIZES[b]['s'])
        if sz in ('Q1', 'Q2', 'Q3'):
            return place_s(g, rc.SIZES[sz]['s'])
        return rc.place(g, sz, self.sc.gbox)

    def frame(self, i):
        f = self.plan[i]
        if f['base'] is None:
            return np.zeros((OH, OW, 3), np.float32)
        sc = self.sc
        bgi = sc.base * (sc.lamp * cbp.lamp_gain(i))[..., None] if self.clean else sc.bg(i, self.t0)
        im = cbp.compose(bgi, self.mask(i, self.grey(i)), sc.fib, 2, closeness=float(f['cl']))
        s = self.shake[i]
        if s:
            dx, dy, k = s
            im = np.roll(im, (dy, dx), (0, 1)) * (1 + 0.05 * k / 6)
        return im

    def __len__(self):
        return len(self.plan)


def final(out, beat, clean=False):
    """court_behind_paper.py beat --idle: the full beat, 1800x1080 ProRes 422 HQ, no sound (like final())"""
    if os.path.exists(out):
        raise SystemExit(f'refusing: {out} exists. Clean renders are never replaced; give the new one a new version')
    r = Renderer(beat, clean)
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{OW}x{OH}',
                          '-r', str(FPS), '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2',
                          '-pix_fmt', 'yuv422p10le', out], stdin=subprocess.PIPE)
    for i in range(len(r)):
        w.stdin.write((np.clip(r.frame(i), 0, 1) * 65535).astype('<u2').tobytes())
    w.stdin.close()
    if w.wait():
        raise SystemExit('ffmpeg failed')
    print(len(r), 'frames ->', out)


def review(out, beat, t0, t1, compare=None):
    """H.264 review of a stretch, with Darren's audio on the same clock; --compare puts the current file beside it."""
    r = Renderer(beat)
    i0, i1 = int(round(t0 * FPS)), min(len(r), int(round(t1 * FPS)))
    tmp = os.path.join(os.path.dirname(out), '_tmp_' + os.path.basename(out))
    mix0 = BEAT_MIX[beat] + i0 / FPS
    W = OW * 2 if compare else OW
    vin = ['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{OH}', '-r', str(FPS), '-i', '-']
    ain = ['-ss', f'{mix0:.4f}', '-t', f'{(i1 - i0) / FPS:.4f}', '-i', MIX]
    w = subprocess.Popen(['ffmpeg', '-v', 'error', '-y'] + vin + ain +
                         ['-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-crf', '16', '-preset', 'medium',
                          '-pix_fmt', 'yuv420p', '-vf', f'scale={W // 2 * 2 if not compare else W // 2}:-2',
                          '-c:a', 'aac', '-b:a', '192k', '-shortest', tmp], stdin=subprocess.PIPE)
    old = None
    if compare:
        old = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{i0 / FPS:.4f}', '-i', compare, '-frames:v',
                                str(i1 - i0), '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    for i in range(i0, i1):
        im = (np.clip(r.frame(i), 0, 1) * 255 + 0.5).astype(np.uint8)
        if old is not None:
            o = np.frombuffer(old.stdout.read(OW * OH * 3), np.uint8).reshape(OH, OW, 3)
            im = np.hstack([o.copy(), im])
            cv2.putText(im, 'NOW', (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 3)
            cv2.putText(im, 'LIVING JUDGE (test)', (OW + 30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (255, 255, 255), 3)
        tc = f'b{beat} {i / FPS:6.2f}s  mix {BEAT_MIX[beat] + i / FPS:6.2f}s'
        cv2.putText(im, tc, (W - 760, OH - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2)
        w.stdin.write(im.tobytes())
    w.stdin.close()
    rc_ = w.wait()
    if old is not None:
        old.wait()
    if rc_:
        raise SystemExit('ffmpeg failed')
    os.replace(tmp, out)
    print(i1 - i0, 'frames ->', out)


def stills(outdir, beat, ats):
    os.makedirs(outdir, exist_ok=True)
    r = Renderer(beat)
    tiles = []
    for t in ats:
        i = int(round(t * FPS))
        im = r.frame(i)
        p = os.path.join(outdir, f'idle_b{beat}_{t:06.2f}s_mix{BEAT_MIX[beat] + t:.2f}.png')
        cbp.save(p, im)
        small = cv2.resize(im, (600, 360), interpolation=cv2.INTER_AREA)
        cv2.putText(small, f'{t:.2f}s mix {BEAT_MIX[beat] + t:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (1, 1, 1), 2)
        tiles.append(small)
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    cbp.save(os.path.join(outdir, f'idle_b{beat}_sheet.png'),
             np.vstack([np.hstack(tiles[k:k + 4]) for k in range(0, len(tiles), 4)]))
    print(len(ats), 'stills ->', outdir)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['stills', 'review', 'beat'])
    ap.add_argument('out')
    ap.add_argument('--beat', type=lambda s: int(s) if s.isdigit() else s, choices=[3, 5, 7, '5cut'], default='5cut')
    ap.add_argument('--at', default='17.4,23.9,25.6')
    ap.add_argument('--t0', type=float, default=12.0)
    ap.add_argument('--t1', type=float, default=40.0)
    ap.add_argument('--compare')
    ap.add_argument('--clean', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'stills':
        stills(a.out, a.beat, [float(x) for x in a.at.split(',')])
    elif a.cmd == 'review':
        review(a.out, a.beat, a.t0, a.t1, a.compare)
    else:
        final(a.out, a.beat, a.clean)
