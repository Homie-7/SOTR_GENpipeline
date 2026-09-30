"""Check a 4K file against the approved 1080 file it was made from, streaming (a 4K show file does not fit in RAM).

  python tools/upscale_check.py SOURCE_1080 UPSCALE_4K

Prints: frame counts and size; PSNR of the 4K brought back to source size (fidelity); geometry shift every 40 f
(phase correlation, px, must be ~0; near-black frames skipped); detail gain (Laplacian variance, 4K vs the source upscaled bicubically);
motion (mean frame-to-frame step, 4K brought back vs source: ratio ~1.00 = the same flicker and events);
motion again on the low band only (light and events without grain: the restore keeps the source's low band, so
this ratio should be ~1.00 even when grain makes the full-band ratio lower); sound (correlation of the two files' audio, 1.000 = identical). Same metrics as the 2026-09-30 checks (LOG).
"""
import subprocess
import sys

import cv2
import numpy as np


def audio(p):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vn', '-ac', '1', '-ar', '8000', '-f', 's16le', '-'],
                         capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32)


def main():
    src, up = sys.argv[1], sys.argv[2]
    cs, cu = cv2.VideoCapture(src), cv2.VideoCapture(up)
    ps, shifts, lap_s, lap_u, fl_s, fl_u, lo_s, lo_u = [], [], [], [], [], [], [], []
    prev_s = prev_d = None
    i = 0
    while True:
        oks, s = cs.read()
        oku, u = cu.read()
        if not (oks and oku):
            break
        h, w = s.shape[:2]
        sf = s.astype(np.float32)
        d = cv2.resize(u, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32)
        mse = ((sf - d) ** 2).mean()
        ps.append(10 * np.log10(255 ** 2 / max(mse, 1e-6)))
        if i % 40 == 0:
            (dx, dy), resp = cv2.phaseCorrelate(cv2.cvtColor(sf, cv2.COLOR_BGR2GRAY), cv2.cvtColor(d, cv2.COLOR_BGR2GRAY))
            if resp > 0.2:  # a near-black frame gives no peak (it reports half the frame); skip it
                shifts.append((round(dx, 2), round(dy, 2)))
            big = cv2.resize(s, (u.shape[1], u.shape[0]), interpolation=cv2.INTER_CUBIC)
            lap_s.append(cv2.Laplacian(cv2.cvtColor(big, cv2.COLOR_BGR2GRAY), cv2.CV_32F).var())
            lap_u.append(cv2.Laplacian(cv2.cvtColor(u, cv2.COLOR_BGR2GRAY), cv2.CV_32F).var())
        ls, ld = cv2.GaussianBlur(sf, (0, 0), 3), cv2.GaussianBlur(d, (0, 0), 3)
        if prev_s is not None:
            fl_s.append(np.abs(sf - prev_s).mean())
            fl_u.append(np.abs(d - prev_d).mean())
            lo_s.append(np.abs(ls - prev_ls).mean())
            lo_u.append(np.abs(ld - prev_ld).mean())
        prev_s, prev_d, prev_ls, prev_ld = sf, d, ls, ld
        size = (u.shape[1], u.shape[0])
        i += 1
    # count what is left in either file (a mismatch is a fail)
    rest_s = rest_u = 0
    while cs.read()[0]:
        rest_s += 1
    while cu.read()[0]:
        rest_u += 1
    print('frames src/up %d/%d  size %dx%d' % ((i + rest_s, i + rest_u) + size))
    ps = np.array(ps)
    print('PSNR vs source (downscaled back): mean %.2f  min %.2f (frame %d)' % (ps.mean(), ps.min(), ps.argmin()))
    if shifts:
        print('geometry shift px every 40 f (%d usable): max |dx| %.2f  max |dy| %.2f' %
              (len(shifts), max(abs(a) for a, _ in shifts), max(abs(b) for _, b in shifts)))
    else:
        print('geometry shift: no usable frame (all too dark for phase correlation)')
    print('detail (Laplacian var) bicubic-src %.1f vs upscale %.1f  (x%.2f)' %
          (np.mean(lap_s), np.mean(lap_u), np.mean(lap_u) / max(np.mean(lap_s), 1e-6)))
    fl_s, fl_u = np.array(fl_s), np.array(fl_u)
    print('motion: frame step src %.3f  up %.3f  ratio %.3f; corr %.4f; worst excess frame %d' %
          (fl_s.mean(), fl_u.mean(), fl_u.mean() / fl_s.mean(), np.corrcoef(fl_s, fl_u)[0, 1],
           int(np.argmax(fl_u - fl_s)) + 1))
    lo_s, lo_u = np.array(lo_s), np.array(lo_u)
    print('motion, low band (blur 3 px: light and events, not grain): ratio %.3f; corr %.4f' %
          (lo_u.mean() / lo_s.mean(), np.corrcoef(lo_s, lo_u)[0, 1]))
    a, b = audio(src), audio(up)
    n = min(len(a), len(b))
    if n and a[:n].std() > 0 and b[:n].std() > 0:
        print('sound: %.1f s vs %.1f s, corr %.4f' % (len(a) / 8000, len(b) / 8000, np.corrcoef(a[:n], b[:n])[0, 1]))
    else:
        print('sound: MISSING or silent (src %d samples, up %d)' % (len(a), len(b)))


if __name__ == '__main__':
    main()
