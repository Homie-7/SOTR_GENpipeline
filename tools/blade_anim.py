"""S9 RAFT b10 blade shadows, ANIMATED test v1 (script, 0 cr, Homie 2026-11-22).

Homie's direction (docs/BRIEF-S9-RAFT.md, last section): stylised horror GLIMPSES. An arm holding a period blade comes
out of the dark. Randomised, one or two screens at a time, never all three. The walls stay dark (the light is on Agnes
and the water); only the glimpse is lit, by a cold moon pool and an edge glint. They close in from different walls in
turn, then sudden attacks: stabs ganging up, back to back. Then the script's four still images (four stabs), blackness.

Blades from tools/blade_frames.py (1816-correct: briquet An XI, naval dirk, boarding sabre An IX, clasp knife, loose
socket bayonet). Walls at true scale, 3 px per cm (3.6 m = 1080 px): LEFT 1440x1080, CENTRE 1800x1080, RIGHT 1440x1080.

Outputs (OUT_DIR):
  S9_b10_BLADES_<WALL>_anim_v1_ALPHA.mov   ProRes 4444 + alpha (straight), one per wall, no sound
  S9_b10_BLADES_3wall_review_v1.mp4         1920x1080 side-by-side review over black (H.264)
Usage: python tools/blade_anim.py OUT_DIR [--seed N] [--stills t1,t2,...]   (--stills writes PNG review frames only)
Heavy: run with CPU affinity FFFF3FFF (off Core 7). Writes _tmp_ names, renamed when ffmpeg finishes. Prints DONE.
"""
import math, os, subprocess, sys
import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import blade_frames as bf

FPS, DUR = 24, 28.0
N = int(FPS * DUR)
WALLS = {"LEFT": (1440, 1080), "CENTRE": (1800, 1080), "RIGHT": (1440, 1080)}
ORDER = ("LEFT", "CENTRE", "RIGHT")
PXCM = 3.0
SS = 2
MOON = np.array([0.62, 0.50, 0.40], np.float32); MOON /= MOON.max()     # BGR, the water's cold moonlight
ICE = np.array([1.0, 0.93, 0.86], np.float32)                           # BGR, edge glint
POOL_PEAK = 0.30
KSCALE = 1.45                                                            # v1 test: glimpses read bigger                                                         # walls stay dark: the pool is dim
BLADES = {"briquet": bf.briquet, "dirk": bf.dirk, "sabre": bf.boarding_sabre, "knife": bf.clasp_knife,
          "bayonet": bf.bayonet}


def ease(u):
    u = np.clip(u, 0, 1); return u * u * (3 - 2 * u)


# ---------------------------------------------------------------- schedule
def entry_geometry(wall, rng):
    """Shoulder S off-frame on the wall's outer side / top; hit point F inside, toward the stage centre and down."""
    W, H = WALLS[wall]
    if wall == "CENTRE":
        side = rng.choice(["top", "tl", "tr", "bl", "br"])
        S = {"top": (rng.uniform(0.2, 0.8) * W, -0.55 * H), "tl": (-0.3 * W, rng.uniform(-0.3, 0.3) * H),
             "tr": (1.3 * W, rng.uniform(-0.3, 0.3) * H), "bl": (-0.25 * W, 1.25 * H), "br": (1.25 * W, 1.25 * H)}[side]
        F = (rng.uniform(0.32, 0.68) * W, rng.uniform(0.40, 0.80) * H)
    else:
        side = rng.choice(["out", "out", "top", "low"])
        S = {"out": (-0.4 * W, rng.uniform(-0.3, 0.5) * H), "top": (rng.uniform(0.0, 0.45) * W, -0.55 * H),
             "low": (-0.35 * W, 1.3 * H)}[side]
        F = (rng.uniform(0.45, 0.82) * W, rng.uniform(0.35, 0.82) * H)
        if wall == "RIGHT":
            S = (W - S[0], S[1]); F = (W - F[0], F[1])
    S, F = np.array(S, float), np.array(F, float)
    # where the line S->F enters the frame: the fist starts there (hidden in the dark at the edge)
    for f in np.linspace(0, 1, 400):
        p = S + (F - S) * f
        if 0 <= p[0] <= W and 0 <= p[1] <= H:
            break
    return S, F, p + (F - S) * 0.03


def make_event(wall, t0, dur, kind, k, depth, rng, blade=None):
    S, F, E0 = entry_geometry(wall, rng)
    k *= KSCALE
    return dict(wall=wall, t0=t0, t1=t0 + dur, kind=kind, k=k, S=S, Fhit=F, Fout=E0, depth=depth,
                blade=blade or rng.choice(list(BLADES)), bend=rng.uniform(-28, 28), flip=bool(rng.random() < 0.5),
                wob=rng.uniform(0, 6.28), seed=int(rng.integers(1e6)))


def active_walls(events, a, b):
    return {e["wall"] for e in events if e["t0"] < b and e["t1"] > a}


def schedule(seed):
    rng = np.random.default_rng(seed)
    ev = []
    # 1) THEY CLOSE IN: one wall at a time, each glimpse a little bigger and deeper; overlaps start near the end
    phaseA = [("RIGHT", 1.5, 1.8, 1.5, .18), ("LEFT", 3.9, 1.7, 1.7, .25), ("CENTRE", 6.0, 1.5, 1.9, .32),
              ("RIGHT", 7.9, 1.3, 2.1, .40), ("LEFT", 9.4, 1.2, 2.3, .48), ("CENTRE", 10.8, 1.1, 2.5, .55),
              ("RIGHT", 11.4, 1.0, 2.5, .60), ("LEFT", 12.4, 0.9, 2.6, .65)]
    for w, t0, d, k, dep in phaseA:
        ev.append(make_event(w, t0, d, "emerge", k, dep, rng))
    # 2) SUDDEN ATTACKS: stabs, back to back, two walls at once or two arms ganging on one wall; never 3 walls lit
    t, T1 = 13.4, 23.0
    while t < T1:
        p = (t - 13.4) / (T1 - 13.4)
        dur = 0.62 - 0.2 * p + rng.uniform(-0.05, 0.05)
        k = 2.6 + 1.1 * p + rng.uniform(-0.2, 0.2)
        busy = active_walls(ev, t, t + dur)
        free = [w for w in ORDER if len(busy | {w}) <= 2]
        r = rng.random()
        if r < 0.30 and len(free) >= 2 and len(busy | set(free[:2])) <= 2:
            ws = list(rng.choice(free, 2, replace=False)); offs = [0, rng.uniform(0.0, 0.12)]
        elif r < 0.52 and free:
            w = rng.choice(free); ws = [w, w]; offs = [0, rng.uniform(0.08, 0.18)]      # ganging: 2 arms, 1 wall
        else:
            ws = [rng.choice(free)] if free else [rng.choice(list(busy))]; offs = [0]
        for w, o in zip(ws, offs):
            ev.append(make_event(w, t + o, dur, "stab", k, 1.0, rng))
        t += dur * rng.uniform(0.55, 0.9) + max(0.0, 0.35 - 0.35 * p) * rng.uniform(0.3, 1.0)
    # 3) FOUR STILL IMAGES = four stabs (script), the four executioners' blades; hard cuts, then blackness
    t = 23.6
    for w, b, k in (("CENTRE", "briquet", 3.4), ("LEFT", "knife", 4.6), ("RIGHT", "dirk", 3.8), ("CENTRE", "sabre", 3.9)):
        ev.append(make_event(w, t, 0.55, "still", k, 1.0, rng, blade=b)); t += 0.55 + 0.22
    return ev


# ---------------------------------------------------------------- pose + light
def pose(e, t):
    """Fist position, blade angle (deg), pool light L, glint G."""
    u = (t - e["t0"]) / (e["t1"] - e["t0"])
    S, Fh, Fo = e["S"], e["Fhit"], e["Fout"]
    d = Fh - S; base = math.degrees(math.atan2(d[1], d[0]))
    rng_w = math.sin(t * 7.3 + e["wob"]) * 0.5 + math.sin(t * 13.1 + 2 * e["wob"]) * 0.5
    if e["kind"] == "emerge":
        Fin = Fo + (Fh - Fo) * e["depth"]
        if u < 0.45:   F = Fo + (Fin - Fo) * ease(u / 0.45)
        elif u < 0.75: F = Fin + (Fh - S) / np.linalg.norm(Fh - S) * 6 * rng_w
        else:          F = Fin + (Fo - Fin) * ease((u - 0.75) / 0.25) ** 0.7
        fl = 0.75 + 0.25 * math.sin(t * 31 + e["wob"]) * math.sin(t * 11.7)          # moon through cloud
        L = ease(u / 0.3) * (1 - ease((u - 0.78) / 0.22)) * fl
        G = 0.35 * L * (0.6 + 0.4 * math.sin(t * 9 + e["wob"]))
        ang = base + e["bend"] + 4 * rng_w
    elif e["kind"] == "stab":
        back = Fo + (Fh - Fo) * 0.35 - (Fh - S) / np.linalg.norm(Fh - S) * 40 * e["k"]
        if u < 0.35:   F = Fo + (back - Fo) * ease(u / 0.35)                         # wind-up out of the dark
        elif u < 0.47: F = back + (Fh - back) * ((u - 0.35) / 0.12) ** 2.2           # the thrust, accelerating
        elif u < 0.72: F = Fh + (Fh - S) / np.linalg.norm(Fh - S) * 8 * math.exp(-(u - 0.47) * 30)  # jolt on impact
        else:          F = Fh + (Fo - Fh) * ease((u - 0.72) / 0.28)
        L = (0.45 if u < 0.30 else 1.0) * (0 if u < 0.08 or u > 0.96 else 1)
        if 0.47 <= u < 0.6: L *= 1.25                                                 # flash on the hit
        G = 1.0 if 0.44 < u < 0.62 else 0.3 * L
        ang = base + e["bend"] * (1 - ease((u - 0.3) / 0.2))
    else:                                                                             # still image
        F, L, G, ang = Fh, 1.15, 1.0, base + e["bend"] * 0.3
    return np.asarray(F, float), ang, L, G


def arm_polys(e, F, ang):
    """Stylised arm: one tapered, slightly bent limb from the off-frame shoulder to the fist, torn sleeve, fist."""
    S, k = e["S"], e["k"] * PXCM
    v = F - S; Lv = np.linalg.norm(v); n = np.array([-v[1], v[0]]) / (Lv + 1e-6)
    bend = (1 if e["flip"] else -1) * 0.12 * Lv
    C = (S + F) / 2 + n * bend
    ts = np.linspace(0, 1, 48)
    P = ((1 - ts) ** 2)[:, None] * S + (2 * (1 - ts) * ts)[:, None] * C + (ts ** 2)[:, None] * F
    tang = np.gradient(P, axis=0); tang /= np.linalg.norm(tang, axis=1, keepdims=True) + 1e-9
    nor = np.stack([-tang[:, 1], tang[:, 0]], 1)
    wcm = np.interp(ts, [0, 0.55, 0.85, 1.0], [13, 11, 7.5, 6.5])
    r = np.random.default_rng(e["seed"])
    rag = np.where((ts > 0.5) & (ts < 0.7), r.uniform(0, 3.5, ts.size), 0)          # the torn sleeve edge
    w = (wcm + rag) * k / 2
    poly = np.vstack([P + nor * w[:, None], (P - nor * w[:, None])[::-1]])
    a = math.radians(ang)
    fist = bf.ellipse_pts(F[0], F[1], 6.0 * k, 5.0 * k)
    thumb = bf.ellipse_pts(F[0] + math.cos(a + 1.2) * 4 * k, F[1] + math.sin(a + 1.2) * 4 * k, 2.6 * k, 1.9 * k)
    return [poly, fist, thumb]


def blade_polys(e, F, ang):
    shapes = [s + np.array([5.5, 0.0]) for s in BLADES[e["blade"]]()]                # grip centre on the fist
    return bf.place(shapes, F[0], F[1], e["k"] * PXCM, ang, flip=e["flip"])


def raster(polys, W, H):
    m = np.zeros((H * SS, W * SS), np.uint8)
    for p in polys:
        q = np.clip(np.round(p * SS), -30000, 30000).astype(np.int32)
        cv2.fillPoly(m, [q], 255, cv2.LINE_AA)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


class Wall:
    def __init__(self, name, seed):
        self.name = name; self.W, self.H = WALLS[name]
        self.yy, self.xx = np.mgrid[0:self.H, 0:self.W].astype(np.float32)
        self.smoke = bf.smoke(self.W * 2, self.H, seed, self.W / 14)

    def frame(self, events, t):
        W, H = self.W, self.H
        sil = np.zeros((H, W), np.float32); asil = sil.copy(); pool = sil.copy(); rim = sil.copy()
        off = int(t * 40) % W; sm = self.smoke[:, off:off + W]           # no wrap seam
        for e in events:
            if not (e["t0"] <= t < e["t1"]):
                continue
            subs = [0.0]
            u = (t - e["t0"]) / (e["t1"] - e["t0"])
            if e["kind"] == "stab" and 0.33 < u < 0.5:
                subs = [-0.33 / FPS, 0.0, 0.33 / FPS]                                # motion blur on the thrust
            ms, bl = [], None
            for o in subs:
                F, ang, L, G = pose(e, t + o)
                b = raster(blade_polys(e, F, ang), W, H)
                a = raster(arm_polys(e, F, ang), W, H)
                ms.append(np.maximum(a, b))
                if o == 0.0: bl, armm, F0, L0, G0 = b, a, F, L, G
            m = cv2.GaussianBlur(sum(ms) / len(ms), (0, 0), 0.8 + 0.3 * e["k"])
            dist = np.sqrt((self.xx - F0[0]) ** 2 + (self.yy - F0[1]) ** 2)
            near = np.exp(-dist / (55 * e["k"] * PXCM))                               # the arm dies into the dark
            sil = np.maximum(sil, m)
            asil = np.maximum(asil, m * np.clip(L0, 0, 1) * np.clip(0.25 + near, 0, 1))
            rx = 62 * e["k"] * PXCM
            d = np.sqrt(((self.xx - F0[0]) / rx) ** 2 + ((self.yy - F0[1]) / (rx * 0.8)) ** 2)
            pool += np.clip(1.08 - d, 0, 1) ** 1.6 * (0.8 + 0.2 * sm) * L0
            dd = max(2, int(e["k"]))
            rb = np.clip(bl - np.roll(bl, dd, axis=0), 0, 1)                         # moon from above: top edge
            ra = np.clip(armm - np.roll(armm, dd + 1, axis=0), 0, 1) * near
            rim = np.maximum(rim, cv2.GaussianBlur(rb * G0 + ra * 0.30 * L0, (0, 0), 1.0))
        pool = np.clip(pool, 0, 1.25)
        P = (POOL_PEAK * pool * (1 - 0.97 * sil))[..., None] * MOON + (0.85 * rim)[..., None] * ICE
        A = np.clip(np.maximum.reduce([np.clip(pool, 0, 1), asil, np.clip(rim * 1.5, 0, 1)]), 0, 1)
        return np.clip(P, 0, 1), A


# ---------------------------------------------------------------- output
GAP = 40
SC = 1920 / (sum(WALLS[w][0] for w in ORDER) + 2 * GAP)


def phase_name(t):
    return ("1  THEY CLOSE IN (one wall at a time)" if t < 13.3 else "2  SUDDEN ATTACKS (back to back, ganging)"
            if t < 23.4 else "3  FOUR STABS (four still images)" if t < 26.7 else "BLACKNESS")


def review(frames, t):
    img = np.zeros((1080, 1920, 3), np.float32)
    sh = int(round(1080 * SC)); y0 = (1080 - sh) // 2; x = 0
    for w in ORDER:
        P = frames[w]; sw = int(round(WALLS[w][0] * SC))
        img[y0:y0 + sh, x:x + sw] = cv2.resize(P, (sw, sh), interpolation=cv2.INTER_AREA)
        cv2.rectangle(img, (x, y0), (x + sw - 1, y0 + sh - 1), (0.16, 0.16, 0.16), 1)
        cv2.putText(img, w, (x + 4, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0.55, 0.55, 0.55), 1, cv2.LINE_AA)
        x += sw + int(GAP * SC)
    cv2.putText(img, "S9 b10 RAFT  BLADES  animated test v1  (script, no sound; walls dark, light on Agnes + water)",
                (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0.7, 0.7, 0.7), 1, cv2.LINE_AA)
    cv2.putText(img, phase_name(t), (20, 1080 - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0.75, 0.75, 0.75), 1, cv2.LINE_AA)
    cv2.putText(img, f"{t:5.2f} s", (1920 - 140, 1080 - 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0.6, 0.6, 0.6), 1,
                cv2.LINE_AA)
    return (img * 255).astype(np.uint8)


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else 1816
    ev = schedule(seed)
    walls = {w: Wall(w, seed + i) for i, w in enumerate(ORDER)}
    byw = {w: [e for e in ev if e["wall"] == w] for w in ORDER}
    for f in range(N):                                                               # the rule: never 3 walls lit
        t = f / FPS
        assert len({e["wall"] for e in ev if e["t0"] <= t < e["t1"]}) <= 2, t
    if "--stills" in sys.argv:
        for t in map(float, sys.argv[sys.argv.index("--stills") + 1].split(",")):
            fr = {w: walls[w].frame(byw[w], t)[0] for w in ORDER}
            cv2.imwrite(os.path.join(out, f"_still_{t:05.2f}.png"), review(fr, t))
        print("DONE stills"); return
    procs, finals = {}, {}
    for w in ORDER:
        W, H = WALLS[w]
        finals[w] = os.path.join(out, f"S9_b10_BLADES_{w}_anim_v1_ALPHA.mov")
        procs[w] = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgba64le",
                                     "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "prores_ks", "-profile:v",
                                     "4444", "-pix_fmt", "yuva444p10le", "-alpha_bits", "16", "-vendor", "apl0",
                                     os.path.join(out, "_tmp_" + os.path.basename(finals[w]))], stdin=subprocess.PIPE)
    finals["review"] = os.path.join(out, "S9_b10_BLADES_3wall_review_v1.mp4")
    procs["review"] = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s",
                                        "1920x1080", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "16",
                                        "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                                        os.path.join(out, "_tmp_" + os.path.basename(finals["review"]))],
                                       stdin=subprocess.PIPE)
    for f in range(N):
        t = f / FPS
        fr = {}
        for w in ORDER:
            P, A = walls[w].frame(byw[w], t)
            fr[w] = P
            straight = np.where(A[..., None] > 1e-4, P / np.maximum(A[..., None], 1e-4), 0)
            rgba = np.dstack([straight[..., 2], straight[..., 1], straight[..., 0], A])
            procs[w].stdin.write((np.clip(rgba, 0, 1) * 65535).astype("<u2").tobytes())
        procs["review"].stdin.write(review(fr, t).tobytes())
        if f % 48 == 0:
            print(f"{f} / {N} frames", flush=True)
    for k, p in procs.items():
        p.stdin.close(); p.wait()
        if p.returncode != 0:
            print(f"ffmpeg failed for {k}"); sys.exit(1)
        os.replace(os.path.join(out, "_tmp_" + os.path.basename(finals[k])), finals[k])
    with open(os.path.join(out, "schedule_v1.txt"), "w") as fh:
        for e in sorted(ev, key=lambda e: e["t0"]):
            fh.write(f"{e['t0']:6.2f}-{e['t1']:6.2f}  {e['wall']:6s} {e['kind']:6s} {e['blade']:8s} k={e['k']:.2f}\n")
    print("DONE", N, "frames")


if __name__ == "__main__":
    main()
