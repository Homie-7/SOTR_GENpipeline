"""M10d: every frame of a window, tiled for eyes. usage: python tools/_joinsheet_m10d.py VIDEO OUTPREFIX F0 F1 [x0 y0 x1 y1] [scale] [per]
Writes OUTPREFIX_<f0>.png sheets of `per` frames (4 across), each labelled with its frame number."""
import sys, subprocess, numpy as np, cv2
v, out, f0, f1 = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
box = list(map(int, sys.argv[5:9])) if len(sys.argv) > 8 else None
sc = float(sys.argv[9]) if len(sys.argv) > 9 else 0.5
per = int(sys.argv[10]) if len(sys.argv) > 10 else 8
W, H = map(int, subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height',
                                '-of', 'csv=p=0', v], capture_output=True, text=True).stdout.strip().split(','))
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', v, '-vf', rf'select=between(n\,{f0}\,{f1})', '-fps_mode', 'passthrough',
                      '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-'], stdout=subprocess.PIPE)
cells = []
for n in range(f0, f1 + 1):
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    im = np.frombuffer(b, np.uint8).reshape(H, W, 3)
    if box: im = im[box[1]:box[3], box[0]:box[2]]
    im = cv2.resize(im, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA).copy()
    cv2.putText(im, str(n), (8, 34), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 255, 255), 2)
    cells.append(im)
p.stdout.close(); p.wait()
for i in range(0, len(cells), per):
    c = cells[i:i + per]
    while len(c) % 4: c.append(np.zeros_like(c[0]))
    rows = [np.hstack(c[r:r + 4]) for r in range(0, len(c), 4)]
    cv2.imwrite(f'{out}_{f0 + i:05d}.png', np.vstack(rows))
print(len(cells), 'frames')
