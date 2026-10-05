> SUPERSEDED 6 Oct 2026 by docs/VID-BRIEF-S7-INTRO-v2.md (Homie rejected the v1 intro). Kept for its connector facts.

# VID BRIEF — S7 intro flight (overnight 6 Oct 2026, delegated by Homie)

Written by the IMG session for a FRESH VID session (house-rules MODE: image and video never share a chat).
Homie is asleep and delegated the calls: *"I trust your judgment… I'm really hoping that this animation and everything is
done in the morning."* Look decisions you make tonight are PROVISIONAL, written up for his review with a recommendation.

## Load first
house-rules (+ `references/findings-video.md` in full), shotcaller-v1. MODE = VID. Read `CLAUDE.md`,
`docs/PLAN-SHIP-INTRO.md` (§1 THE INTRO, Sahaj's notes, the exceptions), `docs/AUTONOMOUS-GEN.md` (pre-flight, THE GATE,
stop rules), `PIPELINE.md` (the connector table + traps, ~lines 78-140), `prompts/S7-INTRO-F1.txt`, top of `LOG.md`.

## The job, in priority order
1. **THE FLIGHT** (CENTRE, 16:9 generated, later cropped 5:3 = 1800x1080). Start frame = the HAZED F1:
   `/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/2_intro/S7-INTRO-F1_v1_1714a32e_haze.png`
   (open it first: open Atlantic, bright late morning, horizon low, the Medusa small and soft under full sail dead
   centre, a goéland argenté gliding left-foreground toward her). Upload it (`media_upload` -> curl PUT -> `media_confirm`).
   The action (PLAN §1): the camera follows the gull low over the swell toward the ship; the ship grows (a French frigate
   of 1816, three masts, sails SET, white Bourbon ensign at the stern); the gull rises over the stern rail.
   Homie's notes on F1 (5 Oct): real aerial perspective in the distance, real physics, the ship NOT crisp from beside
   the bird, depth of field. The camera MOVES in this sequence only (PLAN exception); smooth, following, no shake.
2. **THE LANDING**: a Sequel (`video_extension` forward) from the chosen flight: the gull lands on the rail, a wing
   sweeps the lens = the cut onto the deck (the deck walls already exist: `3_walls/assembled_v1/`).
3. Only if 1+2 are done and budget remains: a review cut (flight + landing joined, 5:3 crop, sound kept) at
   `04_WORKING_FILES/S7_ship/4_intro_video/S7-INTRO_review_v1.mp4`, then a cut on to the day deck still (the three walls
   come up after the wing sweep) as a 4680-wide preview.

## Settings (state the FULL block in every run message and file header)
Seedance 2.5 (`seedance_2_5`) · `omni_reference` with the haze frame as `start_image` (and/or `image_references`) ·
16:9 · 1080p · `bitrate_mode: high` · sound ON (`generate_audio: true`, SOTR rule: generation audio stays on) ·
`use_unlim: false` · batch 1 unless the question is luck.
**Known connector limit (PIPELINE):** `start_image` in omni_reference did NOT pin frame 0 in Sept (a loose reference).
Measure it on the probe (frame 0 vs the haze frame). For a moving shot that's acceptable if the look carries; the
Scene 6 hand-off ("the Medusa appears on the horizon") only needs the same KIND of opening. If it fails twice on look,
check `models_explore` for an image-to-video model that pins the first frame before a third Seedance try.
There is also a `draft` (480p) + `draft_job_id` finalize option: get_cost it; it may be the cheaper way to probe the
full length. Your call, logged.

## Credit rules (Homie's, all of them)
ONE Higgsfield job at a time · `get_cost: true` first (count 2 reports ONE take) · `transactions` after every submit ·
**a 4 s probe before any long take** · stop after two failed versions of the same defect · a transport error may still
have submitted (check transactions before resubmitting) · decline any preset (`declined_preset_id`).
**Cap for this VID session: 600 credits.** (Balance 1,541.49 at the hand-off; the week must end with 500+.)

## After every run
Download ONLY with `python3 tools/fetch.py URL OUT` (DNS here is intercepted). Probe (size, fps, frames, audio), a
contact sheet across the whole clip (never one frame), and check: one ship, sails set, nothing newer than 1816, the gull
still a herring gull (white head, grey mantle, black tips with white mirrors, yellow bill + red spot, pink legs), no
on-screen text, no cut, smooth camera, the ship soft in the distance. Name takes `S7-INTRO-FLIGHT_v<N>_<jobid8>.mp4`.
Python deps: `PYTHONPATH=/private/tmp/claude-502/-Users-homie-Documents-SOTR-GENpipeline/2e0ad28c-7a79-4ec9-a102-cd15be06f811/scratchpad/py`
(numpy, opencv, pillow).

## Files you own tonight
- Media: `/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/4_intro_video/` (create it).
- `prompts/S7-INTRO-FLIGHT.txt`, `prompts/S7-INTRO-LAND.txt` (header = full settings block, PREDICT line, versions).
- `LOG.md`: add your rows at the TOP of the table (newest first, same columns as the S7 rows).
- `docs/NEW-SESSION.md`: append a short `VID (night 6 Oct):` status line under THE TASK after each step.
- Do NOT commit or push (the IMG session wraps). Never delete; rejected takes stay in the folder, marked in LOG.

## Report back (your final message)
What ran (job ids, credits each, total), what was chosen and why, file paths, what failed and the diagnosis, and the
exact next step. Plain and short.
