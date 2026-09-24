"""PROTOTYPE (2026-09-24, not wired into render_wall.py yet): the wall itself breaks into 3D
blocks toward its inner edge, Control-style, the direction Homie asked for after rejecting the
2D dissolve mask. Test on a still:  python tools/fracture_edge_proto.py IN.png OUT.png

Pieces are real regions of the live frame, placed in 3D and seen through a pinhole camera
matched to the locked plate (~45 deg). Front faces carry the picture; side faces give thickness.
"""
import sys

import cv2
import numpy as np

W, H = 1664, 1248
F = (W / 2) / np.tan(np.radians(22.5))  # focal length in px; the wall plane sits at depth F


def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = np.cos(ax), np.sin(ax), np.cos(ay), np.sin(ay), np.cos(az), np.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def project(P):
    """P: (n,3) with z toward the camera (0 = wall plane). Returns (n,2) image coords."""
    s = F / (F - P[:, 2])
    return np.stack([W / 2 + (P[:, 0] - W / 2) * s, H / 2 + (P[:, 1] - H / 2) * s], 1)


def split_blocks(zone_w, rng):
    """Recursive splits into architecture-like rectangles: big near the whole side, small at the edge."""
    out, stack = [], [(0, 0, zone_w, H)]
    while stack:
        x, y, w, h = stack.pop()
        u = (x + w / 2) / zone_w  # 0 at the inner edge
        target = 40 + 190 * u ** 1.2
        if max(w, h) > target * rng.uniform(0.8, 1.3):
            if w > h * rng.uniform(0.6, 1.4):
                c = int(w * rng.uniform(0.35, 0.65)); stack += [(x, y, c, h), (x + c, y, w - c, h)]
            else:
                c = int(h * rng.uniform(0.35, 0.65)); stack += [(x, y, w, c), (x, y + c, w, h - c)]
        else:
            out.append((x, y, w, h))
    return out


class Fracture:
    def __init__(self, zone_frac=0.19, seed=7):
        rng = np.random.default_rng(seed)
        self.zw = int(W * zone_frac)
        self.blocks = []
        for (x, y, w, h) in split_blocks(self.zw, rng):
            u = (x + w / 2) / self.zw
            # only the inner ~2/3 of the zone comes loose; the rest stays attached, so the break
            # line follows block edges (ragged) instead of the zone's straight boundary
            loose = np.clip(1.1 - 1.75 * u + rng.normal(0, 0.18), 0, 1) ** 1.6  # 0 = attached, 1 = free
            gone = rng.uniform() < 0.75 * loose ** 2  # the wall thins out toward the edge
            self.blocks.append(dict(
                x=x, y=y, w=w, h=h, u=u, loose=loose, gone=gone,
                z=loose * rng.uniform(-420, 160),  # most recede into the dark, some come forward
                dx=-loose * rng.uniform(10, 120), dy=loose * rng.uniform(-60, 60),
                rx=loose * rng.uniform(-0.5, 0.5), ry=loose * rng.uniform(-0.7, 0.7), rz=loose * rng.uniform(-0.35, 0.35),
                depth=rng.uniform(18, 40),  # thickness, px
                ph=rng.uniform(0, 2 * np.pi, 4), per=rng.uniform(7, 14, 4)))

    def render(self, frame, t):
        out = frame.copy()
        out[:, :self.zw] = 0  # the void behind the broken wall
        for b in self.blocks:  # attached blocks: exactly the wall, no seams
            if b['loose'] <= 0.08:
                out[b['y']:b['y'] + b['h'], b['x']:b['x'] + b['w']] = frame[b['y']:b['y'] + b['h'], b['x']:b['x'] + b['w']]
        # attached blocks first (in plane), then free ones far-to-near
        order = sorted(self.blocks, key=lambda b: b['z'] if b['loose'] > 0.05 else -1e9)
        for b in order:
            if b['gone'] or b['loose'] <= 0.08:
                continue
            L = b['loose']
            wob = [np.sin(2 * np.pi * t / b['per'][i] + b['ph'][i]) for i in range(4)]
            z = b['z'] + L * 25 * wob[0]
            R = rot(b['rx'] + L * 0.06 * wob[1], b['ry'] + L * 0.06 * wob[2], b['rz'] + L * 0.04 * wob[3])
            c = np.array([b['x'] + b['w'] / 2, b['y'] + b['h'] / 2, 0.0])
            corners = np.array([[b['x'], b['y'], 0], [b['x'] + b['w'], b['y'], 0],
                                [b['x'] + b['w'], b['y'] + b['h'], 0], [b['x'], b['y'] + b['h'], 0]], float)
            move = np.array([b['dx'] + L * 8 * wob[2], b['dy'] + L * 8 * wob[3], z])
            front = (corners - c) @ R.T + c + move
            normal = R @ np.array([0, 0, 1.0])
            back = front - normal * b['depth']
            pf, pb = project(front), project(back)
            src = frame[b['y']:b['y'] + b['h'], b['x']:b['x'] + b['w']]
            face_col = src.reshape(-1, 3).mean(0)
            # side faces: darker, lit by how much each side faces the camera and the light
            for i in range(4):
                j = (i + 1) % 4
                quad = np.array([pf[i], pf[j], pb[j], pb[i]], np.float32)
                edge = front[j] - front[i]
                sn = np.cross(edge, normal); sn /= np.linalg.norm(sn) + 1e-9
                shade = (0.18 + 0.35 * max(0.0, sn @ np.array([0.5, -0.4, 0.75]))) * np.clip(1 + z / 450, 0.08, 1.05)
                cv2.fillConvexPoly(out, quad.astype(np.int32), (face_col * shade).tolist(), lineType=cv2.LINE_AA)
            # front face: the live picture, perspective-warped, darker the further it recedes
            dst = pf.astype(np.float32)
            M = cv2.getPerspectiveTransform(np.float32([[0, 0], [b['w'], 0], [b['w'], b['h']], [0, b['h']]]), dst)
            x0, y0 = np.floor(dst.min(0)).astype(int); x1, y1 = np.ceil(dst.max(0)).astype(int)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, W), min(y1, H)
            if x1 <= x0 or y1 <= y0:
                continue
            T = np.array([[1, 0, -x0], [0, 1, -y0], [0, 0, 1]]) @ M
            warped = cv2.warpPerspective(src, T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
            mask = cv2.warpPerspective(np.ones(src.shape[:2], np.float32), T, (x1 - x0, y1 - y0), flags=cv2.INTER_LINEAR)
            lit = (0.55 + 0.45 * max(0.0, normal @ np.array([0, 0, 1.0]))) * np.clip(1 + z / 450, 0.08, 1.05)
            region = out[y0:y1, x0:x1]
            region[:] = region * (1 - mask[..., None]) + warped * lit * mask[..., None]
        return out


if __name__ == '__main__':
    src, dst = sys.argv[1], sys.argv[2]
    img = cv2.imread(src).astype(np.float32)
    fr = Fracture()
    cv2.imwrite(dst, np.clip(fr.render(img, 0.0), 0, 255).astype(np.uint8))
    print(len(fr.blocks), 'blocks,', sum(b['gone'] for b in fr.blocks), 'gone')
