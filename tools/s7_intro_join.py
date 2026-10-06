"""Join the intro's generated parts into ONE 21:9 clip and retime it with smooth speed ramps (9 Oct, intro v6.1 / v7).

  python tools/s7_intro_join.py OUT.mp4 PART1.mp4 [PART2.mp4 ...] [--ramp A B PEAK EASE]...

PARTS are butted in order (LEADIN = the flight, a backward video_extension, ends exactly where the reversed REV begins;
REV_REVERSED ends exactly on the deck canvas). Times in --ramp are on the JOINED timeline, in seconds.
--ramp A B PEAK EASE: between A and B the speed eases up from 1 to PEAK over EASE s (smoothstep), holds, and eases back
   to 1 over the last EASE s. Homie 9 Oct on v6: "the camera pauses too long on the side rail instead of coming up" and
   "the ship changes its shape… a flicker" (v6 7.6-8.3 s, while the gull crosses the lens): one ramp over both.
PICTURE: each output frame averages the source frames its 180-degree shutter would have seen on the new clock (speed 1 =
   the frame itself; faster = real-looking motion blur, no judder from skipped frames).
SOUND (house rule: it rides in every file): granular overlap-add on the same clock, 80 ms Hann grains at 50% overlap,
   each grain read at normal rate from the source time it belongs to: the ambience keeps its pitch while it speeds up.
Writes H.264 crf 10 + AAC 256k (the input for tools/s7_intro_3walls.py) and prints the durations.
"""
import argparse
import json
import os
import subprocess

import numpy as np

FPS = 24.0
SR = 48000


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                            '-show_entries', 'stream=width,height,nb_read_frames', '-of', 'json', p]))
    s = j['streams'][0]
    return s['width'], s['height'], int(s['nb_read_frames'])


def frames(p, w, h):
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def audio(p, n_samples):
    try:
        b = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'])
        a = np.frombuffer(b, np.float32).reshape(-1, 2)
    except subprocess.CalledProcessError:
        a = np.zeros((0, 2), np.float32)
    a = a[:n_samples]
    return np.pad(a, ((0, n_samples - len(a)), (0, 0))) if len(a) < n_samples else a


def speed(t, ramps):
    v = np.ones_like(t)
    for A, B, P, E in ramps:
        u = np.clip(np.minimum(t - A, B - t) / E, 0, 1)
        v = np.maximum(v, 1 + (P - 1) * u * u * (3 - 2 * u))
    return v


def clock(dur, ramps):
    """output time -> source time"""
    t = np.arange(0, dur, 1 / 4800.0)
    tout = np.concatenate([[0], np.cumsum(1 / speed(t[:-1], ramps)) / 4800.0])
    return lambda x: np.interp(x, tout, t), tout[-1], (tout, t)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out'); ap.add_argument('parts', nargs='+')
    ap.add_argument('--ramp', type=float, nargs=4, action='append', default=[], metavar=('A', 'B', 'PEAK', 'EASE'))
    a = ap.parse_args()
    sizes = [probe(p) for p in a.parts]
    w, h = sizes[0][:2]
    assert all(s[:2] == (w, h) for s in sizes), 'the parts must be the same size'
    F = []
    for p in a.parts:
        F.extend(frames(p, w, h))
    n = len(F)
    dur = n / FPS
    src, dur_out, _ = clock(dur, a.ramp)
    n_out = int(np.floor(dur_out * FPS))
    # sound: the parts butted, then granular OLA on the new clock
    A = np.concatenate([audio(p, int(round(s[2] / FPS * SR))) for p, s in zip(a.parts, sizes)])
    L = int(0.08 * SR); H = L // 2
    win = np.hanning(L).astype(np.float32)[:, None]
    n_samp = int(round(n_out / FPS * SR))
    out_a = np.zeros((n_samp + L, 2), np.float32); norm = np.zeros((n_samp + L, 1), np.float32)
    for k in range(0, n_samp, H):
        s0 = int(round(float(src(k / SR)) * SR))
        g = A[s0:s0 + L]
        if len(g) < L:
            g = np.pad(g, ((0, L - len(g)), (0, 0)))
        out_a[k:k + L] += g * win; norm[k:k + L] += win
    out_a = (out_a / np.maximum(norm, 1e-3))[:n_samp]
    wav = a.out + '._tmp_audio.f32'
    out_a.astype(np.float32).tofile(wav)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{w}x{h}', '-r', '24',
                            '-i', '-', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', wav, '-map', '0:v', '-map', '1:a',
                            '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '256k', '-shortest', a.out], stdin=subprocess.PIPE)
    for k in range(n_out):
        t0, t1 = float(src((k - 0.25) / FPS)), float(src((k + 0.25) / FPS))     # the 180-degree shutter, in source time
        c = float(src(k / FPS)) * FPS
        if (t1 - t0) * FPS <= 1.0:                                              # ~speed 1: one frame (or a 2-frame lerp)
            i = min(int(np.floor(c)), n - 1); j = min(i + 1, n - 1); f = c - i
            fr = F[i] if f < 1e-3 else (F[i] * (1 - f) + F[j] * f + 0.5).astype(np.uint8)
        else:
            i0, i1 = max(0, int(np.floor(t0 * FPS))), min(n - 1, int(np.ceil(t1 * FPS)))
            fr = (np.mean([F[i].astype(np.float32) for i in range(i0, i1 + 1)], 0) + 0.5).astype(np.uint8)
        enc.stdin.write(np.ascontiguousarray(fr).tobytes())
    enc.stdin.close(); enc.wait()
    os.remove(wav)
    print(f'{a.out}: {n} frames ({dur:.2f} s) -> {n_out} frames ({n_out / FPS:.2f} s); ramps {a.ramp}')


if __name__ == '__main__':
    main()
