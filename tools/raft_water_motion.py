"""S9 RAFT floor water: motion tests for Homie's "it feels a bit stuttery" (2026-11-22, RAFT5).

The approved v2 master (tools/raft_water.py) is 24 fps: every 2nd frame of the 59.94 fps drone clip (speed 0.8).
The cadence is even, so the stutter is 24 fps judder of sharp, fast-shutter frames. This script makes the same
graded loop (same grade(), same speed, same 2 s smoothstep wrap) with different motion sampling:

  --fps 24 --shutter 2      24 fps, each output frame = mean of 2 source frames (a 360-degree shutter blur)
  --fps 48                  48 fps, every source frame (step 1, no new pixels)
  --fps 59.94 --flow        59.94 fps, speed 0.8 -> source step 0.8, in-between frames made by DIS optical flow

Output: OUT/S9_RAFT_FLOOR_water_loop_<tag>_CLEAN_4K.mov (ProRes 422 HQ, silent) + the loop length on stdout.
Usage: python tools/raft_water_motion.py SRC OUT_DIR --tag T [--fps F] [--shutter K] [--flow] [--speed 0.8] [--xf-s 2]
"""
import argparse, collections, math, os, subprocess, sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from raft_water import grade, W, H  # noqa: E402  (same grade as the approved v2)


class Src:
    """Sequential decoder with a small cache, so increasing float positions can ask for frames i, i+1."""
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.i = -1
        self.buf = collections.OrderedDict()

    def get(self, j):
        while self.i < j:
            ok, fr = self.cap.read()
            if not ok: raise SystemExit(f"read fail at {self.i + 1}")
            self.i += 1
            self.buf[self.i] = fr
            while len(self.buf) > 8: self.buf.popitem(last=False)
        return self.buf[j]


DIS = cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_MEDIUM)
FS = 4                                              # flow at 1/4 size (960x540), upscaled
_flow_cache = {}


def flows(src, i):
    if i not in _flow_cache:
        a = cv2.cvtColor(cv2.resize(src.get(i), (W // FS, H // FS), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        b = cv2.cvtColor(cv2.resize(src.get(i + 1), (W // FS, H // FS), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        f = DIS.calc(a, b, None); r = DIS.calc(b, a, None)
        up = lambda x: cv2.resize(x, (W, H), interpolation=cv2.INTER_LINEAR) * FS
        _flow_cache.clear(); _flow_cache[i] = (up(f), up(r))
    return _flow_cache[i]


GX, GY = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))


def at(src, p, flow):
    """Source picture at float position p (BGR float 0-255)."""
    i = int(math.floor(p + 1e-6)); t = p - i
    if t < 1e-3 or not flow:
        if t < 1e-3: return src.get(i).astype(np.float32)
        return src.get(i).astype(np.float32) * (1 - t) + src.get(i + 1).astype(np.float32) * t
    f, r = flows(src, i)                           # backward warp of both neighbours toward time t
    a = cv2.remap(src.get(i), GX - t * f[..., 0], GY - t * f[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    b = cv2.remap(src.get(i + 1), GX - (1 - t) * r[..., 0], GY - (1 - t) * r[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return a.astype(np.float32) * (1 - t) + b.astype(np.float32) * t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--tag", required=True)
    ap.add_argument("--fps", default="24"); ap.add_argument("--shutter", type=int, default=1)
    ap.add_argument("--flow", action="store_true"); ap.add_argument("--speed", type=float, default=0.8)
    ap.add_argument("--xf-s", type=float, default=2.0)
    a = ap.parse_args()
    fps_s = {"59.94": "60000/1001", "29.97": "30000/1001"}.get(a.fps, a.fps)
    fps = eval(fps_s)
    os.makedirs(a.out, exist_ok=True)
    src = Src(a.src)
    step = src.fps * a.speed / fps
    if abs(step - round(step)) < 0.01: step = float(round(step))    # same integer lock as raft_water.py v2
    if step != int(step) and not a.flow: print("WARNING fractional step without --flow: linear blend", flush=True)
    XF = int(round(a.xf_s * fps))
    total = int((src.n - 1) / src.fps * a.speed * fps)      # same source span as raft_water.py v2 (src 0..~599)
    N = total - XF
    print(f"src {src.n} f @ {src.fps:.3f}; out {fps_s} step {step:.4f} shutter {a.shutter} flow {a.flow}; "
          f"loop {N} f ({N / fps:.3f} s) + {XF} f crossfade", flush=True)

    tail = {}                                       # pass 1: the tail N..N+XF-1 (decoder is sequential)
    for k in range(N, N + XF):
        tail[k] = frame_with(src, k, step, a)
    src = Src(a.src); _flow_cache.clear()
    out = os.path.join(a.out, f"S9_RAFT_FLOOR_water_loop_{a.tag}_CLEAN_4K.mov")
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr48le", "-s", f"{W}x{H}",
                            "-r", fps_s, "-i", "-", "-c:v", "prores_ks", "-profile:v", "3", "-qscale:v", "2",
                            "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-colorspace", "bt709", out], stdin=subprocess.PIPE)
    for k in range(N):
        img = frame_with(src, k, step, a)
        if k < XF:
            w = (k + 0.5) / XF; w = w * w * (3 - 2 * w)
            img = tail[N + k] * (1 - w) + img * w
        enc.stdin.write((np.clip(img, 0, 1) * 65535).astype(np.uint16).tobytes())
        if k % 60 == 0: print("frame", k, "/", N, flush=True)
    enc.stdin.close(); enc.wait()
    print("DONE", out, N, "frames", flush=True)


def frame_with(src, k, step, a):
    p = k * step
    acc = sum(at(src, p + j, a.flow) for j in range(a.shutter)) / a.shutter
    return grade(np.clip(acc + 0.5, 0, 255).astype(np.uint8))


if __name__ == "__main__":
    main()
