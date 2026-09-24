"""Rebuild a show file's soundtrack from the generated clips' own audio, cut exactly like the picture.

Built 2026-09-25 (Claude). WHY: every Higgsfield clip comes back with audio (Homie leaves it on as a
scratch reference for the sound designer), but the picture tools read frames only, so every show
file was silent. Homie: "embed it within the file, don't get rid of any of the audio".

HOW EACH PIECE IS CUT (24 fps, 48 kHz, 2,000 samples per frame):
- A LOOP CYCLE is built like loop_halo.py builds the picture (--skip 12 --xfade 36): source frames
  48-240, the last 36 frames mixed linearly into source frames 12-47, so cycles join seamlessly.
- The reveal and the snuff play whole (their audio runs ~70 ms short of the picture; the gap is
  filled with the clip's own tail, mirrored).
- A HOLD (a frozen frame: the salon's dusk after the snuff, the judge's raised pose) gets the
  clip's own ambience, crossfade-looped, so nothing buzzes and nothing is invented.
- The court follows render_court.py's own timeline: wherever the picture plays the strike clip
  forward, the strike's audio plays with it (the knock lands with the blow); holds and black get
  the strike clip's room tone from before the blow.
Every splice gets a 10 ms crossfade (no clicks).

  python tools/build_audio.py RECIPE OUT.wav          (recipes: see RECIPES below)
  python tools/build_audio.py RECIPE --mux SHOW.mov OUT.mov

--mux copies the picture stream untouched (-c:v copy, bit-identical) and adds the sound as 24-bit
PCM. It refuses to overwrite. Needs ffmpeg and numpy.
"""
import argparse
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(__file__)
CLIPS = os.path.join(HERE, '..', '..', 'SOTR_MEDIA', '02_APPROVED_BUILDING_BLOCKS', 'clips')
SR, FPS = 48000, 24
SPF = SR // FPS
SPLICE = int(0.010 * SR)


def load(name):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(CLIPS, name), '-vn', '-ac', '2', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def span(a, f0, f1):
    """Audio for source frames [f0, f1), padded with the clip's own tail mirrored if it runs short."""
    s0, s1 = f0 * SPF, f1 * SPF
    out = a[s0:s1]
    short = (s1 - s0) - len(out)
    if short > 0:
        tail = a[-short:][::-1] if short <= len(a) else np.zeros((short, 2), np.float32)
        out = np.concatenate([out, tail])
    return out


def cycle(a, skip=12, x=36, frames=193):
    body = span(a, skip + x, skip + x + frames)
    head = span(a, skip, skip + x)
    n = x * SPF
    w = np.repeat((np.arange(x) + 1) / (x + 1), SPF)[:, None].astype(np.float32)
    body[-n:] = body[-n:] * (1 - w) + head * w
    return body


def ambience(src, nframes, xf=0.4):
    """Crossfade-loop a piece of room tone to any length."""
    k = int(xf * SR)
    need = nframes * SPF
    if len(src) <= 2 * k:
        return np.resize(src, (need, 2))
    unit = src.copy()
    out = unit
    ramp = np.linspace(0, 1, k, dtype=np.float32)[:, None]
    while len(out) < need:
        out = np.concatenate([out[:-k], out[-k:] * (1 - ramp) + unit[:k] * ramp, unit[k:]])
    return out[:need]


def salon(kind, loops=0, hold=0):
    rev, lp, snf = load('loc_SOTR_salon_R_reveal_s9_v1.mp4'), load('loc_SOTR_salon_R_loop_s9_v1.mp4'), \
        load('loc_SOTR_salon_R_snuff_s9_v1.mp4')
    parts = []
    if kind in ('b23', 'IN'):
        parts.append(span(rev, 0, 120))
    parts += [cycle(lp)] * loops
    if kind in ('b23', 'b8', 'OUT'):
        parts.append(span(snf, 0, 120))
    if hold:
        parts.append(ambience(span(snf, 84, 120), hold))  # the snuff's own settled dusk
    return parts


def studio(loops):
    return [cycle(load('loc_SOTR_studio_L_loop_s9_v1.mp4'))] * loops


def court(beat=None, strike=None):
    sys.path.insert(0, HERE)
    import render_court
    seq = [s[0] for s in render_court.timeline(beat, strike)]  # source frame per output frame, None = black
    a = load('fig_SOTR_judge_strike_s9_v1.mp4')
    tone = span(a, 0, 39)  # the room before the blow
    n = len(seq)

    def playing(i):  # the picture plays the clip forward here
        s = seq[i]
        return s is not None and ((i > 0 and seq[i - 1] == s - 1) or (i + 1 < n and seq[i + 1] == s + 1))

    parts, i = [], 0
    while i < n:
        j = i + 1
        if playing(i):
            while j < n and playing(j) and seq[j] == seq[j - 1] + 1:
                j += 1
            parts.append(span(a, seq[i], seq[i] + (j - i)))
        else:
            while j < n and not playing(j):
                j += 1
            parts.append(ambience(tone, j - i))
        i = j
    return parts


RECIPES = {
    'salon_b2-3': lambda: salon('b23', loops=9, hold=840),
    'salon_b8': lambda: salon('b8', loops=1, hold=72),
    'salon_IN': lambda: salon('IN'),
    'salon_HOLD': lambda: salon('HOLD', loops=1),
    'salon_OUT': lambda: salon('OUT'),
    'studio_b4': lambda: studio(9),
    'studio_b6': lambda: studio(4),
    'studio_b9': lambda: studio(5),
    'court_b3': lambda: court(beat=3),
    'court_b5': lambda: court(beat=5),
    'court_b7': lambda: court(beat=7),
    'court_Q1': lambda: court(strike='Q1'),
    'court_Q2': lambda: court(strike='Q2'),
    'court_Q3': lambda: court(strike='Q3'),
    'court_Q4': lambda: court(strike='Q4'),
}


def splice(parts):
    out = np.concatenate(parts).copy()
    pos = 0
    h = SPLICE // 2
    for p in parts[:-1]:
        pos += len(p)
        if h < pos < len(out) - h:
            ramp = np.linspace(0, 1, 2 * h, dtype=np.float32)[:, None]
            left, right = out[pos - h:pos].copy(), out[pos:pos + h].copy()
            # crossfade the outgoing tail into the incoming head over 10 ms
            out[pos - h:pos + h] = (np.concatenate([left, left[::-1]]) * (1 - ramp) +
                                    np.concatenate([right[::-1], right]) * ramp)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('recipe', choices=sorted(RECIPES))
    ap.add_argument('out')
    ap.add_argument('--mux', help='the silent show file to add this soundtrack to (picture copied untouched)')
    a = ap.parse_args()
    if os.path.exists(a.out):
        raise SystemExit(f'refusing: {a.out} exists')
    audio = np.clip(splice(RECIPES[a.recipe]()), -1, 1)
    frames = len(audio) // SPF
    if a.mux:
        n = int(subprocess.check_output(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0',
                                         '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', a.mux]).strip())
        if n != frames:
            raise SystemExit(f'length mismatch: picture {n} frames, sound {frames} frames ({a.recipe})')
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', a.mux, '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                              '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'pcm_s24le', a.out],
                             stdin=subprocess.PIPE)
    else:
        p = subprocess.Popen(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-',
                              '-c:a', 'pcm_s24le', a.out], stdin=subprocess.PIPE)
    p.stdin.write(audio.astype('<f4').tobytes())
    p.stdin.close()
    p.wait()
    print(f'{a.recipe}: {frames} frames ({frames / FPS:.2f} s) -> {a.out}')


if __name__ == '__main__':
    main()
