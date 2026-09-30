"""Make an AI upscale FAITHFUL to its approved source: keep only the upscaler's fine detail, take everything else
(tone, colour, light, the candle flicker, every event's timing) from the source, frame by frame.

WHY (2026-09-30, the 4K test on loc_SOTR_salon_R_loop_s9_v1): both Higgsfield video upscalers change the approved
motion. ByteDance ("aigc", 4k) is clean but damps the halo breathing ~15% (correlation 0.98 with the source);
Topaz (2160p) keeps the flicker exactly but its HEVC has a keyframe every 30 frames and the grain resets on each
one, a texture "tick" every 1.25 s. Flicker and light live in the LOW spatial frequencies; the upscaler's gain is
the HIGH ones. So:  out = upscale - blur(upscale) + blur(source upscaled bicubically).
With ByteDance as the input this gives the source's exact light and motion, the new detail, no ticks, no ringing.
The low band comes from the 10-bit source, and the output is 10-bit ProRes 422 HQ with the SOURCE's own sound.

  python tools/upscale_restore.py SOURCE UPSCALE OUT.mov [--sigma 12] [--size 3600x2160]

--size forces the output size (the upscale is resampled to it): ByteDance returned the 1800x1080 court as
3596x2160, a 0.1% squeeze; the show needs exactly 2x.

--sigma is in SOURCE pixels (scaled to the output). Frames are matched by index; the counts must agree.

--clamp R (output px, default 2; 0 = off): no output pixel may go brighter than the brightest, or darker than the
darkest, source pixel within R of it (the source upscaled bicubically). WHY: ByteDance draws a thin pale rim along
the judge's black silhouette (incidental white, banned by LOOK World 3) and a faint halo round the salon's candle
flames: overshoot the source never had. The clamp removes it and keeps the upscaler's smooth, unstepped edge.
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
    """rgb48 frames (0-1 float32), scaled to (w, h) with bicubic if needed."""
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source')
    ap.add_argument('upscale')
    ap.add_argument('out')
    ap.add_argument('--sigma', type=float, default=12.0, help='low/high split, in source pixels')
    ap.add_argument('--size', help='WxH of the output (default: the size the upscale came back at)')
    ap.add_argument('--clamp', type=int, default=2, help='anti-ringing radius, output px (0 = off)')
    a = ap.parse_args()
    sw, sh, sn, rate = probe(a.source)
    uw, uh, un, _ = probe(a.upscale)
    if a.size:
        uw, uh = (int(v) for v in a.size.lower().split('x'))
    if sn != un:
        raise SystemExit(f'frame counts differ: source {sn}, upscale {un}')
    sig = a.sigma * uw / sw
    enc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{uw}x{uh}',
                            '-r', rate, '-i', '-', '-i', a.source, '-map', '0:v', '-map', '1:a?', '-c:v', 'prores_ks', '-qscale:v', '2',
                            '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-c:a', 'pcm_s24le', '-ar', '48000',
                            '-shortest', a.out], stdin=subprocess.PIPE)
    for i, (u, s) in enumerate(zip(reader(a.upscale, uw, uh), reader(a.source, uw, uh))):
        o = u - cv2.GaussianBlur(u, (0, 0), sig) + cv2.GaussianBlur(s, (0, 0), sig)
        if a.clamp > 0:
            k = np.ones((2 * a.clamp + 1, 2 * a.clamp + 1), np.uint8)
            o = np.minimum(np.maximum(o, cv2.erode(s, k)), cv2.dilate(s, k))
        enc.stdin.write((np.clip(o, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
    enc.stdin.close()
    enc.wait()
    print('wrote', a.out, f'({uw}x{uh}, {sn} frames, sigma {sig:.1f} px, clamp {a.clamp} px)')


if __name__ == '__main__':
    main()
