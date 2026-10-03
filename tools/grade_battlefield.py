"""Scene 5 (the battlefield, Homie's Unreal renders, `SOR Renders/New Renders/Camps/<Angle>/`): the grade for the
client's note "too red" (Meeting 4, 2026-10-03), v2. (v1 graded the old `Camps/Exports` renders, soil only; git history.)

WHY: in these renders BOTH the light and the ground are red: a hot orange sunset with a huge blooming sun, a peach sky,
saturated red soil. The script asks for the opposite (Scene 3, which Scene 5 continues: a battlefield in Napoleonic
France near the north of Italy, "the day is late; it is eerie, smoky, and cold"). A colour-only LUT can't cool the sun
without browning the fires (both are bright orange), but the cameras are LOCKED, so each angle gets one fixed SKY MASK
(found from the picture: the bright, pale region above the horizon, column by column) and two LUTs: one for the sky, one for
the ground; then a FIRE PASS: the fires (the campfire found automatically, the skyline fires placed by eye in SKY_FIRES)
are kept as ADDED LIGHT: the graded picture is warmed in a wide soft pool around each fire as brightly as the fire lit
it in the original, and only the flame cores come back from the original. (A per-pixel fire key in the LUTs speckled
the firelit ground and turned the sun's reflection on the road into lava; keeping the original inside a mask left
stamped orange discs, 2026-10-03.) The first 30 frames (the render warming up) are dropped; the sound rides along.
Every LUT is a .cube, so stills and videos go through the same files with ffmpeg (lut3d + maskedmerge).

  python tools/grade_battlefield.py luts OUTDIR
  python tools/grade_battlefield.py mask FRAME.png OUT/mask_<angle>.png [jagged|soft]   (the sky mask of one angle; soft =
                                                                      the Alps: a per-pixel air map, see make_mask_soft)
  python tools/grade_battlefield.py firemask OUT/fire_<angle>.png <angle> F1.png F2.png ...
  python tools/grade_battlefield.py stills OUTDIR FRAME.png=MASK.png ...  (one sheet: a row per option)
  python tools/grade_battlefield.py match OUTDIR OPTION MASKDIR     (writes S5_match_<OPTION>.json from the fk_<angle>_*.png)
  python tools/grade_battlefield.py render SRC.mov OUT.mov ANGLE OPTION MASKDIR [N] [--despeck]   (in the .cube folder;
                                                                      N = test frames; --despeck = Despeck, the Alps' birds)

MATCH (Homie, 2026-10-03: "all four angles must read as one scene split into four cameras"; Unreal rendered each with
its own exposure and colour): after the grade, each angle's SKY and GROUND (medians over frames spread through the
clip, the sun and the firelight left out) get their own RGB gain toward ONE shared target (the mean of LEFT, FRONT and
RIGHT; the floor, Bottom, takes the ground target), and the sky gets a soft ramp toward each seam so the two walls'
skies meet at the same level where they touch (each side going halfway). One fixed gain field per angle (the cameras
are locked), applied before the fire pass. The geometry (where each horizon sits) is the renders' and is not touched.

Options:
  A  amber dusk      sky: warm, desaturated, the sun calmer; ground: umber   (closest to now and to Scene 6's smoke)
  B  brown earth     sky: near neutral; ground: natural brown earth
  C  cold dusk       sky: pale steel grey, the sun a dim pale disc behind haze; ground: grey-brown mud, darker;
                     the fires are the only warmth (the script: "late… eerie, smoky, and cold")
  S4 the Alps (Scene 4, Homie 2026-10-03: "color match so that everything looks seamless in both the Alps and the
                     camps"): the SAME stock as C, in daylight. Unreal's postcard blue sky and saturated lawn-green
                     are brought into C's family: the sky and the snow pale and steel-cool, the greens muted to olive,
                     the earth grey-brown, highlights eased. It stays day (a flashback home), but the cut into the
                     camps reads as one film. Used with the same sky masks and the same MATCH as the camps.
"""
import os
import shutil
import subprocess
import sys

import cv2
import numpy as np

N = 33
OPTIONS = {
    'A': dict(name='amber dusk',
              g=dict(hue=20.0, sat=0.62, val=0.82, mult=(1.00, 0.94, 0.84), gsat=0.92),
              s=dict(sat=0.60, mult=(1.00, 0.95, 0.88), knee=0.80, comp=0.55, val=0.95)),
    'B': dict(name='brown earth',
              g=dict(hue=24.0, sat=0.52, val=0.78, mult=(1.00, 1.00, 1.00), gsat=0.90),
              s=dict(sat=0.38, mult=(1.00, 0.99, 0.98), knee=0.75, comp=0.45, val=0.92)),
    'S4': dict(name='the Alps, same stock as C', kind='alps',
               g=dict(gsat=0.62, green_sat=0.62, olive=14.0, val=0.90, mult=(0.97, 0.98, 1.00)),
               s=dict(sat=0.42, mult=(0.93, 0.96, 1.03), knee=0.70, comp=0.45, val=0.90)),
    'C': dict(name='cold dusk',
              g=dict(hue=27.0, sat=0.38, val=0.70, mult=(0.93, 0.96, 1.03), gsat=0.72),
              s=dict(sat=0.18, mult=(0.88, 0.93, 1.04), knee=0.62, comp=0.30, val=0.78)),
}
LUMW = np.array([0.2126, 0.7152, 0.0722])


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
    return np.choose(i[..., None], [np.stack(x, -1) for x in ((v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q))])


def fire_key(h, s, v):
    """Flames, embers, the cannonball: bright, saturated, orange-to-yellow (the red soil is redder; the sun's halo is
    paler)."""
    dh = np.abs(((h - 36 + 180) % 360) - 180)
    return ss(0.70, 0.88, v) * ss(0.55, 0.72, s) * (1 - ss(14, 26, dh))


def ground(c, o):
    h, s, v = rgb2hsv(c)
    dh = np.abs(((h - 14 + 180) % 360) - 180)
    soil = (1 - ss(18, 38, dh)) * ss(0.15, 0.32, s)              # the red/orange earth and the light on it
    w = soil
    g = hsv2rgb(h + (o['hue'] - 14) * w, np.clip(s * (1 + (o['sat'] - 1) * w), 0, 1), np.clip(v * (1 + (o['val'] - 1) * w), 0, 1))
    lum = (g @ LUMW)[..., None]
    return np.clip((lum + (g - lum) * o['gsat']) * np.array(o['mult']), 0, 1)


def alps_ground(c, o):
    """Scene 4's meadow: the greens (hue ~60-160) muted and pulled toward olive, everything a little less saturated and
    darker, a touch cooler; the earth and rock keep their hue."""
    h, s, v = rgb2hsv(c)
    dh = np.abs(((h - 105 + 180) % 360) - 180)
    green = (1 - ss(45, 70, dh)) * ss(0.10, 0.25, s)
    g = hsv2rgb(h - o['olive'] * green, np.clip(s * (1 + (o['green_sat'] - 1) * green), 0, 1), np.clip(v * o['val'], 0, 1))
    lum = (g @ LUMW)[..., None]
    return np.clip((lum + (g - lum) * o['gsat']) * np.array(o['mult']), 0, 1)


def sky(c, o):
    lum = (c @ LUMW)[..., None]
    g = (lum + (c - lum) * o['sat']) * np.array(o['mult'])
    gl = (g @ LUMW)[..., None]                                     # the sun: a soft knee on the highlights
    kn, cp = o['knee'], o['comp']
    gl2 = np.where(gl > kn, kn + (gl - kn) * cp, gl)
    g = g * (gl2 / np.maximum(gl, 1e-6)) * o['val']
    return np.clip(g, 0, 1)


def write_cube(path, fn, o, title):
    x = np.linspace(0, 1, N)
    b, g, r = np.meshgrid(x, x, x, indexing='ij')                 # .cube order: red changes fastest
    out = fn(np.stack([r, g, b], -1).reshape(-1, 3), o)
    with open(path, 'w') as f:
        f.write(f'TITLE "{title}"\nLUT_3D_SIZE {N}\n')
        for row in out:
            f.write(f'{row[0]:.6f} {row[1]:.6f} {row[2]:.6f}\n')


def make_luts(outdir):
    os.makedirs(outdir, exist_ok=True)
    for k, o in OPTIONS.items():
        write_cube(os.path.join(outdir, f'S5_{k}_ground.cube'), alps_ground if o.get('kind') == 'alps' else ground, o['g'],
                   f'SOTR S5 {o["name"]} ground')
        write_cube(os.path.join(outdir, f'S5_{k}_sky.cube'), sky, o['s'], f'SOTR S5 {o["name"]} sky')


def make_mask_soft(frame, out):
    """The Alps: the horizon is peaks and a roof, so no column rule works (it striped). A soft per-pixel AIR map: bright
    and pale (sky, cloud, snow) -> 1, the meadow and the dark rock -> 0, closed and feathered so the two LUTs blend
    with no line. Snow takes the sky's treatment, which is the point: the air and the snow are one cold light."""
    im = cv2.imread(frame).astype(np.float32) / 255
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2], hsv[..., 1]
    air = ss(0.50, 0.70, v) * (1 - ss(0.28, 0.45, s))
    air = cv2.morphologyEx(air, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    air = np.clip(cv2.GaussianBlur(air, (0, 0), 6) * 1.3 - 0.15, 0, 1)
    cv2.imwrite(out, (air * 255).astype(np.uint8))
    print(f'soft mask {out}: air {air.mean():.3f}')


def make_mask(frame, out, jagged=False):
    """Sky = the bright, pale region above the horizon (Otsu on brightness minus saturation: the soil is darker and far
    more saturated); each column's horizon is the first row from the top where ground persists; smoothed across columns,
    feathered. No sky -> all black."""
    im = cv2.imread(frame).astype(np.float32) / 255
    H, W = im.shape[:2]
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    feat = cv2.GaussianBlur(hsv[..., 2] - 0.8 * hsv[..., 1], (0, 0), 3)   # the sky: brighter and paler than the ground
    f8 = np.clip(feat * 200 + 100, 0, 255).astype(np.uint8)
    thr, _ = cv2.threshold(f8, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ground_px = (f8 < thr).astype(np.uint8)
    run = cv2.erode(ground_px, np.ones((31, 1), np.uint8), anchor=(0, 0))  # ground that persists 31 rows down
    hz = np.argmax(run > 0, axis=0).astype(np.float32)
    hz[run.max(0) == 0] = H
    ragged = np.std(hz) > 0.12 * H and not jagged                   # no sky: the 'horizon' jumps about (the floor)
    if jagged:                                                      # the Alps: peaks and a roof ARE the horizon
        hz = np.median(np.stack([np.roll(hz, k) for k in range(-6, 7)]), 0)
        hz = cv2.GaussianBlur(hz.reshape(1, -1).astype(np.float32), (0, 0), 2).ravel()
    else:
        hz = np.median(np.stack([np.roll(hz, k) for k in range(-60, 61, 3)]), 0)   # wide: drops narrow dips (a bright road)
        hz = cv2.GaussianBlur(hz.reshape(1, -1).astype(np.float32), (0, 0), 12).ravel()
    yy = np.arange(H, dtype=np.float32)[:, None]
    m = 1 - ss(hz[None, :] - 18, hz[None, :] + 6, yy)
    if ragged or hz.mean() < 0.05 * H:                             # no real sky in this angle (the floor)
        m[:] = 0
    cv2.imwrite(out, (m * 255).astype(np.uint8))
    print(f'mask {out}: horizon rows {hz.min():.0f}-{hz.max():.0f} of {H}')


# the farms burning on each angle's skyline, placed by eye on the locked frames (x, y, radius at 1920x1080): automatic
# detection there also caught the sun's streaks on the road and sunlit grass (2026-10-03)
SKY_FIRES = {
    'front': [(85, 355, 26), (250, 357, 26), (1324, 345, 22), (1378, 347, 22), (1422, 348, 22), (1470, 349, 22), (1520, 349, 22)],
    'left': [(1860, 352, 34)],
    'right': [],
    'bottom': [],
}


def make_fire_mask(frames, out, angle):
    """The fires: the campfire (the one big flame blob, found over several frames spread across the clip; its glow pool
    has an irregular shape) plus the skyline fires of SKY_FIRES, grown into a soft pool so the firelight fades out
    smoothly. Inside it the picture keeps its own colour; everything else is graded. Bright orange elsewhere (the sun's
    reflection on the road) is NOT fire and goes cold with the ground. (A per-pixel key in the LUTs speckled the firelit
    ground and turned the road into lava, 2026-10-03.)"""
    acc = None
    for fr in frames:
        im = cv2.imread(fr).astype(np.float32) / 255
        h, s, v = rgb2hsv(im[..., ::-1])
        k = fire_key(h, s, v)
        acc = k if acc is None else acc + k
    acc /= len(frames)
    H, W = acc.shape
    keep = np.zeros((H, W), np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats((acc > 0.5).astype(np.uint8))
    if n > 1:
        big = 1 + int(np.argmax(st[1:, 4]))
        if st[big, 4] > 1500:                                      # the campfire
            keep[lab == big] = 1
    for x, y, r in SKY_FIRES[angle]:
        cv2.circle(keep, (x, y), r, 1, -1)
    cv2.imwrite(out, keep * 255)
    print(f'fire placement {out}: {int(keep.sum())} px')


FIRE_GAIN = np.array([1.38, 0.92, 0.55], np.float32)             # firelight on the graded picture, RGB gains


class FirePass:
    """Firelight as ADDED LIGHT, not a patch of the old picture (keeping the original inside a mask left stamped orange
    discs, 2026-10-03): inside a wide soft pool around each fire the graded picture is warmed in proportion to how
    brightly the fire lit it in the original; only the flame cores themselves come back from the original."""

    def __init__(self, placement_png):
        src = (cv2.imread(placement_png, 0) > 0).astype(np.uint8)
        if src.sum() > 2000:
            src = cv2.erode(src, np.ones((15, 15), np.uint8))
        self.on = bool(src.sum() > 0)
        f = src.astype(np.float32)
        self.pool = np.clip(cv2.GaussianBlur(f, (0, 0), 40) * 2.2, 0, 1)[..., None]
        self.tight = np.clip(cv2.GaussianBlur(f, (0, 0), 6) * 2.0, 0, 1)

    def __call__(self, orig, graded):
        """orig, graded: float32 RGB 0..1, same size."""
        if not self.on:
            return graded
        lum = orig @ np.array([0.299, 0.587, 0.114], np.float32)
        sat = (orig.max(-1) - orig.min(-1)) / np.maximum(orig.max(-1), 1e-6)
        k = self.pool * ss(0.30, 0.80, lum)[..., None]
        out = graded * (1 + k * (FIRE_GAIN - 1))
        core = (self.tight * ss(0.72, 0.95, lum) * ss(0.35, 0.6, sat))[..., None]
        return np.clip(out * (1 - core) + orig * core, 0, 1)


ANGLES = ('left', 'front', 'right', 'bottom')
SEAMS = (('left', 'front'), ('front', 'right'))                  # (the wall on the left, the wall on the right)
LUM709 = np.array([0.2126, 0.7152, 0.0722], np.float32)
MATCH_EXP, MATCH_WB = 0.8, 0.03                                  # see make_match.gain
RAMP_W = 0.40                                                    # the seam ramp reaches this far into a wall


def _regions(im, m, fire):
    """Sky without the sun (below its 90th percentile) and ground without the firelight, as boolean masks."""
    lum = im @ LUM709
    nofire = (1 - fire.pool[..., 0]) if fire.on else np.ones_like(m)
    sky = None
    if (m > 0.9).sum() > 1000:
        sky = (m > 0.9) & (lum < np.percentile(lum[m > 0.9], 90))
    return sky, (m < 0.1) & (nofire > 0.9)


def gain_field(angle, maskdir, match, shape):
    """The angle's per-pixel RGB gain (H, W, 3): sky gain x the seam ramp where the sky mask is, ground gain elsewhere."""
    a = match[angle]
    m = cv2.imread(os.path.join(maskdir, f'mask_{angle}.png'), 0).astype(np.float32)[..., None] / 255
    H, W = shape
    xs = (np.arange(W, dtype=np.float32) + 0.5) / W
    ramp = np.ones((W, 3), np.float32)
    for side, edge in (('l', a.get('edge_l')), ('r', a.get('edge_r'))):
        if edge is None:
            continue
        d = xs if side == 'l' else 1 - xs                            # 0 at that edge
        w = (1 - ss(0.0, RAMP_W, d))[:, None]
        ramp = ramp * np.exp(w * np.log(np.array(edge, np.float32)))
    sky = np.array(a['sky'], np.float32)[None, None] * ramp[None] if a.get('sky') else 1.0
    return (m * sky + (1 - m) * np.array(a['ground'], np.float32)[None, None]).astype(np.float32)


def make_match(outdir, k, maskdir):
    """Grade the fk_<angle>_*.png samples with option k, measure, write S5_match_<k>.json (see MATCH above)."""
    import glob
    import json
    os.chdir(outdir)
    med, edges = {}, {}
    for ang in ANGLES:
        m = cv2.imread(os.path.join(maskdir, f'mask_{ang}.png'), 0).astype(np.float32) / 255
        fire = FirePass(os.path.join(maskdir, f'fire_{ang}.png'))
        S, Gd, El, Er = [], [], [], []
        for f in sorted(glob.glob(os.path.join(maskdir, f'fk_{ang}_*.png'))):
            tmp = f'_match_{ang}.png'
            graded(f, os.path.join(maskdir, f'mask_{ang}.png'), k, tmp, width=1920)
            im = cv2.imread(tmp)[..., ::-1].astype(np.float32) / 255
            os.remove(tmp)
            sky, gr = _regions(im, m, fire)
            Gd.append(np.median(im[gr], 0))
            if sky is not None:
                S.append(np.median(im[sky], 0))
                W = m.shape[1]
                el, er = sky.copy(), sky.copy()
                el[:, int(0.08 * W):] = False
                er[:, :int(0.92 * W)] = False
                El.append(np.median(im[el], 0))
                Er.append(np.median(im[er], 0))
        med[ang] = dict(sky=np.median(S, 0) if S else None, ground=np.median(Gd, 0))
        edges[ang] = (np.median(El, 0) if El else None, np.median(Er, 0) if Er else None)
    walls = ('left', 'front', 'right')
    t_sky = np.mean([med[a]['sky'] for a in walls], 0)
    t_gr = np.mean([med[a]['ground'] for a in walls], 0)
    def gain(t, m):
        # exposure fully, colour balance gently: the angles can show different CONTENT (the floor is close-up earth,
        # the walls a green meadow), so a full per-channel match would tint one toward the other (the Alps floor went
        # teal, 2026-10-03). Exposure goes MATCH_EXP of the way (in log; a wall facing the sun SHOULD stay a little
        # darker than one lit from the side), clipped 0.8-1.25; the per-channel remainder is clipped to +-MATCH_WB.
        r = (t @ LUM709) / max(float(m @ LUM709), 1e-6)
        L = float(np.clip(r ** MATCH_EXP, 0.8, 1.25))
        ch = (t / np.maximum(m, 1e-6)) / r
        return L * np.clip(ch, 1 - MATCH_WB, 1 + MATCH_WB)
    out = {}
    for ang in ANGLES:
        g_sky = None if med[ang]['sky'] is None else gain(t_sky, med[ang]['sky'])
        out[ang] = dict(sky=None if g_sky is None else g_sky.tolist(),
                        ground=gain(t_gr, med[ang]['ground']).tolist(), edge_l=None, edge_r=None,
                        measured=dict(sky=None if med[ang]['sky'] is None else med[ang]['sky'].tolist(),
                                      ground=med[ang]['ground'].tolist()))
    for a, b in SEAMS:                                               # after the global gains, meet halfway at the seam
        ea = edges[a][1] * np.array(out[a]['sky'])
        eb = edges[b][0] * np.array(out[b]['sky'])
        mid = np.sqrt(ea * eb)
        out[a]['edge_r'] = np.clip(mid / ea, 0.75, 1.33).tolist()
        out[b]['edge_l'] = np.clip(mid / eb, 0.75, 1.33).tolist()
    out['_target'] = dict(sky=t_sky.tolist(), ground=t_gr.tolist(), option=k, ramp_width=RAMP_W)
    with open(f'S5_match_{k}.json', 'w') as f:
        json.dump(out, f, indent=1)
    for ang in ANGLES:
        print(ang, {x: (None if out[ang][x] is None else [round(v, 3) for v in out[ang][x]]) for x in ('sky', 'ground', 'edge_l', 'edge_r')})
    print('wrote', os.path.join(outdir, f'S5_match_{k}.json'))


def load_match(k):
    import json
    p = f'S5_match_{k}.json'
    return json.load(open(p)) if os.path.exists(p) else None


def lut_chain(k, src, mask, fmt):
    """The two LUTs merged by the sky mask, 16-bit throughout."""
    return (f'{src}split[a][b];[a]lut3d=file=S5_{k}_ground.cube:interp=tetrahedral,format=gbrp16le[g];'
            f'[b]lut3d=file=S5_{k}_sky.cube:interp=tetrahedral,format=gbrp16le[s];{mask}format=gray16le,format=gbrp16le[m];'
            f'[g][s][m]maskedmerge,format={fmt}[o]')


def graded(frame, mask, k, out, width=720, match=None):
    """A still through the same chain as the videos: the LUTs merged by the sky mask, (the angle match,) the fire pass."""
    raw = out + '.raw.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', frame, '-i', mask, '-filter_complex', lut_chain(k, '[0]', '[1]', 'rgb48be'),
                    '-map', '[o]', '-frames:v', '1', raw], check=True)
    o = cv2.imread(frame, cv2.IMREAD_UNCHANGED)[..., ::-1].astype(np.float32) / 255
    g = cv2.imread(raw, cv2.IMREAD_UNCHANGED)[..., ::-1].astype(np.float32) / 65535
    os.remove(raw)
    if match is not None:
        ang = os.path.basename(mask)[5:-4]
        g = np.clip(g * gain_field(ang, os.path.dirname(mask), match, g.shape[:2]), 0, 1)
    res = FirePass(mask.replace('mask_', 'fire_'))(o, g)
    hh = int(round(res.shape[0] * width / res.shape[1] / 2)) * 2
    res = cv2.resize(res, (width, hh), interpolation=cv2.INTER_AREA)
    cv2.imwrite(out, (res[..., ::-1] * 255 + 0.5).astype(np.uint8))


def json_probe(src):
    import json
    r = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height,r_frame_rate',
                        '-of', 'json', src], capture_output=True, text=True, check=True)
    return json.loads(r.stdout)['streams'][0]


class Despeck:
    """Scene 4 (Homie 2026-10-03: "get rid of the birds in the Alps"): small, short-lived things in the AIR (a bird, a
    drifting lens orb) are removed; nothing else is touched. The cameras are locked, so for every frame each air pixel
    is compared with its own median over +-1 s (every 2nd frame); a speck = a compact island (3-1500 px) that departs
    from that median by more than ~13/255 after a high-pass (slow clouds and the light changing are broad, so they pass).
    Its pixels (grown 3 px, feathered) are replaced by the median. Logs how many pixels it replaced."""

    def __init__(self, air, K=12, stride=2):
        self.air = air > 0.35
        ys = np.nonzero(self.air.any(1))[0]
        self.y0, self.y1 = (int(ys.min()), int(ys.max()) + 1) if len(ys) else (0, 0)
        self.K, self.st = K, stride
        self.buf, self.base, self.changed = [], 0, 0

    def push(self, g):
        self.buf.append(g)

    def ready(self, i, done):
        return done or len(self.buf) > i - self.base + self.K

    def frame(self, i):
        """The cleaned frame i (all frames up to i+K pushed, or the stream ended)."""
        g = self.buf[i - self.base]
        if self.y1 <= self.y0:
            return g
        n = self.base + len(self.buf)
        idx = [j for j in range(i - self.K, i + self.K + 1, self.st) if self.base <= j < n]
        S = np.stack([self.buf[j - self.base][self.y0:self.y1] for j in idx])
        L = S @ LUM709
        med = np.median(L, 0)
        d = g[self.y0:self.y1] @ LUM709 - med
        hp = d - cv2.GaussianBlur(d, (0, 0), 6)
        cand = ((np.abs(hp) > 0.05) & self.air[self.y0:self.y1]).astype(np.uint8)
        nl, lab, st, _ = cv2.connectedComponentsWithStats(cand, connectivity=8)
        keep = np.isin(lab, [c for c in range(1, nl) if 3 <= st[c, cv2.CC_STAT_AREA] <= 1500])
        out = g
        if keep.any():
            m = cv2.dilate(keep.astype(np.uint8), np.ones((7, 7), np.uint8)).astype(np.float32)
            m = cv2.GaussianBlur(m, (0, 0), 1.5)[..., None]
            ys, xs = np.nonzero(m[..., 0] > 0.01)
            rep = g[self.y0:self.y1].copy()
            rep[ys, xs] = np.median(S[:, ys, xs], 0)
            out = g.copy()
            out[self.y0:self.y1] = g[self.y0:self.y1] * (1 - m) + rep * m
            self.changed += int(keep.sum())
        while len(self.buf) and self.base < i - self.K:                  # drop what no later frame needs
            self.buf.pop(0)
            self.base += 1
        return out


def render(src, out, angle, k, maskdir, trim=30, limit=None, despeck=False):
    """One angle, whole: the first `trim` frames dropped (the render warming up: halftone dots in the sun's bloom,
    unresolved smoke, no campfire, a jump at frame 30), graded (LUTs + sky mask, 16-bit), the fire pass, ProRes 422 HQ
    10-bit at the source's own rate, the source's sound (trimmed the same) in. Written to a _tmp_ name, then renamed.
    Run inside the folder holding the .cube files. Two decoders (graded, original) are read in lockstep."""
    mask, fire = os.path.join(maskdir, f'mask_{angle}.png'), os.path.join(maskdir, f'fire_{angle}.png')
    pr = json_probe(src)
    W, H, fps = pr['width'], pr['height'], pr['r_frame_rate']
    num, den = (int(x) for x in fps.split('/'))
    t0 = f'{trim * den / num:.6f}'
    # exactly the source's frames minus the trim: with no fire pass nothing else bounds the graded stream (the looped mask
    # keeps maskedmerge going), and Right/Bottom ran 12 frames past the end until the encoder's -shortest cut the pipe
    # (2026-10-04)
    total = int(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-count_packets', '-show_entries',
                                'stream=nb_read_packets', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout.strip()) - trim
    if limit:
        total = min(total, limit)
    fp = FirePass(fire)
    match = load_match(k)
    gf = gain_field(angle, maskdir, match, (H, W)) if match else None
    print(f'{angle}: angle match', 'ON' if gf is not None else f'OFF (no S5_match_{k}.json)', flush=True)
    ds = Despeck(cv2.imread(mask, 0).astype(np.float32) / 255) if despeck else None
    tmp = os.path.join(os.path.dirname(out), '_tmp_' + os.path.basename(out))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb48le', '-s', f'{W}x{H}', '-r', fps,
                            '-i', '-', '-ss', t0, '-i', src, '-map', '0:v', '-map', '1:a?', '-c:v', 'prores_ks', '-profile:v', '3',
                            '-qscale:v', '2', '-pix_fmt', 'yuv422p10le', '-vendor', 'apl0', '-c:a', 'pcm_s24le', '-shortest', tmp],
                           stdin=subprocess.PIPE)
    g_cmd = ['ffmpeg', '-v', 'error', '-i', src, '-loop', '1', '-i', mask, '-filter_complex',
             f'[0]trim=start_frame={trim},setpts=PTS-STARTPTS[v];' + lut_chain(k, '[v]', '[1]', 'rgb48le'),
             '-map', '[o]', '-f', 'rawvideo', '-']
    o_cmd = ['ffmpeg', '-v', 'error', '-i', src, '-vf', f'trim=start_frame={trim},setpts=PTS-STARTPTS,format=rgb48le',
             '-f', 'rawvideo', '-']
    if limit:                                                       # a test: only the first `limit` frames
        g_cmd[-3:-3] = ['-frames:v', str(limit)]
        o_cmd[-3:-3] = ['-frames:v', str(limit)]
    gd = subprocess.Popen(g_cmd, stdout=subprocess.PIPE)
    od = subprocess.Popen(o_cmd, stdout=subprocess.PIPE) if fp.on else None
    nb, n = W * H * 6, 0
    got = 0
    while got < total:
        gb = gd.stdout.read(nb)
        if len(gb) < nb:
            break
        g = np.frombuffer(gb, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535
        got += 1
        if gf is not None:
            g = np.clip(g * gf, 0, 1)
        if od is not None:
            ob = od.stdout.read(nb)
            if len(ob) < nb:
                break
            g = fp(np.frombuffer(ob, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535, g)
        if ds is None:
            enc.stdin.write((g * 65535 + 0.5).astype(np.uint16).tobytes())
            n += 1
        else:
            ds.push(g)
            while ds.ready(n, False):
                enc.stdin.write((ds.frame(n) * 65535 + 0.5).astype(np.uint16).tobytes())
                n += 1
        if n % 1500 == 0 and n != getattr(render, '_last', -1):
            render._last = n
            print(f'{angle}: {n} frames', flush=True)
    if ds is not None:                                              # the last K frames
        while n < ds.base + len(ds.buf):
            enc.stdin.write((ds.frame(n) * 65535 + 0.5).astype(np.uint16).tobytes())
            n += 1
        print(f'{angle}: despeck replaced {ds.changed} px in {n} frames ({ds.changed / max(n, 1):.1f} px/frame)', flush=True)
    enc.stdin.close()
    enc.wait()
    for pp in (gd, od):
        if pp is not None:
            pp.kill()
    if enc.returncode != 0:
        raise SystemExit(f'encode failed for {angle}')
    os.replace(tmp, out)
    print(f'{angle}: wrote {out} ({n} frames)')


def main():
    cmd = sys.argv[1]
    if cmd == 'mask':
        if len(sys.argv) > 4 and sys.argv[4] == 'soft':
            make_mask_soft(sys.argv[2], sys.argv[3])
        else:
            make_mask(sys.argv[2], sys.argv[3], jagged=len(sys.argv) > 4 and sys.argv[4] == 'jagged')
        return
    if cmd == 'firemask':                                          # firemask OUT.png ANGLE FRAME1.png ...
        make_fire_mask(sys.argv[4:], sys.argv[2], sys.argv[3])
        return
    if cmd == 'match':                                             # match OUTDIR OPTION MASKDIR
        make_match(os.path.abspath(sys.argv[2]), sys.argv[3], os.path.abspath(sys.argv[4]))
        return
    if cmd == 'render':                                            # render SRC.mov OUT.mov ANGLE OPTION MASKDIR [N]
        rest = [x for x in sys.argv[7:] if x != '--despeck']
        render(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], limit=int(rest[0]) if rest else None,
               despeck='--despeck' in sys.argv)
        return
    outdir = sys.argv[2]
    make_luts(outdir)
    if cmd == 'luts':
        return
    pairs = [tuple(os.path.abspath(x) for x in p.split('=')) for p in sys.argv[3:]]
    os.chdir(outdir)
    shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'GFSDidot-Regular.ttf'), 'didot.ttf')
    labels = {'0': 'AS NOW'} | {k: f'{k}  -  {o["name"]}' for k, o in OPTIONS.items()}
    rows = []
    for k, lab in labels.items():
        cells = []
        for i, (f, m) in enumerate(pairs):
            c = f'_cell_{k}_{i}.png'
            if k == '0':
                subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f, '-vf', 'scale=720:-2', c], check=True)
            else:
                graded(f, m, k, c)
            cells.append(c)
        txt = lab.replace(':', '\\:')
        row = f'_row_{k}.png'
        ins = sum([['-i', c] for c in cells], [])
        subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex',
                        f"hstack=inputs={len(cells)},drawtext=fontfile=didot.ttf:text='{txt}':fontcolor=white:fontsize=30:"
                        'x=14:y=12:box=1:boxcolor=black@0.6:boxborderw=8', row], check=True)
        rows.append(row)
        for c in cells:
            os.remove(c)
    ins = sum([['-i', r] for r in rows], [])
    subprocess.run(['ffmpeg', '-v', 'error', '-y', *ins, '-filter_complex', f'vstack=inputs={len(rows)}', '-q:v', '2',
                    'S5_grade_ALL_OPTIONS.jpg'], check=True)
    for r in rows:
        os.remove(r)
    os.remove('didot.ttf')
    print('wrote', os.path.join(outdir, 'S5_grade_ALL_OPTIONS.jpg'))


if __name__ == '__main__':
    main()
