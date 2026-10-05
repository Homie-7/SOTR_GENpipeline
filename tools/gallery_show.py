"""Build the Louvre gallery's show files (Scenes 1 + 10) for one wall from its finished LIT and DARK stills.

Built 2026-10-05. Homie chose: full length at 1080 for the show, 4K only as short backup hold loops. The gallery is a still
room (SHOTCARDS: "nothing moves in a museum"), so every file is the still held, and the only motion is the blackout:

  tour      LIT held for --tour s (Scene 1, from the tour to "Pas de flash ici!"; the script runs ~11 min).
  blackout  0.5 s LIT (so the operator's cut from `tour` is invisible), then the lights fail BANK BY BANK across the room
            (LEFT, then CENTRE 3 frames later, then RIGHT 3 more): each bank cuts, flickers back once, then dies.
            Then DARK held to --dark s (the whole dark scene, to Sarah's fall and the melt).
  restored  LIT held for --restored s (Scene 10, "Light is suddenly restored": the file opens at full picture).
  loops     --loops: LIT_HOLD and DARK_HOLD, --loop-s long (any still loops seamlessly), for the operator.

Files start and end at full picture (the operator owns the fades). ProRes 422 HQ yuv422p10le at --qscale (a still
encodes every frame identically, so the house q2 rule, which stops frame-to-frame shimmer in motion, buys nothing here:
q8 measured 44 dB PSNR vs the source, visually lossless, at ~40% of q2's size). A silent 48 kHz stereo track rides in
every file so the layout matches the other show files (nothing in the gallery is generated with sound).

  python tools/gallery_show.py --wall LEFT --lit LIT.png --dark DARK.png --size 1440x1080 --out-dir DIR
         [--tour 900] [--dark-s 300] [--restored 300] [--qscale 8] [--files tour,blackout,restored] [--loops --loop-s 32]
"""
import argparse
import os
import subprocess
import tempfile

import cv2
import numpy as np

BANK = {'LEFT': 0, 'CENTRE': 1, 'RIGHT': 2}
# per-frame light level after the bank's cut frame: cut, flicker back once, die (1.0 = lit, 0 = dark)
FAIL = [0.12, 0.0, 0.0, 0.45, 0.08, 0.0]


def load(p, size):
    im = cv2.imread(p, cv2.IMREAD_UNCHANGED)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB).astype(np.float32) / (65535.0 if im.dtype == np.uint16 else 255.0)
    if (im.shape[1], im.shape[0]) != size:
        im = cv2.resize(im, size, interpolation=cv2.INTER_AREA if im.shape[1] > size[0] else cv2.INTER_LANCZOS4)
    return im


def enc_args(q):
    return ['-c:v', 'prores_ks', '-profile:v', '3', '-qscale:v', str(q), '-pix_fmt', 'yuv422p10le',
            '-c:a', 'pcm_s24le', '-shortest']


def still(png, secs, out, q):
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-framerate', '24', '-i', png,
                    '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-t', f'{secs}', *enc_args(q),
                    '-t', f'{secs}', out], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wall', required=True, choices=list(BANK))
    ap.add_argument('--lit', required=True)
    ap.add_argument('--dark', required=True)
    ap.add_argument('--size', required=True)
    ap.add_argument('--out-dir', required=True)
    ap.add_argument('--tour', type=float, default=900)
    ap.add_argument('--dark-s', type=float, default=300)
    ap.add_argument('--restored', type=float, default=300)
    ap.add_argument('--qscale', type=int, default=8)
    ap.add_argument('--files', default='tour,blackout,restored')
    ap.add_argument('--loops', action='store_true')
    ap.add_argument('--loop-s', type=float, default=32)
    ap.add_argument('--suffix', default='')
    a = ap.parse_args()
    size = tuple(map(int, a.size.split('x')))
    os.makedirs(a.out_dir, exist_ok=True)
    tmp = tempfile.mkdtemp()
    lit, dark = load(a.lit, size), load(a.dark, size)
    lp, dp = os.path.join(tmp, 'lit.png'), os.path.join(tmp, 'dark.png')
    for im, p in ((lit, lp), (dark, dp)):
        cv2.imwrite(p, cv2.cvtColor((np.clip(im, 0, 1) * 65535 + 0.5).astype(np.uint16), cv2.COLOR_RGB2BGR))
    W = a.wall
    name = lambda s: os.path.join(a.out_dir, s + a.suffix + '.mov')
    files = a.files.split(',') if a.files else []
    if 'tour' in files:
        still(lp, a.tour, name(f'S1_a_{W}_gallery'), a.qscale)
    if 'restored' in files:
        still(lp, a.restored, name(f'S10_{W}_gallery'), a.qscale)
    if 'blackout' in files:
        n_trans = 48                                  # 2 s: 0.5 s lit, the failure, then dark
        cut = 12 + 3 * BANK[W]
        tdir = os.path.join(tmp, 'tr')
        os.makedirs(tdir)
        for i in range(n_trans):
            k = 1.0 if i < cut else (FAIL[i - cut] if i - cut < len(FAIL) else 0.0)
            fr = dark + k * (lit - dark)
            cv2.imwrite(os.path.join(tdir, f'{i:04d}.png'),
                        cv2.cvtColor((np.clip(fr, 0, 1) * 65535 + 0.5).astype(np.uint16), cv2.COLOR_RGB2BGR))
        # ONE pass (a filter join): a stream-copy concat of two encodes slipped its timestamps once (RIGHT, 2026-10-05:
        # 7200 frames reading as 308.5 s), so the transition and the dark hold are joined inside one encode.
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '24', '-i', os.path.join(tdir, '%04d.png'),
                        '-loop', '1', '-framerate', '24', '-t', f'{a.dark_s - n_trans / 24}', '-i', dp,
                        '-f', 'lavfi', '-t', f'{a.dark_s}', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-filter_complex', '[0:v][1:v]concat=n=2:v=1:a=0,fps=24[v]', '-map', '[v]', '-map', '2:a',
                        *enc_args(a.qscale), '-t', f'{a.dark_s}', name(f'S1_b_{W}_gallery-blackout')], check=True)
    if a.loops:
        still(lp, a.loop_s, name(f'S1-and-S10_{W}_gallery_LIT_HOLD_loop'), a.qscale)
        still(dp, a.loop_s, name(f'S1_{W}_gallery_DARK_HOLD_loop'), a.qscale)
    for f in sorted(os.listdir(a.out_dir)):
        if f.endswith(a.suffix + '.mov') and W in f:
            print(f)


if __name__ == '__main__':
    main()
