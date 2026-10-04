"""Finish one Louvre-gallery wall plate (Scenes 1 + 10): crop to the wall, match the plaster, pin the real paintings.

Built 2026-10-05 for S1-GAL-C / -L / -R. The generated plates carry the room, the gilt frames and the light; the
paintings inside the frames are the generator's own copies and are REPLACED by the public-domain originals (the
Raft rule, LOOK "Scenes 1 + 10"). Steps, in order:

1. CROP (--crop x0,y0,x1,y1): the wall from corner to corner and from the skirting up, in source pixels. The S9
   precedent: a floor strip under the skirting is cropped, not regenerated.
2. FRAMES are found automatically: gilt = saturated warm-yellow pixels; each large gilt component is a frame, its
   enclosed non-gilt hole is the canvas. Printed as JSON so a run can be checked; --frames-only stops here.
3. SCALE (--scale-frame IDX:FACTOR, optional): the framed painting, its frame and its pool of light are enlarged
   about the frame centre over plain plaster (feathered). Used on CENTRE: NBP hangs the Raft at ~48% of the wall
   whatever the prompt says (v1 and v2, 8 takes); the target is ~2/3 (LOOK). The wall is flat, square-on and evenly
   lit, so an enlargement of the region is geometrically what a bigger painting would look like.
4. PIN (--paint IDX:FILE): the real painting is fitted (cover, centred) into canvas IDX. It takes the placeholder's
   per-channel mean and spread (the room's colour and contrast) and the SHAPE of the light across it (the
   placeholder's heavily smoothed luminance relative to its mean), as tools/render_wall.py does for Gerard. Matched
   grain on top. A 2 px feather at the canvas edge so the gilt's lip overlaps it.
5. GRADE (--match-wall REF.png --wall-sample x0,y0,x1,y1 --ref-sample x0,y0,x1,y1): per-channel gain so this wall's
   plaster matches the reference wall's plaster (the seam check: three walls of one room).
5b. ROOM LIGHT (--room-light ROOM.json --u0 METRES), added 2026-10-05 after Homie: "all of this will be projected at
   the same time… it should look cohesive as a single space." Replaces --relight and --match-wall. Every wall's
   plaster is REBUILT from one room-wide model: one plaster colour and one top-down laylight curve (measured once from
   CENTRE with --measure-room), positions in metres along the unfolded room (LEFT 0-4.8, CENTRE 4.8-10.8, RIGHT
   10.8-15.6), soft darkening into the two real corners, the SAME warm pool and drop shadow on every painting, one
   synthetic shadow-gap skirting. The plate keeps only its fine plaster grain. Each frame + painting is re-exposed by
   the change of light in a ring around it, so it sits in its new surroundings.
6. OUT: --out FILE at --size WxH (1440x1080 for L/R, 1800x1080 for C at 1080; doubled for 4K).

Needs numpy, Pillow, opencv (cv2).
"""
import argparse, json, sys
import numpy as np
from PIL import Image
import cv2


def load(p):
    return np.asarray(Image.open(p).convert('RGB'), dtype=np.float32) / 255.0


def save(a, p):
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(p, quality=95)


def gilt_mask(img):
    hsv = cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2HSV)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    m = ((h >= 12) & (h <= 32) & (s >= 125) & (v >= 120)).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((7, 7), np.uint8))
    return m


def find_frames(img, min_frac=0.004):
    H, W = img.shape[:2]
    m = gilt_mask(img)
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    frames = []
    for i in range(1, n):
        x, y, w, h, area = st[i]
        if area < min_frac * H * W or w < 0.05 * W or h < 0.08 * H:
            continue
        # the canvas: walk inward from each side of the frame box along a central strip until the gilt ends
        # (a hole-search fails on portraits: gold inside the painting, ermine, a throne, cuts the hole)
        comp = (lab[y:y + h, x:x + w] == i)
        def run(line, gap=10):
            # skip a fuzzy outer edge, then count gilt until a clear gap (carving has small dark gaps)
            k = 0
            while k < len(line) * 0.1 and not line[k]:
                k += 1
            last = k
            while k < len(line) * 0.3:
                if line[k]:
                    last = k
                elif k - last >= gap:
                    break
                k += 1
            return last + 1
        rows = range(int(h * 0.35), int(h * 0.65), 3)
        cols = range(int(w * 0.35), int(w * 0.65), 3)
        lft = int(np.median([run(comp[r, :]) for r in rows]))
        rgt = int(np.median([run(comp[r, ::-1]) for r in rows]))
        top = int(np.median([run(comp[:, c]) for c in cols]))
        bot = int(np.median([run(comp[::-1, c]) for c in cols]))
        if min(lft, rgt, top, bot) < 3 or lft + rgt > 0.6 * w or top + bot > 0.6 * h:
            continue
        cx, cy, cw, ch = lft + 2, top + 2, w - lft - rgt - 4, h - top - bot - 4
        frames.append({'frame': [int(x), int(y), int(w), int(h)],
                       'canvas': [int(x + cx), int(y + cy), int(cw), int(ch)]})
    # a gilt patch inside a painting is not a frame: drop any box inside another frame's canvas
    def inside(a, b):
        return a[0] >= b[0] and a[1] >= b[1] and a[0] + a[2] <= b[0] + b[2] and a[1] + a[3] <= b[1] + b[3]
    frames = [f for f in frames if not any(inside(f['frame'], g['canvas']) for g in frames if g is not f)]
    frames.sort(key=lambda f: f['frame'][0])
    return frames


def feather_box(H, W, box, pad):
    x, y, w, h = box
    m = np.zeros((H, W), np.float32)
    m[max(0, y):y + h, max(0, x):x + w] = 1
    if pad > 0:
        m = cv2.GaussianBlur(m, (0, 0), pad)
    return m[..., None]


def scale_region(img, fr, factor, margin, dy=0):
    """Enlarge the frame + its light pool about the frame centre, over the plaster."""
    H, W = img.shape[:2]
    x, y, w, h = fr['frame']
    cx, cy = x + w / 2, y + h / 2
    M = np.float32([[factor, 0, cx * (1 - factor)], [0, factor, cy * (1 - factor) + dy]])
    cy0 = cy
    cy = cy + dy  # the enlarged frame's centre
    big = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
    # the region to replace: the enlarged frame plus a margin of its light, feathered into the wall
    bw, bh = w * factor + 2 * margin, h * factor + 2 * margin
    box = [int(cx - bw / 2), int(cy - bh / 2), int(bw), int(bh)]
    a = feather_box(H, W, box, margin / 2.5)
    out = big * a + img * (1 - a)
    nf = dict(fr)
    nf['frame'] = [int(cx - w * factor / 2), int(cy - h * factor / 2), int(w * factor), int(h * factor)]
    c = fr['canvas']
    ccx, ccy = c[0] + c[2] / 2, c[1] + c[3] / 2
    nf['canvas'] = [int(cx + (ccx - cx) * factor - c[2] * factor / 2), int(cy + (ccy - cy0) * factor - c[3] * factor / 2),
                    int(c[2] * factor), int(c[3] * factor)]
    return out, nf


def poly_fit(img, mask, deg_x=2, deg_y=3, step=8):
    H, W = img.shape[:2]
    ys, xs = np.mgrid[0:H:step, 0:W:step]
    sm = cv2.GaussianBlur(img, (0, 0), 6)
    keep = mask[::step, ::step] > 0.5
    X, Y = xs[keep] / W, ys[keep] / H
    terms = lambda X, Y: np.stack([X ** i * Y ** j for i in range(deg_x + 1) for j in range(deg_y + 1)], -1)
    A = terms(X, Y)
    yy, xx = np.mgrid[0:H, 0:W]
    T = terms(xx.ravel() / W, yy.ravel() / H)
    out = np.zeros_like(img)
    for c in range(3):
        coef, *_ = np.linalg.lstsq(A, sm[::step, ::step, c][keep], rcond=None)
        out[..., c] = (T @ coef).reshape(H, W)
    return out


def relight(img, frames, idx, orig_frames, pool_amp=(0.06, 0.05, 0.035), pool_pad=0.10, pool_soft=0.09, keep_pad=0.0):
    """Rebuild the plaster's light around a (scaled) frame: fitted base + one soft pool + the plaster's own texture."""
    H, W = img.shape[:2]
    def rect_mask(box, pad):
        x, y, w, h = box
        m = np.zeros((H, W), np.float32)
        m[max(0, int(y - pad * h)):int(y + h + pad * h), max(0, int(x - pad * h)):int(x + w + pad * h)] = 1
        return m
    fr, of = frames[idx]['frame'], orig_frames[idx]['frame']
    far = 1 - np.maximum(rect_mask(fr, 0.30), rect_mask(of, 0.30))
    base = poly_fit(img, far)
    # one soft warm pool on the painting, ADDED light only (a measured amp came out negative: the base fit is
    # brighter than the ring because the top of the wall is the brightest; 2026-10-05)
    amp = np.float32(pool_amp)
    pool = cv2.GaussianBlur(rect_mask(fr, pool_pad), (0, 0), pool_soft * fr[3])[..., None]
    # the frame's own soft drop shadow, a little below it
    x, y, w, h = fr
    sh = cv2.GaussianBlur(rect_mask([x, y + int(0.012 * h), w, h], 0.0), (0, 0), 0.012 * h)[..., None]
    # fine plaster grain only: a 6 px high-pass carried the old light box's edges through (2026-10-05)
    texture = np.clip(img - cv2.GaussianBlur(img, (0, 0), 2), -0.008, 0.008)
    wall = (base + pool * amp) * (1 - 0.35 * sh) + texture
    keep = cv2.GaussianBlur(rect_mask(fr, keep_pad), (0, 0), 1.5)[..., None]
    return img * keep + wall * (1 - keep)


ROOM_CORNERS = (4.8, 10.8)  # metres along the unfolded room: LEFT|CENTRE and CENTRE|RIGHT


def measure_room(img, cols, wall_h=3.6, out=None):
    """Plaster colour + vertical light curve from plain-plaster columns of the reference (CENTRE) wall."""
    H = img.shape[0]
    strip = np.concatenate([img[:, a:b] for a, b in cols], 1)
    prof = cv2.GaussianBlur(strip.mean(1)[None], (0, 0), H / 60)[0]  # (H, 3)
    v = (1 - (np.arange(H) + 0.5) / H) * wall_h  # height above the floor, m
    keep = v > 0.15  # ignore the skirting zone
    coefs = [np.polyfit(v[keep], prof[keep, c], 4).tolist() for c in range(3)]
    d = {'wall_h': wall_h, 'poly_v': coefs}
    if out:
        json.dump(d, open(out, 'w'), indent=1)
    return d


def room_light(img, frames, room, u0, wall_h=3.6, corner_dark=0.10, corner_m=0.55,
               pool_gain=(0.16, 0.12, 0.07), pool_pad_m=0.22, pool_soft_m=0.30,
               shadow_m=0.035, shadow_k=0.35, skirt_m=0.022):
    H, W = img.shape[:2]
    ppm = H / wall_h
    v = (1 - (np.arange(H) + 0.5) / H) * wall_h
    u = u0 + (np.arange(W) + 0.5) / ppm
    base = np.stack([np.polyval(room['poly_v'][c], v) for c in range(3)], -1)[:, None, :]  # (H,1,3)
    corner = np.ones(W, np.float32)
    for uc in ROOM_CORNERS:
        corner -= corner_dark * np.exp(-np.abs(u - uc) / corner_m)
    wall = base * corner[None, :, None]
    def rect(box, pad_px):
        x, y, w, h = box
        m = np.zeros((H, W), np.float32)
        m[max(0, int(y - pad_px)):int(y + h + pad_px), max(0, int(x - pad_px)):int(x + w + pad_px)] = 1
        return m
    pool = np.zeros((H, W), np.float32)
    shadow = np.zeros((H, W), np.float32)
    keep = np.zeros((H, W), np.float32)
    for f in frames:
        x, y, w, h = f['frame']
        pool = np.maximum(pool, cv2.GaussianBlur(rect(f['frame'], pool_pad_m * ppm), (0, 0), pool_soft_m * ppm))
        shadow = np.maximum(shadow, cv2.GaussianBlur(rect([x, y + int(shadow_m * ppm), w, h], 0), (0, 0), shadow_m * ppm))
        keep = np.maximum(keep, rect(f['frame'], 0))
    wall = wall * (1 + pool[..., None] * np.float32(pool_gain)) * (1 - shadow_k * shadow[..., None])
    # one shadow-gap skirting for the whole room
    sk = np.clip((v - skirt_m) / (0.006), 0, 1)[:, None, None]
    wall = wall * (0.35 + 0.65 * sk)
    grain = np.clip(img - cv2.GaussianBlur(img, (0, 0), 2), -0.008, 0.008)
    new_wall = wall + grain
    # re-expose each frame + painting by the light change in a ring around it
    out = img.copy()
    for f in frames:
        x, y, w, h = f['frame']
        ring = (rect(f['frame'], 0.25 * ppm) - rect(f['frame'], 0.05 * ppm)) > 0.5
        g = np.clip(np.median(new_wall[ring], 0) / (np.median(img[ring], 0) + 1e-4), 0.7, 1.4)
        f['_gain'] = g.round(3).tolist()
        out[y:y + h, x:x + w] = img[y:y + h, x:x + w] * g
    k = cv2.GaussianBlur(keep, (0, 0), 1.2)[..., None]
    return out * k + new_wall * (1 - k)


def pin(img, canvas, paint_path, light_sigma_frac=0.12, grain=0.012, seed=1):
    H, W = img.shape[:2]
    x, y, w, h = canvas
    ph = img[y:y + h, x:x + w]
    src = load(paint_path)
    sh, sw = src.shape[:2]
    s = max(w / sw, h / sh)  # cover
    rs = cv2.resize(src, (int(round(sw * s)), int(round(sh * s))), interpolation=cv2.INTER_AREA)
    oy, ox = (rs.shape[0] - h) // 2, (rs.shape[1] - w) // 2
    p = rs[oy:oy + h, ox:ox + w].copy()
    # colour and contrast of the room: per-channel mean and spread of the placeholder
    for c in range(3):
        pm, ps = p[..., c].mean(), p[..., c].std() + 1e-6
        tm, ts = ph[..., c].mean(), ph[..., c].std()
        p[..., c] = (p[..., c] - pm) / ps * ts + tm
    # the shape of the light across the canvas: the placeholder's smoothed luminance, relative
    lum = ph @ np.float32([0.2126, 0.7152, 0.0722])
    sig = max(w, h) * light_sigma_frac
    shape = cv2.GaussianBlur(lum, (0, 0), sig)
    shape = shape / (shape.mean() + 1e-6)
    plum = cv2.GaussianBlur(p @ np.float32([0.2126, 0.7152, 0.0722]), (0, 0), sig)
    plum = plum / (plum.mean() + 1e-6)
    p = p * (shape / np.clip(plum, 0.2, 5))[..., None]
    rng = np.random.default_rng(seed)
    p = p + rng.normal(0, grain, p.shape[:2]).astype(np.float32)[..., None]
    out = img.copy()
    a = np.ones((h, w), np.float32)
    a = cv2.GaussianBlur(np.pad(a[2:-2, 2:-2], 2), (0, 0), 1.0)[..., None]
    out[y:y + h, x:x + w] = p * a + ph * (1 - a)
    return out


def box_mean(img, b):
    x0, y0, x1, y1 = b
    return img[y0:y1, x0:x1].reshape(-1, 3).mean(0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('plate')
    ap.add_argument('--crop', help='x0,y0,x1,y1 in source px')
    ap.add_argument('--frames-only', action='store_true')
    ap.add_argument('--scale-frame', action='append', default=[], help='IDX:FACTOR[:DY] (DY px, negative = up)')
    ap.add_argument('--scale-margin', type=float, default=0.12, help='light margin, fraction of frame height')
    ap.add_argument('--paint', action='append', default=[], help='IDX:FILE')
    ap.add_argument('--match-wall', help='reference wall image (already finished, same scale)')
    ap.add_argument('--wall-sample', help='x0,y0,x1,y1 plaster box in THIS cropped wall')
    ap.add_argument('--ref-sample', help='x0,y0,x1,y1 plaster box in the reference wall')
    ap.add_argument('--canvas', action='append', default=[], help='IDX:x,y,w,h measured canvas (overrides detection)')
    ap.add_argument('--relight', action='append', default=[], help='IDX: rebuild the wall light around frame IDX')
    ap.add_argument('--measure-room', help='OUT.json: measure plaster colour + light curve from this (cropped) wall')
    ap.add_argument('--room-cols', default='300,600;1960,2230', help='plain-plaster column ranges for --measure-room')
    ap.add_argument('--room-light', help='ROOM.json from --measure-room: rebuild this wall in the room-wide light')
    ap.add_argument('--u0', type=float, default=0.0, help="this wall's left edge, metres along the unfolded room")
    ap.add_argument('--blank', action='append', default=[], help='x0,y0,x1,y1: blur a box flat (a plaque with generated lettering)')
    ap.add_argument('--size', help='WxH output size')
    ap.add_argument('--out')
    a = ap.parse_args()

    img = load(a.plate)
    if a.crop:
        x0, y0, x1, y1 = map(int, a.crop.split(','))
        img = img[y0:y1, x0:x1]
    frames = find_frames(img)
    for spec in a.canvas:
        i, box = spec.split(':')
        frames[int(i)]['canvas'] = list(map(int, box.split(',')))
    print(json.dumps({'size': [img.shape[1], img.shape[0]], 'frames': frames}))
    if a.frames_only:
        return
    orig_frames = json.loads(json.dumps(frames))
    for spec in a.scale_frame:
        parts = spec.split(':')
        i, f = int(parts[0]), float(parts[1])
        dy = float(parts[2]) if len(parts) > 2 else 0.0
        img, frames[i] = scale_region(img, frames[i], f, a.scale_margin * frames[i]['frame'][3], dy)
        print('scaled', i, json.dumps(frames[i]))
    if a.measure_room:
        cols = [tuple(map(int, c.split(','))) for c in a.room_cols.split(';')]
        print('room', json.dumps(measure_room(img, cols, out=a.measure_room))[:200])
        return
    if a.room_light:
        img = room_light(img, frames, json.load(open(a.room_light)), a.u0)
        print('frame gains', [f.get('_gain') for f in frames])
    for spec in a.relight:
        img = relight(img, frames, int(spec), orig_frames)
    for spec in a.blank:
        x0, y0, x1, y1 = map(int, spec.split(','))
        r = img[y0:y1, x0:x1]
        flat = cv2.GaussianBlur(r, (0, 0), max(3, (y1 - y0) / 2))
        flat = cv2.GaussianBlur(flat, (0, 0), max(3, (y1 - y0) / 2))
        img[y0:y1, x0:x1] = flat + np.random.default_rng(7).normal(0, 0.01, r.shape[:2]).astype(np.float32)[..., None]
    for spec in a.paint:
        i, path = spec.split(':', 1)
        img = pin(img, frames[int(i)]['canvas'], path, seed=int(i) + 1)
    if a.match_wall:
        ref = load(a.match_wall)
        g = box_mean(ref, list(map(int, a.ref_sample.split(',')))) / box_mean(img, list(map(int, a.wall_sample.split(','))))
        print('wall gain', g.round(3))
        img = img * g
    if a.size:
        W, H = map(int, a.size.split('x'))
        img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    if a.out:
        save(img, a.out)
        print('wrote', a.out)


if __name__ == '__main__':
    main()
