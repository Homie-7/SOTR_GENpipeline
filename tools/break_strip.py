"""Lay a generated break (the Control-block fragment edge) over a finished wall file, by script.

Built 2026-09-25 (Claude). WHY: the salon break that works is S9-SAL-R-WITHER v5 B, an Edit-video
pass on 4 s of the lit loop (LOG 2026-09-25). A 30 s Edit over the whole beat-2/3 chain failed
(band too wide, snuff lost), so the break is carried onto the finished file here instead, with no
credits spent:

1. FOOTPRINT: the pixels the edit changed, found by differencing the break clip against the clip it
   was edited from (union over all frames, limited to x < --max-x). Pixels the edit left alone
   (the left sconce, panel between the cracks) are NOT in it, so they come from the base file and
   follow its reveal and snuff. The mask is the footprint dilated a little and feathered.
2. MOTION: the break clip is played forward then backward (ping-pong), so the blocks float out and
   back with no crossfade, cycling for the whole file.
3. LIGHT: the break was lit by the lit loop. Every frame it takes the base's light at each place,
   as a smooth per-channel gain: blur(base now) / blur(lit reference), so the fragments dim with
   the snuff and warm with the reveal. The void is black and stays black.
4. FLOOR: the generator's faint floor strip under the break (structural, D14) is faded to black over
   the bottom --floor-frac of the frame, inside the footprint only.

  python tools/break_strip.py BASE.mov BREAK.mp4 EDITED_FROM.mp4 OUT.mov [--max-x 0.24]

The base is never modified. OUT is a separate effect file (CLAUDE.md: clean first, effects
separate); .mov = ProRes 422 HQ 10-bit, anything else H.264 preview. Refuses to overwrite.
Needs ffmpeg, numpy, OpenCV.
"""
import argparse
import json
import os
import subprocess

import cv2
import numpy as np


def info(p):
    s = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height', '-of', 'json', p]))['streams'][0]
    return s['width'], s['height']


def read_all(p, w, h):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt',
                          'rgb24', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base')
    ap.add_argument('brk')
    ap.add_argument('edited_from')
    ap.add_argument('out')
    ap.add_argument('--max-x', type=float, default=0.24, help='how far in from the breaking edge the footprint may reach (fraction of width)')
    ap.add_argument('--side', choices=['left', 'right'], default='left', help='the edge that breaks (salon left, studio right)')
    ap.add_argument('--thresh', type=float, default=18, help='difference (0-255) that counts as changed')
    ap.add_argument('--floor-frac', type=float, default=0.05)
    ap.add_argument('--protect', help='x0,y0,x1,y1 (fractions): a rectangle never taken from the break, e.g. the '
                    'studio canvas, so the painting can never be touched')
    ap.add_argument('--layer-gain', type=float, default=1.0, help='scale the break layer (the model may light its blocks '
                    'brighter than the room)')
    ap.add_argument('--period', type=int, help='fit the float to exactly this many frames (193 = one loop cycle, so a '
                    'HOLD piece loops and IN/HOLD/OUT join)')
    ap.add_argument('--offset', type=int, default=0, help='start the float this many frames into its period')
    ap.add_argument('--lit-ref', help='clip whose mean frame is the light the break was made under '
                                      '(default: edited_from)')
    a = ap.parse_args()
    if os.path.exists(a.out):
        raise SystemExit(f'refusing: {a.out} exists')
    W, H = info(a.base)
    brk = read_all(a.brk, W, H)
    src = read_all(a.edited_from, W, H)
    n = len(brk)

    # 1. footprint
    foot = np.zeros((H, W), np.uint8)
    for k in range(n):
        j = min(round(k * (len(src) - 1) / max(n - 1, 1)), len(src) - 1)
        d = np.abs(cv2.GaussianBlur(cv2.cvtColor(brk[k], cv2.COLOR_RGB2GRAY), (0, 0), 3).astype(np.int16) -
                   cv2.GaussianBlur(cv2.cvtColor(src[j], cv2.COLOR_RGB2GRAY), (0, 0), 3).astype(np.int16))
        foot |= (d > a.thresh).astype(np.uint8)
    if a.side == 'left':
        foot[:, int(a.max_x * W):] = 0
    else:
        foot[:, :int((1 - a.max_x) * W)] = 0
    foot = cv2.dilate(foot, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7)))
    if a.protect:
        x0, y0, x1, y1 = [float(v) for v in a.protect.split(',')]
        foot[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = 0
    mask = cv2.GaussianBlur(foot.astype(np.float32), (0, 0), 4)[..., None]

    # 4. floor fade inside the footprint (applied to the break layer)
    ramp = np.ones((H, 1, 1), np.float32)
    f0 = int(H * (1 - a.floor_frac))
    ramp[f0:, 0, 0] = np.linspace(1, 0, H - f0) ** 1.5

    # 3. lit reference
    ref_clip = read_all(a.lit_ref, W, H) if a.lit_ref else src
    sig = W / 30
    ref = cv2.GaussianBlur(ref_clip.astype(np.float32).mean(axis=0), (0, 0), sig) + 2.0
    del src, ref_clip

    # 2. ping-pong order
    order = list(range(n)) + list(range(n - 2, 0, -1))
    if a.period:  # resample the ping-pong to exactly --period frames (a 7.3 s float becomes 8.04 s)
        order = [order[int(k * len(order) / a.period)] for k in range(a.period)]

    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p']
    rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', a.base, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'],
                          stdout=subprocess.PIPE)
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', '24', '-i', '-', '-i', a.base, '-map', '0:v', '-map', '1:a?', '-c:a', 'copy']
                          + enc + [a.out], stdin=subprocess.PIPE)
    size = W * H * 3 * 2
    i = 0
    while True:
        buf = rd.stdout.read(size)
        if len(buf) < size:
            break
        base = np.frombuffer(buf, '<u2').reshape(H, W, 3).astype(np.float32) / 257.0
        gain = (cv2.GaussianBlur(base, (0, 0), sig) + 2.0) / ref
        layer = brk[order[(i + a.offset) % len(order)]].astype(np.float32) * np.clip(gain, 0, 1.5) * ramp * a.layer_gain
        out = base * (1 - mask) + layer * mask
        wr.stdin.write((np.clip(out, 0, 255) * 257).astype('<u2').tobytes())
        i += 1
    wr.stdin.close()
    wr.wait()
    rd.wait()
    print(f'{i} frames -> {a.out}')


if __name__ == '__main__':
    main()
