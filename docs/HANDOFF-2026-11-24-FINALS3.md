# HANDOFF 2026-11-24 FINALS3 (POST, PC) — star chat local_be5931ed (started 21:20)

Read `docs/HANDOFF-2026-11-24-FINALS2.md` (the five steps, Homie's words) and `docs/PLAN-4K-FINALS-2026-11-24.md` first.
0 cr spent. Balance 2,443. Remote Control is ON for local_be5931ed.

## Done in this chat (uncommitted at writing)
- `tools/court_ext.py`: env `EXT_F24=1` (needs `EXT_E5=1`): `LOOK_OUT` +48 (858 -> 906, override `EXT_F24_LOOK`), b5 knocks[2]
  +5 (1279 -> 1284). `plan` OK: U at out 907-1091, exit R149 IoU 0.9745, lead C, impacts [25, 546, 1284].
- `tools/s9_darren_review.py --f24 WORDS_JSON`: `use_f24` = use_e5 + MIX = local final copy (`MIXF`), FADES none,
  SOUND_UNCUT (straight atrim; verify src = t), b5 strike caption knot 243.21.
- `tools/run_watch.sh LOG python-args` (affinity via `tools/_launch_aff.ps1`, 3 tries, `DONE_RE` env for the end word;
  render_s6 prints `wrote`, so use `DONE_RE='^wrote '`).
- b5 F24 render STARTED 21:24 (watch out `04_WORKING_FILES/S9_gen_judge_review/_watch_f24_b5.out`, log `_log_f24_b5cut.txt`)
  -> `S9_b5_CENTRE_court_GENJUDGE_F24_FULL.mp4`.
- S6 test stills (old chat's run, scale 1 + 2 at t 30/60/100) were running at 21:21 into
  `C:/Users/Homie/AppData/Local/Temp/claude/1a87b61f2be73074/80d44191-1020-4f86-b765-56eadbb138cf/scratchpad/s6still/s1|s2`.

## Next
1. Look at the S6 stills (fleurs on RIGHT same size/place at 4K as 1080). Then start S6 4K + 1080 with run_watch.sh
   (OUT dirs in `04_WORKING_FILES/S6_4K_final/` and `S6_1080_final/`), then mux Homie's FR wav, correlation check.
2. When b5 is DONE: build review
   `python tools/s9_darren_review.py <D>/S9_GENJUDGE_3wall_review_F24.mp4 --f24 <D>/darren_final_23112026/_FINAL_whisper_words.json
   --b3 <D>/S9_b3_CENTRE_court_GENJUDGE_EXT2.mp4 --b5 <D>/S9_b5_CENTRE_court_GENJUDGE_F24_FULL.mp4 --b7 <D>/S9_b7_CENTRE_court_GENJUDGE_EXT5.mp4`
   (b3 = EXT2 file, as EXT4/EXT5 used), then `--verify` (lag 0), frame check at 222.6 s and 237.25 s; open folder in Explorer.
3. Folder clean-up: delegated to a helper (see `docs/FOLDERS-2026-11-24.md` when it lands).
4. Wrap.

## Update 22:10
- b5 F24 DONE (2,424 f, try 1). Review `S9_GENJUDGE_3wall_review_F24.mp4` BUILT (8,428 f, 351.17 s, Darren's final uncut).
  `--verify` lag 0 at every point (corr >= 0.996). Sheets: look-up turns with "Order! ORDER!" caption ~222.6 s;
  gavel impact ~237.2 s (sound 237.25 s, within 1 f). Folder opened in Explorer. WAITING for Homie's notes + Q3 (upscale cr).
- Still open: S6 stills (old chat processes) -> S6 4K/1080 renders; floor-fold helper; wrap.
- 22:20 S6 stills checked (scale 1 vs 2 at 30/60/100 s match; the RIGHT fleur flag is not in those frames: check it on the 4K output).
  S6 renders STARTED (task b3uja8fh7, one chain: 4K then 1080) into `04_WORKING_FILES/_tmp_S6_4K_final/` and `_tmp_S6_1080_final/`
  (S6_LEFT/CENTRE/RIGHT.mov); watch outs `_watch_s6_4k.out` / `_watch_s6_1080.out`, logs `_log_s6_*.txt`. 4K may take ~4 h+.
  After: rename folders without `_tmp_`, mux FR wav (`-c:v copy -c:a pcm_s24le`), correlation check, check fleurs. Do not promote.

## Homie, 24 Nov ~22:40 (verbatim): "continue working, once all is done, shutdown the pc"
Successor star chat takes over here. The old chat (local_be5931ed) is NOT archived until its background jobs end:
- S6 render chain (4K then 1080): watch `04_WORKING_FILES/_watch_s6_4k.out` / `_watch_s6_1080.out` for DONE / FAILED / GAVE UP
  (`ps -ef | grep render_s6` shows it live). If the chain dies, relaunch with the same run_watch.sh lines (see above; DONE_RE='^wrote ').
- Floor-fold helper (subagent in the old chat): D: moves DONE, checksums match; T9 moves were still running. Its report:
  `docs/FOLDERS-2026-11-24.md`, move list `D:\SOTR\MOVES_2026-11-24_floor-fold.tsv`. Check the read-mes + CLAUDE.md Folders rule + G: layout.
Then: S6 rename `_tmp_` folders, mux FR wav, correlation, fleur check on 4K RIGHT (flag frames), NO promotion.
Then wrap (LOG, REGISTER, NEW-SESSION, CLAUDE.md stage, commit + push, git pull on G:, T9 media copy with sha256 incl. the F24 review + S6 finals).
Then shut down the PC (`shutdown /s /t 60`) only when everything is finished AND on the T9 (memory: overnight autonomy).
Open for Homie in the morning: Q3 (S9 upscale ~130 cr / 150-180 cr) after he watches the F24 review.
