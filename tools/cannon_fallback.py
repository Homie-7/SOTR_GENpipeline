"""S5 cannonball option B, 0-cr SCRIPT FALLBACK (Homie F50: "Build it" + "a bit of camera shake so the entire environment shakes").

No generation. Built from the real camps show files and the praised probe v4 CENTRE explosion.

A. Before impact: the REAL camps show files on all four walls (their last NPRE frames). ONE solid dark ball (script-drawn disc,
   no halo, short motion blur) falls on CENTRE along the path of the v4 ball and touches the ground on the contact frame.
B. Contact: ONE warm glow in ONE stage space (LEFT | CENTRE | RIGHT, FLOOR under CENTRE) grows from the impact point over every
   wall in GROW frames (the cannon_glow.py glow). Under the peak every wall cuts: CENTRE to probe v4 (upscaled), LEFT / RIGHT /
   FLOOR to script smoke.
C. After the cut: CENTRE = v4, with script smoke over its top (v4 shows the sky again) and on a thin edge band (so the seams
   carry the same smoke). LEFT / RIGHT / FLOOR = script smoke (advected fbm noise in stage space), colour-matched per frame to
   v4's own smoke, plus small embers (own seed per wall, size per wall). No landscape on any wall after the flash.
D. Camera shake: ONE shake signal, the same offsets on all four walls, from contact, strong then decaying (SHAKE s), with a
   small scale-up (eased in under the glow) so no edge shows.
E. End (v6, Homie F53: "create the smoke in a way that it matches S6's smoke"; "this can still fade away into black"):
   the smoke MOVES like S6 from the explosion on: a fast sideways burst out from the impact (like the CENTRE probe), an upward
   plume that fades away, then S6's own measured wind drift per wall (all walls drift RIGHT; dark top, body low/mid) and S6's
   colour. The file ends in an eased fade to black (embers a little behind); the S6 show files are NOT changed (they start
   from black). No S6 frames, no crossfade, no S6 trims (v5 dropped). Sound: v4's own sound, faded out with the picture.

Timeline (output 25 fps = camps rate; v4 plays 1 frame per output frame):
  o < TAIL            camps only
  TAIL <= o < G0      camps + ball (v4 frames 0..31)          G0 = TAIL + V4FLASH = contact
  G0 <= o < CUT       camps + ball at contact + glow growing  CUT = G0 + GROW (the camps' last frame is out CUT-1)
  o >= CUT            v4 frame o - G0 + V4FLASH / smoke

usage: python tools/cannon_fallback.py OUTDIR [--tail 3.0] [--name S5-CANNON-FALLBACK]
"""
import argparse, os, subprocess, sys
import numpy as np, cv2

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cannon_glow import read, luma, MEDIA, CAMPS, S6, W, H, FPS, NCAMPS, WALLS, GLOW, ORIGIN  # noqa: E402

V4 = f'{MEDIA}/04_WORKING_FILES/S5_cannonball/probe_v4/S5-CANNON-PROBE_v4_CENTRE_a2ab023e.mp4'
V4FLASH = 32                       # v4 frame of the powder flash (probe_v4 measure: first big luma jump f32)
SX, SY = W / 854, H / 480          # v4 -> 1080 scale
# v4 ball path (v4 px), measured: x ~419 while it falls, y per frame; it lands at ~(400, 360) on the contact frame
BALL_Y = {0: 11, 4: 12, 8: 14, 12: 19, 16: 27, 18: 36, 20: 44, 22: 57, 24: 74, 26: 105, 28: 150, 29: 202, 30: 271, 31: 330, 32: 360}
BALL_X = {0: 419, 28: 419, 30: 412, 31: 405, 32: 400}
BALL_R = {0: 2.0, 16: 4.5, 21: 7.0, 28: 10.0, 32: 12.0}     # radius in v4 px
BALL_COL = np.array([14, 12, 18], np.float32)               # BGR, near-black iron


def interp(table, k):
    ks = sorted(table)
    return float(np.interp(k, ks, [table[i] for i in ks]))


def disc_alpha(cx, cy, r, px, py, blur):
    """Anti-aliased solid disc, motion-blurred along (px,py)->(cx,cy) over the last `blur` part of the frame."""
    a = np.zeros((H, W), np.float32)
    x0, x1 = int(max(0, min(cx, px) - r - 3)), int(min(W, max(cx, px) + r + 4))
    y0, y1 = int(max(0, min(cy, py) - r - 3)), int(min(H, max(cy, py) + r + 4))
    if x1 <= x0 or y1 <= y0:
        return a
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    acc = np.zeros_like(xx)
    ns = 7
    for i in range(ns):
        t = 1 - blur * i / (ns - 1)
        bx, by = px + (cx - px) * t, py + (cy - py) * t
        acc += np.clip(r + 0.5 - np.hypot(xx - bx, yy - by), 0, 1)
    a[y0:y1, x0:x1] = acc / ns
    return a


class Smoke:
    """fbm noise in stage space (x in [-W, 2W), y in [0, 2H)), low-res. v6: moved by a displacement map (burst out from the
    impact, then S6's own measured drift), evolving by cross-fading two fields per octave."""

    def __init__(self, seed, ds=6):
        self.ds = ds
        self.sw, self.sh = 3 * W // ds, 2 * H // ds
        rng = np.random.default_rng(seed)
        self.oct = []
        for scale, amp, vx in ((90, 0.50, 0.10), (40, 0.28, -0.12), (18, 0.15, 0.16), (8, 0.07, -0.2)):
            fields = []
            for _ in range(2):
                # periodic (tileable) noise: white noise low-passed in the frequency domain, so BORDER_WRAP has no seam
                wn = rng.standard_normal((self.sh, self.sw)).astype(np.float32)
                fy = np.fft.fftfreq(self.sh)[:, None]
                fx = np.fft.rfftfreq(self.sw)[None, :]
                g = np.exp(-(fx ** 2 + fy ** 2) * (np.pi * scale / 2.5) ** 2)
                f = np.fft.irfft2(np.fft.rfft2(wn) * g, s=wn.shape).astype(np.float32)
                f = (f - f.mean()) / (f.std() + 1e-6) * 0.22 + 0.5
                fields.append(f)
            self.oct.append((scale, amp, vx, fields, rng.random() * 6.28))
        sm = rng.random((self.sh // 60 + 3, self.sw // 60 + 3)).astype(np.float32)
        self.warp = [cv2.resize(rng.random(sm.shape).astype(np.float32), (self.sw, self.sh), interpolation=cv2.INTER_CUBIC) - 0.5
                     for _ in range(2)]
        self.gx, self.gy = np.meshgrid(np.arange(self.sw, dtype=np.float32), np.arange(self.sh, dtype=np.float32))
        self.X = self.gx * ds - W          # stage x (1080 px) of each low-res cell
        self.Y = self.gy * ds

    def field(self, t, dx, dy):
        """t in frames since the cut; dx, dy = content displacement in 1080 px (maps, low-res). Mean ~0.5."""
        out = np.zeros((self.sh, self.sw), np.float32)
        tot = 0
        for scale, amp, vx, (fa, fb), ph in self.oct:
            mx = np.mod(self.gx - (dx + vx * 6 * t) / self.ds, self.sw).astype(np.float32)
            my = np.mod(self.gy - dy / self.ds, self.sh).astype(np.float32)
            a = cv2.remap(fa, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
            b = cv2.remap(fb, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)
            w = 0.5 + 0.5 * np.sin(ph + t / (14 + scale * 0.4))
            out += amp * (a * np.sqrt(w) + b * np.sqrt(1 - w) - 0.5 * (np.sqrt(w) + np.sqrt(1 - w)) + 0.5)
            tot += amp
        out /= tot
        # domain warp for billows
        wx = self.warp[0] * 16 * np.sin(t / 30)
        wy = self.warp[1] * 16 * np.cos(t / 37)
        out = cv2.remap(out, (self.gx + wx).astype(np.float32), (self.gy + wy).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return out

    def wall(self, fld, wall):
        ox, oy = ORIGIN[wall]
        x0, y0 = (ox + W) // self.ds, oy // self.ds
        c = fld[y0:y0 + H // self.ds, x0:x0 + W // self.ds]
        return cv2.resize(c, (W, H), interpolation=cv2.INTER_CUBIC)


class Embers:
    """Small orange embers rising and flickering. Own seed per wall; radius scale per wall."""

    def __init__(self, seed, rscale, n0, n1):
        self.rng = np.random.default_rng(seed)
        self.rs, self.n0, self.n1 = rscale, n0, n1
        self.p = np.zeros((0, 8), np.float32)  # x y vx vy r life age phase

    def spawn(self, k, first=False):
        r = self.rng
        x = r.uniform(0, W, k)
        y = r.uniform(0.15 * H, H, k) if first else r.uniform(0.45 * H, 1.05 * H, k)
        vx = r.normal(0, 0.6, k)
        vy = -r.uniform(0.4, 2.2, k)
        rad = r.uniform(0.9, 2.3, k) * self.rs
        life = r.uniform(40, 140, k)
        return np.stack([x, y, vx, vy, rad, life, np.zeros(k), r.uniform(0, 6.28, k)], 1).astype(np.float32)

    def step(self, t, nt, burst=0):
        target = int(self.n0 + (self.n1 - self.n0) * min(1, t / max(1, nt * 0.6)))
        if t == 0:
            self.p = self.spawn(target + burst, first=True)
        need = target - len(self.p)
        if need > 0:
            self.p = np.concatenate([self.p, self.spawn(need)])
        p = self.p
        p[:, 0] += p[:, 2] + 0.4 * np.sin(p[:, 7] + p[:, 6] / 9)
        p[:, 1] += p[:, 3]
        p[:, 3] *= 0.995
        p[:, 6] += 1
        self.p = p[(p[:, 6] < p[:, 5]) & (p[:, 1] > -10)]

    def draw(self, gain):
        lay = np.zeros((H, W, 3), np.float32)
        for x, y, vx, vy, rad, life, age, ph in self.p:
            u = age / life
            b = gain * np.sin(np.pi * u) ** 0.6 * (0.65 + 0.35 * np.sin(ph + age * 0.9))
            if b <= 0.02:
                continue
            col = (float(40 * b), float(140 * b), float(255 * b))
            cv2.circle(lay, (int(x * 16), int(y * 16)), max(1, int(rad * 16)), col, -1, cv2.LINE_AA, shift=4)
        glow = cv2.GaussianBlur(lay, (0, 0), 3)
        return np.clip(lay + glow * 1.2, 0, 255)


def shake_signal(n, a_x, a_y, decay, length, seed=7):
    """Shared shake offsets (px) for n frames after contact: sum of sines, exp decay, eased to zero at `length`."""
    rng = np.random.default_rng(seed)
    t = np.arange(n, dtype=np.float32) / FPS
    sx = sum(np.sin(2 * np.pi * f * t + rng.random() * 6.28) / (1 + i) for i, f in enumerate((6.3, 9.7, 14.1)))
    sy = sum(np.sin(2 * np.pi * f * t + rng.random() * 6.28) / (1 + i) for i, f in enumerate((7.9, 11.3, 16.7)))
    sx, sy = sx / 1.8, sy / 1.8
    env = np.exp(-t / decay) * np.clip(1 - t / length, 0, 1) ** 0.5
    env[0] = 1.0
    return np.stack([a_x * sx * env, a_y * sy * env], 1)


def smoothstep(e0, e1, x):
    u = np.clip((x - e0) / (e1 - e0), 0, 1)
    return u * u * (3 - 2 * u)


# S6 smoke motion, measured F54 (Farneback on the S6 no-fade 1080 files f0-199, 1080 px per frame at 24 fps; mid+low bands):
# every wall drifts to the RIGHT (wind), a slow rise, dark top. v4 CENTRE settles to the same (+1.1, -0.4) by its f120.
# F55 CORRECTION: Farneback at 480x270 under-read the drift ~4x. Block-match at full res (S6 no-fade f20-140, 3-frame gaps):
# LEFT +10.4, CENTRE +9.0, RIGHT +8.7 px/f, dy ~ -0.3. These are the values used from v6b on.
S6_DX = {'LEFT': 10.4, 'CENTRE': 9.0, 'RIGHT': 8.7}
S6_DY = -0.3
S6V = f'{MEDIA}/04_WORKING_FILES/superseded/S6_wars_FR_nofade/1080'


def flow_stats(frames, a, b):
    """F55: block-match drift (1080 px/f) of the mid band, 3-frame gaps sampled every 10 f over frames a..b-1:
    mean dx, dy, |speed|. (Farneback under-read the fast S6 drift ~4x.)"""
    acc = []
    for i in range(a, b - 3, 10):
        g0 = cv2.cvtColor(cv2.resize(frames[i], (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        g1 = cv2.cvtColor(cv2.resize(frames[i + 3], (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
        ref = g0[225:450, 150:550]
        if ref.mean() < 4:
            continue
        best = None
        for dx in range(-45, 46):
            for dy in range(-8, 5):
                m = float(np.abs(ref - g1[225 + dy:450 + dy, 150 + dx:550 + dx]).mean())
                if best is None or m < best[0]:
                    best = (m, dx, dy)
        dxp, dyp = best[1] * 2 / 3, best[2] * 2 / 3
        acc.append((dxp, dyp, float(np.hypot(dxp, dyp))))
    return np.array(acc).mean(0) if acc else np.zeros(3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--tail', type=float, default=3.0)
    ap.add_argument('--fade', type=int, default=50, help='eased fade to black over the last FADE frames')
    ap.add_argument('--ember-lag', type=int, default=18, help='embers fade this many frames after the smoke starts to fade')
    ap.add_argument('--burst', type=float, default=16, help='outward burst speed at the cut, 1080 px/f')
    ap.add_argument('--burst-tau', type=float, default=22)
    ap.add_argument('--plume', type=float, default=9, help='upward plume speed at the cut, 1080 px/f (it fades out)')
    ap.add_argument('--plume-tau', type=float, default=28)
    ap.add_argument('--s6show', default=S6, help='S6 show files (from black) for the review stage')
    ap.add_argument('--grow', type=int, default=4)
    ap.add_argument('--hold', type=int, default=2)
    ap.add_argument('--decay', type=int, default=10)
    ap.add_argument('--scale', type=float, default=1.04)
    ap.add_argument('--shake', type=float, default=1.8, help='shake length, s')
    ap.add_argument('--shake-x', type=float, default=30)
    ap.add_argument('--shake-y', type=float, default=17)
    ap.add_argument('--cover', type=float, default=0.50, help='CENTRE top smoke cover depth (fraction of H)')
    ap.add_argument('--front', type=float, default=3600, help='smoke front final radius, stage px')
    ap.add_argument('--front-tau', type=float, default=28, help='smoke front ease-out time constant, frames')
    ap.add_argument('--name', default='S5-CANNON-FALLBACK')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    v4 = read(V4, size=(W, H))
    nv = len(v4)
    tail = int(round(a.tail * FPS))
    g0 = tail + V4FLASH
    cut = g0 + a.grow
    n = g0 - V4FLASH + nv
    npre = cut
    F = a.fade
    ix, iy = interp(BALL_X, V4FLASH) * SX, interp(BALL_Y, V4FLASH) * SY
    print(f'v4 {nv} f; tail {tail}; contact out f{g0}; cut f{cut}; out {n} f; impact CENTRE ({ix:.0f},{iy:.0f})', flush=True)

    # A: camps
    walls = {}
    for w in WALLS:
        fr = read(f'{CAMPS}/S5_{w}_camps.mov', ss=(NCAMPS - npre) / FPS, n=npre, size=(W, H))
        assert len(fr) == npre, (w, len(fr))
        walls[w] = [f for f in fr]
    camps_centre = [f.copy() for f in walls['CENTRE']]
    v4_vs_camps = float(np.abs(v4[0].astype(int) - camps_centre[-1].astype(int)).mean())

    # A: the ball
    for o in range(tail, cut):
        k = min(o - tail, V4FLASH)
        cx, cy, r = interp(BALL_X, k) * SX, interp(BALL_Y, k) * SY, interp(BALL_R, k) * SX
        px, py = interp(BALL_X, k - 1) * SX, interp(BALL_Y, k - 1) * SY
        al = disc_alpha(cx, cy, r, px, py, blur=0.45) * min(1, (k + 1) / 4)
        f = walls['CENTRE'][o].astype(np.float32)
        walls['CENTRE'][o] = (f * (1 - al[..., None]) + BALL_COL * al[..., None]).astype(np.uint8)

    # colours: v4's own smoke (smoothed) at the start, S6's own smoke colour per wall at the end
    ker = np.ones(9, np.float32) / 9
    sm = lambda x: np.stack([np.convolve(np.pad(x[:, c], 4, mode='edge'), ker, 'valid') for c in range(3)], 1)

    def box(f, y0, y1, x0, x1):
        return f[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)].reshape(-1, 3).mean(0)
    edge = {}
    for w, (x0, x1) in (('LEFT', (0.0, 0.14)), ('RIGHT', (0.86, 1.0)), ('CENTRE', (0.0, 1.0))):
        eb = sm(np.array([box(f, 0.45, 1.0, x0, x1) for f in v4], np.float32))
        et = sm(np.array([box(f, 0.0, 0.45, x0, x1) for f in v4], np.float32))
        edge[w] = (np.minimum(et, 0.85 * eb), eb)
    fb = sm(np.array([box(f, 0.80, 1.0, 0.1, 0.9) for f in v4], np.float32))
    edge['FLOOR'] = (fb, fb)
    s6v = {w: read(f'{S6V}/S6_{w}_wars_FR-nofade.mov', n=200, size=(W, H)) for w in ('LEFT', 'CENTRE', 'RIGHT')}
    s6col = {w: np.mean([box(f, 0.33, 1.0, 0, 1) for f in s6v[w][:48]], 0).astype(np.float32) for w in s6v}
    s6col['FLOOR'] = 0.7 * s6col['CENTRE']
    v4late = np.mean([box(f, 0.33, 1.0, 0, 1) for f in v4[160:nv - 10]], 0)
    gain_c = np.clip((s6col['CENTRE'] + 1) / (v4late + 1), 0.4, 2.0).astype(np.float32)

    # C: after the cut
    smoke = Smoke(seed=51)
    nt = n - cut
    emb = {'LEFT': Embers(101, 1.0, 60, 260), 'RIGHT': Embers(202, 1.0, 60, 260), 'FLOOR': Embers(303, 1.35, 50, 200),
           'CENTRE': Embers(404, 1.0, 10, 40)}
    yy = (np.arange(H, dtype=np.float32) / H)[:, None]
    xx = (np.arange(W, dtype=np.float32) / W)[None, :]
    YY = np.broadcast_to(yy, (H, W))
    XX = np.broadcast_to(xx, (H, W))
    cover_top = (1 - smoothstep(0.55 * a.cover, a.cover, YY))[..., None]
    cover_c = np.maximum.reduce([1 - smoothstep(0.55 * a.cover, a.cover, YY), 1 - smoothstep(0.0, 0.07, XX),
                                 smoothstep(0.93, 1.0, XX), smoothstep(0.93, 1.0, YY)])[..., None]
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = {w: np.hypot(xs + ORIGIN[w][0] - ix, ys + ORIGIN[w][1] - iy) for w in WALLS}
    # stage drift profile u(x): S6's measured speed at each wall's centre, linear between (FLOOR rides with CENTRE)
    u = np.interp(smoke.X, [-W / 2, W / 2, 3 * W / 2], [S6_DX['LEFT'], S6_DX['CENTRE'], S6_DX['RIGHT']]).astype(np.float32)
    side = np.tanh((smoke.X - ix) / 600).astype(np.float32)
    ramp = np.clip(np.arange(nt, dtype=np.float32) / 40, 0.3, 1.0)        # the wind takes over as the burst dies
    T = np.concatenate([[0], np.cumsum(ramp)[:-1]]).astype(np.float32)
    front_log = []
    for o in range(cut, n):
        t = o - cut
        k = o - g0 + V4FLASH
        B = a.burst * a.burst_tau * (1 - np.exp(-t / a.burst_tau))          # burst displacement, sideways out
        P = a.plume * a.plume_tau * (1 - np.exp(-t / a.plume_tau))          # plume displacement, up
        dx = B * side + u * T[t]
        dy = np.float32(-0.12 * B + S6_DY * T[t])
        fld = smoke.field(float(t), dx, dy)
        fpl = smoke.field(float(t) + 500, dx * 0.6, dy - P)
        wp = float(np.exp(-t / a.plume_tau))                               # the upward part fades away
        e = float(smoothstep(40, 140, t))                                  # colour toward S6
        ytop = 0.02 + 0.2 * float(smoothstep(0, 90, t))                    # S6: dark top, body low/mid
        bm = smoothstep(ytop, ytop + 0.35, YY)[..., None]
        fs = 1 - float(smoothstep(n - F - 1, n - 1, o))                    # eased fade to black, 0 on the last frame
        fe = 1 - float(smoothstep(n - F - 1 + a.ember_lag, n - 1, o))
        rf = a.front * (1 - np.exp(-(t + 1) / a.front_tau))
        dens_c = 0.55 + 1.1 * (0.15 + 0.85 * min(1, t / 60))
        lo = 0.3 - 0.22 * e                                                # S6 has dark gaps between billows
        for w in WALLS:
            nz = smoke.wall(fld, w)
            npl = smoke.wall(fpl, w)
            m = np.clip(1.0 + (nz - 0.5) * dens_c * 1.8, lo, 2.0)[..., None]
            mp = np.clip((npl - 0.42) * 4, 0, 1.6)[..., None]
            et, eb = edge[w]
            cb = eb[k] * (1 - e) + s6col[w] * e
            if w == 'CENTRE':
                wl = (1 - smoothstep(0.0, 0.2, xx))[..., None]
                wr = smoothstep(0.8, 1.0, xx)[..., None]
                cbl = edge['LEFT'][1][k] * (1 - e) + s6col['LEFT'] * e
                cbr = edge['RIGHT'][1][k] * (1 - e) + s6col['RIGHT'] * e
                cb = cb * (1 - wl - wr) + cbl * wl + cbr * wr
            if w == 'FLOOR':
                img = cb * m
            else:
                img = cb * m * bm + et[k] * mp * (1 - bm) * wp
            fm = smoothstep(-1.0, 1.0, (rf - dist[w] + 900 * (nz - 0.5)) / 400)[..., None]
            if w == 'LEFT' and t % 5 == 0:
                front_log.append((o, int(rf), float(fm.mean())))
            img = (img * fm).astype(np.float32)
            emb[w].step(t, nt, burst=40 if w != 'CENTRE' else 0)
            if w == 'CENTRE':
                vf = v4[k].astype(np.float32) * (1 + (gain_c - 1) * e)
                c = np.maximum(cover_c * fm, cover_top)
                img = vf * (1 - c) + (img / np.maximum(fm, 1e-3) * np.maximum(fm, cover_top)) * c
                img = img * fs + emb[w].draw(gain=0.8) * cover_c * fm * fe
            else:
                img = img * fs + emb[w].draw(gain=min(1, 0.4 + t / 30) * (0.9 if w != 'FLOOR' else 0.8)) * fm * fe
            walls[w].append(np.clip(img, 0, 255).astype(np.uint8))

    # B: ONE glow in stage space (cannon_glow.py section B)
    dmax = max(float(d.max()) for d in dist.values())
    feather = 0.35 * dmax
    gend = min(n, cut + a.hold + a.decay)
    for o in range(g0, gend):
        t = o - g0
        if t < a.grow:
            r = (dmax + feather) * ((t + 1) / a.grow) ** 0.8
            env = 0.55 + 0.4 * (t + 1) / a.grow
        elif t < a.grow + a.hold:
            r, env = 1e9, 0.95
        else:
            r = 1e9
            uu = (t - a.grow - a.hold + 1) / a.decay
            env = 0.95 * (1 - uu) ** 2
        for w in WALLS:
            if r < 1e9:
                kk = env * np.clip((r - dist[w]) / feather, 0, 1)
            elif t < a.grow + a.hold:
                kk = np.full((H, W), env, np.float32)
            else:
                uu = (t - a.grow - a.hold + 1) / a.decay
                lr = dmax * (1 - uu) ** 1.5 + 700
                kk = env * np.exp(-(dist[w] / lr) ** 2) * (1 + uu)
            core = np.clip(1 - dist[w] / (0.5 * dmax), 0, 1) * 0.05
            kk = np.clip(kk + core * (kk > 0), 0, 1)[..., None]
            f = walls[w][o].astype(np.float32)
            walls[w][o] = (f * (1 - kk) + GLOW * kk).astype(np.uint8)

    # D: shared camera shake from contact
    shk = shake_signal(n - g0, a.shake_x, a.shake_y, decay=0.45, length=a.shake)
    for o in range(g0, n):
        t = o - g0
        s = 1 + (a.scale - 1) * min(1, (t + 1) / a.grow) ** 2 * (3 - 2 * min(1, (t + 1) / a.grow))
        dxs, dys = shk[t]
        m = np.float32([[s, 0, (1 - s) * W / 2 + dxs], [0, s, (1 - s) * H / 2 + dys]])
        for w in WALLS:
            walls[w][o] = cv2.warpAffine(walls[w][o], m, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT101)

    # measure
    log = [f'v6 (F54): source CENTRE explosion {V4}', f'v4 {nv} f played 1:1 at {FPS} fps; v4 f0 vs camps CENTRE last MAD {v4_vs_camps:.2f}',
           f'out {n} f ({n / FPS:.2f} s); camps f{NCAMPS - npre}..f{NCAMPS - 1}; tail {tail}',
           f'ball out f{tail}..f{g0 - 1}, contact out f{g0} at CENTRE ({ix:.0f},{iy:.0f}); CUT out f{cut} on ALL walls',
           f'glow out f{g0}..f{gend - 1}; shake {a.shake} s from f{g0}; scale {a.scale}',
           f'smoke motion: burst {a.burst} px/f out from the impact (tau {a.burst_tau} f), plume up {a.plume} px/f fading (tau {a.plume_tau} f), '
           f'then S6 drift dx {S6_DX} dy {S6_DY} (ramped in over 40 f)',
           f'fade to black out f{n - F}..f{n - 1} (eased; last frame 0), embers {a.ember_lag} f behind; NO S6 frames, NO crossfade',
           'S6 show files are NOT changed (they start from black).', '',
           'FLOW (block-match, mid band; 1080 px per frame), S6 no-fade vs v6 output:']
    for w in ('LEFT', 'CENTRE', 'RIGHT'):
        s6s = flow_stats(s6v[w], 0, 120)
        b0 = flow_stats(walls[w], cut + 2, cut + 27)
        b1 = flow_stats(walls[w], n - F - 60, n - F)
        log.append(f'{w}: S6 f0-120 dx {s6s[0]:+.2f} dy {s6s[1]:+.2f} speed {s6s[2]:.2f} | v6 burst f{cut + 2}-{cut + 27} dx {b0[0]:+.2f} '
                   f'dy {b0[1]:+.2f} speed {b0[2]:.2f} | v6 before fade f{n - F - 60}-{n - F} dx {b1[0]:+.2f} dy {b1[1]:+.2f} speed {b1[2]:.2f}')
    for w in ('LEFT', 'CENTRE', 'RIGHT'):
        cur = np.mean([box(walls[w][i], 0.33, 1.0, 0, 1) for i in range(n - F - 30, n - F)], 0)
        top = np.mean([luma(walls[w][i][:int(0.2 * H)]) for i in range(n - F - 30, n - F)])
        s6top = np.mean([luma(f[:int(0.2 * H)]) for f in s6v[w][:48]])
        log.append(f'{w} colour before fade (BGR mid+low) {np.round(cur, 1).tolist()} vs S6 {np.round(s6col[w], 1).tolist()}; '
                   f'top-20% luma {top:.1f} vs S6 {s6top:.1f}')
    after = range(g0 + int(a.shake * FPS) + 2, n - F)
    for name, x, y in (('LEFT|CENTRE', 'LEFT', 'CENTRE'), ('CENTRE|RIGHT', 'CENTRE', 'RIGHT')):
        s = [np.abs(walls[x][i][:, -1].astype(int) - walls[y][i][:, 0].astype(int)).mean() for i in after]
        log.append(f'{name} seam MAD after the shake: mean {np.mean(s):.2f} max {max(s):.2f}')
    s = [np.abs(walls['CENTRE'][i][-1].astype(int) - walls['FLOOR'][i][0].astype(int)).mean() for i in after]
    log.append(f'CENTRE bottom|FLOOR top seam MAD after the shake: mean {np.mean(s):.2f} max {max(s):.2f}')
    log.append('smoke front (out f, radius px, LEFT coverage): ' + ', '.join(f'f{o}:{r}:{c:.2f}' for o, r, c in front_log[:16]))
    for w in WALLS:
        log.append(f'{w} mean luma every 25 f from the cut: {[int(luma(walls[w][i])) for i in range(cut, n, 25)]}; last frame {luma(walls[w][n - 1]):.2f}')
    open(f'{a.out}/measure.txt', 'w').write('\n'.join(log) + '\n')
    print('\n'.join(log), flush=True)

    # sound: v4's own sound from out f tail, silence before, 24 -> 25 fps, faded out with the picture
    aud = f'{a.out}/_v4_sound.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', V4, '-af', 'aresample=48000', '-ac', '2', aud], check=True)
    snd = f'{a.out}/_wall_sound.wav'
    lead = (g0 - V4FLASH) / FPS
    filt = (f'[0:a]atempo={25 / 24:.6f}[q];anullsrc=r=48000:cl=stereo,atrim=0:{lead:.6f}[s];[s][q]concat=n=2:v=0:a=1,'
            f'apad,atrim=0:{n / FPS:.6f},afade=t=out:st={(n - F) / FPS:.6f}:d={F / FPS:.6f}:curve=qsin[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', aud, '-filter_complex', filt, '-map', '[a]', snd], check=True)

    def enc(frames, path, w_, h_, sound=True):
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w_}x{h_}',
                              '-r', str(FPS), '-i', '-'] + (['-i', snd, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k']
                             if sound else []) + ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', path],
                             stdin=subprocess.PIPE)
        for f in frames:
            p.stdin.write(np.ascontiguousarray(f).tobytes())
        p.stdin.close()
        p.wait()

    for w in WALLS:
        enc(walls[w], f'{a.out}/{a.name}_{w}.mp4', W, H)

    # review stage: cannon, then the UNCHANGED S6 show files' first 75 frames (they start from black)
    s6 = {w: read(f'{a.s6show}/S6_{w}_wars.mov', n=75, size=(W, H)) for w in ('LEFT', 'CENTRE', 'RIGHT')}
    stsnd = f'{a.out}/_stage_sound.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', snd, '-i', f'{a.s6show}/S6_CENTRE_wars.mov', '-filter_complex',
                    f'[1:a]atrim=0:{75 / 24:.6f},aresample=48000,aformat=channel_layouts=stereo,atempo={25 / 24:.6f}[b];'
                    f'[0:a]aresample=48000,aformat=channel_layouts=stereo[c];[c][b]concat=n=2:v=0:a=1[a]', '-map', '[a]', stsnd], check=True)
    hs, ws = H // 2, W // 2

    def stage(l, c, r, f):
        o = np.zeros((H, W * 3 // 2, 3), np.uint8)
        o[:hs, :ws] = cv2.resize(l, (ws, hs), interpolation=cv2.INTER_AREA)
        o[:hs, ws:2 * ws] = cv2.resize(c, (ws, hs), interpolation=cv2.INTER_AREA)
        o[:hs, 2 * ws:] = cv2.resize(r, (ws, hs), interpolation=cv2.INTER_AREA)
        if f is not None:
            o[hs:, ws:2 * ws] = cv2.resize(f, (ws, hs), interpolation=cv2.INTER_AREA)
        return o

    rev = [stage(walls['LEFT'][i], walls['CENTRE'][i], walls['RIGHT'][i], walls['FLOOR'][i]) for i in range(n)]
    rev += [stage(s6['LEFT'][i], s6['CENTRE'][i], s6['RIGHT'][i], None) for i in range(75)]
    enc(rev, f'{a.out}/_stage_nosound.mp4', W * 3 // 2, H, sound=False)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{a.out}/_stage_nosound.mp4', '-i', stsnd, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-af', 'apad', '-t', f'{len(rev) / FPS:.4f}',
                    f'{a.out}/{a.name}_review_stage.mp4'], check=True)
    os.remove(f'{a.out}/_stage_nosound.mp4')
    idx = sorted(set(list(range(tail, g0, 10)) + list(range(g0 - 1, gend + 2, 3)) + list(range(gend + 2, n + 75, 12))))[:40]
    tiles = [cv2.putText(cv2.resize(rev[i], (480, 360)), f'f{i}', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
             for i in idx]
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f'{a.out}/contact.jpg', np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]),
                [cv2.IMWRITE_JPEG_QUALITY, 85])
    os.makedirs(f'{a.out}/frames', exist_ok=True)
    for i in (g0 - 1, cut + 6, cut + 20, cut + 50, cut + 100, cut + 150, n - F - 1, n - F // 2, n - 1, n + 24, n + 48, n + 74):
        cv2.imwrite(f'{a.out}/frames/stage_f{i}.jpg', rev[i], [cv2.IMWRITE_JPEG_QUALITY, 90])
    print('DONE cannon_fallback', a.out, flush=True)


if __name__ == '__main__':
    main()
