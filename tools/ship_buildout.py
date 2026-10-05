"""Build the ship's side walls OUTWARD from the deck master, so both seams continue pixel for pixel (Job 1, 7 Oct 2026).

  python tools/ship_buildout.py canvas  OUTDIR                       # v1 grey canvases (FAILED: NBP mirrored the strip)
  python tools/ship_buildout.py guide   OUTDIR                       # v2 geometric guide canvases (USED)
  python tools/ship_buildout.py walls   OUTDIR --left L.png --right R.png

GEOMETRY. CENTRE (approved, never re-made) = the master f5180ed8 (3168x1344) resized to 2546x1080 and cropped at x 373..2173.
In 1080 "panorama" px the stage is LEFT 0..1440 | CENTRE 1440..3240 | RIGHT 3240..4680, so the master spans 1067..3613
and holds a TRUE strip of 373 px (464 master px) at the inner edge of each side wall. The rest of each side wall does
not exist in the master.

guide (v2, the one that worked): the same canvas, but the outer part is pre-built from the master's OWN geometry so NBP
only has to re-render it: the rail cap continued on the master's own line (a quadratic through the rail-cap tops read on a
50 px grid, extended by its slope at the edge), the bulwark (planks, stanchions, pins, coils) carried outward by the
bulwark plane's perspective step (an elation about the vanishing point (1592, 519), lambda 4.4e-4 = one gun bay, measured
on the gun ports), sky and sea as row-median colour of the open sky/sea + grain, and a grey patch where the near gun
continues. RIGHT is built on the flipped master and flipped back. Prompts: prompts/S7-SHIP-L-BUILDOUT.txt v2 (+ -R-).

canvas: a 16:9 canvas per side at the master's own resolution (2389x1344): the master's outer 1061 px (the true strip +
597 px of CENTRE for context) at the inner side, the outer 1328 px flat grey #808080. NBP fills the grey
(prompts/S7-SHIP-L-BUILDOUT.txt / -R-).

walls: each returned take is (1) resized to the canvas, (2) registered onto the canvas's TRUE part (SIFT on CLAHE greys,
RANSAC similarity; NBP edits reframe by up to 16%, LOG 2026-10-06), (3) colour-matched to the master over the overlap
(per-channel Lab mean/std, measured on the true part), (4) composited: the master's own pixels wherever they exist,
the take only in the grey, joined over a 64 px feather INSIDE the true part (where the registered take already matches
the master), (5) set into an extended master (3168 + 2 x 1328 px wide) and resized with CENTRE's own factors, so the
inner edge of each side wall is the column that sits next to CENTRE's first/last column in the master.
Writes S7-SHIP-<WALL>_1080.png (+ CENTRE copied from --centre), a preview (seams marked) and BUILDOUT_LOG.txt with the
registration (scale, rotation, residual px) and the SEAM CHECK: the mean abs step across each seam vs the mean abs step
between neighbouring columns inside CENTRE (ratio ~1 = no seam).

LIGHT STATES of these walls: NBP text-only edits of the build-out day walls, aligned by ship_states.py, seams matched by
ship_seams.py --colour-only (a per-row gain on thin strips was tried and painted horizontal streaks: ropes and clouds).

WHY (Homie, 7 Oct, on SEAMED_v2): "the seams are still not fully aligned… you can tell the ship's edges are a bit off."
ship_seams.py could match heights and colour, never the scale (1.3x), the rail angle, the doubled guns or the light, because
the 6 Oct side walls were separate generations. Here the seam IS the master.
"""
import argparse
import os

import cv2
import numpy as np

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/'
MASTER = T + '1_deck_master/S7-SHIP-ROOM_v2_f5180ed8.png'
GREY = 1328          # grey width in master px (= 1067 panorama px)
CW = 2389            # canvas width (16:9 at 1344 high)
KEEP = CW - GREY     # master px kept on the canvas (1061)
FEATHER = 64
JOIN_DECAY = 350.0
MATCH_DECAY = 450.0  # px over which a state's seam gain fades into the side wall   # px over which the join's per-row colour offset fades into the new part


def load_master():
    return cv2.imread(MASTER)


def make_canvas(outdir):
    m = load_master(); H, W = m.shape[:2]
    L = np.full((H, CW, 3), 128, np.uint8); L[:, GREY:] = m[:, :KEEP]
    R = np.full((H, CW, 3), 128, np.uint8); R[:, :KEEP] = m[:, W - KEEP:]
    os.makedirs(outdir, exist_ok=True)
    cv2.imwrite(os.path.join(outdir, 'S7-SHIP-L_BUILDOUT_canvas.png'), L)
    cv2.imwrite(os.path.join(outdir, 'S7-SHIP-R_BUILDOUT_canvas.png'), R)


def make_guide(outdir):
    """v2 input canvases (see the docstring). Ported verbatim from the session's scratch script, 7 Oct."""
    m0 = load_master(); H, W = m0.shape[:2]
    os.makedirs(outdir, exist_ok=True)
    VY, LB = 519.0, 4.4e-4
    RP = {'L': [(0, 818), (250, 785), (500, 743), (750, 697), (1000, 648)],
          'R': [(0, 800), (167, 778), (417, 745), (667, 706), (917, 672)]}
    for side in ('L', 'R'):
        m = m0 if side == 'L' else m0[:, ::-1].copy()
        VX = 1591.6 if side == 'L' else W - 1 - 1591.6
        rx, ry = np.array(RP[side], float).T
        cc = np.polyfit(rx, ry, 2)
        r_m = lambda x: np.polyval(cc, x)
        s0 = np.polyval(np.polyder(cc), 0)
        xe = np.arange(-GREY, 0).astype(np.float32)
        r_t = r_m(0) + s0 * xe
        out = np.zeros((H, GREY, 3), np.float32)
        f = m.astype(np.float32); lum = f.mean(2); bl = f[..., 0] - f[..., 2]
        rows = np.zeros((H, 3), np.float32)
        for y in range(H):
            seg = f[y, :700]; ok = (bl[y, :700] > 8) & (lum[y, :700] > 60)
            if y < VY:
                ok &= lum[y, :700] < np.percentile(lum[y, :700], 60) + 1
            rows[y] = np.median(seg[ok], 0) if ok.sum() > 20 else np.nan
        idx = np.arange(H); good = ~np.isnan(rows[:, 0])
        for c in range(3):
            rows[:, c] = np.interp(idx, idx[good], rows[good, c])
        rows = cv2.GaussianBlur(rows.reshape(-1, 1, 3), (1, 15), 0).reshape(-1, 3)
        for i in range(GREY):
            ys = np.arange(H, dtype=np.float32)
            sy = np.where(ys < VY, ys, VY + (ys - VY) * (r_m(0) - 6 - VY) / (r_t[i] - 6 - VY))
            out[:, i] = rows[np.clip(sy.astype(int), 0, H - 1)]
        out += np.random.default_rng(7).normal(0, 3.0, out.shape)
        u_t = xe - VX; u_s = u_t / (1 - LB * u_t); x_s = u_s + VX; k = u_s / u_t
        ys = np.arange(H, dtype=np.float32)
        mapx = np.tile(x_s[None, :], (H, 1)).astype(np.float32)
        mapy = (r_m(x_s)[None, :] + (ys[:, None] - r_t[None, :]) * k[None, :]).astype(np.float32)
        bul = cv2.remap(m, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE).astype(np.float32)
        below = ys[:, None] >= r_t[None, :] - 1
        out[below] = bul[below]
        out[1060:, GREY - 430:] = 128
        canvas = np.full((H, GREY + KEEP, 3), 128, np.uint8); canvas[:, :GREY] = np.clip(out, 0, 255); canvas[:, GREY:] = m[:, :KEEP]
        if side == 'R':
            canvas = canvas[:, ::-1]
        cv2.imwrite(os.path.join(outdir, f'S7-SHIP-{side}_BUILDOUT_v2_guide.png'), canvas)


def grey_clahe(img):
    g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.createCLAHE(2.0, (8, 8)).apply(g)


def register(take, canvas, true_mask):
    """Similarity transform taking the take onto the canvas, from SIFT matches inside the true part only."""
    sift = cv2.SIFT_create(8000)
    k1, d1 = sift.detectAndCompute(grey_clahe(take), None)
    k2, d2 = sift.detectAndCompute(grey_clahe(canvas), true_mask.astype(np.uint8) * 255)
    mt = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [a for a, b in mt if a.distance < 0.75 * b.distance]
    p1 = np.float32([k1[a.queryIdx].pt for a in good]); p2 = np.float32([k2[a.trainIdx].pt for a in good])
    M, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=2.0, maxIters=5000)
    inl = inl.ravel().astype(bool)
    res = np.linalg.norm((p1[inl] @ M[:, :2].T + M[:, 2]) - p2[inl], axis=1)
    sc = float(np.hypot(M[0, 0], M[1, 0])); rot = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
    return M, dict(matches=len(good), inliers=int(inl.sum()), scale=sc, rot_deg=rot, tx=float(M[0, 2]), ty=float(M[1, 2]),
                   resid_px=float(np.median(res)))


def colour_match(src, ref, mask):
    """Per-channel Lab mean/std transfer, measured where mask is set (the true part, where both show the same pixels)."""
    a = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32); b = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype(np.float32)
    out = a.copy()
    for c in range(3):
        sa, sb = a[..., c][mask], b[..., c][mask]
        out[..., c] = (a[..., c] - sa.mean()) * (sb.std() / max(sa.std(), 1e-3)) + sb.mean()
    return cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)



def replace_band(img, x0, h=6):
    """Cover a thin vertical line at column x0: the 2h columns over it become a cross-fade of the 2h columns just left of
    the band and the 2h columns just right of it (real texture from both sides, no smooth stripe)."""
    out = img.astype(np.float32)
    left = out[:, x0 - 3 * h:x0 - h]; right = out[:, x0 + h:x0 + 3 * h]
    al = np.linspace(0, 1, 2 * h, dtype=np.float32)[None, :, None]
    out[:, x0 - h:x0 + h] = left * (1 - al) + right * al
    return np.clip(out, 0, 255).astype(np.uint8)


def destep(wf, x0, side, canvas_ref=None):
    """Remove a vertical colour step at column x0 by shifting the OUTER side (away from CENTRE) row by row, fading out
    over JOIN_DECAY px. The inner reference is canvas_ref (the master) when given, else the take itself."""
    H, CWd = wf.shape[:2]
    ref = canvas_ref.astype(np.float32) if canvas_ref is not None else wf
    inner = slice(x0 + 4, x0 + 28) if side == 'LEFT' else slice(x0 - 28, x0 - 4)
    outer = slice(x0 - 28, x0 - 4) if side == 'LEFT' else slice(x0 + 4, x0 + 28)
    off = np.median(ref[:, inner], 1) - np.median(wf[:, outer], 1)
    off = cv2.GaussianBlur(cv2.medianBlur(np.clip(off, -60, 60).reshape(-1, 1, 3).astype(np.float32), 5), (1, 41), 0).reshape(-1, 3)
    xs = np.arange(CWd, dtype=np.float32)
    dist = (x0 - xs) if side == 'LEFT' else (xs - x0)
    w = np.exp(-np.maximum(dist, 0) / JOIN_DECAY)
    if canvas_ref is None:
        w = np.where(dist > 0, w, 0)       # the take's own step: only its outer side moves
    w = w[None, :, None]                   # at the boundary the inner (feather) side moves too: it shows the take
    return wf + off[:, None, :] * w


def build_side(take_path, side, m):
    H, W = m.shape[:2]
    canvas = np.full((H, CW, 3), 128, np.uint8)
    true = np.zeros((H, CW), bool)
    if side == 'LEFT':
        canvas[:, GREY:] = m[:, :KEEP]; true[:, GREY:] = True
    else:
        canvas[:, :KEEP] = m[:, W - KEEP:]; true[:, :KEEP] = True
    take = cv2.imread(take_path)
    take = cv2.resize(take, (CW, H), interpolation=cv2.INTER_AREA if take.shape[1] > CW else cv2.INTER_LANCZOS4)
    M, info = register(take, canvas, true)
    warped = cv2.warpAffine(take, M, (CW, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    valid = cv2.warpAffine(np.ones((H, CW), np.uint8), M, (CW, H), flags=cv2.INTER_NEAREST) > 0
    info['holes_px'] = int((~valid & ~true).sum())
    ov = true & valid
    ov_er = cv2.erode(ov.astype(np.uint8), np.ones((9, 9), np.uint8)) > 0
    warped = colour_match(warped, canvas, ov_er)
    info['overlap_mad'] = float(np.abs(warped.astype(np.float32) - canvas.astype(np.float32))[ov_er].mean())
    # JOIN: NBP keeps the guide's flat sky right up to the boundary, so the take steps in colour there (a vertical line in
    # the sky). Per row: the master just inside the true part minus the take just outside it, robustly smoothed, added to
    # the new part and fading out with distance from the boundary.
    wf = warped.astype(np.float32)
    g = GREY if side == 'LEFT' else KEEP
    # (a) the take's OWN step: NBP sometimes leaves a straight vertical edge in the sky and sea a little inside the new part
    #     (d0c874d6: 8 L in the sky, 18 in the sea, at ~130 px from the boundary). Found on the open sky/sea rows.
    L = cv2.cvtColor(warped, cv2.COLOR_BGR2LAB)[..., 0].astype(np.float32)
    prof = L[:int(0.52 * H)].mean(0)
    d = np.abs(prof[6:] - prof[:-6])
    lo, hi = (g - 420, g - 8) if side == 'LEFT' else (g + 8, g + 420)
    xs0 = int(np.argmax(d[lo - 3:hi - 3])) + lo
    med = float(np.median(d[lo - 3:hi - 3]))
    own = d[xs0 - 3] > max(2.0, 8 * med)
    d1 = np.abs(np.diff(prof))
    xs0 = int(np.argmax(d1[xs0 - 5:xs0 + 5])) + xs0 - 5 + 1     # the exact column of the step (first column past it)
    info['own_step'] = f'x{xs0} {d[min(xs0, len(d) - 1) - 3]:.1f}L (median {med:.2f}) {"fixed" if own else "none"}'
    if own:
        wf = destep(wf, xs0, 'LEFT' if side == 'LEFT' else 'RIGHT', canvas_ref=None)
    # (b) the boundary itself: master just inside the true part vs the take just outside it
    wf = destep(wf, g, side, canvas_ref=canvas)
    info['join_offset_mean'] = float(np.abs(np.median(canvas[:, (g + 4 if side == 'LEFT' else g - 28):(g + 28 if side == 'LEFT' else g - 4)].astype(np.float32), 1)
                                            - np.median(wf[:, (g - 28 if side == 'LEFT' else g + 4):(g - 4 if side == 'LEFT' else g + 28)], 1)).mean())
    warped = np.clip(wf, 0, 255).astype(np.uint8)
    # alpha = 1 where the master is used: 0 in the grey, ramping to 1 over FEATHER px inside the true part
    xs = np.arange(CW, dtype=np.float32)
    fd = (xs - GREY) if side == 'LEFT' else (KEEP - 1 - xs)
    a = np.clip(fd / FEATHER, 0, 1)[None, :, None]
    out = (canvas.astype(np.float32) * a + warped.astype(np.float32) * (1 - a)).astype(np.uint8)
    # NBP draws the guide's boundary (and its own step, if any) as a thin 1-2 px line: inpaint a narrow band over each
    # (an inpaint left a smooth stripe that read as a line in the sea; a cross-fade of the real texture either side doesn't)
    for x0 in [g] + ([xs0] if own else []):
        out = replace_band(out, x0)
    return out, info



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=('canvas', 'guide', 'walls')); ap.add_argument('outdir')
    ap.add_argument('--left'); ap.add_argument('--right')
    ap.add_argument('--centre', default=T + '3_walls/assembled_v1/S7-SHIP-CENTRE_1080.png')
    a = ap.parse_args()
    if a.cmd == 'canvas':
        return make_canvas(a.outdir)
    if a.cmd == 'guide':
        return make_guide(a.outdir)
    os.makedirs(a.outdir, exist_ok=True)
    m = load_master(); H, W = m.shape[:2]
    E = np.zeros((H, W + 2 * GREY, 3), np.uint8); E[:, GREY:GREY + W] = m
    log = [f'tools/ship_buildout.py walls  left={a.left}  right={a.right}']
    for side, p in (('LEFT', a.left), ('RIGHT', a.right)):
        if not p:
            continue
        s, info = build_side(p, side, m)
        if side == 'LEFT':
            E[:, :CW] = s
        else:
            E[:, E.shape[1] - CW:] = s
        log.append(f'{side}: ' + ', '.join(f'{k} {v:.3f}' if isinstance(v, float) else f'{k} {v}' for k, v in info.items()))
    # CENTRE was made as R = resize(master, (2546, 1080), INTER_AREA)[:, 373:2173]. The panorama takes R itself for every
    # column the master covers (1067..3613), so each side wall's inner 373 px are bit-identical to the master's own resize
    # and the seam with CENTRE is the master's own neighbouring columns. Only the NEW parts are resampled from E, on the
    # same exact mapping (panorama X <-> master x = (X - 1067) * S, S = W / 2546), with a light prefilter standing in for
    # INTER_AREA, and joined to R over JOIN_R px inside the master's span.
    c = cv2.imread(a.centre)
    S = W / 2546.0
    Rm = cv2.resize(m, (2546, 1080), interpolation=cv2.INTER_AREA)
    big = np.zeros((1080, 4680, 3), np.float32)
    big[:, 1067:3613] = Rm
    Ef = cv2.GaussianBlur(E, (0, 0), 0.45 * S).astype(np.float32)
    X = np.arange(4680, dtype=np.float32)
    mapx = np.tile(((X - 1067 + 0.5) * S - 0.5 + GREY)[None, :], (1080, 1)).astype(np.float32)
    mapy = np.tile(((np.arange(1080, dtype=np.float32) + 0.5) * (H / 1080.0) - 0.5)[:, None], (1, 4680)).astype(np.float32)
    rs = cv2.remap(Ef, mapx, mapy, cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    JOIN_R = 24
    w = np.ones(4680, np.float32)                       # 1 = take the resampled E
    w[1067:3613] = 0
    w[1067:1067 + JOIN_R] = np.linspace(1, 0, JOIN_R)
    w[3613 - JOIN_R:3613] = np.linspace(0, 1, JOIN_R)
    if not a.left:
        w[:1067 + JOIN_R] = 0
    if not a.right:
        w[3613 - JOIN_R:] = 0
    big = big * (1 - w[None, :, None]) + rs * w[None, :, None]
    big = np.clip(big + 0.5, 0, 255).astype(np.uint8)
    log.append(f'resampled-vs-R check over the master span: MAD {np.abs(rs[:, 1200:3400] - Rm[:, 133:2333].astype(np.float32)).mean():.2f}')
    walls = {'LEFT': big[:, :1440], 'CENTRE': c, 'RIGHT': big[:, 3240:]}
    # how well the rebuilt pano reproduces the approved CENTRE (should be ~0.5, the resize kernel)
    log.append(f'CENTRE reproduction MAD {np.abs(big[:, 1440:3240].astype(float) - c).mean():.2f}')
    # the seam step vs the master's OWN step between the same two columns (a true continuation gives a ratio of ~1)
    own = {'LEFT': np.abs(Rm[:, 372].astype(np.float32) - Rm[:, 373]).mean(),
           'RIGHT': np.abs(Rm[:, 2172].astype(np.float32) - Rm[:, 2173]).mean()}
    for side, (x1, x2) in (('LEFT', (walls['LEFT'][:, -1], c[:, 0])), ('RIGHT', (c[:, -1], walls['RIGHT'][:, 0]))):
        step = np.abs(x1.astype(np.float32) - x2.astype(np.float32)).mean()
        log.append(f'SEAM {side}: step {step:.2f} vs the master\'s own step there {own[side]:.2f} (ratio {step / own[side]:.2f})')
    for k, im in walls.items():
        cv2.imwrite(os.path.join(a.outdir, f'S7-SHIP-{k}_1080.png'), im)
    pv = np.concatenate([walls['LEFT'], c, walls['RIGHT']], axis=1)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_clean_2340.png'), cv2.resize(pv, (2340, 540), interpolation=cv2.INTER_AREA))
    for x in (1440, 3240):
        pv[:, x - 2:x + 2] = (0, 200, 255)
    cv2.imwrite(os.path.join(a.outdir, 'S7-SHIP_walls_preview.jpg'), cv2.resize(pv, (2340, 540)), [cv2.IMWRITE_JPEG_QUALITY, 88])
    with open(os.path.join(a.outdir, 'BUILDOUT_LOG.txt'), 'w') as fh:
        fh.write('\n'.join(log) + '\n')
    print('\n'.join(log))


if __name__ == '__main__':
    main()
