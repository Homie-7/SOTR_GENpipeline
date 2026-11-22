# HANDOFF 2026-11-22 EXT5 (Homie's notes on the EXT4 review)

Mode: POST/script. 0 cr. Balance 2,443, floor 1,500. Review only: no upscale, no promotion.
Read first: `CLAUDE.md`, `docs/HANDOFF-2026-11-22-S9darren.md`, `docs/HANDOFF-2026-11-22-EXT4.md`, `docs/HANDOFF-2026-11-22-EXT4b.md`, then this file.

## State (done, committed f740038, on the T9)
- `04_WORKING_FILES/S9_gen_judge_review/S9_GENJUDGE_3wall_review_EXT4.mp4` (351.17 s, sync lag 0 at 15 points).
  Built by `tools/court_ext.py` (env `EXT_D22=1`) + `tools/s9_darren_review.py --d22` (Darren's cuts 183-189 s and 248-290 s,
  straight splices). b5 `S9_b5_CENTRE_court_GENJUDGE_EXT4_FULL.mp4`, b7 `S9_b7_CENTRE_court_GENJUDGE_EXT4.mp4`, b3 = EXT2.
- Review-clock = uncut clock minus 6 s after 183.0, minus 48 s after 242.0 (review).
- EXT4 audit: b5 strike impact at review 4:01.0 (uncut 247.0, KNOCKS 1374); snip splice 4:02.0; b4 splice 3:03.0; b7 impact 4:51.083
  then black next frame (Q5 capper A f0-53).
- Sound at the splices (measured): 4:02.0 goes from ~0 dBFS to -88 dB in one sample (hard stop); 3:03.0 drops -21 -> -45 dB.
- Watchdog gotcha: `_launch_affinity.ps1 -File` splits a `--title` with spaces. Use `_watch_review_m10o_b.sh` style (python direct,
  affinity set after start via Get-Process).
- S6 map-to-ship preview done (`04_WORKING_FILES/S6_map_to_ship_review/`), reported. T9 clone has macOS `._pack-*` junk in
  `.git/objects/pack` (warnings only; pull works; not touched).

## Homie, 22 Nov evening (verbatim)
"At about 357, I think there is a gavel hit, but he's just holding the gavel up top, And then around four seconds, you see the
gavel being dropped, but then there is no sound matching to it. So, can you just match the Gavel hit with the sound because we
are following the sound here
After he finishes saying, cannot be held responsible in the gavel hits, can you make that fade a little bit after the gavel has
been hit so that the impact stays Because right now it's just kind of disappearing mid hit, And we don't really register the
impact the same way, there is quite a bit of echo That we can utilize as a fade

Also on a side, can you just sync the script to match what is being said underneath so the text is actually following what is
happening on the screen

Can you fix all of this, please? Also, if his sound cuts off, then we can probably ease that rather than making it a harsh cut,
and then based on our video, he will be able to adjust his sound design?"

## What this means (EXT5 build)
1. b5 strike: FOLLOW THE SOUND. Darren's mix has a gavel hit near review 3:57 (= uncut ~243.0 s, the old EXT3 KNOCKS 1278 spot);
   the picture strike is now at 4:01.0 with no sound. Measure the gavel transient(s) in the cut mix 3:50-4:05 (onset detection),
   then put the picture impact frame ON that transient (likely back to ~1278; check the look-up U + gap-2 plan still solves).
   Check what then fills to the snip (strike play-through + follow-through, then the snip at 4:02.0): no jump, no frozen hold.
   This overrides Darren's "gavel at 4:07" note: Homie says the sound leads.
2. b7 capper: do NOT snap to black on the impact frame. Play the hit + follow-through (approved A f54-95) and FADE the picture to
   black over the gavel's echo tail in his mix (measure the echo decay after uncut 339.1 s / review 4:51.1; fade ends where it is
   near silent). The impact must register first.
3. Captions: re-time every caption line to what is said in his cut mix (faster-whisper word timings, medium, en, on the cut
   review audio), so the text follows the speech. Stage directions keep their picture events.
4. Sound splices: Homie now allows an EASE at Darren's cuts (not a harsh cut): short fades at 3:03.0 and 4:02.0 (e.g. 0.3-0.5 s
   fade-out of the outgoing sound into the splice; pick by ear/measure; no other level changes). Darren will then adjust his
   sound design to our video. Say exactly what fade you used in the report.
5. Render b5 + b7 as EXT5 (new names, `_tmp_` + watchdog + affinity FFFF3FFF, `tools/court_ext.py` new env flag so EXT4/EXT3
   still rebuild identical), then `S9_GENJUDGE_3wall_review_EXT5.mp4` + verify (lag 0). Audit at 24 fps with contact sheets.
   Never overwrite EXT3/EXT4 or `_KEEP_EXT2_GOOD_fallback_2026-11-21/`. Open Explorer; report to Homie in STE.
6. Wrap: LOG, REGISTER, NEW-SESSION top line, CLAUDE.md stage, commit, push, T9 pull + sha256 media copy.
