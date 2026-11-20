"""Scene 9, Darren's cut: a 3-wall WhatsApp review on HIS audio (docs/S9-DARREN-CUT.md "Build"). Review only, 0 credits.

Built 2026-11-20 (Claude, worker for the M9 live chat). Reads the show folder, never writes to it.

THE CUT: court b5 goes from 101 s to 64.25 s (1542 frames, render_court.BEATS['5cut']), ending at mix 254.0 s once his
fade is over. Every file after it moves CUT = 882 frames (36.75 s) earlier: TOTAL 9580 -> 8698 frames.
HIS AUDIO: 'the judge TO BE CUT DOWN 19112026.mov' with SPLICE = 253.50-290.25 s removed, a straight splice. Both ends
lie inside his digital silence (< -85 dB per 10 ms from 253.41 to 290.31 s), so it is click-free, and the removal is
the same 36.75 s as the picture's, so his sound stays on our clock after the cut.
PICTURE: the 1080 show files (3_HD_1080_fallback, as share_previews.wa_s9), with b5 swapped for the cut file in
04_WORKING_FILES/S9_darren_cut/. Captions = s9_animatic's, with b5's three segments re-pinned to the new strikes
(0.5 / 22.17 / 52.71 s) and everything after b5 shifted by the cut.

  python tools/s9_darren_review.py OUT.mp4 [--b5 PATH] [--b3 PATH] [--b7 PATH] [--title T] [--test SECONDS] [--dry]
  (--b3/--b7/--title added 2026-11-20 for the generated-judge review, tools/court_gen.py; defaults unchanged)
  python tools/s9_darren_review.py OUT.mp4 --verify      (his mix vs the review's sound, lag + correlation per window)

--mix21 (M10b, 2026-11-21, Homie: "The sound Darrin has made is finalised so we will follow it"): his new mix
'G:/SOTR/HF/the judge TO BE CUT DOWN 21112026.mov' plays UNCUT (399.17 s, no splice: he filled the old b5 silence with
new sound at 269-285 s), so b5 runs its full 2424 frames; give --b5 the full-length file. Plus Homie's 1:49-1:57 note:
the salon (RIGHT) and court b3 (CENTRE) end at PAINT_AT = 109.0 s and the LEFT painting comes up there, holding b4's
first frame until its own start (117.38 s), so b4's picture keeps its timing against his sound.
Heavy: run with CPU affinity FFFF3FFF (off Core 7). Writes to a _tmp_ name, renamed when ffmpeg finishes.
"""
import argparse
import os
import subprocess
import sys

import numpy as np

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import s9_animatic as s9  # noqa: E402
import share_previews as sp  # noqa: E402

MIX = r'G:\SOTR\HF\Final changes\the judge TO BE CUT DOWN 19112026.mov'
WORK = r'D:\SOTR\SOTR_MEDIA\04_WORKING_FILES\S9_darren_cut'
B5 = os.path.join(WORK, 'S9_b5_CENTRE_court_DARREN-CUT.mov')
FOLDER = os.path.join(sp.SRC, sp.FALLBACK)
B5_NAME = 'S9_b5_CENTRE_court.mov'
B5_N = 1542                              # render_court.BEATS['5cut'] length 64.25 s
CUT = 2424 - B5_N                        # 882 frames = 36.75 s
SPLICE = (253.50, 253.50 + CUT / s9.FPS)  # in his mix, seconds: inside his silence 253.41-290.31
TITLE = "Scene 9  The Aftermath  (DARREN'S CUT: court b5 101 s -> 64.25 s, review only)"
MIX21 = r'G:\SOTR\HF\the judge TO BE CUT DOWN 21112026.mov'
PAINT_AT = 2616                          # frames = 109.0 s: the LEFT painting comes up here (--mix21)
B4_NAME = 'S9_b4_LEFT_studio.mov'
ENDS_AT_PAINT = ('S9_b2-3_RIGHT_salon.mov', 'S9_b3_CENTRE_court.mov')
PAINT = False


def use_mix21():
    global MIX, B5_N, CUT, SPLICE, PAINT
    MIX, B5_N, CUT, PAINT = MIX21, 2424, 0, True
    SPLICE = (None, None)


def clips(b5, b3=None, b7=None):
    """[(path, wall index, first frame, hold, end)] on the cut timeline (hold = frames of the first frame shown
    before the file plays, end = last frame cap; --mix21 painting note only). b3/b7 = optional replacement court files
    (the generated-judge review, tools/court_gen.py); None = the show's own file."""
    b5_start = s9.S[B5_NAME] * s9.FPS
    wall = {'L': 0, 'C': 1, 'R': 2}
    out = []
    for name, w, start in s9.CLIPS:
        path = b5 if name == B5_NAME else os.path.join(FOLDER, name)
        if name == 'S9_b3_CENTRE_court.mov' and b3:
            path = b3
        if name == 'S9_b7_CENTRE_court.mov' and b7:
            path = b7
        start = int(round(start))
        if start > b5_start:
            start -= CUT
        hold, end = 0, None
        if PAINT and name == B4_NAME:
            hold, start = start - PAINT_AT, PAINT_AT
        if PAINT and name in ENDS_AT_PAINT:
            end = PAINT_AT
        out.append((path, wall[w], start, hold, end))
    return out


def lines():
    """s9_animatic's captions, retimed: b5's segments onto the new strikes, everything after b5 shifted"""
    b5, b6 = s9.S[B5_NAME], s9.S['S9_b6_LEFT_studio.mov']
    knots = [(0.0, 0.0), (0.5, 0.5), (45.0, 22.17), (85.0, 52.71), (100.5, 64.0), (101.0, 64.25)]
    xs, ys = zip(*knots)

    def remap(t):
        if not CUT:
            return t
        if t >= b6 - 1e-6:
            return t - CUT / s9.FPS
        if t >= b5:
            return b5 + float(np.interp(t - b5, xs, ys))
        return t
    keep = s9.SEGMENTS
    try:
        s9.SEGMENTS = [(remap(t0), remap(t1), items) for t0, t1, items in keep]
        ln = s9.timed_lines()
    finally:
        s9.SEGMENTS = keep
    beats = [(remap(t), txt) for t, txt in s9.BEATS]
    return beats, ln


def mix_audio(wav, dur):
    if not CUT:
        subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', MIX, '-map', '0:a:0', '-af', f'atrim=0:{dur:.4f}',
                               '-c:a', 'pcm_s24le', wav])
        return
    a, b = SPLICE
    subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', MIX, '-filter_complex',
                           f'[0:a]atrim=0:{a:.4f},asetpts=PTS-STARTPTS[x];[0:a]atrim=start={b:.4f},asetpts=PTS-STARTPTS[y];'
                           f'[x][y]concat=n=2:v=0:a=1,atrim=0:{dur:.4f}[o]', '-map', '[o]', '-c:a', 'pcm_s24le', wav])


def build(out, b5, test, dry, b3=None, b7=None, title=TITLE):
    cl = clips(b5, b3, b7)
    total = s9.TOTAL - CUT
    n1 = min(total, int(round(test * s9.FPS))) if test else total
    dur = n1 / s9.FPS
    info = [sp.ffprobe(p) for p, *_ in cl]
    size = {}
    for (_, w, *_), i in zip(cl, info):
        size.setdefault(w, (i['w'], i['h']))
    cw, ch, boxes = sp.layout([size[0], size[1], size[2]])
    beats, ln = lines()
    ass = sp.captions_for('S9_darren_cut', cw, ch, dur, os.path.dirname(out), sp.moments_and_lines(beats, ln))
    parts = []
    for li in range(3):
        _, _, w, h = boxes[li]
        pix = 'setsar=1,format=yuv420p'
        segs, pos = [], 0
        mine = sorted((c[2], k) for k, c in enumerate(cl) if c[1] == li)
        for j, (start, k) in enumerate(mine):
            hold, end = cl[k][3], cl[k][4]
            n = int(round(info[k]['dur'] * s9.FPS)) + hold
            if j + 1 < len(mine):
                n = min(n, mine[j + 1][0] - start)
            if end is not None:
                n = min(n, end - start)
            if start > pos:
                parts.append(f'color=c=black:s={w}x{h}:r={s9.FPS},trim=end_frame={start - pos},{pix}[g{li}_{j}]')
                segs.append(f'[g{li}_{j}]')
            f = s9.FADE
            tp = f'tpad=start={hold}:start_mode=clone,' if hold else ''
            parts.append(f'[{k}:v]fps={s9.FPS},{tp}trim=end_frame={n},scale={w}:{h}:flags=bicubic,{pix},'
                         f'fade=t=in:s=0:n={f},fade=t=out:s={n - f}:n={f}[c{li}_{j}]')
            segs.append(f'[c{li}_{j}]')
            pos = start + n
        if total > pos:
            parts.append(f'color=c=black:s={w}x{h}:r={s9.FPS},trim=end_frame={total - pos},{pix}[g{li}_end]')
            segs.append(f'[g{li}_end]')
        parts.append(''.join(segs) + f'concat=n={len(segs)}:v=1:a=0[lane{li}]')
    fg = ';'.join(parts) + ';' + sp.wa_filter(cw, ch, boxes, title, {0: 'lane0', 1: 'lane1', 2: 'lane2'}, 0.0, dur, ass)
    wav = os.path.join(os.path.dirname(out), '_tmp_captions', 'S9_darren_cut_sound.wav')
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for p, *_ in cl:
        cmd += ['-i', p]
    cmd += ['-i', wav, '-filter_complex', fg, '-map', '[v]', '-map', f'{len(cl)}:a:0', '-t', f'{dur:.3f}',
            *sp.wa_encode(str(s9.FPS), dur, dur), out]
    for p, w, st, hold, end in cl:
        print(f'  {["L", "C", "R"][w]}  {st:5d}  {st / s9.FPS:7.2f} s  hold {hold:4d}  end {end}  {os.path.basename(p)}')
    print(f'total {total} frames ({total / s9.FPS:.2f} s); his audio ' +
          (f'spliced {SPLICE[0]:.2f}-{SPLICE[1]:.2f} s' if CUT else f'uncut ({os.path.basename(MIX)})'))
    if not dry:
        mix_audio(wav, dur)
    sp.run(cmd, out, dry, False)


def pcm(path, sr=8000, extra=()):
    raw = subprocess.run(['ffmpeg', '-v', 'error', *extra, '-i', path, '-vn', '-ac', '1', '-ar', str(sr), '-f', 's16le',
                          '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0


def verify(out):
    """His mix vs the review's sound: the review at t must be his mix at t (before the splice) or t + CUT (after)."""
    sr = 8000
    d, o = pcm(MIX, sr), pcm(out, sr)
    sh = CUT / s9.FPS
    print(f'his mix {len(d) / sr:.2f} s, review {len(o) / sr:.2f} s (want {len(d) / sr - sh:.2f})')
    win, maxlag = int(4 * sr), int(0.25 * sr)
    for t in ((10, 100, 108, 112, 190, 212, 240, 250, 272, 300, 330, 350, 370, 390) if not CUT else
              (10, 100, 190, 212, 240, 250, 258, 300, 330, 350, 356)):
        src = t if (not CUT or t < SPLICE[0]) else t + sh
        a = o[int(t * sr):int(t * sr) + win]
        b = d[int(src * sr) - maxlag:int(src * sr) + win + maxlag]
        if len(a) < win or np.std(a) == 0:
            print(f'  {t:5.0f} s  (silent or past the end)')
            continue
        c = np.correlate(b, a, 'valid')
        k = int(np.argmax(np.abs(c)))
        bb = b[k:k + win]
        r = float(np.dot(a, bb) / (np.linalg.norm(a) * np.linalg.norm(bb) + 1e-12))
        print(f'  review {t:5.0f} s <- mix {src:7.2f} s   lag {(k - maxlag) / sr:+.4f} s   corr {r:.4f}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--b5', default=B5)
    ap.add_argument('--test', type=float, default=0)
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--b3', help='replacement court b3 file (e.g. the generated judge); default the show file')
    ap.add_argument('--b7', help='replacement court b7 file; default the show file')
    ap.add_argument('--title', default=TITLE)
    ap.add_argument('--mix21', action='store_true', help="M10b: Darren's 21112026 mix uncut + the 1:49 painting")
    a = ap.parse_args()
    if a.mix21:
        use_mix21()
    if a.verify:
        verify(a.out)
    else:
        build(a.out, a.b5, a.test, a.dry, a.b3, a.b7, a.title)


if __name__ == '__main__':
    main()
