"""Review sheet for a 4-angle Unreal scene (Scenes 4/5): per time, LEFT | FRONT | RIGHT on top, FLOOR centred under, at
5/35/65/95% of the clip; plus a 1:1 crop of the floor centre at each time (speckle check). BOTTOM=path overrides the
floor file (the camps floor has no sky, so it is not de-birded).
  python tools/review_sheet.py DIR PREFIX OUT_PREFIX   (reads DIR/PREFIX_<left|front|right|bottom>.mov)"""
import subprocess, sys, os
from PIL import Image, ImageDraw
d, pre, out = sys.argv[1:4]
def dur(p):
    return float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]))
def grab(p, t):
    raw = subprocess.check_output(['ffmpeg','-v','error','-ss','%.3f'%t,'-i',p,'-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    import io; return Image.open(io.BytesIO(raw)).convert('RGB')
T = dur(f'{d}/{pre}_front.mov')
times = [T*f for f in (0.05, 0.35, 0.65, 0.95)]
rows = []
for t in times:
    im = {a: grab(os.environ.get('BOTTOM') if a == 'bottom' and os.environ.get('BOTTOM') else f'{d}/{pre}_{a}.mov', t) for a in ('left','front','right','bottom')}
    w, h = 640, 360
    s = {a: v.resize((w, h), Image.LANCZOS) for a, v in im.items()}
    tile = Image.new('RGB', (3*w, 2*h+30), (20,20,20))
    tile.paste(s['left'], (0, 30)); tile.paste(s['front'], (w, 30)); tile.paste(s['right'], (2*w, 30)); tile.paste(s['bottom'], (w, h+30))
    ImageDraw.Draw(tile).text((8, 8), f'{pre}  t={t:6.1f}s   LEFT | FRONT | RIGHT, FLOOR under', fill=(230,230,230))
    rows.append(tile)
    # 1:1 floor crop (centre 960x540 of the full-res floor frame)
    b = im['bottom']; W, H = b.size
    b.crop((W//2-480, H//2-270, W//2+480, H//2+270)).save(f'{out}_floor_1to1_t{int(t):03d}.png')
sheet = Image.new('RGB', (rows[0].width, sum(r.height for r in rows)))
y = 0
for r in rows: sheet.paste(r, (0, y)); y += r.height
sheet.save(f'{out}_SHEET.jpg', quality=90)
print('wrote', f'{out}_SHEET.jpg', 'times', [round(t,1) for t in times])
