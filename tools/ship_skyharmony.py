"""ONE SKY across the three ship walls (Homie, 7 Oct, on SUNSET: "visibly dark smoke-ish thing in the centre, make sure that
all is consistent across the 3 screens").

The sunset side walls (NBP build-outs) carry vivid, high-contrast clouds with bright orange edges, glowing brightest at the
FAR left, while the approved CENTRE has soft, hazy clouds that darken to a murky band near the horizon. ship_seams.py made
the colour meet AT the seams; the style still changed across them. Physically the far left should be the darkest (the sun
sits just right of the mast).

FIX (script, 0 cr; CENTRE untouched): in the SKY only (bgmask, above the horizon) of LEFT and RIGHT,
  base   = the sky's broad light (normalised convolution, sigma 40 px), detail = sky - base   (in Lab)
  base  -> CENTRE's own edge light, row by row, carried out flat across the side wall
  detail-> scaled by k = std(CENTRE sky detail) / std(side sky detail), per channel and per side
The sea is never touched. Feathered at the horizon and the mask edges.

  python tools/ship_skyharmony.py STATE [HORIZON_ROW]  # sunset: 448; rewrites 3_walls/seamed_v2/<STATE>/S7-SHIP-{LEFT,RIGHT}_1080.png
                                                   # (old files to 04_WORKING_FILES/superseded/S7_ship_skyharmony_<date>/)
  from ship_skyharmony import harmonise            # used per frame by tools/s7_idle.py --sky-harmony (k from the still)
"""
import os
import shutil
import sys

import cv2
import numpy as np

T = '/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/'
S7 = T + 'S7_ship/'
L0, L1 = 1440, 3240          # CENTRE columns in the 4680 panorama
EDGE = 40                    # columns of CENTRE averaged for its edge light


def horizon_row(pan, bg):
    g = cv2.cvtColor(pan, cv2.COLOR_BGR2GRAY).astype(np.float32)
    dy = np.abs(np.diff(cv2.GaussianBlur(g, (0, 0), 2), axis=0))
    m = (bg[:-1] > 0.5) & (bg[1:] > 0.5)
    prof = (dy * m).sum(1) / np.maximum(m.sum(1), 1)
    lo, hi = 300, 600          # the horizon sits ~0.4 of the way down every state (the rail is lower)
    return int(lo + np.argmax(prof[lo:hi]))


def masked_blur(x, m, s=40):
    f = 8
    xs = cv2.resize(x * m[..., None], None, fx=1 / f, fy=1 / f, interpolation=cv2.INTER_AREA)
    ms = cv2.resize(m, None, fx=1 / f, fy=1 / f, interpolation=cv2.INTER_AREA)
    xs = cv2.GaussianBlur(xs, (0, 0), s / f); ms = cv2.GaussianBlur(ms, (0, 0), s / f)
    b = xs / np.maximum(ms[..., None], 1e-3)
    return cv2.resize(b, (x.shape[1], x.shape[0]), interpolation=cv2.INTER_LINEAR)


def harmonise(pan, bg, H, k=None):
    """pan: 4680x1080 BGR uint8; bg: float 0..1 (1 = sea/sky); H: horizon row. Returns (out uint8, k)."""
    lab = cv2.cvtColor(pan, cv2.COLOR_BGR2LAB).astype(np.float32)
    sky = bg.copy(); sky[H - 4:] = 0
    base = masked_blur(lab, sky)
    det = lab - base
    if k is None:
        k = {}
        cm = sky[:, L0:L1] > 0.9
        cs = det[:, L0:L1][cm].std(0)
        for side, (x0, x1) in (('L', (0, L0)), ('R', (L1, 4680))):
            sm = sky[:, x0:x1] > 0.9
            k[side] = np.clip(cs / np.maximum(det[:, x0:x1][sm].std(0), 1e-3), 0.3, 1.0)
    out = lab.copy()
    eL = base[:, L0:L0 + EDGE].mean(1); eR = base[:, L1 - EDGE:L1].mean(1)       # CENTRE's edge light per row
    for side, (x0, x1), e in (('L', (0, L0), eL), ('R', (L1, 4680), eR)):
        tgt = np.repeat(e[:, None, :], x1 - x0, 1) + det[:, x0:x1] * k[side][None, None, :]
        w = cv2.GaussianBlur(sky[:, x0:x1], (0, 0), 2)[..., None]
        out[:, x0:x1] = lab[:, x0:x1] * (1 - w) + tgt * w
    res = cv2.cvtColor(np.clip(out, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
    touched = np.zeros(pan.shape[:2], bool)
    touched[:, :L0] = cv2.GaussianBlur(sky[:, :L0], (0, 0), 2) > 1e-3
    touched[:, L1:] = cv2.GaussianBlur(sky[:, L1:], (0, 0), 2) > 1e-3
    res[~touched] = pan[~touched]                       # every pixel outside the side skies stays bit-identical
    return res, k


def load(state):
    d = S7 + f'3_walls/seamed_v2/{state}/'
    pan = np.hstack([cv2.imread(d + f'S7-SHIP-{w}_1080.png') for w in ('LEFT', 'CENTRE', 'RIGHT')])
    bg = np.hstack([cv2.imread(S7 + f'5_layers/seamed_v2/{state}/S7-SHIP-{w}_1080_bgmask.png', 0)
                    for w in ('LEFT', 'CENTRE', 'RIGHT')]).astype(np.float32) / 255
    return pan, bg


def main():
    state = sys.argv[1]
    pan, bg = load(state)
    H = int(sys.argv[2]) if len(sys.argv) > 2 else horizon_row(pan, bg)   # sunset: 448 (cloud edges fool the detector)
    res, k = harmonise(pan, bg, H)
    d = S7 + f'3_walls/seamed_v2/{state}/'
    sup = T + 'superseded/S7_ship_skyharmony_2026-10-07/'
    os.makedirs(sup, exist_ok=True)
    for w, (x0, x1) in (('LEFT', (0, L0)), ('RIGHT', (L1, 4680))):
        f = d + f'S7-SHIP-{w}_1080.png'
        shutil.copy2(f, sup + f'S7-SHIP-{w}_1080_{state}_pre_skyharmony.png')
        cv2.imwrite(f, res[:, x0:x1])
    assert (res[:, L0:L1] == pan[:, L0:L1]).all()
    np.save(d + 'SKYHARMONY_k.npy', np.stack([k['L'], k['R']]))
    with open(d + 'SKYMATCH_LOG.txt', 'a') as fh:
        fh.write(f'2026-10-07 ship_skyharmony.py: horizon row {H}; detail gain L {np.round(k["L"], 2).tolist()} '
                 f'R {np.round(k["R"], 2).tolist()}; side skies -> CENTRE edge light; CENTRE untouched; old sides in {sup}\n')
    cv2.imwrite(S7 + f'6_review/S7-SHIP_{state}_skyharmony_compare.jpg',
                cv2.resize(np.vstack([pan[:H + 60], np.full((8, 4680, 3), (0, 255, 255), np.uint8), res[:H + 60]]),
                           None, fx=1 / 3, fy=1 / 3, interpolation=cv2.INTER_AREA))
    print(state, 'horizon', H, 'k', {s: np.round(v, 2).tolist() for s, v in k.items()})


if __name__ == '__main__':
    main()
