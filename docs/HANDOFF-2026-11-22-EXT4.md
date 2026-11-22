# HANDOFF 2026-11-22 EXT4 (state save; the S9 judge EXT4 build is half done)

Mode: POST/script. 0 cr. Balance 2,443, floor 1,500. Review only: no upscale, no promotion.
Read first: `docs/HANDOFF-2026-11-22-S9darren.md` (Darren's notes, the 7 steps), then this file.

## Homie, 22 Nov (verbatim, this chat)
"Okay, sounds like you have a decent plan. Again, we will not make changes to Darren's sound itself at all. We'll just
follow his instructions. I agree with the middle cut issue with the gavel and everything. Feel free to adjust things so
that everything looks nice and seamless. I'm hoping this is not a major issue. I am okay with the suggestions you have
made, so go ahead with that"

"I have another side task for you after that with the S6 map scene where we have the map fading into Sahaja's mock-up
scene. Starin has also shared a sound sample that he has made for the next scene, which brings in Sahaj's new render. I
want you to create maybe like a 30 second or maybe like one minute preview using that sound to show how our Africa map
will fade to Sahaja scene and align it in terms of how it would work. So from the moment Senegal appears on the screen,
I think Direct sound design will start and then it will nicely merge with Sahaja scene as our map frames already. So
yeah, just look at it, figure it out. But yeah, do the judge thing first"
"G:\SOTR\HF\Final changes\221126\Map to ship 22112026_2_DarrinSoundSahajRen.mov"
"I'm going to step away for a while, so yeah, continue starting new chats and continue working"

=> Sound rule: Darren's sound is NOT changed. Only his cuts (183.0-189.0 s and 248.0-290.0 s) are applied, as
   straight splices (no fades, no level changes). If a splice clicks, report it; do not fix it in his sound.

## DONE (this chat)
- Remote Control on. Old star chat local_85933f19 could not be archived (it had live work): archive it now.
- `tools/court_ext.py`: env `EXT_D22=1` (EXT3 unchanged without it; the code paths are only under D22):
  b5 last strike 1278 -> `D22_STRIKE` 1374 (= 247.0 s); after the impact A54..76 at out 1375-1397, black over
  `SNIP` = out 1398-2405 (mix 248.0-290.0 s), A77..94 at out 2406-2423 (the strike plays through across the snip).
  b7 Q5 capper = A f0-53 (impact at out 388), black from out 389.
- Plans checked: b5 `plan --beat 5cut --full` solves: U look-up unchanged (859-1043), gap-2 exit C rate 1.000,
  impacts [25, 546, 1374]. b7: impacts [23, 388], black 389-479.
- faster-whisper (medium, en) on his 22 Nov mix: "Order! Order!" 225.84-228.32; "Get the traitors out" 228.5-231.8;
  last "Order!" before the strike 245.30-246.22 s (so 247.0 is after it, OK). Other "Order!" at 263.6 (inside the snip)
  and 290.64 s (just after the snip, plays over the last 0.75 s of b5). Sarah's line is not in his mix.

## TO DO (in order)
1. `tools/s9_darren_review.py`: add `--d22`: MIX = `G:\SOTR\HF\Final changes\221126\the judge CUT DOWN 22112026_2.mov`,
   uncut placement as --mix21 (CUT=0, PAINT=True) PLUS `CUTS = [(183.0, 189.0), (248.0, 290.0)]`:
   - each lane: trim/concat out the cut frame spans (4392-4536, 5952-6960) BEFORE wa_filter (so the clock and captions
     run on the new timeline); total 9580 -> 8428 f (351.17 s).
   - captions: lines() remap through the cuts; segment 3 of b5 (orig b5+85..b5+100.5, "Bangs the gavel") re-pinned to
     about 245.0-248.0 s; drop segments that end up zero-length.
   - audio: his mix with the same two spans removed, straight concat, nothing else.
   - verify(): map review t -> mix t through the cuts (lag 0 expected).
2. Watchdog `_watch_ext_m10o.sh` (copy of `_watch_ext_m10m.sh` + `export EXT_D22=1`, log names m10o): render
   b5 `S9_b5_CENTRE_court_GENJUDGE_EXT4_FULL.mp4` ("5cut 2424 ... --full") and b7 `S9_b7_CENTRE_court_GENJUDGE_EXT4.mp4`
   ("7 480 ..."), detached, affinity FFFF3FFF via `_launch_affinity.ps1`. b3 = EXT2 file.
3. Review `S9_GENJUDGE_3wall_review_EXT4.mp4` (`--d22 --b3 ..._EXT2.mp4 --b5 ..._EXT4_FULL.mp4 --b7 ..._EXT4.mp4`) with
   a watchdog; verify lag 0. Audit at 24 fps: strike at new 4:01.0 (247.0-6), the snip splice (new 4:02.0), the b4
   splice (new 3:03.0), the b7 snap (old 5:39.1 -> new 4:51.1). Never overwrite EXT3 or `_KEEP_EXT2_GOOD_fallback_2026-11-21/`.
4. Open Explorer on `SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review/`. Report to Homie in STE: the changes and the
   concerns in HANDOFF-2026-11-22-S9darren.md (strike played through; his 248-268 s sound is gone by his cut; every later
   cue moves 6 s, then 48 s earlier; the 290.64 "Order!" now plays over the end of the strike).
5. THEN the S6 side task (below). 6. Wrap: LOG, REGISTER, NEW-SESSION top line, CLAUDE.md stage, commit, push, T9.

## S6 side task (after the judge)
Preview 30-60 s: our S6 v14 Africa map (3 walls, `01_FINAL_FOR_SHOW` S6 files / `render_s6.py`) from the moment
"Sénégal" appears, fading into Sahaj's scene, on Darren's sound from the file above (look at it first: it holds
Darren's sound + Sahaj's new render). Align the map's end with where his sound/Sahaj's render starts so the merge reads.
Review file only, in a new `04_WORKING_FILES/S6_map_to_ship_review/`. 0 cr. Do not change Darren's sound.
