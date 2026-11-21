"""M10c: every-frame check of the judge's cut-out (the mask court_gen_flow.frames() composites), no video decode.
Per frame: soft = half-tone pixels / figure area (a dissolve/fade raises it), IoU with the previous frame,
pieces = separate figure islands > 30 px. Prints every join's +-20 window and every out-of-range frame.
usage: python tools/_maskcheck_m10c.py BEAT [--raise-v5|--raise-v10] [--full]"""
import sys, numpy as np, cv2
sys.path.insert(0, r'C:\Users\Homie\Documents\SOTR_GENpipeline\tools')
import court_gen_flow as f
import court_gen_approved as ga
beat = sys.argv[1]; beat = int(beat) if beat.isdigit() else beat
if '--full' in sys.argv:
    ga.LENGTH['5cut'] = 2424
f.WIDE = True
f.RAISE_V5 = '--raise-v5' in sys.argv
f.RAISE_V10 = '--raise-v10' in sys.argv  # M10d
if f.RAISE_V10:
    import os; f.FIT16_JSON = os.path.join(f.cg.GEN, '_fit_16x9_v8v10.json')
sc = f.Scene(f.merged_fit())
seq, rep = f.build_seq(beat, sc)
soft, iou, pcs, area = [], [], [], []
prev = None
for s in seq:
    if s['src'] is None:
        soft.append(0); iou.append(1); pcs.append(0); area.append(0); prev = None; continue
    m = sc.mask(s['src'], s['f'], s['size'])
    if s['warp']:
        ws, wf, w = s['warp']
        m = f.join_warp(s['src'], m, ws, sc.mask(ws, wf, s['size']), w)
    fig = m < 0.5
    a = fig.sum()
    soft.append(((m > 0.15) & (m < 0.85)).sum() / max(a, 1))
    n, _, st, _ = cv2.connectedComponentsWithStats(fig.astype(np.uint8), 8)
    pcs.append(int((st[1:, 4] > 30).sum()) if n > 1 else 0)
    iou.append(1.0 if prev is None else np.logical_and(fig, prev).sum() / max(1, np.logical_or(fig, prev).sum()))
    area.append(a); prev = fig
soft, iou, pcs = map(np.array, (soft, iou, pcs))
live = np.array([s['src'] is not None for s in seq])
ms, mi = np.median(soft[live]), np.median(iou[live])
print(f'beat {beat} raise_v5={f.RAISE_V5} v10={f.RAISE_V10}: {len(seq)} f, median soft {ms:.4f}, median IoU {mi:.4f}, pieces max {pcs.max()}')
bad = [i for i in range(1, len(seq)) if live[i] and live[i-1] and (iou[i] < 0.95 or soft[i] > 2 * ms + 0.01 or pcs[i] > 1)]
print(f'{len(bad)} out-of-range frames:', ' '.join(f'{i}({seq[i]["src"]}{seq[i]["f"]} IoU{iou[i]:.3f} s{soft[i]:.3f} p{pcs[i]})' for i in bad[:60]))
for j, k, _ in rep:
    lo, hi = max(1, j - 20), min(len(seq), j + 21)
    print(f'  {j:5d} {j/24:6.2f}s {k:22s} minIoU {iou[lo:hi].min():.4f}  maxsoft {soft[lo:hi].max():.4f}  maxpieces {pcs[lo:hi].max()}')
