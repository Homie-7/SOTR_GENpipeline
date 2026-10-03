"""Scene 9 animatic: the eight approved show files on the three walls, in script order, with the script's lines.

WHY (Homie, 2026-10-03): "Can we also make an animatic like the S6 for the S9 as well." Scene 6 has one (all three walls
side by side + a caption strip); Scene 9 only existed as eight separate files, so nobody could watch the scene whole.
This lays the approved files (the 1080 set, with the edge, exactly as they play) on one 4680x1080 canvas at half size
(LEFT 1440 | CENTRE 1800 | RIGHT 1440, the S6 layout), with a caption strip under it.

TIMELINE (from the files themselves, not invented):
  salon b2-3 starts at 0; its snuff falls at ~77.5 s, where the court's beat 3 begins (D3: the candles go out on the
  first gavel), so court b3 = the salon file's last 40 s (both end together). Then every beat follows the one before:
  studio b4, court b5, studio b6, court b7, salon b8, studio b9. Total 9,580 frames (6:39).
  A wall is black when its world isn't on. Beats 1 and 10 (the raft) are a physical riser, not projected.
  The operator's fades at each file's start and end are shown as 0.5 s fades (the files themselves start and end at full
  picture).
CAPTIONS: Scene 9 of the workshop draft V1 (pp. 18-21), word for word. Court lines are pinned to the strikes in
  render_court.py (b3 strike +1.0 s; b5 +0.5 / +45 / +85 s; b7 +0.5 s, capper +16 s); every other line is spread over
  its beat by word count, as D1 estimated the beat lengths. The actors' timing is live; these are proposed.
SOUND: each file's own scratch sound at its place on the timeline (the salon's dusk and the court overlap in beat 3).

  python tools/s9_animatic.py OUT.mp4 [--scale 0.5] [--start S --end S] [--stills DIR --at 10,80,...]
"""
import argparse
import os
import subprocess
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

FPS = 24
SRC = r'D:\SOTR\SOTR_MEDIA\01_FINAL_FOR_SHOW\3_HD_1080_fallback\1_PLAY_THESE_IN_ORDER'
FONTS = os.path.join(os.path.dirname(__file__), 'fonts')
WALLS = {'L': (0, 1440), 'C': (1440, 3240), 'R': (3240, 4680)}
FADE = 12                                   # frames: the operator's fade, shown at each file's start and end

# (file, wall, first frame on the timeline); frame counts are read from the files
CLIPS = [('S9_b2-3_RIGHT_salon.mov', 'R', 0)]
_b3 = 2817 - 960                            # the court's beat 3 = the salon file's last 40 s (starts on the snuff)
CLIPS += [('S9_b3_CENTRE_court.mov', 'C', _b3)]
_t = 2817
for f, w, n in [('S9_b4_LEFT_studio.mov', 'L', 1737), ('S9_b5_CENTRE_court.mov', 'C', 2424),
                ('S9_b6_LEFT_studio.mov', 'L', 772), ('S9_b7_CENTRE_court.mov', 'C', 480),
                ('S9_b8_RIGHT_salon.mov', 'R', 385), ('S9_b9_LEFT_studio.mov', 'L', 965)]:
    CLIPS.append((f, w, _t))
    _t += n
TOTAL = _t                                  # 9580
S = {c[0]: c[2] / FPS for c in CLIPS}       # each file's start, seconds

BEATS = [(0, 'Beat 2 · SALON · the letter'),
         (S['S9_b3_CENTRE_court.mov'], 'Beat 3 · COURT · finding One!  (the salon snuffs and holds in dusk)'),
         (S['S9_b4_LEFT_studio.mov'], 'Beat 4 · STUDIO · "I must have the likeness"'),
         (S['S9_b5_CENTRE_court.mov'], 'Beat 5 · COURT · findings Two! and Three!'),
         (S['S9_b6_LEFT_studio.mov'], 'Beat 6 · STUDIO · "I will show it all!"'),
         (S['S9_b7_CENTRE_court.mov'], 'Beat 7 · COURT · the verdict'),
         (S['S9_b8_RIGHT_salon.mov'], 'Beat 8 · SALON · "Mais bien sûr"'),
         (S['S9_b9_LEFT_studio.mov'], 'Beat 9 · STUDIO · "made visible for all to see"')]

ML, GE, JU, SA = 'MARIE-LOUISE', 'GÉRICAULT', 'JUDGE', 'SARAH'
# segments: (start s, end s, [(speaker, text, fixed seconds or None)]); lines are spread by word count inside a segment
b3, b4, b5, b6, b7, b8, b9 = (S[c[0]] for c in CLIPS[1:])
SEGMENTS = [
    (0.5, 76.5, [
        ('', '(An ornate Louis XIV salon is slowly revealed. A Baroque minuet: harpsichord and strings.)', 6),
        (ML, "Alors, Mademoiselle, did you 'ear about the ship « La Méduse » ? Non ? ...", None),
        (ML, 'So, Corréard recounted the incident in his most recent letter. (Pulls out the letter) I have the letter '
             'here. Come closer, I will read it for you...', None),
        (ML, "'No person can hear this interesting narrative without being deeply affected by the perils and "
             "misfortunes to which the small remnant of persons, who were saved from this deplorable shipwreck was "
             "exposed.'", None),
        (ML, "Écoutez ... 'Of one hundred and fifty persons embarked upon the raft, and left to their fate, only "
             "fifteen remained alive thirteen days afterward;", None),
        (ML, "but of these fifteen, so miraculously saved, life constituted the sole possession, being literally "
             "stripped of everything.'", None),
        (ML, '(Laughs, folds up the letter) Good riddance to the riff-raff. (Strokes her neck)', None),
        (ML, 'The spirit of the revolution is still alive and must be extinguished. We have seen too much violence and '
             'these traitors to the king should all be sent to Africa.', None)]),
    (b3, b3 + 1.0, [('', "(Men's voices mumbling in a courtroom. A voice: 'Order! Order!')", 1)]),
    (b3 + 1.0, b3 + 3.0, [('', '(The gavel. SARAH jumps. He receives a scroll.)', 2)]),
    (b3 + 3.0, b3 + 39.0, [
        (JU, 'In the matter of the criminal indictment of CAPITAINE Hugues Duroy de Chaumareys, previously captain of '
             'the frigate « La Méduse », my findings of fact are:', None),
        (JU, 'One! The Accused exercised appropriate leadership and evacuated the passengers and crew in a controlled '
             'and timely manner from the sinking ship', None),
        (JU, 'to a makeshift raft, in the absence of a sufficient number of lifeboats.', None)]),
    (b4 + 0.5, b4 + 71.5, [
        ('', '(GÉRICAULT paints. SARAH slowly approaches; she recognises the raft painting.)', 5),
        (GE, 'Two survivors from this situation, Messieurs Savigny et Corréard, told me how some of the men on the raft '
             'were killed.', None),
        (GE, 'They said in their book about this terrible voyage that one lost his head. I went to the morgue this '
             'morning and found a head to copy.', None),
        ('', '(He holds up a bloody old hessian bag, takes the head by the hair and shows it to SARAH. She is '
             'repulsed.)', 8),
        (GE, 'You know, I must have the likeness, the detail. My painting must show exactement what happened!', None),
        (GE, '(He pulls the head out of the bag and stares at the face) The sunken eyes. The matted beards. They were '
             'just skeletons when they were saved, tu sais...', None)]),
    (b5 + 0.5, b5 + 45.0, [
        (JU, 'Two! That, the Accused, consistent with Regulation 262(b) of the French Naval Code, made adequate '
             'provision of food and water for the passengers and crew of the raft.', None),
        ('', "(The Public Gallery: 'You're lying!' 'You're protecting the King!' 'Rubbish!' 'Incompetent!')", 9),
        (JU, 'Order! There will be ORDER in the court!', None),
        ('', '(A general hubbub from the Public Gallery.)', 6)]),
    (b5 + 45.0, b5 + 85.0, [
        (JU, 'Three! That the Accused, consistent with Regulation 74 of the said Naval Code, gave orders to a '
             'subordinate to tow the said raft ...', None),
        ('', '(A scuffle in the Public Gallery: yelling and applause.)', 6),
        (JU, 'Order! ORDER! Get them OUT! Get the TRAITORS out of the court! ...', None),
        (JU, "...but that the tow-rope, through 'accidental misadventure', broke and set the raft astray on the high "
             "seas.", None),
        ('', '(The crowd is on the verge of rioting.)', 5)]),
    (b5 + 85.0, b5 + 100.5, [
        (JU, '(Bangs the gavel, completely losing control) Order! Order!', 5),
        (SA, "But that's not what happened... He cut the tow rope!", None)]),
    (b6 + 0.3, b6 + 32.0, [
        (GE, '(Mixing paint) So, Corréard recounted that the next night there was another storm and the soldiers stole '
             'nearly all the wine.', None),
        (GE, 'Do you know how many were murdered this second night?', None),
        (SA, 'No...', 1.5),
        (GE, 'Vingt! Twenty! Quelle honte! Quel scandale!', None),
        (GE, 'I will create a painting that will show all the world this horror story.', None),
        (GE, 'Hunger. Thirst. Madness. Et le cannibalisme aussi. I will show it all!', None)]),
    (b7 + 0.5, b7 + 16.0, [
        (JU, '(Yelling now) I conclude in law that:', 3),
        (JU, 'There was a regrettable loss of life as a result of an Act of God for which the Accused cannot, CAN NOT '
             'be held responsible.', None)]),
    (b7 + 16.0, b7 + 20.0, [('', '(The gavel fills the wall. Black.)', 4)]),
    (b8 + 0.5, b8 + 15.5, [
        (ML, 'Mais bien sûr, dear Chaumareys cannot be punished! The king loves his loyal subjects.', None)]),
    (b9 + 0.3, b9 + 40.0, [
        (GE, 'I will bring down this government and all within it. The corrupt liars!', None),
        (GE, "The injustice will be made visible for all to see. Ils vont devoir s'expliquer un jour.", None),
        ('', '(GÉRICAULT and SARAH step back and look at the painting.)', 4),
        (GE, "Où est la liberté ? Où est l'égalité ? Où est la fraternité ? Où est l'hu-m-ani-té ?", None),
        (GE, "Ohh j'ai la rage, LA RAGE contre ce gouvernement !", None)]),
]


def timed_lines():
    """[(t, speaker, text)]: inside each segment, a line's share of the time follows its word count"""
    out = []
    for t0, t1, items in SEGMENTS:
        rate = lambda sp: 2.0 if sp == JU else 2.3          # D1: words per second (the Judge declaims)
        w = [fx if fx is not None else len(tx.split()) / rate(sp) + 0.6 for sp, tx, fx in items]
        k = (t1 - t0) / sum(w)
        t = t0
        for (sp, tx, _), wi in zip(items, w):
            out.append((t, sp, tx))
            t += wi * k
    return out


LINES = timed_lines()


class Clip:
    """one show file, read sequentially through ffmpeg, already scaled to its wall's size on the canvas"""

    def __init__(self, name, wall, start, scale):
        self.path, self.wall, self.start = os.path.join(SRC, name), wall, start
        x0, x1 = WALLS[wall]
        self.w, self.h = int(round((x1 - x0) * scale)) // 2 * 2, int(round(1080 * scale)) // 2 * 2
        self.n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                              'stream=nb_frames', '-of', 'csv=p=0', self.path]).strip())
        self.p, self.i = None, 0

    def frame(self, f):
        """the picture at timeline frame f, or None if this file isn't on"""
        j = f - self.start
        if j < 0 or j >= self.n:
            if self.p and j >= self.n:
                self.p.kill(); self.p = None
            return None
        if self.p is None:
            self.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{j / FPS:.4f}', '-i', self.path, '-vf',
                                       f'scale={self.w}:{self.h}:flags=area', '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'],
                                      stdout=subprocess.PIPE)
            self.i = j
        buf = self.p.stdout.read(self.w * self.h * 3)
        self.i += 1
        img = np.frombuffer(buf, np.uint8).reshape(self.h, self.w, 3)
        g = min(1.0, (j + 1) / FADE, (self.n - j) / FADE)       # the operator's fade in / out
        return img if g >= 1 else (img * g).astype(np.uint8)


class Strip:
    def __init__(self, W, H):
        self.W, self.sh = W, max(80, int(H * 0.22)) // 2 * 2
        self.f = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(12, int(self.sh * 0.19)))
        self.fs = ImageFont.truetype(os.path.join(FONTS, 'GFSDidot-Regular.ttf'), max(10, int(self.sh * 0.13)))
        self.cache = {}

    def wrap(self, d, text, width):
        out, line = [], ''
        for word in text.split():
            trial = (line + ' ' + word).strip()
            if d.textlength(trial, font=self.f) > width and line:
                out.append(line); line = word
            else:
                line = trial
        return out + [line]

    def render(self, t, scale):
        beat = [b for b in BEATS if b[0] <= t][-1][1]
        cur = [ln for ln in LINES if ln[0] <= t]
        cur = cur[-1] if cur else (0, '', '')
        stamp = f'{int(t // 60)}:{t % 60:04.1f}'
        key = (stamp, beat, cur)
        if key in self.cache:
            return self.cache[key]
        img = Image.new('RGB', (self.W, self.sh), (18, 18, 20))
        d = ImageDraw.Draw(img)
        for wall, (x0, x1) in WALLS.items():                 # row 0: which wall is which, under each wall
            lab = {'L': 'LEFT', 'C': 'CENTRE', 'R': 'RIGHT'}[wall]
            d.text(((x0 + x1) / 2 * scale - d.textlength(lab, font=self.fs) / 2, self.sh * 0.03), lab,
                   font=self.fs, fill=(90, 90, 90))
        d.text((10, self.sh * 0.22), f'{stamp}   {beat}', font=self.fs, fill=(150, 150, 150))   # row 1
        sp, tx = cur[1], cur[2]
        lines = self.wrap(d, (sp + ':  ' if sp else '') + tx, self.W - 20)[:2]
        for k, ln in enumerate(lines):
            d.text((10, self.sh * (0.44 + 0.26 * k)), ln, font=self.f,
                   fill=(230, 225, 210) if sp else (160, 160, 150))
        arr = np.asarray(img)
        self.cache = {key: arr}
        return arr


def canvas(clips, f, scale):
    W, H = int(round(4680 * scale)) // 2 * 2, int(round(1080 * scale)) // 2 * 2
    out = np.zeros((H, W, 3), np.uint8)
    for c in clips:
        img = c.frame(f)
        if img is not None:
            x = int(round(WALLS[c.wall][0] * scale))
            out[:, x:x + img.shape[1]] = img[:, :W - x]
    for xs in (1440, 3240):                                  # the seams, as in the S6 animatic
        x = int(round(xs * scale))
        out[:, max(0, x - 1):x + 1] = (70, 70, 70)
    return out


def audio(path_wav, n0, n1):
    """every file's own sound at its place on the timeline, summed (no normalising), cut to the rendered range"""
    ins, flt = [], []
    for k, (name, _, start) in enumerate(CLIPS):
        ins += ['-i', os.path.join(SRC, name)]
        ms = int(round(start / FPS * 1000))
        flt.append(f'[{k}:a]aresample=48000,adelay={ms}|{ms}[a{k}]')
    mix = ''.join(f'[a{k}]' for k in range(len(CLIPS)))
    flt.append(f'{mix}amix=inputs={len(CLIPS)}:normalize=0:duration=longest,'
               f'atrim={n0 / FPS:.4f}:{n1 / FPS:.4f},asetpts=PTS-STARTPTS[out]')
    subprocess.check_call(['ffmpeg', '-y', '-v', 'error'] + ins + ['-filter_complex', ';'.join(flt), '-map', '[out]',
                                                                   '-c:a', 'pcm_s16le', path_wav])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--scale', type=float, default=0.5)
    ap.add_argument('--start', type=float, default=0.0)
    ap.add_argument('--end', type=float, default=TOTAL / FPS)
    ap.add_argument('--stills')
    ap.add_argument('--at', default='')
    a = ap.parse_args()
    W, H = int(round(4680 * a.scale)) // 2 * 2, int(round(1080 * a.scale)) // 2 * 2
    strip = Strip(W, H)
    if a.stills:
        os.makedirs(a.stills, exist_ok=True)
        for ts in [float(v) for v in a.at.split(',')]:
            f = int(round(ts * FPS))
            clips = [Clip(*c, a.scale) for c in CLIPS]
            fr = np.vstack([canvas(clips, f, a.scale), strip.render(ts, a.scale)])
            Image.fromarray(fr).save(os.path.join(a.stills, f's9_{ts:06.1f}.png'))
            for c in clips:
                if c.p:
                    c.p.kill()
            print('still', ts, flush=True)
        return
    n0, n1 = int(round(a.start * FPS)), min(TOTAL, int(round(a.end * FPS)))
    clips = [Clip(*c, a.scale) for c in CLIPS]
    tmp = tempfile.mkdtemp()
    wav = os.path.join(tmp, 's9_sound.wav')
    audio(wav, n0, n1)
    tmpout = os.path.join(os.path.dirname(os.path.abspath(a.out)), '_tmp_' + os.path.basename(a.out))
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H + strip.sh}',
                          '-r', str(FPS), '-i', '-', '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264',
                          '-crf', '19', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                          '-shortest', '-movflags', '+faststart', tmpout], stdin=subprocess.PIPE)
    for f in range(n0, n1):
        t = f / FPS
        p.stdin.write(np.vstack([canvas(clips, f, a.scale), strip.render(t, a.scale)]).tobytes())
        if f % (FPS * 20) == 0:
            print(f'{t:6.1f} s', flush=True)
    p.stdin.close()
    p.wait()
    os.replace(tmpout, a.out)
    print('wrote', a.out, n1 - n0, 'frames')


if __name__ == '__main__':
    main()
