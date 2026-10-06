# PC handover, 8 Oct 2026: bring the Windows PC in line with the T9

**For:** the Claude Code session on the Windows PC (Homie pastes the block below). **Mode: POST.** No generation, 0 credits.

Since 5 Oct every session ran on the MacBook, straight on the T9. The T9 is now the newer copy of everything: the gallery
(Scenes 1 + 10, approved and in the show folder), the ship (Scenes 7-8, work in progress), the 8 Oct clean-up and the
rewritten READMEs. D: is behind. This file is the whole job, in order.

## Paste this into a fresh chat on the PC

```
Load house-rules. MODE = POST. Read CLAUDE.md, then docs/PC-HANDOVER-2026-10-08.md, and do it exactly, step by step,
stopping after each dry run to show me the summary before running it for real. Keep answers short and plain.
```

## Why the order matters

`tools/backup_t9.py` (D: -> T9) must **not** run until step 6. It replaces any T9 file whose size differs from D:'s, so
run first it would put D:'s OLD `00_READ_ME_FIRST.txt` and `README.txt` over the T9's new ones, and copy back to the T9
everything the 8 Oct clean-up binned (412 GB). D: is brought up to date from the T9 first, then checked.

## The steps

**0. Preflight.**
- `git pull` in `C:\Users\Homie\Documents\SOTR_GENpipeline`.
- The T9 is `G:` (`G:\SOTR\HF\SOTR_MEDIA` exists); D: has `D:\SOTR\SOTR_MEDIA`; the junction
  `C:\Users\Homie\Documents\SOTR_MEDIA` points to it (`D:\SOTR\_migration.log`).
- Note D:'s free space.

**1. The 5 Oct reorganisation, on D: (if not already done).** Done already if `D:\SOTR\REORG_2026-10-05_moves.tsv` exists:
skip to step 2. Otherwise:
`python tools/reorg_2026-10-05.py D:/SOTR plan`, show Homie, then `... run`. It moves Scenes 4 and 5 into
`01_FINAL_FOR_SHOW` (renames on D:, nothing copied). Its gallery lines report "missing" on D: and are skipped: the
gallery arrives in its final layout in step 3. Then `python tools/promote_gallery_2026-10-05.py D:/SOTR plan`: if every
line is "missing" (expected: D: never had the gallery), skip it; otherwise `run`.

**2. The 8 Oct clean-up, on D:.** Homie's rule: *"Anything that isn't going to make it to the show and/or isn't needed
to make adjustments and changes can be binned."* Same list as the T9; nothing is deleted, it all goes to a bin on D:.
```
python tools/cleanup_2026-10-08.py --pass 2 --media D:/SOTR/SOTR_MEDIA/ --bin D:/SOTR/_DELETE_ME_2026-10-08/ --tsv D:/SOTR/CLEANUP_2026-10-08_moves.tsv --skip-missing
```
Dry run first (it lists every item and the GB), show Homie, then add `--go`. Pass 1 (the ship) is not needed: the ship
was never on D:. Video files go; the recipes beside them (LUTs, match JSONs, masks, scripts, PLAN jsons) stay.

**3. Copy the T9's newer work to D:.**
```
python tools/sync_from_t9.py
```
Dry run: it lists what it would COPY (on the T9, missing on D:), what it would REPLACE (D:'s copy differs; D:'s old copy
goes to `D:\SOTR\_DELETE_ME_2026-10-08\replaced_by_t9\`), the GB, D:'s free space, and the files only on D:. Expect,
roughly 80 GB: the gallery show files in `01_FINAL_FOR_SHOW` (folders 1, 2, 5), `02_APPROVED_BUILDING_BLOCKS\S1_gallery`,
`04_WORKING_FILES\S1_gallery`, `04_WORKING_FILES\S7_ship` (**the ship's only copy is on the T9 today**),
`05_REFERENCE_UPLOADS` additions, `Final Animations`, and the two READMEs as replacements.
Show Homie, then `python tools/sync_from_t9.py --go`. It is disk-bound, not CPU-heavy, but long: run it detached
with output to a log (a background shell with a timeout can kill it). Every copy is sha256-checked; it exits 1 on any
mismatch (the bad copy is left as a `_tmp_` name).

**4. The files only on D:.** The dry run in step 3 lists them (also in `D:\SOTR\SYNC_FROM_T9_2026-10-08.tsv` as
`D-ONLY`). After steps 1-2 the list should be empty or short. Show it to Homie; move nothing on your own.

**5. Prove they match.** `python tools/sync_from_t9.py --hash`: must say 0 to copy, 0 to replace (every file compared
byte for byte; slow, about 300 GB read twice: run it detached).

**6. Only now, the usual backup check.** `python tools/backup_t9.py --dry`: should find nothing new to copy to the T9,
apart from step 4's D:-only files (if Homie kept any). If it lists anything else, stop and report.

**7. The source renders on F:.** Scenes 4 and 5 can only be regraded from the original Unreal renders now (their grade
intermediates were binned). Confirm these exist and report their file counts:
`F:\OrCha Drive\SOR Show Final\Renders (050422)\Alps\` (Scene 4) and the camps renders under
`F:\OrCha Drive\SOR Show Final\New Renders\` (Scene 5). If either is missing, tell Homie before he empties any bin.

**8. Wrap.** One LOG row (what moved, GB, checks passed), refresh `docs/NEW-SESSION.md` "THE TASK, RIGHT NOW" (mark the
PC housekeeping done), commit, push, then `git pull` in the T9's copy `G:\SOTR\HF\SOTR_GENpipeline`.

**9. Tell Homie (his job, not yours):** empty `D:\SOTR\_DELETE_ME_2026-10-08\` and the T9's
`G:\SOTR\HF\_DELETE_ME_2026-10-08\` once step 7 is confirmed.

## Standing rules that apply here

- **Never hard-delete.** Everything goes to a dated `_DELETE_ME_` bin; Homie empties it.
- **Copy, never mirror-delete** between drives.
- **The PC crashes under all-core load** (Core 7): anything CPU-heavy runs with affinity `FFFF3FFF` and writes to
  `_tmp_` names. Long jobs run detached.
- **Never touch:** `comp\` (Homie's After Effects area), `Final Animations\`, and Homie's own folders outside
  `SOTR_MEDIA` (`G:\SOTR\HF\sea\`, `G:\SOTR\HF\SOTR\`).
- The T9's clean-up record: `G:\SOTR\HF\CLEANUP_2026-10-08_moves.tsv`; what was binned and why: `REGISTER.md`,
  section "2026-10-08 · FILE MANAGEMENT".

## Not for the PC

The ship review (intro v6, the idles), the 4K upscales and the destruction are MacBook/VID work for after Homie's
verdict: `docs/NEW-SESSION.md`.
