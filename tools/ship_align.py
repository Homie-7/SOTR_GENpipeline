"""Warp a light-state take of a ship wall onto the DAY wall's exact framing (one zoom + shift + tiny rotation).

  python tools/ship_align.py DAY_WALL_1080.png TAKE.png OUT.png [--check]

DAY_WALL_1080.png is the assembled day wall (assembled_v1/S7-SHIP-<WALL>_1080.png); its size is the output size.
TAKE.png is the raw NBP state edit at full resolution (any aspect). SIFT features on contrast-equalised greys (the
light changes, the wood and rigging don't), ratio test, RANSAC similarity: day -> take. The take is then sampled
through that transform, so the output sits on the day wall pixel for pixel. Prints the scale, shift, inliers and how
much of the frame fell outside the take (filled from the day wall, darkened to the take's level, and reported).

WHY (2026-10-06): the light states are crossfaded on ONE geometry. NBP edits of the 5:3 CENTRE come back 16:9 and
re-framed by up to ~25% (NIGHT a9ec4c60: 7.5% larger + 64 px; MAGIC b74194cc: 21% smaller). ship_assemble.py's plain
scale-and-crop kept that drift, so a light change would jump. The side walls drift <0.5% and need no warp.
"""
import argparse

import cv2
import numpy as np


def similarity(ref, img):
    cl = cv2.createCLAHE(3, (8, 8))
    g1 = cl.apply(cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY))
    g2 = cl.apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    sift = cv2.SIFT_create(6000)
    k1, d1 = sift.detectAndCompute(g1, None)
    k2, d2 = sift.detectAndCompute(g2, None)
    ms = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [a for a, b in ms if a.distance < 0.7 * b.distance]
    a = np.float32([k1[m.queryIdx].pt for m in good])
    b = np.float32([k2[m.trainIdx].pt for m in good])
    M, inl = cv2.estimateAffinePartial2D(a, b, ransacReprojThreshold=3, maxIters=5000)
    return M, int(inl.sum()), len(good)


def fill_from_day(out, day, valid, refl=None, band=48, feather=16):
    """Where the take has no pixels (a strip at an edge), use the day wall (same geometry, so rigging and planks run
    on) recoloured to the take: LAB mean/std matched on the valid band just inside the strip. A strip on the TOP edge
    (sky) takes the take's own pixels reflected at the edge instead (`refl`): the day sky carries clouds and the mast's
    painted band, which recolouring can't remove (NIGHT a9ec4c60, 2026-10-06)."""
    miss = ~valid
    near = cv2.dilate(miss.astype(np.uint8), np.ones((2 * band + 1, 2 * band + 1), np.uint8)) > 0
    o = cv2.cvtColor(out, cv2.COLOR_BGR2LAB).astype(np.float32)
    d = cv2.cvtColor(day, cv2.COLOR_BGR2LAB).astype(np.float32)
    fill = d.copy()
    n, lab = cv2.connectedComponents(miss.astype(np.uint8))
    for k in range(1, n):
        reg = lab == k
        ring = cv2.dilate(reg.astype(np.uint8), np.ones((2 * band + 1, 2 * band + 1), np.uint8)) > 0
        ring &= valid
        for c in range(3):
            mo, so = o[..., c][ring].mean(), o[..., c][ring].std() + 1e-3
            md, sd = d[..., c][ring].mean(), d[..., c][ring].std() + 1e-3
            fill[..., c][reg | (near & ring)] = (d[..., c][reg | (near & ring)] - md) * (so / sd) + mo
    fill = cv2.cvtColor(np.clip(fill, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR).astype(np.float32)
    if refl is not None:
        for k in range(1, n):
            reg = lab == k
            if reg[0].any():                         # touches the top edge: its SKY rows (above the horizon) only;
                top = cv2.dilate(reg.astype(np.uint8), np.ones((feather * 2 + 1, 1), np.uint8)) > 0
                top[int(0.387 * reg.shape[0]):] = False  # a ring round the frame must not mirror the deck (WRECK 40936720)
                fill[top] = refl[top]
    # alpha: 1 in the strip, ramping to 0 over `feather` px into the take
    dist = cv2.distanceTransform(valid.astype(np.uint8), cv2.DIST_L2, 5)
    alpha = np.clip(1 - dist / feather, 0, 1)[..., None]
    return np.clip(out * (1 - alpha) + fill * alpha, 0, 255).astype(np.uint8)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('day'); ap.add_argument('take'); ap.add_argument('out')
    ap.add_argument('--check', action='store_true', help='re-measure the output against the day wall')
    a = ap.parse_args()
    day = cv2.imread(a.day)
    take = cv2.imread(a.take)
    h, w = day.shape[:2]
    # match at the day wall's scale: shrink the take so features are comparable, then lift M back to full res
    f = h / take.shape[0]
    small = cv2.resize(take, (int(round(take.shape[1] * f)), h), interpolation=cv2.INTER_AREA)
    M, inl, n = similarity(day, small)
    M_full = M / f
    out = cv2.warpAffine(take, M_full, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LANCZOS4,
                         borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0))
    inside = cv2.warpAffine(np.full(take.shape[:2], 255, np.uint8), M_full, (w, h),
                            flags=cv2.WARP_INVERSE_MAP | cv2.INTER_NEAREST, borderValue=0)
    miss = (inside == 0).mean()
    if miss > 0:
        refl = cv2.warpAffine(take, M_full, (w, h), flags=cv2.WARP_INVERSE_MAP | cv2.INTER_LANCZOS4,
                              borderMode=cv2.BORDER_REFLECT_101).astype(np.float32)
        out = fill_from_day(out, day, inside > 0, refl)
    cv2.imwrite(a.out, out)
    s = np.hypot(M[0, 0], M[1, 0])
    print(f'scale {s:.4f} (take/day)  shift {M[0, 2]:.1f},{M[1, 2]:.1f} px  inliers {inl}/{n}  outside-take {miss * 100:.2f}%')
    if a.check:
        M2, i2, n2 = similarity(day, out)
        print(f'check: scale {np.hypot(M2[0, 0], M2[1, 0]):.4f} shift {M2[0, 2]:.1f},{M2[1, 2]:.1f} px  inliers {i2}/{n2}')


if __name__ == '__main__':
    main()
