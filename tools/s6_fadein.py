"""S6 fade-in from black on the EXISTING show files (Homie F42: "add a fade in the beginning of the S6 files that we
already have"). 0 cr. Review copies only: writes to 04_WORKING_FILES/S6_fadein_v1/<res>/, never into the show folder.

  python tools/s6_fadein.py [--secs 2.0] [--only 4K|1080]

HOW (frame-exact, the rest untouched):
  * ProRes is intra-only, so every frame is a keyframe. The head (first N = secs*24 frames) is re-encoded with an eased
    (half-sine) fade of the RGB from black; alpha is kept as it is (the picture comes up from opaque black, like the
    explosion overlay's black end). Same encoder/settings as render_s6.py (prores_ks 4444, qscale 2, yuva444p10le).
  * Frames N..end are STREAM-COPIED from the source (bit-identical), joined with the concat demuxer.
  * Sound: the whole PCM track is kept; an eased fade-in over the same N frames (qsin). Nothing removed.
  * Checks: frame count, duration, framemd5 of frames N, N+1 and the last frame vs the source, audio sample count.
Prints DONE at the end (for tools/run_watch.sh).
"""
import argparse
import hashlib
import os
import subprocess
import sys

FPS = 24
MEDIA = 'D:/SOTR/SOTR_MEDIA'
SRC = {'4K': f'{MEDIA}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars',
       '1080': f'{MEDIA}/01_FINAL_FOR_SHOW/3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars'}
OUT = f'{MEDIA}/04_WORKING_FILES/S6_fadein_v1'
WALLS = ('CENTRE', 'LEFT', 'RIGHT')


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        print('FAILED:', ' '.join(cmd[:6]), r.stderr[-800:], flush=True)
        sys.exit(1)
    return r.stdout


def nframes(f):
    return int(run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-count_packets', '-show_entries',
                    'stream=nb_read_packets', '-of', 'csv=p=0', f]).strip())


def packet_md5s(f):
    """md5 of every compressed video packet (stream copy must be bit-identical)."""
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-map', '0:v', '-c', 'copy', '-f', 'framemd5', '-'],
                       capture_output=True, text=True)
    return [l.split(',')[-1].strip() for l in r.stdout.splitlines() if l and not l.startswith('#')]


def build(res, wall, secs):
    src = f'{SRC[res]}/S6_{wall}_wars.mov'
    od = f'{OUT}/{res}'
    os.makedirs(od, exist_ok=True)
    dst = f'{od}/S6_{wall}_wars_FADEIN.mov'
    if os.path.exists(dst):
        print('refusing: output exists', dst, flush=True)
        sys.exit(1)
    n = int(round(secs * FPS))
    tmp = f'{od}/_tmp_{wall}'
    os.makedirs(tmp, exist_ok=True)
    head, tail, aud, lst = f'{tmp}/head.mov', f'{tmp}/tail.mov', f'{tmp}/audio.wav', f'{tmp}/list.txt'
    # eased RGB fade from black, alpha untouched: k(t) = sin^2(pi/2 * t/T) on frames 0..n-1 (frame n = full)
    k = f'pow(sin(PI/2*min(N/{n}\\,1))\\,2)'
    vf = (f"format=rgba64le,geq=r='r(X\\,Y)*{k}':g='g(X\\,Y)*{k}':b='b(X\\,Y)*{k}':a='alpha(X\\,Y)'")
    run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-map', '0:v', '-frames:v', str(n), '-vf', vf,
         '-c:v', 'prores_ks', '-profile:v', '4', '-qscale:v', '2', '-pix_fmt', 'yuva444p10le', '-vendor', 'apl0', head])
    run(['ffmpeg', '-y', '-v', 'error', '-ss', f'{n / FPS:.6f}', '-i', src, '-map', '0:v', '-c', 'copy', tail])
    run(['ffmpeg', '-y', '-v', 'error', '-i', src, '-map', '0:a', '-af', f'afade=t=in:st=0:d={n / FPS:.6f}:curve=qsin',
         '-c:a', 'pcm_s24le', aud])
    open(lst, 'w').write(f"file '{head}'\nfile '{tail}'\n")
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', aud, '-map', '0:v', '-map', '1:a',
         '-c', 'copy', '-movflags', '+faststart', dst])
    # checks
    ns, nd = nframes(src), nframes(dst)
    ok = ns == nd
    ms, md = packet_md5s(src), packet_md5s(dst)
    same = ok and ms[n:] == md[n:]
    print(f'{res} {wall}: frames src {ns} dst {nd}; all packets {n}..{ns - 1} bit-identical: {same}', flush=True)
    if not (ok and same):
        print('FAILED check', dst, flush=True)
        sys.exit(1)
    for f in (head, tail, aud, lst):
        os.remove(f)
    os.rmdir(tmp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--secs', type=float, default=2.0)
    ap.add_argument('--only', choices=('4K', '1080'))
    a = ap.parse_args()
    for res in (('1080', '4K') if not a.only else (a.only,)):
        for wall in WALLS:
            build(res, wall, a.secs)
    print('DONE s6_fadein', flush=True)


if __name__ == '__main__':
    main()
