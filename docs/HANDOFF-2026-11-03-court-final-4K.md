# Handoff: Scene 9 court "judge behind the parchment" -> FINAL 4K show files (POST, script + ByteDance upscale)

Homie (2026-11-03): chose A2 level 2 (the gavel judge) and said "finalize this and do the whole 4K renders and everything else that needs to go in the final show." That is the explicit go-ahead for the renders, upscales and the show-folder promotion. His "in front" variant (`--front`) was rejected and reverted; `tools/court_behind_paper.py` is the committed original. Do not commit unless asked; other sessions edit render_s6.py / gallery_rehang.py, do not touch those.

## The look (approved test)
`tools/court_behind_paper.py clip OUT.mp4 --level 2 --a2` (Q2, 117 frames, one strike). Test clip: `C:\Users\Homie\Documents\SOTR_MEDIA\04_WORKING_FILES\S9_court_behind_paper\S9_court_behind_paper_Q2_strike_A2_level2.mp4`.
Judge = soft warm shadow through the paper (`compose()`: level 2 = sigma 8 px, keeps 22% light; A2 = sharper as `closeness(idx)` rises over the blow f40-96, softer after), fibre over him, burn at the paper edges (`Scene.bg(n, t0)` uses `BurnEdges`, `BEAT_T0 = {3:0, 5:960, 7:3384}`).

## What the show needs (court files today, all 4K 3600x2160 24 fps ProRes HQ + PCM audio)
In `SOTR_MEDIA\01_FINAL_FOR_SHOW\`: `1_PLAY_THESE_IN_ORDER\S9_b3_CENTRE_court.mov` (40 s, Q1), `S9_b5_CENTRE_court.mov` (101 s, Q2 then Q3 on "Three!" 45 s and "Order!" 85 s), `S9_b7_CENTRE_court.mov` (20 s, Q4 push-in strike, then the Q5 capper = gavel alone fills the wall, then black); `2_BACKUP_LOOPS_for_operator\S9_b3_CENTRE_court_strike-size1.mov`, `...b5..._strike-size2`, `...size3`, `S9_b7_..._strike-size4` (117 frames each). Plus `_CLEAN` masters in `03_CLEAN_MASTERS_no_edge\` (S9_b3/b5/b7_CENTRE_court_CLEAN.mov, 1080) and the 1080 fallbacks (check `3_HD_1080_fallback\` and `04_WORKING_FILES\4K_records\MANIFEST_4K_2026-10-01.txt` for what exists/where 1080 versions live).
Beat timings/cues: `render_court.py` `BEATS` + `timeline()`. Current builds: `render_court.py OUT.mov --beat N --scrim --burn` (b3/b5/b7) and `--strike Q1..Q4 --scrim --burn`, 1800x1080, ProRes `-qscale:v 2`; sound added by `tools/build_audio.py` (every show file carries its sound; verify by correlation with the source).

## Plan
1. Add a `--behind` option (level 2 + A2 `closeness`, same `compose()`) to the render path so beats 3/5/7 and the 4 strikes are built exactly like the current ones (same timeline, shake, burn t0 per beat, same Q sizes via `render_court_v2.SIZES`) but with the behind-paper judge. Prefer a thin wrapper script or putting it in `court_behind_paper.py` (a `beat`/`strike` command reusing `rc.timeline(beat, strike)`; note `rc.timeline(None, size)` in the existing `clip()` is the strike case). Decide the Q5 capper (gavel alone, no figure silhouette to hide): keep the current approved capper look but run it through the same paper/fibre treatment so it matches; say what you chose.
2. Render clean 1080 masters (1800x1080) with `-qscale:v 2`, new version names, NEVER overwrite: old files go to `04_WORKING_FILES\superseded\` with the version added (Folders rule in CLAUDE.md). Check frame-by-frame against the old court for timing (same length, strike frames).
3. Sound: `tools/build_audio.py` exactly as for the old court files; verify correlation.
4. 4K: the repo's route is ByteDance video upscale ("aigc" 4k) via the Higgsfield connector/CLI, then `tools/upscale_restore.py` (court size `--size 3600x2160`), checked by `tools/upscale_check.py` (all VERDICTs). ~0.08 cr/s, so about 15 credits for all 7 files; submit one job at a time; clips over ~2 min go in two overlapping halves (b5 is 101 s: single is fine). Use `tools/fetch.py` for downloads (DNS interception) and run heavy jobs with affinity FFFF3FFF (PC Core 7 crash), writing `_tmp_` names then rename. Look at `04_WORKING_FILES\4K_records\JOBS_v3.txt`, `results_v3.txt`, `overrides_v3.txt` and `promote_4k.py` for exactly how the court's 4K was done before; reuse that recipe.
5. Promote with `promote_4k.py` (gated on every upscale_check VERDICT) under the SAME show names into `01_FINAL_FOR_SHOW`; update `00_READ_ME_FIRST.txt` only if its court wording changes. Then T9 (drive G:): copy new/changed media, verify sha256 (never mirror-delete), `git pull` is not needed unless the repo is committed.
6. Record: `REGISTER.md` + `LOG.md` rows, `docs/NEW-SESSION.md`, a build recipe in `04_WORKING_FILES\build_recipes\`. Commit only if Homie asks.

## Rules that bite
Final product: files start/end at full picture, no playback fixes. Locked cameras. No negative prompts (not generating anyway). Declare mode POST at the top. Credits are a small spend here; report the total. Nothing else in the show folder changes.
First action: load only `house-rules` (finishing.md) if needed, otherwise start step 1.

## PROGRESS (session "court final 4K", 2026-11-03)
Full notes: `C:\Users\Homie\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_9962e930-f72e-4245-8c98-d7ee3c1214bb\HANDOFF-court-final-4K-progress.md`. Done: `court_behind_paper.py beat|strike` added (function `final()`); 1080 renders go to `04_WORKING_FILES/S9_court_behind_paper/final_1080/`. Sound plan: mux the OLD show file's audio onto the new picture (identical timeline). Remaining: renders, sound, 4K, promote, T9, records.

## DONE (all steps): D: + T9 (17/17 OK) promoted, WhatsApp 08_S9 swapped (old in G:/D: WHATSAPP_3_wall_previews/_DELETE_ME_2026-11-03), LOG/REGISTER/NEW-SESSION/recipe written. 144.4 cr.
