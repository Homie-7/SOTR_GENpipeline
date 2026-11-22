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
--d22 (M10o, 2026-11-22, Darren's notes "cut 3:03-3:09 ... snip 4:08-4:50"): his 22 Nov mix
'G:/SOTR/HF/Final changes/221126/the judge CUT DOWN 22112026_2.mov' on the --mix21 placement, then CUTS removed from
picture AND his sound as straight splices (Homie: "we will not make changes to Darren's sound itself at all"). All his
timecodes are on the uncut EXT3 clock. b5's "Bangs the gavel" caption is re-pinned to the moved strike (245-248 s uncut).
Total 9580 -> 8428 frames (351.17 s).
--e5 (M10p, 2026-11-22, Homie on EXT4): --d22, plus (1) an EASE at his two splices, nothing else done to his sound:
a half-sine fade-out of the OUTGOING sound only, FADES[i] s long, ending on the splice (3:03.0: 0.30 s, his sound
already falling -15 -> -26 dB into -46 dB; 4:02.0: 0.50 s, -8 dB into his digital silence); no fade-in (his sound
after each splice is his own entrance); (2) captions re-timed to the speech: every spoken line starts on the first
word faster-whisper (medium, en, word timings, no VAD) hears of it in the cut mix (WORDS json, review clock). Only
the JUDGE is a recorded voice in his mix (the salon/studio lines are the live actors): their lines and the stage
directions keep their estimate / picture events; a judge line not heard keeps its estimate; b5's
"Bangs the gavel" is re-pinned to the strike ON his gavel (243.0 s uncut, court_ext EXT_E5).
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
MIX22 = r'G:\SOTR\HF\Final changes\221126\the judge CUT DOWN 22112026_2.mov'
CUTS = []                                # [(start s, end s)] on the uncut clock, removed from picture + sound (--d22)
B5_KNOTS = None                          # b5-relative caption re-pin (--d22)
FADES = []                               # --e5: fade-out (s) of the outgoing sound into each splice, one per CUTS
WORDS = None                             # --e5: faster-whisper words [(start, end, word)] on the review clock


def use_mix21():
    global MIX, B5_N, CUT, SPLICE, PAINT
    MIX, B5_N, CUT, PAINT = MIX21, 2424, 0, True
    SPLICE = (None, None)


def use_d22():
    global MIX, CUTS, B5_KNOTS
    use_mix21()
    MIX = MIX22
    CUTS = [(183.0, 189.0), (248.0, 290.0)]
    # b5 seg 1 (0.5-45) unchanged; seg 2 ends at the moved strike's lead-in; seg 3 "Bangs the gavel" -> 245.0-248.0 s
    B5_KNOTS = [(0.0, 0.0), (45.0, 45.0), (85.0, 245.0 - 189.75), (100.5, 248.0 - 189.75), (101.0, 101.0)]


def use_e5(words):
    global FADES, WORDS, B5_KNOTS
    import json
    use_d22()
    FADES = [0.30, 0.50]
    B5_KNOTS = [(0.0, 0.0), (45.0, 45.0), (85.0, 243.0 - 189.75), (100.5, 248.0 - 189.75), (101.0, 101.0)]
    WORDS = json.load(open(words, encoding='utf-8'))


def _toks(text):
    import re
    import unicodedata
    t = re.sub(r'\([^)]*\)', ' ', text)
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode().lower()
    return re.findall(r"[a-z0-9]+", t)


def speech_times(ln):
    """M10p: each spoken line -> the start of its first word heard in the cut mix (difflib alignment of all spoken
    lines against all heard words, in order). Returns {line index: t}."""
    import difflib
    ref, own = [], []
    for i, (t, sp, tx) in enumerate(ln):
        if sp == s9.JU and 'gavel' not in tx:   # the judge is the only recorded voice; the others are live actors
            for w in _toks(tx):
                ref.append(w)
                own.append(i)
    heard = [(w0, tk) for w0, w1, wd in WORDS for tk in _toks(wd)]
    sm = difflib.SequenceMatcher(None, ref, [tk for _, tk in heard], autojunk=False)
    hits = {}
    for a, b, n in sm.get_matching_blocks():
        for k in range(n):
            hits.setdefault(own[a + k], []).append(heard[b + k][0])
    out = {}
    for i, ts in hits.items():
        n_words = sum(1 for o in own if o == i)
        if len(ts) >= min(2, n_words):
            out[i] = min(ts)
    return out


def cut_frames():
    return [(int(round(a * s9.FPS)), int(round(b * s9.FPS))) for a, b in CUTS]


def cutmap(t):
    """uncut seconds -> cut seconds (a time inside a cut lands on the splice)"""
    s = t
    for a, b in CUTS:
        if t >= b:
            s -= b - a
        elif t > a:
            s -= t - a
    return s


def uncut(t):
    """cut seconds -> uncut seconds (his mix clock)"""
    for a, b in sorted(CUTS):
        if t >= a - 1e-9:
            t += b - a
    return t


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
        if CUTS:
            if B5_KNOTS and b5 <= t < b6 - 1e-6:
                kx, ky = zip(*B5_KNOTS)
                t = b5 + float(np.interp(t - b5, kx, ky))
            return cutmap(t)
        if not CUT:
            return t
        if t >= b6 - 1e-6:
            return t - CUT / s9.FPS
        if t >= b5:
            return b5 + float(np.interp(t - b5, xs, ys))
        return t
    keep = s9.SEGMENTS
    try:
        s9.SEGMENTS = [(a, b, items) for a, b, items in ((remap(t0), remap(t1), items) for t0, t1, items in keep)
                       if b - a > 0.05]
        ln = s9.timed_lines()
    finally:
        s9.SEGMENTS = keep
    beats = [(remap(t), txt) for t, txt in s9.BEATS]
    if WORDS:
        st = speech_times(ln)
        new = [st.get(i, t) for i, (t, _, _) in enumerate(ln)]
        for i, (t, sp, tx) in enumerate(ln):
            print(f'  caption {t:7.2f} -> {new[i]:7.2f}  {"heard" if i in st else "est. "}  {sp[:10]:10s} {tx[:60]}')
        ln = sorted(((new[i], sp, tx) for i, (t, sp, tx) in enumerate(ln)), key=lambda r: r[0])
    return beats, ln


def mix_audio(wav, dur):
    if CUTS:                                 # straight splices, nothing else done to his sound
        keep, t = [], 0.0
        for a, b in sorted(CUTS):
            keep.append((t, a))
            t = b
        fd = FADES or [0] * len(keep)            # --e5: ease the outgoing sound into each splice
        fc = ''.join(f'[0:a]atrim=start={x:.4f}' + (f':end={y:.4f}' if y else '') + ',asetpts=PTS-STARTPTS' +
                     (f',afade=t=out:st={y - x - fd[i]:.4f}:d={fd[i]:.4f}:curve=hsin' if y and fd[i] else '') + f'[k{i}];'
                     for i, (x, y) in enumerate(keep + [(t, None)]))
        n = len(keep) + 1
        fc += ''.join(f'[k{i}]' for i in range(n)) + f'concat=n={n}:v=0:a=1,atrim=0:{dur:.4f}[o]'
        subprocess.check_call(['ffmpeg', '-v', 'error', '-y', '-i', MIX, '-filter_complex', fc, '-map', '[o]',
                               '-c:a', 'pcm_s24le', wav])
        return
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
    cf = cut_frames()
    lane_total = total
    total -= sum(b - a for a, b in cf)
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
        if lane_total > pos:
            parts.append(f'color=c=black:s={w}x{h}:r={s9.FPS},trim=end_frame={lane_total - pos},{pix}[g{li}_end]')
            segs.append(f'[g{li}_end]')
        if cf:                               # --d22: drop the cut frame spans (uncut clock), then re-time
            sel = '+'.join(f'between(n\\,{a}\\,{b - 1})' for a, b in cf)
            parts.append(''.join(segs) + f'concat=n={len(segs)}:v=1:a=0[raw{li}]')
            parts.append(f"[raw{li}]select='not({sel})',setpts=N/({s9.FPS}*TB)[lane{li}]")
        else:
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
          (f'cut {CUTS} ' + (f'(fade-out {FADES} s hsin into each splice)' if FADES else '(straight splices)') + f' {os.path.basename(MIX)}' if CUTS else f'spliced {SPLICE[0]:.2f}-{SPLICE[1]:.2f} s' if CUT else f'uncut ({os.path.basename(MIX)})'))
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
    sh = CUT / s9.FPS + sum(b - a for a, b in CUTS)
    print(f'his mix {len(d) / sr:.2f} s, review {len(o) / sr:.2f} s (want {len(d) / sr - sh:.2f})')
    win, maxlag = int(4 * sr), int(0.25 * sr)
    pts = (10, 100, 150, 178, 186, 200, 225, 236, 240, 246, 260, 290, 320, 340, 347) if CUTS else None
    for t in pts or ((10, 100, 108, 112, 190, 212, 240, 250, 272, 300, 330, 350, 370, 390) if not CUT else
              (10, 100, 190, 212, 240, 250, 258, 300, 330, 350, 356)):
        src = uncut(t) if CUTS else (t if (not CUT or t < SPLICE[0]) else t + sh)
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
    ap.add_argument('--d22', action='store_true', help="M10o: Darren's 22112026_2 mix, uncut placement + his two cuts")
    ap.add_argument('--e5', metavar='WORDS_JSON', help="M10p: --d22 + eased splices + captions on the heard speech")
    a = ap.parse_args()
    if a.e5:
        use_e5(a.e5)
    elif a.d22:
        use_d22()
    elif a.mix21:
        use_mix21()
    if a.verify:
        verify(a.out)
    else:
        build(a.out, a.b5, a.test, a.dry, a.b3, a.b7, a.title)


if __name__ == '__main__':
    main()
