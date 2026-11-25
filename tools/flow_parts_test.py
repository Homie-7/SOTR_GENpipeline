import sys, numpy as np, cv2
sys.path.insert(0, 'tools')
import cannon_fallback as cf
sm = cf.Smoke(seed=51); W = cf.W
ix = 899.0
side = np.tanh((sm.X - ix) / 600).astype(np.float32)
u = np.interp(sm.X, [-W/2, W/2, 3*W/2], [cf.S6_DX['LEFT'], cf.S6_DX['CENTRE'], cf.S6_DX['RIGHT']]).astype(np.float32)
tt = np.arange(200, dtype=np.float32)
sr = cf.smoothstep(38, 108, tt).astype(np.float32)
Tlo = np.concatenate([[0], np.cumsum(1-sr)[:-1]]); Thi = np.concatenate([[0], np.cumsum(sr)[:-1]])
vlo = 0.25*cf.S6_DX['CENTRE']
def bm(a, b):
    g0 = cv2.resize(a, (960, 540)); g1 = cv2.resize(b, (960, 540))
    ref = g0[225:450, 150:550]; best = None
    for dx in range(-45, 46):
        for dy in range(-8, 5):
            m = float(np.abs(ref - g1[225+dy:450+dy, 150+dx:550+dx]).mean())
            if best is None or m < best[0]: best = (m, dx, dy)
    return best[1]*2/3
def disp(t, burst, drift):
    B = 3*12*(1-np.exp(-t/12)) if burst else 0
    return (B*side + (vlo*Tlo[t] + u*Thi[t] if drift else 0)).astype(np.float32)
for label, bu, dr in (('burst only', 1, 0), ('drift only', 0, 1), ('both', 1, 1)):
    for w in ('LEFT', 'CENTRE', 'RIGHT', 'FLOOR'):
        v = [bm(sm.wall(sm.field(float(t), disp(t, bu, dr), np.float32(0)), w)*255,
                sm.wall(sm.field(float(t+3), disp(t+3, bu, dr), np.float32(0)), w)*255) for t in range(22, 62, 4)]
        print(label, w, ' '.join(f'{x:+.0f}' for x in v), f'mean {np.mean(v):+.2f}')
