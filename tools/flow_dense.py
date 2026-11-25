import sys, cv2, numpy as np
d = sys.argv[1]; a, b = int(sys.argv[2]), int(sys.argv[3])
def frames(p):
    c = cv2.VideoCapture(p); out = []
    while True:
        ok, f = c.read()
        if not ok: break
        out.append(f)
    return out
def bm(f0, f1):
    g0 = cv2.cvtColor(cv2.resize(f0, (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    g1 = cv2.cvtColor(cv2.resize(f1, (960, 540), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY).astype(np.float32)
    ref = g0[225:450, 150:550]
    best = None
    for dx in range(-45, 46):
        for dy in range(-8, 5):
            m = float(np.abs(ref - g1[225+dy:450+dy, 150+dx:550+dx]).mean())
            if best is None or m < best[0]: best = (m, dx, dy)
    # contrast of match: zero-shift error vs best error
    m0 = float(np.abs(ref - g1[225:450, 150:550]).mean())
    return best[1]*2/3, best[2]*2/3, best[0], m0, ref.std()
for w in ('LEFT', 'CENTRE', 'RIGHT', 'FLOOR'):
    F = frames(f'{d}/S5-CANNON-FALLBACK_{w}.mp4')
    rows = [bm(F[i], F[i+3]) for i in range(a, b, 2)]
    sp = [np.hypot(r[0], r[1]) for r in rows]
    print(w, 'median spd %.2f mean %.2f' % (np.median(sp), np.mean(sp)))
    print('   dx:', ' '.join('%+.0f' % r[0] for r in rows))
    print('   err best/zero:', ' '.join('%.1f/%.1f' % (r[2], r[3]) for r in rows[::3]), ' std %.1f' % rows[0][4])
