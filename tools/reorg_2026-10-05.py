"""2026-10-05: the handover reorganisation (Homie: "do some file management and put all the relevant files in production
ready… things that I'm gonna hand over… there's so many files here and there, I'm not sure which one is which").
His calls: ALL approved scenes go into the handover folder now (Scenes 4 and 5 join 6 and 9; the gallery joins when it
is built); Scene 5's Rich dusk PLAYS, its Cold dusk sits in a separate client-option folder.

  01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/   + S4_<WALL>_alps.mov, S5_<WALL>_camps.mov   (front = CENTRE)
  01_FINAL_FOR_SHOW/4_CLIENT_OPTION_S5_cold_dusk/  S5_<WALL>_camps_cold-dusk.mov
  01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector/  S4_FLOOR_alps.mov, S5_FLOOR_camps.mov (the floor is unconfirmed)
  02_APPROVED_BUILDING_BLOCKS/S1_gallery/    the gallery's chosen generated takes + the four public-domain paintings
  04_WORKING_FILES/S1_gallery/1_READY_for_show_build/   the finished walls (LIT v2, DARK v1) and floor v2 pieces
  04_WORKING_FILES/S1_gallery/2_PUDDLE_RETURN_in_progress/   the glimmer test (look OK'd) until the new water exists
  04_WORKING_FILES/superseded/S1_gallery/   versions that were used and then replaced (pale floor, LIT v1, vanish v1)
  04_WORKING_FILES/superseded/S4_alps_grade_v1/   the first Alps grade (S4), replaced by A4
  <root>/_DELETE_ME_2026-10-05/              unchosen and rejected takes (Homie empties it; Claude never hard-deletes)

Every move is a RENAME on the same drive (instant, no copy, nothing lost), checked by size after, and written to
<root>/REORG_2026-10-05_moves.tsv (old -> new) so it can be reversed. A destination that already exists is never
overwritten. Missing sources are skipped and reported, so the PC can run the same script on D: (it has Scenes 4/5 but
not yet the gallery, whose master is the T9: copy S1 over in its NEW layout afterwards, sha256 verified).

  python tools/reorg_2026-10-05.py "/Volumes/DMD T9/SOTR/HF" plan      prints the plan (no changes)
  python tools/reorg_2026-10-05.py "/Volumes/DMD T9/SOTR/HF" run       does it      (on the PC: D:/SOTR, or G:/SOTR/HF)
"""
import os
import sys
import time

BIN = '_DELETE_ME_2026-10-05'
M = 'SOTR_MEDIA'
G = '04_WORKING_FILES/S1_gallery'
BB = '02_APPROVED_BUILDING_BLOCKS/S1_gallery'
READY = G + '/1_READY_for_show_build'
SUP = '04_WORKING_FILES/superseded/S1_gallery'
PLAY = '01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER'
OPT = '01_FINAL_FOR_SHOW/4_CLIENT_OPTION_S5_cold_dusk'
FLOOR = '01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector'
WALL = {'front': 'CENTRE', 'left': 'LEFT', 'right': 'RIGHT', 'bottom': 'FLOOR'}


def plan():
    """(src, dst) pairs, relative to SOTR_MEDIA. dst None = the bin (same relative path inside it)."""
    mv = []
    # --- the handover: Scenes 4 and 5 -----------------------------------------------------------------------------
    for a, w in WALL.items():
        play = FLOOR if w == 'FLOOR' else PLAY     # the floor renders apart: a floor projector is not confirmed
        mv.append((f'04_WORKING_FILES/S4_alps_grade_v2/A4_matched/S4_alps_{a}.mov', f'{play}/S4_{w}_alps.mov'))
        mv.append((f'04_WORKING_FILES/S5_battlefield_grade/S5_PRIMARY_rich_dusk/S5_camps_{a}.mov', f'{play}/S5_{w}_camps.mov'))
        mv.append((f'04_WORKING_FILES/S5_battlefield_grade/S5_SECONDARY_cold_dusk/S5_camps_{a}.mov',
                   f'{OPT}/S5_{w}_camps_cold-dusk.mov'))
    mv.append(('04_WORKING_FILES/S4_alps_grade', '04_WORKING_FILES/superseded/S4_alps_grade_v1'))
    # --- the gallery: chosen generated sources -> building blocks -------------------------------------------------
    for f in ['room/S1-GAL-ROOM_v1_56306f43.png', 'centre/S1-GAL-C_v1_2800713a.png', 'left/S1-GAL-L_v1_9194a1ce.png',
              'right/S1-GAL-R_v1_a77585ae.png', 'floor/S1-GAL-FLOOR_v2_a650a2ac.png']:
        mv.append((f'{G}/{f}', f'{BB}/{os.path.basename(f)}'))
    for f in ['src_SOTR_louisXVI_callet.jpg', 'src_SOTR_marieantoinette_gautierdagoty.jpg', 'src_SOTR_napoleon_ingres.jpg',
              'src_SOTR_raft_gericault.jpg']:
        mv.append((f'{G}/sources/{f}', f'{BB}/paintings/{f}'))
    # --- ready for the show build --------------------------------------------------------------------------------
    for w, size in [('C', '1800x1080'), ('L', '1440x1080'), ('R', '1440x1080')]:
        for f in [f'S1-GAL-{w}_LIT_v2_{size}.png', f'S1-GAL-{w}_LIT_v2_native.png', f'S1-GAL-{w}_DARK_v1_{size}.png']:
            mv.append((f'{G}/finished/{f}', f'{READY}/walls/{f}'))
    for f in ['S1-GAL_LIT_v2_SEAM_4680x1080.png', 'S1-GAL_DARK_v1_SEAM_4680x1080.png', 'S1-GAL_room_light_v2.json']:
        mv.append((f'{G}/finished/{f}', f'{READY}/walls/{f}'))
    mv.append((f'{G}/floor/S1-GAL-FLOOR_v2_a650a2ac_desheen.png', f'{READY}/floor/S1-GAL-FLOOR_v2_a650a2ac_desheen.png'))
    for f in ['S1-GAL-FLOOR_DRY_1920x1080.png', 'S1-GAL-FLOOR_SPILL_1920x1080.png', 'S1-GAL-FLOOR_DRY_HOLD_1920x1080.mov',
              'S1-GAL-FLOOR_SPILL_HOLD_1920x1080.mov', 'S1-GAL-FLOOR_VANISH_1920x1080.mov',
              'S1-GAL-FLOOR_VANISH_REVIEW_spill-vanish-dry_full+zoom.mp4']:
        mv.append((f'{G}/finished/floor_v2/{f}', f'{READY}/floor/{f}'))
    mv.append((f'{G}/finished/S1-GAL_REVIEW_walls+floor_v2_SPILL.jpg', f'{READY}/S1-GAL_REVIEW_walls+floor_v2_SPILL.jpg'))
    # --- the puddle return, in progress --------------------------------------------------------------------------
    for f in ['GLIMMER_TEST_REVIEW_lit_then_dark_fullfloor+zoom.mp4', 'GLIMMER_TEST_dark_hold_1920x1080.mov',
              'GLIMMER_TEST_lit_on_v2_1920x1080.mov', 'SHA256SUMS_2026-10-05.txt']:
        mv.append((f'{G}/puddle_return/{f}', f'{G}/2_PUDDLE_RETURN_in_progress/{f}'))
    # --- superseded: used, then replaced --------------------------------------------------------------------------
    mv.append((f'{G}/finished/v1_seam_matched', f'{SUP}/walls_LIT_v1'))
    mv.append((f'{G}/finished/S1-GAL_room_light_v1.json', f'{SUP}/walls_LIT_v1/S1-GAL_room_light_v1.json'))
    mv.append((f'{G}/finished/floor_v1', f'{SUP}/floor_v1_pale_oak'))
    mv.append((f'{G}/floor/S1-GAL-FLOOR_v1_a4ea7b7a.png', f'{SUP}/floor_v1_pale_oak/S1-GAL-FLOOR_v1_a4ea7b7a.png'))
    for f in ['S1-GAL_REVIEW_walls+floor_GLOW-DARK.jpg', 'S1-GAL_REVIEW_walls+floor_SPILL.jpg']:
        mv.append((f'{G}/finished/{f}', f'{SUP}/floor_v1_pale_oak/{f}'))
    mv.append((f'{G}/finished/floor_v2/superseded/S1-GAL-FLOOR_VANISH_v1erode_1920x1080.mov',
               f'{SUP}/floor_v2_vanish_v1/S1-GAL-FLOOR_VANISH_v1erode_1920x1080.mov'))
    # --- the bin: unchosen and rejected takes ---------------------------------------------------------------------
    for f in ['room/S1-GAL-ROOM_v1_1b530434.png', 'room/S1-GAL-ROOM_v1_28fac021.png', 'room/S1-GAL-ROOM_v1_f805b472.png',
              'centre/S1-GAL-C_v1_182e5ed7.png', 'centre/S1-GAL-C_v1_1bda31c9.png', 'centre/S1-GAL-C_v1_1e2e7c0a.png',
              'centre/S1-GAL-C_v2_15b07502.png', 'centre/S1-GAL-C_v2_24eb6ba8.png', 'centre/S1-GAL-C_v2_721782b1.png',
              'centre/S1-GAL-C_v2_7ebbcde8.png',
              'left/S1-GAL-L_v1_12266b5f.png', 'left/S1-GAL-L_v1_23301870.png', 'left/S1-GAL-L_v1_91e3660d.png',
              'right/S1-GAL-R_v1_016443f1.png', 'right/S1-GAL-R_v1_20e290e5.png', 'right/S1-GAL-R_v1_c8c95ffc.png',
              'floor/S1-GAL-FLOOR_v1_73058283.png', 'floor/S1-GAL-FLOOR_v1_7e1bad6a.png', 'floor/S1-GAL-FLOOR_v1_d1923008.png',
              'floor/S1-GAL-FLOOR_v2_14d53e61.png', 'floor/S1-GAL-FLOOR_v2_73c67f9b.png', 'floor/S1-GAL-FLOOR_v2_e60dc032.png',
              'floor/S1-GAL-PUDDLE_v1_1fb5971a.png', 'floor/S1-GAL-PUDDLE_v1_9f086ce6.png', 'floor/S1-GAL-PUDDLE_v1_e3547656.png',
              'floor/S1-GAL-PUDDLE_v1_e377f119.png', 'floor/S1-GAL-PUDDLE_v2_0c86fd44.png', 'floor/S1-GAL-PUDDLE_v2_63f6b202.png',
              'floor/S1-GAL-PUDDLE_v2_d5e3e4c2.png', 'floor/S1-GAL-PUDDLE_v2_eea94f69.png', 'floor/v2_review',
              'puddle_return/S1-GAL-PUDDLE-RETURN_v1.mp4', 'puddle_return/S1-GAL-PUDDLE-RETURN_v2.mp4',
              'puddle_return/S1-GAL-PUDDLE-RETURN_v3.mp4', 'puddle_return/S1-GAL-PUDDLE-RETURN_v2cut+v3_FLOOR_1920x1080.mov']:
        mv.append((f'{G}/{f}', None))
    return mv


def size_of(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    return sum(os.path.getsize(os.path.join(d, f)) for d, _, fs in os.walk(p) for f in fs)


def main():
    if len(sys.argv) < 3 or sys.argv[2] not in ('plan', 'run'):
        sys.exit(__doc__)
    root, mode = sys.argv[1], sys.argv[2]
    media = os.path.join(root, M)
    log = os.path.join(root, 'REORG_2026-10-05_moves.tsv')
    done = skipped = 0
    touched_dirs = set()
    out = open(log, 'a') if mode == 'run' else None
    for src_r, dst_r in plan():
        src = os.path.join(media, src_r)
        dst = os.path.join(media, dst_r) if dst_r else os.path.join(root, BIN, M, src_r)
        if not os.path.exists(src):
            print('SKIP (missing)', src_r)
            skipped += 1
            continue
        if os.path.exists(dst):
            sys.exit(f'STOP: destination exists, not overwriting: {dst}')
        if mode == 'plan':
            print(f'{src_r}\n    -> {os.path.relpath(dst, root)}')
            continue
        n = size_of(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        os.rename(src, dst)
        if not os.path.exists(dst) or size_of(dst) != n:
            sys.exit(f'STOP: size check failed after moving {src_r}')
        out.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")}\t{src}\t{dst}\t{n}\n')
        out.flush()
        touched_dirs.add(os.path.dirname(src))
        done += 1
    if mode == 'run':
        # folders emptied by the moves go too (only if nothing but macOS ._ metadata is left; those go to the bin)
        for d in sorted(touched_dirs, key=len, reverse=True):
            while d.startswith(media) and d != media and os.path.isdir(d):
                left = os.listdir(d)
                if any(not f.startswith('._') and f != '.DS_Store' for f in left):
                    break
                for f in left:
                    b = os.path.join(root, BIN, M, os.path.relpath(os.path.join(d, f), media))
                    os.makedirs(os.path.dirname(b), exist_ok=True)
                    os.rename(os.path.join(d, f), b)
                os.rmdir(d)
                d = os.path.dirname(d)
        out.close()
    print(f'{mode}: {done} moved, {skipped} skipped' + (f'; log {log}' if mode == 'run' else ''))


if __name__ == '__main__':
    main()
