"""The Louvre gallery walls in the BLACKOUT (Scene 1), made from the approved LIT v2 walls by script.

Built 2026-10-05. Script: "BLACKOUT. We are in the dark and the gallery room becomes eerily silent… all of the following
dialogue is performed in the dark… AMINA shines her torch on 'The Raft of the Medusa'." So:
- the room almost gone: every wall at --level of its lit value, a breath of cool (no new light source is invented);
- the paintings and gilt keep a little more (--paint-level), so the Raft is BARELY there when Amina's real torch finds
  it (a real torch on a black projection would show only a blank screen);
- on CENTRE only, the glowing puddle's teal light rising softly up the foot of the wall below the Raft (light only,
  it never crosses a seam), matching the floor's GLOW-DARK. Still image; the floor carries the motion.

  python tools/gallery_dark.py LIT.png OUT.png --frames x,y,w,h[;x,y,w,h] [--puddle-light]
Needs numpy, Pillow, opencv.
"""
import argparse
import numpy as np
from PIL import Image
import cv2

TEAL = np.float32([0.16, 0.78, 0.70])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('lit')
    ap.add_argument('out')
    ap.add_argument('--frames', required=True, help='frame boxes in this image, x,y,w,h;…')
    ap.add_argument('--level', type=float, default=0.05)
    ap.add_argument('--paint-level', type=float, default=0.11)
    ap.add_argument('--puddle-light', action='store_true')
    a = ap.parse_args()
    img = np.asarray(Image.open(a.lit).convert('RGB'), np.float32) / 255
    H, W = img.shape[:2]
    m = np.zeros((H, W), np.float32)
    for b in a.frames.split(';'):
        x, y, w, h = map(int, b.split(','))
        m[y:y + h, x:x + w] = 1
    m = cv2.GaussianBlur(m, (0, 0), 1.5)[..., None]  # tight: a wider blur left a light halo round each frame
    lvl = a.level * (1 - m) + a.paint_level * m
    out = img * lvl * np.float32([0.85, 0.93, 1.0])
    if a.puddle_light:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        up = np.exp(-(H - yy) / (0.22 * H))                     # strongest at the floor, fading up the wall
        across = np.exp(-((xx - W / 2) / (0.22 * W)) ** 2)      # centred under the Raft
        out = out + (up * across)[..., None] * TEAL * 0.16
    Image.fromarray((np.clip(out, 0, 1) * 255 + 0.5).astype(np.uint8)).save(a.out)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
