"""Scene 5 (the battlefield, Homie's Unreal renders): the grade for the client's note "too red" (Meeting 4, 2026-10-03).

WHY: the red is the GROUND, not the light: the soil is a vivid outback red (hue ~5-20 deg, mid brightness) under an
already grey sky. So the grade moves only the soil's reds toward the brown/ochre mud of a European battlefield, and
protects what must stay orange: the fires and embers (brighter and more yellow than the soil). Grass and sky untouched.
Each option is a 3D LUT (.cube), so the stills Homie judges and the videos (and the cannonball overlays, alpha kept)
are graded by the SAME file through ffmpeg's lut3d.

  python tools/grade_battlefield.py luts OUTDIR                    (writes S5_grade_<A|B|C>.cube)
  python tools/grade_battlefield.py stills OUTDIR FRAME.png ...   (one comparison sheet per option + all-in-one)

Options (docs/PLAN-MEETING4.md task 3):
  A  amber dusk   the soil to a warm umber, the whole picture a little dimmer and more amber (closest to Scene 6's
                  opening smoke, so the join holds)
  B  midway       the soil to a natural brown earth; nothing else changes
  C  grey smoke   the soil to grey-brown mud, the whole picture cooler and greyer (fires kept)
"""
import os
import subprocess
import sys

import numpy as np

N = 33
OPTIONS = {
    #     soil hue -> deg, soil sat x, soil val x, global mult (r, g, b), global sat x
    'A': dict(hue=20.0, sat=0.68, val=0.80, mult=(1.00, 0.93, 0.82), gsat=0.95, name='amber dusk'),
    'B': dict(hue=24.0, sat=0.58, val=0.78, mult=(1.00, 1.00, 1.00), gsat=1.00, name='midway, brown earth'),
    'C': dict(hue=27.0, sat=0.42, val=0.74, mult=(0.95, 0.97, 1.02), gsat=0.80, name='grey smoke'),
}


def ss(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def rgb2hsv(c):
    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    mx, mn = c.max(-1), c.min(-1)
    d = mx - mn + 1e-9
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    s = np.where(mx > 0, (mx - mn) / (mx + 1e-9), 0)
    return h, s, mx


def hsv2rgb(h, s, v):
    h = (h % 360) / 60
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, t = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    out = np.choose(i[..., None], [np.stack(x, -1) for x in ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))])
    return out


def grade(c, o):
    """c: (..., 3) RGB 0..1 -> graded."""
    h, s, v = rgb2hsv(c)
    dh = np.abs(((h - 12 + 180) % 360) - 180)                    # distance from the soil's red, degrees
    soil = (1 - ss(16, 34, dh)) * ss(0.18, 0.35, s)              # red and saturated enough to be the earth
    fire = ss(0.72, 0.92, v) * ss(0.35, 0.6, s)                  # bright and saturated: flames, embers, their glow
    w = soil * (1 - fire)
    h2 = h + (o['hue'] - 12) * w                                  # rotate toward brown, keeping each pixel's offset
    s2 = s * (1 + (o['sat'] - 1) * w)
    v2 = v * (1 + (o['val'] - 1) * w)
    g = hsv2rgb(h2, np.clip(s2, 0, 1), np.clip(v2, 0, 1))
    lum = (g @ np.array([0.2126, 0.7152, 0.0722]))[..., None]
    keep = fire[..., None]                                        # the global look leaves the fire alone
    gg = (lum + (g - lum) * o['gsat']) * np.array(o['mult'])
    return np.clip(g * keep + gg * (1 - keep), 0, 1)


def write_cube(path, o):
    x = np.linspace(0, 1, N)
    b, g, r = np.meshgrid(x, x, x, indexing='ij')                 # .cube order: red changes fastest
    c = np.stack([r, g, b], -1).reshape(-1, 3)
    out = grade(c, o)
    with open(path, 'w') as f:
        f.write(f'TITLE "SOTR S5 grade {o["name"]}"\nLUT_3D_SIZE {N}\n')
        for row in out:
            f.write(f'{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n')


def main():
    cmd, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for k, o in OPTIONS.items():
        write_cube(os.path.join(outdir, f'S5_grade_{k}.cube'), o)
    if cmd == 'luts':
        return
    frames = sys.argv[3:]
    font = 'didot.ttf'
    here = os.getcwd()
    os.chdir(outdir)
    if not os.path.exists(font):
        import shutil
        shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'GFSDidot-Regular.ttf'), font)
    labels = {'0': 'AS NOW'} | {k: f'{k}  -  {o["name"]}' for k, o in OPTIONS.items()}
    rows = []
    for k in labels:
        ins, chain = [], []
        for i, fr in enumerate(frames):
            ins += ['-i', os.path.join(here, fr) if not os.path.isabs(fr) else fr]
            lut = '' if k == '0' else f'lut3d=file=S5_grade_{k}.cube:interp=tetrahedral,'
            chain.append(f'[{i}]{lut}scale=720:-2[f{i}]')
        txt = labels[k].replace(':', '\\:')
        chain.append(''.join(f'[f{i}]' for i in range(len(frames))) + f'hstack=inputs={len(frames)},'
                     f"drawtext=fontfile={font}:text='{txt}':fontcolor=white:fontsize=34:x=16:y=14:box=1:boxcolor=black@0.6:boxborderw=8[o]")
        row = f'_row_{k}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', ';'.join(chain), '-map', '[o]', '-frames:v', '1', row], check=True)
        rows.append(row)
    for k, row in zip(labels, rows):
        if k != '0':
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', rows[0], '-i', row, '-filter_complex', 'vstack', '-q:v', '2',
                            f'S5_grade_option_{k}.jpg'], check=True)
    ins = sum([['-i', r] for r in rows], [])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', f'vstack=inputs={len(rows)}', '-q:v', '2',
                    'S5_grade_ALL_OPTIONS.jpg'], check=True)
    for r in rows:
        os.remove(r)
    print('wrote', outdir)


if __name__ == '__main__':
    main()
