"""Turn a generated ambient clip into a clean, seamless loop, optionally boosting its light flicker.

Built 2026-09-24 for S9-SAL-R-LOOP. Homie approved "B" (boost 3) from the preview this reproduces.

What it does, in order:
  1. Drops the first frames (Seedance's frame 0 is the reference image itself, cleaner than
     the rest).
  2. Cancels slow drift: a per-pixel linear brightness trend across the clip (the salon dimmed
     about 3% over 10 s), measured on heavily blurred luminance so grain doesn't count.
  3. Boosts the fast, large-scale light change (the halo breathing) by --boost. Only the
     blurred component is amplified, so flames keep their shape and grain isn't amplified.
  4. Crossfade loop: the tail blends into the head over --xfade frames, so the output cycles
     seamlessly.

Needs ffmpeg on PATH, numpy and Pillow.

  python tools/loop_halo.py IN.mp4 OUT.mov --boost 3 --skip 12 --xfade 36
  python tools/loop_halo.py IN.mp4 PREVIEW.mp4 --boost 3 --cycles 3     # H.264 preview

.mov output is ProRes 422 HQ, 10-bit, for the comp. Anything else is H.264 8-bit, for preview.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image


def probe(path):
    out = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                                   '-show_entries', 'stream=width,height,nb_frames',
                                   '-of', 'json', path])
    s = json.loads(out)['streams'][0]
    return int(s['width']), int(s['height']), int(s['nb_frames'])


def read_frames(path, w, h, fmt, dtype, chans):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'scale={w}:{h}',
                          '-f', 'rawvideo', '-pix_fmt', fmt, '-'], stdout=subprocess.PIPE)
    size = w * h * chans * np.dtype(dtype).itemsize
    try:
        while True:
            buf = p.stdout.read(size)
            if len(buf) < size:
                break
            yield np.frombuffer(buf, dtype).reshape(h, w, chans) if chans > 1 else np.frombuffer(buf, dtype).reshape(h, w)
    finally:
        p.kill()
        p.wait()


def box(a, r):
    for ax in (0, 1):
        pad = [(r + 1, r) if i == ax else (0, 0) for i in (0, 1)]
        c = np.cumsum(np.pad(a, pad, mode='edge'), axis=ax)
        n = c.shape[ax]
        a = (np.take(c, range(2 * r + 1, n), axis=ax) - np.take(c, range(0, n - 2 * r - 1), axis=ax)) / (2 * r + 1)
    return a


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('out')
    ap.add_argument('--boost', type=float, default=1.0, help='multiplier on the fast light flicker (1 = as generated)')
    ap.add_argument('--skip', type=int, default=12, help='frames dropped from the head')
    ap.add_argument('--xfade', type=int, default=36, help='crossfade length in frames')
    ap.add_argument('--cycles', type=int, default=1, help='how many loop cycles to write (1 for the comp)')
    ap.add_argument('--no-detrend', action='store_true')
    a = ap.parse_args()

    W, H, _ = probe(a.src)
    qw, qh = W // 4, H // 4

    # Analysis pass, at quarter resolution: blurred luminance per frame.
    B = np.stack([box(box(f.astype(np.float32), 5), 5)
                  for f in read_frames(a.src, qw, qh, 'gray16le', '<u2', 1)])[a.skip:]
    n = B.shape[0]
    t = np.arange(n, dtype=np.float32)
    tm = t.mean()
    if a.no_detrend:
        gain = np.ones_like(B)
    else:
        slope = ((B - B.mean(0)) * (t - tm)[:, None, None]).sum(0) / ((t - tm) ** 2).sum()
        gain = B.mean(0)[None] / (B.mean(0)[None] + slope[None] * (t - tm)[:, None, None])
    Bd = B * gain
    D = (Bd - Bd.mean(0)) / Bd.mean(0)
    G = gain * (1 + (a.boost - 1) * D)   # final per-pixel gain map per frame

    def up(g):
        return np.asarray(Image.fromarray(g.astype(np.float32), 'F').resize((W, H), Image.BILINEAR))

    # Render pass, at full resolution and 16 bits per channel. Streamed: only the head frames
    # the crossfade blends into are held in memory.
    X = a.xfade
    m = n - X
    head = []
    for i, f in enumerate(read_frames(a.src, W, H, 'rgb48le', '<u2', 3)):
        if i >= a.skip + X:
            break
        if i >= a.skip:
            head.append(f)
    if a.out.lower().endswith('.mov'):
        enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le']
    else:
        enc = ['-c:v', 'libx264', '-crf', '16', '-pix_fmt', 'yuv420p']
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le',
                          '-s', f'{W}x{H}', '-r', '24', '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)

    def lit(raw, i):
        return raw.astype(np.float32) * up(G[i])[..., None]

    for _ in range(a.cycles):
        body = read_frames(a.src, W, H, 'rgb48le', '<u2', 3)
        for _ in range(a.skip + X):
            next(body)
        for k, raw in enumerate(body):
            if k >= m:
                break
            f = lit(raw, X + k)
            if k >= m - X:
                j = k - (m - X)
                w = (j + 1) / (X + 1)
                f = f * (1 - w) + lit(head[j], j) * w
            p.stdin.write(np.clip(f, 0, 65535).astype('<u2').tobytes())
        body.close()
    p.stdin.close()
    p.wait()
    print(f'{a.out}: {m} frames per cycle ({m / 24:.2f} s) x {a.cycles}')


if __name__ == '__main__':
    main()
