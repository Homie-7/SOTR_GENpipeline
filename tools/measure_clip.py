"""Measure a generated clip the same way every time (docs/AUTONOMOUS-GEN.md step 3).

Built 2026-09-24 for the Higgsfield connector gate. It measures the technical faults;
taste stays with Homie.

  python tools/measure_clip.py CLIP.mp4 --plate PLATE.jpg [--ref APPROVED.mp4] [--sheet OUT.jpg]

Reports:
  probe       size, fps, frames, codec, bit depth, bitrate, audio
  lock        phase-correlation shift of frames skip / middle / last against frame skip (px)
  framing     shift of the middle frame against the plate, scaled to the clip (px and %)
  light       whole-frame luma trend first->last (%), and the flicker in the most-moving
              2% of the frame (the halos) after removing that trend, peak to peak (%)
  flames      small very bright blobs per sampled frame (min / median / max)
  --ref       the same numbers for an approved clip, side by side
  --sheet     a contact sheet of 12 frames across the whole clip (lesson 8)

Needs ffmpeg/ffprobe on PATH, numpy.
"""
import argparse
import json
import subprocess
from collections import deque

import numpy as np

W, H = 832, 624  # half of Seedance's 4:3 1080p (1664x1248), enough for every check here


def probe(path):
    out = json.loads(subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries',
        'stream=codec_type,codec_name,profile,width,height,pix_fmt,r_frame_rate,nb_frames,bit_rate,sample_rate,channels'
        ':format=duration,bit_rate', '-of', 'json', path]))
    v = next(s for s in out['streams'] if s['codec_type'] == 'video')
    a = next((s for s in out['streams'] if s['codec_type'] == 'audio'), None)
    return {
        'size': f"{v['width']}x{v['height']}", 'fps': v['r_frame_rate'], 'frames': int(v.get('nb_frames', 0)),
        'codec': f"{v['codec_name']} {v.get('profile', '')}", 'pix_fmt': v['pix_fmt'],
        'video_mbps': round(int(v.get('bit_rate', 0)) / 1e6, 2), 'duration': float(out['format']['duration']),
        'audio': f"{a['codec_name']} {a['sample_rate']} Hz {a['channels']}ch" if a else 'none',
    }


def luma(path, n=None):
    args = ['ffmpeg', '-v', 'error', '-i', path]
    if n:
        args += ['-frames:v', str(n)]
    raw = subprocess.run(args + ['-vf', f'scale={W}:{H}', '-f', 'rawvideo', '-pix_fmt', 'gray16le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, '<u2').reshape(-1, H, W).astype(np.float32) / 65535 * 255


def shift(a, b):
    """Integer translation of b relative to a, by phase correlation."""
    fa, fb = np.fft.fft2(a - a.mean()), np.fft.fft2(b - b.mean())
    r = fa * np.conj(fb)
    c = np.abs(np.fft.ifft2(r / (np.abs(r) + 1e-9)))
    y, x = np.unravel_index(np.argmax(c), c.shape)
    return (int(x if x < W // 2 else x - W), int(y if y < H // 2 else y - H))


def blur(a, r=12):
    for ax in (-2, -1):
        pad = [(0, 0)] * a.ndim
        pad[ax] = (r + 1, r)
        c = np.cumsum(np.pad(a, pad, mode='edge'), axis=ax)
        n = c.shape[ax]
        a = (np.take(c, range(2 * r + 1, n), axis=ax) - np.take(c, range(0, n - 2 * r - 1), axis=ax)) / (2 * r + 1)
    return a


def blobs(mask):
    seen = np.zeros_like(mask, bool)
    count = 0
    for y, x in zip(*np.nonzero(mask)):
        if seen[y, x]:
            continue
        count += 1
        q = deque([(y, x)])
        seen[y, x] = True
        while q:
            cy, cx = q.popleft()
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        q.append((ny, nx))
    return count


def measure(path, plate, skip):
    p = probe(path)
    f = luma(path)
    body = f[skip:]
    mid, last = body[len(body) // 2], body[-1]
    out = {'probe': p, 'lock_px': {'mid': shift(body[0], mid), 'last': shift(body[0], last)}}
    if plate:
        pl = luma(plate, 1)[0]
        dx, dy = shift(pl, mid)
        out['framing_vs_plate'] = {'px_at_832': (dx, dy), 'pct': (round(100 * dx / W, 2), round(100 * dy / H, 2)),
                                   'mean_luma_plate': round(float(pl.mean()), 1), 'mean_luma_clip': round(float(mid.mean()), 1)}
    means = body.reshape(len(body), -1).mean(1)
    out['light'] = {'trend_pct': round(100 * (means[-12:].mean() - means[:12].mean()) / means.mean(), 2)}
    b = blur(body)
    t = np.arange(len(b), dtype=np.float32)
    t -= t.mean()
    slope = (b * t[:, None, None]).sum(0) / (t ** 2).sum()
    resid = b - b.mean(0) - slope * t[:, None, None]
    sd = resid.std(0)
    hot = sd >= np.quantile(sd, 0.98)
    cold = sd <= np.quantile(sd, 0.50)
    hs = resid[:, hot].mean(1) / b.mean(0)[hot].mean()
    cs = resid[:, cold].mean(1) / b.mean(0)[cold].mean()
    out['light'].update({'halo_flicker_p2p_pct': round(100 * float(hs.max() - hs.min()), 2),
                         'static_noise_p2p_pct': round(100 * float(cs.max() - cs.min()), 2),
                         'first_frame_step': round(float(np.abs(f[1] - f[0]).mean()), 2),
                         'median_frame_step': round(float(np.median(np.abs(np.diff(body[::1], axis=0)).mean((1, 2)))), 2)})
    thr = np.quantile(body[0], 0.9995)
    counts = [blobs(body[i] >= thr) for i in np.linspace(0, len(body) - 1, 12).astype(int)]
    out['flames'] = {'threshold': round(float(thr), 1), 'min': min(counts), 'median': int(np.median(counts)), 'max': max(counts)}
    return out


def sheet(path, dest, frames):
    step = max(frames // 12, 1)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf',
                    f"select='not(mod(n\\,{step}))',scale=416:-1,tile=4x3",
                    '-frames:v', '1', dest], check=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('clip')
    ap.add_argument('--plate')
    ap.add_argument('--ref')
    ap.add_argument('--skip', type=int, default=12)
    ap.add_argument('--sheet')
    a = ap.parse_args()
    res = {'clip': measure(a.clip, a.plate, a.skip)}
    if a.ref:
        res['ref'] = measure(a.ref, a.plate, a.skip)
    print(json.dumps(res, indent=1, default=float))
    if a.sheet:
        sheet(a.clip, a.sheet, res['clip']['probe']['frames'])
