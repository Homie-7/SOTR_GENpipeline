# HANDOFF 2026-11-22 EXT4b (state save, star chat local_e34e5cc9, ~155k tokens)

Read first: `docs/HANDOFF-2026-11-22-EXT4.md` (Homie's words verbatim, the TO DO list), then this file.
Mode POST/script. 0 cr. Review only: no upscale, no promotion. Sound rule: Darren's sound is NOT changed (straight splices).

## DONE in this chat
- Remote Control on. Chat retitled star. Old star `local_85933f19` could NOT be archived (live work): retry. `local_c5e89e28`
  (the chat that started this one) still to archive when idle.
- `tools/s9_darren_review.py --d22` written + tested (`--test 4` OK, dry run OK): MIX22 = 221126 mix, use_mix21 placement,
  CUTS [(183,189),(248,290)] removed from every lane with `select=not(between(n,...))` after the lane concat, sound = 3 atrim
  pieces concat (no fades), captions: B5_KNOTS re-pin "Bangs the gavel" to 245-248 s uncut, then cutmap; verify() maps via uncut().
  Total 8428 f = 351.17 s. Beats: b5 183.75, b6 242.75, b7 274.92, b8 294.92, b9 310.96 s (new clock).
- Renders launched detached 17:12: `S9_gen_judge_review/_watch_ext_m10o.sh` (EXT_D22=1, affinity) -> b5 `..._EXT4_FULL.mp4` (2424 f),
  then b7 `..._EXT4.mp4` (480 f). Log `_watch_m10o.out`, `_log_m10o_b5cut.txt` / `_log_m10o_b7.txt`.
- Review chained: `_watch_review_m10o.sh` waits for "ALL DONE|GAVE UP" in `_watch_m10o.out`, then builds
  `S9_GENJUDGE_3wall_review_EXT4.mp4` (--d22, title "EXT4: Darren's 22 Nov cuts") + `--d22 --verify`. Log `_watch_review_m10o.out`.

## NEXT
1. When `_watch_review_m10o.out` says ALL DONE: check verify lag 0 everywhere; audit at 24 fps (contact sheet): strike at new
   241.0 s (4:01.0), the snip splice new 242.0 s, the b4 splice new 183.0 s, b7 snap new ~4:51.1. Open Explorer on the folder.
   Report to Homie in STE with the concerns (HANDOFF-2026-11-22-S9darren.md "Concerns").
2. S6 side task. Found so far: Darren's file `Map to ship 22112026_2_DarrinSoundSahajRen.mov` = 1920x1080 24 fps, 535.46 s,
   pcm 48k. It is Sahaj's mock-up page (3 walls in a row on top ~1536 px wide, floor trapezoid under CENTRE, cue panel right,
   strip at bottom). Picture is BLACK 0-17.96 s, hard on at 18.0 s (Sahaj's cue 0:00 = file 18.0 s: his TC 0:04:04 at file 22 s).
   Darren's sound fades in from 0 s (about -97 dB -> -50 dB by ~1 s blocks). So: our map from "Sénégal" fills 0-18 s, then
   Sahaj's scene. In `render_s6.py` the Senegal name fades in at MAP_T0+0.5..+3.0 (MAP_T0 = 147.5 s, old clock; check the
   v14 / new-clock value, T_NEW, and V7_M1 = the map's end into the water). Build 30-60 s preview in new
   `04_WORKING_FILES/S6_map_to_ship_review/`: S6 v14 map walls (show files in 01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_*_wars.mov)
   from the "Sénégal" frame, placed into Sahaj's layout (or side by side), crossfade into his picture at 18 s, his sound untouched.
3. Wrap: LOG, REGISTER, NEW-SESSION top line, CLAUDE.md stage, commit (s9_darren_review.py, court_ext.py, docs), push, T9.

## UPDATE 17:25
- S6 preview DONE + eyed: `04_WORKING_FILES/S6_map_to_ship_review/S6_map_to_ship_preview_v1.mp4` (45 s, 1080, Darren's sound
  untouched = his file's audio 0-45 s). Our three 1080 S6 walls (3_HD_1080_fallback) 147.0-165.0 s, placed in Sahaj's wall row
  (x 0-473 / 473-1064 / 1064-1536, y 24-378), alpha fade into his picture 18-19 s. Explorer opened.
  FINDING for Homie: the S6 show files are ProRes 4444 with ALPHA that ramps to 0 over ~161-163 s (luma stays). If a player
  honours alpha, the last ~2 s of S6 show black. The preview drops the alpha (format=yuv444p) so the sea shows.
  Command is in this chat's transcript; rebuild = ffmpeg trim=start=7:duration=18 after -ss 140 per wall.
- S9 b5 EXT4 render slow: 360/2424 f at 17:21 (~45 min for b5). Background waiter b3mphci08 waits for ALL DONE/GAVE UP.
