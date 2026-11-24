"""F26 (25 Nov): finish the S9 judge 4K upscales.
restore (tools/upscale_restore.py) -> mux Darren's final-mix slice -> 1080 twin -> checks.
Writes into 04_WORKING_FILES/S9_4K_final/out/ with _tmp_ names, renames when each step is good.
Prints DONE at the end (tools/run_watch.sh)."""
import os, subprocess, sys
import numpy as np

M = r'D:/SOTR/SOTR_MEDIA/04_WORKING_FILES'
D = M + '/S9_4K_final'
MIX = M + '/S9_gen_judge_review/darren_final_23112026/the judge CUT DOWN 23112026.mov'
# name, restore source, upscale, mix start (s, cut clock), frames
JOBS = [
    ('S9_b3_CENTRE_court', D + '/upload/S9_b3_CENTRE_court_EXT2.mp4', D + '/dl/S9_b3_up4k.mp4', 77.375, 960),
    ('S9_b5_CENTRE_court', D + '/source/S9_b5_CENTRE_court_F25cut_src.mkv', D + '/dl/S9_b5_up4k.mp4', 183.75, 1416),
    ('S9_b7_CENTRE_court', D + '/upload/S9_b7_CENTRE_court_EXT5.mp4', D + '/dl/S9_b7_up4k.mp4', 274.9166667, 480),
]
OUT = D + '/out'
os.makedirs(OUT, exist_ok=True)
PY = sys.executable


def run(cmd):
    print('>', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True)


def frames(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries',
                        'stream=nb_read_packets', '-of', 'csv=p=0', p], capture_output=True, text=True)
    return int(r.stdout.strip())


def pcm(p, ss=None, t=None):
    cmd = ['ffmpeg', '-v', 'error']
    if ss is not None:
        cmd += ['-ss', str(ss)]
    cmd += ['-i', p]
    if t is not None:
        cmd += ['-t', str(t)]
    cmd += ['-map', '0:a:0', '-ac', '1', '-ar', '8000', '-f', 'f32le', '-']
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32)


def lag(a, ref_start, n):
    """Cross-correlate file audio a against the mix around ref_start (+-2 s). Returns lag in ms."""
    ref = pcm(MIX, max(0, ref_start - 2), n / 24 + 4)
    a = a[:8000 * 20]
    best, bl = -1, None
    for off in range(0, len(ref) - len(a), 8):
        c = float(np.dot(ref[off:off + len(a)], a))
        if c > best:
            best, bl = c, off
    return (bl - min(2, ref_start) * 8000) / 8.0


for name, src, up, ss, n in JOBS:
    dur = n / 24
    r_nos = OUT + f'/{name}_4K_nosnd.mov'
    f4 = OUT + f'/{name}_4K.mov'
    f1 = OUT + f'/{name}_1080.mov'
    if not os.path.exists(r_nos):
        tmp = OUT + f'/_tmp_{name}_4K_nosnd.mov'
        run([PY, 'tools/upscale_restore.py', src, up, tmp, '--size', '3600x2160', '--clamp', '2'])
        os.replace(tmp, r_nos)
    if not os.path.exists(f4):
        tmp = OUT + f'/_tmp_{name}_4K.mov'
        run(['ffmpeg', '-v', 'error', '-y', '-i', r_nos, '-ss', str(ss), '-t', f'{dur:.6f}', '-i', MIX,
             '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'pcm_s24le', '-ar', '48000',
             '-t', f'{dur:.6f}', tmp])
        os.replace(tmp, f4)
    if not os.path.exists(f1):
        tmp = OUT + f'/_tmp_{name}_1080.mov'
        run(['ffmpeg', '-v', 'error', '-y', '-i', f4, '-vf', 'scale=1800:1080:flags=lanczos', '-c:v', 'prores_ks',
             '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-c:a', 'copy', tmp])
        os.replace(tmp, f1)
    for f in (f4, f1):
        fr = frames(f)
        lg = lag(pcm(f), ss, n)
        ok = fr == n and abs(lg) <= 1
        print(f'CHECK {os.path.basename(f)} frames {fr}/{n} audio-lag {lg:.1f} ms {"OK" if ok else "BAD"}', flush=True)
    run([PY, 'tools/upscale_check.py', src, f4])
    print(f'FINISHED {name}', flush=True)
print('DONE')
