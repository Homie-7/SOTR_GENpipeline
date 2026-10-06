"""The ship's 21:9 DECK CANVAS per light state (Homie, 7 Oct, route A: the intro and the idles as ONE picture across the
three walls).

Seedance's 21:9 is 992x432 = 2.2963:1. The three walls (LEFT 1440 | CENTRE 1800 | RIGHT 1440 = 4680x1080) are the CENTRED
4.33:1 band of that frame, so a canvas is 4680 x 2038 with the walls at rows 479..1559 and 479 rows to fill above (sky,
rigging going up) and below (deck toward the camera). The canvas is (a) the intro's END frame (day) and (b) each idle
loop's START frame; tools/s7_intro_3walls.sh crops the same band back out, so the walls land on our pixels.

  python tools/ship_canvas21.py guide STATE OUTDIR          # canvas with a guide fill (smooth sky above, deck rows below)
  python tools/ship_canvas21.py merge STATE TAKE.png OUTDIR  # NBP take -> registered on the band -> our band pinned back

merge: the take is resized to the canvas width, registered onto the band (SIFT on CLAHE greys, RANSAC similarity: NBP
reframes, LOG 2026-10-06), then the walls' own pixels replace the band (24 px feather into the take), so the band is our
approved walls exactly. Writes S7-SHIP-CANVAS21_<STATE>.png (4680x2038) + _upload.png (2480x1080) + a check jpg.
"""
import argparse
import os

import cv2
import numpy as np

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/'
WALLS = T + '3_walls/seamed_v2/'
W, H = 4680, 2038
B0 = (H - 1080) // 2           # 479
FEATHER = 24


def walls(state):
    d = WALLS + state + '/'
    return np.hstack([cv2.imread(d + f'S7-SHIP-{w}_1080.png') for w in ('LEFT', 'CENTRE', 'RIGHT')])


def guide(state, outdir):
    band = walls(state).astype(np.float32)
    top = band[:60]
    xs = np.arange(W)
    g = cv2.cvtColor(band[:60].astype(np.uint8), cv2.COLOR_BGR2GRAY).astype(np.float32)
    bh = cv2.morphologyEx(g, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (31, 31)))
    ok = (bh < np.percentile(bh, 40)) & (g > np.percentile(g, 30))
    yy, xx = np.nonzero(ok)
    sky = np.stack([np.polyval(np.polyfit(xx / W, top[yy, xx, c], 4), xs / W) for c in range(3)], 1)
    canvas = np.zeros((H, W, 3), np.float32)
    canvas[:B0] = sky[None] + np.random.default_rng(1).normal(0, 2.0, (B0, W, 1))
    canvas[B0:B0 + 1080] = band
    canvas[B0 + 1080:] = band[-1][None]
    out = os.path.join(outdir, f'S7-SHIP-CANVAS21_{state}_guide.png')
    cv2.imwrite(out, np.clip(canvas, 0, 255).astype(np.uint8))
    print('guide', out)


def clahe(img):
    return cv2.createCLAHE(3, (8, 8)).apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))


def merge(state, take_path, outdir):
    band = walls(state)
    take = cv2.imread(take_path)
    s = W / take.shape[1]
    take = cv2.resize(take, (W, int(round(take.shape[0] * s))), interpolation=cv2.INTER_LANCZOS4)
    # register: take -> canvas coordinates, matching on the band
    ref = np.zeros((H, W, 3), np.uint8); ref[B0:B0 + 1080] = band
    sift = cv2.SIFT_create(8000)
    k1, d1 = sift.detectAndCompute(clahe(take), None)
    mref = np.zeros((H, W), np.uint8); mref[B0 + 20:B0 + 1060] = 255
    k2, d2 = sift.detectAndCompute(clahe(ref), mref)
    mt = cv2.BFMatcher().knnMatch(d1, d2, k=2)
    good = [m for m, n in mt if m.distance < 0.75 * n.distance]
    p1 = np.float32([k1[m.queryIdx].pt for m in good]); p2 = np.float32([k2[m.trainIdx].pt for m in good])
    A, inl = cv2.estimateAffinePartial2D(p1, p2, method=cv2.RANSAC, ransacReprojThreshold=3.0, maxIters=20000)
    reg = cv2.warpAffine(take, A, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REPLICATE)
    res = np.linalg.norm((cv2.transform(p1[inl.ravel() > 0][None], A)[0] - p2[inl.ravel() > 0]), axis=1)
    sc = float(np.hypot(A[0, 0], A[1, 0]))
    # pin our band back, feathered into the take
    a = np.zeros((H, 1), np.float32); a[B0:B0 + 1080] = 1
    a[B0:B0 + FEATHER, 0] = np.linspace(0, 1, FEATHER); a[B0 + 1080 - FEATHER:B0 + 1080, 0] = np.linspace(1, 0, FEATHER)
    full = ref.astype(np.float32)
    full[:B0] = reg[:B0]; full[B0 + 1080:] = reg[B0 + 1080:]
    a3 = a[..., None]
    out = reg.astype(np.float32) * (1 - a3) + full * a3
    out[B0 + FEATHER:B0 + 1080 - FEATHER] = band[FEATHER:1080 - FEATHER]
    out = np.clip(out, 0, 255).astype(np.uint8)
    base = os.path.join(outdir, f'S7-SHIP-CANVAS21_{state}')
    cv2.imwrite(base + '.png', out)
    cv2.imwrite(base + '_upload.png', cv2.resize(out, (2480, 1080), interpolation=cv2.INTER_AREA))
    chk = cv2.resize(out, (1560, 679), interpolation=cv2.INTER_AREA)
    for y in (B0, B0 + 1080):
        cv2.line(chk, (0, int(y / 3)), (1559, int(y / 3)), (0, 0, 255), 1)
    for x in (1440, 3240):
        cv2.line(chk, (x // 3, 0), (x // 3, 678), (0, 255, 255), 1)
    cv2.imwrite(base + '_check.jpg', chk)
    print(f'{state}: {int(inl.sum())} inliers, scale {sc:.4f}, residual median {np.median(res):.2f} px -> {base}.png')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=('guide', 'merge')); ap.add_argument('state')
    ap.add_argument('rest', nargs='+')
    a = ap.parse_args()
    if a.cmd == 'guide':
        guide(a.state, a.rest[0])
    else:
        merge(a.state, a.rest[0], a.rest[1])


if __name__ == '__main__':
    main()
