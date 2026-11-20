# S9: Darren's judge mix vs our beat files (measured 2026-11-20, M9g). 0 cr.

Tool: `tools/s9_mix_measure.py` (read-only). Its envelope CSV, in 0.5 s steps, is at
`D:\SOTR\SOTR_MEDIA\04_WORKING_FILES\S9_darren_cut\_measure_env.csv`.
Mix: `G:\SOTR\HF\Final changes\the judge TO BE CUT DOWN 19112026.mov`, 399.17 s. The picture is our preview and its length
matches our 9580 frames.

## Facts
- **His sound is on our clock.** Lag is 0.00 to 0.09 s wherever his mix still holds our files' sound (0, 70, 190, 320,
  330, 350 s). Everywhere else it is his own sound (corr ~0).
- **Digital silence** (< -90 dB):
  - 116.0-117.0 s: a 1 s pause.
  - **253.5-290.0 s (36.5 s)**, the tail of court b5. His sound fades out from 247 to 253.5.
  - **357.5-399.0 s**: the last 1.5 s of salon b8 and ALL of studio b9. His sound fades out from 353.5.
- Per beat file:
  - b4 and b6 (studio): his ambience throughout, about -31 dB, 0% silent.
  - b5: 36% silent.
  - b9: 100% silent.
- His judge speech in b5 is concertina'd into 190-247 s. The loud peaks (likely the gavel and "Order!") are at
  198.0, 207.5, 212.5, 219.5, 226-227.5, 233.5, 243-243.5 and **245.5-246.0 (the loudest, -9.4 dB)**.

## Decision (by measurement)
- **"About 35 s" = the b5 tail (36.5 s).** Court b5 is cut from 101 s to about **64.2 s**: it ends at mix 254.0, once his
  fade has finished. Everything after it moves 36.6 s earlier (b6 then starts at 254.0).
- **The b9 silence is not a cut.** b9 is the studio finale with Géricault's live lines. The b4 and b6 studio beats carry
  his ambience; b9 carries none, so his mock-up simply ends after the verdict and the salon. Adding 41.5 s to the cut
  would make 78 s, not "about 35". b9 stays 40.2 s. **Flag to Homie:** b9 has no sound in his mix.
- **The b5 strikes must move, not just be trimmed.** Our b5 cues (`render_court.py` BEATS[5]) strike at 0.5, 45 and 85 s
  into the file, which is mix 190.3, 234.8 and 274.8. The 274.8 strike falls in his silence.
  - New cues: 0.5 s (190.3), then on his peaks: about 43.7 s (233.5) and about 55.7 s (245.5, the final "Order!").
  - Refine all three to his onsets at 0.02 s resolution before building: run an onset detector on 185-250 s, and listen
    around each peak.
- **Build (next chat):**
  - Add a b5 cut-length beat to `court_behind_paper.py` / `render_court.py` with `length=64.2` and the new cues. Keep the
    old BEATS[5] and add a new key or flag, so the shipped b5 file stays bit-identical without it.
  - Render it at review scale to `04_WORKING_FILES\S9_darren_cut\`.
  - Re-time `s9_animatic.CLIPS`: b5 n becomes about 1541 frames, TOTAL about 8697.
  - Make a 3-wall WhatsApp review (`share_previews.wa_s9` pattern) on HIS audio: his mix with 253.5-290.0 removed (a
    straight splice in the silence, so it is click-free) and his audio from 290.0 on shifted onto the new clock.
  - Review only. Nothing goes into 01_FINAL_FOR_SHOW.

## Idle judge (next, after the cut): what is under the holds
Not analysed yet. The holds are the b5 RAISED stretches between strikes (190.3-233.5 and 234.8-245.5 on the new cut),
plus b3 and b7. Use the CSV and listen: is it a crowd hubbub, room tone or breath? Then propose 2-3 options to Homie
BEFORE building anything (stills or short clips, script only).
