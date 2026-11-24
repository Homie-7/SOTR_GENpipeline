# HANDOFF 2026-11-24 FINALS2 (POST, PC) — S9 judge re-time + S6 4K render + show-folder clean-up

Previous star chat: local_80d44191 (this one, retitled "(old)"). Read `docs/PLAN-4K-FINALS-2026-11-24.md` first (commit edd0b47).
Credit balance 2,443 (floor 1,500). 0 cr spent this meeting.

## Homie's words (24 Nov, verbatim)
1. On the plan: "Fix the look-up and the strike, then show me the review."
2. "Run side tasks of rendering the S6 and anything else as that is a green light and has no conflicts."
3. "Continue working, I will come back and check in after a while. Make sure you rearrange files and keep things
   clean and clear for the show in T9. No need to have separate folders for the floor projection, keep them with the
   final for show files where they apply."

Not yet a yes: Q3, the S9 upscale (~130 cr, 150-180 with strike backups). Ask after he sees the re-timed review.
The b7 hit (sound 3 frames early) stays AS IS (my recommendation, he picked "look-up and strike" only).

## State
- Darren's final: `SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review/darren_final_23112026/the judge CUT DOWN 23112026.mov`
  (sha256 0dc9ae27…e4cd423). It is ALREADY CUT (351.17 s = the review clock). Its whisper words (review clock):
  `darren_final_23112026/_FINAL_whisper_words.json`.
- Measured: "Order! Order!" 222.58 s (EXT5 220.60, +1.98 s = +48 f). b5 gavel sound 237.25 s vs picture impact
  237.04 s (+5 f; template match +0.217 s). b7 sound 3 f before contact (leave).
- A background run (task b8dmkcj1e in the old chat) renders S6 test stills at scale 1 and 2, t = 30, 60, 100 s, to
  `C:/Users/Homie/AppData/Local/Temp/claude/1a87b61f2be73074/80d44191-1020-4f86-b765-56eadbb138cf/scratchpad/s6still/s1|s2`
  (logs log1.txt / log2.txt). If missing, re-run them. Compare the fleurs-de-lis on RIGHT: same size and place at 4K as
  at 1080 (the 3 Nov v14 4K used the DEFAULT 1080 flag/smoke loops, no `--flag-loop`; keep that).

## To do, in order
1. **S6 4K render** (0 cr, ~4 h, background, affinity FFFF3FFF, watchdog + auto-relaunch, `_tmp_` names), after the still check:
   `python tools/render_s6.py <OUT> --scale 2.0 --final --v6 --v7 --v7-feather --v7-alpha --warm 10 --retime-fr`, per the plan
   (ProRes 4444 straight alpha, 2880/3600/2880x2160, 2910 f, 121.25 s). Then the same at `--scale 1.0` (1080 + CLEAN).
   Mux `G:\SOTR\HF\Final changes\Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` with `-c:v copy -c:a pcm_s24le`. Check
   the sound by correlation. Check how render_s6 names/splits the 3 walls in its output first (read main() 2541-2634).
2. **S9 re-time** in `tools/court_ext.py`: add env `EXT_F24=1` (on top of the EXT5 env): `LOOK_OUT` 858 -> 906 (+48),
   b5 strike knock (knocks[2], after the E5 +1) +5 frames (1279 -> 1284). b7 unchanged. If `lookup_to_raise` finds no exit
   (the gap to the strike shrinks from 183 to ~140 f), report and try +44..+48. EXT5 env (from the summary):
   `EXT_BP='S9-CRT-IDLE_v15back_*.mp4' EXT_BP2='S9-CRT-IDLE_v15back2_*.mp4' EXT_BP3='S9-CRT-IDLE_v15back3_*.mp4'
   EXT_RAMP_MODE=motion EXT_LOOKUP='S9-CRT-IDLE_v16fwd_*.mp4' EXT_E5=1`; `python tools/court_ext.py render OUT --beat 5cut --full`
   -> `S9_b5_CENTRE_court_GENJUDGE_F24_FULL.mp4`. b3/b7 reuse the EXT5 files.
3. **Review** in `tools/s9_darren_review.py`: add `--f24 WORDS_JSON`: like `use_e5` but MIX = Darren's final local copy,
   picture CUTS still applied, SOUND NOT CUT (take his file straight, `atrim=0:dur`; no FADES), `verify` with src = t,
   WORDS = `_FINAL_whisper_words.json`, b5 strike caption knot 243.0 -> 243.21. Build `S9_GENJUDGE_3wall_review_F24.mp4`,
   verify lag 0, look at the look-up (222.6 s) and strike (237.25 s) frame by frame at 24 fps. Open the folder in Explorer.
4. **Show folder clean-up** (Homie's words 3): fold `01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector/` into the
   show folders where each file applies (e.g. S9 raft water + its frame-rate options next to the S9 show files; the
   B/C/D options in a clearly named sub-folder or with clear names). Moves inside D: with checksums; update
   `00_READ_ME_FIRST.txt` and `SOTR_MEDIA/README.txt` and the CLAUDE.md Folders rule; then MIRROR the same layout on the
   T9 (`G:\SOTR\HF\SOTR_MEDIA`) with sha256 — copy new layout, move the T9's own old copies the same way; nothing is
   hard-deleted (any leftover goes to a dated `_DELETE_ME_` bin). Do NOT promote new S6/S9 finals until Homie looks.
5. Wrap: LOG, REGISTER, NEW-SESSION, CLAUDE.md stage; commit; push; `git pull` on G:; T9 media copy.
