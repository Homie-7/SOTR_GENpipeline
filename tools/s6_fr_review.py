"""Scene 6 French cut: the WhatsApp-style three-wall review composite on Darrin's French track (Meeting 8, 20 Nov 2026).

Homie 17 Nov: "the WhatsApp-like scene composite ... so I can show it to them". REVIEW ONLY, never the show folder.
Reads the scale-0.5 review render (`render_s6.py --final --retime-fr ...`, ProRes 4444 with alpha, 121.25 s):
  LEFT / RIGHT  over black (in Sahaj's production ref the side walls are black when his fly-in starts)
  CENTRE        over Sahaj's fly-in, cut to the CENTRE wall like render_s6's own Sahaj read (ROOM rows 30:473):
                his frame 1 held under the whole scene, then his clip PLAYS for --tail s after 121.25 s, so Homie
                sees the hand-over into S7.
Sound = Darrin's wav (121.25 s), silence under the tail. Captions = render_s6.py LINES_FR / MOVES_FR (script V2, the
new track's seconds), read with ast like share_previews.s6_captions. Output written to _tmp_ and renamed when done.

  python tools/s6_fr_review.py [--render DIR] [--out FILE] [--tail 4] [--test SECONDS]
"""
import argparse
import ast
import os
import subprocess
import sys

TOOLS = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, TOOLS)
import share_previews as sp  # noqa: E402

REVIEW = 'D:/SOTR/SOTR_MEDIA/04_WORKING_FILES/S6_french_review'
WAV = 'G:/SOTR/HF/Final changes/Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav'
SAHAJ = 'D:/SOTR/SOTR_MEDIA/05_REFERENCE_UPLOADS/S6_handoff_Sahaj/A_flyin_m07v3_unity_03oct_ROOM.mp4'
SAHAJ_CROP = 'crop=738:443:591:30'      # ROOM 1920x1008: rows 30:473 = the room, CENTRE = x 1440..3240 of 4680
FR_DUR, FPS = 121.25, 24
TITLE = 'Scene 6  The Napoleonic Wars  (FRENCH CUT on Darrin\u2019s track, review)'


def fr_captions():
    tree = ast.parse(open(os.path.join(TOOLS, 'render_s6.py'), encoding='utf-8').read())
    v = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('LINES_FR', 'MOVES_FR')}
    moves = v['MOVES_FR'] + [(FR_DUR, 'HAND-OVER  \u00b7  S6 has ended (clear alpha); Sahaj\u2019s S7 fly-in plays '
                                       'under the CENTRE wall (his preview), side walls black')]
    return sp.moments_and_lines(moves, v['LINES_FR'], 4.5)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--render', default=os.path.join(REVIEW, 'render_scale05'))
    ap.add_argument('--out', default=os.path.join(REVIEW, '06_S6_wars_FRENCH_review.mp4'))
    ap.add_argument('--tail', type=float, default=4.0)
    ap.add_argument('--test', type=float, default=0)
    a = ap.parse_args()

    walls = [os.path.join(a.render, f'S6_{w}.mov') for w in ('LEFT', 'CENTRE', 'RIGHT')]
    info = [sp.ffprobe(p) for p in walls]
    for p, i in zip(walls, info):
        if i['dur'] < FR_DUR - 0.05:
            sys.exit(f'{p}: {i["dur"]:.2f} s, short of {FR_DUR}')
    n_s6, n_tail = int(round(FR_DUR * FPS)), int(round(a.tail * FPS))
    total = (n_s6 + n_tail) / FPS
    dur = min(total, a.test) if a.test else total
    cw, ch, boxes = sp.layout([(i['w'], i['h']) for i in info])
    out_dir = os.path.dirname(a.out)
    ass = sp.captions_for('06_S6_wars_FRENCH_review', cw, ch, dur, out_dir, fr_captions())

    parts = []
    for k in range(3):
        _, _, w, h = boxes[k]
        parts.append(f'[{k}:v]trim=end_frame={n_s6},setpts=PTS-STARTPTS,scale={w}:{h}:flags=bicubic,format=rgba,'
                     f'tpad=stop_mode=add:stop={n_tail}:color=black@0.0[s{k}]')
        if k == 1:
            parts.append(f'[4:v]{SAHAJ_CROP},scale={w}:{h}:flags=bicubic,setsar=1,format=rgba,split[sa][sb]')
            parts.append(f'[sa]trim=end_frame=1,loop=loop={n_s6 - 1}:size=1,setpts=N/{FPS}/TB[hold]')
            parts.append(f'[sb]trim=start_frame=1:end_frame={1 + n_tail},setpts=PTS-STARTPTS[play]')
            parts.append('[hold][play]concat=n=2:v=1:a=0[bg1]')
        else:
            parts.append(f'color=c=black:s={w}x{h}:r={FPS}:d={total:.3f},format=rgba[bg{k}]')
        parts.append(f'[bg{k}][s{k}]overlay=0:0:format=auto:eof_action=pass,format=yuv420p,setsar=1[lane{k}]')
    fg = ';'.join(parts) + ';' + sp.wa_filter(cw, ch, boxes, TITLE, {0: 'lane0', 1: 'lane1', 2: 'lane2'}, 0.0, dur, ass)
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for p in walls:
        cmd += ['-i', p]
    cmd += ['-i', WAV, '-i', SAHAJ, '-filter_complex', fg + f';[3:a]apad=whole_dur={total:.3f}[a]',
            '-map', '[v]', '-map', '[a]', '-t', f'{dur:.3f}', *sp.wa_encode(str(FPS), dur, dur), a.out]
    sp.run(cmd, a.out, False, True)
    print('wrote', a.out, f'{dur:.2f} s', flush=True)


if __name__ == '__main__':
    main()
