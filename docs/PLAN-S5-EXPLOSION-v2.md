# PLAN — S5 cannonball explosion, v2 (rethink after F34)

2026-11-25 · IMG/plan only, no video spent · style frames: `prompts/S5-CANNON-RETHINK-SF.txt`
Brief: `docs/BRIEF-F31-CANNONBALL-BLADES.md` (Homie F34 verbatim, F35 decisions). Review v1 (`04_WORKING_FILES/S5_cannonball/review_v1/`) is rejected: "a cheap fade".

## 1. The look we are matching (study in `04_WORKING_FILES/S5_cannonball/rethink_v1/frames/`, sheet `_contact_sheet_frames.jpg`)

- S5 end (all walls, nearly static for 430 s): warm rose-orange dusk, low sun upper-left in the CENTRE sky behind thin cloud, back light toward the audience.
  Pink-salmon haze over dark brown-olive ground with green scrub. LEFT = grassy hill, small fires far right. CENTRE = wide plain, camp on the right horizon,
  smoke plumes at both sides, a yellow fire glow lower left. RIGHT = tent camp on a ridge, scrub slope. FLOOR = top-down dry leaves and grass, a diagonal path.
- S6 start: NOT a full-frame smoke. Black upper half, a low band of rust / red-brown smoke with orange embers (mean ~RGB 30,14,7). S6 has no FLOOR file (black).
- So the end state is: the dust takes every wall, then darkness falls from the top and the smoke settles low = S6 frame 0 ("Smoke and darkness cover the camp").

## 2. The event, beat by beat (t = 0 is the current S5 last frame; 12 s; same times on all four walls)

| t (s) | RIGHT | CENTRE | LEFT | FLOOR | Sound |
|---|---|---|---|---|---|
| 0.0-1.0 | calm dusk | calm | calm | calm | rising whistle of round shot |
| 1.0-1.8 | the ball crosses high to low, exits the CENTRE-side edge | — | — | — | whistle peaks, Doppler |
| 1.8-2.4 | — | the ball enters from the right edge, falls to mid-ground centre | — | — | |
| 2.4 | — | IMPACT on the ground | — | shock: dust jumps | deep thud + crack |
| 2.4-2.6 | — | short dull orange powder flash at the base (3-5 frames) | — | — | |
| 2.6-4.5 | smoke rolls in from left edge | dark earth column, turf, stones, splinters on arcs; grey-brown smoke rolls out | dust begins at right edge | clods land, dust spreads | earth rain, rattle |
| 3.5-6.0 | dust wave, falling debris | column falls back, dust fills | dust wave from the right edge, falling debris (frame b) | covered in dust, debris on ground | roar of the wave |
| 6.0-8.0 | full-frame dust | full-frame dust | full-frame dust | full-frame dust | low rumble |
| 8.0-12.0 | darkness from the top, rust smoke settles low, embers | same (frame c) | same | fades to black | wind, crackle, embers |
| 12.0 | = S6_RIGHT frame 0 | = S6_CENTRE frame 0 | = S6_LEFT frame 0 | black | hands over to S6 audio |

Nothing straddles a seam except light, dust and smoke (allowed). The ball is two separate passes (RIGHT exit, CENTRE entry), timed by script.

## 3. Route (recommended): image-to-video per wall, start AND end frame locked

- Seedance 2.5, `omni_reference`, `start_image` = that wall's real S5 last frame, `end_image` = that wall's S6 frame 0 (16:9 bottom-anchored crop,
  already made: `frames/S6_*_first_16x9.png`). FLOOR: end_image = black. Locked camera, 12 s, sound ON, 16:9, one prompt per wall from the beat table.
- Why: the clip starts on the exact S5 picture and lands on the exact S6 picture by itself, so there is no fade and no matte reveal.
  The style frames show the model keeps the S5 light and framing in an edit (frames a, b PASS).
- Order (AUTONOMOUS-GEN THE GATE, one change per version, probe short first):
  1. CENTRE probe, 12 s, 480p draft (~36 cr). Check: ball visible, flash brief, no fireball, locked camera, lands on S6.
  2. If PASS: RIGHT, LEFT, FLOOR at 480p draft (~108 cr) to check the four play in sync.
  3. Finalize / regenerate the chosen four at 1080p (768 cr) only with Homie's yes. Then 4K by Topaz like the rest of the show.

What the script does (0 cr, `tools/` new `cannon_v2.py`, affinity FFFF3FFF):
- Sync: align the four clips on the impact frame (detect the flash peak on CENTRE, the dust start on the others); trim to a common 12 s.
- Ball: if a pass is missing or mistimed on RIGHT/CENTRE, re-time that wall by a few frames (no comp of a new ball unless Homie asks).
- Join into S6: conform 25 fps S5 / 24 fps S6 (render the explosion at 24 fps, retime S5 side), match the last second's grade to S6 frame 0
  so the cut onto S6 is invisible, and fit 16:9 into the 4:3 / 5:3 wall raster the same way the S5 show file does.
- Sound: cut the generated audio of each wall in, CENTRE carries the impact; cross-mix into S5's tail and out to S6's head (verify by correlation).
- Clean first: CLEAN master per wall in `03_CLEAN_MASTERS_no_edge/`, edge versions rebuilt from clean.

## 4. Deliverables (no version numbers in show names; versions in REGISTER)

- `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05_the-camps/S5_{LEFT,CENTRE,RIGHT,FLOOR}_camps.mov` re-made: the current S5 picture + the 12 s explosion
  at the end, sound in, full picture at start and end. Its last frame = S6's first frame, so S5 flows into S6 on the operator's GO.
- CLEAN copies in `03_CLEAN_MASTERS_no_edge/`; old S5 files to `04_WORKING_FILES/superseded/`; the generated clips in `02_APPROVED_BUILDING_BLOCKS/` on approval.

## 5. Cost (estimate_video_cost, Seedance 2.5 omni_reference, 16:9, sound on; quoted 2026-11-25)

| Option | What | 480p draft | 720p | 1080p |
|---|---|---|---|---|
| A (recommended) | 4 walls x 12 s, start+end frame | ~144 (36 each) | 336 (84 each) | 768 (192 each) |
| A-short | 4 walls x 8 s (tighter: wave 2.5 s, settle 3 s) | 96 (24 each) | 224 (56 each) | 512 (128 each) |
| B | CENTRE generated 12 s; LEFT/RIGHT/FLOOR 8 s | ~108 | 252 | 576 |
| Probe only | CENTRE 12 s | ~36 | 84 | 192 |

Quoted points: 8 s 720p 56, 8 s 1080p 128, 12 s 720p 84, 12 s 1080p 192, 8 s 480p draft 24. The 12 s draft figure is derived (3 cr/s).
Balance ~2,251.85 after this session's 6 cr. Anything over ~100 cr asks Homie first.

## 6. Risks

1. Fireball: the model reaches for a modern HE blast. Mitigation: "solid iron round shot, black powder, brief dull flash, grey-brown smoke" + start frame realism; reject on sight.
2. Sync across four separate generations: impact and wave times drift. Mitigation: script re-time on the impact frame; dust is forgiving, the ball is not.
3. Camera shake / drift on impact (Seedance likes a shake). Locked camera stated; a shaken take fails THE GATE.
4. The end_image pull: the model may cross-dissolve to S6 instead of settling (the "cheap fade" again). Check the last 4 s at 24 fps.
5. Aspect: S5 is 16:9, S6 is 4:3 / 5:3. The S6 end frames are crops; the join needs the same fit as the S5 show file. Frame rates 25 vs 24.
6. Seams: debris must stay on its wall; only dust, smoke and light cross.
7. FLOOR top-down view: the model may not understand a ground-level hit seen from above. Fallback: FLOOR from the script (dust + falling clods plate).
8. Cost: the full set at 1080p is 768 cr, near the 1,000 session cap.

## 7. Homie decides

- The look: style frames a / b / c (`04_WORKING_FILES/S5_cannonball/rethink_v1/`).
- The length: 12 s (recommended) or 8 s.
- The go-ahead for the CENTRE probe (~36 cr draft, or 84 cr at 720p).
