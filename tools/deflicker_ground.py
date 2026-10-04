"""Take the render flicker out of the GROUND of a locked-camera Unreal render (Scene 5 camps Front, Homie 2026-10-04:
"the flickering on the ground in front video is still there, is there no way to fix it?").

WHAT FLICKERS (measured 2026-10-04 on New Renders/Camps/Front, i.e. already in Unreal's render, not the grade):
  - rectangular ground patches that drift, then JUMP by up to ~15/255 in one frame (shadow tiles popping);
  - the foreground campfire's light pool: per-pixel speckle every frame (render noise in the fire's light).
The camera is locked and the ground does not move, so each ground pixel is averaged over time with a TRIANGULAR window
of 25 frames (1 s at 25 fps; two 13-frame running means): a pop becomes a ~1 s fade, the speckle averages out, and the
fire light's slower swells stay. NOT touched: the sky (the sky mask), a band just below the horizon and the horizon
fires with their plumes (fire placement blobs, grown), and every FLAME (flame_zone: where it is flame-bright in a
quarter of the clip, grown). Sparks that leave a flame zone are averaged away (tiny, and part of the flicker). Everything else is the input through a 16-bit path; ProRes 422 HQ 10-bit q2, the
input's sound stream-copied, written to a _tmp_ name and renamed.

  python tools/deflicker_ground.py IN.mov OUT.mov SKYMASK.png FIREPLACEMENT.png [--frames N]
"""
import os
import subprocess
import sys
from collections import deque

import cv2
import numpy as np

B = 13                 # each running mean is 13 frames; two in a row = a 25-frame triangle (1 s at 25 fps)
HORIZON_PAD = 30       # px below the sky mask that stay untouched (the plumes' feet, the horizon fires)
BIG_FIRE = 20000       # a fire-placement blob bigger than this is a lit area (the foreground pool), not a flame: smoothed


def flame_zone(src, W, H, N):
    """Where a flame IS, not where the firelight falls: one frame a second over the clip; a pixel that is flame-bright
    (luma > 0.93, saturated) in at least a quarter of them is a flame (the lit ground's hot speckle jumps around, so it
    rarely is); grown 21 px. Measured 2026-10-04: the Front's foreground pool is lit to p90 luma 0.82, p99 0.96, so a
    per-frame brightness test cannot tell the flame from the ground it lights."""
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-frames:v', str(N), '-vf', 'select=not(mod(n\\,25))',
                           '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    cnt, k = np.zeros((H, W), np.float32), 0
    while True:
        b = pr.stdout.read(W * H * 3)
        if len(b) < W * H * 3:
            break
        f = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
        lum = f @ np.array([0.299, 0.587, 0.114], np.float32)
        sat = (f.max(-1) - f.min(-1)) / np.maximum(f.max(-1), 1e-6)
        cnt += (lum > 0.93) & (sat > 0.35)
        k += 1
    pr.wait()
    z = (cnt >= 0.25 * max(k, 1)).astype(np.uint8)
    return cv2.dilate(z, np.ones((43, 43), np.uint8)), k


def probe(p):
    o = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=width,height,r_frame_rate,nb_frames', '-of', 'csv=p=0', p]).decode().strip().split(',')
    return int(o[0]), int(o[1]), o[2], int(o[3])


def main():
    src, out, skyp, firep = sys.argv[1:5]
    a = sys.argv[5:]
    nmax = int(a[a.index('--frames') + 1]) if '--frames' in a else None
    W, H, fps, nf = probe(src)
    N = min(nf, nmax) if nmax else nf

    sky = cv2.resize(cv2.imread(skyp, 0), (W, H)) > 90
    below = cv2.dilate(sky.astype(np.uint8), np.ones((2 * HORIZON_PAD + 1, 1), np.uint8)) > 0     # sky + a band under it
    fire = (cv2.resize(cv2.imread(firep, 0), (W, H)) > 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fire, 8)
    small = np.isin(lab, [c for c in range(1, n) if st[c, cv2.CC_STAT_AREA] <= BIG_FIRE]).astype(np.uint8)
    keep = below | (cv2.dilate(small, np.ones((81, 81), np.uint8)) > 0)                         # horizon fires + plumes
    fz, ns = flame_zone(src, W, H, N)
    keep |= fz > 0
    print(f'{os.path.basename(out)}: flame zones {int(fz.sum())} px from {ns} samples', flush=True)
    ground = cv2.GaussianBlur((~keep).astype(np.float32), (0, 0), 12)
    rows = np.nonzero(ground.max(1) > 0.001)[0]
    y0 = int(rows.min())
    g_w = ground[y0:][..., None]
    print(f'{os.path.basename(out)}: smoothing rows {y0}-{H} ({g_w.mean() * 100:.0f}% of them), {N} frames', flush=True)

    rp = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-frames:v', str(N), '-f', 'rawvideo', '-pix_fmt',
                           'rgb48le', '-'], stdout=subprocess.PIPE)
    tmp = os.path.join(os.path.dirname(out) or '.', '_tmp_' + os.path.basename(out))
    wr = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}', '-r', fps, '-i', '-']
    if nmax is None:
        wr += ['-i', src, '-map', '0:v', '-map', '1:a?', '-c:a', 'copy']
    wr += ['-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-pix_fmt', 'yuv422p10le', '-vendor', 'apl0', tmp]
    wp = subprocess.Popen(wr, stdin=subprocess.PIPE)

    fb = W * H * 6

    def frames():
        first = last = None
        k = 0
        while k < N:
            b = rp.stdout.read(fb)
            if len(b) < fb:
                break
            f = np.frombuffer(b, np.uint16).reshape(H, W, 3)
            if first is None:
                first = f
                for _ in range(B - 1):                    # pad the start (2 x 6 frames) with frame 0
                    yield f
            last = f
            k += 1
            yield f
        for _ in range(B - 1):                            # and the end with the last frame
            yield last

    X, Y, F = deque(), deque(), deque()
    S1 = np.zeros((H - y0, W, 3), np.float64)
    S2 = np.zeros_like(S1)
    written = 0
    for f in frames():
        F.append(f)
        if len(F) > B:
            F.popleft()
        x = f[y0:].astype(np.float64)
        X.append(x)
        S1 += x
        if len(X) > B:
            S1 -= X.popleft()
        if len(X) < B:
            continue
        b1 = S1 / B
        Y.append(b1)
        S2 += b1
        if len(Y) > B:
            S2 -= Y.popleft()
        if len(Y) < B:
            continue
        o = F[0]                                          # the original of the frame now centred in both windows
        sm = S2 / B
        og = o[y0:].astype(np.float32)
        w = g_w
        res = o.copy()
        res[y0:] = np.clip(og * (1 - w) + sm.astype(np.float32) * w + 0.5, 0, 65535).astype(np.uint16)
        wp.stdin.write(res.tobytes())
        written += 1
        if written % 1500 == 0:
            print(f'{os.path.basename(out)}: {written} frames', flush=True)
        if written >= N:
            break
    rp.stdout.close()
    rp.terminate()
    wp.stdin.close()
    if wp.wait() != 0 or written != N:
        sys.exit(f'failed: wrote {written} of {N}')
    os.replace(tmp, out)
    print(f'{os.path.basename(out)}: wrote {written} frames', flush=True)


if __name__ == '__main__':
    main()
