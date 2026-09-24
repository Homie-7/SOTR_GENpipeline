"""Render the court's appearances on CENTRE from the approved strike clip.

Built 2026-09-24 from LOOK.md World 3 and D1/D7/D8/D9 (Claude, delegated by Homie).

SOURCE: SOTR_MEDIA/loops/fig_SOTR_judge_strike_s9_v1.mp4 (1080x1920, 97 frames): raised pose to
f47, the blow f48-53, the gavel held huge toward the lens f54-96 with its SANCTIONED white
keyline (LOOK World 3 carve-out, kept).

TWO-TONE: each source frame is resized in grey first, then thresholded (clean curves at any
size), with a narrow anti-aliased band. EPAULETTE PATCH: small white specks enclosed in the
black (the fringe hatching) are filled; the keyline is a long ring far above the area limit,
so it survives.

FIELD (D7): bone-white, brighter at the centre like a lamp behind paper, falling off into
darkness at the left and right, so CENTRE is not a hard rectangle. The court never
disintegrates: the lie holds its shape.

SIZES (figure scale s; the source frame's bottom sits on the wall's floor line while the legs
are in shot, LOOK World 3 step 3): Q1 ~1.2 m, Q2 ~2.4 m, Q3 fills the wall with the head just
cropped, Q4 a push-in on the head and chest, Q5 the gavel alone filling the wall (D8).
Each strike is a HARD jump: raised pose, the blow, the gavel held at the lens ~1 s, then a hard
cut back to the raised pose. Every impact shudders the field (~6 frames).

  python tools/render_court.py OUT.mov --beat 3|5|7        (timed appearance, D1 lengths)
  python tools/render_court.py OUT.mov --strike Q1|Q2|Q3|Q4 (one strike, for a live operator)

Output: CENTRE 5:3 at working resolution, 1800x1080, 24 fps. Clean renders go to
SOTR_MEDIA/renders/clean/ and are never overwritten. Needs ffmpeg, numpy, OpenCV.
"""
import argparse
import os
import subprocess

import cv2
import numpy as np

HERE = os.path.dirname(__file__)
SRC = os.path.join(HERE, '..', '..', 'SOTR_MEDIA', 'loops', 'fig_SOTR_judge_strike_s9_v1.mp4')
OW, OH, FPS = 1800, 1080, 24
SW, SH = 1080, 1920
BONE = np.array([0.93, 0.89, 0.80], np.float32)

# figure scale and placement per size. 'floor': source bottom on the wall bottom; otherwise
# (x, y) = the source point that goes to the frame centre.
SIZES = {
    'Q1': dict(s=0.222, floor=True),
    'Q2': dict(s=0.443, floor=True),
    'Q3': dict(s=0.632, floor=True),
    'Q4': dict(s=1.45, floor=False, cx=575, cy=520),
    'Q5': dict(s=None, floor=False),  # computed from the gavel's box at the lens
}
RAISED, BLOW, HELD = 0, (40, 96), 96

# D1 timings (seconds within the appearance): (time, size, 'strike') and the file length
BEATS = {
    3: dict(length=40, cues=[(0.0, 'Q1', 'appear'), (1.0, 'Q1', 'strike')]),
    5: dict(length=101, cues=[(0.0, 'Q2', 'appear'), (0.5, 'Q2', 'strike'), (45.0, 'Q3', 'strike'),
                              (85.0, 'Q3', 'strike')]),
    7: dict(length=20, cues=[(0.0, 'Q4', 'appear'), (0.5, 'Q4', 'strike'), (16.0, 'Q5', 'capper')]),
}


def load_source():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                         capture_output=True, check=True).stdout
    f = np.frombuffer(raw, np.uint8).reshape(-1, SH, SW).astype(np.float32) / 255
    out = []
    for g in f:
        black = (g < 0.5).astype(np.uint8)
        # epaulette patch: fill small white islands fully enclosed by black
        n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
        g = g.copy()
        for i in range(1, n):
            x, y, w, h, area = st[i]
            touches = x == 0 or y == 0 or x + w >= SW or y + h >= SH
            if area < 600 and not touches:
                g[lab == i] = 0.0
        out.append(g)
    return np.stack(out)


def gavel_box(g):
    """Bounding box of the white keyline ring (white enclosed by black) in a held frame."""
    black = (g < 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(1 - black, 8)
    best = None
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if x == 0 or y == 0 or x + w >= SW or y + h >= SH:
            continue
        if best is None or area > best[4]:
            best = st[i]
    x, y, w, h, _ = best
    return x, y, w, h


def field():
    yy, xx = np.mgrid[0:OH, 0:OW].astype(np.float32)
    xn, yn = (xx - OW / 2) / (OW / 2), (yy - OH / 2) / (OH / 2)
    glow = 0.86 + 0.14 * np.exp(-(xn ** 2 * 1.2 + yn ** 2 * 1.6))       # lamp behind the paper
    side = 1 - ((np.abs(xn) - 0.72) / 0.28).clip(0, 1) ** 1.3            # falls to dark at L/R
    side = side * side * (3 - 2 * side)
    return BONE[None, None, :] * (glow * side)[..., None]


def place(g, size, gbox):
    sz = SIZES[size]
    if size == 'Q5':
        x, y, w, h = gbox
        s = OH * 1.05 / h
        cx, cy = x + w / 2, y + h / 2
        M = np.float32([[s, 0, OW / 2 - s * cx], [0, s, OH / 2 - s * cy]])
    elif sz['floor']:
        s = sz['s']
        M = np.float32([[s, 0, OW / 2 - s * SW / 2], [0, s, OH - s * SH]])
    else:
        s = sz['s']
        M = np.float32([[s, 0, OW / 2 - s * sz['cx']], [0, s, OH / 2 - s * sz['cy']]])
    grey = cv2.warpAffine(g, M, (OW, OH), flags=cv2.INTER_CUBIC, borderValue=1.0)
    return np.clip((grey - 0.44) / 0.12, 0, 1)  # threshold with a narrow AA band: 0 black, 1 white


def timeline(beat=None, strike=None):
    """Yields (source frame index, size, impact) per output frame."""
    if strike:
        seq = [(RAISED, strike, False)] * 12
        for i in range(BLOW[0], BLOW[1] + 1):
            seq.append((i, strike, i == 53))
        seq += [(HELD, strike, False)] * 24 + [(RAISED, strike, False)] * 24
        return seq
    b = BEATS[beat]
    n = int(b['length'] * FPS)
    seq = [None] * n
    cues = sorted(b['cues'])
    size = cues[0][1]
    for i in range(n):
        seq[i] = (RAISED, size, False)
    for t, size, kind in cues:
        start = int(t * FPS)
        if kind == 'appear':
            for i in range(start, n):
                seq[i] = (RAISED, size, False)
            continue
        if kind == 'capper':  # D8: the gavel alone fills the wall, held, then black
            k = start
            for i in range(47, 60):
                if k < n:
                    seq[k] = (i, 'Q5', i == 53); k += 1
            for _ in range(36):
                if k < n:
                    seq[k] = (59, 'Q5', False); k += 1
            for i in range(k, n):
                seq[i] = (None, None, False)  # black
            break
        k = start
        for i in range(BLOW[0], BLOW[1] + 1):
            if k < n:
                seq[k] = (i, size, i == 53); k += 1
        for _ in range(24):
            if k < n:
                seq[k] = (HELD, size, False); k += 1
        for i in range(k, n):
            seq[i] = (RAISED, size, False)
    return seq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--beat', type=int, choices=[3, 5, 7])
    ap.add_argument('--strike', choices=['Q1', 'Q2', 'Q3', 'Q4'])
    ap.add_argument('--overwrite', action='store_true')
    a = ap.parse_args()
    if os.path.exists(a.out) and not a.overwrite:
        raise SystemExit(f'refusing: {a.out} exists. Clean renders are never replaced; give the new one a new version')
    src = load_source()
    gbox = gavel_box(src[59])
    fld = field()
    seq = timeline(a.beat, a.strike)
    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w_ = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{OW}x{OH}',
                           '-r', str(FPS), '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(1817)
    shake = 0
    cache = {}
    for idx, size, impact in seq:
        if idx is None:
            img = np.zeros((OH, OW, 3), np.float32)
        else:
            key = (idx, size)
            if key not in cache:
                cache = {k: v for k, v in cache.items() if k[0] == RAISED} if len(cache) > 8 else cache
                cache[key] = place(src[idx], size, gbox)
            m = cache[key]
            img = fld * m[..., None]
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
