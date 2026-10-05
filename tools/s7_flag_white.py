"""Paint the generated masthead flag of S7-INTRO-FLIGHT v2 (a red/white/blue, Union-Jack-like flag: wrong for a French
ship of 1816, whose flag is the plain white Bourbon) WHITE, by script.
  python flag_white.py IN.mp4 OUT.mov [--sheet SHEET.jpg]
Track: per frame (F0..F1), pink-not-brown pixels in Lab (a >= 5, a >= b + 3, L > 110) are grouped; the flag is the group
nearest the previous frame's flag (seeded at f168 by its known position), within 30 px. Inside its box (+8 px), pixels
that differ from the local sky (a/b distance > 4 or L more than 15 under it) and are not dark spars (L >= 90) are
replaced by a warm white (the sky's L - 3, a = sky a, b = sky b + 5: the sails' tint), feathered 1.5 px. Every other
pixel and frame is untouched (bit-identical decode). ProRes 422 HQ q2 + the source audio.
"""
import subprocess, sys
import numpy as np, cv2

F0, F1, SEED = 156, 285, (962 + 5, 294 + 4)

def comps(f):
    lab = cv2.cvtColor(f[:640], cv2.COLOR_BGR2LAB).astype(int)
    L, a, b = lab[..., 0], lab[..., 1] - 128, lab[..., 2] - 128
    m = ((a >= 5) & (a >= b + 3) & (L > 110)).astype(np.uint8)
    k, lb, st, cen = cv2.connectedComponentsWithStats(cv2.dilate(m, np.ones((5, 5), np.uint8)))
    return [(st[i], cen[i]) for i in range(1, k) if st[i, 4] >= 6]

def paint(f, box):
    x0, y0, x1, y1 = box
    roi = f[y0:y1, x0:x1]
    lab = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB).astype(np.float32)
    border = np.concatenate([lab[0], lab[:, 0], lab[:, -1]])
    sky = border[border[:, 0] >= np.percentile(border[:, 0], 70)].mean(0)
    dab = np.hypot(lab[..., 1] - sky[1], lab[..., 2] - sky[2])
    m = (((dab > 4) | (lab[..., 0] < sky[0] - 15)) & (lab[..., 0] >= 90)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.5)
    hard = m > 0.5
    mu = lab[..., 0][hard].mean() if hard.any() else sky[0]
    tgt = np.empty_like(lab)
    tgt[..., 0] = sky[0] - 3 + 0.3 * (lab[..., 0] - mu)   # keep a little of the cloth's shading (its folds)
    tgt[..., 1] = sky[1]
    tgt[..., 2] = sky[2] + 5
    out = lab * (1 - m[..., None]) + tgt * m[..., None]
    g = f.copy()
    g[y0:y1, x0:x1] = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    return g

def main():
    inp, outp = sys.argv[1], sys.argv[2]
    sheet = sys.argv[sys.argv.index('--sheet') + 1] if '--sheet' in sys.argv else None
    c = cv2.VideoCapture(inp)
    W, H = int(c.get(3)), int(c.get(4))
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', '24',
                          '-i', '-', '-i', inp, '-map', '0:v', '-map', '1:a', '-c:v', 'prores_ks', '-profile:v', '3',
                          '-qscale:v', '2', '-pix_fmt', 'yuv422p10le', '-c:a', 'pcm_s16le', outp], stdin=subprocess.PIPE)
    prev = np.array(SEED, float); n = 0; log = []; shots = []; lastbox = None; vel = np.zeros(2)
    while True:
        ok, f = c.read()
        if not ok:
            break
        if F0 <= n <= F1 and prev is not None:
            cs = comps(f)
            best = None
            for st, cen in cs:
                d = np.hypot(*(cen - prev))
                if d < 30 and (best is None or d < best[0]):
                    best = (d, st, cen)
            if best:
                _, st, cen = best
                x, y, w, h = st[:4]
                box = (max(0, x - 8), max(0, y - 8), min(W, x + w + 8), min(H, y + h + 8))
                vel = cen - prev
            elif log and log[-1] == n - 1 and lastbox is not None:
                # a frame where the detector missed: reuse the last box, moved on by the last step (no 1-frame flash)
                dx, dy = int(round(vel[0])), int(round(vel[1]))
                x0, y0, x1, y1 = lastbox
                box = (max(0, x0 + dx), max(0, y0 + dy), min(W, x1 + dx), min(H, y1 + dy))
                cen = prev + vel
                best = True
            if best:
                g = paint(f, box); lastbox = box
                if sheet and n % 12 == 0:
                    x0, y0, x1, y1 = box
                    pad = 24
                    A = f[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
                    B = g[max(0, y0 - pad):y1 + pad, max(0, x0 - pad):x1 + pad]
                    t = np.hstack([A, B]); t = cv2.resize(t, (400, int(400 * t.shape[0] / t.shape[1])))
                    cv2.putText(t, str(n), (4, 14), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
                    shots.append(t)
                f = g; prev = cen; log.append(n)
        p.stdin.write(f.tobytes()); n += 1
    p.stdin.close(); p.wait()
    print('frames', n, 'painted', len(log), (log[0], log[-1]) if log else None, 'gaps',
          [i for i in range(log[0], log[-1]) if i not in log] if log else None)
    if sheet and shots:
        w = max(s.shape[1] for s in shots)
        cv2.imwrite(sheet, np.vstack([cv2.copyMakeBorder(s, 0, 2, 0, w - s.shape[1], cv2.BORDER_CONSTANT) for s in shots]))

main()
