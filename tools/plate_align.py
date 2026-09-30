"""Put a generated take back on the APPROVED plate's geometry: warp it to the approved framing, and replace the
bottom band (where the take shows floor) with the approved plate, relit column by column from the take.

WHY (2026-10-01, the studio candle arc v4): the 10 s (B6) and 30 s (B9) candle takes came back reframed. The canvas
stops ~37-40 px above the frame bottom with a strip of FLOOR below it (STAGE: no floor, ever), and B6 is ~2.5% smaller
than the approved framing. The 4 s probes were framed right, and they were what the "no floor" check measured.
render_studio.py paints the Raft on the APPROVED canvas position, so a reframed take also doubles the canvas's bottom
edge under the painting. A regeneration can't be trusted to hold framing at length; this fixes it for 0 credits.

  python tools/plate_align.py TAKE.mov APPROVED_LOOP OUT.mov [--band-pad 30 --feather 24]

1. The warp: one uniform zoom + shift, TAKE -> approved framing, from the CANVAS EDGES of the two clips' mean frames
   (left and right edge -> scale, left and top edge -> shift). The framing is constant through a take (ECC per frame:
   within 0.03% over B6's 240 frames and B9's 720). ECC on the whole mean frame was tried first and missed B6's 2.5%
   width change (the plaster texture outvoted the edges), so the edges are measured directly: they are what must line
   up with render_studio.py's painting.
2. The band: the warped take's lowest strong horizontal edge (the canvas foot, in the canvas columns) minus --band-pad
   is where the approved plate takes over, with a --feather row ramp above it. The plate = the approved loop's mean
   frame (its geometry is right), multiplied per column and per frame by the take's light in a strip just above
   the band (smoothed along x), so the candle's flicker carries on down to the bottom edge.
Everything above the band is the take's own pixels (warped). 10-bit in and out, ProRes 422 HQ q2, the take's sound.
"""
import argparse
import json
import subprocess

import cv2
import numpy as np


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                            '-show_entries', 'stream=width,height,nb_read_frames,r_frame_rate',
                                            '-of', 'json', p]))['streams'][0]
    return int(j['width']), int(j['height']), int(j['nb_read_frames']), j['r_frame_rate']


def reader(p, w, h):
    cmd = ['ffmpeg', '-v', 'error', '-i', p, '-vf', f'scale={w}:{h}:flags=bicubic', '-f', 'rawvideo',
           '-pix_fmt', 'rgb48le', '-']
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    n = w * h * 3 * 2
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint16).reshape(h, w, 3).astype(np.float32) / 65535
    pr.wait()


def mean_frame(p, w, h):
    acc, n = None, 0
    for f in reader(p, w, h):
        acc = f.copy() if acc is None else acc + f
        n += 1
    return acc / n


def canvas_edges(f):
    """left, right, top edge of the bright canvas (px), from smoothed row/column profiles of a mean frame."""
    g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY)
    h, w = g.shape
    col = np.diff(cv2.GaussianBlur(g[int(h * .25):int(h * .72)].mean(0).reshape(1, -1), (1, 9), 0).ravel())
    row = np.diff(cv2.GaussianBlur(g[:, int(w * .3):int(w * .72)].mean(1).reshape(-1, 1), (9, 1), 0).ravel())
    return int(np.argmax(col[:int(w * .42)])), int(w * .54) + int(np.argmin(col[int(w * .54):])), int(np.argmax(row[:int(h * .32)]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('approved')
    ap.add_argument('out')
    ap.add_argument('--band-pad', type=int, default=30, help='rows above the take\'s canvas foot where the plate starts')
    ap.add_argument('--feather', type=int, default=24, help='rows of blend above the band')
    ap.add_argument('--strip', type=int, default=40, help='rows above the feather that sample the take\'s light')
    a = ap.parse_args()
    w, h, n, rate = probe(a.take)
    P = mean_frame(a.approved, w, h)
    T = mean_frame(a.take, w, h)
    (Lr, Rr, Tr), (Lt, Rt, Tt) = canvas_edges(P), canvas_edges(T)
    sc = (Rt - Lt) / (Rr - Lr)
    W = np.float32([[sc, 0, Lt - sc * Lr], [0, sc, Tt - sc * Tr]])  # approved coords -> take coords
    print('canvas edges L/R/top: approved %d/%d/%d, take %d/%d/%d' % (Lr, Rr, Tr, Lt, Rt, Tt))
    warp = lambda f: cv2.warpAffine(f, W, (w, h), flags=cv2.INTER_CUBIC | cv2.WARP_INVERSE_MAP, borderMode=cv2.BORDER_REFLECT)
    Tw = warp(T)
    # the canvas foot in the warped take: strongest row step in the lowest 12% (canvas columns = middle 60%)
    y0 = int(h * 0.88)
    rows = cv2.cvtColor(Tw, cv2.COLOR_RGB2GRAY)[y0:, int(w * 0.2):int(w * 0.8)].mean(1)
    foot = y0 + int(np.argmax(np.abs(np.diff(rows))))
    b0 = foot - a.band_pad
    f0 = b0 - a.feather
    s0 = f0 - a.strip
    print('warp: scale %.4f %.4f  shift %.1f %.1f px;  canvas foot at row %d -> plate from row %d (feather %d-%d, light strip %d-%d)'
          % (np.hypot(W[0, 0], W[1, 0]), np.hypot(W[0, 1], W[1, 1]), W[0, 2], W[1, 2], foot, b0, f0, b0, s0, f0))
    ramp = np.zeros((h, 1, 1), np.float32)
    ramp[f0:b0, 0, 0] = np.linspace(0, 1, b0 - f0, endpoint=False)
    ramp[b0:] = 1
    Pref = P[s0:f0].mean(0)  # per column, per channel: the plate's light in the sampling strip
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{w}x{h}',
                            '-r', rate, '-i', '-', '-i', a.take, '-map', '0:v', '-map', '1:a?', '-c:v', 'prores_ks',
                            '-qscale:v', '2', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-c:a', 'copy',
                            '-shortest', a.out], stdin=subprocess.PIPE)
    k = 0
    for f in reader(a.take, w, h):
        fw = warp(f)
        g = fw[s0:f0].mean(0) / np.maximum(Pref, 1e-4)             # the take's light relative to the plate, per column
        g = cv2.GaussianBlur(g[None], (0, 0), sigmaX=25, sigmaY=0)[0]  # smooth along x (no column stripes)
        band = P * g[None]
        o = fw * (1 - ramp) + band * ramp
        enc.stdin.write((np.clip(o, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
        k += 1
    enc.stdin.close()
    enc.wait()
    print('wrote', a.out, f'({w}x{h}, {k} of {n} frames)')


if __name__ == '__main__':
    main()
