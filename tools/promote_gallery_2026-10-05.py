"""2026-10-05 (evening): promote the APPROVED gallery (Scenes 1 + 10) into the client delivery.

Homie approved the gallery show files ("I guess we can call it finished") and asked to finish the puddle. Moves:

  01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/   + S1_a_<WALL>_gallery.mov, S1_b_<WALL>_gallery-blackout.mov, S10_<WALL>_gallery.mov
  01_FINAL_FOR_SHOW/2_BACKUP_LOOPS_for_operator/  + the 4K S1-and-S10_<WALL>_gallery_LIT_HOLD_loop / S1_<WALL>_..._DARK_HOLD_loop
  01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector/  + S1_a / S1_a2 / S1_b / S10 _FLOOR_gallery*.mov
  04_WORKING_FILES/superseded/S1_gallery/walls_LIT_v2_DARK_v1/   the walls before the re-hang
  04_WORKING_FILES/superseded/S1_gallery/puddle_v6_eased_stop/   the eased-stop return (replaced by the FLOW)
  <root>/_DELETE_ME_2026-10-05/…/2_PUDDLE_RETURN_in_progress/    the v4 (dome, rejected) and v5 (probe) takes

Every move is a RENAME on the same drive, checked by size, logged to <root>/PROMOTE_GALLERY_2026-10-05_moves.tsv. An
existing destination is never overwritten; a missing source is skipped and reported (the PC copies S1 from the T9).

  python tools/promote_gallery_2026-10-05.py "/Volumes/DMD T9/SOTR/HF" plan|run
"""
import os
import sys
import time

M = 'SOTR_MEDIA'
G = '04_WORKING_FILES/S1_gallery'
REV = G + '/3_SHOW_FILES_1080_for_review'
WALLS = G + '/1_READY_for_show_build/walls'
PR = G + '/2_PUDDLE_RETURN_in_progress'
SUP = '04_WORKING_FILES/superseded/S1_gallery'
BIN = '_DELETE_ME_2026-10-05'


def plan():
    mv = []
    for w in ('LEFT', 'CENTRE', 'RIGHT'):
        for f in (f'S1_a_{w}_gallery.mov', f'S1_b_{w}_gallery-blackout.mov', f'S10_{w}_gallery.mov'):
            mv.append((f'{M}/{REV}/{f}', f'{M}/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/{f}'))
        for f in (f'S1-and-S10_{w}_gallery_LIT_HOLD_loop.mov', f'S1_{w}_gallery_DARK_HOLD_loop.mov'):
            mv.append((f'{M}/{REV}/4K_backup_loops/{f}', f'{M}/01_FINAL_FOR_SHOW/2_BACKUP_LOOPS_for_operator/{f}'))
    for f in ('S1_a_FLOOR_gallery.mov', 'S1_a2_FLOOR_gallery-puddle-returns.mov', 'S1_b_FLOOR_gallery-blackout.mov',
              'S10_FLOOR_gallery.mov'):
        mv.append((f'{M}/{REV}/FLOOR_only_if_a_floor_projector/{f}',
                   f'{M}/01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector/{f}'))
    for w in 'LCR':
        sz = '1800x1080' if w == 'C' else '1440x1080'
        for f in (f'S1-GAL-{w}_LIT_v2_native.png', f'S1-GAL-{w}_LIT_v2_{sz}.png', f'S1-GAL-{w}_DARK_v1_{sz}.png'):
            mv.append((f'{M}/{WALLS}/{f}', f'{M}/{SUP}/walls_LIT_v2_DARK_v1/{f}'))
    for f in ('S1-GAL_LIT_v2_SEAM_4680x1080.png', 'S1-GAL_DARK_v1_SEAM_4680x1080.png'):
        mv.append((f'{M}/{WALLS}/{f}', f'{M}/{SUP}/walls_LIT_v2_DARK_v1/{f}'))
    for f in ('S1-GAL-PUDDLE-RETURN_v6_FLOOR_lit_1920x1080.mov', 'S1-GAL-PUDDLE-RETURN_v6_FLOOR_dark_1920x1080.mov',
              'S1-GAL-PUDDLE-RETURN_v6_REVIEW_lit_then_dark_fullfloor+zoom.mp4'):
        mv.append((f'{M}/{PR}/{f}', f'{M}/{SUP}/puddle_v6_eased_stop/{f}'))
    for f in ('S1-GAL-PUDDLE-RETURN_v4.mp4', 'S1-GAL-PUDDLE-RETURN_v5.mp4'):
        mv.append((f'{M}/{PR}/{f}', f'{BIN}/{M}/{PR}/{f}'))
    return mv


def main():
    root, mode = sys.argv[1], sys.argv[2]
    log = os.path.join(root, 'PROMOTE_GALLERY_2026-10-05_moves.tsv')
    done = skipped = 0
    for a, b in plan():
        src, dst = os.path.join(root, a), os.path.join(root, b)
        if not os.path.exists(src):
            print('SKIP (missing)', a); skipped += 1; continue
        if os.path.exists(dst):
            print('SKIP (exists) ', b); skipped += 1; continue
        print(('MOVE ' if mode == 'run' else 'plan ') + a + '  ->  ' + b)
        if mode != 'run':
            continue
        size = os.path.getsize(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.rename(src, dst)
        assert os.path.getsize(dst) == size, dst
        tw =os.path.join(os.path.dirname(src), '._' + os.path.basename(src))
        if os.path.exists(tw):
            os.rename(tw, os.path.join(os.path.dirname(dst), '._' + os.path.basename(dst)))
        with open(log, 'a') as fh:
            fh.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}\t{a}\t{b}\t{size}\n')
        done += 1
    print(f'{mode}: {done} moved, {skipped} skipped')


if __name__ == '__main__':
    main()
