"""Light-arc preview from the ship's IDLE LOOPS (day -> magic hour -> sunset -> night), all three walls.

Every idle loop is 157 frames with the SAME horizon motion (tools/s7_idle.py), so the skies are crossfaded at the SAME loop
phase: the deck and the horizon never jump; only the light changes. Sound crossfaded the same way.

  python tools/s7_idle_arc.py OUT.mp4 [--hold 10] [--xfade 3] [--width 2340]
"""
import argparse
import subprocess

import cv2
import numpy as np

D = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/8_idle/'
STATES = ('day', 'magic', 'sunset', 'night')


def load(st, W, H):
    p = D + f'{st}/S7-SHIP-IDLE_{st}_3walls_LOOP.mp4'
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                          stdout=subprocess.PIPE)
    fr = []
    while True:
        b = pr.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        fr.append(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    au = np.frombuffer(subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '2', '-ar', '48000', '-f', 'f32le', '-']),
                       np.float32).reshape(-1, 2)
    return fr, au


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('--hold', type=float, default=10)
    ap.add_argument('--xfade', type=float, default=3); ap.add_argument('--width', type=int, default=2340)
    a = ap.parse_args()
    W = a.width; H = int(round(W * 1080 / 4680 / 2)) * 2
    L = [load(s, W, H) for s in STATES]
    n = len(L[0][0]); assert all(len(x[0]) == n for x in L), 'loops differ in length'
    seg = a.hold + a.xfade
    total = a.hold * len(STATES) + a.xfade * (len(STATES) - 1)
    N = int(round(total * 24))

    def weights(t):
        w = np.zeros(len(STATES))
        k = min(int(t // seg), len(STATES) - 1); r = t - k * seg
        if r < a.hold or k == len(STATES) - 1:
            w[k] = 1
        else:
            s = (r - a.hold) / a.xfade; s = s * s * (3 - 2 * s); w[k] = 1 - s; w[k + 1] = s
        return w

    # audio first (to a temp file), then the picture
    sr = 48000; A = int(round(total * sr)); la = len(L[0][1])
    au = np.zeros((A, 2), np.float32)
    for j in range(0, A, 480):
        w = weights(j / sr)
        for k, (_, x) in enumerate(L):
            if w[k]:
                idx = (np.arange(j, min(j + 480, A)) % la)
                au[j:j + len(idx)] += w[k] * x[idx]
    tmp = a.out + '.f32'; au.tofile(tmp)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
                            '-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', tmp, '-c:v', 'libx264', '-crf', '17', '-preset', 'medium',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '256k', '-shortest', '-movflags', '+faststart', a.out],
                           stdin=subprocess.PIPE)
    for i in range(N):
        w = weights(i / 24); p = i % n
        f = sum(w[k] * L[k][0][p].astype(np.float32) for k in range(len(STATES)) if w[k])
        enc.stdin.write(np.clip(f, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    import os; os.remove(tmp)
    print(f'wrote {a.out}: {total:.1f} s, {W}x{H}, states {STATES}, hold {a.hold}s, xfade {a.xfade}s at the same loop phase')


if __name__ == '__main__':
    main()
