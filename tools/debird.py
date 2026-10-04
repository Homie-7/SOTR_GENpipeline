"""Remove the birds from a locked-camera battlefield render, AFTER the grade (Scene 5 camps, Homie 2026-10-04: "get rid of
the birds in the whole camps scene… the obvious ones in the front circling need to go").

WHY a separate pass, not grade_battlefield's Despeck: Despeck compares each air pixel with its median over +-1 s and keeps
islands up to 1,500 px. The camps' near birds are big (up to ~60 px across) and circle slowly, so over +-1 s a bird can sit
on its own median and survive, and the camps sky also holds smoke drifting up from the plumes, which a looser Despeck would
start to eat. Here a bird is what is BOTH:
  - darker than the pixel's median over +-2 s (every 5th frame), after a high-pass (clouds and the light are broad), and
  - FAST: it changes within 3 frames (a bird flies and flaps; smoke and clouds creep), measured over the whole island,
inside the sky mask but outside the SMOKE MAP (smoke_map), as a compact island (<= 1,600 px, bbox <= 100 x 70 px full size), in CALM sky: the ring around it
barely departs from its median (test 2026-10-04: without that, a dark smoke puff popping out of a plume was taken). Its pixels (grown, feathered) are replaced by
the +-2 s median of the graded frames. Everything else is the input, bit for bit through the 16-bit path; ProRes 422 HQ
10-bit q2 out, the input's sound stream-copied. Written to a _tmp_ name, renamed on success.

  python tools/debird.py IN.mov OUT.mov SKYMASK.png [--start F --frames N]   (a test range: frames F..F+N-1, no sound)
"""
import os
import subprocess
import sys
from collections import deque

import cv2
import numpy as np

K, ST = 50, 5                 # +-50 frames (2 s at 25 fps), every 5th frame -> 21 samples for the median
FAST_GAP, FAST_THR = 3, 0.02  # "fast" = luma moves more than ~5/255 within 3 frames
DARK_THR = 0.035              # darker than the median by ~9/255 after the high-pass
MAX_AREA, MAX_W, MAX_H = 400, 50, 35   # half-res: the biggest real bird is ~60 x 30 px full size
R, RING_THR = 8, 0.012        # the ring 3-8 half-res px around an island must be still sky (mean |change| < ~3/255)
LUM = np.array([0.2126, 0.7152, 0.0722], np.float32)
SMOKE_IQR = 0.02              # smoke map: where the sky's broad brightness spreads (25th-75th pct) more than ~5/255


def smoke_map(src, W, y0, y1, hw, hh, cache):
    """Where smoke (or cloud) ever drifts: one frame a second over the WHOLE clip, half size, blurred; the spread between
    the 25th and 75th percentile per pixel of a band-pass (3-30 px: shapes, not the light slowly changing over minutes). A bird is there for a moment, so it barely moves the percentiles; smoke that
    rolls through a place for minutes does. Grown 12 px. Nothing inside it is touched. Cached as a PNG beside the output."""
    if os.path.exists(cache):
        return cv2.imread(cache, 0) > 0
    cmd = ['ffmpeg', '-v', 'error', '-i', src, '-vf', 'select=not(mod(n\\,25)),' + f'crop={W}:{y1 - y0}:0:{y0},'
           f'scale={hw}:{hh}:flags=area,format=gray16le', '-fps_mode', 'passthrough', '-f', 'rawvideo', '-']
    pr = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    fs = []
    while True:
        b = pr.stdout.read(hw * hh * 2)
        if len(b) < hw * hh * 2:
            break
        g = np.frombuffer(b, np.uint16).reshape(hh, hw).astype(np.float32) / 65535
        fs.append(cv2.GaussianBlur(g, (0, 0), 3) - cv2.GaussianBlur(g, (0, 0), 30))   # band-pass: the light's slow drift out
    pr.wait()
    q25, q75 = np.percentile(np.stack(fs), [25, 75], axis=0)
    m = cv2.dilate(((q75 - q25) > SMOKE_IQR).astype(np.uint8), np.ones((25, 25), np.uint8))
    cv2.imwrite(cache, m * 255)
    print(f'smoke map: {len(fs)} samples, {m.mean() * 100:.1f}% of the sky band protected -> {cache}', flush=True)
    return m > 0


def probe(p):
    o = subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=width,height,r_frame_rate', '-of', 'csv=p=0', p]).decode().strip().split(',')
    return int(o[0]), int(o[1]), o[2]


def main():
    src, out, mpath = sys.argv[1:4]
    a = sys.argv[4:]
    start = int(a[a.index('--start') + 1]) if '--start' in a else 0
    nmax = int(a[a.index('--frames') + 1]) if '--frames' in a else None
    W, H, fps = probe(src)
    sky = cv2.resize(cv2.imread(mpath, 0), (W, H)) > 90
    rows = np.nonzero(sky.any(1))[0]
    y0, y1 = int(rows.min()), int(rows.max()) + 1
    skyb = sky[y0:y1]
    hw, hh = W // 2, (y1 - y0) // 2
    skyh = cv2.resize(skyb.astype(np.uint8), (hw, hh), interpolation=cv2.INTER_NEAREST) > 0
    skyh &= ~smoke_map(src, W, y0, y1, hw, hh, os.path.join(os.path.dirname(out) or '.', os.path.splitext(os.path.basename(src))[0] + '_smokemap.png'))

    rd = ['ffmpeg', '-v', 'error']
    if start:
        rd += ['-ss', '%.6f' % (start * eval(fps.replace('/', '*1.0/')) ** -1)]
    rd += ['-i', src, '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-']
    rp = subprocess.Popen(rd, stdout=subprocess.PIPE)
    tmp = os.path.join(os.path.dirname(out) or '.', '_tmp_' + os.path.basename(out))
    wr = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}', '-r', fps, '-i', '-']
    if nmax is None:
        wr += ['-i', src, '-map', '0:v', '-map', '1:a?', '-c:a', 'copy']
    wr += ['-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-pix_fmt', 'yuv422p10le', '-vendor', 'apl0', tmp]
    wp = subprocess.Popen(wr, stdin=subprocess.PIPE)

    fb = W * H * 6
    full, band, lum = deque(), deque(), deque()        # full frames (uint16), the sky band (uint16), half-res luma
    base, n_in, n_out, changed, hit_frames = 0, 0, 0, 0, 0
    done = False
    while True:
        if not done and (nmax is None or n_in < nmax):
            b = rp.stdout.read(fb)
            if len(b) < fb:
                done = True
            else:
                f = np.frombuffer(b, np.uint16).reshape(H, W, 3)
                full.append(f)
                bd = f[y0:y1]
                band.append(bd)
                lum.append(cv2.resize((bd.astype(np.float32) / 65535) @ LUM, (hw, hh), interpolation=cv2.INTER_AREA))
                n_in += 1
        else:
            done = True
        # emit frame n_out once frames up to n_out+K are in (or the input ended)
        while n_out < n_in and (done or n_in > n_out + K):
            i = n_out - base
            g = full[i]
            idx = [j for j in range(n_out - K, n_out + K + 1, ST) if base <= j < n_in]
            L = lum[i]
            med = np.median(np.stack([lum[j - base] for j in idx]), 0)
            d = L - med
            hp = d - cv2.GaussianBlur(d, (0, 0), 5)
            dark = ((hp < -DARK_THR) & skyh).astype(np.uint8)
            nb = [j for j in (n_out - FAST_GAP, n_out + FAST_GAP) if base <= j < n_in]
            fast = np.max(np.stack([np.abs(L - lum[j - base]) for j in nb]), 0) > FAST_THR if nb else np.zeros_like(dark, bool)
            nl, lab, st, _ = cv2.connectedComponentsWithStats(dark, connectivity=8)
            keep = np.zeros(nl, bool)
            ad = np.abs(d)
            for c in range(1, nl):
                x, y, w, h, area = st[c]
                if area < 2 or area > MAX_AREA or w > MAX_W or h > MAX_H:
                    continue
                isl = lab[y:y + h, x:x + w] == c
                if fast[y:y + h, x:x + w][isl].mean() < 0.3:
                    continue
                # calm surroundings: a bird crosses still sky; a puff of smoke sits in moving smoke
                X0, Y0, X1, Y1 = max(0, x - R), max(0, y - R), min(hw, x + w + R), min(hh, y + h + R)
                isl = lab[Y0:Y1, X0:X1] == c
                ring = cv2.dilate(isl.astype(np.uint8), np.ones((2 * R + 1, 2 * R + 1), np.uint8)).astype(bool)
                ring &= ~cv2.dilate(isl.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(bool)
                if ad[Y0:Y1, X0:X1][ring].mean() < RING_THR and (dark[Y0:Y1, X0:X1][ring] > 0).mean() < 0.05:
                    keep[c] = True
            m = keep[lab]
            if m.any():
                mf = cv2.resize(m.astype(np.uint8), (W, y1 - y0), interpolation=cv2.INTER_NEAREST)
                mf = cv2.dilate(mf, np.ones((9, 9), np.uint8)).astype(np.float32)
                mf = cv2.GaussianBlur(mf, (0, 0), 2.0) * skyb
                ys, xs = np.nonzero(mf > 0.01)
                rep = np.median(np.stack([band[j - base][ys, xs] for j in idx]), 0).astype(np.float32)
                cur = g[y0:y1][ys, xs].astype(np.float32)
                w_ = mf[ys, xs][:, None]
                g = g.copy()
                g[y0 + ys, xs] = np.clip(cur * (1 - w_) + rep * w_ + 0.5, 0, 65535).astype(np.uint16)
                changed += int(m.sum()) * 4
                hit_frames += 1
            wp.stdin.write(g.tobytes())
            n_out += 1
            if n_out % 1500 == 0:
                print(f'{os.path.basename(out)}: {n_out} frames, birds in {hit_frames}', flush=True)
            while base < n_out - K:
                full.popleft(); band.popleft(); lum.popleft(); base += 1
        if done and n_out >= n_in:
            break
    rp.stdout.close()
    rp.terminate()
    wp.stdin.close()
    if wp.wait() != 0:
        sys.exit('encoder failed')
    os.replace(tmp, out)
    print(f'{os.path.basename(out)}: wrote {n_out} frames; birds removed in {hit_frames} frames '
          f'({changed} px, {changed / max(n_out, 1):.0f} px/frame)', flush=True)


if __name__ == '__main__':
    main()
