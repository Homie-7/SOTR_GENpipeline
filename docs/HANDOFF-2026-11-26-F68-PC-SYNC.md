# Handoff 2026-11-26 F68 — PC sync: bring the 26 Nov S5 work from the T9 to D:

Homie will open this on the PC and say "update things". Mode: POST. 0 credits. Do these steps in order.

## What changed on the T9 (Mac, 26 Nov, F66 + F67 + F68)
- F66: S5 cannon v10 promoted (4K show files + CLEAN masters).
- F67: S5 camps-with-cannon alternative built (working folder).
- F68: the alternative promoted next to the originals (Homie: "I need you to keep it as an alterntive alongside the original").
- The 01 read-me and `_SHA256.txt` were edited on the T9. The D: copies of those two files are OLD.

T9 on the PC = `G:\SOTR\HF\` (check the drive letter first). Media on the PC = `D:\SOTR\SOTR_MEDIA`
(`C:\Users\Homie\Documents\SOTR_MEDIA` is a junction to it; check it exists).

## Steps
1. Repo: `git pull` in the PC repo, then `git pull` in `G:\SOTR\HF\SOTR_GENpipeline`. Both must be at bc491e4 or later.
2. Copy these from `G:\SOTR\HF\SOTR_MEDIA\` to `D:\SOTR\SOTR_MEDIA\` (same subfolders). COPY ONLY, never mirror-delete
   (no `robocopy /MIR`, no `/PURGE`). Use `tools/archive_move.py` style copy + sha256, or robocopy without /MIR then hash.
   Run the big copies in the background (~70 GB in all).

   | T9 path (under `SOTR_MEDIA\`) | Size | sha256 (first 8) |
   |---|---|---|
   | `01_FINAL_FOR_SHOW\1_PLAY_THESE_IN_ORDER\S05_the-camps\S5_CENTRE_cannon.mov` | 0.6 GB | 71e911da |
   | `...\S05_the-camps\S5_FLOOR_cannon.mov` | 0.6 GB | 28d6baaf |
   | `...\S05_the-camps\S5_LEFT_cannon.mov` | 0.6 GB | 1083c959 |
   | `...\S05_the-camps\S5_RIGHT_cannon.mov` | 0.5 GB | e988ebc0 |
   | `...\S05_the-camps\ALTERNATIVE_camps-ending-with-cannon_one-file\S5_CENTRE_camps-with-cannon.mov` | 13.0 GB | 84162704 |
   | `...\ALTERNATIVE_camps-ending-with-cannon_one-file\S5_FLOOR_camps-with-cannon.mov` | 27.0 GB | bfc3bf62 |
   | `...\ALTERNATIVE_camps-ending-with-cannon_one-file\S5_LEFT_camps-with-cannon.mov` | 15.4 GB | 6cb121bc |
   | `...\ALTERNATIVE_camps-ending-with-cannon_one-file\S5_RIGHT_camps-with-cannon.mov` | 15.5 GB | 65586d5f |
   | `03_CLEAN_MASTERS_no_edge\S5_<W>_cannon_CLEAN.mov` (4 files) | 2.3 GB | same as the cannon show file of the same wall |
   | `01_FINAL_FOR_SHOW\00_READ_ME_FIRST.txt` | small | overwrite the D: copy (the T9 one is newer) |
   | `01_FINAL_FOR_SHOW\_SHA256.txt` | small | overwrite the D: copy (95 lines; full hashes for all show files) |

   Optional (working files, keep D: complete): `04_WORKING_FILES\S5_camps_with_cannon\` (4 x .mov + `_SHA256.txt`, ~70 GB;
   ask Homie first, D: space) and the new folders in `04_WORKING_FILES\S5_cannonball\` (`fallback_v4` .. `fallback_v10_4K`).
   Do not copy the Mac `._*` files.
3. Verify on D:: run sha256 on every copied show file and compare with the full hashes in `01_FINAL_FOR_SHOW\_SHA256.txt`
   (the paths in it are relative to `01_FINAL_FOR_SHOW\`). The 4 CLEANs must equal the 4 cannon show files.
4. Before you overwrite, look at the D: read-me and `_SHA256.txt`: if D: has lines the T9 does not have, stop and tell Homie.
5. Check the D: `S05_the-camps` folder has, after the copy: `S5_<W>_camps.mov` (4, unchanged), `S5_<W>_cannon.mov` (4),
   `S05_2022_cannonball_explosion_ALPHA_reference.mov`, and the `ALTERNATIVE_camps-ending-with-cannon_one-file\` folder (4).
6. Log: one LOG row + one REGISTER line ("26 Nov S5 files synced T9 -> D:, sha256 verified"), update
   `docs/NEW-SESSION.md` THE TASK, RIGHT NOW, commit (HEAD-EOL method if the files show CRLF-only changes), push,
   pull in the T9 clone. Short STE report to Homie.

Done = all files on D: with matching sha256, docs committed. Then nothing is open for S5.
