"""S5 cannonball: key the generated green-screen element into a free 1080p alpha overlay + reviews.

Usage
    python tools/cannon_alpha.py                 # KEY (refuses if the .mov exists) + REVIEW
    python tools/cannon_alpha.py --review-only   # reviews from the existing KEY .mov
    python tools/cannon_alpha.py --test DIR      # tuning stills only (keyed frames over red), no media written
    options: --seed N (review moments, default 5), --n 3

Context (Homie F41): the cannonball is a FREE alpha overlay the operator fires at ANY moment over the
camps wall file. No timecode, nothing baked into the camps picture. 0 credits: script only.

Method
  1. Decode the source (854x480, 24 fps) as RGB float.
  2. Key: d = G - max(R, B). alpha = 1 - smoothstep(KEY_LO, KEY_HI, d). The green screen gives d ~108
     (bright) and falls with the backdrop as it darkens 5.0-6.5 s (d 50 -> 34 -> 16 -> 4); smoke and
     embers give d < 0. So the dark backdrop fills in to OPAQUE black smoothly (intended: the cover
     darkens to black). A 1 px spatial blur softens h264 blocks in the matte.
  3. Alpha flicker: temporal smoothing (5-tap binomial) of the matte, weight ramped in from 4.0 s
     to 4.75 s so the fast debris of the burst (0.9-3 s) is not ghosted.
  4. Colour: remove the screen colour S (per frame: median of the pixels with d >= 0.9 x the frame's 99.5th
     percentile of d, so S follows the backdrop as it darkens; else the last S)
     from the edge mix: C' = C - (1 - alpha) * S, un-premultiplied by max(alpha, UNPREM_FLOOR);
     then despill G <= (R + B)/2 + 4 (max(R,B) left an olive rim); in the rim zone
     (source d from -10 to 15) the limit slides to 0.6 R + 0.4 B (warm brown, not olive).
     The spill removed from G is removed as screen colour (G and B in the screen's ratio), so no teal cast. Result: no green fringe and no teal/blue halo.
  5. Ending: from END_START (7.0 s) to END_BLACK (9.0 s) a smoothstep eases RGB to 0 and alpha to 1;
     9.0 s to the end (10.04 s) is full opaque black.
  6. RGBA 16-bit raw -> ffmpeg lanczos 1920x1080 -> ProRes 4444 (prores_ks profile 4, yuva444p10le,
     vendor apl0) + the source audio as pcm_s24le 48 kHz.
  7. Review: 3 seeded random fire moments in S5_CENTRE_camps.mov (read-only). Each review = 3 s camps,
     the 10.04 s overlay, 2 s camps after; 1280x720 h264, sound = camps + explosion mixed. Contact
     sheet of review 1 (every 0.5 s, 5x4, from 1 s before the impact).
"""
import argparse, glob, os, random, subprocess, sys
import numpy as np

SRC = 'D:/SOTR/SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/alpha_v1/S5-CANNON-ALPHA_v1_ba3c61fc.mp4'
DIR = os.path.dirname(SRC)
OUT = f'{DIR}/S5-CANNON-ALPHA_v1_KEY_1080.mov'
REVIEW_DIR = f'{DIR}/review'
CAMPS_GLOB = 'D:/SOTR/SOTR_MEDIA/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05*/S5_CENTRE_camps.mov'
FONT = 'C\\:/Windows/Fonts/consola.ttf'

W, H, FPS = 854, 480, 24
KEY_LO, KEY_HI = 10.0, 50.0        # d = G - max(R,B): <= LO opaque, >= HI transparent
UNPREM_FLOOR = 0.35
RIM_D = (-10.0, 15.0)             # despill rim zone in source d
DESPILL_BIAS = 4.0                 # despill: G <= (R+B)/2 + bias (avg despill; max(R,B) left a green rim)
SMOOTH_IN = (4.0, 4.75)            # temporal matte smoothing ramps in here (seconds)
END_START, END_BLACK = 7.0, 9.0    # ease to opaque black
PRE, POST = 3.0, 2.0               # review: camps before / after the overlay


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def pin_affinity(mask=0xFFFF3FFF):
    """Keep this process and every ffmpeg child off Core 7 (the PC hard-crashes there under all-core load)."""
    if sys.platform == 'win32':
        import ctypes
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        if not k.SetProcessAffinityMask(ctypes.c_void_p(k.GetCurrentProcess()), ctypes.c_size_t(mask)):
            sys.exit('could not set CPU affinity FFFF3FFF')


def run(cmd):
    print('>>', ' '.join(cmd)[:300], flush=True)
    subprocess.run(cmd, check=True)


def decode():
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', SRC, '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(np.float32)


def blur1(a):
    """3x3 binomial blur (1 px) on a 2-D matte."""
    p = np.pad(a, 1, mode='edge')
    h = (p[:, :-2] + 2 * p[:, 1:-1] + p[:, 2:]) / 4
    return (h[:-2] + 2 * h[1:-1] + h[2:]) / 4


def key(v):
    n = len(v)
    d = v[..., 1] - np.maximum(v[..., 0], v[..., 2])
    alpha = 1.0 - smoothstep(KEY_LO, KEY_HI, d)
    alpha = np.stack([blur1(a) for a in alpha])
    # temporal smoothing, ramped in after the burst
    pad = np.concatenate([alpha[:1], alpha[:1], alpha, alpha[-1:], alpha[-1:]])
    sm = (pad[:-4] + 4 * pad[1:-3] + 6 * pad[2:-2] + 4 * pad[3:-1] + pad[4:]) / 16
    t = np.arange(n) / FPS
    w = smoothstep(*SMOOTH_IN, t)[:, None, None]
    alpha = (1 - w) * alpha + w * sm
    # ending: alpha -> 1, rgb -> 0
    e = smoothstep(END_START, END_BLACK, t)
    alpha = alpha + (1 - alpha) * e[:, None, None]
    rgb = np.empty_like(v)
    S = np.array([0.0, 174.0, 64.0], np.float32)
    for i in range(n):
        # screen colour tracks the backdrop as it darkens: median of the most-key pixels of this frame
        top = np.percentile(d[i], 99.5)
        if top > 8:
            pure = d[i] >= 0.9 * top
            if pure.sum() > 500:
                S = np.median(v[i][pure], axis=0)
        elif top <= 4:
            S = np.zeros(3, np.float32)
        a = alpha[i][..., None]
        c = (v[i] - (1 - a) * S) / np.maximum(a, UNPREM_FLOOR)
        c = np.clip(c, 0, 255)
        # despill: G <= (R+B)/2 + bias in clean smoke; in the green-contaminated rim (source d near 0
        # or above) the limit slides to 0.6 R + 0.4 B so a dark rim reads warm brown, not olive
        k = smoothstep(RIM_D[0], RIM_D[1], d[i])
        lim = (1 - k) * (0.5 * (c[..., 0] + c[..., 2]) + DESPILL_BIAS) + k * (0.6 * c[..., 0] + 0.4 * c[..., 2])
        # remove the spill as SCREEN COLOUR, not green alone: the screen carries blue too (B/G ~0.37),
        # so clamping G only left a teal/blue cast on the darkening backdrop and the flash rim
        spill = np.maximum(c[..., 1] - lim, 0.0)[..., None]
        c = np.clip(c - spill * (S / max(S[1], 1.0)), 0, 255) if S[1] > 1 else c
        lim = (1 - k) * (0.5 * (c[..., 0] + c[..., 2]) + DESPILL_BIAS) + k * (0.6 * c[..., 0] + 0.4 * c[..., 2])
        c[..., 1] = np.minimum(c[..., 1], lim)   # clamp again on the new R, B
        rgb[i] = c * (1 - e[i])
    return rgb, alpha


def write_key(rgb, alpha):
    if os.path.exists(OUT):
        sys.exit(f'REFUSE: {OUT} exists (never overwrite; make a new version)')
    cmd = ['ffmpeg', '-v', 'error', '-y',
           '-f', 'rawvideo', '-pix_fmt', 'rgba64le', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-i', SRC, '-map', '0:v', '-map', '1:a',
           '-vf', 'scale=1920:1080:flags=lanczos+accurate_rnd+full_chroma_int,format=yuva444p10le',
           '-c:v', 'prores_ks', '-profile:v', '4', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0',
           '-alpha_bits', '16',
           '-af', 'apad', '-c:a', 'pcm_s24le', '-ar', '48000', '-t', f'{len(rgb) / FPS:.6f}', OUT]
    print('>> encode', OUT, flush=True)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(len(rgb)):
        fr = np.concatenate([rgb[i], alpha[i][..., None] * 255.0], axis=-1)
        p.stdin.write((np.clip(fr, 0, 255) * 257.0 + 0.5).astype('<u2').tobytes())
    p.stdin.close()
    if p.wait():
        sys.exit('ffmpeg encode failed')


def test_stills(rgb, alpha, outdir):
    os.makedirs(outdir, exist_ok=True)
    from PIL import Image
    red = np.array([200, 30, 30], np.float32)
    for f in [12, 22, 30, 48, 72, 96, 120, 132, 138, 144, 156, 180, 220]:
        a = alpha[f][..., None]
        comp = rgb[f] * a + red * (1 - a)
        Image.fromarray(np.clip(comp, 0, 255).astype(np.uint8)).save(f'{outdir}/t_{f:03d}.png')
        Image.fromarray((alpha[f] * 255).astype(np.uint8)).save(f'{outdir}/a_{f:03d}.png')
    print('test stills in', outdir)


def dur(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True, check=True).stdout)


def reviews(seed, n):
    camps = glob.glob(CAMPS_GLOB)
    if len(camps) != 1:
        sys.exit(f'camps file not found uniquely: {camps}')
    camps = camps[0].replace('\\', '/')
    os.makedirs(REVIEW_DIR, exist_ok=True)
    kd = dur(OUT)
    cd = dur(camps)
    total = PRE + kd + POST
    rng = random.Random(seed)
    starts = sorted(round(rng.uniform(PRE, cd - kd - POST - 0.5), 2) for _ in range(n))
    print(f'seed {seed}: fire moments (s into S5_CENTRE_camps.mov) = {starts}', flush=True)
    outs = []
    for k, t in enumerate(starts, 1):
        out = f'{REVIEW_DIR}/S5-CANNON-ALPHA_v1_review{k}_fire{t:07.2f}s.mp4'
        if os.path.exists(out):
            print('exists, skip', out); outs.append((out, t)); continue
        fc = (f'[0:v]scale=1280:720:flags=lanczos,format=yuv420p[bg];'
              f'[1:v]fps=25,scale=1280:720:flags=lanczos,format=yuva444p,setpts=PTS+{PRE}/TB[fg];'
              f'[bg][fg]overlay=0:0:eof_action=pass:format=auto,format=yuv420p,'
              f'drawtext=fontfile=\'{FONT}\':fontcolor=white:fontsize=22:box=1:boxcolor=black@0.5:x=12:y=12:'
              f'text=\'camps {t:.2f}s + fire at 3.00 s   %{{pts\\:hms}}\'[v];'
              f'[1:a]adelay={int(PRE*1000)}|{int(PRE*1000)}[ea];'
              f'[0:a][ea]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.97[a]')
        run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{t - PRE:.3f}', '-t', f'{total:.3f}', '-i', camps,
             '-i', OUT, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
             '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
             '-t', f'{total:.3f}', out])
        outs.append((out, t))
    sheet = outs[0][0].replace('.mp4', '_sheet.jpg')
    run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{PRE + 0.92 - 1.0:.2f}', '-i', outs[0][0],
         '-vf', 'fps=2,scale=480:-2,tile=5x4', '-frames:v', '1', '-q:v', '3', sheet])
    print('sheet', sheet)
    return outs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--review-only', action='store_true')
    ap.add_argument('--test')
    ap.add_argument('--seed', type=int, default=5)
    ap.add_argument('--n', type=int, default=3)
    a = ap.parse_args()
    pin_affinity()
    print(f'key thresholds: d=G-max(R,B) lo {KEY_LO} hi {KEY_HI}; unprem floor {UNPREM_FLOOR}; despill bias {DESPILL_BIAS}, rim d {RIM_D}; '
          f'temporal smooth from {SMOOTH_IN}; end ease {END_START}-{END_BLACK} s', flush=True)
    if not a.review_only:
        if not a.test and os.path.exists(OUT):
            sys.exit(f'REFUSE: {OUT} exists (never overwrite; make a new version)')
        rgb, alpha = key(decode())
        if a.test:
            test_stills(rgb, alpha, a.test)
            print('DONE cannon_alpha'); return
        write_key(rgb, alpha)
    reviews(a.seed, a.n)
    print('DONE cannon_alpha')


if __name__ == '__main__':
    main()
