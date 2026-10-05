"""Re-hang the Louvre gallery's paintings on a finished LIT wall: centred on the wall, one centre line on the side walls.

Built 2026-10-05 (Homie: "this is a three-wall setting, so I want the paintings nice and centered on all sides… the Raft
right bang on in the middle… between the two paintings on one side and one painting on the other, keep them nicely
centered on each wall"). Works on the finished LIT v2 natives (gallery_wall.py --room-light output), so the approved
look is untouched; only positions change:

1. FRAMES found on the finished wall (gallery_wall.find_frames). Targets, in metres on the 3.6 m wall:
   CENTRE: the Raft centred left-right (height kept: LOOK hangs it high and large).
   LEFT:   the PAIR centred left-right as a group (equal margins), each painting on the centre line --centre-line.
   RIGHT:  Napoleon centred left-right, on the same centre line.
2. PLASTER rebuilt with gallery_wall.room_light's model and defaults (one room light; the pool and drop shadow follow
   each painting to its new place), carrying the wall's own fine grain; where a frame used to hang, the grain is
   filled with tiles of plain plaster from the same wall. Validated: with no move the rebuild matches v2 (--no-move).
3. FRAMES pasted at their new places (a 3 px apron, feathered), re-exposed by the ring light change (~1 for these moves).
4. --hires UPSCALED.png: work at the upscale's resolution (the 4K loops): the gilt comes from the upscale, the paintings
   are RE-PINNED from the public-domain originals (--paint IDX:FILE, gallery_wall.pin) so no upscaler texture is kept.

  python tools/gallery_rehang.py LIT_native.png --wall L|C|R --room ROOM.json --out OUT.png [--size WxH]
         [--centre-line 1.61] [--hires UP.png] [--paint IDX:FILE] [--no-move] [--frames-json OUT.json]
Needs numpy, Pillow, opencv (and tools/gallery_wall.py beside it).
"""
import argparse
import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gallery_wall as gw  # noqa: E402

U0 = {'L': 0.0, 'C': 4.8, 'R': 10.8}   # each wall's left edge, metres along the unfolded room (gallery_wall)
WALL_H = 3.6


def targets(frames, wall, W, H, centre_line):
    """(dx, dy) in native px per frame."""
    ppm = H / WALL_H
    cy_t = H - centre_line * ppm
    if wall == 'L':
        gx0 = min(f['frame'][0] for f in frames)
        gx1 = max(f['frame'][0] + f['frame'][2] for f in frames)
        dx = W / 2 - (gx0 + gx1) / 2
        return [(dx, cy_t - (f['frame'][1] + f['frame'][3] / 2)) for f in frames]
    out = []
    for f in frames:
        x, y, w, h = f['frame']
        out.append((W / 2 - (x + w / 2), 0.0 if wall == 'C' else cy_t - (y + h / 2)))
    return out


def model_wall(H, W, frames, room, u0, img):
    """gallery_wall.room_light's plaster, verbatim maths and defaults, for frames at their (new) boxes; no paste."""
    corner_dark, corner_m = 0.10, 0.55
    pool_gain, pool_pad_m, pool_soft_m = (0.16, 0.12, 0.07), 0.22, 0.30
    shadow_m, shadow_k, skirt_m = 0.035, 0.35, 0.022
    ppm = H / WALL_H
    v = (1 - (np.arange(H) + 0.5) / H) * WALL_H
    u = u0 + (np.arange(W) + 0.5) / ppm
    base = np.stack([np.polyval(room['poly_v'][c], v) for c in range(3)], -1)[:, None, :]
    corner = np.ones(W, np.float32)
    for uc in gw.ROOM_CORNERS:
        corner -= corner_dark * np.exp(-np.abs(u - uc) / corner_m)
    wall = base * corner[None, :, None]

    def rect(box, pad_px):
        x, y, w, h = box
        m = np.zeros((H, W), np.float32)
        m[max(0, int(y - pad_px)):int(y + h + pad_px), max(0, int(x - pad_px)):int(x + w + pad_px)] = 1
        return m
    pool = np.zeros((H, W), np.float32)
    shadow = np.zeros((H, W), np.float32)
    for f in frames:
        x, y, w, h = f['frame']
        pool = np.maximum(pool, cv2.GaussianBlur(rect(f['frame'], pool_pad_m * ppm), (0, 0), pool_soft_m * ppm))
        shadow = np.maximum(shadow, cv2.GaussianBlur(rect([x, y + int(shadow_m * ppm), w, h], 0), (0, 0),
                                                     shadow_m * ppm))
    wall = wall * (1 + pool[..., None] * np.float32(pool_gain)) * (1 - shadow_k * shadow[..., None])
    sk = np.clip((v - skirt_m) / 0.006, 0, 1)[:, None, None]
    return (wall * (0.35 + 0.65 * sk)).astype(np.float32), rect


def grain_of(img, s):
    return np.clip(img - cv2.GaussianBlur(img, (0, 0), 2 * s), -0.008, 0.008)


def fill_grain(grain, hole, plain, tile, seed=3):
    """Replace grain inside `hole` with random whole tiles of plain plaster (no frame, old or new)."""
    H, W = hole.shape
    rng = np.random.default_rng(seed)
    cand = [(y, x) for y in range(0, H - tile, tile // 2) for x in range(0, W - tile, tile // 2)
            if plain[y:y + tile, x:x + tile].all()]
    out = grain.copy()
    yy, xx = np.nonzero(hole)
    if not len(yy):
        return out
    for y in range(yy.min() // tile * tile, yy.max() + 1, tile):
        for x in range(xx.min() // tile * tile, xx.max() + 1, tile):
            sl = (slice(y, min(y + tile, H)), slice(x, min(x + tile, W)))
            if not hole[sl].any():
                continue
            cy, cx = cand[rng.integers(len(cand))]
            src = grain[cy:cy + tile, cx:cx + tile][:sl[0].stop - y, :sl[1].stop - x]
            m = hole[sl][..., None]
            out[sl] = np.where(m, src, out[sl])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('native')
    ap.add_argument('--wall', required=True, choices=['L', 'C', 'R'])
    ap.add_argument('--room', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--size')
    ap.add_argument('--centre-line', type=float, default=1.61, help='side walls: painting centres, metres above floor')
    ap.add_argument('--hires')
    ap.add_argument('--paint', action='append', default=[])
    ap.add_argument('--no-move', action='store_true')
    ap.add_argument('--frames-json')
    a = ap.parse_args()

    nat = gw.load(a.native)
    Hn, Wn = nat.shape[:2]
    frames = gw.find_frames(nat)
    mv = [(0.0, 0.0)] * len(frames) if a.no_move else targets(frames, a.wall, Wn, Hn, a.centre_line)
    ppm_n = Hn / WALL_H
    for f, (dx, dy) in zip(frames, mv):
        x, y, w, h = f['frame']
        print(f"frame {f['frame']}: move {dx / ppm_n * 100:+.1f} cm, {-dy / ppm_n * 100:+.1f} cm up -> centre "
              f"{(x + w / 2 + dx) / Wn * 100:.2f}% across, {(Hn - (y + h / 2 + dy)) / ppm_n:.3f} m high", flush=True)

    img = gw.load(a.hires) if a.hires else nat
    if a.hires:
        img = cv2.resize(img, (round(Wn * img.shape[0] / Hn), img.shape[0]), interpolation=cv2.INTER_LANCZOS4) \
            if abs(img.shape[1] / img.shape[0] - Wn / Hn) > 0.002 else img
    H, W = img.shape[:2]
    sx, sy = W / Wn, H / Hn
    s = (sx + sy) / 2
    sc = lambda b: [int(round(b[0] * sx)), int(round(b[1] * sy)), int(round(b[2] * sx)), int(round(b[3] * sy))]
    old = [dict(frame=sc(f['frame']), canvas=sc(f['canvas'])) for f in frames]
    new = [dict(frame=[o['frame'][0] + round(dx * sx), o['frame'][1] + round(dy * sy)] + o['frame'][2:],
                canvas=[o['canvas'][0] + round(dx * sx), o['canvas'][1] + round(dy * sy)] + o['canvas'][2:])
           for o, (dx, dy) in zip(old, mv)]

    room = json.load(open(a.room))
    wall, rect = model_wall(H, W, new, room, U0[a.wall], img)
    apron = max(2, round(3 * s))
    g = grain_of(img, s)
    occupied_old = np.zeros((H, W), bool)
    occupied_new = np.zeros((H, W), bool)
    for o, n in zip(old, new):
        occupied_old |= rect(o["frame"], apron + round(64 * s)) > 0.5   # wide: the old edge + a plate ledge 43 px under it live in the grain
        occupied_new |= rect(n['frame'], apron) > 0.5
    plain = ~(occupied_old | occupied_new)
    g = fill_grain(g, occupied_old & ~occupied_new, plain, tile=max(32, round(64 * s)))
    new_wall = wall + g
    out = new_wall.copy()
    keep = np.zeros((H, W), np.float32)
    for o, n in zip(old, new):
        x, y, w, h = o['frame']
        nx, ny = n['frame'][:2]
        pa = apron
        patch = img[y - pa:y + h + pa, x - pa:x + w + pa]
        ring_new = (rect(n['frame'], 0.25 * H / WALL_H) - rect(n['frame'], 0.05 * H / WALL_H)) > 0.5
        ring_old = (rect(o['frame'], 0.25 * H / WALL_H) - rect(o['frame'], 0.05 * H / WALL_H)) > 0.5
        gain = np.clip(np.median(new_wall[ring_new], 0) / (np.median(img[ring_old], 0) + 1e-4), 0.9, 1.1)
        print('  ring gain', gain.round(3), flush=True)
        m = np.zeros((H, W), np.float32)
        m[ny - pa:ny + h + pa, nx - pa:nx + w + pa] = 1
        out[ny - pa:ny + h + pa, nx - pa:nx + w + pa] = patch * gain
        keep = np.maximum(keep, rect(n["frame"], apron - 1))   # the apron too: the frame's fuzzy outer edge
    k = cv2.GaussianBlur(keep, (0, 0), 1.2 * s)[..., None]
    out = out * k + new_wall * (1 - k)
    for spec in a.paint:
        i, path = spec.split(':', 1)
        out = gw.pin(out, new[int(i)]['canvas'], path, seed=int(i) + 1)
    if a.frames_json:
        json.dump({'size': [W, H], 'frames': new}, open(a.frames_json, 'w'), indent=1)
    if a.size:
        Wo, Ho = map(int, a.size.split('x'))
        out = cv2.resize(out, (Wo, Ho), interpolation=cv2.INTER_AREA)
    gw.save(out, a.out)
    print('wrote', a.out, out.shape[1], 'x', out.shape[0], flush=True)


if __name__ == '__main__':
    main()
