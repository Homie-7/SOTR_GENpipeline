"""Light copies of the show for sharing: Darrin's proxies (the sound designer) and three-wall WhatsApp previews.

Built 2026-10-24 (Homie). Reads the show folder, never writes to it. Two jobs:

  darrin    Every file in folders 1, 2, 4 and 5 of 01_FINAL_FOR_SHOW (folder 3 is the same picture at 1080, skipped),
            same folder and file names, as H.264 MP4 540 px tall, same frame rate, full length, the file's own sound
            as AAC 192k, with the file name, the time and the frame number burned in. Plus 00_READ_ME_DARRIN.txt.
  whatsapp  One MP4 per scene, numbered in play order, the three walls side by side as the audience sees them
            (LEFT | CENTRE | RIGHT), every wall the same height at its own proportions (4:3 / 5:3 / 4:3; Scenes 4 and 5
            are 16:9 renders and keep 16:9), ~1600 px wide, each file capped to stay under ~95 MB. Under the walls a
            caption bar from the script: the moment in the scene, and the line being spoken (Scenes 6 and 9, timed as in
            their animatics: render_s6.py LINES/MOVES, s9_animatic.py) or what happens (the scenes cut on cue).
            Scene 9 = the real show timeline (s9_animatic.CLIPS: the court comes in under the salon's last 40 s, every
            file with the operator's 0.5 s fades), each file's own sound mixed at its place. Scene 7 = Homie's ship,
            WORK IN PROGRESS (04_WORKING_FILES): the intro v8, then the light-arc preview v3. Sound = the CENTRE file's.

Every output is written to a _tmp_ name and renamed only when ffmpeg finishes; an existing output is skipped (so a
crashed run resumes) unless --force. --check probes every output against its source (length, frame rate, sound).
Heavy: run with CPU affinity FFFF3FFF (off Core 7).

  python tools/share_previews.py --job darrin|whatsapp|both [--src DIR] [--darrin-out DIR] [--wa-out DIR]
         [--test SECONDS] [--only SUBSTRING] [--force] [--check] [--dry]
"""
import argparse
import json
import os
import subprocess
import sys

SRC = 'D:/SOTR/SOTR_MEDIA/01_FINAL_FOR_SHOW'
DARRIN_OUT = 'D:/SOTR/FOR DARRIN'
WA_OUT = 'D:/SOTR/WHATSAPP_3_wall_previews'
DARRIN_FOLDERS = ['1_PLAY_THESE_IN_ORDER', '2_BACKUP_LOOPS_for_operator', '4_CLIENT_OPTION_S5_cold_dusk',
                  '5_FLOOR_only_if_a_floor_projector']
FONT = 'C\\:/Windows/Fonts/consola.ttf'
PLAY = '1_PLAY_THESE_IN_ORDER'

# (output name, title, folder, (LEFT, CENTRE, RIGHT) files) for the scenes that use all three walls at once
FALLBACK = '3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER'   # Scenes 6 + 9 at 1080: the same picture, timing and sound
SCENES = [
    ('01_S1_a_gallery', 'Scene 1  Au Louvre  (the tour)', PLAY,
     ('S1_a_LEFT_gallery.mov', 'S1_a_CENTRE_gallery.mov', 'S1_a_RIGHT_gallery.mov')),
    ('02_S1_b_gallery-blackout', 'Scene 1  Au Louvre  (the blackout)', PLAY,
     ('S1_b_LEFT_gallery-blackout.mov', 'S1_b_CENTRE_gallery-blackout.mov', 'S1_b_RIGHT_gallery-blackout.mov')),
    ('03_S4_alps', 'Scene 4  The Alps', PLAY, ('S4_LEFT_alps.mov', 'S4_CENTRE_alps.mov', 'S4_RIGHT_alps.mov')),
    ('04_S5_camps', 'Scene 5  The camps  (rich dusk)', PLAY,
     ('S5_LEFT_camps.mov', 'S5_CENTRE_camps.mov', 'S5_RIGHT_camps.mov')),
    ('05_S5_camps_OPTION_cold-dusk', 'Scene 5  The camps  (OPTION: cold dusk)', '4_CLIENT_OPTION_S5_cold_dusk',
     ('S5_LEFT_camps_cold-dusk.mov', 'S5_CENTRE_camps_cold-dusk.mov', 'S5_RIGHT_camps_cold-dusk.mov')),
    ('06_S6_wars', 'Scene 6  The Napoleonic Wars', FALLBACK, ('S6_LEFT_wars.mov', 'S6_CENTRE_wars.mov', 'S6_RIGHT_wars.mov')),
    ('09_S10_gallery', 'Scene 10  Back at the Louvre', PLAY,
     ('S10_LEFT_gallery.mov', 'S10_CENTRE_gallery.mov', 'S10_RIGHT_gallery.mov')),
]
S9_NAME, S9_TITLE = '08_S9_aftermath', 'Scene 9  The Aftermath'
S7_NAME = '07_S7_ship_WORK-IN-PROGRESS'
S7_TITLE = 'Scene 7  Expedition to Senegal  (Homie\u2019s ship, WORK IN PROGRESS)'
S7_DIR = 'D:/SOTR/SOTR_MEDIA/04_WORKING_FILES/S7_ship'
# the intro v8 (4680x1080), then the light-arc preview v3 (2340x540: day, magic hour, sunset, night; hold 7 s, xfade 2 s)
S7_FILES = ('4_intro_video/rev/S7-INTRO_3walls_v8_INTO_DAY_IDLE.mp4', '6_review/S7-SHIP_idle_arc_preview_v3.mp4')
WALL_NAMES = ('LEFT', 'CENTRE (back wall)', 'RIGHT')
TOOLS = os.path.dirname(os.path.abspath(__file__))

# the caption bar for the scenes cut on cue (no timed lines): [(from s, moment, speaker, line)]; '' speaker = what happens
CAPTIONS = {
    '01_S1_a_gallery': [
        (0, 'THE TOUR  \u00b7  plays under the whole tour; the operator cuts to the blackout on the cue', '',
         '(Martin leads the tour group through the gallery: Louis XVI and Marie-Antoinette (left), the Raft of the '
         'Medusa (centre), Napol\u00e9on (right). Amina keeps trying to mop up a strange puddle on the floor.)')],
    '02_S1_b_gallery-blackout': [
        (0, 'CUE: Sarah\u2019s selfie flash  \u00b7  the lights fail bank by bank', 'MARTIN',
         'Non! Mademoiselle! Excusez-moi. NON! Pas de flash ici!'),
        (4, 'BLACKOUT  \u00b7  the whole dark scene plays on this, to Sarah\u2019s fall', '',
         '(In the dark: Martin is called away with his torch, Amina tells the group a story, and Sarah slips on the '
         'glowing puddle and falls.)')],
    '03_S4_alps': [
        (0, 'FLASHBACK  \u00b7  Laux, in the Hautes-Alpes  \u00b7  a movement scene to music', '',
         '(Agn\u00e8s, 16, works the fields with her younger sister. A soldier of Napol\u00e9on\u2019s army appears; '
         'she gives him bread and water, and leaves with him.)')],
    '04_S5_camps': [
        (0, 'BATTLEFIELDS OF FRANCE  \u00b7  the army camps at dusk', '',
         '(Agn\u00e8s, back in the present: \u201cOui, c\u2019\u00e9tait Henri.\u201d Fifteen years, two babies lost. '
         'A wounded soldier: the Austrians are coming. An errant cannonball; smoke and darkness cover the camp.)')],
    '09_S10_gallery': [
        (0, 'BACK AT THE LOUVRE  \u00b7  light is suddenly restored', '',
         '(Sarah wakes, Martin by her side; Ann rushes in. Amina gives back the phone: \u201cYou were there! In that '
         'painting!\u201d On to the Mona Lisa. FIN.)')],
}
CAPTIONS['05_S5_camps_OPTION_cold-dusk'] = CAPTIONS['04_S5_camps']

# composite layout: TOP the title row, the walls, BOTTOM their labels, CAP the caption bar
WA_W, MARGIN, GAP, MAX_H, TOP, BOTTOM, CAP = 1600, 10, 10, 360, 40, 30, 92
BG, UNLIT = '0x262626', '0x000000'
WA_MB = 95

README = """FOR DARRIN (SOUND DESIGNER) - SECRET OF THE RAFT PROJECTIONS                       {date}
From Homie.

WHAT THIS IS
  Light preview copies of every projection file in the show, so you can line sound up against the picture.
  They are NOT the show files (those are 4K / ProRes and very large); the picture and timing are identical:
  same length, same frame rate, same frame count. Burned into every picture: the file's name (top left) and
  the time and frame number (bottom left; the time is from the start of the file, frames count from 0).

WHERE TO START
  1_PLAY_THESE_IN_ORDER/   THE SHOW. This is the one that matters. In script order:
    Scene 1   S1_a_*  (15:00, the tour)  then  S1_b_*  (5:00, the blackout, cue "Pas de flash ici!")
    Scene 4   S4_*    (2:53)
    Scene 5   S5_*    (7:11)
    Scene 6   S6_*    (2:45)
    Scene 9   S9_b2-3_RIGHT_salon  S9_b3_CENTRE_court  S9_b4_LEFT_studio  S9_b5_CENTRE_court
              S9_b6_LEFT_studio  S9_b7_CENTRE_court  S9_b8_RIGHT_salon  S9_b9_LEFT_studio
    Scene 10  S10_*   (5:00)
  (Windows sorts S10 above S1; play order is as listed here.)

  Scenes 1, 4, 5, 6 and 10: three files per scene, one per wall (LEFT, CENTRE = the back wall, RIGHT, as the
  audience sees them). They start together and stay in sync, and the three carry the SAME sound track, so for
  sound you only need one of them (the CENTRE file).
  Scene 9: one file per beat, each on its own wall, played one after another in the order above.

ABOUT THE SOUND IN THESE FILES
  Scenes 6 and 9 carry a rough scratch track (the sound that came out of the generated clips). It is a
  reference only, not the sound design: use it, replace it or ignore it.
  Scenes 1, 4, 5 and 10 are SILENT: their sound track is there but empty. Nothing to match there except picture.

THE OTHER FOLDERS (only if you need them)
  2_BACKUP_LOOPS_for_operator/        Short seamless loops the operator can hold if a scene runs longer than its file.
                                      They loop, so any sound under them has to loop too.
  4_CLIENT_OPTION_S5_cold_dusk/       A second look for Scene 5 the client may choose instead. Same timing as S5.
  5_FLOOR_only_if_a_floor_projector/  Floor images, only used if the floor is projected (not confirmed yet).
  (There is no folder 3: in the show folder it is the same picture at a lower resolution.)

Questions: Homie.
"""


def ffprobe(path):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'format=duration:stream=codec_type,width,height,r_frame_rate,nb_frames', '-of', 'json', path],
                       capture_output=True, text=True, check=True)
    j = json.loads(r.stdout)
    v = next(s for s in j['streams'] if s['codec_type'] == 'video')
    n, d = v['r_frame_rate'].split('/')
    return {'dur': float(j['format']['duration']), 'w': int(v['width']), 'h': int(v['height']),
            'fps': float(n) / float(d), 'rate': v['r_frame_rate'],
            'audio': any(s['codec_type'] == 'audio' for s in j['streams'])}


def even(x):
    return max(2, int(round(x / 2.0)) * 2)


def esc(t):
    """Escape text for a drawtext text='...' value inside a filtergraph."""
    return t.replace('\\', '\\\\').replace(':', '\\:').replace("'", "\u2019").replace('%', '\\%').replace(',', '\\,')


def run(cmd, out, dry, force):
    if os.path.exists(out) and not force:
        print(f'skip (exists)  {out}', flush=True)
        return
    print(f'make  {out}', flush=True)
    if dry:
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = os.path.join(os.path.dirname(out), '_tmp_' + os.path.basename(out))
    subprocess.run(cmd[:-1] + [tmp], check=True)
    os.replace(tmp, out)


# ---------------------------------------------------------------- darrin

def darrin_jobs(src, out):
    for folder in DARRIN_FOLDERS:
        for f in sorted(os.listdir(os.path.join(src, folder))):
            if f.lower().endswith('.mov') and not f.startswith(('._', '_tmp_')):
                yield os.path.join(src, folder, f), os.path.join(out, folder, os.path.splitext(f)[0] + '.mp4')


def darrin_cmd(inp, out, test):
    name = esc(os.path.splitext(os.path.basename(inp))[0])
    box = f"fontfile='{FONT}':fontsize=18:fontcolor=white:box=1:boxcolor=black@0.55:boxborderw=5"
    vf = (f"scale=-2:540:flags=bicubic,"
          f"drawtext={box}:x=10:y=10:text='{name}',"
          f"drawtext={box}:x=10:y=h-th-12:text='%{{pts\\:hms}}   frame %{{frame_num}}'")
    t = ['-t', str(test)] if test else []
    return ['ffmpeg', '-v', 'error', '-y', '-i', inp, *t, '-map', '0:v:0', '-map', '0:a:0?', '-vf', vf,
            '-c:v', 'libx264', '-preset', 'medium', '-crf', '23', '-pix_fmt', 'yuv420p', '-fps_mode', 'passthrough',
            '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', out]


# ---------------------------------------------------------------- the composite

def layout(sizes):
    """Wall boxes (x, y, w, h) at one shared height, each at its own aspect, centred on a ~WA_W canvas."""
    aspects = [w / h for w, h in sizes]
    h = min(MAX_H, (WA_W - 2 * MARGIN - 2 * GAP) / sum(aspects))
    h = int(h) // 2 * 2
    ws = [even(a * h) for a in aspects]
    cw = even(sum(ws) + 2 * GAP + 2 * MARGIN)
    x = (cw - (sum(ws) + 2 * GAP)) // 2
    boxes = []
    for w in ws:
        boxes.append((x, TOP, w, h))
        x += w + GAP
    return cw, TOP + h + BOTTOM + CAP, boxes


# ---------------------------------------------------------------- the caption bar

def moments_and_lines(moves, lines, hold=None):
    """[(t, moment, speaker, line)] at every change of either; a line shows `hold` s, or (None) until the next one"""
    ev = {t for t, _ in moves} | {t for t, _, _ in lines}
    if hold:
        ev |= {t + hold for t, _, _ in lines}
    out = []
    for t in sorted(ev):
        mo = ([m for m in moves if m[0] <= t + 1e-6] or [(0, '')])[-1][1]
        cur = [ln for ln in lines if ln[0] <= t + 1e-6]
        if cur and hold:
            nxt = [ln[0] for ln in lines if ln[0] > cur[-1][0]]
            if t >= min(cur[-1][0] + hold, nxt[0] if nxt else 1e9) - 1e-6:
                cur = []
        sp, tx = (cur[-1][1], cur[-1][2]) if cur else ('', '')
        if not out or out[-1][1:] != (mo, sp, tx):
            out.append((t, mo, sp, tx))
    return out


def s6_captions():
    """render_s6.py's MOVES and LINES (each line 4.5 s or to the next), read without importing it (cv2)"""
    import ast
    tree = ast.parse(open(os.path.join(TOOLS, 'render_s6.py'), encoding='utf-8').read())
    v = {n.targets[0].id: ast.literal_eval(n.value) for n in tree.body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('LINES', 'MOVES')}
    return moments_and_lines(v['MOVES'], v['LINES'], 4.5)


def s7_captions(intro):
    deck = ('(Sarah and Amina reappear as sailors beside Agn\u00e8s on the deck and load the boat, in a comic operatic '
            'style. AGN\u00c8S: \u201cAllons en Afrique!\u201d)')
    caps = [(0, 'THE ARRIVAL  \u00b7  a gull flies in from the sea and lands on the deck', '',
             '(We hear the waves and seagulls. The rising and falling deck of the frigate Medusa is revealed.)')]
    for k, st in enumerate(('DAY', 'MAGIC HOUR', 'SUNSET', 'NIGHT')):
        caps.append((intro + (k * 9 - 1 if k else 0), f'THE DECK  \u00b7  the four light states, a preview:  {st}', '',
                     deck))
    return caps


def ass_time(t):
    t = max(0.0, t)
    return f'{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}'


def write_ass(path, caps, cw, ch, dur):
    """the caption bar as an ASS file in canvas pixels: the moment (grey) over the line (white; what happens, warm)"""
    y0 = ch - CAP + 6
    style = 'Style: {},Arial,{},&H00{c},&H00{c},&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,7,{m},{m},{v},1'
    head = ['[Script Info]', 'ScriptType: v4.00+', f'PlayResX: {cw}', f'PlayResY: {ch}', 'WrapStyle: 0',
            'ScaledBorderAndShadow: yes', '', '[V4+ Styles]',
            'Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, '
            'Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, '
            'MarginL, MarginR, MarginV, Encoding',
            style.format('Moment', 17, c='9A9A9A', m=MARGIN + 4, v=y0),
            style.format('Line', 21, c='F2F2F2', m=MARGIN + 4, v=y0 + 24),
            style.format('Desc', 20, c='B4C8D6', m=MARGIN + 4, v=y0 + 24),
            '', '[Events]', 'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
    clean = lambda x: x.replace('\\', '/').replace('{', '(').replace('}', ')').replace('\n', ' ')
    caps = [c for c in caps if c[0] < dur]
    ev = []
    for k, (t, mo, sp, tx) in enumerate(caps):
        t1 = caps[k + 1][0] if k + 1 < len(caps) else dur + 1
        if mo:
            ev.append(f'Dialogue: 0,{ass_time(t)},{ass_time(t1)},Moment,,0,0,0,,{clean(mo)}')
        if tx:
            ev.append(f'Dialogue: 0,{ass_time(t)},{ass_time(t1)},{"Line" if sp else "Desc"},,0,0,0,,'
                      + clean(f'{sp}:  {tx}' if sp else tx))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(head + ev) + '\n')


def ass_arg(path):
    q = lambda p: p.replace('\\', '/').replace(':', '\\:')
    return f"ass=filename='{q(path)}':fontsdir='{q('C:/Windows/Fonts')}'"


def captions_for(name, cw, ch, dur, out_dir, caps):
    path = os.path.join(out_dir, '_tmp_captions', name + '.ass')
    write_ass(path, caps, cw, ch, dur)
    return ass_arg(path)


# ---------------------------------------------------------------- whatsapp

def wa_filter(cw, ch, boxes, title, live, t0, dur, ass=''):
    """Filtergraph: pads for the live walls (dict wall -> '0:v' or a label), dark boxes for the rest, the caption bar"""
    parts = [f'color=c={BG}:s={cw}x{ch}:r=24:d={dur:.3f}[bg0]']
    cur = 'bg0'
    for i, (x, y, w, h) in enumerate(boxes):
        if i in live:
            parts.append(f'[{live[i]}]scale={w}:{h}:flags=bicubic,setsar=1[w{i}]')
        else:
            parts.append(f'color=c={UNLIT}:s={w}x{h}:r=24:d={dur:.3f}[w{i}]')
        nxt = f'bg{i + 1}'
        parts.append(f'[{cur}][w{i}]overlay={x}:{y}:shortest=1:eof_action=endall[{nxt}]')
        cur = nxt
    txt = "fontfile='{}':fontcolor=white".format(FONT)
    lab = []
    for i, (x, y, w, h) in enumerate(boxes):
        lab.append(f"drawtext={txt}:fontsize=15:fontcolor=0xbbbbbb:text='{esc(WALL_NAMES[i])}'"
                   f":x={x}+({w}-tw)/2:y={y + h + 8}")
    lab.append(f"drawtext={txt}:fontsize=20:text='{esc(title)}':x={MARGIN}:y=11")
    lab.append(f"drawtext={txt}:fontsize=18:text='%{{pts\\:hms\\:{t0:.3f}}}':x=w-tw-{MARGIN}:y=12")
    if ass:
        lab.append(ass)
    parts.append(f'[{cur}]' + ','.join(lab) + ',format=yuv420p[v]')
    return ';'.join(parts)


def wa_rate(dur):
    """Video maxrate in kbit/s so the file stays under WA_MB (96k audio)."""
    return int(min(3000, WA_MB * 8000 / max(dur, 1) - 110))


def wa_encode(fps, dur, total):
    k = wa_rate(total)
    return ['-r', fps, '-c:v', 'libx264', '-preset', 'slow', '-crf', '23', '-maxrate', f'{k}k',
            '-bufsize', f'{2 * k}k', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '96k', '-ar', '48000',
            '-movflags', '+faststart']


def wa_scene_cmd(src, scene, out, test):
    name, title, folder, files = scene
    paths = [os.path.join(src, folder, f) for f in files]
    info = [ffprobe(p) for p in paths]
    dur = min(i['dur'] for i in info)
    if test:
        dur = min(dur, test)
    cw, ch, boxes = layout([(i['w'], i['h']) for i in info])
    caps = s6_captions() if name == '06_S6_wars' else CAPTIONS[name]
    ass = captions_for(name, cw, ch, dur, os.path.dirname(out), caps)
    fg = wa_filter(cw, ch, boxes, title, {0: '0:v', 1: '1:v', 2: '2:v'}, 0.0, dur, ass)
    fg = fg.replace(':r=24:', f":r={info[1]['rate']}:")
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for p in paths:
        cmd += ['-t', f'{dur:.3f}', '-i', p]
    cmd += ['-filter_complex', fg, '-map', '[v]', '-map', '1:a:0?', '-t', f'{dur:.3f}',
            *wa_encode(info[1]['rate'], dur, dur), out]
    return cmd


def s9_timeline():
    """tools/s9_animatic.py: CLIPS (file, wall, first frame), TOTAL frames, BEATS, LINES, audio()"""
    sys.path.insert(0, TOOLS)
    import s9_animatic
    return s9_animatic


def wa_s9(src, out, test, dry, force):
    """Scene 9 on its real show timeline: one lane per wall (black between its files, the 0.5 s operator fades),
    every file's own sound mixed at its place (s9_animatic.audio)."""
    s9 = s9_timeline()
    folder = os.path.join(src, FALLBACK)
    n1 = min(s9.TOTAL, int(round(test * s9.FPS))) if test else s9.TOTAL
    dur = n1 / s9.FPS
    wall = {'L': 0, 'C': 1, 'R': 2}
    clips = [(os.path.join(folder, f), wall[w], start) for f, w, start in s9.CLIPS]
    info = [ffprobe(p) for p, _, _ in clips]
    size = {}
    for (_, w, _), i in zip(clips, info):
        size.setdefault(w, (i['w'], i['h']))
    cw, ch, boxes = layout([size[0], size[1], size[2]])
    tmpdir = os.path.join(os.path.dirname(out), '_tmp_captions')
    ass = captions_for(S9_NAME, cw, ch, dur, os.path.dirname(out), moments_and_lines(s9.BEATS, s9.LINES))
    parts = []
    for li in range(3):
        _, _, w, h = boxes[li]
        pix = f'setsar=1,format=yuv420p'
        segs, pos = [], 0
        mine = sorted((start, k) for k, (_, wl, start) in enumerate(clips) if wl == li)
        for j, (start, k) in enumerate(mine):
            n = int(round(info[k]['dur'] * s9.FPS))
            if j + 1 < len(mine):
                n = min(n, mine[j + 1][0] - start)
            if start > pos:
                parts.append(f'color=c=black:s={w}x{h}:r={s9.FPS},trim=end_frame={start - pos},{pix}[g{li}_{j}]')
                segs.append(f'[g{li}_{j}]')
            f = s9.FADE
            parts.append(f'[{k}:v]fps={s9.FPS},trim=end_frame={n},scale={w}:{h}:flags=bicubic,{pix},'
                         f'fade=t=in:s=0:n={f},fade=t=out:s={n - f}:n={f}[c{li}_{j}]')
            segs.append(f'[c{li}_{j}]')
            pos = start + n
        if s9.TOTAL > pos:
            parts.append(f'color=c=black:s={w}x{h}:r={s9.FPS},trim=end_frame={s9.TOTAL - pos},{pix}[g{li}_end]')
            segs.append(f'[g{li}_end]')
        parts.append(''.join(segs) + f'concat=n={len(segs)}:v=1:a=0[lane{li}]')
    fg = ';'.join(parts) + ';' + wa_filter(cw, ch, boxes, S9_TITLE, {0: 'lane0', 1: 'lane1', 2: 'lane2'}, 0.0, dur, ass)
    wav = os.path.join(tmpdir, S9_NAME + '_sound.wav')
    cmd = ['ffmpeg', '-v', 'error', '-y']
    for p, _, _ in clips:
        cmd += ['-i', p]
    cmd += ['-i', wav, '-filter_complex', fg, '-map', '[v]', '-map', f'{len(clips)}:a:0', '-t', f'{dur:.3f}',
            *wa_encode(str(s9.FPS), dur, dur), out]
    if os.path.exists(out) and not force:
        print(f'skip (exists)  {out}', flush=True)
        return
    if not dry:
        s9.audio(wav, 0, n1)
    run(cmd, out, dry, True)


def wa_s7(out, test, dry, force):
    """Scene 7, Homie's ship (work in progress): the intro v8, then the light-arc preview, cut into its three walls."""
    paths = [os.path.join(S7_DIR, f) for f in S7_FILES]
    info = [ffprobe(p) for p in paths]
    dur = info[0]['dur'] + info[1]['dur']
    if test:
        dur = min(dur, test)
    cw, ch, boxes = layout([(1440, 1080), (1800, 1080), (1440, 1080)])
    ass = captions_for(S7_NAME, cw, ch, dur, os.path.dirname(out), s7_captions(info[0]['dur']))
    au = 'aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo'
    parts = [f'[{k}:v]fps=24,scale=2340:540:flags=bicubic,setsar=1,format=yuv420p[s{k}];[{k}:a]{au}[a{k}]'
             for k in range(2)]
    parts.append('[s0][a0][s1][a1]concat=n=2:v=1:a=1[cv][ca]')
    parts.append('[cv]split=3[x0][x1][x2];[x0]crop=720:540:0:0[l0];[x1]crop=900:540:720:0[l1];'
                 '[x2]crop=720:540:1620:0[l2]')
    fg = ';'.join(parts) + ';' + wa_filter(cw, ch, boxes, S7_TITLE, {0: 'l0', 1: 'l1', 2: 'l2'}, 0.0, dur, ass)
    cmd = ['ffmpeg', '-v', 'error', '-y', '-i', paths[0], '-i', paths[1], '-filter_complex', fg,
           '-map', '[v]', '-map', '[ca]', '-t', f'{dur:.3f}', *wa_encode('24', dur, dur), out]
    run(cmd, out, dry, force)


# ---------------------------------------------------------------- check

def check(src, darrin_out, wa_out, jobs):
    bad = 0
    rows = []
    if 'darrin' in jobs:
        for inp, out in darrin_jobs(src, darrin_out):
            rows.append((inp, out, None))
    if 'whatsapp' in jobs:
        for name, _, folder, files in SCENES:
            rows.append((os.path.join(src, folder, files[1]), os.path.join(wa_out, name + '.mp4'), None))
        s7 = sum(ffprobe(os.path.join(S7_DIR, f))['dur'] for f in S7_FILES)
        rows.append((None, os.path.join(wa_out, S7_NAME + '.mp4'), s7))
        s9 = s9_timeline()
        rows.append((None, os.path.join(wa_out, S9_NAME + '.mp4'), s9.TOTAL / s9.FPS))
    for inp, out, want in rows:
        if not os.path.exists(out):
            print(f'MISSING  {out}')
            bad += 1
            continue
        o = ffprobe(out)
        if inp:
            i = ffprobe(inp)
            want = i['dur']
            ok = abs(o['dur'] - want) < 0.15 and abs(o['fps'] - i['fps']) < 0.01 and o['audio'] == i['audio']
        else:
            ok = abs(o['dur'] - want) < 0.5 and o['audio']
        mb = os.path.getsize(out) / 1e6
        print(f"{'ok ' if ok else 'BAD'}  {o['w']}x{o['h']}  {o['dur']:8.2f}s (src {want:8.2f})  {o['fps']:.3f}fps  "
              f"{'sound' if o['audio'] else 'NO SOUND'}  {mb:7.1f} MB  {out}")
        bad += not ok
    print(f'check: {len(rows)} files, {bad} problems')
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--job', required=True, choices=['darrin', 'whatsapp', 'both'])
    ap.add_argument('--src', default=SRC)
    ap.add_argument('--darrin-out', default=DARRIN_OUT)
    ap.add_argument('--wa-out', default=WA_OUT)
    ap.add_argument('--test', type=float, default=0, help='encode only the first N seconds of each file')
    ap.add_argument('--only', default='', help='only outputs whose path contains this')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--dry', action='store_true')
    a = ap.parse_args()
    jobs = ['darrin', 'whatsapp'] if a.job == 'both' else [a.job]
    if a.check:
        sys.exit(1 if check(a.src, a.darrin_out, a.wa_out, jobs) else 0)
    if 'darrin' in jobs:
        if not a.dry:
            os.makedirs(a.darrin_out, exist_ok=True)
            import datetime
            with open(os.path.join(a.darrin_out, '00_READ_ME_DARRIN.txt'), 'w', encoding='utf-8', newline='\r\n') as fh:
                fh.write(README.format(date=datetime.date.today().strftime('%d %B %Y').lstrip('0')))
        for inp, out in darrin_jobs(a.src, a.darrin_out):
            if a.only in out:
                run(darrin_cmd(inp, out, a.test), out, a.dry, a.force)
    if 'whatsapp' in jobs:
        for scene in SCENES:
            out = os.path.join(a.wa_out, scene[0] + '.mp4')
            if a.only in out:
                run(wa_scene_cmd(a.src, scene, out, a.test), out, a.dry, a.force)
        out = os.path.join(a.wa_out, S7_NAME + '.mp4')
        if a.only in out:
            wa_s7(out, a.test, a.dry, a.force)
        out = os.path.join(a.wa_out, S9_NAME + '.mp4')
        if a.only in out:
            wa_s9(a.src, out, a.test, a.dry, a.force)
    print('done' + (' (dry run: nothing written)' if a.dry else ''))


if __name__ == '__main__':
    main()
