# HANDOFF 2026-11-24 FINALS4 (POST, PC) — star chat local_40f0bf85 (started ~22:50)

**TOP, for Homie in the morning: Q3 — the S9 upscale (~130 cr; 150-180 with strike backups). Ask after he watches
`S9_GENJUDGE_3wall_review_F24.mp4`.** 0 cr spent. Balance 2,443.

Read FINALS3 first (same folder). Homie's words 24 Nov ~22:40: "continue working, once all is done, shutdown the pc".

## State at ~23:30
- S6 chain (old chat local_be5931ed, task b3uja8fh7): 4K render running since 22:24 (python pid 38620, ~15 GB RAM),
  then 1080. Waiter in this chat: task bprz4qolq (ends on DONE/FAILED/GAVE UP in `_watch_s6_1080.out`, FAILED/GAVE UP in
  `_watch_s6_4k.out`, or no run_watch.sh). If it dies, relaunch with the run_watch.sh lines in FINALS3 (DONE_RE='^wrote ').
- Floor fold on D: CHECKED. 14 moves, sha256 before = after (`D:\SOTR\MOVES_2026-11-24_floor-fold.tsv`). Read-mes
  (`00_READ_ME_FIRST.txt`, `SOTR_MEDIA/README.txt`, S2 read-me) describe the new layout. The two empty old folders
  (`5_FLOOR_only_if_a_floor_projector`, S2 `3_FLOOR_only_if_a_floor_projector`) moved to `D:\SOTR\_DELETE_ME_2026-11-24\`.
  `docs/FOLDERS-2026-11-24.md` was NEVER written (the helper died).
- T9 mirror NOT done: the helper's `mv.py` died with WinError 121 (semaphore timeout) on `G:\SOTR\HF\SOTR_MEDIA\01_FINAL_FOR_SHOW`.
  G: hung for ~30 min, then came back "Healthy"; at 23:25 `G:\SOTR\HF\SOTR_MEDIA\01_FINAL_FOR_SHOW` reported NOT FOUND.
  Investigate the G: layout before any copy. Never mirror-delete.
- 25 Nov 00:21-00:24: System log shows `UASPStor 129 "Reset to device, \Device\RaidPort4"` every ~16 s and `disk 153`
  IO retries on Disk 3. `G:\SOTR\HF\SOTR_MEDIA` gives "Input/output error" / semaphore timeout; `G:\SOTR\HF` lists.
  DECISION: write NOTHING to the T9 while it resets (risk of damage). The T9 needs Homie: replug it (another port or
  cable, ideally a rear USB port), then run `chkdsk G:` (read-only first) before any copy. So the T9 copy + `git pull` on G:
  wait, and the PC does NOT shut down tonight.
- 25 Nov 00:44-00:53: robocopy of the French wav off the T9 FAILED (ERROR 1117 / 121, exit 8). The wav exists ONLY on
  the T9 (`tools/s6_fr_review.py` WAV path; no copy on C: or D:). So the S6 finals mux WAITS for the T9 fix. Target folder
  `04_WORKING_FILES/S6_FR_audio/` is made and empty.
- Shells were slow and one bash fork failed while the 4K render runs. Use long timeouts.

## Still to do
1. When S6 is done: rename `_tmp_S6_4K_final` -> `S6_4K_final`, `_tmp_S6_1080_final` -> `S6_1080_final`; mux
   `G:\SOTR\HF\Final changes\Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` (`-c:v copy -c:a pcm_s24le`); correlation check;
   fleur flag check on 4K RIGHT vs 1080. Do NOT promote.
2. Wrap: LOG, REGISTER, NEW-SESSION, CLAUDE.md stage; commit only this work's files (CLAUDE.md, court_ext.py,
   s9_darren_review.py, run_watch.sh, _launch_aff.ps1, the FINALS3/4 handoffs) + push; `git pull` on G:; T9 media copy with
   sha256 (F24 review + b5 F24 + S6 finals + the floor-fold layout).
3. Archive local_be5931ed when its jobs end. Shut down (`shutdown /s /t 60`) ONLY when all is done AND on the T9.
   If the T9 stays broken: do not shut down; report it to Homie (replug the T9).
