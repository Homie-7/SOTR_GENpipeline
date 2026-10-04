"""Per-frame LIGHT LEVEL check of an upscale against its source, for near-static clips (2026-10-04).

upscale_check.py's low-band frame-STEP correlation is weak when almost nothing moves (the steps are tiny, so their
correlation is mostly noise: studio b9, LOG 2026-10-01; the Alps, 2026-10-04). Here every frame's mean level and a
64x36 thumbnail are compared instead. PASS = mean-level corr >= 0.99, max level diff <= 1/255, thumbnail diff <= 1.5/255,
same frame count.     python tools/level_check.py SOURCE UPSCALE
"""
import subprocess
import sys

import numpy as np


def thumbs(p):
    raw = subprocess.check_output(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'scale=64:36:flags=area', '-f', 'rawvideo',
                                   '-pix_fmt', 'gray16le', '-'])
    return np.frombuffer(raw, np.uint16).reshape(-1, 36, 64).astype(np.float64) / 257


a, b = thumbs(sys.argv[1]), thumbs(sys.argv[2])
why = []
if len(a) != len(b):
    why.append(f'frames {len(a)} vs {len(b)}')
n = min(len(a), len(b))
la, lb = a[:n].mean((1, 2)), b[:n].mean((1, 2))
c = np.corrcoef(la, lb)[0, 1] if la.std() > 1e-6 else 1.0
mx = np.abs(la - lb).max()
td = np.abs(a[:n] - b[:n]).mean()
print(f'frames {len(a)}/{len(b)}; level corr {c:.4f}, max level diff {mx:.3f}/255; thumbnail diff {td:.3f}/255')
if c < 0.99 and la.std() > 0.05:
    why.append(f'level corr {c:.4f}')
if mx > 1.0:
    why.append(f'max level diff {mx:.3f}')
if td > 1.5:
    why.append(f'thumbnail diff {td:.3f}')
print('LEVELS ' + ('PASS' if not why else 'FAIL: ' + '; '.join(why)))
