r"""F26 (25 Nov): make 01_FINAL_FOR_SHOW the ONE hand-over folder, in script order, one subfolder per scene.
Promotes the S9 court 4K finals (S9_4K_final/out) and the S6 French finals (*_FRsound.mov).
Old show files -> 04_WORKING_FILES/superseded/<group>/ with the version added. Unneeded -> D:\SOTR\_DELETE_ME_2026-11-25\.
Never deletes. Same-drive moves are renames; every moved file is sha256'd first and logged to MOVES TSV.
Usage: handover_2026-11-25.py [--dry]      Then: --t9 applies the same TSV on G:\SOTR\HF (moves within G, sha checked)."""
import os, sys, hashlib, glob, time

ROOT = {'D': r'D:\SOTR', 'G': r'G:\SOTR\HF'}
DRY, T9 = '--dry' in sys.argv, '--t9' in sys.argv
TSV = r'D:\SOTR\HANDOVER_2026-11-25_moves.tsv'
M = 'SOTR_MEDIA'
FS = M + r'\01_FINAL_FOR_SHOW'
P, H = FS + r'\1_PLAY_THESE_IN_ORDER', FS + r'\3_HD_1080_fallback\1_PLAY_THESE_IN_ORDER'
W = M + r'\04_WORKING_FILES'
SUP = W + r'\superseded'
BIN = r'_DELETE_ME_2026-11-25'
SC = {'S1': 'S01_Au-Louvre', 'S2': 'S02_painting-melt', 'S4': 'S04_the-Alps', 'S5': 'S05_the-camps',
      'S6': 'S06_Napoleonic-wars', 'S9': 'S09_the-Aftermath', 'S10': 'S10_back-at-the-Louvre'}
WALLS = ('LEFT', 'CENTRE', 'RIGHT')


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        while (b := f.read(8 << 20)):
            h.update(b)
    return h.hexdigest()


def plan():
    r"""(src rel, dst rel) pairs, rel to D:\SOTR (= G:\SOTR\HF). Built from what is on D: now."""
    mv, D = [], ROOT['D']
    ls = lambda rel: sorted(os.listdir(os.path.join(D, rel))) if os.path.isdir(os.path.join(D, rel)) else []
    # 1. superseded: old S6 English + old S9 court, show 4K + 1080 + CLEAN
    for w in WALLS:
        mv.append((P + rf'\S6_{w}_wars.mov', SUP + rf'\S6_wars_v14-EN_165s\S6_{w}_wars_v14-EN.mov'))
        mv.append((H + rf'\S6_{w}_wars.mov', SUP + rf'\S6_wars_v14-EN_165s\1080\S6_{w}_wars_v14-EN.mov'))
        mv.append((M + rf'\03_CLEAN_MASTERS_no_edge\S6_{w}_wars_CLEAN.mov',
                   SUP + rf'\S6_wars_v14-EN_165s\CLEAN\S6_{w}_wars_CLEAN_v14-EN.mov'))
    for b in ('b3', 'b5', 'b7'):
        n = f'S9_{b}_CENTRE_court'
        mv.append((P + rf'\{n}.mov', SUP + rf'\S9_court_GENJUDGE_pre-F25\{n}_pre-F25.mov'))
        mv.append((H + rf'\{n}.mov', SUP + rf'\S9_court_GENJUDGE_pre-F25\1080\{n}_pre-F25.mov'))
        mv.append((M + rf'\03_CLEAN_MASTERS_no_edge\{n}_CLEAN.mov',
                   SUP + rf'\S9_court_behind-paper_CLEAN\{n}_CLEAN_behind-paper.mov'))
    # 2. promote the new finals
    for w in WALLS:
        mv.append((W + rf'\S6_4K_final\S6_{w}_FRsound.mov', P + rf'\{SC["S6"]}\S6_{w}_wars.mov'))
        mv.append((W + rf'\S6_1080_final\S6_{w}_FRsound.mov', H + rf'\{SC["S6"]}\S6_{w}_wars.mov'))
    for b in ('b3', 'b5', 'b7'):
        n = f'S9_{b}_CENTRE_court'
        mv.append((W + rf'\S9_4K_final\out\{n}_4K.mov', P + rf'\{SC["S9"]}\{n}.mov'))
        mv.append((W + rf'\S9_4K_final\out\{n}_1080.mov', H + rf'\{SC["S9"]}\{n}.mov'))
    # 3. every other show file into its scene folder (names unchanged)
    done = {s for s, _ in mv}
    for rel, dstroot in ((P, P), (H, H)):
        for fn in ls(rel):
            src = rel + '\\' + fn
            if src in done or fn in SC.values():
                continue
            sc = fn.split('_')[0].split('-')[0]
            if sc in SC:
                if os.path.isdir(os.path.join(D, src)):
                    for f2 in ls(src):
                        mv.append((src + '\\' + f2, dstroot + rf'\{SC[sc]}\{fn}\{f2}'))
                else:
                    mv.append((src, dstroot + rf'\{SC[sc]}\{fn}'))
    s2 = FS + r'\6_NEW_S2_PAINTING_MELT_play_in_show'
    for fn in ls(s2 + r'\1_PLAY_IN_SHOW_4K'):
        mv.append((s2 + rf'\1_PLAY_IN_SHOW_4K\{fn}', P + rf'\{SC["S2"]}\{fn}'))
    for fn in ls(s2 + r'\2_HD_1080_fallback'):
        mv.append((s2 + rf'\2_HD_1080_fallback\{fn}', H + rf'\{SC["S2"]}\{fn}'))
    mv.append((s2 + r'\00_READ_ME_S2_PAINTING_MELT.txt', P + rf'\{SC["S2"]}\_READ_ME_S2_painting-melt.txt'))
    # 4. bin: the old court strike loops (do not match the generated judge) + dead tests + duplicates
    for base in (FS + r'\2_BACKUP_LOOPS_for_operator', FS + r'\3_HD_1080_fallback\2_BACKUP_LOOPS_for_operator',
                 M + r'\03_CLEAN_MASTERS_no_edge\backups'):
        for fn in ls(base):
            if 'court_strike-size' in fn:
                mv.append((base + '\\' + fn, BIN + '\\' + base + '\\' + fn))
    for d in ('S9_idle_judge_test', 'S9_judge_opaque_test', 'S9_court_behind_paper', 'S6_french_review',
              'S6_map_to_ship_review'):
        for root, _, files in os.walk(os.path.join(D, W, d)):
            for fn in files:
                rel = os.path.relpath(os.path.join(root, fn), D)
                mv.append((rel, BIN + '\\' + rel))
    for w in WALLS:
        for d in ('S6_4K_final', 'S6_1080_final'):
            mv.append((W + rf'\{d}\S6_{w}.mov', BIN + rf'\{W}\{d}\S6_{w}_no-sound.mov'))
    for f in glob.glob(os.path.join(D, W, r'S9_4K_final\out\*_nosnd.mov')):
        rel = os.path.relpath(f, D)
        mv.append((rel, BIN + '\\' + rel))
    return mv


def main():
    if T9:
        G = ROOT['G']
        rows = [l.rstrip('\n').split('\t') for l in open(TSV, encoding='utf-8')][1:]
        out = open(TSV.replace('.tsv', '_T9.tsv'), 'a', encoding='utf-8')
        for st, s, d, h, _ in rows:
            if st != 'MOVED':
                continue
            gs, gd = os.path.join(G, s), os.path.join(G, d)
            if not os.path.exists(gs):
                out.write(f'T9_NOSRC\t{s}\n'); continue      # new on D: (copied later by t9_sync)
            if os.path.exists(gd):
                out.write(f'T9_DSTEXISTS\t{d}\n'); continue
            if DRY:
                out.write(f'T9_WOULD\t{s}\t{d}\n'); continue
            hg = sha(gs)
            if hg != h:                                        # an old T9 version: bin it, t9_sync copies the new one
                bp = os.path.join(G, BIN, s)
                os.makedirs(os.path.dirname(bp), exist_ok=True); os.rename(gs, bp)
                out.write(f'T9_OLDVER_BINNED\t{s}\t{hg}\n'); continue
            os.makedirs(os.path.dirname(gd), exist_ok=True); os.rename(gs, gd)
            out.write(f'T9_MOVED\t{s}\t{d}\t{h}\n'); out.flush()
        print('DONE T9')
        return
    mv = plan()
    D = ROOT['D']
    new = not os.path.exists(TSV)
    out = open(TSV if not DRY else TSV.replace('.tsv', '_dry.tsv'), 'a', encoding='utf-8')
    if new or DRY:
        out.write('status\tsrc\tdst\tsha256\ttime\n')
    for s, d in mv:
        ps, pd = os.path.join(D, s), os.path.join(D, d)
        if not os.path.exists(ps):
            out.write(f'NOSRC\t{s}\t{d}\t\t\n'); continue
        if os.path.exists(pd):
            out.write(f'DSTEXISTS\t{s}\t{d}\t\t\n'); continue
        if DRY:
            out.write(f'WOULD\t{s}\t{d}\t{os.path.getsize(ps)}\t\n'); continue
        h = sha(ps)
        os.makedirs(os.path.dirname(pd), exist_ok=True)
        os.rename(ps, pd)
        out.write(f'MOVED\t{s}\t{d}\t{h}\t{time.strftime("%H:%M:%S")}\n'); out.flush()
    if not DRY:   # remove folders left empty by the moves (empty only; os.rmdir refuses anything else)
        for base in (FS, os.path.join(W, 'S6_4K_final'), os.path.join(W, 'S6_1080_final')):
            for root, dirs, files in sorted(os.walk(os.path.join(D, base)), key=lambda x: -len(x[0])):
                if not os.listdir(root):
                    os.rmdir(root)
    print('DONE', len(mv), 'moves')


main()
