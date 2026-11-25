"""Scene 5 -> Scene 6 cannonball cue: a 4-surface REVIEW file (LEFT | CENTRE | RIGHT, FLOOR under CENTRE). 0 credits.

Built 2026-11-25 (F33, docs/HANDOFF-2026-11-25-F33.md "Next" 2, docs/BRIEF-F31-CANNONBALL-BLADES.md Proposal 3).
Reads the show folder and the generated fireball, never writes to them. Writes only to OUT_DIR.

THE CUE (24 fps, frame numbers on the review clock, all set in the TIMINGS block below):
  0 .. IMPACT-FLIGHT        the last seconds of Scene 5 (each wall's own S5 show file, ending on its last frame at CUT)
  IMPACT-FLIGHT .. IMPACT   a drawn 1819 round shot (dark iron, shaded, 5-sample motion blur) flies in on RIGHT and arcs
                            to CENTRE, growing as it nears (it comes at the audience)
  IMPACT ..                 the generated fireball (S5-CANNON-FIRE v1, on black) bursts on CENTRE, keyed luma-to-alpha;
                            LEFT / RIGHT / FLOOR get the same fire, offset off their centre-side edge and scaled (RIGHT
                            mirrored), plus a warm flash over their S5 picture that follows the fire's brightness
  SMOKE_START .. CUT        a growing noisy matte (from each wall's impact point) reveals Scene 6's FIRST FRAME while
                            the fire fades out, so the frame before CUT IS S6 frame 0 on every wall (matte = 1, fire = 0)
  CUT ..                    Scene 6 plays from its frame 0 (S6 has no FLOOR file: the FLOOR reveals black, its S6 state)
Every layer is one alpha OVER the S5 picture (overlay()), so the later per-wall 4K ProRes 4444 alpha cue file is the
same function at the S6 wall size: `overlay(wall, f, W, H, ...)` returns (rgb, alpha). Not built here.
Review: S5 (16:9 renders) is fitted to each wall's S6 shape (4:3 / 5:3 / 4:3; FLOOR 16:9), as the mapper fills a flat.
Sound: S5 CENTRE's own sound to CUT, S6 CENTRE's own sound from CUT, the fireball's generated sound at its place.

  python tools/cannon_review.py [--out PATH] [--sheet PATH] [--check]
Heavy decode (4K ProRes): run with CPU affinity FFFF3FFF (off Core 7); child ffmpeg processes inherit it.
"""
import argparse
import os
import subprocess
import sys

import cv2
import numpy as np

# ---------------------------------------------------------------- TIMINGS (frames at 24 fps)
FPS = 24
PRE = 48            # S5 alone before the ball (2.0 s)
FLIGHT = 30         # ball flight RIGHT -> CENTRE (1.25 s)
IMPACT = PRE + FLIGHT           # 78: first fire frame (3.25 s)
SMOKE_START = IMPACT + 24       # 102: the S6 reveal matte starts growing (4.25 s)
CUT = IMPACT + 84               # 162: S6 frame 0 plays here (6.75 s); frame CUT-1 == S6 frame 0
POST = 96           # S6 after the cut (4.0 s)
TOTAL = CUT + POST              # 258 frames = 10.75 s
FIRE_FADE_START = SMOKE_START   # the fire layer fades to 0 by CUT-1

# ---------------------------------------------------------------- LOOK
FIRE_LO, FIRE_GAIN = 0.035, 7.0         # luma-to-alpha: a = clip((luma - LO) * GAIN)
FIRE_FEATHER = 0.40                     # elliptical edge feather of the fire (fraction of its half-size)
FLASH_RGB = np.array([255, 178, 110], np.float32) / 255.0
FLASH_MAX = 0.55
BALL_RGB = np.array([34, 31, 29], np.float32) / 255.0
BALL_HI = np.array([150, 110, 80], np.float32) / 255.0    # warm sky rim on the iron
BALL_R0, BALL_R1 = 0.007, 0.045         # radius in wall heights: far -> at impact
BALL_START = (4.05, 0.18)               # (u, v) in wall heights on the unfolded L|C|R strip
BALL_ARC = 0.22                         # arc height (wall heights)
BALL_EASE = 1.7                         # p ** EASE: it speeds up as it nears
BLUR_SAMPLES, SHUTTER = 5, 0.5
MATTE_SOFT, MATTE_NOISE = 0.18, 0.45    # reveal edge softness and noise amplitude (wall heights)
WALL_ASPECT = {'LEFT': 4 / 3, 'CENTRE': 5 / 3, 'RIGHT': 4 / 3, 'FLOOR': 16 / 9}
# fire placement per wall: centre (x, y) as fractions of the wall, fire width as a fraction of wall width, mirror
FIRE_AT = {'CENTRE': (0.50, 0.55, 1.15, False),
           'LEFT':   (1.22, 0.55, 1.75, False),
           'RIGHT':  (-0.22, 0.55, 1.75, True),
           'FLOOR':  (0.50, -0.45, 1.30, False)}
STRIP_U0 = {'LEFT': 0.0, 'CENTRE': 4 / 3, 'RIGHT': 3.0}  # ball strip: where each wall starts (wall heights)

# ---------------------------------------------------------------- FILES
MEDIA = r'D:\SOTR\SOTR_MEDIA'
PLAY = os.path.join(MEDIA, '01_FINAL_FOR_SHOW', '1_PLAY_THESE_IN_ORDER')
S5 = {w: os.path.join(PLAY, 'S05_the-camps', f'S5_{w}_camps.mov') for w in ('LEFT', 'CENTRE', 'RIGHT', 'FLOOR')}
S6 = {w: os.path.join(PLAY, 'S06_Napoleonic-wars', f'S6_{w}_wars.mov') for w in ('LEFT', 'CENTRE', 'RIGHT')}
FIRE = os.path.join(MEDIA, '04_WORKING_FILES', 'S5_cannonball', 'gen', 'S5-CANNON-FIRE_v1_37ea12e7.mp4')
OUT_DIR = os.path.join(MEDIA, '04_WORKING_FILES', 'S5_cannonball', 'review_v1')
OUT = os.path.join(OUT_DIR, 'S5_CANNON_cue_review_v1.mp4')
SHEET = os.path.join(OUT_DIR, '_sheet_review_v1.jpg')
FONT = 'C\\:/Windows/Fonts/consola.ttf'

# ---------------------------------------------------------------- REVIEW LAYOUT (share_previews style + FLOOR row)
CW, MARGIN, GAP, TOP, LAB = 1600, 10, 10, 40, 30
WH = 360                                  # wall height in the top row
FH = 270                                  # FLOOR height
BG = (38, 38, 38)


def boxes():
    ws = {w: int(round(WALL_ASPECT[w] * WH)) // 2 * 2 for w in ('LEFT', 'CENTRE', 'RIGHT')}
    x = (CW - (sum(ws.values()) + 2 * GAP)) // 2
    b = {}
    for w in ('LEFT', 'CENTRE', 'RIGHT'):
        b[w] = (x, TOP, ws[w], WH)
        x += ws[w] + GAP
    fw = int(round(WALL_ASPECT['FLOOR'] * FH)) // 2 * 2
    cx, _, cwid, _ = b['CENTRE']
    b['FLOOR'] = (cx + (cwid - fw) // 2, TOP + WH + LAB, fw, FH)
    ch = TOP + WH + LAB + FH + LAB + 44
    return b, ch


# ---------------------------------------------------------------- decode
def frames(path, w, h, n, pre=(), vf_extra='', pad_ok=False):
    vf = f'fps={FPS},scale={w}:{h}:flags=bicubic{vf_extra},format=rgb24'
    p = subprocess.run(['ffmpeg', '-v', 'error', *pre, '-i', path, '-frames:v', str(n), '-vf', vf, '-f', 'rawvideo', '-'],
                       capture_output=True, check=True)
    a = np.frombuffer(p.stdout, np.uint8).reshape(-1, h, w, 3)
    if len(a) < n and not pad_ok:                         # hold the last frame if the source is a frame short
        a = np.concatenate([a, np.repeat(a[-1:], n - len(a), 0)])
    return a


def duration(path):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path],
                                capture_output=True, text=True, check=True).stdout)


# ---------------------------------------------------------------- layers
def smooth(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def noise_field(w, h, seed):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for k, amp in ((6, 0.55), (14, 0.3), (32, 0.15)):
        g = rng.random((max(2, k * h // w), k)).astype(np.float32)
        acc += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
    acc = (acc - acc.min()) / (acc.max() - acc.min() + 1e-6)
    return acc - 0.5                       # [-0.5, 0.5]


class Wall:
    def __init__(self, name, W, H, fire, fire_env, burst, s6_first):
        self.name, self.W, self.H = name, W, H
        self.fire, self.env, self.burst = fire, fire_env, burst
        self.s6_first = s6_first.astype(np.float32) / 255.0        # (H, W, 3)
        fx, fy, fs, mirror = FIRE_AT[name]
        self.fx, self.fy, self.fs, self.mirror = fx, fy, fs, mirror
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        self.xs, self.ys = xs / W, ys / H
        asp = W / H
        self.d = np.sqrt(((self.xs - fx) * asp) ** 2 + (self.ys - fy) ** 2)    # wall heights from the impact point
        self.noise = noise_field(W, 2 * H, sum(map(ord, name)))                   # scrolls up through the reveal
        self.r_end = float(self.d.max()) + 0.5 * MATTE_NOISE + MATTE_SOFT + 0.02
        # flash falloff: strongest on the side facing CENTRE
        fall = {'LEFT': self.xs ** 1.5, 'RIGHT': (1 - self.xs) ** 1.5, 'FLOOR': (1 - self.ys) ** 1.5,
                'CENTRE': np.full_like(self.xs, 0.6)}[name]
        self.fall = (0.25 + 0.75 * fall)[..., None]
        # fire placement (pixels)
        self.fw = int(round(fs * W))
        self.fh = int(round(self.fw * fire.shape[1] / fire.shape[2]))
        self.fx0 = int(round(fx * W - self.fw / 2))
        self.fy0 = int(round(fy * H - self.fh / 2))
        e = FIRE_FEATHER
        u = np.linspace(0, 1, self.fw, dtype=np.float32)
        v = np.linspace(0, 1, self.fh, dtype=np.float32)
        # elliptical feather: the burst frames carry a full-frame glow, a rectangle would show its corners
        rr = np.sqrt(((u[None, :] - 0.5) / 0.5) ** 2 + ((v[:, None] - 0.5) / 0.5) ** 2)
        self.feather = smooth((1.08 - rr) / e)

    def fire_layer(self, f):
        """(rgb, a) of the fire on this wall at review frame f, or None."""
        k = f - IMPACT + self.burst
        if f < IMPACT or k >= len(self.fire):
            return None
        src = self.fire[k].astype(np.float32) / 255.0
        if self.mirror:
            src = src[:, ::-1]
        src = cv2.resize(src, (self.fw, self.fh), interpolation=cv2.INTER_LINEAR)
        luma = src @ np.array([0.2126, 0.7152, 0.0722], np.float32)
        a = np.clip((luma - FIRE_LO) * FIRE_GAIN, 0, 1) * self.feather
        rgb = np.zeros((self.H, self.W, 3), np.float32)
        al = np.zeros((self.H, self.W), np.float32)
        x0, y0 = self.fx0, self.fy0
        sx0, sy0 = max(0, -x0), max(0, -y0)
        dx0, dy0 = max(0, x0), max(0, y0)
        w = min(self.fw - sx0, self.W - dx0)
        h = min(self.fh - sy0, self.H - dy0)
        if w <= 0 or h <= 0:
            return None
        rgb[dy0:dy0 + h, dx0:dx0 + w] = src[sy0:sy0 + h, sx0:sx0 + w]
        al[dy0:dy0 + h, dx0:dx0 + w] = a[sy0:sy0 + h, sx0:sx0 + w]
        fade = 1.0 - smooth((f - FIRE_FADE_START) / max(1, (CUT - 1 - FIRE_FADE_START)))
        if f >= CUT - 1:
            fade = 0.0
        return rgb, al * fade

    def flash_layer(self, f):
        if self.name == 'CENTRE':
            return None                     # CENTRE has the fire itself
        k = f - IMPACT + self.burst
        if f < IMPACT or k >= len(self.env):
            return None
        a = FLASH_MAX * self.env[k] * self.fall[..., 0]
        if f >= CUT - 1:
            a = a * 0
        return np.broadcast_to(FLASH_RGB, (self.H, self.W, 3)), a

    def ball_layer(self, f):
        if self.name not in STRIP_U0 or not (IMPACT - FLIGHT <= f < IMPACT):
            return None
        acc = np.zeros((self.H, self.W), np.float32)
        col = np.zeros((self.H, self.W, 3), np.float32)
        u0 = STRIP_U0[self.name]
        end = (STRIP_U0['CENTRE'] + FIRE_AT['CENTRE'][0] * WALL_ASPECT['CENTRE'], FIRE_AT['CENTRE'][1])
        for s in range(BLUR_SAMPLES):
            t = (f - (IMPACT - FLIGHT) + SHUTTER * s / BLUR_SAMPLES) / FLIGHT
            p = min(1.0, max(0.0, t)) ** BALL_EASE
            u = BALL_START[0] + (end[0] - BALL_START[0]) * p
            v = BALL_START[1] + (end[1] - BALL_START[1]) * p - BALL_ARC * 4 * p * (1 - p)
            r = BALL_R0 * (BALL_R1 / BALL_R0) ** p
            cx, cy, rp = (u - u0) * self.H, v * self.H, r * self.H
            if cx < -rp - 2 or cx > self.W + rp + 2:
                continue
            dx, dy = self.xs * self.W - cx, self.ys * self.H - cy
            dist = np.sqrt(dx * dx + dy * dy)
            a = np.clip(rp + 0.5 - dist, 0, 1)
            # shading: dark iron, warm rim light from the upper left
            nx, ny = dx / max(rp, 1e-3), dy / max(rp, 1e-3)
            lit = np.clip(-0.6 * nx - 0.8 * ny, 0, 1) ** 3 * np.clip(dist / max(rp, 1e-3), 0, 1)
            c = BALL_RGB[None, None, :] + (BALL_HI - BALL_RGB)[None, None, :] * lit[..., None] * 0.8
            col += c * a[..., None]
            acc += a
        if acc.max() <= 0:
            return None
        a = acc / BLUR_SAMPLES
        rgb = col / np.maximum(acc, 1e-6)[..., None]
        return rgb, a

    def reveal_layer(self, f):
        if f < SMOKE_START:
            return None
        if f >= CUT - 1:
            return self.s6_first, np.ones((self.H, self.W), np.float32)
        t = smooth((f - SMOKE_START) / (CUT - 1 - SMOKE_START))
        r = t * self.r_end
        sh = int((f - SMOKE_START) * self.H / (2.0 * (CUT - SMOKE_START)))   # scroll the noise upward
        n = self.noise[self.H - sh: 2 * self.H - sh] if sh > 0 else self.noise[self.H:]
        m = np.clip((r - self.d + MATTE_NOISE * n) / MATTE_SOFT, 0, 1)
        return self.s6_first, m


def overlay(wall, f):
    """The cue as ONE layer over S5 at frame f: unpremultiplied rgb (H, W, 3) float and alpha (H, W) float."""
    P = np.zeros((wall.H, wall.W, 3), np.float32)
    A = np.zeros((wall.H, wall.W), np.float32)
    for layer in (wall.flash_layer(f), wall.fire_layer(f), wall.ball_layer(f), wall.reveal_layer(f)):
        if layer is None:
            continue
        c, a = layer
        P = c * a[..., None] + P * (1 - a[..., None])
        A = a + A * (1 - a)
    rgb = P / np.maximum(A, 1e-6)[..., None]
    return rgb, A


# ---------------------------------------------------------------- build
def build(out, sheet):
    b, ch = boxes()
    os.makedirs(os.path.dirname(out), exist_ok=True)
    s5_start = {w: duration(S5[w]) - CUT / FPS for w in S5}
    print('decode fire ...', flush=True)
    fire = frames(FIRE, 640, 360, 10000, pad_ok=True)
    luma = fire.astype(np.float32).mean(axis=(1, 2, 3))
    burst = int(np.argmax(luma > 10))
    env = np.clip((luma - 5) / (luma.max() - 5), 0, 1)
    print(f'fire {len(fire)} frames, burst at fire frame {burst}', flush=True)
    s5, s6, walls = {}, {}, {}
    for w, (x, y, ww, hh) in b.items():
        print(f'decode {w} ...', flush=True)
        s5[w] = frames(S5[w], ww, hh, CUT, pre=('-ss', f'{s5_start[w]:.4f}'))
        s6[w] = frames(S6[w], ww, hh, POST) if w in S6 else np.zeros((POST, hh, ww, 3), np.uint8)
        walls[w] = Wall(w, ww, hh, fire, env, burst, s6[w][0])
    tmp = os.path.join(os.path.dirname(out), '_tmp_video.mp4')
    wav = os.path.join(os.path.dirname(out), '_tmp_sound.wav')
    # the sound: S5 CENTRE to CUT, S6 CENTRE from CUT, the fireball's own sound at its place
    fire_at_ms = int(round((IMPACT - burst) / FPS * 1000))
    cut_ms = int(round(CUT / FPS * 1000))
    af = (f'[0:a]atrim=0:{CUT / FPS:.4f},asetpts=N/SR/TB,aresample=48000[a5];'
          f'[1:a]atrim=0:{POST / FPS:.4f},asetpts=N/SR/TB,aresample=48000,adelay={cut_ms}|{cut_ms}[a6];'
          f'[2:a]aresample=48000,adelay={fire_at_ms}|{fire_at_ms}[af];'
          f'[a5][a6][af]amix=inputs=3:normalize=0:duration=longest,atrim=0:{TOTAL / FPS:.4f},'
          f'alimiter=limit=0.95:level=disabled[a]')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{s5_start["CENTRE"]:.4f}', '-i', S5['CENTRE'],
                    '-i', S6['CENTRE'], '-i', FIRE, '-filter_complex', af, '-map', '[a]', '-c:a', 'pcm_s16le', wav],
                   check=True)
    phases = [(0, IMPACT - FLIGHT, 'Scene 5'), (IMPACT - FLIGHT, IMPACT, 'the ball  RIGHT to CENTRE'),
              (IMPACT, SMOKE_START, 'impact  fire on CENTRE + flash and fire on LEFT / RIGHT / FLOOR'),
              (SMOKE_START, CUT, 'smoke reveals Scene 6 frame 1  (the change is inside the file)'),
              (CUT, TOTAL, 'Scene 6 plays')]
    txt = f"fontfile='{FONT}':fontcolor=white"
    dt = [f"drawtext={txt}:fontsize=20:x={MARGIN}:y=11:text='Scene 5 -> 6  CANNONBALL CUE  review v1  (0 cr  script)'",
          f"drawtext={txt}:fontsize=18:x=w-tw-{MARGIN}:y=12:text='%{{pts\\:hms}}  f %{{frame_num}}'"]
    names = {'LEFT': 'LEFT', 'CENTRE': 'CENTRE (back wall)', 'RIGHT': 'RIGHT', 'FLOOR': 'FLOOR  (S6 = black  no floor file)'}
    for w, (x, y, ww, hh) in b.items():
        dt.append(f"drawtext={txt}:fontsize=15:fontcolor=0xbbbbbb:x={x}+({ww}-tw)/2:y={y + hh + 7}:text='{names[w]}'")
    for a, z, t in phases:
        dt.append(f"drawtext={txt}:fontsize=18:fontcolor=0xffd9a0:x={MARGIN}:y=h-32:"
                  f"text='{t}':enable=between(n\\,{a}\\,{z - 1})")
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{ch}',
                            '-r', str(FPS), '-i', '-', '-i', wav, '-vf', ','.join(dt) + ',format=yuv420p',
                            '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart',
                            tmp], stdin=subprocess.PIPE)
    for f in range(TOTAL):
        canvas = np.full((ch, CW, 3), BG, np.uint8)
        for w, (x, y, ww, hh) in b.items():
            if f < CUT:
                base = s5[w][f].astype(np.float32) / 255.0
                rgb, a = overlay(walls[w], f)
                pic = rgb * a[..., None] + base * (1 - a[..., None])
                pic = np.clip(pic * 255 + 0.5, 0, 255).astype(np.uint8)
            else:
                pic = s6[w][f - CUT]
            canvas[y:y + hh, x:x + ww] = pic
        enc.stdin.write(canvas.tobytes())
        if f % 24 == 0:
            print(f'  frame {f}/{TOTAL}', flush=True)
    enc.stdin.close()
    if enc.wait() != 0:
        sys.exit('ffmpeg encode failed')
    os.replace(tmp, out)
    os.remove(wav)
    make_sheet(out, sheet)


def make_sheet(out, sheet):
    vf = (f"select='not(mod(n\\,12))',drawtext=fontfile='{FONT}':fontcolor=yellow:fontsize=40:box=1:boxcolor=black@0.6:"
          f"x=12:y=h-60:text='%{{pts\\:hms}} f%{{frame_num}}',scale=640:-2,tile=4x6")
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', out, '-vf', vf, '-frames:v', '1', '-q:v', '3', sheet],
                   check=True)


def check(out):
    """ffprobe + the join: per wall box, the decoded frame CUT-1 (last cue frame) vs frame CUT (S6 frame 0)."""
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries',
                        'stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate:format=duration',
                        '-of', 'compact', out], capture_output=True, text=True, check=True)
    print(r.stdout.strip())
    b, ch = boxes()
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', out, '-vf', f"select='between(n\\,{CUT - 2}\\,{CUT})'",
                          '-fps_mode', 'passthrough', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, ch, CW, 3).astype(np.float32)
    for w, (x, y, ww, hh) in b.items():
        a, c, d = (fr[i, y:y + hh, x:x + ww] for i in range(3))
        print(f'{w:7s} |cue last - S6 f0| mean {np.abs(c - d).mean():.2f}  max {np.abs(c - d).max():.0f}   '
              f'(prev cue frame vs S6 f0 mean {np.abs(a - d).mean():.2f})')
    # the source truth: S6 frame 0 at the box size vs the cue's last frame, before H.264
    for w in S6:
        x, y, ww, hh = b[w]
        s6f = frames(S6[w], ww, hh, 1)[0].astype(np.float32)
        print(f'{w:7s} output f{CUT - 1} vs S6 source f0 (encode error only): mean {np.abs(fr[1, y:y + hh, x:x + ww] - s6f).mean():.2f}')


def pin_affinity(mask=0xFFFF3FFF):
    """Keep this process and every ffmpeg child off Core 7 (the PC hard-crashes there under all-core load)."""
    if sys.platform == 'win32':
        import ctypes
        k = ctypes.windll.kernel32
        k.GetCurrentProcess.restype = ctypes.c_void_p
        if not k.SetProcessAffinityMask(ctypes.c_void_p(k.GetCurrentProcess()), ctypes.c_size_t(mask)):
            sys.exit('could not set CPU affinity FFFF3FFF')


def main():
    pin_affinity()
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=OUT)
    ap.add_argument('--sheet', default=SHEET)
    ap.add_argument('--check', action='store_true', help='only check an existing output')
    a = ap.parse_args()
    if not a.check:
        build(a.out, a.sheet)
    check(a.out)


if __name__ == '__main__':
    main()
