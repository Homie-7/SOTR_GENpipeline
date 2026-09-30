"""Scene 6: turn the generated flag and smoke into seamless loops the scene script can read (picture + sound).

WHY: S6-FLAG and S6-SMOKE are generated as a 4 s probe plus a 30 s Sequel of it (a native join), but the scene
needs the flag for ~36 s at a stretch and the smoke for the whole 2:45. Playback holds nothing (final-product
rule), so the files are looped here, once: the probe and the Sequel are joined, and the last XF seconds are
crossfaded into the first ones (loop_halo.py's method). The loop's length is N - XF frames; frame N - XF runs
straight into the crossfade, whose last frame is frame XF, which runs straight into the body. No ping-pong.

  python tools/s6_loops.py PROBE.mp4 SEQUEL.mp4 OUT.mov [--xf 1.5] [--crop-bottom 0.08]

OUT is ProRes 422 HQ (10-bit) with 48 kHz 24-bit PCM, the clips' own sound looped the same way.
"""
import argparse
import os
import subprocess
import tempfile


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('probe')
    ap.add_argument('sequel')
    ap.add_argument('out')
    ap.add_argument('--xf', type=float, default=1.5, help='loop crossfade, seconds')
    ap.add_argument('--crop-bottom', type=float, default=0.0, help='fraction of the height cut off the bottom')
    a = ap.parse_args()
    tmp = tempfile.mkdtemp()
    joined = os.path.join(tmp, 'joined.mov')
    crop = f',crop=iw:ih*{1 - a.crop_bottom:.4f}:0:0' if a.crop_bottom > 0 else ''
    # 1. join probe + Sequel (same size and rate by construction), 10-bit intermediate
    run(['ffmpeg', '-y', '-v', 'error', '-i', a.probe, '-i', a.sequel, '-filter_complex',
         f'[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a];[v]format=yuv422p10le{crop}[vv];[a]aresample=48000[aa]',
         '-map', '[vv]', '-map', '[aa]', '-c:v', 'prores_ks', '-profile:v', '3', '-c:a', 'pcm_s24le', joined])
    dur = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0',
                                         joined]).decode().strip())
    xf = a.xf
    # 2. loop = crossfade(tail -> head) + body; tail starts at dur - xf, head is 0..xf, body is xf..dur - xf
    fc = (f'[0:v]split=3[v1][v2][v3];[v1]trim=0:{xf},setpts=PTS-STARTPTS[head];'
          f'[v2]trim={xf}:{dur - xf},setpts=PTS-STARTPTS[body];'
          f'[v3]trim={dur - xf}:{dur},setpts=PTS-STARTPTS[tail];'
          f'[tail][head]xfade=transition=fade:duration={xf}:offset=0[x];[x][body]concat=n=2:v=1:a=0[v];'
          f'[0:a]asplit=3[a1][a2][a3];[a1]atrim=0:{xf},asetpts=PTS-STARTPTS[ah];'
          f'[a2]atrim={xf}:{dur - xf},asetpts=PTS-STARTPTS[ab];'
          f'[a3]atrim={dur - xf}:{dur},asetpts=PTS-STARTPTS[at];'
          f'[at][ah]acrossfade=d={xf}:c1=tri:c2=tri[ax];[ax][ab]concat=n=2:v=0:a=1[a]')
    run(['ffmpeg', '-y', '-v', 'error', '-i', joined, '-filter_complex', fc, '-map', '[v]', '-map', '[a]',
         '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-c:a', 'pcm_s24le', a.out])
    print('wrote', a.out, f'(loop {dur - xf:.2f} s)')


if __name__ == '__main__':
    main()
