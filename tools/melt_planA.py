"""S2 painting melt, Plan A build steps (after melt_reproject.py video ... SCALE 1 for each surface).

  python tools/melt_planA.py prep   DIR      -> DIR/topaz_in_<W>.mp4: f0-215 of native_<W>.mp4, retimed 25->24 (every frame kept), padded to 1920x1080
  python tools/melt_planA.py build  DIR W    -> DIR/<W>_CLEAN_4K.mov + _1080.mov: Topaz melt (crop back) dissolved into the Lanczos sea, sound, ProRes 422 HQ 24 fps

Every source frame is kept (25 -> 24 fps plays 4% slower, 500 f = 20.83 s). Topaz covers frames 0-215; it dissolves into the Lanczos-4K
sea over frames 190-215 (same content, only the sharpness changes). Sound: 'paiinting audio.wav' from 1.625 s (its hit at 3.125 s meets
the pour's first big motion at frame 36), cut at the picture end, no fade (the operator fades file start/end).
"""
import os
import subprocess
import sys

SIZES = {'CENTRE': (1800, 1080), 'LEFT': (1440, 1080), 'RIGHT': (1440, 1080), 'FLOOR': (1920, 1080)}
T_END = 215          # last Topaz frame
X0, X1 = 190, 215    # dissolve frames
R0, R1 = 4, 12       # true-Raft overlay dissolves out (the paint starts to move ~f8)
AUDIO = r'F:\OrCha Drive\SOR DESK BACK UP\RMIT Black Box first show\Final Animations\Painting melt + Ocean loop\paiinting audio.wav'
A_OFF = 1.625


def run(a):
    print(' '.join(a[:6]), '...', flush=True)
    subprocess.run(a, check=True)


def prep(d):
    for w, (ww, hh) in SIZES.items():
        run(['ffmpeg', '-v', 'error', '-y', '-r', '24', '-i', f'{d}/native_{w}.mp4', '-vf',
             f'select=lte(n\\,{T_END}),setpts=N/24/TB,pad=1920:1080:{(1920 - ww) // 2}:{(1080 - hh) // 2}:black',
             '-fps_mode', 'passthrough', '-c:v', 'libx264', '-crf', '12', '-preset', 'slow', '-pix_fmt', 'yuv420p',
             f'{d}/topaz_in_{w}.mp4'])


def build(d, w):
    ww, hh = SIZES[w]
    W4, H4 = ww * 2, hh * 2
    cx, cy = (3840 - W4) // 2, (2160 - H4) // 2
    raft = f'{d}/raft_overlay_{w}_4K.png'      # the true Raft, registered + histogram-matched to Topaz frame 0 (CENTRE only)
    has_raft = os.path.exists(raft)
    fc = (f'[0:v]crop={W4}:{H4}:{cx}:{cy},setpts=N/24/TB,format=yuv422p10le[t0];'
          + (f'[3:v]format=rgba,fade=t=out:st={R0 / 24}:d={(R1 - R0) / 24}:alpha=1[rf];[t0][rf]overlay=eof_action=pass,format=yuv422p10le[t];'
             if has_raft else '[t0]null[t];') +
          f'[1:v]setpts=N/24/TB,scale={W4}:{H4}:flags=lanczos,format=yuv422p10le[l];'
          f'[t]tpad=stop_mode=clone:stop=400[tp];'
          f'[l][tp]blend=shortest=1:all_expr=\'if(lt(N\\,{X0})\\,B\\,if(gt(N\\,{X1})\\,A\\,A*(N-{X0})/{X1 - X0}+B*(1-(N-{X0})/{X1 - X0})))\'[v4];'
          f'[v4]split[o4][s];[s]scale={ww}:{hh}:flags=lanczos[o1]')
    run(['ffmpeg', '-v', 'error', '-y', '-r', '24', '-i', f'{d}/topaz_out_{w}.mp4', '-r', '24', '-i', f'{d}/native_{w}.mp4',
         '-ss', str(A_OFF), '-i', AUDIO] + (['-loop', '1', '-framerate', '24', '-t', str(R1 / 24 + 1), '-i', raft] if has_raft else []) + [
         '-filter_complex', fc,
         '-map', '[o4]', '-map', '2:a', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-c:a', 'pcm_s24le', '-ar', '48000',
         '-shortest', '-r', '24', f'{d}/{w}_CLEAN_4K.mov',
         '-map', '[o1]', '-map', '2:a', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2', '-c:a', 'pcm_s24le', '-ar', '48000',
         '-shortest', '-r', '24', f'{d}/{w}_CLEAN_1080.mov'])


if __name__ == '__main__':
    if sys.argv[1] == 'prep':
        prep(sys.argv[2])
    elif sys.argv[1] == 'build':
        build(sys.argv[2], sys.argv[3])
