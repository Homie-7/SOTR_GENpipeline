"""S9 RAFT b10 KNIFE FLASHES v1 (script, 0 cr, Homie F36 2026-11-25).

Homie (F34 + F36, verbatim in docs/BRIEF-F31-CANNONBALL-BLADES.md): four separate ALPHA files, one per lightning flash,
which he triggers by hand in QLab with sounds (his explicit exception to the final-product rule for this cue). Arms and
blades only, the ship's people (soldier, sailor), not zombie-like. "Silhouettes hidden in lightning": DARK arm + blade
silhouettes in front of a soft cold blue-grey cloud glow that flickers like lightning, like blades_anim_v1. They start
far (F1, F2 small at their corners) and come close (F4 large). No light spot on F3 (his "E3").

Sources: the four approved-for-test stills in 04_WORKING_FILES/S9_raft/knife_sf_v2/ (2752x1536, lit arm on black).
Per still: arm mask (luma threshold + morphology; keep the components that touch the frame edge; an explicit exclusion
removes the F3 top light spot), filled near-black, a thin cold rim on the top (light) side, a faint blade glint from the
still's own steel highlights. Behind: a procedural cold cloud pool (blade_anim MOON colour, smoke noise) that the
silhouette blocks. Envelope ~1.5 s: 2-3 flicker peaks in (60-120 ms), a hold ~0.4 s, a fall to fully transparent.
First and last frames are fully transparent (alpha 0), so QLab can fire it at any time. Small push-in inside each file.

Outputs (OUT_DIR):
  S9_b10_KNIFE_F<n>_flash_{VER}_ALPHA_3600x2160.mov / _1800x1080.mov   ProRes 4444 + straight alpha, 24 fps, no sound
  S9_b10_KNIFE_flashes_review_v1.mp4   the four in order over 18% grey (left) and over the raft water (right), 1920x1080
  _sheet_v1.jpg  peak frame of each flash, over grey;  _masks_v1.jpg  the four masks
Usage: python tools/knife_flash.py OUT_DIR [--masks]     (--masks writes the mask sheet only)
Run with CPU affinity FFFF3FFF (off Core 7). Writes _tmp_ names, renamed when ffmpeg finishes. Prints DONE.
"""
import os, subprocess, sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blade_frames as bf

SRC = r"D:\SOTR\SOTR_MEDIA\04_WORKING_FILES\S9_raft\knife_sf_v2"
RAFT = r"D:\SOTR\SOTR_MEDIA\01_FINAL_FOR_SHOW\1_PLAY_THESE_IN_ORDER\S09_the-Aftermath\S9_b1-and-b10_FLOOR_raft-water.mov"
FPS = 24
W4, H4 = 3600, 2160                     # CENTRE wall raster at 4K (true scale 6 px/cm); 1800x1080 is the 1080 copy
MOON = np.array([0.62, 0.50, 0.40], np.float32); MOON /= MOON.max()     # BGR, blade_anim's cold moonlight
ICE = np.array([1.0, 0.93, 0.86], np.float32)                           # BGR, rim + glint

# name, file, scale on the canvas, anchor (source point -> canvas point, in 0..1), softness px@4K, exclusions, seed
FLASHES = [
    dict(n=1, f="S9-RAFT-KNIFE-SF_v2_F1_e4c28176.png", s=0.55, a=(0.0, 0.0), soft=3.0, excl=[], close=15, seed=11),
    dict(n=2, f="S9-RAFT-KNIFE-SF_v2_F2_9a60dd1c.png", s=0.55, a=(1.0, 0.0), soft=3.0, excl=[], close=15, seed=12),
    dict(n=3, f="S9-RAFT-KNIFE-SF_v2_F3_bc2fbe19.png", s=0.80, a=(0.5, 0.0), soft=1.6,
         excl=[(0.505, 0.0, 0.215, 0.205, 9.0), (0.50, 0.0, 0.29, 0.32, 0.35)], close=15, seed=13),          # the F3 top light spot ("E3"): ellipse cx, cy, rx, ry
    dict(n=4, f="S9-RAFT-KNIFE-SF_v2b_F4_fd1a7c13.png", s=1.00, a=(0.5, 0.0), soft=0.0, excl=[], close=101, close2=31, fill_at=[(0.717, 0.389), (0.643, 0.389)], seed=14),   # F4 holes = shadow under the forearm (F39 look), filled
]
DUR = 1.5
N = int(round(DUR * FPS))               # 36 frames
V2 = "--v2" in sys.argv                 # Homie F38: solid (no holes), darker, edges dissolve before the frame, subtle arm motion
VER = "v2" if V2 else "v1"
# v2 per flash: limbs = (x split in canvas 0..1 or None, pivot in canvas 0..1, rotate deg, drop as a fraction of H)
# the rotation turns each arm about its entry point so the blade comes DOWN (a slow stab between the flashes)
LIMBS = {1: [(None, (0.0, 0.0), -2.2, 0.025)],
         2: [(None, (1.0, 0.0), 2.2, 0.025)],
         3: [((0.0, 0.47), (0.0, 0.05), -1.6, 0.020), ((0.47, 1.0), (1.0, 0.0), 1.8, 0.028)],
         4: [(None, (0.65, 0.0), 1.5, 0.035)]}
PUSH = 0.04                             # push-in over the file


def envelope(t):
    """Lightning: three sharp peaks in, a flickering hold, then a fall to exactly 0. Sub-frame averaged."""
    def raw(x):
        v = 0.0
        for c, w, a in ((0.10, 0.035, 1.00), (0.27, 0.025, 0.55), (0.44, 0.05, 0.95)):
            v = max(v, a * np.exp(-0.5 * ((x - c) / w) ** 2))
        if 0.44 <= x < 0.95:                                   # hold ~0.4 s with a small shimmer
            v = max(v, 0.62 + 0.06 * np.sin(x * 47) + 0.04 * np.sin(x * 113))
        elif x >= 0.95:                                        # fall
            u = min(1, (x - 0.95) / 0.45)
            v = max(v, 0.62 * (1 - u) ** 2 * (1 + 0.15 * np.sin(x * 61)))
        return v
    if t <= 0 or t >= (N - 1) / FPS:
        return 0.0
    return float(np.mean([raw(t + o / FPS) for o in (-0.375, -0.125, 0.125, 0.375)]))


KEEP_HOLE = 0.003                       # v2: an enclosed hole of >= 0.3% of the frame is a REAL gap (the sabre knuckle-bow); lace holes are < 0.05%
HOLES = []                              # v2 report: (frac, cx, cy, kept) per enclosed hole, filled by arm_mask


def arm_mask(img, excl, close=15, close2=None, fill_at=()):
    h, w = img.shape[:2]
    f = img.astype(np.float32) / 255
    luma = cv2.GaussianBlur(f.max(axis=2), (0, 0), 2.0)
    m = (luma > 0.10).astype(np.uint8)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    for cx, cy, rx, ry, lo in excl:          # inside the ellipse a pixel must be brighter than lo (9 = drop all)
        inside = (((xx / w - cx) / rx) ** 2 + ((yy / h - cy) / ry) ** 2) < 1
        m[inside & (luma < lo)] = 0
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    keep = np.zeros_like(m)
    for i in range(1, n):
        x, y, bw, bh, area = st[i]
        edge = x <= 2 or y <= 2 or x + bw >= w - 2 or y + bh >= h - 2
        if area > 0.002 * h * w and (edge or area > 0.01 * h * w):
            keep[lab == i] = 1
    # fill holes (gaps between fingers and guard)
    # pad with a background ring, flood the outside; background not reached is a hole (small ones only)
    inv = np.pad(1 - keep, 1, constant_values=1).astype(np.uint8)
    cv2.floodFill(inv, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 2)
    holes = (inv[1:-1, 1:-1] == 1).astype(np.uint8)
    n2, lab2, st2, _ = cv2.connectedComponentsWithStats(holes, 8)
    for i in range(1, n2):
        if st2[i][4] < (0.0005 if V2 else 0.02) * h * w:     # v2: only lace holes here; the v2 block below decides the rest
            keep[lab2 == i] = 1
    if V2:
        # v2 (Homie F38 "holes in the silhouette"): a wider close joins blade to guard and sleeve to sleeve, then EVERY
        # enclosed hole is filled (no size limit), then the outline is smoothed (blur + threshold) so no lace of holes stays
        # F39 fix: holes >= KEEP_HOLE stay open (the F1/F3 sabre knuckle-bow), unless listed in fill_at (a shadow, not a gap)
        k2 = close2 if close2 else max(close, 31)
        keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k2, k2)))

        def fill_small(keep, log):
            inv = np.pad(1 - keep, 1, constant_values=1).astype(np.uint8)
            cv2.floodFill(inv, np.zeros((h + 4, w + 4), np.uint8), (0, 0), 2)
            n3, lab3, st3, cen3 = cv2.connectedComponentsWithStats((inv[1:-1, 1:-1] == 1).astype(np.uint8), 8)
            for i in range(1, n3):
                fr = st3[i][4] / (h * w); cx, cy = cen3[i][0] / w, cen3[i][1] / h
                forced = any(abs(cx - fx) < 0.04 and abs(cy - fy) < 0.04 for fx, fy in fill_at)
                kept = fr >= KEEP_HOLE and not forced
                if not kept:
                    keep[lab3 == i] = 1
                if log and fr > 0.0005:
                    HOLES.append((round(fr * 100, 3), round(cx, 3), round(cy, 3), kept))
            return keep
        keep = fill_small(keep, False)
        keep = (cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 4.0) > 0.5).astype(np.uint8)
        keep = fill_small(keep, True)
    sm = cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 1.2)
    # glint: the still's own steel highlights (bright, low saturation) inside the mask
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32) / 255
    glint = np.clip((hsv[..., 2] - 0.45) / 0.4, 0, 1) * np.clip(1 - hsv[..., 1] / 0.35, 0, 1) * sm
    if V2:   # darker (Homie F38 "we still see a lot of clarity"): only the brightest steel keeps a faint glint, no cloth
        glint = np.clip((hsv[..., 2] - 0.80) / 0.2, 0, 1) * np.clip(1 - hsv[..., 1] / 0.12, 0, 1) * sm
    return sm, glint


def place(layer, fl, k, extra=None):
    """Source layer -> 4K canvas: cover-fit, then the flash scale (times push-in k) about its anchor; extra = a 2x3
    canvas-space affine applied after (v2 limb motion)."""
    h, w = layer.shape[:2]
    cover = max(W4 / w, H4 / h)
    s = cover * fl["s"] * k
    ax, ay = fl["a"]
    # source anchor point -> canvas anchor point
    sx, sy = ax * w, ay * h
    cx, cy = ax * W4, ay * H4
    M = np.float32([[s, 0, cx - s * sx], [0, s, cy - s * sy]])
    if extra is not None:
        M = (np.vstack([extra, [0, 0, 1]]) @ np.vstack([M, [0, 0, 1]]))[:2].astype(np.float32)
    return cv2.warpAffine(layer, M, (W4, H4), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)


class Flash:
    def __init__(self, fl):
        self.fl = fl
        img = cv2.imread(os.path.join(SRC, fl["f"]))
        self.mask, self.glint = arm_mask(img, fl["excl"], fl["close"], fl.get("close2"), fl.get("fill_at", ()))
        self.smoke = bf.smoke(W4 // 4 + 200, H4 // 4, fl["seed"], 40)
        yy, xx = np.mgrid[0:H4, 0:W4].astype(np.float32)
        self.yy, self.xx = yy, xx
        if V2:
            # edge dissolve (Homie F38): nothing touches any frame edge; a smoke-broken soft falloff on all four sides,
            # so no wall's flash runs into its neighbour. Margins: sides 14% of W, top 9% of H, bottom 12% of H.
            nz = cv2.resize(bf.smoke(W4 // 8, H4 // 8, fl["seed"] + 100, 20), (W4, H4))
            nz = (nz - nz.mean()) / (nz.std() + 1e-6)
            def ramp(d, m):
                u = np.clip(d / m + 0.18 * nz, 0, 1) * np.clip(d / (0.3 * m), 0, 1)   # F39: the noise may not lift the very edge off 0
                return u * u * (3 - 2 * u)
            self.vig = (ramp(xx, 0.14 * W4) * ramp(W4 - 1 - xx, 0.14 * W4) * ramp(yy, 0.09 * H4)
                        * ramp(H4 - 1 - yy, 0.12 * H4)).astype(np.float32)

    def motion(self, f):
        """v2: per-limb affines at frame f. Eased slow stab (rotate about the entry point + drop) plus a small tremor."""
        u = f / (N - 1)
        e = u * u * (3 - 2 * u)
        out = []
        for i, (split, piv, rot, drop) in enumerate(LIMBS[self.fl["n"]]):
            trem = 0.08 * np.sin(2 * np.pi * (2.3 + 0.7 * i) * u + i)
            a = np.deg2rad(rot * (e + trem))
            px, py = piv[0] * W4, piv[1] * H4
            c, sn = np.cos(a), np.sin(a)
            R = np.float32([[c, -sn, px - c * px + sn * py], [sn, c, py - sn * px - c * py]])
            R[1, 2] += drop * H4 * (e - 0.5)
            out.append((split, R))
        return out

    def frame(self, f):
        t = f / FPS
        L = envelope(t)
        k = 1 + PUSH * (f / (N - 1))
        if V2:
            sil = np.zeros((H4, W4), np.float32); gl = np.zeros((H4, W4), np.float32)
            for split, R in self.motion(f):
                ms, gs = self.mask, self.glint
                if split is not None:     # cut the source at the canvas x split (before motion) so each arm moves alone
                    cut = place(np.ones_like(self.mask), self.fl, k)
                    xs = (self.xx[0] >= split[0] * W4) & (self.xx[0] < split[1] * W4)
                    part = (cut * xs[None, :]).astype(np.float32)
                    sil = np.maximum(sil, cv2.warpAffine(place(self.mask, self.fl, k) * part, R, (W4, H4)))
                    gl = np.maximum(gl, cv2.warpAffine(place(self.glint, self.fl, k) * part, R, (W4, H4)))
                else:
                    sil = np.maximum(sil, place(ms, self.fl, k, R)); gl = np.maximum(gl, place(gs, self.fl, k, R))
        else:
            sil = place(self.mask, self.fl, k)
            gl = place(self.glint, self.fl, k)
        if self.fl["soft"] > 0:
            sil = cv2.GaussianBlur(sil, (0, 0), self.fl["soft"])
            gl = cv2.GaussianBlur(gl, (0, 0), self.fl["soft"])
        # the cloud pool sits behind the arm: centre of the silhouette's mass, pulled toward the wall centre
        m = cv2.moments(cv2.resize(sil, (W4 // 8, H4 // 8)))
        if m["m00"] > 0:
            px, py = m["m10"] / m["m00"] * 8, m["m01"] / m["m00"] * 8
        else:
            px, py = W4 / 2, H4 / 2
        px, py = 0.7 * px + 0.3 * W4 / 2, 0.7 * py + 0.3 * H4 * 0.45
        rx = (0.30 + 0.35 * self.fl["s"]) * W4
        d = np.sqrt(((self.xx - px) / rx) ** 2 + ((self.yy - py) / (rx * 0.75)) ** 2)
        off = int(t * 30)
        sm = cv2.resize(self.smoke[:, off:off + W4 // 4], (W4, H4), interpolation=cv2.INTER_LINEAR)
        pool = np.clip(1.05 - d, 0, 1) ** 1.5 * np.clip(0.75 + 0.35 * sm, 0.2, 1.3)
        pool = np.clip(pool, 0, 1)
        # rim: the light is high above, so the top edges of the arm catch it
        dd = 5
        rim = np.clip(sil - np.roll(sil, dd, axis=0), 0, 1)
        rim = cv2.GaussianBlur(rim, (0, 0), 1.5) * (0.5 + 0.5 * np.clip(pool * 1.6, 0, 1))
        if V2:
            rim *= 0.45                                        # darker silhouette: a thinner, dimmer rim
        Lp = 0.55 * L                                          # pool brightness at peak (soft, not a white-out)
        P = (Lp * pool * (1 - (1.0 if V2 else 0.97) * sil))[..., None] * MOON
        P += (np.clip(0.65 * rim * L + 0.35 * gl * L ** 1.5, 0, 1))[..., None] * ICE
        A = np.maximum(np.clip(pool * min(1, 1.6 * L), 0, 1), sil * min(1, 1.8 * L))
        A = np.maximum(A, np.clip(rim * 1.5 * L, 0, 1))
        if V2:
            P *= self.vig[..., None]; A *= self.vig
        if f == 0 or f == N - 1:
            A[:] = 0; P[:] = 0
        return np.clip(P, 0, 1), np.clip(A, 0, 1)


def enc(path, w, h):
    return subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba64le", "-s", f"{w}x{h}",
                             "-r", str(FPS), "-i", "-", "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt",
                             "yuva444p10le", "-alpha_bits", "16", "-vendor", "apl0", path], stdin=subprocess.PIPE)


def straight_rgba(P, A):
    s = np.where(A[..., None] > 1e-4, P / np.maximum(A[..., None], 1e-4), 0)
    return (np.clip(np.dstack([s[..., 2], s[..., 1], s[..., 0], A]), 0, 1) * 65535).astype("<u2").tobytes()


def raft_bg():
    cap = cv2.VideoCapture(RAFT)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 200)
    ok, fr = cap.read()
    if not ok:
        return np.full((540, 900, 3), 0.05, np.float32)
    return cv2.resize(fr, (900, 540), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


def review_frame(P, A, raft, label, t):
    img = np.zeros((1080, 1920, 3), np.float32)
    p = cv2.resize(P, (900, 540), interpolation=cv2.INTER_AREA); a = cv2.resize(A, (900, 540))[..., None]
    grey = np.full((540, 900, 3), 0.18, np.float32)
    img[270:810, 40:940] = p + grey * (1 - a)
    img[270:810, 980:1880] = p + raft * (1 - a)
    for x, s in ((40, "over 18% grey"), (980, "over the raft water (context only)")):
        cv2.putText(img, s, (x, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0.6, 0.6, 0.6), 1, cv2.LINE_AA)
    cv2.putText(img, "S9 b10 RAFT  KNIFE FLASHES " + VER + "  (script, 0 cr; 4 alpha files for QLab; CENTRE 5:3)", (40, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0.75, 0.75, 0.75), 1, cv2.LINE_AA)
    cv2.putText(img, label, (40, 880), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0.8, 0.8, 0.8), 1, cv2.LINE_AA)
    cv2.putText(img, f"{t:4.2f} s", (1760, 880), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0.6, 0.6, 0.6), 1, cv2.LINE_AA)
    return (np.clip(img, 0, 1) * 255).astype(np.uint8)


LABELS = {1: "F1  soldier arm, far, upper LEFT", 2: "F2  sailor arm, far, upper RIGHT",
          3: "F3  both arms, closer", 4: "F4  one arm, close (the murder)"}


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    if "--masks" in sys.argv:
        tiles = []
        for fl in FLASHES:
            img = cv2.imread(os.path.join(SRC, fl["f"]))
            m, g = arm_mask(img, fl["excl"], fl["close"], fl.get("close2"), fl.get("fill_at", ()))
            v = (np.dstack([m, m, m]) * 0.6 + np.dstack([g, g, g]) * 0.4)
            tiles.append(cv2.resize((v * 255).astype(np.uint8), (960, 536)))
        cv2.imwrite(os.path.join(out, f"_masks_{VER}.jpg"), np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])]))
        print("DONE masks"); return
    raft = raft_bg()
    rv_path = os.path.join(out, f"S9_b10_KNIFE_flashes_review_{VER}.mp4")
    rv = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt",
                           "yuv420p", "-movflags", "+faststart", os.path.join(out, "_tmp_" + os.path.basename(rv_path))],
                          stdin=subprocess.PIPE)
    sheet, stats = [], []
    for fl in FLASHES:
        fx = Flash(fl)
        names = {r: os.path.join(out, f"S9_b10_KNIFE_F{fl['n']}_flash_{VER}_ALPHA_{r}.mov") for r in ("3600x2160", "1800x1080")}
        p4 = enc(os.path.join(out, "_tmp_" + os.path.basename(names["3600x2160"])), W4, H4)
        p1 = enc(os.path.join(out, "_tmp_" + os.path.basename(names["1800x1080"])), 1800, 1080)
        best, bestL = None, -1
        for f in range(N):
            P, A = fx.frame(f)
            p4.stdin.write(straight_rgba(P, A))
            P1 = cv2.resize(P, (1800, 1080), interpolation=cv2.INTER_AREA)
            A1 = cv2.resize(A, (1800, 1080), interpolation=cv2.INTER_AREA)
            p1.stdin.write(straight_rgba(P1, A1))
            rv.stdin.write(review_frame(P1, A1, raft, LABELS[fl["n"]], f / FPS).tobytes())
            L = envelope(f / FPS)
            stats.append(f"F{fl['n']} f{f:02d} t={f / FPS:4.2f} L={L:.3f} alpha_max={A.max():.3f}")
            if L > bestL and f > 12:
                bestL, best = L, review_frame(P1, A1, raft, LABELS[fl["n"]], f / FPS)[270:810, 40:940]
        for f in range(12):                                   # a short black gap between flashes in the review
            rv.stdin.write(np.zeros((1080, 1920, 3), np.uint8).tobytes())
        for p, k in ((p4, "3600x2160"), (p1, "1800x1080")):
            p.stdin.close(); p.wait()
            if p.returncode != 0:
                print("ffmpeg failed", fl["n"], k); sys.exit(1)
            os.replace(os.path.join(out, "_tmp_" + os.path.basename(names[k])), names[k])
        sheet.append(best)
        print(f"F{fl['n']} done", flush=True)
    rv.stdin.close(); rv.wait()
    os.replace(os.path.join(out, "_tmp_" + os.path.basename(rv_path)), rv_path)
    cv2.imwrite(os.path.join(out, f"_sheet_{VER}.jpg"), np.vstack([np.hstack(sheet[:2]), np.hstack(sheet[2:])]))
    with open(os.path.join(out, f"_envelope_{VER}.txt"), "w") as fh:
        fh.write("\n".join(stats) + "\n")
    print("DONE", 4 * N, "frames")


if __name__ == "__main__":
    main()
