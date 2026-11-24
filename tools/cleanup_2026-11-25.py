"""Clean-up, 25 Nov 2026 (Homie, after the hand-over: "do a proper clean up locally and on the t9, remove anything that
isn't needed anymore and optimise everything so that we have space").

Claude never hard-deletes (standing rule). Every listed path is MOVED (same volume = a rename, so the bytes are not
touched) into <bin>/<its path under SOTR_MEDIA>, and every move is written to the TSV (src, dst, bytes). Homie empties
the bin. Run it once on D: and once on the T9 (G:); the T9 may hold extra old files inside the same folders, they go too.

KEPT UNTOUCHED: 01_FINAL_FOR_SHOW, 02_APPROVED_BUILDING_BLOCKS, 03_CLEAN_MASTERS_no_edge, 05_REFERENCE_UPLOADS,
06_PRESENTATIONS, comp/, Final Animations/, every recipe/log/plan, every generated source, S7_ship (Homie's ship, still
in progress), S2 plan A (the Topaz sources), S9_4K_final (the upscale sources), the S9 Darren-cut court file (a tool writes
there), the F25 review files and darren_final_23112026.

GOES: 04_WORKING_FILES/superseded/ (every replaced version), the gallery's RIGHT wall v4 + v5 (v6 is the source),
an old bin inside S1_gallery, the raft water motion tests + v1 (v2 is the show's), the S6 v7 4K temp renders (S6 is now
the French cut), the Darren-cut superseded renders, and the older Judge review videos (EXT..EXT5, F24, F25a, try-1 temps,
the EXT2 fallback, caption temp files).

  python tools/cleanup_2026-11-25.py --media D:/SOTR/SOTR_MEDIA --bin D:/SOTR/_DELETE_ME_2026-11-25_cleanup
      --tsv D:/SOTR/CLEANUP_2026-11-25_moves.tsv [--go]
  python tools/cleanup_2026-11-25.py --media G:/SOTR/HF/SOTR_MEDIA --bin G:/SOTR/HF/_DELETE_ME_2026-11-25_cleanup
      --tsv G:/SOTR/HF/CLEANUP_2026-11-25_moves.tsv [--go]
"""
import argparse
import os
import re
import sys

W = '04_WORKING_FILES/'
FIXED = [
    W + 'superseded',
    W + 'S1_gallery/3_RIGHT_DAVID_v4',
    W + 'S1_gallery/3_RIGHT_DAVID_v5',
    W + 'S1_gallery/_DELETE_ME_2026-11-03',
    W + 'S9_raft/water_motion_test',
    W + 'S9_raft/v1',
    W + 'S9_raft/v1_render.log',
    W + 'S9_raft/v1_render.log.err',
    W + 'S6_v7_map_option/_tmp_4K_alpha_native',
    W + 'S9_darren_cut/superseded',
    W + 'S9_gen_judge_review/_KEEP_EXT2_GOOD_fallback_2026-11-21',
    W + 'S9_gen_judge_review/_tmp_captions',
]
REVIEW = W + 'S9_gen_judge_review'
KEEP_REVIEW = re.compile(r'_F25(_FULL)?\.mp4$')


def size(p):
    if os.path.isfile(p):
        return os.path.getsize(p)
    t = 0
    for r, _, fs in os.walk(p):
        for f in fs:
            try:
                t += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--media', required=True)
    ap.add_argument('--bin', required=True)
    ap.add_argument('--tsv', required=True)
    ap.add_argument('--go', action='store_true')
    a = ap.parse_args()
    media = a.media.rstrip('/\\')
    items = list(FIXED)
    rd = os.path.join(media, REVIEW)
    if os.path.isdir(rd):
        for f in sorted(os.listdir(rd)):
            p = os.path.join(rd, f)
            if not os.path.isfile(p):
                continue
            # old review videos + their analysis files + try-1 temps; keep F25 and every log/plan/note
            if (f.endswith('.mp4') or '.mp4.' in f or f.startswith('_tmp_')) and not KEEP_REVIEW.search(f):
                items.append(REVIEW + '/' + f)
    total, rows = 0, []
    for rel in items:
        src = os.path.join(media, rel)
        if not os.path.exists(src):
            continue
        b = size(src)
        total += b
        rows.append((src, os.path.join(a.bin, rel), b))
        print(f'{b / 1e9:8.2f} GB  {rel}')
    print(f'TOTAL {total / 1e9:.2f} GB in {len(rows)} paths')
    if not a.go:
        return
    with open(a.tsv, 'a', encoding='utf-8') as t:
        for src, dst, b in rows:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            if os.path.exists(dst):
                sys.exit(f'STOP: {dst} exists')
            os.rename(src, dst)  # same volume: a rename, bytes untouched
            if os.path.exists(src) or not os.path.exists(dst) or size(dst) != b:
                sys.exit(f'STOP: move check failed for {src}')
            t.write(f'{src}\t{dst}\t{b}\n')
            t.flush()
    print('MOVED, all checked (size after = size before)')


if __name__ == '__main__':
    main()
