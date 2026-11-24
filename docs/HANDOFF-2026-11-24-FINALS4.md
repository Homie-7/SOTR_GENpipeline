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

## Update 25 Nov (morning)
- S6 chain DONE (try 1 each, 04:04). Renamed to `04_WORKING_FILES/S6_4K_final/` + `S6_1080_final/` (S6_LEFT/CENTRE/RIGHT.mov,
  ProRes 4444 alpha, 24 fps, 2910 f each, NO sound). Fleur flag (RIGHT, 80-86 s): 4K = 1080 in cloth, fleurs, timing; small
  burn holes differ in shape (noise per pixel grid). Reported to Homie, not fixed.
- Docs (LOG, REGISTER, NEW-SESSION, CLAUDE.md stage) committed + pushed: 5c35c4c. Old chat local_0e75b379 archived;
  local_be5931ed + local_9bef2981 refused archive (Remote Control on).
- HOMIE (25 Nov, verbatim): "T9 is replugged". chkdsk NOT confirmed. FIRST: check the System log for new UASPStor 129
  resets and test a read of `G:\SOTR\HF\SOTR_MEDIA` (timeout). Ask whether he ran `chkdsk G:` if unclear; if the resets
  are gone, proceed.
- NEXT, in order: (a) copy the FR wav to `04_WORKING_FILES/S6_FR_audio/`; (b) mux into S6_4K_final + S6_1080_final
  (new files beside, `-c:v copy -c:a pcm_s24le`; clean renders never overwritten); (c) correlation check vs the wav;
  (d) `git pull` in `G:\SOTR\HF\SOTR_GENpipeline`; (e) T9 media copy with sha256 (F24 review + b5 F24 + S6 finals +
  01_FINAL_FOR_SHOW floor-fold layout: apply `D:\SOTR\MOVES_2026-11-24_floor-fold.tsv` moves on G:, copy, never
  mirror-delete); (f) shutdown /s /t 60 only if Homie still wants it (his night order was "once all is done, shutdown").
  Q3 (S9 upscale ~130 cr) still open.

## Still to do (original list)
1. When S6 is done: rename `_tmp_S6_4K_final` -> `S6_4K_final`, `_tmp_S6_1080_final` -> `S6_1080_final`; mux
   `G:\SOTR\HF\Final changes\Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` (`-c:v copy -c:a pcm_s24le`); correlation check;
   fleur flag check on 4K RIGHT vs 1080. Do NOT promote.
2. Wrap: LOG, REGISTER, NEW-SESSION, CLAUDE.md stage; commit only this work's files (CLAUDE.md, court_ext.py,
   s9_darren_review.py, run_watch.sh, _launch_aff.ps1, the FINALS3/4 handoffs) + push; `git pull` on G:; T9 media copy with
   sha256 (F24 review + b5 F24 + S6 finals + the floor-fold layout).
3. Archive local_be5931ed when its jobs end. Shut down (`shutdown /s /t 60`) ONLY when all is done AND on the T9.
   If the T9 stays broken: do not shut down; report it to Homie (replug the T9).

## Update 25 Nov (later): Homie's F24 notes + F25 fix (chat local_f32d8ea7)
- HOMIE (25 Nov, verbatim, on `S9_GENJUDGE_3wall_review_F24.mp4`): "At about 3:49, there is a a slight snap to position
  on the judge. At about 4:01. the background paper also snaps to a different state. Fix those two and we are good to go.
  Not sure what happened to T9 but it should be fine now". "Good to go" = approval after the fix; Q3 (S9 upscale ~130 cr)
  still needs his explicit yes + number.
- Causes (b5 F24 plan): 3:49 = b5 out 1092-1094, the look-up exit U185 -> R149 leaves 3 R frames before lead C, so R's
  framing (~3 %) eased onto C's over 3 f. 4:01 = the review splice (b5 out 1398 -> 2406): the paper burn + lamp clock ran
  on through the 1008 f cut, so the paper jumped 42 s.
- Fix: `tools/court_ext.py` env `EXT_F25=1` (needs EXT_F24=1): reframe over the last REFRAME (96) f before the lead, back
  through U (out 999-1094); U -> R snap ease 16 f (`EXT_F25_EASE`); background clock skips SNIP for b5 out >= 2406.
  Render -> `S9_b5_CENTRE_court_GENJUDGE_F25_FULL.mp4` (run_watch.sh, log `_render_b5_F25.log`), then the review
  `S9_GENJUDGE_3wall_review_F25.mp4` (same `--f24` command, `--b5` the F25 file), `--verify`, steps at the two joins.
- T9: silent at-rest corruption found (same size, wrong bytes, mostly 22 Nov files). The repo clone was re-cloned fresh
  (old one in `G:\SOTR\HF\_DELETE_ME_2026-11-25\`). A read-only media audit runs: `D:\SOTR\T9_AUDIT_2026-11-25\audit.tsv`.
- First pass renamed `*_F25a_*` (paper fix + reframe fix; the judge still rose ~8 px in 2 f at the R151 -> C0 join,
  out 1095-1096, found with a dark-pixel centroid probe). Second pass adds the R -> lead ease: the lead's first 16 f
  flow-snap back from R's last frame (`snap=('R', rf, 1-smooth)`), so out 1076-1110 move smoothly. That render is
  the `*_F25_*` file.
- T9 audit result: 1,208 OK, 13 BAD + 9 SIZE_DIFF (all re-copied from D:), 315 ONLY_ON_T9 (kept). Sync script
  `D:\SOTR\T9_SYNC_2026-11-25\t9_sync.py` (floor-fold moves on G with sha, then copy-new with sha; old T9 versions go to
  `G:\SOTR\HF\_DELETE_ME_2026-11-25\SOTR_MEDIA\`). Log `sync.tsv`. It skips the F25 files: copy them after the render.
