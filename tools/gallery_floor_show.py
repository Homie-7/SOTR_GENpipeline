"""Build the Louvre gallery's FLOOR show files (Scenes 1 + 10), only used if a floor projector is confirmed.

Built 2026-10-05 (Homie: "I think we should definitely finish the puddle"). The script's floor beats (Workshop Draft V1):
p.3 the group enters on a recent spill, Amina mopping; p.6 "Tant pis pour la flaque ! … Allez-vous-en! The water
disappears. Then it mysteriously returns, glowing." (lights on); p.7 BLACKOUT; p.8 Sarah slips on the puddle in the dark;
Scene 10: the floor is dry. So, from the approved pieces:

  S1_a_FLOOR_gallery                  SPILL held --tour s (still: q8, every frame identical)
  S1_a2_FLOOR_gallery-puddle-returns  cue "Allez-vous-en!": VANISH (approved dewet, 3.5 s) -> DRY --gap s ("Then…") ->
                                      the return (puddle_comp --flow, LIT, its last 8 s = one seamless glimmer cycle) ->
                                      that cycle looped to --returns s. The take's sound rides with the return.
  S1_b_FLOOR_gallery-blackout         the lit pool + glimmer, the lights cut with CENTRE's bank (frame 15, gallery_show's
                                      FAIL pattern; the glimmer is the water's own light and stays), then the DARK cycle
                                      looped to --dark-s s.
  S10_FLOOR_gallery                   DRY held --restored s (still).

Moving files are ProRes 422 HQ q2 (the house rule against shimmer); stills q8 (identical frames). 24 fps, stereo PCM.

  python tools/gallery_floor_show.py --floor-dir 1_READY_for_show_build/floor --lit RETURN_LIT.mov --dark RETURN_DARK.mov
         --out-dir DIR [--cycle 192] [--tour 900] [--gap 1.5] [--returns 480] [--dark-s 300] [--restored 300]
"""
import argparse
import os
import subprocess
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import puddle_comp as pc  # noqa: E402
from gallery_show import FAIL  # noqa: E402

CUT = 15          # CENTRE's bank (gallery_show: 12 + 3 * 1); the floor lies in front of CENTRE
PRORES = ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le', '-c:a', 'pcm_s24le']


def run(args):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *args], check=True)


def still(png, secs, out):
    run(['-loop', '1', '-framerate', '24', '-i', png, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
         *PRORES, '-qscale:v', '8', '-t', f'{secs}', out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--floor-dir', required=True)
    ap.add_argument('--lit', required=True, help='puddle_comp --flow LIT render ending in --cycle frames of hold')
    ap.add_argument('--dark', required=True, help='the same render with --dark')
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--cycle', type=int, default=192, help='frames in one glimmer cycle (puddle_comp --loop 8 s)')
    ap.add_argument('--tour', type=float, default=900)
    ap.add_argument('--gap', type=float, default=1.5)
    ap.add_argument('--returns', type=float, default=480)
    ap.add_argument('--dark-s', type=float, default=300)
    ap.add_argument('--restored', type=float, default=300)
    ap.add_argument('--files', default='a,a2,b,s10')
    a = ap.parse_args()
    os.makedirs(a.out_dir, exist_ok=True)
    fd = a.floor_dir
    spill, dry = os.path.join(fd, 'S1-GAL-FLOOR_SPILL_1920x1080.png'), os.path.join(fd, 'S1-GAL-FLOOR_DRY_1920x1080.png')
    vanish = os.path.join(fd, 'S1-GAL-FLOOR_VANISH_1920x1080.mov')
    out = lambda s: os.path.join(a.out_dir, s + '.mov')
    files = a.files.split(',')
    _, _, n_lit = pc.probe(a.lit)
    c0 = n_lit - a.cycle                       # first frame of the glimmer cycle in the LIT render

    if 'a' in files:
        still(spill, a.tour, out('S1_a_FLOOR_gallery'))
    if 's10' in files:
        still(dry, a.restored, out('S10_FLOOR_gallery'))
    if 'a2' in files:
        loops = int(np.ceil(a.returns / (a.cycle / 24))) + 1
        fc = (f'[0:v]setpts=PTS-STARTPTS[v0];[1:v]setpts=PTS-STARTPTS[v1];[2:v]split[c][k];'
              f'[c]setpts=PTS-STARTPTS[v2];'
              f'[k]trim=start_frame={c0},setpts=PTS-STARTPTS,loop=loop={loops}:size={a.cycle}:start=0,setpts=N/(24*TB)[v3];'
              f'[v0][v1][v2][v3]concat=n=4:v=1:a=0,fps=24[v];'
              f'[3:a]atrim=0:{3.5 + a.gap},asetpts=PTS-STARTPTS[s0];[2:a]asetpts=PTS-STARTPTS[s1];'
              f'[4:a]asetpts=PTS-STARTPTS[s2];[s0][s1][s2]concat=n=3:v=0:a=1[a]')
        run(['-i', vanish, '-loop', '1', '-framerate', '24', '-t', f'{a.gap}', '-i', dry, '-i', a.lit,
             '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
             '-filter_complex', fc, '-map', '[v]', '-map', '[a]', *PRORES, '-qscale:v', '2', '-ar', '48000',
             '-t', f'{a.returns}', out('S1_a2_FLOOR_gallery-puddle-returns')])
    if 'b' in files:
        _, _, n_dark = pc.probe(a.dark)
        lit = list(pc.frames(a.lit, 1920, 1080))[c0:]
        dark = list(pc.frames(a.dark, 1920, 1080))[n_dark - a.cycle:]
        tmp = tempfile.mkdtemp()
        first = os.path.join(tmp, 'first.mov')
        enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', '1920x1080',
                                '-r', '24', '-i', '-', '-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', '2',
                                '-pix_fmt', 'yuv422p10le', first], stdin=subprocess.PIPE)
        for j in range(a.cycle):               # one cycle: lit, the failure on CENTRE's frame, then dark
            k = 1.0 if j < CUT else (FAIL[j - CUT] if j - CUT < len(FAIL) else 0.0)
            f = dark[j] + k * (lit[j] - dark[j])
            enc.stdin.write((np.clip(f, 0, 1) * 65535 + 0.5).astype(np.uint16).tobytes())
        enc.stdin.close()
        enc.wait()
        loops = int(np.ceil(a.dark_s / (a.cycle / 24))) + 1
        fc = (f'[1:v]trim=start_frame={n_dark - a.cycle},setpts=PTS-STARTPTS,loop=loop={loops}:size={a.cycle}:start=0,setpts=N/(24*TB)[d];'
              f'[0:v][d]concat=n=2:v=1:a=0,fps=24[v]')
        run(['-i', first, '-i', a.dark, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-filter_complex', fc,
             '-map', '[v]', '-map', '2:a', *PRORES, '-qscale:v', '2', '-t', f'{a.dark_s}',
             out('S1_b_FLOOR_gallery-blackout')])
    for f in sorted(os.listdir(a.out_dir)):
        if 'FLOOR' in f and not f.startswith('._'):
            print(f)


if __name__ == '__main__':
    main()
