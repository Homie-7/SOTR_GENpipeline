"""2026-10-02: the end-of-project cleanup (Homie: "Delete everything unnecessary. Only keep what we need… and stuff that we
might need in the future to keep working off… do a full project cleanup, recompartmentalize everything").

Claude does not hard-delete (a standing safety rule), so everything unneeded is MOVED into one bin per drive, which Homie
empties himself:  D:/SOTR/_DELETE_ME_2026-10-02/   and   G:/SOTR/HF/_DELETE_ME_2026-10-02/
Every move is a rename on the same drive (nothing copied, nothing lost until the bin is emptied), and every move is
written to D:/SOTR/CLEANUP_2026-10-02_moves.tsv (old -> new), so the whole thing can be reversed.

KEEP = what plays (01), what built it and can rebuild it (approved generated sources, clean masters, edge kits, the b9
candle takes, the Scene 6 loops, recipes), what the team uses (presentations, Homie's comp/), and the one previous
approved version of a show file (studio b9 v3). Everything else: the bin.

  python tools/cleanup_2026-10-02.py plan            prints the plan for D: (no changes)
  python tools/cleanup_2026-10-02.py run             does it on D:
  python tools/cleanup_2026-10-02.py t9 [--dry]      the same layout on the T9: renames what matches by size, bins the rest
"""
import os
import sys
import time

ROOT_D = 'D:/SOTR'
ROOT_G = 'G:/SOTR/HF'
BIN = '_DELETE_ME_2026-10-02'
MOVES = 'D:/SOTR/CLEANUP_2026-10-02_moves.tsv'

T = '03_TESTS_IN_PROGRESS'
F = '01_FINAL_FOR_SHOW'
A = '02_APPROVED_BUILDING_BLOCKS'
W = '04_WORKING_FILES'

# old path (relative to SOTR_MEDIA) -> new path (relative to SOTR_MEDIA). A folder rule moves the whole folder.
KEEP = [
    (f'{F}/4_HD_1080_same_files', f'{F}/3_HD_1080_fallback'),
    (f'{F}/3_CLEAN_no_edge', '03_CLEAN_MASTERS_no_edge'),
    # Scene 6 generated: the probe takes + Sequels (sources) and the loops render_s6.py reads (1080 and 4K)
    (f'{T}/S6_generated/S6-FLAG_v1_A.mp4', f'{A}/S6_generated/S6-FLAG_v1_A.mp4'),
    (f'{T}/S6_generated/S6-FLAG_v2.mp4', f'{A}/S6_generated/S6-FLAG_v2.mp4'),
    (f'{T}/S6_generated/S6-SMOKE_v1.mp4', f'{A}/S6_generated/S6-SMOKE_v1.mp4'),
    (f'{T}/S6_generated/S6-SMOKE_v2.mp4', f'{A}/S6_generated/S6-SMOKE_v2.mp4'),
    (f'{T}/S6_generated/S6-FLAG_loop.mov', f'{A}/S6_generated/S6-FLAG_loop.mov'),
    (f'{T}/S6_generated/S6-SMOKE_loop.mov', f'{A}/S6_generated/S6-SMOKE_loop.mov'),
    (f'{T}/S6_generated/4K', f'{A}/S6_generated/4K'),
    # studio b9 (candle arc v5): the generated takes and the candle the show file is painted on
    (f'{T}/studio_candle_arc/S9-STU-L-B9_v1.mp4', f'{A}/studio_b9_candle/S9-STU-L-B9_v1.mp4'),
    (f'{T}/studio_candle_arc/S9-STU-L-B9_v1_long.mp4', f'{A}/studio_b9_candle/S9-STU-L-B9_v1_long.mp4'),
    (f'{T}/studio_candle_arc/B9_candle_965f.mov', f'{A}/studio_b9_candle/B9_candle_965f.mov'),
    (f'{T}/studio_candle_arc/B9_candle_965f_aligned.mov', f'{A}/studio_b9_candle/B9_candle_965f_aligned.mov'),
    # the frozen generated breaks every edge file is drawn from (court burns by script, needs no kit)
    (f'{T}/edge_flow/kit_salon.npz', f'{W}/edge_kits/kit_salon.npz'),
    (f'{T}/edge_flow/kit_studio.npz', f'{W}/edge_kits/kit_studio.npz'),
    # recipes: how the current show files were built
    (f'{T}/studio_candle_arc/build.sh', f'{W}/build_recipes/studio_candle_arc_build_v4.sh'),
    (f'{T}/studio_candle_arc/build_v5.sh', f'{W}/build_recipes/studio_candle_arc_build_v5.sh'),
    (f'{T}/scene9_fix_v4/FIX.sh', f'{W}/build_recipes/scene9_fix_v4_FIX.sh'),
    (f'{T}/OVERNIGHT_2026-09-30.sh', f'{W}/build_recipes/OVERNIGHT_2026-09-30.sh'),
    (f'{T}/OVERNIGHT_PART2_2026-09-30.sh', f'{W}/build_recipes/OVERNIGHT_PART2_2026-09-30.sh'),
    # the 4K promotion: script, sha256 manifest, check results
    (f'{T}/upscale_4k/promote_4k.py', f'{W}/4K_records/promote_4k.py'),
    (f'{T}/upscale_4k/MANIFEST_4K_2026-10-01.txt', f'{W}/4K_records/MANIFEST_4K_2026-10-01.txt'),
    (f'{T}/upscale_4k/results_v3.txt', f'{W}/4K_records/results_v3.txt'),
    (f'{T}/upscale_4k/overrides_v3.txt', f'{W}/4K_records/overrides_v3.txt'),
    (f'{T}/upscale_4k/JOBS_v3.txt', f'{W}/4K_records/JOBS_v3.txt'),
    (f'{T}/upscale_4k/promote_4k.log', f'{W}/4K_records/promote_4k.log'),
    (f'{T}/upscale_4k/queue5.log', f'{W}/4K_records/queue5.log'),
    # the previous approved studio b9 (v5 replaced it 2026-10-01): the one fallback kept
    (f'{T}/superseded/studio_b9_v3', f'{W}/superseded/studio_b9_v3'),
    # Scene 6's approved animatic (v4): the look the client signed off
    (f'{T}/S6_animatic/S6-ANIMATIC_v4.mp4', f'{W}/S6-ANIMATIC_v4_approved.mp4'),
]
# kept where they are (listed so nothing under them is binned)
STAY = [f'{F}/00_READ_ME_FIRST.txt', f'{F}/1_PLAY_THESE_IN_ORDER', f'{F}/2_BACKUP_LOOPS_for_operator',
        f'{A}/clips', f'{A}/stills', f'{A}/S6_public_domain', '06_PRESENTATIONS', 'comp', 'README.txt',
        '05_REFERENCE_UPLOADS/SAL-R-LOOP_comp_f0.png', '05_REFERENCE_UPLOADS/SAL-R-LOOP_comp_upload.mp4',
        '05_REFERENCE_UPLOADS/SAL-R-LOOP_comp_upload_4s.mp4', '05_REFERENCE_UPLOADS/SAL-R-clean-gerard-f300.png',
        '05_REFERENCE_UPLOADS/STU-L-LOOP_comp_f0.png', '05_REFERENCE_UPLOADS/STU-L-LOOP_comp_upload_4s.mp4']


def log(f, *a):
    s = time.strftime('%H:%M:%S ') + ' '.join(str(x) for x in a)
    print(s, flush=True)
    if f:
        f.write(s + '\n'); f.flush()


def files_under(p):
    if os.path.isfile(p):
        return [p]
    out = []
    for r, _, fs in os.walk(p):
        out += [os.path.join(r, x).replace('\\', '/') for x in fs]
    return out


def plan(root):
    """[(old_abs, new_abs)] for one drive's SOTR folder: KEEP renames + everything else under SOTR_MEDIA to the bin"""
    M = f'{root}/SOTR_MEDIA'
    moves, kept = [], set()
    for old, new in KEEP:
        if os.path.exists(f'{M}/{old}'):
            moves.append((f'{M}/{old}', f'{M}/{new}'))
            kept.update(files_under(f'{M}/{old}'))
    for s in STAY:
        if os.path.exists(f'{M}/{s}'):
            kept.update(files_under(f'{M}/{s}'))
    for f in files_under(M):
        if f not in kept:
            moves.append((f, f'{root}/{BIN}/SOTR_MEDIA/' + f[len(M) + 1:]))
    return moves


def apply(moves, logf):
    with open(MOVES, 'a', encoding='utf-8') as tsv:
        for old, new in moves:
            if os.path.exists(new):
                log(logf, 'EXISTS, skipped:', new); continue
            os.makedirs(os.path.dirname(new), exist_ok=True)
            os.replace(old, new)
            tsv.write(f'{old}\t{new}\n')
    # empty folders left behind under SOTR_MEDIA (the keep moves emptied them): remove only if truly empty
    for r, ds, fs in sorted(os.walk(moves[0][0].split('/SOTR_MEDIA/')[0] + '/SOTR_MEDIA'), key=lambda x: -len(x[0])):
        if not os.listdir(r):
            os.rmdir(r)


def summary(moves, root):
    keep = [m for m in moves if f'/{BIN}/' not in m[1]]
    binned = [m for m in moves if f'/{BIN}/' in m[1]]
    size = sum(os.path.getsize(o) for o, _ in binned if os.path.isfile(o))
    print(f'{root}: {len(keep)} keep-renames, {len(binned)} files to the bin ({size / 1e9:.1f} GB)')
    return keep, binned


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'plan'
    if cmd in ('plan', 'run'):
        mv = plan(ROOT_D)
        keep, binned = summary(mv, ROOT_D)
        arch = f'{ROOT_D}/SOTR_MEDIA_ARCHIVE'
        if cmd == 'plan':
            for o, n in keep:
                print('KEEP', o[len(ROOT_D) + 12:], '->', n[len(ROOT_D) + 12:])
            for o, n in binned:
                print('BIN ', o[len(ROOT_D) + 12:], f'{os.path.getsize(o) / 1e6:.0f}M')
            print('BIN  SOTR_MEDIA_ARCHIVE (whole folder)' if os.path.isdir(arch) else '')
        else:
            lf = open(f'{ROOT_D}/CLEANUP_2026-10-02.log', 'a', encoding='utf-8')
            apply(mv, lf)
            for x in ['SOTR_MEDIA_ARCHIVE', '_OVERNIGHT_PART2_2026-09-30.log', '_OVERNIGHT_PART2_2026-09-30.sh',
                      '_OVERNIGHT_PART2_console.txt', '_OVERNIGHT_PART2_log_before_migration.txt']:
                if os.path.exists(f'{ROOT_D}/{x}'):
                    os.makedirs(f'{ROOT_D}/{BIN}', exist_ok=True)
                    os.replace(f'{ROOT_D}/{x}', f'{ROOT_D}/{BIN}/{x}')
                    open(MOVES, 'a', encoding='utf-8').write(f'{ROOT_D}/{x}\t{ROOT_D}/{BIN}/{x}\n')
            log(lf, 'D: CLEANUP DONE', len(keep), 'kept-renamed,', len(binned), 'binned')
    elif cmd == 't9':
        mv = plan(ROOT_G)
        keep, binned = summary(mv, ROOT_G)
        if '--dry' in sys.argv:
            for o, n in keep:
                print('KEEP', o[len(ROOT_G) + 12:], '->', n[len(ROOT_G) + 12:])
        else:
            lf = open(f'{ROOT_D}/CLEANUP_2026-10-02.log', 'a', encoding='utf-8')
            apply(mv, lf)
            log(lf, 'T9 CLEANUP DONE', len(keep), 'kept-renamed,', len(binned), 'binned')
