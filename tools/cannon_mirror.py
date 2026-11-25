"""S5 cannonball option B, method F47 "MIRROR TAKEOVER" (0 cr probe).

Why (Homie F46): four separate generations never read as ONE event (timing, seams, colour). So all four walls are
derived from ONE take (CENTRE probe v4):
  * Before the flash each wall plays its OWN camps picture (CENTRE: the take itself, which starts on the camps last frame).
  * On ONE frame (the take's white flash) every wall cuts to the blast. The flash hides the cut (the 2022 trick).
  * After the flash: LEFT = RIGHT = CENTRE mirrored left-right, FLOOR = CENTRE's lower band mirrored top-bottom.
    A mirror copy has the SAME pixel column on both sides of a seam, so every seam is continuous by construction,
    every wall is on the same frame (time alignment exact) and has the same grade (colour match exact).
    Mirrored motion runs outward from the centre on both side walls: right for a blast centred on CENTRE.
  * "Destroy the whole centre at once": after the flash the take plays FAST (speed ramp SPEED0 -> 1x by source frame
    RAMP_END, with frame blending for motion blur), so the smoke fills the walls within ~1 s.
  * End: the take ends in embers on near-black; an eased fade to black over the last FADE frames, because the S6 show
    files now fade in from black (F42/F43).

usage: python tools/cannon_mirror.py OUTDIR [--speed0 4] [--ramp-end 150] [--tail 3.0] [--fade 25] [--preroll reverse|loop]
Output (review drafts, 1920x1080, 25 fps = the camps rate): <WALL>_mirror.mp4 x4, review_stage.mp4 (LEFT|CENTRE|RIGHT over
FLOOR, then the S6 fade-in head), contact sheet, measure.txt (seam continuity + flash frame per wall).
"""
import argparse, os, subprocess
import numpy as np, cv2

MEDIA = 'C:/Users/Homie/Documents/SOTR_MEDIA'
CAMPS = f'{MEDIA}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05_the-camps'
S6 = f'{MEDIA}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars'
TAKE = f'{MEDIA}/04_WORKING_FILES/S5_cannonball/probe_v4/S5-CANNON-PROBE_v4_CENTRE_a2ab023e.mp4'
W, H, FPS = 1920, 1080, 25
NCAMPS = 10770
CUT = 33          # take frame where every wall cuts to the blast (take luma 211: near-white flash)
FLASH_END = 38    # take plays 1:1 through the flash
FLOOR_BAND = 0.55 # FLOOR = lower 55% of CENTRE, mirrored top-bottom (no sky on the floor)


def read(path, ss=None, n=None, scale=True):
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None:
        cmd += ['-ss', f'{ss:.4f}']
    cmd += ['-i', path]
    if n:
        cmd += ['-frames:v', str(n)]
    cmd += ['-vf', f'scale={W}:{H}:flags=lanczos' if scale else 'null', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def ramp_map(nsrc, speed0, ramp_end):
    """Source positions (float) for each output frame from CUT on. 1x through the flash, then speed0 easing to 1x."""
    pos, s = [], float(CUT)
    while s <= nsrc - 1:
        pos.append(s)
        if s < FLASH_END:
            v = 1.0
        else:
            t = min(1.0, (s - FLASH_END) / (ramp_end - FLASH_END))
            v = 1.0 + (speed0 - 1.0) * (1 - t * t * (3 - 2 * t))
        s += v
    return pos


def blend(src, a, b):
    """Mean of source frames covering [a, b) (motion blur for the fast part); single frame when b - a <= 1."""
    i0, i1 = int(np.floor(a)), max(int(np.floor(a)) + 1, int(np.ceil(b)))
    i1 = min(i1, len(src))
    if i1 - i0 <= 1:
        return src[min(i0, len(src) - 1)]
    return np.mean(src[i0:i1].astype(np.float32), 0).astype(np.uint8)


def floor_of(c):
    band = c[int(H * (1 - FLOOR_BAND)):]
    return cv2.resize(band, (W, H), interpolation=cv2.INTER_LINEAR)[::-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--speed0', type=float, default=4.0)
    ap.add_argument('--ramp-end', type=float, default=150)
    ap.add_argument('--tail', type=float, default=3.0)
    ap.add_argument('--fade', type=int, default=25)
    ap.add_argument('--preroll', default='reverse')
    ap.add_argument('--offsets', default='0,0,0', help='v2: source-frame time offsets for LEFT,RIGHT,FLOOR away from the seam')
    ap.add_argument('--band', type=float, default=0.3, help='v2: fraction of the wall over which the offset fades in from the seam')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    take = read(TAKE)
    ntail = int(round(a.tail * FPS))
    pre = CUT - 1  # take frames 1..CUT-1 run on CENTRE after the camps end, before the cut
    walls = {}
    for w in ('LEFT', 'CENTRE', 'RIGHT', 'FLOOR'):
        tail = read(f'{CAMPS}/S5_{w}_camps.mov', ss=(NCAMPS - ntail) / FPS, n=ntail)
        assert len(tail) == ntail, (w, len(tail))
        if w == 'CENTRE':
            ext = take[1:CUT]
        elif a.preroll == 'loop':
            ext = read(f'{CAMPS}/S5_{w}_camps.mov', n=pre)
        else:  # play back the last frames in reverse (a near-still camps picture; 1.3 s)
            ext = tail[-2:-2 - pre:-1]
        walls[w] = list(tail) + list(ext)
    pos = ramp_map(len(take), a.speed0, a.ramp_end)
    # v2: identical to the mirror AT the seam (continuity), a time-shifted mirror further out (breaks the kaleidoscope)
    offs = [float(x) for x in a.offsets.split(',')]
    ramp = lambda d: (lambda t: (t * t * (3 - 2 * t)))(np.clip(d / (a.band), 0, 1)).astype(np.float32)
    xs = np.arange(W) / (W - 1)
    wl = ramp(1 - xs)[None, :, None]                    # LEFT seam = its right edge
    wr = ramp(xs)[None, :, None]                        # RIGHT seam = its left edge
    wf = ramp(np.arange(H) / (H - 1))[:, None, None]    # FLOOR seam = its top edge

    def sidemix(m, o, wgt):
        if m is o:
            return m
        return (m.astype(np.float32) * (1 - wgt) + o.astype(np.float32) * wgt).astype(np.uint8)

    for k, p in enumerate(pos):
        q = pos[k + 1] if k + 1 < len(pos) else p + 1
        c = blend(take, p, q)
        walls['CENTRE'].append(c)
        oth = {}
        for name, o in zip(('LEFT', 'RIGHT', 'FLOOR'), offs):
            oth[name] = c if o == 0 else blend(take, min(p + o, len(take) - 1), min(q + o, len(take)))
        walls['LEFT'].append(sidemix(c[:, ::-1], oth['LEFT'][:, ::-1], wl))
        walls['RIGHT'].append(sidemix(c[:, ::-1], oth['RIGHT'][:, ::-1], wr))
        walls['FLOOR'].append(sidemix(floor_of(c), floor_of(oth['FLOOR']), wf))
    n = len(walls['CENTRE'])
    cut_out = ntail + pre
    # v2: the flash reaches every wall on the same frames (hides the cut on LEFT/RIGHT/FLOOR, the 2022 takeover)
    flash = np.array([200, 235, 255], np.float32)  # BGR warm white
    for i in range(cut_out - 1, cut_out + 8):
        lc = cv2.cvtColor(walls['CENTRE'][i], cv2.COLOR_BGR2GRAY).mean()
        k = float(np.clip((lc - 100) / 90, 0, 1)) * 0.85
        for w in ('LEFT', 'RIGHT', 'FLOOR'):
            if k > 0:
                walls[w][i] = (walls[w][i].astype(np.float32) * (1 - k) + flash * k).astype(np.uint8)
    for w in walls:
        f = walls[w]
        for i in range(a.fade):
            t = (i + 1) / a.fade
            k = 1 - np.sin(np.pi / 2 * t) ** 2
            f[n - a.fade + i] = (f[n - a.fade + i].astype(np.float32) * k).astype(np.uint8)
    # measure: seam continuity (mean abs diff of the facing edge columns) and the cut frame
    log = [f'frames {n} ({n / FPS:.2f} s) at {FPS} fps; camps tail {ntail}; cut to blast at out f{cut_out} '
           f'({cut_out / FPS:.2f} s) on ALL walls; take src for out frames: {[round(p, 1) for p in pos[:40]]} ...',
           f'speed0 {a.speed0} ramp_end {a.ramp_end} fade {a.fade} preroll {a.preroll} offsets {a.offsets} band {a.band}']
    for name, x, y in (('LEFT|CENTRE', walls['LEFT'], walls['CENTRE']), ('CENTRE|RIGHT', walls['CENTRE'], walls['RIGHT'])):
        seam = [np.abs(x[i][:, -1].astype(int) - y[i][:, 0].astype(int)).mean() for i in range(cut_out, n)]
        log.append(f'{name} seam MAD after cut: max {max(seam):.2f} mean {np.mean(seam):.2f}')
    sf = [np.abs(walls['CENTRE'][i][-1].astype(int) - walls['FLOOR'][i][0].astype(int)).mean() for i in range(cut_out, n)]
    log.append(f'CENTRE bottom|FLOOR top seam MAD after cut: max {max(sf):.2f} mean {np.mean(sf):.2f}')
    for w in walls:
        luma = [int(cv2.cvtColor(walls[w][i], cv2.COLOR_BGR2GRAY).mean()) for i in range(cut_out - 3, cut_out + 6)]
        log.append(f'{w} luma f{cut_out - 3}..f{cut_out + 5}: {luma}')
    open(f'{a.out}/measure.txt', 'w').write('\n'.join(log) + '\n')
    print('\n'.join(log))
    # sound: the take's own sound on every wall, retimed like the picture (camps rate + ramp), cut point aligned
    aud = f'{a.out}/_take_sound.wav'
    t0 = CUT / 24.0
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', TAKE, '-af', f'aresample=48000', '-ac', '2', aud], check=True)
    pre_s = cut_out / FPS
    take_s = len(pos) / FPS
    # pre-cut: silence for the tail, then take sound 1/24..CUT/24 at 25/24; post-cut: take sound from t0, squeezed to fit
    src_post = (len(take) - CUT) / 24.0
    tempo = src_post / take_s
    filt = (f'[0:a]atrim={1 / 24:.6f}:{t0},asetpts=PTS-STARTPTS,atempo={25 / 24:.6f}[p];'
            f'[0:a]atrim={t0},asetpts=PTS-STARTPTS,atempo={min(tempo, 2.0):.6f}' + (f',atempo={tempo / 2.0:.6f}' if tempo > 2 else '') + '[q];'
            f'anullsrc=r=48000:cl=stereo,atrim=0:{ntail / FPS:.6f}[s];[s][p][q]concat=n=3:v=0:a=1,'
            f'afade=t=out:st={(n - a.fade) / FPS:.6f}:d={a.fade / FPS:.6f},atrim=0:{n / FPS:.6f}[a]')
    snd = f'{a.out}/_wall_sound.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', aud, '-filter_complex', filt, '-map', '[a]', snd], check=True)

    def enc(frames, path, w_, h_, sound=True):
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w_}x{h_}',
                              '-r', str(FPS), '-i', '-'] + (['-i', snd, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k']
                             if sound else []) + ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', path], stdin=subprocess.PIPE)
        for f in frames:
            p.stdin.write(np.ascontiguousarray(f).tobytes())
        p.stdin.close()
        p.wait()

    for w in walls:
        enc(walls[w], f'{a.out}/S5-CANNON-MIRROR_{w}.mp4', W, H)
    # stage review: LEFT|CENTRE|RIGHT on top (960x540 each), FLOOR under CENTRE; then 3 s of the S6 fade-in heads
    s6 = {w: read(f'{S6}/S6_{w}_wars.mov', n=75) for w in ('LEFT', 'CENTRE', 'RIGHT')}
    blk = np.zeros((H, W * 3 // 2, 3), np.uint8)
    hs, ws = H // 2, W // 2

    def stage(l, c, r, f):
        o = blk.copy()
        o[:hs, :ws] = cv2.resize(l, (ws, hs), interpolation=cv2.INTER_AREA)
        o[:hs, ws:2 * ws] = cv2.resize(c, (ws, hs), interpolation=cv2.INTER_AREA)
        o[:hs, 2 * ws:] = cv2.resize(r, (ws, hs), interpolation=cv2.INTER_AREA)
        if f is not None:
            o[hs:, ws:2 * ws] = cv2.resize(f, (ws, hs), interpolation=cv2.INTER_AREA)
        return o

    rev = [stage(walls['LEFT'][i], walls['CENTRE'][i], walls['RIGHT'][i], walls['FLOOR'][i]) for i in range(n)]
    rev += [stage(s6['LEFT'][i], s6['CENTRE'][i], s6['RIGHT'][i], None) for i in range(75)]
    enc(rev, f'{a.out}/_stage_nosound.mp4', W * 3 // 2, H, sound=False)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{a.out}/_stage_nosound.mp4', '-i', snd, '-map', '0:v', '-map', '1:a',
                    '-c:v', 'copy', '-c:a', 'aac', '-af', 'apad', '-t', f'{len(rev) / FPS:.4f}',
                    f'{a.out}/S5-CANNON-MIRROR_review_stage.mp4'], check=True)
    os.remove(f'{a.out}/_stage_nosound.mp4')
    # contact sheet: every 10 frames from 6 before the cut
    idx = list(range(cut_out - 6, n, 10))[:24]
    tiles = [cv2.putText(cv2.resize(rev[i], (480, 360)), f'f{i}', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
             for i in idx]
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    rows = [np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]
    cv2.imwrite(f'{a.out}/contact.jpg', np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
    print('DONE cannon_mirror', a.out)


if __name__ == '__main__':
    main()
