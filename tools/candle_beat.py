"""Lay a studio candle loop out to one beat's exact length, with the take's OWN sound looped the same way.

WHY (2026-09-30, the candle arc, LOOK D6): beats 6 and 9 get their own generated candles (S9-STU-L-B6 / -B9, 30 s
takes). loop_halo.py makes the picture loop but carries no sound, and render_studio.py writes picture only; the
sound rule says every show file carries the clips' own sound. This builds the beat's candle clip (picture +
sound) that render_studio.py paints on, and whose sound is muxed into the finished files.

  python tools/candle_beat.py TAKE.mp4 LOOP.mov OUT.mov --frames 772 [--lift 1.12,0.30] [--skip 12 --xfade 36]

LOOP.mov = loop_halo.py's output from TAKE.mp4 with the same --skip / --xfade, so the sound loop matches the
picture loop frame for frame: one cycle = source frames (skip + xfade) .. (skip + xfade + m), its last xfade
frames crossfaded into source frames skip .. skip + xfade (loop_halo.py's construction).

--lift BASE,EDGE (beat 9, "steady and at its brightest"): the light raised by BASE, and by up to EDGE more where the
light is lower, so the pool is brighter and the umber shadow is pushed back (the light reaches further). The gain
map is static (from the loop's mean frame), so the candle's own flicker is kept, only lifted. Why a script: the
generated B9 came back steadier but not brighter; its REFERENCE line pins the light level (LOG 2026-09-30).
"""
import argparse
import json
import subprocess

import cv2
import numpy as np

FPS = 24
SR = 48000


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                            '-show_entries', 'stream=width,height,nb_read_frames', '-of', 'json', p]))
    s = j['streams'][0]
    return int(s['width']), int(s['height']), int(s['nb_read_frames'])


def frames(p, w, h):
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'],
                          stdout=subprocess.PIPE)
    n = w * h * 6
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        yield np.frombuffer(b, np.uint16).reshape(h, w, 3).astype(np.float32) / 65535
    pr.wait()


def audio(p):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-map', '0:a', '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                       capture_output=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('loop')
    ap.add_argument('out')
    ap.add_argument('--frames', type=int, required=True)
    ap.add_argument('--lift', help='BASE,EDGE gains, e.g. 1.12,0.30')
    ap.add_argument('--skip', type=int, default=12)
    ap.add_argument('--xfade', type=int, default=36)
    a = ap.parse_args()
    W, H, L = probe(a.loop)
    loop = list(frames(a.loop, W, H))
    gain = None
    if a.lift:
        base, edge = (float(v) for v in a.lift.split(','))
        mean = np.mean(loop, axis=0).mean(2)
        lum = cv2.GaussianBlur(mean, (0, 0), W / 40)
        norm = np.clip(lum / np.percentile(lum, 99), 0, 1)
        gain = (base + edge * (1 - norm))[..., None].astype(np.float32)
    # sound: one cycle exactly as loop_halo builds the picture, then tiled
    A = audio(a.take)
    spf = SR / FPS
    s0, X, m = a.skip, a.xfade, L
    seg = lambda f0, f1: A[int(round(f0 * spf)):int(round(f1 * spf))]
    body = seg(s0 + X, s0 + X + m).copy()
    head = seg(s0, s0 + X)
    nx = min(len(head), int(round(X * spf)))
    w = np.linspace(1 / (X + 1), X / (X + 1), nx, dtype=np.float32)[:, None]
    body[-nx:] = body[-nx:] * (1 - w) + head[:nx] * w
    need = int(round(a.frames * spf))
    snd = np.tile(body, (need // len(body) + 1, 1))[:need]
    wav = a.out + '.wav.tmp'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-c:a',
                    'pcm_s24le', '-f', 'wav', wav], input=np.ascontiguousarray(snd).tobytes(), check=True)
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'prores_ks',
                            '-profile:v', '3', '-qscale:v', '2', '-pix_fmt', 'yuv422p10le', '-c:a', 'pcm_s24le',
                            '-shortest', a.out], stdin=subprocess.PIPE)
    for i in range(a.frames):
        f = loop[i % L]
        if gain is not None:
            f = f * gain
        enc.stdin.write((np.clip(f, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
    enc.stdin.close()
    enc.wait()
    import os
    os.remove(wav)
    print(f'wrote {a.out}: {a.frames} frames from a {L}-frame loop' + (f', lift {a.lift}' if a.lift else ''))


if __name__ == '__main__':
    main()
