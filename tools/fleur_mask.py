"""Meeting 8: rasterise ONE fleur-de-lis from Wikimedia Commons' Flag_of_Royalist_France.svg (public domain) to a mask.

Headless Edge renders the SVG at 3000x2000 (no cairosvg on the PC); the top-left fleur is cropped (+pad) and the mask is
(r - b) normalised (white field -> 0, gold -> 1). Writes fleur_mask.png next to the SVG. render_s6.py's GenFlag._fleurs reads it.
"""
import os, subprocess, sys
import numpy as np
from PIL import Image

D = r'D:/SOTR/SOTR_MEDIA/05_REFERENCE_UPLOADS/S6_fleur'
SVG = os.path.join(D, 'Flag_of_Royalist_France.svg')
EDGE = r'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'
W, H = 3000, 2000


def main():
    html = os.path.join(D, '_render_svg.html')
    shot = os.path.join(D, '_render_svg_3000.png')
    with open(html, 'w', encoding='utf-8') as fh:
        fh.write('<html><body style="margin:0;background:#fff">'
                 f'<img src="Flag_of_Royalist_France.svg" style="display:block;width:{W}px;height:{H}px"></body></html>')
    url = 'file:///' + html.replace('\\', '/')
    shot = os.path.normpath(shot)
    prof = os.path.join(os.environ.get('TEMP', D), 'sotr_edge_headless')     # own profile: never hands off to a running Edge
    subprocess.run([EDGE, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--user-data-dir={prof}',
                    '--allow-file-access-from-files', f'--window-size={W},{H}', f'--screenshot={shot}', url],
                   check=True, timeout=120)
    im = np.asarray(Image.open(shot).convert('RGB'), np.float32)
    print('shot', im.shape)
    m = np.clip(im[..., 0] - im[..., 2], 0, None)
    # find the top-left fleur's bbox from the mask itself (left third, top 2/3)
    sub = m[:, : W // 3] > 40
    ys, xs = np.nonzero(sub)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    print('bbox', x0, x1, y0, y1)
    p = 12
    c = im[max(0, y0 - p): y1 + p + 1, max(0, x0 - p): x1 + p + 1]
    # coverage: solid inside the fleur (gold, shading and outline all have low blue; the white field has b=255)
    cov = np.clip((255 - c[..., 2]) / (255 - 75), 0, 1)
    # shade: the drawing's own light inside the fleur (main gold g=226 -> 1.0, the darker gold and outline lower)
    shade = np.clip(c[..., 1] / 226.0, 0.45, 1.0)
    out = os.path.join(D, 'fleur_mask.png')
    Image.fromarray((cov * 255 + 0.5).astype(np.uint8)).save(out)
    Image.fromarray((shade * 255 + 0.5).astype(np.uint8)).save(os.path.join(D, 'fleur_shade.png'))
    print('wrote', out, cov.shape)


if __name__ == '__main__':
    sys.exit(main())
