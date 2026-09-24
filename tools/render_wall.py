"""Render one wall's finished file: clips in sequence, the real painting, and the fragment edge.

Built 2026-09-24 (as comp_portrait.py; renamed when it grew). Homie's final-product rule: the
delivered file already carries everything the picture needs. The show operator does the fades
at the start and end in playback (Homie, 2026-09-24), so files start and end at full picture.

THE PAINTING (--painting, optional). The camera is locked and the generator's placeholder
painting never moves, so every change in it over time is LIGHT (candle flicker, the halos, the
snuff's darkening, left side first). Every frame, the real painting takes the placeholder's own
per-channel mean and spread at that moment (so its colour and contrast are the room's, even at
dusk) and the SHAPE of the light across it (the placeholder's smoothed luminance relative to
the reference frame). Matched grain on top. (Scaling each colour channel by the placeholder's
change turned Gerard's ermine lavender at dusk; don't.)

THE FRAGMENT EDGE (--fragment-edge left|right). Homie, 2026-09-24, after the 2022 concept
(Slide 9): each world is a fragment of reality, not a hard rectangle. It stays whole on its
OUTER side and breaks up toward the CENTRE of the stage. The salon plays on the RIGHT wall, so
its image breaks on its LEFT edge; the studio (LEFT wall) breaks on its RIGHT edge. The zone
(--fragment-width, fraction of the frame width) breaks up to black, in one of two styles
(--fragment-style): 'dissolve', an organic blotchy breakup with fine particles, drifting slowly
upward (closest to Slide 9); or 'shatter', whole shards dropping out. The front wanders along
the height. (A first version drew crack lines along every shard edge; on the wall they read as
a chicken-wire mesh, so there are none.) Black is no light on a projector, so the wall simply
ends in pieces.

JOINS. Each clip after the first eases from the previous clip's exposure to its own over
--join-ramp frames (no crossfade, so nothing ghosts).

  python tools/render_wall.py OUT.mov IN1 [IN2 ...] [--painting GERARD.jpg --rect x,y,w,h]
         [--fragment-edge left --fragment-width 0.12] [--ref CLIP]

Inputs play in order as ONE file. Same size, 24 fps. The grade reference is frame 0 of --ref
(default: the first input). .mov = ProRes 422 HQ 10-bit; anything else = H.264 preview.
--fade-in / --tail-hold / --fade-out exist but default to 0 (the operator's job).
FILES: clean renders go to SOTR_MEDIA/renders/clean/ and are never replaced; effect versions
(--fragment-edge) go to renders/fx/ as separate files. The tool refuses to mix them up or to
overwrite an existing file (unless --overwrite).
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


def nb_frames(path):
    return int(json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-count_frames', '-select_streams', 'v:0',
                                                   '-show_entries', 'stream=nb_read_frames', '-of', 'json', path]))
               ['streams'][0]['nb_read_frames'])


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


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def value_noise(h, w, cell, rng, wrap_y=False):
    """Smooth random field in [0, 1]: a random grid, bicubic-upsampled.

    wrap_y: the field is exactly periodic in y (period = a whole number of cells >= h), so it
    can be rolled for drift with no seam. The grid is stacked three times, upsampled, and the
    middle period kept, so the upsampling sees wrapped neighbours at both ends.
    """
    gw = int(np.ceil(w / cell)) + 3
    if wrap_y:
        gh = int(np.ceil(h / cell))
        g = rng.uniform(0, 1, (gh, gw)).astype(np.float32)
        big = Image.fromarray(np.vstack([g, g, g]), mode='F').resize((gw * cell, 3 * gh * cell), Image.BICUBIC)
        a = np.asarray(big)[gh * cell:2 * gh * cell, :w]
    else:
        gh = int(np.ceil(h / cell)) + 3
        g = rng.uniform(0, 1, (gh, gw)).astype(np.float32)
        a = np.asarray(Image.fromarray(g, mode='F').resize((gw * cell, gh * cell), Image.BICUBIC))[:h, :w]
    return np.clip(a, 0, 1)


class Fragments:
    """A one-sided breakup mask. u = 0 at the inner (breaking) edge, 1 where the zone ends.

    style 'dissolve': an organic, blotchy breakup (fractal noise) with fine particles at the
      front, drifting slowly upward. Closest to the 2022 Slide 9 concept.
    style 'shatter': whole shards (jittered Voronoi cells) drop out to black; no crack lines
      (they read as a mesh on the wall).
    Both: the front wanders along the height (low-frequency noise), so it isn't a straight band.
    """

    def __init__(self, W, H, edge, width, cell, shimmer, style='dissolve', drift=6.0, seed=1819):
        self.zw = max(int(W * width), 1)
        self.edge, self.W, self.H, self.shimmer, self.style, self.drift = edge, W, H, shimmer, style, drift
        rng = np.random.default_rng(seed)
        yy, xx = np.mgrid[0:H, 0:self.zw].astype(np.float32)
        self.u = (xx + 0.5) / self.zw
        # the front wanders along the height
        self.wander = (value_noise(H, 1, int(H / 5), rng)[:, :1] - 0.5) * 0.35
        if style == 'dissolve':
            fields = []
            for c, wgt in ((int(cell * 1.6), 0.55), (int(cell * 0.6), 0.30), (max(int(cell * 0.2), 3), 0.15)):
                fields.append((value_noise(H, self.zw, c, rng, wrap_y=True), wgt))
            self.fields = fields
            self.speck = value_noise(H, self.zw, max(int(cell * 0.08), 2), rng, wrap_y=True)
        else:
            gw, gh = int(np.ceil(self.zw / cell)) + 2, int(np.ceil(H / cell)) + 2
            sx = (np.arange(gw)[None, :] - 1 + rng.uniform(0.1, 0.9, (gh, gw))) * cell
            sy = (np.arange(gh)[:, None] - 1 + rng.uniform(0.1, 0.9, (gh, gw))) * cell
            gi, gj = (xx // cell).astype(int) + 1, (yy // cell).astype(int) + 1
            d1 = np.full(xx.shape, np.inf, np.float32)
            idx = np.zeros(xx.shape, int)
            for dj in (-1, 0, 1):
                for di in (-1, 0, 1):
                    ci, cj = np.clip(gi + di, 0, gw - 1), np.clip(gj + dj, 0, gh - 1)
                    d = np.hypot(xx - sx[cj, ci], yy - sy[cj, ci])
                    closer = d < d1
                    idx = np.where(closer, cj * gw + ci, idx)
                    d1 = np.where(closer, d, d1)
            n = gw * gh
            self.idx = idx
            self.su = np.clip((sx.ravel() + 0.5) / self.zw, 0, 1)
            self.sy = np.clip(sy.ravel(), 0, H - 1).astype(int)
            self.thr = rng.uniform(0, 1, n)
            self.phase, self.period = rng.uniform(0, 2 * np.pi, n), rng.uniform(4, 9, n)

    def mask(self, t):
        if self.style == 'dissolve':
            shift = int(round(t * self.drift))  # slow upward drift, px/s
            n = sum(np.roll(f, -shift, axis=0)[:self.H] * wgt for f, wgt in self.fields)
            n = n + self.shimmer * np.sin(2 * np.pi * t / 7.0)
            level = self.u + self.wander - 0.5 + (n - 0.5) * 1.3  # wide reach: islands of picture and holes
            m = smoothstep(-0.06, 0.06, level)
            # fine particles: a few specks survive past the front, a few holes open behind it
            sp = np.roll(self.speck, -2 * shift, axis=0)[:self.H]
            near = smoothstep(0.35, 0.0, np.abs(level))
            m = np.clip(m + near * smoothstep(0.72, 0.82, sp) - near * smoothstep(0.74, 0.84, 1 - sp), 0, 1)
        else:
            su = self.su + self.wander[self.sy, 0]
            ramp = smoothstep(0.0, 1.0, su)
            thr = self.thr + self.shimmer * np.sin(2 * np.pi * t / self.period + self.phase)
            m = (thr < 0.04 + 0.96 * ramp).astype(np.float32)[self.idx]
        m = np.maximum(m, smoothstep(0.8, 1.0, self.u))  # always whole at the zone's outer boundary: no straight cut
        m = blur(m, 1)
        return m if self.edge == 'left' else m[:, ::-1]

    def apply(self, f, t):
        m = self.mask(t)[..., None]
        if self.edge == 'left':
            f[:, :self.zw] *= m
        else:
            f[:, self.W - self.zw:] *= m
        return f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('inputs', nargs='+')
    ap.add_argument('--painting', help='real painting to put over the placeholder (optional)')
    ap.add_argument('--rect', default='586,154,468,720', help='x,y,w,h of the canvas opening (salon RIGHT)')
    ap.add_argument('--grain', type=float, default=1.0, help='x the measured grain of the placeholder')
    ap.add_argument('--feather', type=float, default=1.5, help='painting edge softening, px')
    ap.add_argument('--light-radius', type=int, default=60, help='smoothing of the light map, px')
    ap.add_argument('--ref', help='clip whose frame 0 sets the grade (default: first input)')
    ap.add_argument('--fragment-edge', choices=['left', 'right'], help='the edge that breaks up (toward CENTRE)')
    ap.add_argument('--fragment-width', type=float, default=0.12, help='breakup zone, fraction of frame width')
    ap.add_argument('--fragment-cell', type=float, default=70, help='shard size, px at the clip resolution')
    ap.add_argument('--fragment-shimmer', type=float, default=0.04, help='slow flicker at the front')
    ap.add_argument('--fragment-style', choices=['dissolve', 'shatter'], default='dissolve')
    ap.add_argument('--fragment-drift', type=float, default=6.0, help='dissolve: upward drift, px/s')
    ap.add_argument('--join-ramp', type=int, default=24,
                    help='frames over which each joined clip eases from the previous clip\'s exposure to its own')
    ap.add_argument('--fade-in', type=float, default=0, help='seconds up from black (default off: operator)')
    ap.add_argument('--tail-hold', type=float, default=0, help='seconds holding the last frame (default off)')
    ap.add_argument('--fade-out', type=float, default=0, help='seconds down to black (default off: operator)')
    ap.add_argument('--overwrite', action='store_true', help='allow replacing an existing output file')
    a = ap.parse_args()

    # File management (Homie, 2026-09-24): clean renders are masters and are never replaced;
    # effect versions (fragment edge) are always separate files, in renders/fx/.
    import os
    out_norm = os.path.abspath(a.out).replace(os.sep, '/')
    if a.fragment_edge and '/clean/' in out_norm:
        raise SystemExit('refusing: a fragment/effect render cannot go in renders/clean/ (use renders/fx/)')
    if not a.fragment_edge and '/fx/' in out_norm:
        raise SystemExit('refusing: a render without effects belongs in renders/clean/, not renders/fx/')
    if os.path.exists(a.out) and not a.overwrite:
        raise SystemExit(f'refusing: {a.out} exists. Clean renders are never replaced; give the new one a new version')

    W, H = size(a.inputs[0])
    for p in a.inputs[1:]:
        assert size(p) == (W, H), f'{p} is not {W}x{H}'

    paint = None
    if a.painting:
        x, y, w, h = map(int, a.rect.split(','))
        sl = (slice(y, y + h), slice(x, x + w))
        refclip = a.ref or a.inputs[0]
        first = next(frames(refclip, W, H))
        second = list(zip(range(2), frames(refclip, W, H)))[1][1]
        ref = first[sl]
        lum = lambda im: im @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        ref_shape = blur(lum(ref), a.light_radius)
        ref_shape = ref_shape / ref_shape.mean() + 1e-4
        paint = cover(Image.open(a.painting), w, h)
        pm, ps = paint.reshape(-1, 3).mean(0), paint.reshape(-1, 3).std(0)
        paint_n = (paint - pm) / ps  # normalised; re-graded to the placeholder every frame
        sigma = float(np.std((second[sl] - blur(second[sl], 2)) - (ref - blur(ref, 2))) / np.sqrt(2)) * a.grain
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        d = np.minimum.reduce([xx + 0.5, w - 0.5 - xx, yy + 0.5, h - 0.5 - yy])
        pmask = np.clip(d / max(a.feather, 1e-3), 0, 1)[..., None]

    frag = Fragments(W, H, a.fragment_edge, a.fragment_width, a.fragment_cell, a.fragment_shimmer,
                     a.fragment_style, a.fragment_drift) \
        if a.fragment_edge else None

    enc = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le'] if a.out.lower().endswith('.mov') \
        else ['-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p']
    w_ = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', '24', '-i', '-'] + enc + [a.out], stdin=subprocess.PIPE)
    rng = np.random.default_rng(1819)
    tail = round(a.tail_hold * 24)
    total = sum(nb_frames(p) for p in a.inputs) + tail
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
                    ratio = last.reshape(-1, 3).mean(0) / (f.reshape(-1, 3).mean(0) + 1e-6)
                if ratio is not None and i < a.join_ramp:
                    f = f * (ratio + (1 - ratio) * (i / a.join_ramp))
                last = f
                yield f.copy()  # edited in place below; keep the source clean for the tail
        for _ in range(tail):
            yield last.copy()

    n = 0
    for f in source():
        if paint is not None:
            ph = f[sl]
            m, sd = ph.reshape(-1, 3).mean(0), ph.reshape(-1, 3).std(0)
            shape = blur(lum(ph), a.light_radius)
            shape = np.clip(shape / shape.mean() / ref_shape, 0.2, 3)[..., None]
            lit = (paint_n * sd + m) * shape
            if sigma > 0:
                lit = lit + rng.normal(0, sigma, (h, w, 1)).astype(np.float32)
            f[sl] = f[sl] * (1 - pmask) + np.clip(lit, 0, 1) * pmask
        if frag is not None:
            frag.apply(f, n / 24)
        f *= level(n)
        w_.stdin.write((np.clip(f, 0, 1) * 65535).astype('<u2').tobytes())
        n += 1
    w_.stdin.close()
    w_.wait()
    print(f'{n} frames -> {a.out}' + (f' (painting at {a.rect})' if paint is not None else '')
          + (f' (fragment edge {a.fragment_edge}, {a.fragment_width:.0%})' if frag else ''))


if __name__ == '__main__':
    main()
