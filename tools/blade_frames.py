"""S9 RAFT b10 dagger shadows: 3 style frames across LEFT / CENTRE / RIGHT (stills, 0 cr, Homie 2026-11-22).

Period blades from docs/RESEARCH-S9-RAFT-BLADES.md (1816-correct): infantry sabre-briquet An XI (D-guard),
loose socket bayonet 1777/An IX (offset elbow), boarding axe 1786 (rear spike), sailor's clasp knife.
Shapes are drawn in cm, cast as shadows into a cold moon wash. Walls at true aspect (STAGE.md):
LEFT 4:3, CENTRE 5:3, RIGHT 4:3.

  A  FOUR HANDS     the four executioners (3 sailors + 1 soldier), one blade each, raised; hard moon shadows
  B  THEY CLOSE IN  a crowd of arms and blades rising from the bottom and the outer edges toward CENTRE
  C  FANTASMAGORIE  1797-style shadow show: huge, soft, smoky blades swelling out of the dark

Homie 2026-11-22: sharp little daggers and sabres, suggestive only, in ALPHA to superimpose.
Outputs: style sheet over a moon wall + alpha/ RGBA PNGs per wall.
Usage: python tools/blade_frames.py OUT_DIR
"""
import math, os, sys
import cv2
import numpy as np

PXMM = 0.25                          # preview scale: 0.25 px per mm
WALLS = {"LEFT": (4800, 3600), "CENTRE": (6000, 3600), "RIGHT": (4800, 3600)}
SS = 3                               # supersample for clean edges
MOON = np.array([0.62, 0.50, 0.40], np.float32)     # BGR, cold moonlight on the wall (as the water)


def ellipse_pts(cx, cy, rx, ry, a0=0, a1=360, n=40):
    t = np.radians(np.linspace(a0, a1, n))
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], 1)


# ---- shapes in cm; the fist sits at (0,0); the blade points along +x; the arm leaves along -x/+y side
def briquet():
    xs = np.linspace(0, 59, 30)
    sag = 3.2 * (xs / 59) ** 2                              # slight even curve
    w = np.interp(xs, [0, 51, 59], [3.1, 2.8, 0.0])
    back = np.stack([xs, -sag - w / 2 * 0 - 1.4], 1)
    edge = np.stack([xs, -sag + w - 1.4], 1)
    back[-5:, 1] += np.linspace(0, 1.6, 5)                  # clipped "hatchet" point
    blade = np.vstack([back, edge[::-1]])
    grip = np.array([[-11, -1.6], [0, -1.6], [0, 1.6], [-11, 1.6]])
    # D-shaped knuckle bow round the outside of the fist, cross to pommel
    outer = ellipse_pts(-5.5, 4.2, 6.3, 4.6, 0, 180)
    inner = ellipse_pts(-5.5, 4.2, 5.4, 3.7, 0, 180)[::-1]
    bow = np.vstack([outer, inner])
    quillon = np.array([[0, -1.8], [0.8, -1.8], [0.8, -4.8], [0, -4.8]])
    ball = ellipse_pts(0.4, -5.3, 0.9, 0.9)
    return [blade, grip, bow, quillon, ball]


def bayonet():
    socket = np.array([[-9, -1.2], [0, -1.2], [0, 1.2], [-9, 1.2]])
    ring = np.array([[-6, -1.6], [-5, -1.6], [-5, 1.6], [-6, 1.6]])
    neck = np.array([[-0.6, -1.0], [0.8, -1.0], [1.6, -3.6], [0.4, -3.6]])   # the cranked elbow
    blade = np.array([[0.6, -3.0], [39, -3.9], [0.6, -4.9]])                 # long triangular spike, offset
    return [socket, ring, neck, blade]


def boarding_axe():
    haft = np.array([[-30, -1.5], [24, -1.4], [24, 1.4], [-30, 1.5]])
    head = np.array([[15, -1.6], [22, -1.6], [25, -9], [23.5, -14.5], [16.5, -15.5], [13.5, -10], [15.5, -6]])
    spike = np.array([[16, 1.5], [21, 1.5], [19.2, 11.5], [18.4, 12.2]])     # bec de corbin
    langet = np.array([[8, -1.8], [16, -1.8], [16, 1.8], [8, 1.8]])
    return [haft, head, spike, langet]


def clasp_knife():
    handle = np.array([[-11, -1.5], [0, -1.3], [0.6, 1.4], [-11, 1.6]])
    xs = np.linspace(0, 12, 12)
    blade = np.vstack([np.stack([xs, -1.1 + 0.02 * xs ** 2 * 0], 1),
                       np.stack([xs[::-1], np.interp(xs[::-1], [0, 9, 12], [1.0, 0.7, -0.3])], 1)])
    blade[11, 1] = -0.2
    return [handle, blade]


def dirk():
    """Naval dirk / poignard: short straight double-edged blade, small cross, ~22 cm."""
    blade = np.array([[1.2, -1.1], [17, -0.8], [23, 0.0], [17, 0.8], [1.2, 1.1]])
    cross = np.array([[0, -3.2], [1.2, -3.2], [1.2, 3.2], [0, 3.2]])
    grip = np.array([[-9, -1.1], [0, -1.3], [0, 1.3], [-9, 1.1]])
    pommel = ellipse_pts(-9.6, 0, 1.2, 1.4)
    return [blade, cross, grip, pommel]


def boarding_sabre():
    """Boarding sabre An IX: broad, nearly straight, ~65 cm, sheet-iron shell guard."""
    xs = np.linspace(0, 65, 30)
    sag = 1.6 * (xs / 65) ** 2
    w = np.interp(xs, [0, 55, 65], [3.8, 3.5, 0.0])
    blade = np.vstack([np.stack([xs, -sag - 1.8], 1), np.stack([xs[::-1], (-sag + w - 1.8)[::-1]], 1)])
    shell = ellipse_pts(0.2, 0.5, 1.6, 6.5)
    grip = np.array([[-12, -1.7], [0, -1.7], [0, 1.7], [-12, 1.7]])
    bow = np.vstack([ellipse_pts(-6, 4.6, 6.6, 4.4, 0, 180), ellipse_pts(-6, 4.6, 5.6, 3.5, 0, 180)[::-1]])
    return [blade, shell, grip, bow]


def hand_hint(seed=0):
    """Suggestive only: a soft fist blob and a fading wrist, no fingers."""
    return [ellipse_pts(-5, 0.5, 6.0, 5.0), np.array([[-10, 2], [-1, 3], [2, 40], [-14, 40]], float)]


def arm(length=70, ragged=0, seed=0):
    rng = np.random.default_rng(seed)
    fist = ellipse_pts(-5, 0.5, 6.2, 5.2)
    thumb = ellipse_pts(-1.5, -4.2, 2.6, 1.8)
    # forearm leaves the fist toward +y (down the frame, toward the body below)
    fa = np.array([[-10, 2], [-1, 3], [3, length], [-15, length]], float)
    cuff_y = length * 0.45
    teeth = []
    for i in range(9):                                       # torn shirt sleeve edge
        x = -17 + i * 2.6
        teeth.append([x, cuff_y + rng.uniform(-3, 3)])
    sleeve = np.vstack([[[-17, length + 30], [7, length + 30], [6, cuff_y]], teeth[::-1]])
    return [fist, thumb, fa, sleeve]


def figure(blade_fn, seed=0, arm_len=70):
    return arm(arm_len, seed=seed) + blade_fn()


def place(shapes, x, y, scale_px_per_cm, ang_deg, flip=False):
    a = math.radians(ang_deg)
    R = np.array([[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]])
    out = []
    for s in shapes:
        p = s.copy().astype(float)
        if flip: p[:, 0] *= -1
        out.append((p @ R.T) * scale_px_per_cm + [x, y])
    return out


def rasterise(polys, w, h):
    m = np.zeros((h * SS, w * SS), np.uint8)
    for p in polys:
        cv2.fillPoly(m, [np.round(p * SS).astype(np.int32)], 255, cv2.LINE_AA)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


def moon_wash(w, h, cx, cy, r, seed):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * 0.8)) ** 2)
    pool = np.clip(1.15 - d, 0, 1) ** 1.6
    rng = np.random.default_rng(seed)                       # faint ripple light, as if off the sea
    n = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), w / 60)
    n = (n - n.mean()) / (n.std() + 1e-6)
    return np.clip(pool * (0.94 + 0.04 * n), 0, 1)


def smoke(w, h, seed, scale):
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for o, amp in ((scale, 1.0), (scale / 2.5, 0.5), (scale / 6, 0.25)):
        n = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), o)
        acc += amp * (n - n.mean()) / (n.std() + 1e-6)
    return acc / 1.75


def dissolve(mask, W, H, seed, scale, keep=0.55):
    """Suggestive, not literal: smoke noise eats the shadow, harder at the tip, so it reads as a hint."""
    sm = smoke(W, H, seed, scale)
    eat = np.clip(0.5 + 0.5 * sm, 0, 1)
    return np.clip(mask * (keep + (1 - keep) * eat) - 0.25 * np.clip(-sm, 0, None) * mask, 0, 1)


def blade_set(name, frame, seed, W, H, cm):
    """Blades only (no hands: suggestive, not literal). Returns (core polygons, soften px, ghost or None).
    Angle: the point goes along +x turned by ang degrees (90 = point down)."""
    S, D, K, B = briquet, dirk, clasp_knife, boarding_sabre
    rng = np.random.default_rng(seed + 7)
    if frame == "A":                                         # one raised blade per wall, point down, about to strike
        spec = {"CENTRE": (S, 0.42, 0.10, 4.2, 62, False),
                "LEFT":   (D, 0.40, 0.14, 8.0, 74, False),
                "RIGHT":  (B, 0.62, 0.08, 3.9, 116, True)}[name]
        fn, fx, fy, sc, ang, fl = spec
        return place(fn(), W * fx, H * fy, cm * sc, ang if not fl else ang - 180, flip=fl), 1.6, None
    if frame == "B":                                         # many small blades rising from below + the outer edge
        polys = []
        n = {"LEFT": 7, "CENTRE": 5, "RIGHT": 7}[name]
        fns = [D, S, K, B, D, K, S]
        for j in range(n):
            fx = (j + 0.5) / n + rng.uniform(-0.04, 0.04)
            outer = (1 - fx) if name == "LEFT" else (fx if name == "RIGHT" else 0.5 - abs(fx - 0.5))
            fy = 1.02 - 0.42 * outer * rng.uniform(0.6, 1.0) - rng.uniform(0.0, 0.12)
            lean = (fx - 0.5) * -60 if name == "CENTRE" else (30 if name == "LEFT" else -30)
            ang = -90 + lean + rng.uniform(-18, 18)          # points up, leaning toward the centre of the stage
            fn = fns[(j + seed) % 7]
            sc = {D: 5.0, K: 6.5, S: 2.6, B: 2.4}[fn] * rng.uniform(0.8, 1.1)
            polys += place(fn(), W * fx, H * fy, cm * sc, ang)
        return polys, 1.6, None
    # C: fantasmagorie, one huge soft blade per wall, swelling (a bigger, softer ghost behind it)
    spec = {"CENTRE": (S, 0.30, 0.05, 7.5, 40, False),
            "LEFT":   (D, 0.30, 0.02, 15.0, 62, False),
            "RIGHT":  (B, 0.75, 0.04, 7.0, 128, True)}[name]
    fn, fx, fy, sc, ang, fl = spec
    a2 = ang if not fl else ang - 180
    core = place(fn(), W * fx, H * fy, cm * sc, a2, flip=fl)
    ghost = place(fn(), W * fx, H * fy, cm * sc * 1.15, a2, flip=fl)
    return core, 7.0, ghost


def wall(name, frame, seed):
    """Returns (alpha 0-1, preview BGR) for one wall."""
    W, H = (int(v * PXMM) for v in WALLS[name])
    cm = PXMM * 10
    polys, soft, ghost = blade_set(name, frame, seed, W, H, cm)
    m = cv2.GaussianBlur(rasterise(polys, W, H), (0, 0), soft)
    if ghost is not None:
        g = cv2.GaussianBlur(rasterise(ghost, W, H), (0, 0), 22)
        m = np.maximum(m, 0.55 * g)
    a = dissolve(m, W, H, seed * 13 + len(name), W / 22, keep={"A": 0.80, "B": 0.70, "C": 0.65}[frame])
    a = np.clip(a * 0.92, 0, 1)                             # never a full black hole; a shadow, not a cut-out
    wash = moon_wash(W, H, W * 0.5, H * 0.35, W * 0.85, seed)
    prev = (wash * (1 - a))[..., None] * MOON * 0.55
    return a, prev, W, H


def write_rgba(path, a):
    """Alpha PNG for superimposing: colour = near-black cold blue, alpha = shadow density."""
    h, w = a.shape
    rgba = np.zeros((h, w, 4), np.uint16)
    rgba[..., 0] = int(0.06 * 65535); rgba[..., 1] = int(0.03 * 65535); rgba[..., 2] = int(0.02 * 65535)
    rgba[..., 3] = (np.clip(a, 0, 1) * 65535).astype(np.uint16)
    cv2.imwrite(path, rgba)


def main():
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    os.makedirs(os.path.join(out, "alpha"), exist_ok=True)
    gap, rows = 24, []
    for i, (fr, label) in enumerate([("A", "A  ONE BLADE PER WALL"), ("B", "B  THEY CLOSE IN"), ("C", "C  FANTASMAGORIE")]):
        tiles = [wall(n, fr, i + 1) for n in ("LEFT", "CENTRE", "RIGHT")]
        H = tiles[0][3]; W = sum(t[2] for t in tiles) + 2 * gap
        row = np.zeros((H + 60, W, 3), np.float32) + 0.08
        x = 0
        for (a, img, w, h), n in zip(tiles, ("LEFT", "CENTRE", "RIGHT")):
            row[60:60 + h, x:x + w] = img
            write_rgba(os.path.join(out, "alpha", f"S9_b10_blades_{fr}_{n}_ALPHA.png"), a)
            cv2.putText(row, n, (x + 8, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0.6, 0.6, 0.6), 1, cv2.LINE_AA)
            x += w + gap
        cv2.putText(row, label, (W - 520, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0.85, 0.85, 0.85), 2, cv2.LINE_AA)
        rows.append(row)
    p = os.path.join(out, "S9_b10_blades_STYLE_FRAMES_A_B_C.png")
    cv2.imwrite(p, (np.clip(np.vstack(rows), 0, 1) * 255).astype(np.uint8))
    print(p)


if __name__ == "__main__":
    main()
