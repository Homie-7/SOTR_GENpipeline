"""Every-frame check of a rendered court beat: per frame, black area, 'mid-grey' fraction (soft/faded figure),
IoU with the previous frame, and count of separate black pieces. Flags frames where these jump.
usage: python framecheck.py VIDEO beat [--raise-v5 --full]  -> prints flags + per-join +-20 table summary"""
import sys, subprocess, json, numpy as np, cv2
sys.path.insert(0, r'C:\Users\Homie\Documents\SOTR_GENpipeline\tools')
import court_gen_flow as f
import court_gen_approved as ga

video, beat = sys.argv[1], sys.argv[2]
beat = int(beat) if beat.isdigit() else beat
if '--full' in sys.argv:
    ga.LENGTH['5cut'] = 2424
f.WIDE = True
f.RAISE_V5 = '--raise-v5' in sys.argv
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                '-of', 'json', video], capture_output=True, text=True).stdout)['streams'][0]
W, H = pr['width'], pr['height']
proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', video, '-f', 'rawvideo', '-pix_fmt', 'gray', '-'],
                        stdout=subprocess.PIPE)
seq, rep = f.build_seq(beat)
area, mid, iou, pieces = [], [], [], []
prev = None
while True:
    buf = proc.stdout.read(W * H)
    if len(buf) < W * H:
        break
    g = np.frombuffer(buf, np.uint8).reshape(H, W).astype(np.float32) / 255.0
    blk = g < 0.5
    a = blk.mean()
    m = ((g > 0.15) & (g < 0.85)).mean()
    n, lab, st, _ = cv2.connectedComponentsWithStats(blk.astype(np.uint8), 8)
    big = st[1:, 4] if n > 1 else np.array([0])
    pc = int((big > 30).sum())
    io = 1.0 if prev is None else (np.logical_and(blk, prev).sum() / max(1, np.logical_or(blk, prev).sum()))
    area.append(a); mid.append(m); iou.append(io); pieces.append(pc); prev = blk
proc.wait()
N = len(area)
area, mid, iou, pieces = map(np.array, (area, mid, iou, pieces))
print(f'{video}: {N} frames {W}x{H}; seq {len(seq)}')
# ratio of mid-grey to area: a fade shows a big mid/area rise
ratio = mid / np.maximum(area, 1e-4)
med_r = np.median(ratio[area > 0.002]) if (area > 0.002).any() else 0
med_iou = np.median(iou[1:])
print(f'median mid/area {med_r:.3f}  median IoU {med_iou:.4f}  max pieces {pieces.max()}')
flags = []
for i in range(1, N):
    if area[i] < 0.002 and area[i - 1] < 0.002:
        continue
    why = []
    if ratio[i] > med_r * 1.8 and ratio[i] - med_r > 0.05: why.append(f'soft {ratio[i]:.3f}')
    if iou[i] < 0.90: why.append(f'IoU {iou[i]:.3f}')
    if pieces[i] > max(2, np.median(pieces)) + 1: why.append(f'pieces {pieces[i]}')
    if abs(area[i] - area[i - 1]) / max(area[i - 1], 1e-4) > 0.06: why.append(f'area {area[i-1]:.4f}->{area[i]:.4f}')
    if why:
        flags.append((i, why))
print(f'{len(flags)} flagged frames')
for i, why in flags[:80]:
    s = seq[i] if i < len(seq) else {}
    print(f'  {i:5d} {s.get("src")}{s.get("f")}: ' + ', '.join(why))
print('joins (+-20): min IoU, max soft ratio, max pieces')
for j, k, _ in rep:
    lo, hi = max(1, j - 20), min(N, j + 21)
    print(f'  {j:5d} {k:28s} IoU {iou[lo:hi].min():.4f}  soft {ratio[lo:hi].max():.3f}  pieces {pieces[lo:hi].max()}')
np.savez(sys.argv[1] + '.fc.npz', area=area, mid=mid, iou=iou, pieces=pieces)
