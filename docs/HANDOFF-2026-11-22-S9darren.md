# HANDOFF 2026-11-22: S9 judge, Darren's 22 Nov notes -> new 3-wall review (EXT4)

Mode: POST/script. 0 cr planned (balance 2,443, floor 1,500). Review only: nothing upscaled, nothing into 01_FINAL_FOR_SHOW.
Read first: this file, `docs/HANDOFF-2026-11-21-M10n.md` (EXT3 build facts), `tools/s9_darren_review.py`, `tools/court_ext.py`.

## Homie, 22 Nov (verbatim)
"feedback from darren has arrived, He has requested some changes. I don't think there's anything crazy, but it does affect
some of the timing questions we had earlier. He took our file, which was the S9_GENJUDGE_3wall_review_EXT3 And I think made
some changes to it ... `G:\SOTR\HF\Final changes\221126\the judge CUT DOWN 22112026_2.mov`"
"can you go through this and identify what we need to change and then prepare another preview?"
"If there are any concerns pointed out, but I don't think there's any big issues out there"
Still no feedback on the S6 French wars: wait for it.

## Darren (verbatim, via Homie)
"(still some video trimming to do - cut 3:03-3:09; 4:03 gavel animation needs to come at 4:07 (after the last "order!")
then snip 4:08-4:50; 5:40 the gavel landing should snap us to black; please ignore the cicadas in the salon - fixing that
now.. We'll talk tomorrow about the music for the painting!)"

## Measured (this chat)
- His file: 1600x522 h264 24 fps + pcm_s24le 48k stereo, 399.17 s = SAME length as EXT3. Picture = our EXT3; the AUDIO is
  his NEW mix. vs the 21112026 mix it differs 1:19-3:31 (salon sound, cicadas: ignore) and 5:23-5:39 (levels), and he has
  emptied the spans he wants cut: 183-189 s fades to -45 dB; 268?-290.25 s is digital silence (-107 dB); sound returns 290.3.
- All his timecodes are on HIS file's clock (= the EXT3 clock, uncut). Beat starts (s9_animatic.S): b4 LEFT 117.375,
  b5 CENTRE 189.75 (2424 f), b6 LEFT 290.75, b7 CENTRE 322.917 (480 f), b8 RIGHT 342.917, b9 LEFT 358.958.
- b5 knocks (court_gen.KNOCKS['5cut']): out 25, 546, 1278 (Q3). 1278 = 243.0 s = his "4:03". Look-up U sits in gap 2.
- b7 knocks: 23, 388 (Q5 capper). 388 = 339.08 s; his audio has the gavel transient at 339.1 s = his "5:40".
  The Q5 capper now plays approved A f0-95 (impact f53, then 42 f follow-through), then black.

## The changes (what to build)
1. b5 strike +4 s: KNOCKS['5cut'][2] 1278 -> 1374 (= 247.0 s). timeline() refills gap 2 (look-up + read) by itself;
   check the plan (`court_ext.py plan --beat 5cut --full`, EXT_LOOKUP set as in M10n) solves with rate <= 12 %.
   Make it an env flag (e.g. EXT_D22=1) so EXT3 still rebuilds bit-identical without it. Optional: confirm with a
   faster-whisper word pass that the last "order!" ends before 247.0 s; nudge the impact if not.
2. Snip 4:08-4:50 (248.0-290.0 s): picture and HIS sound, same span. To avoid a jump inside the judge, end b5 on the
   approved strike played through: after the 1374 impact, A f54-95 = 42 f = 1.75 s = exactly 1 s before the snip +
   the 0.75 s left of b5 after it (290.0-290.75). Then CENTRE black, b6 LEFT starts as before. (Darren's literal cut would
   jump from mid-strike to a reading frame.) Sound: his 248.0 is loud (-7 dB) into his silence: a 20-30 ms fade at the splice.
3. Cut 3:03-3:09 (183.0-189.0 s): picture (end of b4 LEFT, check what is on screen) and his sound; his sound is ~-40 dB
   there, clean splice. Everything after moves 6 s earlier; after the snip 48 s earlier. New total 351.17 s (8428 f).
4. b7 snap to black at the gavel landing: Q5 capper = A f0-53 (impact frame shown), black from the next frame
   (no shake tail, no follow-through). Same env flag.
5. Captions/beat text in s9_darren_review: re-pin the moved strike and shift for both cuts (add a cut list, e.g.
   `--d22` with CUTS = [(183.0, 189.0), (248.0, 290.0)] on his mix `221126/the judge CUT DOWN 22112026_2.mov`).
6. Render b5 `S9_b5_CENTRE_court_GENJUDGE_EXT4_FULL.mp4` + b7 `S9_b7_..._EXT4.mp4` (detached, affinity FFFF3FFF, watchdog
   from `_watch_ext_m10m.sh`, _tmp_ names), b3 = EXT2. Then `S9_GENJUDGE_3wall_review_EXT4.mp4`; verify sync vs his
   mix with the same cuts applied (lag 0). Audit the strike, both splices and the b7 snap at 24 fps (contact sheet).
   Never overwrite EXT3 or `_KEEP_EXT2_GOOD_fallback_2026-11-21/`.
7. Open Explorer on `04_WORKING_FILES/S9_gen_judge_review/`. Report to Homie in STE: the changes, the concerns below.

## Concerns to tell Homie
- The snip as written cuts mid-strike to a reading frame; we play the strike through instead (1.75 s), same length.
- The snip cuts his sound mid-swell at 248.0 s (a short fade only). His later sound from 248-268 s is lost: his choice.
- Cutting 54 s moves every later cue; any timing he gave earlier for the end (b6-b9) shifts by 48 s.
- "ignore the cicadas": no action. Music for the painting (S2): tomorrow's talk, no action.

## Wrap
LOG, REGISTER, NEW-SESSION top line, CLAUDE.md stage, commit, push, T9 pull + sha256 media copy.
