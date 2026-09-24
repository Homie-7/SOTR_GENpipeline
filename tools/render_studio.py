"""Render a studio beat: the approved candle loop with The Raft of the Medusa on the canvas,
at the stage the script calls for, growing while Géricault paints.

Built 2026-09-24 from LOOK.md D4 (Claude, delegated by Homie). The script says the painting is
"half-completed" at beat 4; it grows through beat 6 and is complete at beat 9, the waving
figure at the apex painted LAST.

LIGHT. The canvas is blank primed cloth, so its pixels ARE the light: light = canvas pixel /
the primer's colour at full light (99th percentile of the canvas on the reference frame). The
painting's colours are multiplied by it, so the candle pool, its flicker and its falloff fall
across the Raft for real, and the canvas weave (fine detail of the blank canvas) stays on top.

UNPAINTED AREAS show how Géricault worked: the composition outlined in umber on the primer.
The outline is drawn from the painting's own contours (a difference of Gaussians).

PAINT ORDER (a map over the painting, 0 = first): the lower band (the dead and dying, the raft,
the sea) -> the heap of bodies and the sail -> the sky -> the apex figure last, with brush-
stroke-shaped frontiers. Stage cut-offs: beat 4 = 0.45, beat 6 = 0.80, beat 9 = 1.06 (the apex sits up to 1.01).
Within a beat the painting grows from --stage-from to --stage-to over --grow seconds.

  python tools/render_studio.py OUT.mov LOOP [LOOP ...] --stage-from 0.36 --stage-to 0.45
         [--grow 20] [--tail-hold 0]

Finished clean renders go to SOTR_MEDIA/01_FINAL_FOR_SHOW/LEFT_wall_STUDIO/ and are never overwritten (same rules as
render_wall.py). Needs ffmpeg, numpy, Pillow, OpenCV.
"""
import argparse
import os
import sys

import cv2
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
from render_wall import blur, frames, nb_frames, size, smoothstep, value_noise  # noqa: E402

RAFT = os.path.join(os.path.dirname(__file__), '..', '..', 'SOTR_MEDIA', 'comp', 'Raft_of_the_Medusa_Gericault_WGA08630.jpg')
# canvas corners in the approved studio plate/loop (1664x1248), measured 2026-09-24: TL TR BR BL
QUAD = np.float32([[248, 229], [1503, 229], [1525, 1248], [231, 1248]])
CROP_X = (0.075, 0.925)  # the visible canvas is squarer (1.25:1) than the Raft (1.47:1)
UMBER = np.array([0.30, 0.19, 0.11], np.float32)


def paint_order(h, w, rng):
    y, x = np.mgrid[0:h, 0:w].astype(np.float32)
    xn, yn = x / w * (CROP_X[1] - CROP_X[0]) + CROP_X[0], y / h  # coords in the FULL painting
    p = 0.04 + 0.9 * (1 - yn) ** 1.05                          # bottom first, top last
    sail = ((xn > 0.12) & (xn < 0.5) & (yn < 0.62)).astype(np.float32)
    p = p * (1 - 0.25 * blur(sail, 25))                         # the mast and sail with the bodies
    apex = np.exp(-(((xn - 0.715) / 0.06) ** 2 + ((yn - 0.24) / 0.13) ** 2))
    p = np.where(apex > 0.35, 0.96 + 0.05 * apex, np.minimum(p, 0.95))  # the apex figure last
    # brush-stroke frontier: noise smeared along a diagonal stroke direction
    n = value_noise(h, w, 18, rng) - 0.5
    k = np.zeros((31, 31), np.float32)
    cv2.line(k, (0, 22), (30, 8), 1.0, 2)
    n = cv2.filter2D(n, -1, k / k.sum())
    n = n / (np.abs(n).max() + 1e-6)
    return np.clip(p + 0.07 * n, 0, 1.2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--stage-from', type=float, required=True)
    ap.add_argument('--stage-to', type=float, required=True)
    ap.add_argument('--grow', type=float, default=20.0, help='seconds for the painting to grow')
    ap.add_argument('--tail-hold', type=float, default=0)
    ap.add_argument('--overwrite', action='store_true')
    a = ap.parse_args()
    if os.path.exists(a.out) and not a.overwrite:
        raise SystemExit(f'refusing: {a.out} exists. Clean renders are never replaced; give the new one a new version')

    W, H = size(a.inputs[0])
    rng = np.random.default_rng(1819)
    raft = Image.open(RAFT).convert('RGB')
    cw = int(round(np.linalg.norm(QUAD[1] - QUAD[0]) + np.linalg.norm(QUAD[2] - QUAD[3])) / 2)
    ch = int(round(np.linalg.norm(QUAD[3] - QUAD[0]) + np.linalg.norm(QUAD[2] - QUAD[1])) / 2)
    x0, x1 = int(raft.width * CROP_X[0]), int(raft.width * CROP_X[1])
    raft = np.asarray(raft.crop((x0, 0, x1, raft.height)).resize((cw, ch), Image.LANCZOS)).astype(np.float32) / 255
    gray = cv2.cvtColor(raft, cv2.COLOR_RGB2GRAY)
    dog = cv2.GaussianBlur(gray, (0, 0), 1.2) - cv2.GaussianBlur(gray, (0, 0), 3.5)
    lines = np.clip(-dog * 9, 0, 1) ** 0.8                     # dark contours -> umber strokes
    order = paint_order(ch, cw, rng)

    M = cv2.getPerspectiveTransform(np.float32([[0, 0], [cw, 0], [cw, ch], [0, ch]]), QUAD)
    warp = lambda img: cv2.warpPerspective(img, M, (W, H), flags=cv2.INTER_LINEAR)
    raft_f, lines_f = warp(raft), warp(lines)[..., None]
    order_f = warp(order)
    cmask = warp(np.ones((ch, cw), np.float32))
    cmask = cv2.erode(cmask, np.ones((3, 3), np.uint8))[..., None]  # stay 1 px inside the canvas edge

    first = next(frames(a.inputs[0], W, H))
    inside = cmask[..., 0] > 0.99
    primer = np.percentile(first[inside], 99, axis=0).astype(np.float32)

    import subprocess
    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w_ = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', '24', '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)
    tail = round(a.tail_hold * 24)

    def source():
        last = None
        for p in a.inputs:
            for f in frames(p, W, H):
                last = f
                yield f.copy()
        for _ in range(tail):
            yield last.copy()

    n = 0
    for f in source():
        t = n / 24
        k = smoothstep(0, 1, min(t / max(a.grow, 1e-3), 1.0))
        thr = a.stage_from + (a.stage_to - a.stage_from) * k
        alpha = smoothstep(thr + 0.012, thr - 0.012, order_f)[..., None]  # painted where order < thr
        soft = cv2.GaussianBlur(f, (0, 0), 2.0)
        light = soft / primer
        weave = np.clip(f / (soft + 1e-4), 0.85, 1.15)                    # canvas texture on top
        painted = raft_f * light * weave
        drawn = f * (1 - 0.75 * lines_f) + UMBER * light * 0.75 * lines_f
        canvas = painted * alpha + drawn * (1 - alpha)
        f = f * (1 - cmask) + canvas * cmask
        w_.stdin.write((np.clip(f, 0, 1) * 65535).astype('<u2').tobytes())
        n += 1
    w_.stdin.close()
    w_.wait()
    print(f'{n} frames -> {a.out} (stage {a.stage_from:.2f} -> {a.stage_to:.2f} over {a.grow:.0f} s)')


if __name__ == '__main__':
    main()
