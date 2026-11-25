"""S5 cannon probe review with a SEAMLESS join into S6 (F40).

Review = S5 tail (seg_a) + probe (scaled to 1920x1080) + S6 head (seg_c).
The S6 head moves from frame 0, so a still probe end cuts into moving smoke.
Fix: build a synthetic S6 pre-roll by pulling S6 frame 0 backward along its own
optical flow (mean of frames 0->1..0->4), then crossfade the probe's last N frames
into that pre-roll; the last pre-roll frame leads straight into the real frame 0.

usage: python tools/probe_join.py PROBE.mp4 SEG_A.mp4 SEG_C.mp4 OUT.mp4 [N=24]
"""
import subprocess, sys
import numpy as np, cv2

W, H, FPS = 1920, 1080, 24


def frames(path, scale=True):
    vf = f"scale={W}:{H}:flags=lanczos" if scale else "null"
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", vf, "-f", "rawvideo",
                          "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)


def dur(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True).stdout)


def main():
    probe, sa, sc, out = sys.argv[1:5]
    N = int(sys.argv[5]) if len(sys.argv) > 5 else 24
    P, A, C = frames(probe), frames(sa), frames(sc)
    # mean per-frame flow of the S6 head, at half res for robustness
    g = [cv2.cvtColor(cv2.resize(f, (W // 2, H // 2), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY) for f in C[:5]]
    flows = [cv2.calcOpticalFlowFarneback(g[0], g[k], None, 0.5, 4, 31, 5, 7, 1.5, 0) / k for k in range(1, 5)]
    v = np.mean(flows, 0)
    v = cv2.GaussianBlur(v, (0, 0), 6)
    v = cv2.resize(v, (W, H), interpolation=cv2.INTER_LINEAR) * 2.0
    print("S6 flow px/f mean x %.3f y %.3f" % (v[..., 0].mean(), v[..., 1].mean()))
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    f0 = C[0]
    pre = []  # pre[i] = S6 at time -(N-i), i = 0..N-1
    for i in range(N):
        k = N - i
        pre.append(cv2.remap(f0, gx + k * v[..., 0], gy + k * v[..., 1], cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT))
    P = P.copy()
    for i in range(N):
        t = (i + 1) / (N + 1)
        a = t * t * (3 - 2 * t)
        idx = len(P) - N + i
        P[idx] = cv2.addWeighted(P[idx], 1 - a, pre[i], a, 0)
    # join check: MAD of the last built frame vs S6 frame 0
    mad = np.abs(P[-1].astype(np.int16) - f0.astype(np.int16)).mean()
    mad_prev = np.abs(C[1].astype(np.int16) - C[0].astype(np.int16)).mean()
    print("join MAD %.2f (S6 own f0->f1 MAD %.2f)" % (mad, mad_prev))
    la, lp = len(A) / FPS, len(P) / FPS
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-i", sa, "-i", probe, "-i", sc,
                            "-filter_complex",
                            f"[1:a]aresample=48000,atrim=0:{la},asetpts=PTS-STARTPTS[a1];"
                            f"[2:a]aresample=48000,atrim=0:{lp},asetpts=PTS-STARTPTS,afade=t=out:st={lp - 0.6}:d=0.6,adelay={int(la * 1000)}|{int(la * 1000)}[a2];"
                            f"[3:a]aresample=48000,afade=t=in:d=0.6,adelay={int((la + lp - 0.6) * 1000)}|{int((la + lp - 0.6) * 1000)}[a3];"
                            "[a1][a2][a3]amix=inputs=3:normalize=0:duration=longest[a]",
                            "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p",
                            "-c:a", "aac", "-b:a", "192k", "-shortest", out], stdin=subprocess.PIPE)
    for seq in (A, P, C):
        for f in seq:
            enc.stdin.write(f.tobytes())
    enc.stdin.close()
    enc.wait()
    print("DONE", out, "frames", len(A) + len(P) + len(C), "probe+join at", la, "s, S6 at", la + lp, "s")


if __name__ == "__main__":
    main()
