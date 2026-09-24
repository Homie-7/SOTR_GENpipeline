"""Reorganise SOTR_MEDIA (Homie, 2026-09-24). Moves only, never deletes; sha256 checked per file.

  python reorg.py ROOT [--dry]
Files not in the map are left exactly where they are (e.g. the T9's extra old files).
"""
import hashlib
import os
import shutil
import sys

F, B, T, R, U = ('01_FINAL_FOR_SHOW', '02_APPROVED_BUILDING_BLOCKS', '03_TESTS_IN_PROGRESS',
                 '04_REJECTED', '05_REFERENCE_UPLOADS')
MAP = {
    # finals
    'renders/clean/loc_SOTR_salon_R_b2-3_s9_v1.mov': f'{F}/RIGHT_wall_SALON/loc_SOTR_salon_R_b2-3_s9_v1.mov',
    'renders/clean/loc_SOTR_salon_R_b8_s9_v1.mov': f'{F}/RIGHT_wall_SALON/loc_SOTR_salon_R_b8_s9_v1.mov',
    'renders/clean/loc_SOTR_salon_R_IN_s9_v1.mov': f'{F}/RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_IN_s9_v1.mov',
    'renders/clean/loc_SOTR_salon_R_HOLD_s9_v1.mov': f'{F}/RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_HOLD_s9_v1.mov',
    'renders/clean/loc_SOTR_salon_R_OUT_s9_v1.mov': f'{F}/RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_OUT_s9_v1.mov',
    'renders/clean/loc_SOTR_studio_L_b4_s9_v1.mov': f'{F}/LEFT_wall_STUDIO/loc_SOTR_studio_L_b4_s9_v1.mov',
    'renders/clean/loc_SOTR_studio_L_b6_s9_v1.mov': f'{F}/LEFT_wall_STUDIO/loc_SOTR_studio_L_b6_s9_v1.mov',
    'renders/clean/loc_SOTR_studio_L_b9_s9_v1.mov': f'{F}/LEFT_wall_STUDIO/loc_SOTR_studio_L_b9_s9_v1.mov',
    'renders/clean/fig_SOTR_judge_C_b3_s9_v1.mov': f'{F}/CENTRE_wall_COURT/fig_SOTR_judge_C_b3_s9_v1.mov',
    'renders/clean/fig_SOTR_judge_C_b5_s9_v1.mov': f'{F}/CENTRE_wall_COURT/fig_SOTR_judge_C_b5_s9_v1.mov',
    'renders/clean/fig_SOTR_judge_C_b7_s9_v1.mov': f'{F}/CENTRE_wall_COURT/fig_SOTR_judge_C_b7_s9_v1.mov',
    **{f'renders/clean/fig_SOTR_judge_C_strike{q}_s9_v1.mov': f'{F}/CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strike{q}_s9_v1.mov'
       for q in ('Q1', 'Q2', 'Q3', 'Q4')},
    # approved building blocks
    'plates/court/fig_SOTR_judge_s9_v1.png': f'{B}/stills/fig_SOTR_judge_s9_v1.png',
    'plates/salon/loc_SOTR_salon_R_s9_v1.jpg': f'{B}/stills/loc_SOTR_salon_R_s9_v1.jpg',
    'plates/salon/loc_SOTR_salon_R_dark_s9_v1.jpg': f'{B}/stills/loc_SOTR_salon_R_dark_s9_v1.jpg',
    'plates/salon/loc_SOTR_salon_room_s9_v1.png': f'{B}/stills/loc_SOTR_salon_room_s9_v1.png',
    'plates/studio/loc_SOTR_studio_L_s9_v1.jpg': f'{B}/stills/loc_SOTR_studio_L_s9_v1.jpg',
    'plates/studio/loc_SOTR_studio_room_s9_v2.png': f'{B}/stills/loc_SOTR_studio_room_s9_v2.png',
    'loops/loc_SOTR_salon_R_loop_s9_v1.mp4': f'{B}/clips/loc_SOTR_salon_R_loop_s9_v1.mp4',
    'loops/loc_SOTR_salon_R_loop_s9_v1_comp.mov': f'{B}/clips/loc_SOTR_salon_R_loop_s9_v1_comp.mov',
    'loops/loc_SOTR_salon_R_reveal_s9_v1.mp4': f'{B}/clips/loc_SOTR_salon_R_reveal_s9_v1.mp4',
    'loops/loc_SOTR_salon_R_snuff_s9_v1.mp4': f'{B}/clips/loc_SOTR_salon_R_snuff_s9_v1.mp4',
    'loops/loc_SOTR_studio_L_loop_s9_v1.mp4': f'{B}/clips/loc_SOTR_studio_L_loop_s9_v1.mp4',
    'loops/loc_SOTR_studio_L_loop_s9_v1_comp.mov': f'{B}/clips/loc_SOTR_studio_L_loop_s9_v1_comp.mov',
    'loops/fig_SOTR_judge_strike_s9_v1.mp4': f'{B}/clips/fig_SOTR_judge_strike_s9_v1.mp4',
    # tests / in progress
    **{f'loops/S9-SAL-R-WITHER_v{v}_{x}.mp4': f'{T}/edge_break_tests/S9-SAL-R-WITHER_v{v}_{x}.mp4'
       for v in (1, 2, 3) for x in 'AB'},
    'loops/S9-SAL-R-SNUFF_v4_web5s.mp4': f'{T}/runner_up_takes/S9-SAL-R-SNUFF_v4_web5s.mp4',
    'loops/S9-SAL-R-SNUFF_v4_probeA.mp4': f'{T}/runner_up_takes/S9-SAL-R-SNUFF_v4_probeA.mp4',
    'loops/S9-SAL-R-LOOP_v1_parity.mp4': f'{T}/connector_test/S9-SAL-R-LOOP_v1_parity.mp4',
    'renders/clean/loc_SOTR_salon_R_seq_s9_v1_clean_HOLDS-TBD.mov': f'{T}/superseded/loc_SOTR_salon_R_seq_s9_v1_clean_HOLDS-TBD.mov',
    # reference uploads
    **{f'refs/{n}': f'{U}/{n}' for n in ('SAL-R-LOOP_comp_f0.png', 'SAL-R-LOOP_comp_upload.mp4',
                                        'SAL-R-clean-gerard-f300.png', 'STU-L-LOOP_comp_f0.png')},
}
REJ = ['S9-SAL-R-REVEAL_v1_A.mp4', 'S9-SAL-R-SNUFF_v1.mp4', 'S9-SAL-R-SNUFF_v2.mp4', 'S9-SAL-R-SNUFF_v3.mp4',
       'S9-SAL-R-SNUFF_v4_probeB.mp4', 'S9-SAL-R-SNUFF_v5_probeA.mp4', 'S9-SAL-R-SNUFF_v5_probeB.mp4',
       'S9-SAL-R-SNUFF_v7_A.mp4', 'S9-SAL-R-SNUFF_v8_A.mp4', 'S9-SAL-R-SNUFF_v8_B.mp4', 'S9-STU-L-LOOP_v1.mp4',
       'loc_SOTR_studio_L_s9_v1_uncropped.jpeg']
MAP.update({f'rejected/{n}': f'{R}/{n}' for n in REJ})


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()


if __name__ == '__main__':
    root, dry = sys.argv[1], '--dry' in sys.argv
    moved = skipped = 0
    for src, dst in MAP.items():
        s, d = os.path.join(root, src), os.path.join(root, dst)
        if not os.path.exists(s):
            if os.path.exists(d):
                skipped += 1
                continue
            print('MISSING', src)
            continue
        if os.path.exists(d):
            print('TARGET EXISTS, left alone:', dst)
            continue
        if dry:
            print('would move', src, '->', dst)
            continue
        before = sha(s)
        os.makedirs(os.path.dirname(d), exist_ok=True)
        shutil.move(s, d)
        if sha(d) != before:
            raise SystemExit(f'CHECKSUM CHANGED on {dst}, stopping')
        moved += 1
    # remove directories only if now EMPTY (never files)
    for sub in ('renders/clean', 'renders/fx', 'renders', 'loops', 'plates/court', 'plates/salon', 'plates/studio',
                'plates', 'refs', 'rejected'):
        p = os.path.join(root, sub)
        if not dry and os.path.isdir(p) and not os.listdir(p):
            os.rmdir(p)
    print(f'{root}: moved {moved}, already moved {skipped}')
