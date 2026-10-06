"""The ship's IDLE LOOP per light state, as ONE picture across the three walls (route A, Homie 7 Oct: "idle animations for
all the basic states of the ship… it has to match").

  python tools/s7_idle.py CLIP.mp4 STATE OUTDIR [--xfade 1.5]

CLIP is a Seedance 21:9 take started from the state's deck canvas (prompts/S7-SHIP-IDLE.txt), at 1080p or upscaled.
1. Each frame is registered to the canvas (ECC affine on frame 0 and on the last frame, interpolated in between: Seedance
   reframes ~1% and may drift), then the centred 4.33:1 band is cut (4680x1080 = LEFT 1440 | CENTRE 1800 | RIGHT 1440).
2. ONLY THE SEA AND SKY come from the clip: the approved still (3_walls/seamed_v2/<state>) is laid back over everything
   else through the 5_layers/seamed_v2/<state> bgmasks (255 = sea/sky; 1.5 px feather). The ship can't drift or morph.
3. MOTION (Homie 7 Oct): the camera is fixed to the ship, so the DECK stays put and only the SEA + SKY roll (--roll deg)
   and heave (--heave px) behind it, in canvas space so the strips above/below fill the edges; a small vibration
   (--shake px) moves the whole frame; every term periodic over the loop (seamless), zero at frame 0. 0 0 0 = locked.
4. Seamless loop: the last XFADE s are crossfaded into the first (picture and sound), so the file cycles without a join.
5. The clip's own sound rides through, crossfaded the same way (house rule).
6. (v2, 8 Oct, Homie: "the ship's bow moves separately from the ship") the rolled WORLD layer holds NO ship: the masks are
   the refined 5_layers/.../_bgmask_v2 (tools/s7_worldfill.py: the forecastle gun, sail holes, blocks, rope edges are ship),
   and before the roll the clip's own ship (dilated --fill-grow px) is filled with sea/sky (sea mirrored from above the hull,
   sky push-pull), so no clip yard, gun or rail can roll into view beside the still ship. --check writes a no-shake test.
7. (v3, 9 Oct, Homie: "I can very clearly see the lines of what was erased") --world: CLIP is a SHIP-FREE sea + sky take
   (prompts/S7-SEA-IDLE.txt, started from 9_seaplate/S7-SEA-PLATE_<state>_upload.png): it is registered to that plate
   (on the sky and the horizon, the swell moves), and NOTHING is filled: there was never a ship in it to erase.
Writes S7-SHIP-IDLE_<state>_3walls_LOOP.mp4 (H.264 review, 4680x1080) + per wall _LEFT/_CENTRE/_RIGHT.mov (ProRes 422 HQ,
-qscale:v 2) and a log line (ECC, drift).
"""
import argparse
import json
import os
import subprocess

import cv2
import numpy as np

from s7_worldfill import clean_edges, fill_world, horizon_cols

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/'
OW, OH = 4680, 1080
WALLS = (('LEFT', 0, 1440), ('CENTRE', 1440, 3240), ('RIGHT', 3240, 4680))


def probe(p):
    j = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                            '-show_entries', 'stream=width,height,nb_read_frames', '-of', 'json', p]))
    s = j['streams'][0]
    return s['width'], s['height'], int(s['nb_read_frames'])


def read_frames(p, w, h):
    pr = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', p, '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'],
                          stdout=subprocess.PIPE)
    n = w * h * 3
    out = []
    while True:
        b = pr.stdout.read(n)
        if len(b) < n:
            break
        out.append(np.frombuffer(b, np.uint8).reshape(h, w, 3))
    return out


def read_audio(p, sr=48000):
    try:
        b = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '2', '-ar', str(sr), '-f', 'f32le', '-'])
        return np.frombuffer(b, np.float32).reshape(-1, 2).copy()
    except subprocess.CalledProcessError:
        return None


def ecc(frame, can, mask=None):
    g1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY).astype(np.float32)
    g0 = cv2.cvtColor(can, cv2.COLOR_BGR2GRAY).astype(np.float32)
    M = np.eye(2, 3, dtype=np.float32)
    cc, M = cv2.findTransformECC(g0, g1, M, cv2.MOTION_AFFINE,
                                 (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-7), mask, 5)
    return cc, M


def band(img):
    """the canvas's own band (rows 479..1559 of 2038), whatever the clip's size or aspect, resized to 4680x1080"""
    h = img.shape[0]
    y0, y1 = int(round(h * 479 / 2038)), int(round(h * 1559 / 2038))
    return cv2.resize(img[y0:y1], (OW, OH), interpolation=cv2.INTER_LANCZOS4)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('clip'); ap.add_argument('state'); ap.add_argument('outdir')
    ap.add_argument('--xfade', type=float, default=1.5)
    ap.add_argument('--roll', type=float, default=0.6, help='deg, the horizon'); ap.add_argument('--heave', type=float, default=8.0, help='px, the horizon')
    ap.add_argument('--shake', type=float, default=0.6, help='px, the whole frame'); ap.add_argument('--tag', default='')
    ap.add_argument('--sky-harmony', type=int, default=0, help='horizon row: run ship_skyharmony on every frame (sunset: 448)')
    ap.add_argument('--fill-grow', type=int, default=5, help='px at 4680: the clip ship is dilated this much before the fill')
    ap.add_argument('--mask', default=None, help='bgmask suffix in 5_layers/seamed_v2/<state>/ (default _bgmask_v2; '
                    '--world: _bgmask_v3, the true silhouette)')
    ap.add_argument('--frames', type=int, default=0, help='render only the first N loop frames (tests)')
    ap.add_argument('--world', action='store_true', help='v3: CLIP is the ship-free sea plate take (no fill)')
    a = ap.parse_args()
    a.mask = a.mask or ('_bgmask_v3' if a.world else '_bgmask_v2')
    st = a.state
    w, h, n = probe(a.clip)
    fr = read_frames(a.clip, w, h)
    n = len(fr)
    ref = f'9_seaplate/S7-SEA-PLATE_{st}_reg.png' if a.world else f'7_canvas21/S7-SHIP-CANVAS21_{st}.png'
    can = cv2.resize(cv2.imread(T + ref), (w, h), interpolation=cv2.INTER_AREA)
    em = None
    if a.world:                                      # the swell moves: register on the sky and the horizon line only
        em = np.zeros((h, w), np.uint8); em[:int(h * (479 + 470) / 2038)] = 255
    c0, M0 = ecc(fr[0], can, em); c1, M1 = ecc(fr[-1], can, em)
    if a.world:                                      # the clouds drift ON PURPOSE and would drag a last-frame fit; the
        M1 = M0                                      # horizon of the sea take is steady (9 Oct draft: within 1 px)
    drift = float(np.abs(M1 - M0)[:, 2].max())
    print(f'{st}: ECC first {c0:.4f} last {c1:.4f}; drift {drift:.2f} px at {w}x{h}')
    still = np.hstack([cv2.imread(T + f'3_walls/seamed_v2/{st}/S7-SHIP-{x}_1080.png') for x, _, _ in WALLS]).astype(np.float32)
    bgu = np.hstack([cv2.imread(T + f'5_layers/seamed_v2/{st}/S7-SHIP-{x}_1080{a.mask}.png', 0) for x, _, _ in WALLS])
    _, Hc = horizon_cols(still.astype(np.uint8), bgu)
    if a.world:                                      # no pale rim of baked-in canvas sky on the ship's edge
        still, rim = clean_edges(still, bgu)
        print(f'{st}: ship edge cleaned on {rim.sum()} px')
    bg = cv2.GaussianBlur(bgu.astype(np.float32) / 255.0, (0, 0), 1.5)[..., None]
    # 1) every clip frame registered to the canvas (still at clip size), 2) the loop crossfade in clip space
    al = []
    for i, f in enumerate(fr):
        t = i / max(1, n - 1)
        M = (M0 * (1 - t) + M1 * t).astype(np.float32)
        al.append(cv2.warpAffine(f, M, (w, h), flags=cv2.INTER_LANCZOS4 | cv2.WARP_INVERSE_MAP,
                                 borderMode=cv2.BORDER_REFLECT_101))   # v2: REPLICATE smeared the edge into streaks
    X = int(round(a.xfade * 24)); L = n - X
    seq = [cv2.addWeighted(al[L + i], 1 - (i + 1) / (X + 1), al[i], (i + 1) / (X + 1), 0) if i < X else al[i]
           for i in range(L)]
    f0 = al[0].copy()
    del al, fr

    # 3) the ship's motion (Homie 7 Oct: "we are on the ship and it cannot be super stable"): roll + heave + a small
    #    shake, every term a whole number of cycles over the loop so the file still loops; zero at frame 0
    def motion(i):
        u = 2 * np.pi * i / L
        roll = a.roll * (0.8 * np.sin(u) + 0.2 * np.sin(2 * u + 1.3) - 0.2 * np.sin(1.3))
        heave = a.heave * (0.7 * np.sin(u + 0.9) + 0.3 * np.sin(3 * u + 0.4) - 0.7 * np.sin(0.9) - 0.3 * np.sin(0.4))
        ks = (9, 13, 17, 23); ph = (0.3, 1.9, 4.1, 2.7)
        sx = a.shake * sum(np.sin(k * u + p) - np.sin(p) for k, p in zip(ks, ph)) / len(ks)
        sy = a.shake * sum(np.sin(k * u + p + 1.1) - np.sin(p + 1.1) for k, p in zip(ks, ph)) / len(ks)
        return roll, heave, sx

    def motion_v(i):
        u = 2 * np.pi * i / L
        ks = (9, 13, 17, 23); ph = (0.3, 1.9, 4.1, 2.7)
        return a.shake * sum(np.sin(k * u + p + 1.1) - np.sin(p + 1.1) for k, p in zip(ks, ph)) / len(ks)

    CH, B0 = 2038, 479
    # the hole in the WORLD layer: the ship (grown), and everything under the band (the near deck); sky above the band
    hole = np.zeros((CH, OW), bool); hole[B0 + OH:] = True
    if a.fill_grow:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * a.fill_grow + 1,) * 2)
        hole[B0:B0 + OH] = cv2.dilate((bgu < 128).astype(np.uint8), k).astype(bool)
    else:
        hole[B0:B0 + OH] = bgu < 128
    Hfull = Hc + B0                                    # per column: sky fills sky, sea fills sea (mirrored from above)
    HK = None
    if a.sky_harmony:
        import sys as _s; _s.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from ship_skyharmony import harmonise
        kk = np.load(T + f'3_walls/seamed_v2/{st}/SKYHARMONY_k.npy'); HK = {'L': kk[0], 'R': kk[1]}
    G = None
    if a.world:                                      # the take's grade drifts from its start frame (9 Oct day: a touch
        # turquoise): one smooth gain, frame 0 -> the plate (canvas-matched), by distance to the horizon (rows) and slowly
        # sideways; the take's colour is steady over its 8 s (checked), so the same gain serves every frame
        pl = cv2.imread(T + f'9_seaplate/S7-SEA-PLATE_{st}_reg.png').astype(np.float32)
        f0f = cv2.resize(f0, (OW, 2038), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
        ab = lambda x: cv2.GaussianBlur(x, (0, 0), sigmaX=200, sigmaY=6)
        G = np.clip(ab(pl) / np.maximum(ab(f0f), 1), 0.8, 1.25)
        G = cv2.GaussianBlur(G, (0, 0), sigmaX=60, sigmaY=4)
        print(f'{st}: take -> plate gain {G.reshape(-1, 3).mean(0).round(3)} (B,G,R mean), {G.min():.2f}..{G.max():.2f}')
    S = 1.0 + (a.roll * np.pi / 180 * 540 + 4) / 2340 if a.roll else 1.0   # covers the outer corners under the roll
    def frame_out(i):
        # the camera is fixed to the ship: the DECK stays put, the WORLD (sea + sky) rolls and heaves behind it
        # (Homie 7 Oct: "the water horizon might move… according to how the ship will move")
        full = cv2.resize(seq[i], (OW, CH), interpolation=cv2.INTER_LANCZOS4)
        if a.sky_harmony:                            # ONE sky across the walls (tools/ship_skyharmony.py), k from the still
            E = 64
            reg = full[B0 - E:B0 + OH]
            bgx = np.vstack([np.ones((E, OW), np.float32), bg[..., 0]])
            full[B0 - E:B0 + OH] = harmonise(reg, bgx, a.sky_harmony + E, k=HK)[0]
        if not a.world:
            full = fill_world(full, hole, Hfull)       # NO ship in the world layer: only sea + sky roll
        else:
            full = full.astype(np.float32) * G
        r, dy, dx = motion(i)
        M = cv2.getRotationMatrix2D((OW / 2, CH / 2), r, S)
        M[1, 2] += dy - B0
        world = cv2.warpAffine(full, M, (OW, OH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
        comp = np.clip(world * bg + still * (1 - bg), 0, 255).astype(np.uint8)
        if a.shake:                                  # the ship's own small vibration moves everything, deck included
            V = np.float32([[1, 0, dx], [0, 1, motion_v(i)]])
            comp = cv2.warpAffine(comp, V, (OW, OH), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT)
        return comp

    au = read_audio(a.clip)
    os.makedirs(a.outdir, exist_ok=True)
    wav = os.path.join(a.outdir, f'_tmp_{st}.f32')
    if au is not None:
        sr = 48000; La = int(round(L / 24 * sr)); Xa = int(round(X / 24 * sr))
        au = au[:La + Xa] if len(au) >= La + Xa else np.pad(au, ((0, La + Xa - len(au)), (0, 0)))
        lo = au[:La].copy(); s = np.linspace(0, 1, Xa, dtype=np.float32)[:, None]
        lo[:Xa] = au[La:La + Xa] * (1 - s) + au[:Xa] * s
        lo.astype(np.float32).tofile(wav)
    base = os.path.join(a.outdir, f'S7-SHIP-IDLE_{st}{a.tag}')
    ain = ['-f', 'f32le', '-ar', '48000', '-ac', '2', '-i', wav] if au is not None else []
    amap = ['-map', '1:a', '-c:a'] if au is not None else []

    def enc(path, vcodec, crop=None):
        W = crop[2] - crop[1] if crop else OW
        cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{OH}', '-r', '24', '-i', '-']
        cmd += ain + ['-map', '0:v'] + (amap + (['aac', '-b:a', '256k'] if vcodec == 'h264' else ['pcm_s16le']) if amap else [])
        if vcodec == 'h264':
            cmd += ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-movflags', '+faststart']
        else:
            cmd += ['-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-pix_fmt', 'yuv422p10le']
        cmd += ['-shortest', path]
        return subprocess.Popen(cmd, stdin=subprocess.PIPE)

    procs = [enc(base + '_3walls_LOOP.mp4', 'h264')] + [enc(base + f'_{wl[0]}.mov', 'prores', wl) for wl in WALLS]
    first = last = None
    for i in range(a.frames or L):
        f = frame_out(i)
        first = f if first is None else first; last = f
        procs[0].stdin.write(f.tobytes())
        for p, wl in zip(procs[1:], WALLS):
            p.stdin.write(np.ascontiguousarray(f[:, wl[1]:wl[2]]).tobytes())
    for p in procs:
        p.stdin.close(); p.wait()
    if au is not None:
        os.remove(wav)
    j = np.abs(last.astype(np.float32) - first.astype(np.float32)).mean()
    print(f'{st}: loop {L} frames ({L / 24:.2f} s), xfade {X}; last->first step MAD {j:.2f} -> {base}_*')


if __name__ == '__main__':
    main()
