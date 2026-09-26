"""Reorganise 01_FINAL_FOR_SHOW around the script (Homie 2026-09-26: "we have so many files, I am getting
confused"). The show folder becomes: the 8 files that play, in beat order; the 10 operator backups; and
the same 18 pictures without the edge. Version numbers leave the file names (they live in REGISTER.md
and the read-me); names say beat, wall and world. Moves only (same drive), sha256 checked before and
after every move. Nothing is deleted.

  python tools/reorg_media_2026-09-26.py ROOT [--go]      (dry run without --go)
  ROOT = C:/Users/Homie/Documents/SOTR_MEDIA  (or the T9 copy, G:/SOTR/HF/SOTR_MEDIA)
"""
import hashlib
import os
import sys

F = '01_FINAL_FOR_SHOW'
PLAY, BACK, CLEAN = f'{F}/1_PLAY_THESE_IN_ORDER', f'{F}/2_BACKUP_LOOPS_for_operator', f'{F}/3_CLEAN_no_edge'
S, R, C, L = f'{F}/RIGHT_wall_SALON', None, f'{F}/CENTRE_wall_COURT', f'{F}/LEFT_wall_STUDIO'

# (old path, new path, what it was: kept in the read-me and REGISTER)
MAP = [
    # the files that play, in beat order
    (f'{S}/with_edge_effect/loc_SOTR_salon_R_b2-3_s9_v3_edge2b.mov', f'{PLAY}/S9_b2-3_RIGHT_salon.mov', 'salon v3, edge2b'),
    (f'{C}/with_edge_effect/fig_SOTR_judge_C_b3_s9_v2_edge3b.mov', f'{PLAY}/S9_b3_CENTRE_court.mov', 'court v2, edge3b'),
    (f'{L}/with_edge_effect/loc_SOTR_studio_L_b4_s9_v3_edge2.mov', f'{PLAY}/S9_b4_LEFT_studio.mov', 'studio v3, edge2'),
    (f'{C}/with_edge_effect/fig_SOTR_judge_C_b5_s9_v2_edge3b.mov', f'{PLAY}/S9_b5_CENTRE_court.mov', 'court v2, edge3b'),
    (f'{L}/with_edge_effect/loc_SOTR_studio_L_b6_s9_v3_edge2.mov', f'{PLAY}/S9_b6_LEFT_studio.mov', 'studio v3, edge2'),
    (f'{C}/with_edge_effect/fig_SOTR_judge_C_b7_s9_v2_edge3b.mov', f'{PLAY}/S9_b7_CENTRE_court.mov', 'court v2, edge3b'),
    (f'{S}/with_edge_effect/loc_SOTR_salon_R_b8_s9_v3_edge2b.mov', f'{PLAY}/S9_b8_RIGHT_salon.mov', 'salon v3, edge2b'),
    (f'{L}/with_edge_effect/loc_SOTR_studio_L_b9_s9_v3_edge2.mov', f'{PLAY}/S9_b9_LEFT_studio.mov', 'studio v3, edge2'),
    # operator backups, with the edge
    (f'{S}/with_edge_effect/backup_pieces/loc_SOTR_salon_R_IN_s9_v2_edge2.mov', f'{BACK}/S9_b2_RIGHT_salon_IN_candles-light.mov', 'salon IN v2, edge2'),
    (f'{S}/with_edge_effect/backup_pieces/loc_SOTR_salon_R_HOLD_s9_v2_edge2.mov', f'{BACK}/S9_b2_RIGHT_salon_HOLD_loop.mov', 'salon HOLD v2, edge2'),
    (f'{S}/with_edge_effect/backup_pieces/loc_SOTR_salon_R_OUT_s9_v2_edge2b.mov', f'{BACK}/S9_b3-and-b8_RIGHT_salon_OUT_snuff.mov', 'salon OUT v2, edge2b'),
    (f'{C}/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ1_s9_v2_edge3b.mov', f'{BACK}/S9_b3_CENTRE_court_strike-size1.mov', 'court Q1 v2, edge3b'),
    (f'{L}/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b4_s9_v3_edge2.mov', f'{BACK}/S9_b4_LEFT_studio_HOLD_loop.mov', 'studio HOLD-b4 v3, edge2'),
    (f'{C}/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ2_s9_v2_edge3b.mov', f'{BACK}/S9_b5_CENTRE_court_strike-size2.mov', 'court Q2 v2, edge3b'),
    (f'{C}/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ3_s9_v2_edge3b.mov', f'{BACK}/S9_b5_CENTRE_court_strike-size3.mov', 'court Q3 v2, edge3b'),
    (f'{L}/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b6_s9_v3_edge2.mov', f'{BACK}/S9_b6_LEFT_studio_HOLD_loop.mov', 'studio HOLD-b6 v3, edge2'),
    (f'{C}/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ4_s9_v2_edge3b.mov', f'{BACK}/S9_b7_CENTRE_court_strike-size4.mov', 'court Q4 v2, edge3b'),
    (f'{L}/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b9_s9_v3_edge2.mov', f'{BACK}/S9_b9_LEFT_studio_HOLD_loop.mov', 'studio HOLD-b9 v3, edge2'),
    # the same pictures without the edge
    (f'{S}/loc_SOTR_salon_R_b2-3_s9_v3.mov', f'{CLEAN}/S9_b2-3_RIGHT_salon_CLEAN.mov', 'salon v3'),
    (f'{C}/fig_SOTR_judge_C_b3_s9_v2.mov', f'{CLEAN}/S9_b3_CENTRE_court_CLEAN.mov', 'court v2'),
    (f'{L}/loc_SOTR_studio_L_b4_s9_v3.mov', f'{CLEAN}/S9_b4_LEFT_studio_CLEAN.mov', 'studio v3'),
    (f'{C}/fig_SOTR_judge_C_b5_s9_v2.mov', f'{CLEAN}/S9_b5_CENTRE_court_CLEAN.mov', 'court v2'),
    (f'{L}/loc_SOTR_studio_L_b6_s9_v3.mov', f'{CLEAN}/S9_b6_LEFT_studio_CLEAN.mov', 'studio v3'),
    (f'{C}/fig_SOTR_judge_C_b7_s9_v2.mov', f'{CLEAN}/S9_b7_CENTRE_court_CLEAN.mov', 'court v2'),
    (f'{S}/loc_SOTR_salon_R_b8_s9_v3.mov', f'{CLEAN}/S9_b8_RIGHT_salon_CLEAN.mov', 'salon v3'),
    (f'{L}/loc_SOTR_studio_L_b9_s9_v3.mov', f'{CLEAN}/S9_b9_LEFT_studio_CLEAN.mov', 'studio v3'),
    (f'{S}/backup_pieces/loc_SOTR_salon_R_IN_s9_v2.mov', f'{CLEAN}/backups/S9_b2_RIGHT_salon_IN_candles-light_CLEAN.mov', 'salon IN v2'),
    (f'{S}/backup_pieces/loc_SOTR_salon_R_HOLD_s9_v2.mov', f'{CLEAN}/backups/S9_b2_RIGHT_salon_HOLD_loop_CLEAN.mov', 'salon HOLD v2'),
    (f'{S}/backup_pieces/loc_SOTR_salon_R_OUT_s9_v2.mov', f'{CLEAN}/backups/S9_b3-and-b8_RIGHT_salon_OUT_snuff_CLEAN.mov', 'salon OUT v2'),
    (f'{C}/backup_pieces/fig_SOTR_judge_C_strikeQ1_s9_v2.mov', f'{CLEAN}/backups/S9_b3_CENTRE_court_strike-size1_CLEAN.mov', 'court Q1 v2'),
    (f'{L}/backup_pieces/loc_SOTR_studio_L_HOLD-b4_s9_v3.mov', f'{CLEAN}/backups/S9_b4_LEFT_studio_HOLD_loop_CLEAN.mov', 'studio HOLD-b4 v3'),
    (f'{C}/backup_pieces/fig_SOTR_judge_C_strikeQ2_s9_v2.mov', f'{CLEAN}/backups/S9_b5_CENTRE_court_strike-size2_CLEAN.mov', 'court Q2 v2'),
    (f'{C}/backup_pieces/fig_SOTR_judge_C_strikeQ3_s9_v2.mov', f'{CLEAN}/backups/S9_b5_CENTRE_court_strike-size3_CLEAN.mov', 'court Q3 v2'),
    (f'{L}/backup_pieces/loc_SOTR_studio_L_HOLD-b6_s9_v3.mov', f'{CLEAN}/backups/S9_b6_LEFT_studio_HOLD_loop_CLEAN.mov', 'studio HOLD-b6 v3'),
    (f'{C}/backup_pieces/fig_SOTR_judge_C_strikeQ4_s9_v2.mov', f'{CLEAN}/backups/S9_b7_CENTRE_court_strike-size4_CLEAN.mov', 'court Q4 v2'),
    (f'{L}/backup_pieces/loc_SOTR_studio_L_HOLD-b9_s9_v3.mov', f'{CLEAN}/backups/S9_b9_LEFT_studio_HOLD_loop_CLEAN.mov', 'studio HOLD-b9 v3'),
    # the meeting one-pager, out of the media root
    ('Scene9_One-Pager_dark.pdf', '06_PRESENTATIONS/Scene9_One-Pager_dark.pdf', 'meeting one-pager 2026-09-26'),
]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''):
            h.update(b)
    return h.hexdigest()


def main():
    root, go = sys.argv[1], '--go' in sys.argv
    missing = [o for o, _, _ in MAP if not os.path.exists(os.path.join(root, o))]
    clash = [n for _, n, _ in MAP if os.path.exists(os.path.join(root, n))]
    if missing or clash:
        raise SystemExit(f'stop: missing {missing} / already there {clash}')
    for old, new, what in MAP:
        print(f'{old}\n    -> {new}   ({what})')
        if go:
            src, dst = os.path.join(root, old), os.path.join(root, new)
            before = sha(src)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.rename(src, dst)
            assert sha(dst) == before, f'checksum changed: {new}'
            print(f'    OK {before[:12]}')
    if go:  # the old wall folders should now be empty: remove only EMPTY folders
        for w in ('RIGHT_wall_SALON', 'LEFT_wall_STUDIO', 'CENTRE_wall_COURT'):
            for d, _, _ in sorted(os.walk(os.path.join(root, F, w)), key=lambda t: -len(t[0])):
                if not os.listdir(d):
                    os.rmdir(d)
                else:
                    print('NOT EMPTY, kept:', d, os.listdir(d))
    print(f'{len(MAP)} files', 'moved' if go else '(dry run)')


if __name__ == '__main__':
    main()
