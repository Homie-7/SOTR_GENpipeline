"""Replace a frozen, smoky dusk hold with a smoke-free one (salon, after the snuff), touching NOTHING else.

Built 2026-09-26 (Claude). WHY (Homie): in the salon files, after the candles go out, "the smoke is
kind of stuck on that frame". The dusk after the snuff was a HOLD of the snuff clip's last frame, and
that frame still carries wisps, so they froze for the whole hold (35 s in b2-3, 3 s in b8). Homie:
"make sure everything else remains exactly how it is… the still smoke is the only problem."

HOW: the wall is static after the candles are out and the smoke moves, so a low per-pixel percentile
over the settled frames is the room without smoke (a clean dusk plate). Over the last --dissolve
frames of the snuff the live frames blend into the plate, so the smoke thins away while it is still
moving; the hold is then the clean plate.

EXACTNESS: every frame before the dissolve is STREAM-COPIED from the source (ProRes is intra-frame, so
the copy is bit-identical, never re-encoded); only the tail is encoded; the sound is copied untouched.

  clean:  python tools/clean_hold.py clean BASE.mov OUT.mov --settle 1905 --hold 1977 [--dissolve 36]
            b2-3: --settle 1905 --hold 1977      b8: --settle 241 --hold 313
  splice: python tools/clean_hold.py splice HEAD_SRC.mov TAIL.mov OUT.mov --at FRAME
            OUT = HEAD_SRC's frames [0, FRAME) stream-copied + all of TAIL, with HEAD_SRC's sound.
            (For the edge file: TAIL = edge_flow.py render of the new clean file with
             --start FRAME/24 --t0 FRAME, so the drifting blocks carry on exactly.)

Refuses to overwrite. Needs ffmpeg, numpy.
"""
import argparse
import json
import os
import subprocess
import tempfile

import numpy as np


def size(p):
    s = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                            'stream=width,height', '-of', 'json', p]))['streams'][0]
    return s['width'], s['height']


def splice(head_src, at, tail, out):
    """head_src frames [0, at) stream-copied, then tail, with head_src's audio, into out."""
    d = tempfile.mkdtemp(dir=os.path.dirname(out))
    head = os.path.join(d, 'head.mov')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', head_src, '-map', '0:v', '-frames:v', str(at), '-c', 'copy', head],
                   check=True)
    lst = os.path.join(d, 'list.txt')
    with open(lst, 'w') as f:
        f.write(f"file '{head}'\nfile '{os.path.abspath(tail)}'\n".replace('\\', '/'))
    subprocess.run(['ffmpeg', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', head_src, '-map', '0:v',
                    '-map', '1:a?', '-c', 'copy', out], check=True)
    os.remove(head)
    os.remove(lst)
    os.rmdir(d)


def clean(a):
    W, H = size(a.base)
    n = a.hold - a.settle
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', a.base, '-vf', f'select=gte(n\\,{a.settle})',
                          '-fps_mode', 'passthrough', '-frames:v', str(n), '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'],
                         capture_output=True, check=True).stdout
    plate = np.percentile(np.frombuffer(raw, '<u2').reshape(-1, H, W, 3).astype(np.float32), a.pct, axis=0)
    del raw
    d0 = a.hold - a.dissolve
    tail = a.out + '.tail.mov'
    rd = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', a.base, '-vf', f'select=gte(n\\,{d0})', '-fps_mode',
                           'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-'], stdout=subprocess.PIPE)
    wr = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}',
                           '-r', '24', '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le',
                           tail], stdin=subprocess.PIPE)
    sz = W * H * 6
    i = d0
    while True:
        buf = rd.stdout.read(sz)
        if len(buf) < sz:
            break
        f = np.frombuffer(buf, '<u2').reshape(H, W, 3).astype(np.float32)
        w = min(1.0, (i - d0 + 1) / a.dissolve)
        w = w * w * (3 - 2 * w)
        wr.stdin.write(np.clip(f * (1 - w) + plate * w, 0, 65535).astype('<u2').tobytes())
        i += 1
    wr.stdin.close()
    wr.wait()
    rd.wait()
    splice(a.base, d0, tail, a.out)
    os.remove(tail)
    print(f'{i} frames -> {a.out} (frames 0-{d0 - 1} stream-copied; smoke dissolves {d0}-{a.hold - 1}; '
          f'clean plate from {a.hold})')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('clean')
    c.add_argument('base')
    c.add_argument('out')
    c.add_argument('--settle', type=int, required=True)
    c.add_argument('--hold', type=int, required=True)
    c.add_argument('--dissolve', type=int, default=36)
    c.add_argument('--pct', type=float, default=10)
    s = sub.add_parser('splice')
    s.add_argument('head_src')
    s.add_argument('tail')
    s.add_argument('out')
    s.add_argument('--at', type=int, required=True)
    a = ap.parse_args()
    if os.path.exists(a.out):
        raise SystemExit(f'refusing: {a.out} exists')
    if a.cmd == 'clean':
        clean(a)
    else:
        splice(a.head_src, a.at, a.tail, a.out)
        print(f'-> {a.out}')


if __name__ == '__main__':
    main()
