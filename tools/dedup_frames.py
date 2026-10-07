"""Remove a generator's repeated frames and re-space the motion evenly (9 Oct: S7-INTRO-LEADIN v4 at 1080p repeats one
frame every 23-24 frames, f7, 30, 54, … 217: a hitch every second).

  python tools/dedup_frames.py IN.mp4 OUT.mp4 [--thresh 0.2]

A frame whose mean difference from the previous one is under THRESH x the clip's median step is a repeat: it is dropped.
The remaining unique frames are put back on an even clock with the ORIGINAL frame count (so the duration and the sound are
unchanged): each output frame sits at a fractional position between two unique frames and is made by warping both toward
it along the DIS optical flow and blending. Positions that land on a unique frame use it untouched.
Writes H.264 crf 10 + the input's sound copied.
"""
import argparse
import json
import subprocess

import cv2
import numpy as np


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height', '-of', 'json', p]))
    return j['streams'][0]['width'], j['streams'][0]['height']


def frames(p, w, h):
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
    out = []
    while True:
        b = pr.stdout.read(w * h * 3)
        if len(b) < w * h * 3:
            break
        out.append(np.frombuffer(b, np.uint8).reshape(h, w, 3))
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('inp'); ap.add_argument('out')
    ap.add_argument('--thresh', type=float, default=0.2)
    a = ap.parse_args()
    w, h = probe(a.inp)
    F = frames(a.inp, w, h)
    n = len(F)
    small = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (w // 4, h // 4)).astype(np.float32) for f in F]
    d = np.array([np.abs(small[i] - small[i - 1]).mean() for i in range(1, n)])
    med = np.median(d)
    keep = [0] + [i for i in range(1, n) if d[i - 1] >= a.thresh * med]
    print(f'{n} frames, median step {med:.1f}; repeats dropped: {[i for i in range(1, n) if i not in keep]}')
    U = [F[i] for i in keep]
    m = len(U)
    gray = [cv2.cvtColor(u, cv2.COLOR_BGR2GRAY) for u in U]
    dis = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '24',
                            '-i', '-', '-i', a.inp, '-map', '0:v', '-map', '1:a?', '-c:v', 'libx264', '-crf', '10',
                            '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'copy', a.out], stdin=subprocess.PIPE)
    cache = {}
    for k in range(n):
        x = k * (m - 1) / (n - 1)
        i = int(np.floor(x)); f = x - i
        if f < 1e-3 or i >= m - 1:
            fr = U[min(i, m - 1)]
        else:
            if i not in cache:
                cache.clear()
                cache[i] = (dis.calc(gray[i], gray[i + 1], None), dis.calc(gray[i + 1], gray[i], None))
            fw, bw = cache[i]
            # pixel p at time f: sample frame i at p - f*fw, frame i+1 at p - (1-f)*bw
            a0 = cv2.remap(U[i], gx - f * fw[..., 0], gy - f * fw[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
            a1 = cv2.remap(U[i + 1], gx - (1 - f) * bw[..., 0], gy - (1 - f) * bw[..., 1], cv2.INTER_LINEAR,
                           borderMode=cv2.BORDER_REPLICATE)
            fr = cv2.addWeighted(a0, 1 - f, a1, f, 0)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
    enc.stdin.close(); enc.wait()
    print(f'{a.out}: {m} unique frames re-spaced over {n}')


if __name__ == '__main__':
    main()
