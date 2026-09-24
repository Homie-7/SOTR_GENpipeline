"""Put the real painting into a generated wall clip, lit by the clip's own light.

Built 2026-09-24 for the salon (Gerard's Louis XVIII over the generator's placeholder king),
under Homie's final-product rule: the delivered file already carries the right painting.

Why it works: the camera is locked and the placeholder painting never moves, so every change
in the placeholder over time is LIGHT (candle flicker, the halos, the snuff's darkening, left
side first). Every frame, the painting takes the placeholder's own per-channel mean and spread
at that moment (so its colour and contrast are the room's, even at dusk), and the SHAPE of the
light across it (e.g. the left side darkening first) from the placeholder's smoothed luminance
relative to the reference frame. (v1 multiplied each colour channel by the placeholder's
change; at dusk that turned Gerard's white ermine lavender and brighter than the gilt.)

  python tools/comp_portrait.py OUT.mov IN1 [IN2 ...] --painting GERARD.jpg
         [--rect 586,154,468,720] [--grain 1.0] [--feather 1.5]

Inputs play in the order given and come out as ONE file (e.g. reveal, loop x N, snuff).
All inputs must be the same size and 24 fps. The reference frame is frame 0 of --ref (default:
the first input); for the salon use the lit comp loop, so the grade is the lit room's.
Sequence options, all built INTO the file (final-product rule): --fade-in S from black,
--tail-hold S holding the last frame (a still dusk wall), --fade-out S to black.
.mov output = ProRes 422 HQ 10-bit; anything else = H.264 preview.
Needs ffmpeg on PATH, numpy, Pillow.
"""
import argparse
import json
import subprocess

import numpy as np
from PIL import Image


def size(path):
    s = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height', '-of', 'json', path]))['streams'][0]
    return s['width'], s['height']


def frames(path, w, h):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'],
                         stdout=subprocess.PIPE)
    n = w * h * 6
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) < n:
                break
            yield np.frombuffer(buf, '<u2').reshape(h, w, 3).astype(np.float32) / 65535
    finally:
        p.kill()
        p.wait()


def blur(a, r):
    for ax in (0, 1):
        pad = [(0, 0)] * a.ndim
        pad[ax] = (r + 1, r)
        c = np.cumsum(np.pad(a, pad, mode='edge'), axis=ax)
        n = c.shape[ax]
        a = (np.take(c, range(2 * r + 1, n), axis=ax) - np.take(c, range(0, n - 2 * r - 1), axis=ax)) / (2 * r + 1)
    return a


def cover(img, w, h):
    """Scale to cover w x h, centre-crop. No stretching."""
    s = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * s), round(img.height * s)), Image.LANCZOS)
    x, y = (img.width - w) // 2, (img.height - h) // 2
    return np.asarray(img.crop((x, y, x + w, y + h)).convert('RGB')).astype(np.float32) / 255


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--painting', required=True)
    ap.add_argument('--rect', default='586,154,468,720', help='x,y,w,h of the canvas opening (salon RIGHT)')
    ap.add_argument('--grain', type=float, default=1.0, help='x the measured grain of the placeholder')
    ap.add_argument('--feather', type=float, default=1.5, help='edge softening, px')
    ap.add_argument('--light-radius', type=int, default=60, help='smoothing of the light map, px')
    ap.add_argument('--ref', help='clip whose frame 0 sets the grade (default: first input)')
    ap.add_argument('--fade-in', type=float, default=0, help='seconds up from black at the start')
    ap.add_argument('--tail-hold', type=float, default=0, help='seconds holding the last frame')
    ap.add_argument('--fade-out', type=float, default=0, help='seconds down to black at the end')
    ap.add_argument('--join-ramp', type=int, default=24,
                    help='frames over which each joined clip eases from the previous clip\'s exposure to its own')
    a = ap.parse_args()

    W, H = size(a.inputs[0])
    for p in a.inputs[1:]:
        assert size(p) == (W, H), f'{p} is not {W}x{H}'
    x, y, w, h = map(int, a.rect.split(','))
    sl = (slice(y, y + h), slice(x, x + w))

    refclip = a.ref or a.inputs[0]
    first = next(frames(refclip, W, H))
    second = list(zip(range(2), frames(refclip, W, H)))[1][1]
    ref = first[sl]
    lum = lambda im: im @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    ref_shape = blur(lum(ref), a.light_radius)
    ref_shape = ref_shape / ref_shape.mean() + 1e-4

    # grade the painting to sit like the placeholder: per-channel mean and spread
    paint = cover(Image.open(a.painting), w, h)
    pm, ps = paint.reshape(-1, 3).mean(0), paint.reshape(-1, 3).std(0)
    paint_n = (paint - pm) / ps  # normalised; re-graded to the placeholder every frame

    # grain: frame-to-frame noise of the placeholder's fine detail
    sigma = float(np.std((second[sl] - blur(second[sl], 2)) - (ref - blur(ref, 2))) / np.sqrt(2)) * a.grain

    # soft edge mask
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum.reduce([xx + 0.5, w - 0.5 - xx, yy + 0.5, h - 0.5 - yy])
    mask = np.clip(d / max(a.feather, 1e-3), 0, 1)[..., None]

    if a.out.lower().endswith('.mov'):
        enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le']
    else:
        enc = ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w_ = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', '24', '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(1819)
    nb = lambda p: int(json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams',
                    'v:0', '-show_entries', 'stream=nb_read_frames', '-of', 'json', p]))['streams'][0]['nb_read_frames'])
    tail = round(a.tail_hold * 24)
    total = sum(nb(p) for p in a.inputs) + tail
    fi, fo = round(a.fade_in * 24), round(a.fade_out * 24)

    def level(i):
        g = 1.0
        if fi and i < fi:
            g = min(g, (i + 1) / fi)
        if fo and i >= total - fo:
            g = min(g, (total - i - 1) / fo)
        return g

    def source():
        last = None
        for path in a.inputs:
            ratio = None
            for i, f in enumerate(frames(path, W, H)):
                if i == 0 and last is not None:
                    # exposure match at the join: ease from the outgoing clip's level to this one's
                    ratio = last.reshape(-1, 3).mean(0) / (f.reshape(-1, 3).mean(0) + 1e-6)
                if ratio is not None and i < a.join_ramp:
                    f = f * (ratio + (1 - ratio) * (i / a.join_ramp))
                last = f
                yield f.copy()  # the loop below edits in place; keep the source clean for the tail
        for _ in range(tail):
            yield last.copy()

    n = 0
    for f in source():
        ph = f[sl]
        m, sd = ph.reshape(-1, 3).mean(0), ph.reshape(-1, 3).std(0)
        shape = blur(lum(ph), a.light_radius)
        shape = np.clip(shape / shape.mean() / ref_shape, 0.2, 3)[..., None]
        lit = (paint_n * sd + m) * shape
        if sigma > 0:
            lit = lit + rng.normal(0, sigma, (h, w, 1)).astype(np.float32)
        f[sl] = f[sl] * (1 - mask) + np.clip(lit, 0, 1) * mask
        f *= level(n)
        w_.stdin.write((np.clip(f, 0, 1) * 65535).astype('<u2').tobytes())
        n += 1
    w_.stdin.close()
    w_.wait()
    print(f'{n} frames -> {a.out} (rect {x},{y},{w},{h}, grain sigma {sigma:.4f})')


if __name__ == '__main__':
    main()
