"""S9 RAFT floor water (Route C, Homie's stock clip, 2026-11-22).

Top-down stock ocean -> moonlit night FLOOR loop. DEFAULT (Homie 2026-11-22): the FULL 16:9 ocean frame, no raft hole,
no bars, no fade, no sound; the projection expert fits the raft and the floor. --envelope gives docs/FLOOR-PLAN.md section 2:
16:9 frame, floor envelope 10,057 x 4,350 mm at true proportion, full width, centred, black above/below,
top of picture = upstage, soft fade to black 300 mm inside the envelope edge, brightness capped, no pre-warp.

Outputs (OUT dir):
  S9_RAFT_FLOOR_water_loop_CLEAN_4K.mov   seamless loop unit, no raft, ProRes 422 HQ, 24 fps (the master)
  S9_RAFT_FLOOR_b1_preview_PLACEHOLDER_RAFT_1080.mp4   40 s look preview, placeholder raft masked black + wash line,
                                                       scratch sea sound from the S7 night take

The source clip has no usable sound (-91 dB), so scratch sound comes from S7-SEA-IDLE_night_v2.
Usage: python tools/raft_water.py SRC OUT_DIR [--speed 0.8] [--raft-mm 2400x1800]
"""
import argparse, os, subprocess, sys
import cv2
import numpy as np

W, H = 3840, 2160
ENV_MM = (10057, 4350)
PX_PER_MM = W / ENV_MM[0]
ENV_H = int(round(ENV_MM[1] * PX_PER_MM))          # 1660
ENV_Y0 = (H - ENV_H) // 2
SAFE_PX = int(round(300 * PX_PER_MM))              # 115
FPS = 24
XF = 48                                            # loop crossfade, frames

# night palette (BGR, 0-1), body from the S7 night sea (water region median ~ BGR 66/46/26)
BODY = np.array([0.56, 0.33, 0.13], np.float32)    # deep moonlit blue-teal at full source luminance
MOON = np.array([0.95, 0.90, 0.86], np.float32)    # pale cool moonlight on foam
PEAK = 0.42                                        # brightness cap (provisional; set at the seat preview)


def envelope_fade():
    """Soft fade to black from the safe line to the envelope edge, black outside the envelope."""
    m = np.zeros((H, W), np.float32)
    m[ENV_Y0 + SAFE_PX:ENV_Y0 + ENV_H - SAFE_PX, SAFE_PX:W - SAFE_PX] = 1.0
    m = cv2.GaussianBlur(m, (0, 0), SAFE_PX * 0.55)
    env = np.zeros((H, W), np.float32)
    env[ENV_Y0:ENV_Y0 + ENV_H, :] = 1.0
    return (m * env)[..., None]


def softcap(x):
    """Soft knee into the brightness cap, so foam keeps its texture instead of clipping flat."""
    return PEAK * np.tanh(x / PEAK)


def grade(bgr8):
    """Day turquoise -> late-night dark blue. Hue is thrown away; luminance drives body + moonlit foam."""
    f = bgr8.astype(np.float32) / 255.0
    L = f[..., 0] * 0.114 + f[..., 1] * 0.587 + f[..., 2] * 0.299
    # flatten the daylight gradients (the bright shallow glow) so the sea reads open and deep
    low = cv2.GaussianBlur(L, (0, 0), 120)
    detail = L - low
    base = 0.30 + 0.35 * (low - low.mean())
    body = np.clip(base + 1.1 * detail, 0, 1) ** 1.15
    foam = cv2.GaussianBlur(np.clip((L - 0.50) / 0.45, 0, 1) ** 1.4, (0, 0), 1.2)   # whitecaps, foam veins
    out = body[..., None] * BODY + (foam * 0.42)[..., None] * MOON
    return softcap(out)


def raft_masks(raft_mm):
    rw, rh = (int(round(v * PX_PER_MM)) for v in raft_mm)
    cx, cy = W // 2, ENV_Y0 + ENV_H // 2
    r = np.zeros((H, W), np.uint8)
    cv2.rectangle(r, (cx - rw // 2, cy - rh // 2), (cx + rw // 2, cy + rh // 2), 255, -1)
    raft = cv2.GaussianBlur(r.astype(np.float32) / 255, (0, 0), 3)
    d = cv2.distanceTransform(255 - r, cv2.DIST_L2, 5)          # px from the raft edge, outside
    wash = np.exp(-d / (120 * PX_PER_MM)) * (d > 0)             # ~120 mm wash band
    return raft[..., None], wash.astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--speed", type=float, default=0.8)
    ap.add_argument("--raft-mm", default="2400x1800")
    ap.add_argument("--preview-s", type=float, default=40.0)
    ap.add_argument("--envelope", action="store_true", help="old FLOOR-PLAN framing: envelope band, black bars, safe-area fade")
    ap.add_argument("--raft", action="store_true", help="placeholder raft + scratch sound in the preview (off: Homie 2026-11-22, the projection expert fits the raft, sound is Darren's)")
    ap.add_argument("--scratch", default=r"C:\Users\Homie\Documents\SOTR_MEDIA\04_WORKING_FILES\S7_ship\9_seaplate\S7-SEA-IDLE_night_v2_6f1a54ec.mp4")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    cap = cv2.VideoCapture(a.src)
    sfps = cap.get(cv2.CAP_PROP_FPS); sn = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    total = int((sn - 1) / sfps * a.speed * FPS)                 # output frames available
    N = total - XF                                               # loop length
    want = {k: int(round(k * sfps * a.speed / FPS)) for k in range(N + XF)}
    print(f"src {sn} f @ {sfps:.3f}; out {N} f loop ({N / FPS:.2f} s) + {XF} f crossfade", flush=True)

    fade = envelope_fade()
    ys = slice((2160 - ENV_H) // 2, (2160 - ENV_H) // 2 + ENV_H)  # centre crop of the source to the envelope

    def place(src):
        if not a.envelope:                                       # Homie 2026-11-22: full ocean frame, no hole,
            return grade(src)                                    # no bars, no fade; the projection expert fits it
        img = np.zeros((H, W, 3), np.float32)
        img[ENV_Y0:ENV_Y0 + ENV_H] = grade(src[ys])
        return img * fade

    # pass 1: grade the tail (frames N..N+XF-1) and keep them for the crossfade
    by_src = {}
    for k, s in want.items():
        by_src.setdefault(s, []).append(k)
    tail = {}
    frames_needed = sorted(by_src)
    out_path = os.path.join(a.out, "S9_RAFT_FLOOR_water_loop_CLEAN_4K.mov")
    tail_keys = set(range(N, N + XF))
    i = 0
    for s in frames_needed:
        while i <= s:
            ok, fr = cap.read(); i += 1
            if not ok: raise SystemExit(f"read fail at {i}")
        for k in by_src[s]:
            if k in tail_keys:
                tail[k] = place(fr)
    cap.release()

    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr48le", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "prores_ks", "-profile:v", "3", "-qscale:v", "2",
                            "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", out_path], stdin=subprocess.PIPE)
    cap = cv2.VideoCapture(a.src); i = 0; peak = 0.0
    for s in frames_needed:
        while i <= s:
            ok, fr = cap.read(); i += 1
        for k in by_src[s]:
            if k >= N: continue
            img = place(fr)
            if k < XF:                                           # tail -> head crossfade = seamless wrap
                w = (k + 0.5) / XF
                w = w * w * (3 - 2 * w)
                img = tail[N + k] * (1 - w) + img * w
            peak = max(peak, float(img.max()))
            enc.stdin.write((np.clip(img, 0, 1) * 65535).astype(np.uint16).tobytes())
            if k % 60 == 0: print("frame", k, flush=True)
    enc.stdin.close(); enc.wait()
    print("master", out_path, "peak", round(peak, 3), flush=True)

    # preview: tile the loop to preview-s, placeholder raft + wash line, 1080, scratch sound
    raft, wash = raft_masks([int(v) for v in a.raft_mm.split("x")])
    pf = int(a.preview_s * FPS)
    prev = os.path.join(a.out, "S9_RAFT_FLOOR_b1_preview_PLACEHOLDER_RAFT_1080.mp4" if a.raft else "S9_RAFT_FLOOR_water_40s_preview_1080.mp4")
    aud = ["-stream_loop", "-1", "-i", a.scratch, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k"] if a.raft else ["-map", "0:v"]
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-stream_loop", "-1", "-i", out_path, "-frames:v", str(pf),
                            "-f", "rawvideo", "-pix_fmt", "bgr48le", "-"], stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080",
                            "-r", str(FPS), "-i", "-", *aud, "-t", str(a.preview_s),
                            "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", prev], stdin=subprocess.PIPE)
    fb = W * H * 3 * 2
    for k in range(pf):
        buf = dec.stdout.read(fb)
        if len(buf) < fb: break
        img = np.frombuffer(buf, np.uint16).reshape(H, W, 3).astype(np.float32) / 65535
        lum = cv2.GaussianBlur(img.max(2), (0, 0), 6)
        churn = 0.5 + 0.5 * np.sin(k / FPS * 2 * np.pi / 3.1 + wash * 9)   # slow lap against the edge
        foamline = np.clip(wash * (0.02 + 1.6 * lum) * (0.6 + 0.4 * churn), 0, PEAK)[..., None] * MOON
        if a.raft:
            img = softcap(img + foamline) * (1 - raft)
        small = cv2.resize(img, (1920, 1080), interpolation=cv2.INTER_AREA)
        enc.stdin.write((np.clip(small, 0, 1) * 255 + 0.5).astype(np.uint8).tobytes())
    dec.stdout.close(); dec.wait(); enc.stdin.close(); enc.wait()
    print("preview", prev, flush=True)


if __name__ == "__main__":
    main()
