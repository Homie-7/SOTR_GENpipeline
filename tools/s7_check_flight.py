"""Check a flight take: probe, frame 0 vs the start frame, motion smoothness, cut detection, contact sheet.
  python check_flight.py CLIP START.png SHEET.jpg"""
import json, subprocess, sys, io
import numpy as np, cv2
from PIL import Image, ImageDraw

clip, start, sheet = sys.argv[1:4]
pr = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
     'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,pix_fmt,sample_rate,channels:format=duration',
     '-of', 'json', clip]))
v = next(s for s in pr['streams'] if s['codec_type'] == 'video')
a = [s for s in pr['streams'] if s['codec_type'] == 'audio']
print('PROBE', v['width'], 'x', v['height'], v['r_frame_rate'], 'frames', v.get('nb_frames'), v['codec_name'], v['pix_fmt'],
      'dur', pr['format']['duration'], 'audio', [(s['codec_name'], s.get('sample_rate'), s.get('channels')) for s in a])
W, H = int(v['width']), int(v['height'])
cap = cv2.VideoCapture(clip)
frames = []
while True:
    ok, f = cap.read()
    if not ok:
        break
    frames.append(f)
n = len(frames)
print('decoded frames', n)
# frame 0 vs start
ref = cv2.resize(cv2.imread(start), (W, H), interpolation=cv2.INTER_AREA)
f0 = frames[0]
g0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY).astype(np.float32)
gr = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY).astype(np.float32)
mad = np.abs(f0.astype(np.float32) - ref.astype(np.float32)).mean()
shift, resp = cv2.phaseCorrelate(gr, g0)
warp = np.eye(2, 3, dtype=np.float32)
try:
    cc, warp = cv2.findTransformECC(gr / 255, g0 / 255, warp, cv2.MOTION_AFFINE,
                                    (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6), None, 5)
    sx, sy = np.linalg.norm(warp[:, 0]), np.linalg.norm(warp[:, 1])
    print(f'FRAME0 vs start: MAD {mad:.1f}/255  phase shift {shift[0]:.1f},{shift[1]:.1f}px (resp {resp:.2f})  '
          f'ECC cc {cc:.3f} sx {sx:.3f} sy {sy:.3f} dx {warp[0,2]:.1f} dy {warp[1,2]:.1f}')
except cv2.error as e:
    print(f'FRAME0 vs start: MAD {mad:.1f}/255 phase {shift} ECC failed')
# cut detection + motion: frame-to-frame mean abs diff on small greys
small = [cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (160, 90)).astype(np.float32) for f in frames]
d = np.array([np.abs(small[i] - small[i - 1]).mean() for i in range(1, n)])
med = np.median(d)
spikes = [(i, round(float(x), 1)) for i, x in enumerate(d, 1) if x > max(4 * med, 12)]
print(f'frame diff median {med:.2f}, max {d.max():.2f} at f{int(d.argmax())+1}; spikes (cut?) {spikes[:10]}')
# global motion per second (phase corr between consecutive small frames)
mv = []
for i in range(1, n):
    s, _ = cv2.phaseCorrelate(small[i - 1], small[i])
    mv.append(np.hypot(*s) * W / 160)
mv = np.array(mv)
per_s = [round(float(mv[int(k * 24):int((k + 1) * 24)].mean()), 1) for k in range(int(np.ceil((n - 1) / 24)))]
jerk = np.abs(np.diff(mv))
print('global motion px/frame per second:', per_s, ' jerk p95 %.1f' % np.percentile(jerk, 95))
# contact sheet 16 frames
idx = np.linspace(0, n - 1, 16).astype(int)
tw, th = 480, int(480 * H / W)
sh = Image.new('RGB', (4 * tw, 4 * (th + 18)), (20, 20, 20))
dr = ImageDraw.Draw(sh)
for k, i in enumerate(idx):
    im = Image.fromarray(cv2.cvtColor(frames[i], cv2.COLOR_BGR2RGB)).resize((tw, th), Image.LANCZOS)
    x, y = (k % 4) * tw, (k // 4) * (th + 18)
    sh.paste(im, (x, y + 18))
    dr.text((x + 4, y + 3), f'f{i}  {i/24:.2f}s', fill=(230, 230, 230))
sh.save(sheet, quality=90)
print('sheet', sheet)
