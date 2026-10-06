"""File management, 8 Oct 2026 (Homie: "do a proper file management run… things that are no longer needed can be deleted").

Claude never hard-deletes (standing rule): every listed path is MOVED (same volume, a rename) into
  /Volumes/DMD T9/SOTR/HF/_DELETE_ME_2026-10-08/<its path under SOTR_MEDIA>
for Homie to empty, and every move is written to /Volumes/DMD T9/SOTR/HF/CLEANUP_2026-10-08_moves.tsv (src, dst, bytes).
macOS '._' sidecars move with their file.

  python tools/cleanup_2026-10-08.py [--pass 2]          dry run: lists what would move and the total
  python tools/cleanup_2026-10-08.py [--pass 2] --go     moves
  ON THE PC (D: holds the same finished-scene files; the T9 sync copies anything new, so D: must be cleaned too or the
  files come back): python tools/cleanup_2026-10-08.py --pass 2 --media D:/SOTR/SOTR_MEDIA/ --bin D:/SOTR/_DELETE_ME_2026-10-08/
    --tsv D:/SOTR/CLEANUP_2026-10-08_moves.tsv --skip-missing [--go]   (pass 1 = the ship, which never existed on D:)

PASS 2 (Homie, same day: "Anything that isn't going to make it to the show and/or isn't needed to make adjustments and
changes can be binned"): the finished scenes' intermediates. VIDEO_ONLY folders lose only their .mov/.mp4 files: the
recipes (LUTs, match JSONs, masks, scripts, sound, READMEs) stay where they are. Kept untouched: 01_FINAL_FOR_SHOW,
02_APPROVED_BUILDING_BLOCKS, 03_CLEAN_MASTERS_no_edge, 05_REFERENCE_UPLOADS, 06_PRESENTATIONS, comp/ (Homie's AE area),
Final Animations/ and HF/sea/ (Homie's own material), every generated source take, edge_kits, build_recipes, 4K_records.

WHAT STAYS in S7_ship (current or needed): seamed_v2 walls + their masks (incl. _bgmask_v2), seamed_v1 (the walls Homie
approved 6 Oct, the fallback), every path a tool reads (assembled_v1, 5_layers/day, 5_layers/buildout_day, the master
ROOM_v2_f5180ed8, superseded/S7_ship_skyharmony_2026-10-07), every CHOSEN generated take (REGISTER), the buildout guides +
intermediate steps, 7_canvas21, 8_idle (raw takes + v2 idles), intro v6 and its finals, the v5 1080p flight take (240 cr of
source) and the F1 21:9 v2 opening (v6's image reference). WHAT GOES: unchosen takes, rejected intros (v1 review, FLIGHT
v1-v3, LAND, BOARD, v4), superseded state sets (assembled_* except v1, their layers), drafts whose finals exist, old review
files, the v1 idles (the bow bug) and the defective zig-zag CENTREs.
"""
import argparse
import os
import sys

HF = '/Volumes/DMD T9/SOTR/HF/'
MEDIA = HF + 'SOTR_MEDIA/'
BIN = HF + '_DELETE_ME_2026-10-08/'
TSV = HF + 'CLEANUP_2026-10-08_moves.tsv'
S7 = '04_WORKING_FILES/S7_ship/'

LIST = [S7 + p for p in [
    # 1_deck_master: unchosen room takes + unused outpaints (the master is ROOM_v2_f5180ed8)
    '1_deck_master/S7-SHIP-ROOM_v1_087f71a5.png', '1_deck_master/S7-SHIP-ROOM_v1_3c3b909e.png',
    '1_deck_master/S7-SHIP-ROOM_v1_4d719159.png', '1_deck_master/S7-SHIP-ROOM_v1_82f8306c.png',
    '1_deck_master/S7-SHIP-ROOM_v2_0aebdf8a.png', '1_deck_master/S7-SHIP-ROOM_v2_20f01ff7.png',
    '1_deck_master/S7-SHIP-ROOM_v2_33dc1d0a.png', '1_deck_master/S7-SHIP-ROOM_v2_f5180ed8_OP_L_c3bd8ce7.png',
    '1_deck_master/S7-SHIP-ROOM_v2_f5180ed8_OUTPAINT_dbd00788.png',
    # 2_intro: the rejected v1 intro's first frames + the unused 2nd astern take
    '2_intro/S7-INTRO-F1_v1_1714a32e.png', '2_intro/S7-INTRO-F1_v1_1714a32e_haze.png',
    '2_intro/S7-INTRO-F1_v1_1714a32e_haze_submask.png', '2_intro/S7-INTRO-F1_v1_30c3d773.png',
    '2_intro/S7-INTRO-F1_v1_450ae830.png', '2_intro/S7-INTRO-F1_v1_66ad98e8.png',
    '2_intro/S7-INTRO-F1-ASTERN_v1_b8b5fd73.png',
    # 3_walls: the old separately generated side walls (replaced by the build-out), superseded state sets
    '3_walls/S7-SHIP-L_v2_260b6359.png', '3_walls/S7-SHIP-L_v2_4efe4822.png', '3_walls/S7-SHIP-L_v2_b297c01e.png',
    '3_walls/S7-SHIP-L_v2_e3a2e0ee.png', '3_walls/S7-SHIP-R_v1_1652a84c.png', '3_walls/S7-SHIP-R_v1_972c8b09.png',
    '3_walls/S7-SHIP-R_v1_ab8fc4ae.png', '3_walls/S7-SHIP-R_v1_b6b0baac.png',
    '3_walls/assembled_magic_v1', '3_walls/assembled_night_v1', '3_walls/assembled_night_v2',
    '3_walls/assembled_sunset_v1', '3_walls/assembled_sunset_v2', '3_walls/assembled_wreck_v1',
    # 3_walls/states: side-wall state takes (sides now built out) + unchosen CENTRE takes (sunset's 4 kept: pick unrecorded)
    '3_walls/states/S7-SHIP-L_MAGIC_v1_45285089.png', '3_walls/states/S7-SHIP-L_MAGIC_v1_a2976650.png',
    '3_walls/states/S7-SHIP-L_NIGHT_v1_7f2bac7d.png', '3_walls/states/S7-SHIP-L_NIGHT_v1_84412bd6.png',
    '3_walls/states/S7-SHIP-L_NIGHT_v2_23d25153.png', '3_walls/states/S7-SHIP-L_NIGHT_v2_2b35f9e3.png',
    '3_walls/states/S7-SHIP-L_SUNSET_v1_17bd1936.png', '3_walls/states/S7-SHIP-L_SUNSET_v1_5294584f.png',
    '3_walls/states/S7-SHIP-R_MAGIC_v1_bd967e9d.png', '3_walls/states/S7-SHIP-R_MAGIC_v1_ee985325.png',
    '3_walls/states/S7-SHIP-R_NIGHT_v2_96478c46.png', '3_walls/states/S7-SHIP-R_NIGHT_v2_c053079c.png',
    '3_walls/states/S7-SHIP-R_SUNSET_v1_68744df0.png',
    '3_walls/states/S7-SHIP-C_MAGIC_v1_03998404.png', '3_walls/states/S7-SHIP-C_NIGHT_v1_35026a1f.png',
    '3_walls/states/S7-SHIP-C_WRECK_v1_764e5fe0.png', '3_walls/states/S7-SHIP-C_WRECK_v1_7ebcb04b.png',
    '3_walls/states/S7-SHIP-C_WRECK_v2_6af84bdc.png',
    # 3_walls/buildout_v1: the failed v1 grey canvases + their takes, unchosen takes, rejected script attempts
    '3_walls/buildout_v1/S7-SHIP-L_BUILDOUT_canvas.png', '3_walls/buildout_v1/S7-SHIP-R_BUILDOUT_canvas.png',
    '3_walls/buildout_v1/S7-SHIP-L_BUILDOUT_v1_21684352.png', '3_walls/buildout_v1/S7-SHIP-L_BUILDOUT_v1_78fc5792.png',
    '3_walls/buildout_v1/S7-SHIP-L_BUILDOUT_v2_9ae16aac.png', '3_walls/buildout_v1/S7-SHIP-R_BUILDOUT_v2_17aeab59.png',
    '3_walls/buildout_v1/_rejected_rowgain_match', '3_walls/buildout_v1/seamed/_rejected_sunset_deglare_Lonly',
    '3_walls/buildout_v1/aligned/sunset_try1', '3_walls/buildout_v1/seamed/sunset_try1',
    '3_walls/buildout_v1/states/S7-SHIP-L_MAGIC_bo_2b346d4e.png', '3_walls/buildout_v1/states/S7-SHIP-R_MAGIC_bo_08d69553.png',
    '3_walls/buildout_v1/states/S7-SHIP-L_NIGHT_bo_0a5228f3.png', '3_walls/buildout_v1/states/S7-SHIP-R_NIGHT_bo_ea8f2e3a.png',
    '3_walls/buildout_v1/states/S7-SHIP-L_SUNSET_bo2_6eeabe78.png', '3_walls/buildout_v1/states/S7-SHIP-L_SUNSET_bo_b1288006.png',
    '3_walls/buildout_v1/states/S7-SHIP-L_SUNSET_bo_c07073e5.png', '3_walls/buildout_v1/states/S7-SHIP-R_SUNSET_bo2_c4ab12c8.png',
    '3_walls/buildout_v1/states/S7-SHIP-R_SUNSET_bo_897bf6ba.png', '3_walls/buildout_v1/states/S7-SHIP-R_SUNSET_bo_b6acfbbf.png',
    # 4_intro_video: the rejected v1 intro, the 16:9 redo (FLIGHT v3, BOARD), route A drafts/builds, v6 drafts/previews
    '4_intro_video/S7-INTRO-FLIGHT_v1draft480_e358e812.mp4', '4_intro_video/S7-INTRO-FLIGHT_v2_b37921bd.mp4',
    '4_intro_video/S7-INTRO-FLIGHT_v2_b37921bd_flagwhite.mov', '4_intro_video/S7-INTRO-FLIGHT_v2_b37921bd_trim346_upload.mp4',
    '4_intro_video/S7-INTRO-FLIGHT_v2draft480_d27ab78a.mp4', '4_intro_video/S7-INTRO-LAND_v1draft480_4ff856e8.mp4',
    '4_intro_video/S7-INTRO-LAND_v2_4140a014.mp4', '4_intro_video/S7-INTRO-LAND_v2draft480_f41213bf.mp4',
    '4_intro_video/S7-INTRO_review_v1.mp4', '4_intro_video/S7-INTRO_review_v1_3walls_4680.mp4',
    '4_intro_video/endframe', '4_intro_video/redo_v2',
    '4_intro_video/routeA_21x9/S7-INTRO-FLIGHT_v4draft480_615146e9.mp4',
    '4_intro_video/routeA_21x9/S7-INTRO-FLIGHT_v5draft480_69161783.mp4',
    '4_intro_video/routeA_21x9/S7-INTRO_3walls_PREVIEW_v4draft.mp4', '4_intro_video/routeA_21x9/S7-INTRO_3walls_PREVIEW_v5draft.mp4',
    '4_intro_video/routeA_21x9/S7-INTRO_3walls_v5.mp4', '4_intro_video/routeA_21x9/S7-INTRO_3walls_v5_INTO_DAY_IDLE.mp4',
    '4_intro_video/routeA_21x9/S7-INTRO-F1-ASTERN_21x9.png',
    '4_intro_video/rev/S7-INTRO-REV_v1draft480_93befdb5.mp4', '4_intro_video/rev/S7-INTRO-REV_v1draft480_REVERSED_3wallband.mp4',
    '4_intro_video/rev/S7-INTRO-REV_v1draft480_REVERSED_full.mp4', '4_intro_video/rev/S7-INTRO-LEADIN_v1draft480_45013f4b.mp4',
    '4_intro_video/rev/S7-INTRO_v6draft_JOINED_21x9.mp4', '4_intro_video/rev/S7-INTRO_3walls_v6draft_INTO_DAY_IDLE.mp4',
    '4_intro_video/rev/_old_S7-INTRO_3walls_v6_INTO_DAY_IDLE_xfade05.mp4', '4_intro_video/rev/S7-INTRO_3walls_v6.mp4',
    # 5_layers: the layers of the superseded assembled_* state sets
    '5_layers/magic_v1', '5_layers/night_v2', '5_layers/sunset_v2', '5_layers/wreck_v1',
    # 6_review: superseded review files and temporary strips
    '6_review/S7-SHIP_all_states_contact.jpg', '6_review/S7-SHIP_all_states_contact_SEAMED_v2.jpg',
    '6_review/S7-SHIP_idle_arc_preview_v1.mp4', '6_review/S7-SHIP_light_arc_preview.mp4',
    '6_review/S7-SHIP_light_arc_preview_SEAMED_v2.mp4',
    '6_review/_seamed_day.png', '6_review/_seamed_magic.png', '6_review/_seamed_night.png', '6_review/_seamed_sunset.png',
    '6_review/_seamed_wreck.png', '6_review/_strip_magic_v1.png', '6_review/_strip_night_v2.png',
    '6_review/_strip_sunset_v2.png', '6_review/_strip_v1.png', '6_review/_strip_wreck_v1.png',
]] + [
    # replaced versions that were defective: the v1 idles (the bow bug), the zig-zag CENTREs
    '04_WORKING_FILES/superseded/S7_ship_idle_v1_2026-10-08',
    '04_WORKING_FILES/superseded/S7_ship_ropes_zigzag_2026-10-07',
]


W = '04_WORKING_FILES/'
LIST2 = [W + p for p in [
    'superseded',                                    # every replaced version: none goes to the show, none is an input
    'S6-ANIMATIC_v4_approved.mp4', 'S9-ANIMATIC_v1.mp4', 'S6_flags_v6_preview',
    'S1_gallery/3_SHOW_FILES_1080_for_review',
    'S1_gallery/2_PUDDLE_RETURN_in_progress/GLIMMER_TEST_REVIEW_lit_then_dark_fullfloor+zoom.mp4',
    'S1_gallery/2_PUDDLE_RETURN_in_progress/GLIMMER_TEST_dark_hold_1920x1080.mov',
    'S1_gallery/2_PUDDLE_RETURN_in_progress/GLIMMER_TEST_lit_on_v2_1920x1080.mov',
    'S1_gallery/2_PUDDLE_RETURN_in_progress/S1-GAL-PUDDLE-RETURN_v6flow_REVIEW_lit_then_dark_fullfloor+zoom.mp4',
    'S1_gallery/1_READY_for_show_build/floor/S1-GAL-FLOOR_VANISH_REVIEW_spill-vanish-dry_full+zoom.mp4',
    'S5_battlefield_grade/superseded', 'S5_battlefield_grade/test_front_C_10s.mov',
    'S6_v6_option/S6_CENTRE_wars.mov', 'S6_v6_option/S6_LEFT_wars.mov', 'S6_v6_option/S6_RIGHT_wars.mov',
    'S6_v6_option/4K/raw',
    'S7_ship/3_walls/seamed_v1', 'S7_ship/5_layers/seamed_v1', 'S7_ship/4_intro_video/routeA_21x9/S7-INTRO-FLIGHT_v5_6e515e2d.mp4',
]]
VIDEO_ONLY = [W + p for p in [
    'S5_battlefield_grade/C_matched', 'S5_battlefield_grade/N_matched', 'S5_battlefield_grade/N_nobirds',
    'S5_battlefield_grade/C2_graded', 'S5_battlefield_grade/C2_test', 'S5_battlefield_grade/N_v5_graded',
    'S5_battlefield_grade/S5_PRIMARY_rich_dusk', 'S5_battlefield_grade/S5_SECONDARY_cold_dusk',
    'S4_alps_grade_v2/A4_matched/review', 'S4_alps_grade_v2/A4_matched/4K/uploads',   # their sheets + PLAN jsons stay
    'S6_v6_option/uploads', 'S6_v6_option/uploads_halves',                              # their PLAN.json stays
    'S9_studio_canvas_edge',                         # its 1080 + 4K files = the show's (same bytes); uploads, raws, _regress
]]


def videos_in(rel):
    out = []
    for r, _, fs in os.walk(MEDIA + rel):
        for f in fs:
            if not f.startswith('._') and f.lower().endswith(('.mov', '.mp4')):
                out.append(os.path.relpath(os.path.join(r, f), MEDIA))
    return sorted(out)


def move(src, dst):
    """rename; if the destination folder already exists in the bin (pass 1 made it), merge into it child by child"""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src) and os.path.isdir(dst):
        for c in os.listdir(src):
            if c.startswith('._'):
                continue                      # a macOS sidecar: exFAT moves it with its file
            move(os.path.join(src, c), os.path.join(dst, c))
        for c in os.listdir(src):            # only sidecars left
            if c.startswith('._'):
                try:
                    os.remove(os.path.join(src, c))
                except FileNotFoundError:
                    pass
        os.rmdir(src)
    else:
        os.rename(src, dst)


def size(p):
    if os.path.isdir(p):
        return sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(p) for f in fs)
    return os.path.getsize(p)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--go', action='store_true')
    ap.add_argument('--pass', dest='pss', type=int, default=1)
    ap.add_argument('--media'); ap.add_argument('--bin'); ap.add_argument('--tsv')
    ap.add_argument('--skip-missing', action='store_true', help='list missing paths and carry on (D: never had some)')
    a = ap.parse_args()
    global LIST, MEDIA, BIN, TSV
    MEDIA = a.media or MEDIA; BIN = a.bin or BIN; TSV = a.tsv or TSV
    if a.pss == 2:
        LIST = LIST2 + [v for d in VIDEO_ONLY for v in videos_in(d)]
    missing = [p for p in LIST if not os.path.exists(MEDIA + p)]
    if missing:
        print('MISSING' + (' (skipped):' if a.skip_missing else ' (nothing moved):'), *missing, sep='\n  ')
        if not a.skip_missing:
            sys.exit(1)
        LIST = [p for p in LIST if p not in missing]
    tot = 0
    rows = []
    for p in LIST:
        b = size(MEDIA + p); tot += b
        rows.append((MEDIA + p, BIN + 'SOTR_MEDIA/' + p, b))
        print(f'{b / 1e6:9.1f} MB  {p}')
    print(f'{len(LIST)} items, {tot / 1e9:.2f} GB')
    if not a.go:
        print('dry run: nothing moved (--go to move)'); return
    with open(TSV, 'a') as t:
        for src, dst, b in rows:
            move(src, dst)
            side = os.path.join(os.path.dirname(src), '._' + os.path.basename(src))
            if os.path.exists(side) and os.path.exists(os.path.dirname(dst)):
                os.rename(side, os.path.join(os.path.dirname(dst), '._' + os.path.basename(dst)))
            t.write(f'{src}\t{dst}\t{b}\n')
    print(f'moved {len(rows)} items ({tot / 1e9:.2f} GB) to {BIN}; list in {TSV}')


if __name__ == '__main__':
    main()
