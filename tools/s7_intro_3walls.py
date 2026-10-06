"""The ship intro as ONE picture across the three walls, landing EXACTLY on the deck walls (route A, Homie 7 Oct).

  python tools/s7_intro_3walls.py CLIP_21x9.mp4 CANVAS.png WALLDIR OUT.mp4 [--ramp 2.5] [--xfade 0.5] [--hold 3]

1. The clip's LAST frame is registered to the deck canvas (ECC, affine; the v5 draft ended 2.3% zoomed in).
2. Over the last RAMP seconds that correction is eased in (smoothstep), so the camera's own settle carries it and the
   last frame sits on the canvas pixel for pixel.
3. Every frame is scaled to 4680 wide and the centred 4.33:1 band kept (LEFT 1440 | CENTRE 1800 | RIGHT 1440).
4. The last frame dissolves over XFADE s into the walls (WALLDIR/S7-SHIP-{LEFT,CENTRE,RIGHT}_1080.png), held HOLD s,
   or with --then IDLE.mp4 into the playing idle loop (its sound mixed in under the dissolve).
5. The clip's own sound rides through, padded under the hold (house rule). H.264 review file.
"""
import argparse
import json
import subprocess

import cv2
import numpy as np

OW, OH = 4680, 1080


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                            '-show_entries', 'stream=width,height,nb_read_frames', '-of', 'json', p]))
    s = j['streams'][0]
    return s['width'], s['height'], int(s['nb_read_frames'])


def frames(p, w, h):
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                          stdout=subprocess.PIPE)
    n = w * h * 3
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint8).reshape(h, w, 3)


def band(img):
    """the canvas's own band (rows 479..1559 of 2038), whatever the clip's size or aspect, resized to 4680x1080"""
    h = img.shape[0]
    y0, y1 = int(round(h * 479 / 2038)), int(round(h * 1559 / 2038))
    return cv2.resize(img[y0:y1], (OW, OH), interpolation=cv2.INTER_LANCZOS4)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('clip'); ap.add_argument('canvas'); ap.add_argument('walldir'); ap.add_argument('out')
    ap.add_argument('--ramp', type=float, default=2.5); ap.add_argument('--xfade', type=float, default=0.5)
    ap.add_argument('--hold', type=float, default=3.0)
    ap.add_argument('--then', help='an idle loop (4680x1080) to dissolve INTO and play for --hold s, instead of the still walls')
    a = ap.parse_args()
    w, h, n = probe(a.clip)
    last = None
    for f in frames(a.clip, w, h):
        last = f
    can = cv2.resize(cv2.imread(a.canvas), (w, h), interpolation=cv2.INTER_AREA)
    g1 = cv2.cvtColor(last, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g0 = cv2.cvtColor(can, cv2.COLOR_BGR2GRAY).astype(np.float32)
    M = np.eye(2, 3, dtype=np.float32)
    cc, M = cv2.findTransformECC(g0, g1, M, cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-7), None, 5)
    print(f'last frame -> canvas: ECC {cc:.4f}, M {np.round(M, 4).tolist()}')
    I = np.eye(2, 3, dtype=np.float32)
    nr = int(round(a.ramp * 24))
    walls = np.hstack([cv2.imread(f'{a.walldir}/S7-SHIP-{x}_1080.png') for x in ('LEFT', 'CENTRE', 'RIGHT')])
    dur = n / 24.0
    if a.then:      # the idle's sound comes in under the dissolve, mixed with the intro's tail
        ains = ['-i', a.clip, '-stream_loop', '-1', '-i', a.then]
        amap = ['-filter_complex', f'[1:a]aresample=48000,apad[x];[2:a]aresample=48000,adelay={int((dur - a.xfade) * 1000)}|{int((dur - a.xfade) * 1000)}[y];[x][y]amix=inputs=2:duration=first:normalize=0[a]',
                '-map', '0:v', '-map', '[a]']
    else:
        ains = ['-i', a.clip]; amap = ['-map', '0:v', '-map', '1:a?', '-af', 'aresample=48000,apad']
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{OW}x{OH}',
                            '-r', '24', '-i', '-'] + ains + amap + ['-shortest',
                            '-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p',
                            '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', a.out], stdin=subprocess.PIPE)
    lastb = None
    for i, f in enumerate(frames(a.clip, w, h)):
        k = i - (n - nr)
        if k >= 0:
            t = (k + 1) / nr
            s = t * t * (3 - 2 * t)
            Mt = I + s * (M - I)
            f = cv2.warpAffine(f, Mt, (w, h), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP,
                               borderMode=cv2.BORDER_REPLICATE)
        lastb = band(f)
        enc.stdin.write(lastb.tobytes())
    nx, nh = int(round(a.xfade * 24)), int(round(a.hold * 24))
    idle = list(frames(a.then, OW, OH)) if a.then else None
    for j in range(nx + nh):
        al = min(1.0, (j + 1) / max(1, nx))
        tgt = idle[j % len(idle)] if idle else walls
        enc.stdin.write(cv2.addWeighted(lastb, 1 - al, tgt, al, 0).tobytes())
    enc.stdin.close(); enc.wait()
    d = np.abs(lastb.astype(np.float32) - walls.astype(np.float32)).mean()
    print(f'wrote {a.out}: {n} clip frames + {nx} dissolve + {nh} hold; band vs walls at the join: MAD {d:.1f}')


if __name__ == '__main__':
    main()
