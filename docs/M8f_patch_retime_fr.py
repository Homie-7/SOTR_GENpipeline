# Draft patch for tools/render_s6.py --retime-fr (chat f, 17 Nov 2026). NOT YET APPLIED OR TESTED.
# Run from the repo root:  python docs/M8f_patch_retime_fr.py   (asserts each anchor occurs exactly once; aborts otherwise)
# HEAD's original is in git (git show HEAD:tools/render_s6.py) for the bit-identical check.
p = 'tools/render_s6.py'
s = open(p, encoding='utf-8').read()


def rep(old, new):
    global s
    n = s.count(old)
    assert n == 1, (old[:80], n)
    s = s.replace(old, new)


rep("V6 = False\n", '''V6 = False
# --retime-fr (Meeting 8, 17 Nov 2026, docs/S6-FR-CUES.md + docs/HANDOFF-2026-11-17-M8e.md): the scene retimed to Darrin's
# French track (121.25 s). Every scripted cue reads t_old = TMAP(t_new); the physical textures (flag and smoke loops, smoke
# drift) read t_old + PHYS_D = t_new, so they keep real speed. RIGHT flag = white with gold fleurs-de-lis (Louise); the map
# ends in an ink-in-water dissolve to alpha. OFF by default: PHYS_D = 0.0 and t + 0.0 == t, so v14 is bit-identical.
RETIME_FR = False
PHYS_D = 0.0
T_NEW = 0.0
FR_DUR = 121.25
FR_KNOTS = [(0.00, 0.0), (15.94, 18.0), (19.26, 23.5), (24.84, 32.0), (29.84, 38.0), (33.04, 41.0), (34.28, 43.5),
            (35.92, 46.0), (37.50, 50.0), (38.74, 52.5), (40.32, 57.0), (43.90, 59.5), (46.80, 63.0), (48.64, 67.0),
            (51.42, 79.0), (52.86, 82.4), (54.20, 84.4), (55.80, 86.4), (58.10, 96.0), (62.50, 101.0), (64.68, 105.0),
            (68.92, 110.0), (75.28, 121.0), (78.80, 124.0), (80.08, 126.0), (81.84, 128.0), (83.90, 130.5), (88.60, 137.5),
            (90.74, 141.0), (97.50, 145.0), (99.28, 147.0), (112.78, 160.5), (120.25, 165.0), (121.25, 165.0)]
INK0, INK1 = 112.78, 120.25                     # the ink dissolve (new s, real time); clear 120.25-121.25
FLEUR_COLS, FLEUR_ROWS = 10, 7                   # Louise's flag: 10 across, 7 rows, alternate rows offset half a cell
_TMAP = None


def tmap_build(sigma_s=0.5):
    """TMAP per frame: the knots, piecewise linear, Gaussian-smoothed (endpoints pinned by odd reflection)."""
    global _TMAP
    n = int(round(FR_DUR * FPS)) + 1
    tn = np.arange(n) / FPS
    kn, ko = zip(*FR_KNOTS)
    to = np.interp(tn, kn, ko)
    r = int(4 * sigma_s * FPS)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / (sigma_s * FPS)) ** 2)
    k /= k.sum()
    pad = np.concatenate([2 * to[0] - to[r:0:-1], to, 2 * to[-1] - to[-2:-r - 2:-1]])
    _TMAP = (tn, np.convolve(pad, k, mode='valid'))


def retime(t):
    """t_new -> t_old under --retime-fr (sets PHYS_D and T_NEW); identity otherwise."""
    global PHYS_D, T_NEW
    if not RETIME_FR:
        return t
    if _TMAP is None:
        tmap_build()
    to = float(np.interp(t, *_TMAP))
    PHYS_D, T_NEW = t - to, t
    return to
''')
# PHYS_D readers
rep("f = self.rd.get(int(round((t + self.offset) * FPS)))", "f = self.rd.get(int(round((t + PHYS_D + self.offset) * FPS)))")
rep("if self.tl_prev is not None and self.tl_prev[0] == int(round((t + self.offset) * FPS)) - 1:",
    "if self.tl_prev is not None and self.tl_prev[0] == int(round((t + PHYS_D + self.offset) * FPS)) - 1:")
rep("self.tl_prev = (int(round((t + self.offset) * FPS)), tl)", "self.tl_prev = (int(round((t + PHYS_D + self.offset) * FPS)), tl)")
rep("E = slide(self.E, bw, bh, bw / 2 + self.ctx.px(900) - 18 * self.ctx.s * t, bh / 2 + self.ctx.px(600) - 9 * self.ctx.s * t)",
    "E = slide(self.E, bw, bh, bw / 2 + self.ctx.px(900) - 18 * self.ctx.s * (t + PHYS_D), "
    "bh / 2 + self.ctx.px(600) - 9 * self.ctx.s * (t + PHYS_D))")
rep("la = self.ra.get(int(round(t * FPS)))\n        lb = self.rb.get(int(round((t + 11.0) * FPS)))",
    "la = self.ra.get(int(round((t + PHYS_D) * FPS)))\n        lb = self.rb.get(int(round((t + PHYS_D + 11.0) * FPS)))")
rep("a = slide(self.a, W, H, (DUR - t) * self.va[0] + W / 2 + 2, t * self.va[1] + H / 2 + 2)\n"
    "        b = slide(self.b, W, H, (DUR - t) * self.vb[0] + W / 2 + 2, t * self.vb[1] + H / 2 + 2)",
    "tp = t + PHYS_D\n        a = slide(self.a, W, H, (DUR - tp) * self.va[0] + W / 2 + 2, tp * self.va[1] + H / 2 + 2)\n"
    "        b = slide(self.b, W, H, (DUR - tp) * self.vb[0] + W / 2 + 2, tp * self.vb[1] + H / 2 + 2)")
# fleur-de-lis flag
rep("        if self.kind == 'white':\n            f = whitec\n", "        if self.kind in ('white', 'fleur'):\n            f = whitec\n")
rep("""            if drain is not None:
                f = self._v6_drain(f, whitec, T1, T2, *drain)
""", """            if drain is not None:
                f = self._v6_drain(f, whitec, T1, T2, *drain)
            if self.kind == 'fleur':
                f = self._fleurs(f, uc, whitec)
""")
rep("    def frame(self, t):\n", '''    def _fleurs(self, f, uc, whitec):
        """Meeting 8 (Louise): the Monarchistes' flag is white with gold fleurs-de-lis, a staggered grid laid in cloth
        coordinates so it rides the folds, shaded by the cloth's own light like whitec."""
        wdm = float(np.median(self.wd))
        if not hasattr(self, 'fl_tile'):
            cw = max(4.0, 3.0 / FLEUR_COLS * wdm)                       # ~3 cloth units (blue+white+red) across, 10 columns
            ch = self.bh / FLEUR_ROWS
            k = 4                                                        # supersampled, then reduced (no aliasing)
            TW, TH = int(round(cw * k)), int(round(2 * ch * k))
            im = Image.new('L', (TW, TH), 0)
            d = ImageDraw.Draw(im)
            fn = ImageFont.truetype(r'C:\\Windows\\Fonts\\seguisym.ttf', max(6, int(0.78 * ch * k)))
            for cx, cy in ((0.5 * TW, 0.25 * TH), (0.0, 0.75 * TH), (TW, 0.75 * TH)):
                d.text((cx, cy), '\\u269c', font=fn, fill=255, anchor='mm')
            t_ = np.asarray(im, F32) / 255
            self.fl_tile = cv2.resize(t_, (max(2, TW // k), max(2, TH // k)), interpolation=cv2.INTER_AREA)
            self.fl_cw, self.fl_ch = cw, ch
        th, tw = self.fl_tile.shape
        xs = (uc + 1.0) * wdm
        mx = (np.mod(xs / self.fl_cw, 1.0) * tw).astype(F32)
        my = (np.mod((self.Y + 0.5 * self.fl_ch) / (2 * self.fl_ch), 1.0) * th).astype(F32)
        m = cv2.remap(self.fl_tile, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_WRAP)[..., None]
        gold = whitec / np.array([0.66, 0.51, 0.38], F32) * np.array([0.78, 0.52, 0.12], F32)
        return f * (1 - m) + gold * m

    def frame(self, t):
''')
rep("        S['flagR'] = GenFlag(ctx, 'R', 'white', box=(0.10, 0.05, 0.90), seed=32)",
    "        S['flagR'] = GenFlag(ctx, 'R', 'fleur' if RETIME_FR else 'white', box=(0.10, 0.05, 0.90), seed=32)")
# ink dissolve
rep("""        if V7_ALPHA:
            # no Sahaj pixels""", """        if RETIME_FR:                                                   # Meeting 8: the ink dissolve sets the alpha
            canvas[:] = np.clip(mapw, 0, None)
            return
        if V7_ALPHA:
            # no Sahaj pixels""")
rep("""            self.cov = None
            self.morph(canvas, t)
            self.draw_route7(canvas, t)
""", """            self.cov = None
            self.morph(canvas, t)
            self.draw_route7(canvas, t)
            if RETIME_FR:
                self.ink(canvas, t)
                return
""")
rep("    def draw_route7(self, canvas, t):\n", '''    def ink(self, canvas, t):
        """Meeting 8 (Homie): the liquefied map, line and name dissolve like ink in water: swirled by an evolving curl
        flow, pushed out from Senegal, spreading and thinning until the frame is clear (alpha 0). Real time: INK0-INK1 new s."""
        p = ssf(INK0, INK1, T_NEW)
        if p <= 0:
            self.alpha = np.ones((self.H, self.W), F32)
            return
        px = self.ctx.px
        if not hasattr(self, 'ink_v'):
            vs = []
            for sd in (121, 122):
                psi = fractal(self.H, self.W, np.random.default_rng(sd), scales=(px(700), px(260)), gains=(1, 0.45))
                psi = cv2.GaussianBlur(psi, (0, 0), px(30))
                vx = cv2.Sobel(psi, cv2.CV_32F, 0, 1, ksize=3)
                vy = -cv2.Sobel(psi, cv2.CV_32F, 1, 0, ksize=3)
                n = max(float(np.percentile(np.hypot(vx, vy), 95)), 1e-6)
                vs.append((vx / n, vy / n))
            self.ink_v = vs
        (ax, ay), (bx, by) = self.ink_v
        c, s_ = np.cos(0.15 * T_NEW), np.sin(0.15 * T_NEW)
        vx, vy = (c * ax + s_ * bx).astype(F32), (c * ay + s_ * by).astype(F32)
        d = px(140) * p ** 1.3
        X, Y = self.gx.copy(), self.gy.copy()
        for _ in range(4):
            sx = cv2.remap(vx, X, Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
            sy = cv2.remap(vy, X, Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
            X, Y = X - sx * d / 4, Y - sy * d / 4
        pin = self.view(t)[1]
        rx, ry = self.gx - pin[0], self.gy - pin[1]
        rn = np.maximum(np.hypot(rx, ry), 1.0)
        push = px(60) * p ** 2
        X, Y = (X - rx / rn * push).astype(F32), (Y - ry / rn * push).astype(F32)
        col = cv2.remap(canvas, X, Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        nad = cv2.remap(self.dnoise, X, Y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        al = ss(0, 1, np.clip((1 - p) * 1.7 - 0.7 * (1 - nad), 0, 1)).astype(F32)
        sg = px(2 + 40 * p ** 1.5)
        canvas[:] = np.clip(cv2.GaussianBlur(col, (0, 0), sg), 0, None)
        self.alpha = np.clip(cv2.GaussianBlur(al, (0, 0), sg), 0, 1).astype(F32)

    def draw_route7(self, canvas, t):
''')
# render loops
rep("""    for i in range(n0, n1):
        t = i / FPS
        fr = (render_frame(ctx, S, t, dt) * 65535 + 0.5).astype(np.uint16)""", """    for i in range(n0, n1):
        t = retime(i / FPS)
        fr = (render_frame(ctx, S, t, dt) * 65535 + 0.5).astype(np.uint16)""")
rep("""    mux_audio(outdir, n0 / FPS, n1 / FPS)
    print('wrote', outdir)""", """    if RETIME_FR:                                   # Meeting 8: no scratch mux; the review composite carries Darrin's wav
        for name in ('LEFT', 'CENTRE', 'RIGHT'):
            os.replace(os.path.join(outdir, f'S6_{name}_picture.mov'), os.path.join(outdir, f'S6_{name}.mov'))
    else:
        mux_audio(outdir, n0 / FPS, n1 / FPS)
    print('wrote', outdir)""")
rep("""    a = ap.parse_args()
    global GEN_FLAG, GEN_SMOKE, V6, V7, V7_ALPHA, V7_FEATHER
""", """    ap.add_argument('--retime-fr', action='store_true',
                    help="Meeting 8: retimed to Darrin's French track (121.25 s; --at/--start/--end in NEW s), fleur-de-lis RIGHT "
                         'flag, ink dissolve to alpha, no scratch mux')
    a = ap.parse_args()
    global GEN_FLAG, GEN_SMOKE, V6, V7, V7_ALPHA, V7_FEATHER, RETIME_FR
    RETIME_FR = a.retime_fr
    if RETIME_FR and a.end == DUR:
        a.end = FR_DUR
""")
# stills: render at t_old, NAME by the new second (tn == ts without the switch, so v14 names are unchanged)
rep("""            for i in range(int(a.warm * FPS), 0, -1):               # run --warm s (3 by default) up to it so particles and fragments exist
                render_frame(ctx, S, max(0.0, ts - i * dt), dt)
            fr = (render_frame(ctx, S, ts, dt) * 255).astype(np.uint8)""", """            tn = ts
            for i in range(int(a.warm * FPS), 0, -1):               # run --warm s (3 by default) up to it so particles and fragments exist
                render_frame(ctx, S, retime(max(0.0, tn - i * dt)), dt)
            ts = retime(tn)
            fr = (render_frame(ctx, S, ts, dt) * 255).astype(np.uint8)""")
rep("cv2.imwrite(os.path.join(a.stills, f's6_{ts:06.1f}_{nm}.png'), cv2.cvtColor(o, cv2.COLOR_RGB2BGR))",
    "cv2.imwrite(os.path.join(a.stills, f's6_{tn:06.1f}_{nm}.png'), cv2.cvtColor(o, cv2.COLOR_RGB2BGR))")
rep("cv2.imwrite(os.path.join(a.stills, f's6_{ts:06.1f}.png'), cv2.cvtColor(caption(ctx, fr, ts), cv2.COLOR_RGB2BGR))",
    "cv2.imwrite(os.path.join(a.stills, f's6_{tn:06.1f}.png'), cv2.cvtColor(caption(ctx, fr, ts), cv2.COLOR_RGB2BGR))")
rep("""            render_frame(ctx, S, max(0.0, (n0 - i) / FPS), dt)""", """            render_frame(ctx, S, retime(max(0.0, (n0 - i) / FPS)), dt)""")
rep("""    for i in range(n0, n1):
        t = i / FPS
        fr = (render_frame(ctx, S, t, dt) * 255).astype(np.uint8)""", """    for i in range(n0, n1):
        t = retime(i / FPS)
        fr = (render_frame(ctx, S, t, dt) * 255).astype(np.uint8)""")
open(p, 'w', encoding='utf-8').write(s)
print('patched', p)
