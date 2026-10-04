"""Long clips through ByteDance video upscale, in overlapping pieces (2026-10-04).

WHY: ByteDance "aigc" 4k TIMES OUT on long clips (three 165 s Scene 6 walls failed after ~16 min and were refunded;
117 s had worked), and it only outputs 24/30/60 fps while Scene 4 is 29.97 and Scene 5 is 25 fps, and
upscale_restore.py matches frames by index. So:
  split: the clip is cut into pieces of at most MAX frames that overlap by 48 frames, every frame kept and LABELLED at
         30 fps (setpts; nothing dropped or duplicated), HEVC Main10 crf 12, plus a manifest. Upscale each piece with
         fps=30 (the probe returned 300 of 300 frames).
  join:  the upscaled pieces are crossfaded over each overlap (in the high detail only, in effect: upscale_restore takes
         the light and motion from the source afterwards) into ONE intermediate with exactly the source's frame count,
         ProRes 422 HQ q2. Then:  upscale_restore.py SOURCE JOINED OUT --size WxH --clamp 2  (writes the source's own
         frame rate and sound).

  python tools/upscale_pieces.py split SOURCE.mov OUTDIR [--max 3300]      -> OUTDIR/<name>_p<k>.mp4 + <name>_pieces.json
  python tools/upscale_pieces.py join  MANIFEST.json RAWDIR OUT.mov        (RAWDIR/<name>_p<k>_bd4k.mp4)
"""
import json
import math
import os
import subprocess
import sys

OV = 48          # overlap, frames
LABEL = 30       # the fps the pieces are labelled at (ByteDance: 24/30/60)


def nframes(p):
    return int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_frames',
                                        '-show_entries', 'stream=nb_read_frames', '-of', 'csv=p=0', p]).decode().strip())


def split(src, outdir, mx):
    n = nframes(src)
    name = os.path.splitext(os.path.basename(src))[0]
    k = max(1, math.ceil((n - OV) / (mx - OV)))
    L = math.ceil((n + (k - 1) * OV) / k)                    # equal pieces
    starts = [min(i * (L - OV), n - L) for i in range(k)] if k > 1 else [0]
    os.makedirs(outdir, exist_ok=True)
    pieces = []
    for i, s in enumerate(starts):
        ln = min(L, n - s)
        out = os.path.join(outdir, f'{name}_p{i}.mp4')
        if not os.path.exists(out):
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf',
                            f'trim=start_frame={s}:end_frame={s + ln},setpts=N/{LABEL}/TB', '-r', str(LABEL),
                            '-c:v', 'libx265', '-preset', 'medium', '-crf', '12', '-pix_fmt', 'yuv420p10le',
                            '-tag:v', 'hvc1', '-an', out], check=True, stdin=subprocess.DEVNULL)
        got = nframes(out)
        assert got == ln, f'{out}: {got} frames, expected {ln}'
        pieces.append(dict(file=os.path.basename(out), start=s, frames=ln))
        print(f'{out}: frames {s}-{s + ln - 1} ({ln}, {ln / LABEL:.1f} s at {LABEL})', flush=True)
    man = dict(source=os.path.abspath(src), frames=n, overlap=OV, label_fps=LABEL, pieces=pieces)
    mp = os.path.join(outdir, f'{name}_pieces.json')
    json.dump(man, open(mp, 'w'), indent=1)
    print('manifest', mp)


def join(mp, rawdir, out):
    man = json.load(open(mp))
    ps = man['pieces']
    ins, fc = [], []
    for i, p in enumerate(ps):
        f = os.path.join(rawdir, p['file'].replace('.mp4', '_bd4k.mp4'))
        got = nframes(f)
        assert got == p['frames'], f'{f}: {got} frames, expected {p["frames"]}'
        ins += ['-i', f]
        fc.append(f'[{i}]settb=AVTB,fps={LABEL}[v{i}]')
    cur, t = 'v0', ps[0]['frames']                           # running length in frames
    for i in range(1, len(ps)):
        ov = ps[i - 1]['start'] + ps[i - 1]['frames'] - ps[i]['start']
        off = (t - ov) / LABEL
        fc.append(f'[{cur}][v{i}]xfade=transition=fade:duration={ov / LABEL:.6f}:offset={off:.6f}[x{i}]')
        cur, t = f'x{i}', t + ps[i]['frames'] - ov
    assert t == man['frames'], f'joined length {t} != source {man["frames"]}'
    tmp = os.path.join(os.path.dirname(out) or '.', '_tmp_' + os.path.basename(out))
    subprocess.run(['ffmpeg', '-v', 'error', '-y'] + ins + ['-filter_complex', ';'.join(fc) + f';[{cur}]format=yuv422p10le[o]',
                    '-map', '[o]', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-an', tmp],
                   check=True, stdin=subprocess.DEVNULL)
    got = nframes(tmp)
    assert got == man['frames'], f'joined file has {got} frames, expected {man["frames"]}'
    os.replace(tmp, out)
    print(f'{out}: {got} frames joined from {len(ps)} pieces', flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'split':
        a = sys.argv[4:]
        split(sys.argv[2], sys.argv[3], int(a[a.index('--max') + 1]) if '--max' in a else 3300)
    elif sys.argv[1] == 'join':
        join(sys.argv[2], sys.argv[3], sys.argv[4])
