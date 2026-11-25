"""S5 cannonball option B, method F48 "GLOW BRIDGE + ONE WIDE TAKE" (0 cr). See docs/S5-CANNON-F48-METHOD.md section 3.

A. Before impact: the REAL camps show files on all four walls (the last NPRE frames of each, no generated frames). The ball is keyed
   from the wide take (take minus its own f0, a dark disc) and composited onto the real CENTRE frames.
B. Impact: ONE warm glow, computed in ONE stage coordinate space (LEFT | CENTRE | RIGHT side by side, FLOOR below CENTRE), grows from
   the impact point over every wall in ~4 frames and peaks near-white on the SAME frames on all walls. Every wall cuts to the take
   under the peak.
C. After the cut: the wide take cut into contiguous windows. LEFT | CENTRE | RIGHT = three thirds of the top band of the take (each
   third stretched 1.5x horizontally to 16:9); FLOOR = the take below the band, under the CENTRE third, NOT flipped.
D. End: eased fade to black over the last FADE frames (the S6 files fade in from black).
E. Sound: the take's own sound on every wall file (silence under the camps tail, as cannon_mirror.py).

Timeline (output 25 fps = camps rate; the take plays 1 frame per output frame, i.e. 24 -> 25 fps):
  out o < TAIL                 camps frames NCAMPS-NPRE+o, no ball
  TAIL <= o < cut              camps frames + keyed ball from take frame o-TAIL
  o >= cut                     take frame o-TAIL in windows
  The camps picture runs unbroken to the cut, so this file overlays the last NPRE frames of the camps show files.

usage: python tools/cannon_glow.py TAKE OUTDIR [--tail 3.0] [--fade 25] [--impact N] [--name S5-CANNON-GLOW]
"""
import argparse, os, subprocess
import numpy as np, cv2

MEDIA = os.environ.get('SOTR_MEDIA', 'C:/Users/Homie/Documents/SOTR_MEDIA').replace('\\', '/')  # set SOTR_MEDIA to work off the T9 on another computer
CAMPS = f'{MEDIA}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05_the-camps'
S6 = f'{MEDIA}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars'
W, H, FPS = 1920, 1080, 25
NCAMPS = 10770
WALLS = ('LEFT', 'CENTRE', 'RIGHT', 'FLOOR')
GLOW = np.array([205, 240, 255], np.float32)  # BGR warm yellow-white
# wall origin in stage pixels (x, y): one coordinate space for the glow
ORIGIN = {'LEFT': (-W, 0), 'CENTRE': (0, 0), 'RIGHT': (W, 0), 'FLOOR': (0, H)}


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                          '-of', 'csv=p=0', path], capture_output=True, text=True, check=True).stdout.strip()
    return tuple(int(v) for v in out.split(',')[:2])


def read(path, ss=None, n=None, size=None):
    w, h = size or probe(path)
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None:
        cmd += ['-ss', f'{ss:.4f}']
    cmd += ['-i', path]
    if n:
        cmd += ['-frames:v', str(n)]
    cmd += ['-vf', f'scale={w}:{h}:flags=lanczos', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)


def luma(f):
    return float(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).mean())


class Geo:
    """Take <-> wall mapping. Band = top bh rows of the take; thirds of width tw; FLOOR = rows bh..th under the CENTRE third."""

    def __init__(self, tw_, th_):
        self.tw, self.th = tw_, th_
        self.w3 = tw_ / 3.0
        self.bh = self.w3 * 1.5 * 9 / 16
        assert self.bh < th_, 'take too flat for a 1.5x band'

    def window(self, f, wall):
        x0 = {'LEFT': 0, 'CENTRE': 1, 'RIGHT': 2, 'FLOOR': 1}[wall] * self.w3
        y0, y1 = (self.bh, self.th) if wall == 'FLOOR' else (0, self.bh)
        # affine crop+scale with sub-pixel origin, so the thirds stay exactly contiguous
        sx, sy = W / self.w3, H / (y1 - y0)
        m = np.float32([[sx, 0, -x0 * sx + (sx - 1) / 2], [0, sy, -y0 * sy + (sy - 1) / 2]])
        return cv2.warpAffine(f, m, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    def take_to_centre(self, x, y):
        return (x - self.w3) * W / self.w3, y * H / self.bh


def detect_impact(take, geo):
    """First frame where the centre third of the band jumps in luma (the powder flash), and its brightest point."""
    c = [luma(f[:int(geo.bh), int(geo.w3):int(2 * geo.w3)]) for f in take]
    base = np.median(c[:10])
    fi = next(i for i, v in enumerate(c) if v > base + 25)
    d = cv2.GaussianBlur(cv2.cvtColor(take[fi], cv2.COLOR_BGR2GRAY).astype(np.float32) -
                         cv2.cvtColor(take[0], cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 6)
    d[int(geo.bh):] = d[int(geo.bh):] * 0.5
    y, x = np.unravel_index(np.argmax(d), d.shape)
    return fi, (float(x), float(y)), c


def ball_alpha(take, k, fi):
    """Dark-disc key of the ball on take frame k: darker than take f0 and than the previous key frames' median sky."""
    f0 = cv2.cvtColor(take[0], cv2.COLOR_BGR2GRAY).astype(np.float32)
    g = cv2.cvtColor(take[k], cv2.COLOR_BGR2GRAY).astype(np.float32)
    d = cv2.GaussianBlur(f0 - g, (0, 0), 1.0)
    m = (d > 18).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n <= 1:
        return None
    # the ball = the darkest compact component (not a large redraw region)
    best, bscore = None, 0
    for i in range(1, n):
        area = st[i, cv2.CC_STAT_AREA]
        if area < 2 or area > 0.004 * m.size:
            continue
        score = d[lab == i].mean()
        if score > bscore:
            best, bscore = i, score
    if best is None:
        return None
    a = np.clip((d - 10) / 30, 0, 1) * cv2.dilate((lab == best).astype(np.uint8), np.ones((5, 5), np.uint8))
    return a.astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('take')
    ap.add_argument('out')
    ap.add_argument('--tail', type=float, default=3.0)
    ap.add_argument('--fade', type=int, default=25)
    ap.add_argument('--impact', type=int, default=None, help='take frame of the flash (auto if omitted)')
    ap.add_argument('--grow', type=int, default=4, help='frames for the glow to cover every wall')
    ap.add_argument('--hold', type=int, default=2, help='frames at the peak (the cut is on the first one)')
    ap.add_argument('--decay', type=int, default=8, help='frames for the glow to fall off over the take')
    ap.add_argument('--name', default='S5-CANNON-GLOW')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    take = read(a.take)
    nt, th_, tw_ = take.shape[:3]
    geo = Geo(tw_, th_)
    fi, (ix, iy), cl = detect_impact(take, geo)
    if a.impact is not None:
        fi = a.impact
    tail = int(round(a.tail * FPS))
    g0 = tail + fi - 1                # glow starts 1 frame before the take's flash frame
    cut = g0 + a.grow                 # first peak frame: every wall cuts here
    npre = cut                        # camps frames used (all of them real, up to the cut)
    n = tail + nt                     # output length: tail + every take frame
    # impact point in stage pixels (CENTRE coords)
    sx, sy = geo.take_to_centre(ix, iy)
    print(f'take {tw_}x{th_} {nt} f; band {geo.bh:.1f} rows; impact take f{fi} at ({ix:.0f},{iy:.0f}) -> CENTRE ({sx:.0f},{sy:.0f}); '
          f'glow out f{g0}..; cut out f{cut}; out {n} f', flush=True)

    # A: camps frames (the last npre of each show file) + the ball on CENTRE
    walls = {}
    for w in WALLS:
        fr = read(f'{CAMPS}/S5_{w}_camps.mov', ss=(NCAMPS - npre) / FPS, n=npre, size=(W, H))
        assert len(fr) == npre, (w, len(fr))
        walls[w] = [f for f in fr]
    camps_centre = [f.copy() for f in walls['CENTRE']]
    prev = None
    ball_frames = 0
    for o in range(tail, cut):
        k = o - tail
        if k >= fi:
            break
        al = ball_alpha(take, k, fi)
        if al is None:
            prev = None
            continue
        ac = geo.window(np.dstack([al] * 3), 'CENTRE')[..., 0]
        col = geo.window(take[k], 'CENTRE').astype(np.float32)
        # motion blur: half of the previous key, so a fast ball streaks
        if prev is not None:
            ac = np.maximum(ac, prev[0] * 0.5)
            col = np.where((ac > prev[0] * 0.5)[..., None], col, prev[1])
        prev = (ac, col)
        f = walls['CENTRE'][o].astype(np.float32)
        walls['CENTRE'][o] = (f * (1 - ac[..., None]) + col * ac[..., None]).astype(np.uint8)
        ball_frames += 1

    # C: windows of the take from the cut on
    for o in range(cut, n):
        f = take[o - tail]
        for w in WALLS:
            walls[w].append(geo.window(f, w))

    # B: ONE glow in stage space
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dist = {}
    for w in WALLS:
        ox, oy = ORIGIN[w]
        dist[w] = np.hypot(xx + ox - sx, yy + oy - sy)
    dmax = max(float(d.max()) for d in dist.values())
    feather = 0.35 * dmax
    for o in range(g0, min(n, cut + a.hold + a.decay)):
        t = o - g0
        if t < a.grow:                       # growth: radius from 0 to past the farthest corner, intensity eases up
            r = (dmax + feather) * ((t + 1) / a.grow) ** 0.8
            env = 0.55 + 0.4 * (t + 1) / a.grow
        elif t < a.grow + a.hold:
            r, env = 1e9, 0.95
        else:
            r = 1e9
            u = (t - a.grow - a.hold + 1) / a.decay
            env = 0.95 * (1 - u) ** 2
        for w in WALLS:
            kk = env * np.clip((r - dist[w]) / feather, 0, 1)
            if r >= 1e9:
                kk = np.full((H, W), env, np.float32)
            core = np.clip(1 - dist[w] / (0.5 * dmax), 0, 1) * 0.05  # a little hotter at the impact
            kk = np.clip(kk + core * (kk > 0), 0, 1)[..., None]
            f = walls[w][o].astype(np.float32)
            walls[w][o] = (f * (1 - kk) + GLOW * kk).astype(np.uint8)

    # D: eased fade to black
    for w in WALLS:
        for i in range(a.fade):
            kf = 1 - np.sin(np.pi / 2 * (i + 1) / a.fade) ** 2
            walls[w][n - a.fade + i] = (walls[w][n - a.fade + i].astype(np.float32) * kf).astype(np.uint8)

    # measure
    log = [f'take {a.take}', f'take {tw_}x{th_}, {nt} f; band {geo.bh:.1f} of {th_} rows; window {geo.w3:.1f}x{geo.bh:.1f} (band), '
           f'FLOOR {geo.w3:.1f}x{th_ - geo.bh:.1f}',
           f'out {n} f ({n / FPS:.2f} s) at {FPS} fps; camps frames used {npre} (from camps f{NCAMPS - npre}); tail {tail}',
           f'impact take f{fi} at take ({ix:.0f},{iy:.0f}) = CENTRE ({sx:.0f},{sy:.0f}); ball keyed on {ball_frames} frames',
           f'glow out f{g0}..f{cut + a.hold + a.decay - 1} (grow {a.grow}, hold {a.hold}, decay {a.decay}); CUT out f{cut} on ALL walls']
    for name, x, y in (('LEFT|CENTRE', 'LEFT', 'CENTRE'), ('CENTRE|RIGHT', 'CENTRE', 'RIGHT')):
        s = [np.abs(walls[x][i][:, -1].astype(int) - walls[y][i][:, 0].astype(int)).mean() for i in range(cut, n - a.fade)]
        inner = [np.abs(walls[y][i][:, 0].astype(int) - walls[y][i][:, 1].astype(int)).mean() for i in range(cut, n - a.fade)]
        log.append(f'{name} seam MAD after cut: mean {np.mean(s):.2f} max {max(s):.2f} (adjacent columns inside a wall: mean {np.mean(inner):.2f})')
    s = [np.abs(walls['CENTRE'][i][-1].astype(int) - walls['FLOOR'][i][0].astype(int)).mean() for i in range(cut, n - a.fade)]
    log.append(f'CENTRE bottom|FLOOR top seam MAD after cut: mean {np.mean(s):.2f} max {max(s):.2f}')
    for w in WALLS:
        lu = [luma(walls[w][i]) for i in range(g0 - 2, cut + a.hold + 4)]
        pk = g0 - 2 + int(np.argmax(lu))
        log.append(f'{w} glow peak out f{pk}; luma f{g0 - 2}..: {[int(v) for v in lu]}')
    mad = [np.abs(walls['CENTRE'][i].astype(int) - camps_centre[i].astype(int)).mean() for i in range(tail)]
    madb = [np.abs(walls['CENTRE'][i].astype(int) - camps_centre[i].astype(int)).mean() for i in range(tail, g0)]
    log.append(f'CENTRE pre-impact MAD vs camps: tail (no ball) max {max(mad):.3f}; ball frames mean {np.mean(madb):.3f} '
               f'max {max(madb):.3f} (ball pixels only)')
    top = [float((cv2.cvtColor(take[i][:int(geo.bh * 0.2)], cv2.COLOR_BGR2GRAY).astype(int) -
                  cv2.cvtColor(take[0][:int(geo.bh * 0.2)], cv2.COLOR_BGR2GRAY).astype(int)).__abs__().mean()) for i in range(nt)]
    cov = next((i for i in range(fi, nt) if top[i] > 30), None)
    log.append(f'take top-20% band MAD vs f0 > 30 from take f{cov} ({(cov or 0) / 24:.2f} s); min after it {min(top[cov:]) if cov else 0:.1f}')
    log.append(f'take end luma (last 5 f): {[int(luma(take[i])) for i in range(nt - 5, nt)]}')
    open(f'{a.out}/measure.txt', 'w').write('\n'.join(log) + '\n')
    print('\n'.join(log), flush=True)

    # E: sound = the take's own sound (silence under the camps tail), retimed 24 -> 25 fps
    aud = f'{a.out}/_take_sound.wav'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a.take, '-af', 'aresample=48000', '-ac', '2', aud], check=True)
    snd = f'{a.out}/_wall_sound.wav'
    filt = (f'[0:a]atempo={25 / 24:.6f}[q];anullsrc=r=48000:cl=stereo,atrim=0:{tail / FPS:.6f}[s];[s][q]concat=n=2:v=0:a=1,'
            f'apad,atrim=0:{n / FPS:.6f},afade=t=out:st={(n - a.fade) / FPS:.6f}:d={a.fade / FPS:.6f}[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', aud, '-filter_complex', filt, '-map', '[a]', snd], check=True)

    def enc(frames, path, w_, h_, sound=True):
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w_}x{h_}',
                              '-r', str(FPS), '-i', '-'] + (['-i', snd, '-map', '0:v', '-map', '1:a', '-c:a', 'aac', '-b:a', '192k']
                             if sound else []) + ['-c:v', 'libx264', '-crf', '16', '-preset', 'medium', '-pix_fmt', 'yuv420p', path],
                             stdin=subprocess.PIPE)
        for f in frames:
            p.stdin.write(np.ascontiguousarray(f).tobytes())
        p.stdin.close()
        p.wait()

    for w in WALLS:
        enc(walls[w], f'{a.out}/{a.name}_{w}.mp4', W, H)
    s6 = {w: read(f'{S6}/S6_{w}_wars.mov', n=75, size=(W, H)) for w in ('LEFT', 'CENTRE', 'RIGHT')}
    hs, ws = H // 2, W // 2

    def stage(l, c, r, f):
        o = np.zeros((H, W * 3 // 2, 3), np.uint8)
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
                    f'{a.out}/{a.name}_review_stage.mp4'], check=True)
    os.remove(f'{a.out}/_stage_nosound.mp4')
    # contact sheet: the ball fall, every glow frame, then every 12 frames
    idx = sorted(set(list(range(tail, g0, max(1, (g0 - tail) // 4))) + list(range(g0 - 1, cut + a.hold + a.decay, 2)) +
                     list(range(cut + a.hold + a.decay, n, 12))))[:32]
    tiles = [cv2.putText(cv2.resize(rev[i], (480, 360)), f'f{i}', (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
             for i in idx]
    while len(tiles) % 4:
        tiles.append(np.zeros_like(tiles[0]))
    cv2.imwrite(f'{a.out}/contact.jpg', np.vstack([np.hstack(tiles[i:i + 4]) for i in range(0, len(tiles), 4)]),
                [cv2.IMWRITE_JPEG_QUALITY, 85])
    print('DONE cannon_glow', a.out, flush=True)


if __name__ == '__main__':
    main()
