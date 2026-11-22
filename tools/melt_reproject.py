"""Map the 2019 Houdini melt render (360 x 180 equirect, 4096x3112, 25 fps) onto the three SOTR walls.

The render is a panorama seen from one point. Each wall is a flat plane in the set (STAGE.md), so we look up,
for every wall pixel, the direction from a virtual eye to that point on the wall, and sample the panorama there.
The eye is placed so the Raft's frame lands at the S1 gallery hang (frame ~0.4-3.4 m on CENTRE, ~4.2 m wide).

  python tools/melt_reproject.py stills SRC OUTDIR 0 60 150 300      -> per-wall PNGs + a 3-wall sheet (1080 walls)
  python tools/melt_reproject.py video SRC OUT.mp4 WALL F0 F1 SCALE    -> one wall, frames F0..F1, wall size * SCALE
  python tools/melt_reproject.py density                               -> source px per wall px (upscale factor)

Read-only on SRC. Lanczos sampling only (no AI). SCALE 1 = 1080 wall.
"""
import subprocess
import sys

import cv2
import numpy as np

SW, SH = 4096, 3112
# set geometry, mm (STAGE.md): x right, y upstage (0 = downstage line of the flats), z up
CENTRE_Y = 4350 + 830
EYE = np.array([0.0, CENTRE_Y - 2826.0, 970.0])   # solved so pitch +40.7 / -11.4 (the frame) -> 3400 / 400 mm on CENTRE
WALLS = {  # name: (px w, px h at 1080, left-edge point, right-edge point)
    'LEFT': (1440, 1080, (-5028.0, 0.0), (-3000.0, 4350.0)),
    'CENTRE': (1800, 1080, (-3000.0, CENTRE_Y), (3000.0, CENTRE_Y)),
    'RIGHT': (1440, 1080, (3000.0, 4350.0), (5028.0, 0.0)),
}


FLOOR_W, FLOOR_H = 10057.0, 4350.0   # FLOOR-PLAN.md envelope, top-down ortho, top = upstage


def floor_maps(scale=1.0):
    # 16:9 frame (1920x1080 at scale 1); the envelope fills the width (1920x830), black above and below
    W, H = int(round(1920 * scale)), int(round(1080 * scale))
    eh = W * FLOOR_H / FLOOR_W
    x0 = (H - eh) / 2
    uu, vv = np.meshgrid((np.arange(W) + 0.5) / W, (np.arange(H) + 0.5 - x0) / eh)
    px = -FLOOR_W / 2 + FLOOR_W * uu
    py = FLOOR_H * (1 - vv)
    dx, dy, dz = px - EYE[0], py - EYE[1], -EYE[2]
    yaw = np.degrees(np.arctan2(dx, dy))
    pitch = np.degrees(np.arctan2(dz, np.hypot(dx, dy)))
    mx = ((yaw / 360.0 + 0.5) * SW - 0.5).astype(np.float32)
    my = ((0.5 - pitch / 180.0) * SH - 0.5).astype(np.float32)
    out = (vv < 0) | (vv > 1)
    mx[out] = -1e6
    my[out] = -1e6
    return mx, my


def maps(wall, scale=1.0):
    if wall == 'FLOOR':
        return floor_maps(scale)
    w, h, a, b = WALLS[wall]
    w, h = int(round(w * scale)), int(round(h * scale))
    u = (np.arange(w) + 0.5) / w
    v = (np.arange(h) + 0.5) / h
    uu, vv = np.meshgrid(u, v)
    px = a[0] + (b[0] - a[0]) * uu
    py = a[1] + (b[1] - a[1]) * uu
    pz = 3600.0 * (1 - vv)
    dx, dy, dz = px - EYE[0], py - EYE[1], pz - EYE[2]
    yaw = np.degrees(np.arctan2(dx, dy))
    pitch = np.degrees(np.arctan2(dz, np.hypot(dx, dy)))
    mx = ((yaw / 360.0 + 0.5) * SW - 0.5).astype(np.float32)
    my = ((0.5 - pitch / 180.0) * SH - 0.5).astype(np.float32)
    return mx, my


def frames(src, f0, f1):
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'select=between(n\\,{f0}\\,{f1})', '-fps_mode', 'passthrough',
                          '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE, stdin=subprocess.DEVNULL)
    n = SW * SH * 3
    while True:
        buf = p.stdout.read(n)
        if len(buf) < n:
            break
        yield np.frombuffer(buf, np.uint8).reshape(SH, SW, 3)
    p.wait()


def remap(img, m):
    r = cv2.remap(img, m[0], m[1], cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_WRAP)
    r[m[1] < -1e5] = 0
    return r


def density():
    for wall in list(WALLS) + ['FLOOR']:
        mx, my = maps(wall)
        gx = np.abs(np.diff(mx, axis=1))
        gy = np.abs(np.diff(my, axis=0))
        gx = gx[(gx < SW / 2) & (gx > 0)]
        print(f'{wall}: source px per 1080-wall px  horiz min {gx.min():.2f} median {np.median(gx):.2f} max {gx.max():.2f}'
              f' | vert median {np.median(gy):.2f}  -> upscale needed at 1080 ~{1/np.median(gx):.2f}x, at 4K ~{2/np.median(gx):.2f}x')


def stills(src, out, nums):
    import os
    os.makedirs(out, exist_ok=True)
    M = {w: maps(w) for w in WALLS}
    nums = sorted(int(n) for n in nums)
    rows = []
    for n in nums:
        img = next(frames(src, n, n))
        walls = [remap(img, M[w]) for w in ('LEFT', 'CENTRE', 'RIGHT')]
        for w, im in zip(('LEFT', 'CENTRE', 'RIGHT'), walls):
            cv2.imwrite(f'{out}/f{n:03d}_{w}.png', im)
        gap = np.full((1080, 24, 3), 40, np.uint8)
        row = np.hstack([walls[0], gap, walls[1], gap, walls[2]])
        cv2.putText(row, f'f{n} ({n/25:.1f} s)', (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.6, (0, 255, 255), 3)
        fl = remap(img, maps('FLOOR'))
        cv2.imwrite(f'{out}/f{n:03d}_FLOOR.png', fl)
        fl = cv2.resize(fl, (1800, 1012), interpolation=cv2.INTER_AREA)
        pad = np.full((1012, row.shape[1], 3), 0, np.uint8)
        x = (row.shape[1] - 1800) // 2
        pad[:, x:x + 1800] = fl
        cv2.rectangle(pad, (x, 0), (x + 1799, 1011), (60, 60, 60), 2)
        row = np.vstack([row, pad])
        rows.append(cv2.resize(row, (row.shape[1] // 3, row.shape[0] // 3), interpolation=cv2.INTER_AREA))
    cv2.imwrite(f'{out}/SHEET_3wall.png', np.vstack(rows))


def video(src, out, wall, f0, f1, scale):
    m = maps(wall, float(scale))
    h, w = m[0].shape
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}', '-r', '25',
                            '-i', '-', '-c:v', 'libx264', '-crf', '10', '-preset', 'slow', '-pix_fmt', 'yuv420p', out],
                           stdin=subprocess.PIPE)
    for img in frames(src, int(f0), int(f1)):
        enc.stdin.write(remap(img, m).tobytes())
    enc.stdin.close()
    enc.wait()


if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'density':
        density()
    elif c == 'stills':
        stills(sys.argv[2], sys.argv[3], sys.argv[4:])
    elif c == 'video':
        video(*sys.argv[2:8])
