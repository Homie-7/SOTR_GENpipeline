"""Render the court's appearances on CENTRE, v2: real performance and the scrim field.

Built 2026-09-25 from LOOK.md D12 and D13 (Claude, delegated by Homie). v1 (render_court.py) stays
as it was, so the v1 renders can be rebuilt.

WHAT CHANGED FROM v1 (Homie: "the same silhouette scaled one by one"; "the first judge feels too
small"; the field "too bright… very flat 2D"):
- Between strikes the judge READS (S9-CRT-READ loop, 350 frames, loops with no crossfade) instead
  of freezing in the raised pose.
- Each appearance strikes differently: beat 3 the MEASURED blow (S9-CRT-STRIKE-B3), beat 5 the
  measured blow on "Two!", the approved strike on "Three!" and the FRANTIC DOUBLE
  (S9-CRT-STRIKE-B5) when he loses control, beat 7 the approved strike at the push-in, then the
  Q5 capper (D8). B3 and B5 are Sequels of the reading loop, so the loop is phased to hand over
  on its last frame (349) exactly when they start: the join is the model's own.
- Sizes: Q1 ~2.0 m (was 1.2 m), Q2 ~2.7 m, Q3 fills with the head just cropped, Q4 push-in.
- The field (D13): a lit paper scrim in the shadow-theatre tradition. Dimmer warm paper with grain
  and fibre, the lamp behind it breathing, soft grey shadows of the bar's balustrade (near) and two
  tall arched windows (far). Only the judge is crisp black.
Everything else as v1: threshold after resizing (clean curves), the epaulette patch, the floor
rule (source bottom on the wall bottom while the legs are in shot), a hard jump and a shudder on
every impact, files start and end at full picture.

  python tools/render_court_v2.py OUT.mov --beat 3|5|7
  python tools/render_court_v2.py OUT.png --still Q1        (one frame, for a look check)

Output: CENTRE 5:3, 1800x1080, 24 fps. Clean renders go to
SOTR_MEDIA/01_FINAL_FOR_SHOW/CENTRE_wall_COURT/ and are never overwritten. Needs ffmpeg, numpy, OpenCV.
"""
import argparse
import os
import subprocess

import cv2
import numpy as np

HERE = os.path.dirname(__file__)
MEDIA = os.path.join(HERE, '..', '..', 'SOTR_MEDIA')
SRC = {
    'read': os.path.join(MEDIA, '03_TESTS_IN_PROGRESS', 'judge_tests', 'S9-CRT-READ_v1_loop.mov'),
    'b3': os.path.join(MEDIA, '03_TESTS_IN_PROGRESS', 'judge_tests', 'S9-CRT-STRIKE-B3_v2.mp4'),
    'b5': os.path.join(MEDIA, '03_TESTS_IN_PROGRESS', 'judge_tests', 'S9-CRT-STRIKE-B5_v1.mp4'),
    'appr': os.path.join(MEDIA, '02_APPROVED_BUILDING_BLOCKS', 'clips', 'fig_SOTR_judge_strike_s9_v1.mp4'),
}
OW, OH, FPS = 1800, 1080, 24
SW, SH = 1080, 1920
PX_PER_M = OH / 3.6

SIZES = {
    'Q1': dict(s=0.37, floor=True),
    'Q2': dict(s=0.50, floor=True),
    'Q3': dict(s=0.65, floor=True),
    'Q4': dict(s=1.45, floor=False, cx=575, cy=520),
    'Q5': dict(s=None, floor=False),
}
# per strike clip: first frame used, the impact frame (shudder), last frame used.
# 'seq' = a Sequel of the reading loop (the loop must hand over on frame 349 just before it).
STRIKES = {
    'b3': dict(first=0, impact=[43], last=67, seq=True),       # B3 v2: raise, blow lands f43 (measured)
    'b5': dict(first=0, impact=[24, 64], last=88, seq=True),   # B5 v1: blows land f24 and f64 (measured)
    'appr': dict(first=40, impact=[53], last=77, seq=False),   # the approved clip: blow f48-53
}
APPR_HELD = 96

# D1 timings (seconds within the appearance) -> (time, size, clip)
BEATS = {
    3: dict(length=40, cues=[(1.0, 'Q1', 'b3')]),
    5: dict(length=101, cues=[(0.5, 'Q2', 'b3'), (45.0, 'Q3', 'appr'), (85.0, 'Q3', 'b5')]),
    7: dict(length=20, cues=[(0.5, 'Q4', 'appr'), (16.0, 'Q5', 'capper')]),
}
READ_N = 350


BAR_FIX = {'b5'}  # clips whose incidental white bar across the held gavel is closed (never 'appr': its keyline is sanctioned)


def load(path, close_bars=False):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={SW}:{SH}', '-f', 'rawvideo',
                          '-pix_fmt', 'gray', '-'], capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW).astype(np.float32) / 255
    out = []
    for g in f:
        black = (g < 0.5).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
        g = g.copy()
        for i in range(1, n):  # epaulette patch: small white islands enclosed by black
            x, y, w, h, area = st[i]
            if area < 600 and not (x == 0 or y == 0 or x + w >= SW or y + h >= SH):
                g[lab == i] = 0.0
        if close_bars:  # a thin horizontal white bar with black above and below it -> black
            black = (g < 0.5).astype(np.uint8)
            closed = cv2.morphologyEx(black, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 15)))
            g[(closed == 1) & (black == 0)] = 0.0
        out.append((g * 255 + 0.5).astype(np.uint8))  # 8-bit in memory (4 clips as float32 ~5 GB)
    return np.stack(out)


def gavel_box(g):
    black = (g < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(black, 8)
    comps = sorted((st[i] for i in range(1, n)), key=lambda c: -c[4])
    x, y, w, h, _ = comps[1]
    return x, y, w, h


# ---------------------------------------------------------------- the field (D13)
def _blur(a, s):
    return cv2.GaussianBlur(a, (0, 0), s)


def field_static():
    rng = np.random.default_rng(1817)
    yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
    xn, yn = (xx - OW / 2) / (OW / 2), (yy - OH / 2) / (OH / 2)
    mott = _blur(rng.normal(0, 1, (OH, OW)).astype(np.float32), 60); mott /= mott.std()
    mid = _blur(rng.normal(0, 1, (OH, OW)).astype(np.float32), 6); mid /= mid.std()
    fib = cv2.GaussianBlur(rng.normal(0, 1, (OH, OW)).astype(np.float32), (0, 0), sigmaX=3, sigmaY=1.2)
    fib /= fib.std()
    tooth = rng.normal(0, 1, (OH, OW)).astype(np.float32)
    paper = 1 + 0.035 * mott + 0.022 * mid + 0.006 * fib + 0.01 * tooth
    # far layer: two tall arched windows (the lamp shows through them), their frames and bars shade
    far = np.zeros((OH, OW), np.float32)
    wall = np.full((OH, OW), 0.35, np.float32)
    for cx in (OW * 0.25, OW * 0.75):
        w, top, bot = 0.95 * PX_PER_M, OH - 3.3 * PX_PER_M, OH - 0.9 * PX_PER_M
        x0, x1, ya = int(cx - w / 2), int(cx + w / 2), int(top + w / 2)
        frame = np.zeros_like(far); glass = np.zeros_like(far); bars = np.zeros_like(far)
        cv2.rectangle(frame, (x0 - 18, ya), (x1 + 18, int(bot)), 1, -1)
        cv2.ellipse(frame, (int(cx), ya), (int(w / 2) + 18, int(w / 2) + 18), 0, 180, 360, 1, -1)
        cv2.rectangle(glass, (x0, ya), (x1, int(bot)), 1, -1)
        cv2.ellipse(glass, (int(cx), ya), (int(w / 2), int(w / 2)), 0, 180, 360, 1, -1)
        cv2.line(bars, (int(cx), int(top)), (int(cx), int(bot)), 1, 7)
        for k in range(1, 5):
            y = int(ya + k * (bot - ya) / 5)
            cv2.line(bars, (x0, y), (x1, y), 1, 7)
        far = np.maximum(far, np.clip(frame - glass, 0, 1) + bars * glass)
        wall *= 1 - glass
    far = _blur(np.maximum(far, wall), 22)
    # near layer: the bar's balustrade, rail at 1.0 m
    near = np.zeros((OH, OW), np.float32)
    rail_y, rail_h, base = int(OH - 1.0 * PX_PER_M), int(0.07 * PX_PER_M), OH - int(0.12 * PX_PER_M)
    cv2.rectangle(near, (0, rail_y), (OW, rail_y + rail_h), 1, -1)
    cv2.rectangle(near, (0, base), (OW, OH), 1, -1)
    step = int(0.22 * PX_PER_M)
    for x in range(step // 2, OW, step):
        for y in range(rail_y + rail_h, base):
            t = (y - rail_y - rail_h) / (base - rail_y - rail_h)
            r = 0.07 if (0.1 < t < 0.14 or 0.86 < t < 0.9) else 0.035 + 0.03 * np.sin(np.pi * (0.15 + 0.75 * t)) ** 2
            near[y, int(x - r * PX_PER_M):int(x + r * PX_PER_M)] = 1
    near = _blur(near, 7)
    scenery = 1 - 0.30 * far - 0.30 * near
    lamp = 0.42 + 0.58 * np.exp(-(xn ** 2 * 0.9 + (yn + 0.1) ** 2 * 1.3))
    paper_rgb = np.array([0.80, 0.72, 0.58], np.float32)
    return paper_rgb[None, None] * (paper * scenery)[..., None], lamp


class TornEdges:
    """D7 (revised 2026-09-24) + Homie 2026-09-25 ("these realities have the fragmented edges throughout
    the whole time"): the lit paper tears at BOTH sides into the dark, and scraps of it float there,
    drifting slowly. Depth ~8% per side. Behind the judge, who never breaks (at every cue he stays
    inside the torn line: the widest, Q4's scroll arm, reaches ~84% of the width)."""

    def __init__(self, depth=0.08, n=16, seed=1819):
        rng = np.random.default_rng(seed)
        y = np.arange(OH, dtype=np.float32)
        self.mask = np.ones((OH, OW), np.float32)
        rim = np.zeros((OH, OW), np.float32)
        for side in (0, 1):
            # a ragged torn line: slow wander + tear detail
            wav = sum(rng.normal(0, 1) * np.sin(2 * np.pi * (y / OH) * f + rng.uniform(0, 6.3)) / f
                      for f in (1, 2, 3, 5, 8, 13))
            det = np.cumsum(rng.normal(0, 1, OH)); det = det - np.convolve(det, np.ones(41) / 41, 'same')
            edge = OW * depth * (1 + 0.25 * wav / 2) + 1.2 * det
            xs = np.arange(OW, dtype=np.float32)[None, :]
            d = (xs - edge[:, None]) if side == 0 else ((OW - 1 - xs) - edge[:, None])
            self.mask *= np.clip(d / 1.5, 0, 1)
            rim = np.maximum(rim, np.exp(-np.clip(d, 0, None) / 2.0) * (d > 0))
        self.rim = rim
        # floating scraps: torn polygons of paper, lit dimmer than the sheet, drifting in place
        self.scraps = []
        for side in (0, 1):
            for _ in range(n):
                r = rng.uniform(8, 34)
                k = rng.integers(5, 9)
                ang = np.sort(rng.uniform(0, 2 * np.pi, k))
                rad = r * rng.uniform(0.55, 1.0, k)
                poly = np.stack([rad * np.cos(ang), rad * np.sin(ang)], 1)
                x0 = rng.uniform(0.004, depth * 0.9) * OW
                cx = x0 if side == 0 else OW - x0
                self.scraps.append(dict(poly=poly, cx=cx, cy=rng.uniform(0.04, 0.96) * OH,
                                        amp=rng.uniform(3, 10), f=rng.uniform(0.03, 0.08), ph=rng.uniform(0, 6.3),
                                        rot=rng.uniform(-0.15, 0.15), shade=0.35 + 0.45 * (1 - x0 / (depth * OW))))

    def frame(self, i):
        """(field mask, scrap alpha, scrap shade) for output frame i."""
        t = i / FPS
        alpha = np.zeros((OH, OW), np.float32)
        shade = np.zeros((OH, OW), np.float32)
        for s in self.scraps:
            a = s['rot'] * np.sin(2 * np.pi * s['f'] * 0.7 * t + s['ph'])
            R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]], np.float32)
            dx = s['amp'] * np.sin(2 * np.pi * s['f'] * t + s['ph'])
            dy = s['amp'] * 0.6 * np.sin(2 * np.pi * s['f'] * 1.3 * t + s['ph'] * 1.7)
            pts = (s['poly'] @ R.T + [s['cx'] + dx, s['cy'] + dy]).astype(np.int32)
            m = np.zeros((OH, OW), np.uint8)
            cv2.fillPoly(m, [pts], 1, lineType=cv2.LINE_AA)
            alpha = np.maximum(alpha, m.astype(np.float32))
            shade = np.where(m > 0, s['shade'], shade)
        return self.mask, alpha, shade


def with_edges(base, lamp_i, edges, i):
    """The lit field with its torn edges and floating scraps (before the figure is laid on)."""
    fmask, alpha, shade = edges.frame(i)
    lit = base * lamp_i[..., None]
    sheet = lit * (fmask * (1 + 0.12 * edges.rim))[..., None]
    scraps = lit * (shade * alpha)[..., None]
    return sheet * (1 - alpha[..., None]) + scraps


def lamp_gain(i):
    """The lamp behind the paper breathes: slow swell plus a small quick flicker (like the candles)."""
    t = i / FPS
    return 1 + 0.025 * np.sin(2 * np.pi * 0.23 * t) + 0.008 * np.sin(2 * np.pi * 1.3 * t + 1.1) \
        + 0.005 * np.sin(2 * np.pi * 3.1 * t + 0.4)


# ---------------------------------------------------------------- placement and timeline
def place(g, size, gbox):
    sz = SIZES[size]
    if size == 'Q5':
        x, y, w, h = gbox
        s = OH * 1.05 / h
        M = np.float32([[s, 0, OW / 2 - s * (x + w / 2)], [0, s, OH / 2 - s * (y + h / 2)]])
    elif sz['floor']:
        s = sz['s']
        M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * SH]])
    else:
        s = sz['s']
        M = np.float32([[s, 0, OW / 2 - s * sz['cx']], [0, s, OH / 2 - s * sz['cy']]])
    grey = cv2.warpAffine(g, M, (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)


def timeline(beat):
    """(clip, frame, size, impact) per output frame, or None for black."""
    b = BEATS[beat]
    n = int(b['length'] * FPS)
    seq = [None] * n
    cues = sorted(b['cues'])
    starts = [int(t * FPS) for t, _, _ in cues]
    # segments: [0, s0) reading, then each strike, then reading until the next cue
    pos = 0
    size = cues[0][1]
    read_start = 0  # loop phase at the start of the current reading segment
    for k, (t, csize, clip) in enumerate(cues):
        start = starts[k]
        if clip == 'capper':
            for i in range(start - pos):  # he reads on until the capper
                seq[pos + i] = ('read', (read_start + i) % READ_N, size, False)
            # D8: the approved clip's blow at Q5, held, then black
            for i, f in enumerate(range(47, 60)):
                if start + i < n:
                    seq[start + i] = ('appr', f, 'Q5', f == 53)
            j = start + 13
            for _ in range(36):
                if j < n:
                    seq[j] = ('appr', APPR_HELD, 'Q5', False); j += 1
            for i in range(j, n):
                seq[i] = None
            return seq
        st = STRIKES[clip]
        # the reading segment before this strike: phase it so a Sequel strike follows frame 349
        seg = start - pos
        if st['seq']:
            read_start = (READ_N - 1 - (seg - 1)) % READ_N
        for i in range(seg):
            seq[pos + i] = ('read', (read_start + i) % READ_N, size, False)
        size = csize
        j = start
        for f in range(st['first'], st['last'] + 1):
            if j < n:
                seq[j] = (clip, f, size, f in st['impact']); j += 1
        pos = min(j, n)
        read_start = 0
    for i in range(pos, n):
        seq[i] = ('read', (read_start + i - pos) % READ_N, size, False)
    return seq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--beat', type=int, choices=[3, 5, 7])
    ap.add_argument('--still', choices=list(SIZES)[:4])
    ap.add_argument('--overwrite', action='store_true')
    a = ap.parse_args()
    if os.path.exists(a.out) and not a.overwrite:
        raise SystemExit(f'refusing: {a.out} exists. Clean renders are never replaced; give the new one a new version')
    base, lamp = field_static()
    if a.still:
        g = load(SRC['read'])[0].astype(np.float32) / 255
        m = place(g, a.still, None)
        img = base * (lamp * lamp_gain(0))[..., None] * m[..., None]
        cv2.imwrite(a.out, (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8))
        print('still ->', a.out)
        return
    seq = timeline(a.beat)
    used = {s[0] for s in seq if s}
    src = {k: load(SRC[k], close_bars=k in BAR_FIX) for k in used}
    gbox = gavel_box(src['appr'][APPR_HELD].astype(np.float32) / 255) if 'appr' in src else None
    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w_ = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{OW}x{OH}',
                           '-r', str(FPS), '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(1817)
    shake = 0
    for i, item in enumerate(seq):
        if item is None:
            img = np.zeros((OH, OW, 3), np.float32)
        else:
            clip, f, size, impact = item
            f = min(f, len(src[clip]) - 1)
            m = place(src[clip][f].astype(np.float32) / 255, size, gbox)
            img = base * (lamp * lamp_gain(i))[..., None] * m[..., None]
            if impact:
                shake = 6
            if shake:
                amp = 7 * shake / 6
                dx, dy = rng.integers(-amp, amp + 1, 2)
                img = np.roll(img, (int(dy), int(dx)), (0, 1)) * (1 + 0.05 * shake / 6)
                shake -= 1
            img = img + rng.normal(0, 0.004, (OH, OW, 1)).astype(np.float32) * (m[..., None] > 0.5)
        w_.stdin.write((np.clip(img, 0, 1) * 65535).astype('<u2').tobytes())
    w_.stdin.close()
    w_.wait()
    print(f'{len(seq)} frames -> {a.out}')


if __name__ == '__main__':
    main()
