# Starting a new session

Paste the block below as the first message of a fresh Claude Code chat, run from the
`SOTR_GENpipeline` folder. `CLAUDE.md` loads automatically. This block tells the session
what the task is right now.

**One session at a time.** Close the old chat first. Run `git pull` before starting and
`git push` at the end.

**This file goes stale unless it's updated on every wrap.** If it disagrees with
`CLAUDE.md` → "Current stage," `CLAUDE.md` wins. Fix this file, then act.

---

```
Load house-rules, declare MODE, then read CLAUDE.md, STAGE.md, PIPELINE.md, LOOK.md,
SHOTCARDS.md and docs/AUTONOMOUS-GEN.md before anything else. State in one line what you
loaded and which mode you're in. Ask Homie what we're working on before doing anything.

This is SOTR: theatre projection backgrounds for Secret of the Raft, built in Higgsfield.
NOT a film. Live actors perform in front of three surfaces, named as the AUDIENCE sees them:
LEFT flat 4800x3600, CENTRE (back wall) 6000x3600, RIGHT flat 4800x3600. Locked cameras,
walls as walls at true scale, no people in any plate, nothing newer than the scene's era.

THE TASK, RIGHT NOW (8 Oct, end of day): HOMIE'S REVIEW of the two fixes, both rebuilt today. Then 4K + destruction.
  WATCH (T9 04_WORKING_FILES/S7_ship/):
  1. 4_intro_video/rev/S7-INTRO_3walls_v6_INTO_DAY_IDLE.mp4 = INTRO v6: flight -> boards amidships -> lands EXACTLY on the
     deck walls -> the day idle. (Homie OK'd the reversed draft and the finalize.)
  2. 6_review/S7-SHIP_idle_BOW_v1_vs_v2_day.mp4 (bow before/after) + 6_review/S7-SHIP_idle_arc_preview_v2.mp4 (all 4 idles).
  NEXT after his verdict: (a) 4K: ByteDance video upscale of the two intro parts + the 4 idle clips, then rerun
  s7_idle.py / s7_intro_3walls.py --constant on the 4K clips; (b) the same horizon motion ramped onto the intro's held end
  (intro -> idle currently dissolves into the moving idle over 0.5 s); (c) the destruction (wreck state), script first.
  Known residuals: idles = a faint 1 px seam in the narrow sea strip between the forecastle rail and the horizon when the
  sea heaves; intro = the main course is SET outside (as the F1 opening) but FURLED on our deck (as the approved plate).
  Mode VID for any generation; script work is POST. Credits: CLI balance 935 after today (315 spent).

HIGGSFIELD NOW = THE CLI (set up 8 Oct; the claude.ai connector is not connected on this Claude account):
  binary ~/.npm-global/bin/higgsfield (aliases hf, higgs; PATH added in ~/.zshrc), signed in; workspace "Private"
  (a4274571-f90b-43b3-9485-c41e2e15cc59, plus plan, 1,250 credits at setup). Models: seedance_2_5, nano_banana_pro,
  bytedance_image_upscale, topaz_hyperion_2_5. Commands: `hf generate cost|create|wait|get|list`, `hf upload`,
  `hf model list --video`, `hf account status|transactions`. Skills installed: higgsfield-generate (+6 others) in
  ~/.claude/skills (read higgsfield-generate before the first call). The same rules apply: one job at a time, cost first,
  transactions after. Media uploaded to the OLD account (media ids above) do NOT exist on this one: re-upload.

(DONE 8 Oct, see PROGRESS) ISSUE 1: THE INTRO DOES NOT ARRIVE AT THE END FRAME (S7-INTRO_3walls_v5_INTO_DAY_IDLE.mp4, Homie's screenshots at 0:10 and 0:18).
  What happens: the camera climbs the side near the STERN (0:10, the stern gallery beside it) and comes aboard near the
  stern on the starboard side; then (about 0:16-0:19) the picture CROSS-MORPHS into the deck plate: a double exposure
  (the starboard rail and gun in the foreground ghosted over the centred deck view). The camera never travels to the
  plate's position. Seedance's end_image pin is doing a MORPH, not a camera move (as BOARD v1's hard cut: the same failure
  in a softer form). Claude's ECC check on the last frame (0.994) passed because only the LAST frame was checked.
  Homie: "the camera needs to go to the front and seamlessly align with the end frame. Needs to be done again."
  FIX PLAN (rec): put the boarding WHERE THE PLATE'S CAMERA IS, so the end is a short real move, not a long trip:
   - The plate camera stands on the centreline just aft of the mast in the canvas, looking forward to the bow. Write the
     geography explicitly: the camera overtakes along the starboard side PAST the stern and quarterdeck to amidships,
     rises over the rail there (beside the mast in the plate), moves IN to the centreline and turns to face the bow,
     settling into the last frame. Give it time: board by ~11 s, centreline move + turn 11-17 s, settle 17-20 s.
   - Or split: A = flight + climb + over the rail amidships (no end_image), B = Sequel/omni from A's last frame with
     end_image = canvas, 6-8 s, ONLY "steps in to the centreline and turns to face forward" (a small move the model can
     really make). Probe B at 480p first.
   - CHECK EVERY FRAME OF THE LAST 4 s, not just the last: (a) ghosting = the frame is a blend of two views (edges doubled;
     test: a frame f ~= a*f_prev_view + b*canvas with both a,b >0.2, or two peaks in the phase-correlation surface); (b) the
     affine to the canvas must CONVERGE smoothly (scale/translation changing every frame), never jump while the image
     cross-fades. Look at a contact sheet of every 6th frame of the last 4 s at full size before calling it a pass.
  Credits: the CLI account ("Private") had 1,250 on 8 Oct. A 480p draft 20 s = 60, 8 s = 24; 1080p 8 s = 96, 20 s = 240.

(DONE 8 Oct, see PROGRESS) ISSUE 2: IN THE IDLES THE SHIP'S FRONT MOVES SEPARATELY FROM THE SHIP (6_review/S7-SHIP_idle_arc_preview_v1.mp4).
  Cause (tools/s7_idle.py): the WORLD layer (the whole clip frame) is rolled/heaved and shown through the still's bgmask;
  wherever the mask's sea/sky touches the ship (the far bow/forecastle near the horizon, the bowsprit, rope edges) or the
  clip's own ship sits slightly differently from the still, SHIP PIXELS FROM THE CLIP get rolled with the sea: the bow
  appears to move/distort separately.
  FIX PLAN: (1) the world layer must contain NO ship: erode the bgmask ~6 px (dilate the ship) and FILL the ship holes in
  the clip frame from the surrounding sea/sky (normalised-convolution fill, horizontal) BEFORE rolling; then lay the
  still ship over it. (2) Open 5_layers/seamed_v2/<state>/*_check.jpg and the masks at the far bow at 4x: the forecastle,
  bowsprit and the far rail must be SHIP (0) in the mask; fix the mask by hand/script if not. (3) Verify: difference of
  consecutive frames INSIDE the ship mask must be ~0 (only the 0.6 px vibration) everywhere incl. the bow; make a 4x crop
  of the bow over the loop. Also consider the roll pivot at the horizon point behind the bow (so the bow area moves least).
  Rebuild all 4 idles + the arc preview with the SAME motion settings.

PROGRESS 8 OCT (MacBook, CLI; MODE VID; Homie present):
- ISSUE 2 FIXED BY SCRIPT (0 cr). Cause confirmed on the pixels: (a) the old bgmasks marked SHIP as sea/sky at the bow (the
  forecastle gun's barrel, holes in the furled sail, blocks, rope edges) so those pixels showed the rolling world; (b) the
  rolled world was the whole clip frame, so the clip's own yard + gun rolled into view (v1 day at 4 s: the forecastle gun
  DOUBLED, the yard ghosted). Fix: NEW tools/s7_worldfill.py -> 5_layers/seamed_v2/<state>/*_bgmask_v2.png (+ _v2check.jpg;
  old masks kept): ship found by colour vs a smooth sea/sky model near the ship, a straight fitted horizon never frozen, sea
  specks dropped, ship grown 2 px. tools/s7_idle.py v2: the clip's ship (grown 5 px) is FILLED before the roll (sea copied
  sideways from open water in the same row = same haze; else mirrored from above; sky push-pull from sky only), and the
  registration border mirrors (v1 smeared LEFT's outer edge into streaks). Motion settings unchanged (roll 0.6 / heave 8 /
  shake 0.6, same phases, 157 f). VERIFIED (day, no-shake test): ship core range max 6 levels = codec noise, 0 px moving;
  4x bow crops clean in every 20th frame. v1 idles moved to 04_WORKING_FILES/superseded/S7_ship_idle_v1_2026-10-08/.
  Rebuilt: 8_idle/<state>/ + 6_review/S7-SHIP_idle_arc_preview_v2.mp4 + S7-SHIP_idle_BOW_v1_vs_v2_day.mp4 (side by side).
- ISSUE 1 DONE = INTRO v6 (315 cr): REV probe 24 + final 96; LEADIN draft 39 + final 156. The boarding generated
  BACKWARDS from the day canvas (prompts/S7-INTRO-REV.txt) and played reversed; the flight = a BACKWARD video_extension
  of that reversed clip (prompts/S7-INTRO-LEADIN.txt, + F1 astern as an image reference), so the join is the model's own
  continuation inside a full-frame planking close-up (1080p: join step 2.7 px between 2.9-3.4 and 3.3 px/frame steps).
  3-wall build: s7_intro_3walls.py --constant (one correction on every frame = Seedance's fixed 2.2% zoom). Checked:
  every 6th frame of the last 4 s at full size = single sharp images, no double exposure; ECC to the walls 0.83 -> 0.993
  over the last second. (A blend-regression ghost test was tried and was BLIND to v5's known morph: don't trust it; look.)
  CLI: `--draft false` is required with `--draft_job_id`. Original plan notes:
- ISSUE 1 PLAN (Claude's pick, invented, UNTESTED at the time): generate the boarding BACKWARDS from the day canvas (start pins are
  exact, end pins cut/morph: BOARD v1 + v5) and play it reversed, so the intro ENDS pixel-exact with a real move.
  prompts/S7-INTRO-REV.txt v1 (480p 8 s probe = 24 cr; canvas uploaded on the new account: media de76e4f6-025f-4f2c-
  8b37-2950f1f01383). The flight joins its reversed first frame afterwards (backward video_extension, or a flight ending
  close on the bulwark). v5's own rail crossing has no full-frame occluder (checked 24 fps): it can't be the join as is.

LATEST (7 Oct, evening; Claude switched to a 2nd account; Higgsfield connector NOT connected on it; HF balance ~99 cr per
Homie, who can connect another HF account with credits):
DONE, ALL FOR HOMIE'S REVIEW (T9 04_WORKING_FILES/S7_ship/):
- INTRO v5 (route A, one 21:9 take, no hard cut, gull flies off, lands on OUR deck): 4_intro_video/routeA_21x9/
  S7-INTRO_3walls_v5_INTO_DAY_IDLE.mp4 (the intro across the 3 walls dissolving into the day idle) + S7-INTRO_3walls_v5.mp4.
- IDLE LOOPS x4: 8_idle/<day|magic|sunset|night>/ (3walls_LOOP.mp4 review + LEFT/CENTRE/RIGHT ProRes). Deck still, the
  horizon rolls/heaves behind it (identical in all 4 states, so a crossfade between skies never jumps).
- FIXES: night CENTRE ropes (ship_ropefix.py); SUNSET one sky across the walls (ship_skyharmony.py; the "dark smoke").
- LOG + REGISTER rows written (7 Oct route A).
OPEN / NEXT:
1. Homie's verdicts: intro v5 (stern windows' yellow trim; a quarterdeck rail flashes past), the 4 idles, the sunset sky.
2. A light-arc preview built from the IDLES (day -> magic -> sunset -> night crossfades) replacing SEAMED_v3.
3. 4K: upscale_video (ByteDance aigc 4k, ~1 cr each) on the 4 idle clips + the intro BEFORE the band crop (needs the HF
   connector), then rerun s7_idle.py / s7_intro_3walls.py on the 4K clips.
4. Destruction (the wreck state): script first (mast fall, list, shudder) on the wreck walls. (Wreck CENTRE ropes FIXED.)
   Review: 6_review/S7-SHIP_idle_arc_preview_v1.mp4 (day->magic->sunset->night from the idles, same-phase crossfades).
5. Watch: a thin bright horizon line on LEFT near the sunset loop point (natural glint, kept).

HANDOVER, 7 OCT DAY (Homie present; MODE = VID; Claude's weekly limit at 95%, so another account may continue from here).
THE TASK: THE SHIP INTRO, ROUTE A (Homie's pick): ONE seamless picture across all THREE walls, ending on the deck with the
gull landed, NO hard cuts. Be efficient: Homie is short of time.
- Homie on the overnight work: the FLIGHT v3 (redo_v2/S7-INTRO-FLIGHT_v3_24ba0a6b.mp4, 16:9) "looks good", BUT "it has to be a
  seamless thing across all 3 screens". It played on CENTRE only. Route A = regenerate at 21:9 and lay the MIDDLE 4.33:1 band
  (54% of the frame height, centred) across LEFT+CENTRE+RIGHT (4680x1080; 4K 9360x2160 after upscale).
- ONE 20 s take (flight -> up the starboard side -> over the rail -> the camera settles looking forward along the deck, mast
  centred -> the gull LANDS on the rail at the right). No Sequel join and no end_image (BOARD v1: end_image forced a hard cut
  at 2.75 s). The end goes onto the deck walls (3_walls/seamed_v2/day) by a ~1 s script dissolve.
- PROMPT: prompts/S7-INTRO-FLIGHT.txt v4 (top of file: settings, GATE, prediction). Start frame = T9
  S7_ship/4_intro_video/routeA_21x9/S7-INTRO-F1-ASTERN_21x9.png (F1-ASTERN haze cropped 2752x1180 at y=100), uploaded as
  media 83eb6345-979a-40f0-a152-d51e36de2066 (role start_image).
- SUBMITTED 7 Oct: the 480p draft = job 615146e9-3685-4eaa-bf6a-95bbb0211db7 (60 cr; preset 3D RENDER declined). Check it
  first (jobs_wait / job_display) before submitting anything new.
- DRAFT RESULT (7 Oct): routeA_21x9/S7-INTRO-FLIGHT_v4draft480_615146e9.mp4 (992x432, 20 s) + 3-wall preview
  S7-INTRO_3walls_PREVIEW_v4draft.mp4 (tools/s7_intro_3walls.sh). NO hard cut (largest frame diff = the rail crossing, spread
  over f327-335 = motion). Flaps, comes close, up the side, aboard, the gull lands on the rail. Faults: gold trim on the stern
  windows; the generated deck is a diagonal view with sails set, NOT our walls' straight-ahead deck, so the end is a 1 s
  DISSOLVE onto the walls, not a match. Homie (7 Oct): "the bird can just fly away and we land at the end frame… whatever
  makes it easy". Awaiting Homie: finalize this draft (job 615146e9 via draft_job_id, ~240 cr) or re-roll.
- PLAN AGREED WITH HOMIE (7 Oct): "use all the credits… it is now or never… we need precision". (1) DECK CANVAS per sky
  state (day/magic/sunset/night) = our walls in the centred band of a 21:9 frame (tools/ship_canvas21.py; T9 S7_ship/7_canvas21/,
  prompt prompts/S7-SHIP-CANVAS21.txt, 2 cr each): DONE day/magic/sunset, night running. (2) INTRO v5: end_image = the day
  canvas, the gull flies away at 8-10 s, the camera alone settles into our deck (prompts/S7-INTRO-FLIGHT.txt v5, draft job
  69161783-c0a7-4d33-a2df-cfffd53bc276). If it cuts hard: v4 + dissolve. Then finalize 1080p (~240). (3) IDLE LOOPS per
  state: 10 s locked camera from each canvas (start_image), sea+sky alive as ONE picture across the 3 walls, the ship laid
  back on from the approved stills via 5_layers masks, crossfade loop (720p = 70 each). (4) destruction later.
- STATUS AT HANDOVER (7 Oct, Claude's weekly limit hit; Higgsfield balance ~663; Homie: "use all the credits… now or
  never… precision"):
  * DECK CANVASES DONE (8 cr): T9 S7_ship/7_canvas21/S7-SHIP-CANVAS21_{day,magic,sunset,night}.png (+ _upload.png 2480x1080,
    _check.jpg). Band = our seamed_v2 walls exactly (registration residual ~1-1.4 px). Night: NBP added a 2nd moon in the
    (never projected) top strip, painted out by script (a faint glow remains there, harmless).
  * INTRO v5 DRAFT PASSES (60 cr): routeA_21x9/S7-INTRO-FLIGHT_v5draft480_69161783.mp4. No hard cut (biggest frame diff
    f322-326 = motion blur over the rail). The gull flies off, the camera climbs alone, settles on OUR deck: last frame vs
    day canvas ECC 0.998, affine scale 0.977 (2.3% zoomed) + (-4.9, -3.1) px at 480p. To review: yellow trim on the stern
    windows (could be painted ochre, period-plausible; Homie to judge), a turned quarterdeck rail flashes past.
  * NEXT, IN THIS ORDER: (a) build its 3-wall preview: tools/s7_intro_3walls.sh, BUT add an end alignment: over the last
    ~2 s ramp the inverse of that affine so the last frame lands pixel-exact on the canvas band, then a 0.5 s dissolve into
    the seamed_v2/day walls; show Homie. (b) FINALIZE v5 at 1080p: generate_video with draft_job_id
    69161783-c0a7-4d33-a2df-cfffd53bc276, same params as the v5 header (preflight 240 cr). Re-measure the end affine at 1080p.
    (c) IDLE LOOPS: prompts/S7-SHIP-IDLE.txt (written, not run), 1080p 8 s = 96 cr each x 4 = 384. Day first, check, then
    the rest. (d) destruction later with whatever is left (~40 cr after a+b+c: script-first).
  * RUNNING / DONE AFTER THE FIRST HANDOVER: v5 FINALIZE 1080p submitted = job 6e515e2d-7021-41a7-b733-eb8c1a490abc (240 cr,
    one debit checked). DAY IDLE submitted = job fcb5117d-6c6b-4038-af46-3dc86430933d (96 cr; preset IN THE DARK declined).
    Canvas uploads for the idles: magic be2d4524-8d34-4bd9-9a91-5ef11e719228 · sunset 5494e0d8-83d7-4234-9698-b3b061d56e74 ·
    night 2a518de2-e311-4a5b-bd6d-4e449b80abf7. NEW tools/s7_intro_3walls.py (end alignment + dissolve + sound): the v5
    DRAFT preview = routeA_21x9/S7-INTRO_3walls_PREVIEW_v5draft.mp4 (lands on the walls, MAD 12.8 at the join = 480p softness).
    When the 1080p final lands: download to routeA_21x9/S7-INTRO-FLIGHT_v5_6e515e2d.mp4 and rerun s7_intro_3walls.py on it.
  * UPDATE 2 (7 Oct, later): INTRO v5 FINAL 1080p DOWNLOADED: routeA_21x9/S7-INTRO-FLIGHT_v5_6e515e2d.mp4 (2206x946!
    Seedance 1080p 21:9 = 2.332, the draft 992x432 = 2.296: both tools now crop the CANVAS's band rows 479..1559/2038 and
    resize, so any size lands right). NEXT: run tools/s7_intro_3walls.py on it -> S7-INTRO_3walls_v5.mp4, show Homie.
    DAY IDLE DONE: 8_idle/S7-SHIP-IDLE_day_v1_fcb5117d.mp4 -> tools/s7_idle.py -> 8_idle/day/ (3walls_LOOP.mp4 review +
    LEFT/CENTRE/RIGHT ProRes; loop 6.54 s, xfade 1.5 s, ECC 0.995, drift 0.4 px). SHIP MOTION (Homie: "we are on the ship…
    cannot be super stable… the water horizon might move"): camera fixed to the ship = DECK STILL, the SEA+SKY roll 0.6 deg
    and heave 8 px behind it (canvas space, periodic over the loop), + 0.6 px vibration on the whole frame (--roll/--heave/
    --shake). MAGIC idle submitted next; then sunset, night (96 each; preset IN THE DARK declined each time).
    LATER: the same horizon motion on the intro's held end (ramp it in) so intro -> idle has no jump.
  * UPDATE 3: INTRO 3-WALL v5 BUILT = routeA_21x9/S7-INTRO_3walls_v5.mp4 (from the 1080p final; last frame -> canvas ECC
    0.994, eased in over the last 2.5 s; 0.5 s dissolve into the walls; MAD 11.6 at the join). Idles submitted: magic
    49c15d8f-db80-4cd5-9979-2c1950fafe86, sunset 15bb1b83-8524-41d0-8eb7-4bc450e58ebc, night 7e5a0433-7479-43f5-ae45-4bd3368be146
    (96 each, debits checked). Balance after night ~39. For each: download to 8_idle/S7-SHIP-IDLE_<state>_v1_<id>.mp4, look at
    3 frames, then: PYTHONPATH=<scratch>/py python3 tools/s7_idle.py CLIP <state> 8_idle/<state>.
  * UPDATE 4 (account switched; the Higgsfield CONNECTOR IS NOT CONNECTED on this Claude account): the 3 idle takes were
    fetched by URL pattern hf_<YYYYMMDD>_<HHMMSS of submission>_<jobid>.mp4 on d8j0ntlcm91z4.cloudfront.net/user_3HbkTR9l…
    (magic 003131, sunset 003247, night 003304; probe with curl -I --resolve). All 4 idles = 2206x946, 193 frames -> every
    loop 157 frames (6.54 s) with the SAME motion (Homie: "camera movements… consistent across all variations"): s7_idle.py
    defaults roll 0.6 / heave 8 / shake 0.6, same phases, period = loop length. Intro -> idle in one file:
    routeA_21x9/S7-INTRO_3walls_v5_INTO_DAY_IDLE.mp4 (s7_intro_3walls.py --then). Homie: HF balance shows 99 cr; he can
    connect another HF account with credits if needed.
  * Credits this session so far: v4 draft 60 + canvases 8 + v5 draft 60 = 128 (balance 791.49 -> ~663.49).
- NIGHT CENTRE ROPES FIXED (tools/ship_ropefix.py, K=34): installed in seamed_v2/night, old in
  04_WORKING_FILES/superseded/S7_ship_ropes_zigzag_2026-10-07/. Magic and sunset had no zig-zag. Arc preview NOT yet rebuilt.
- Bird across seams (Homie asked): OK if brief/fast; a big slow wing held across a seam breaks (25 deg fold + 830 mm gap):
  the gull stays in the middle (CENTRE) when close.
- STEPS: (1) 480p draft (draft: true, ~60 cr, get_cost first) -> download to routeA_21x9/ (tools/fetch.py) -> check: no cut
  (frame-diff spikes), flapping, aboard, gull on rail, band holds gull + ship; (2) if it passes, finalize 1080p via
  draft_job_id (~240 cr); (3) build the 3-wall cut by script: scale the 21:9 to 4680 wide, crop the centred 4.33:1 band,
  split 1440|1800|1440, dissolve the last ~1 s into seamed_v2/day walls, carry the sound (build_audio rule); show Homie.
  If it fails twice on the same defect: stop, report. Then LOG/REGISTER rows + commit.
- CREDITS: balance ~851 after the overnight VID (228 spent: FLIGHT v3 draft 36 + final 144, BOARD v1 draft 24, BOARD v2
  draft 24 = submitted, never downloaded, superseded by route A). Keep 500 at the week's end.
- PARKED (0 cr, script, Homie asked "can it be fixed?"): the ROPES ZIG-ZAG at the very top of CENTRE in the non-day states
  (magic/sunset/night; check wreck). Cause: tools/ship_align.py filled CENTRE's missing top strip (~40 px) with the take
  MIRRORED, folding the shrouds into a V. Fix: rebuild that strip from the DAY wall's straight rigging, recoloured per state;
  old CENTRE files to superseded/; rebuild the SEAMED arc preview. Day CENTRE is clean.
- Homie finds the T9 folders hard to navigate: when showing files, `open -R` the exact file and say which 1-2 to watch.

MORNING REVIEW, 7 OCT (Homie: watch these; T9 = /Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/):
1. THE SEAMS, REBUILT: 6_review/S7-SHIP_light_arc_preview_SEAMED_v3.mp4 (+ S7-SHIP_all_states_contact_SEAMED_v3.jpg).
   The side walls now continue the deck master (same rail line, gun scale, planks, light at both seams). Walls per state:
   3_walls/seamed_v2/<day|magic|sunset|night|wreck>/. Rec: approve; they replace seamed_v1.
   Known: CENTRE's own top shrouds kink (a reflected strip from the 6 Oct alignment, in the approved CENTRE files); SUNSET's
   side glow toward CENTRE was tamed by script (tools/ship_skymatch.py).
2. THE INTRO START FRAME: 2_intro/S7-INTRO-F1-ASTERN_v1_34a41ccb_haze.png (from astern, gull mid-wingbeat, white ensign).
3. THE INTRO REDO (VID sub-agent, cap 450 cr): was STILL RUNNING when the session hit its limit. Its files:
   4_intro_video/redo_v2/ (review cut S7-INTRO_review_v2.mp4 if it got that far). NOT YET VERIFIED by Claude, NOT logged,
   its prompts (S7-INTRO-FLIGHT.txt / S7-INTRO-BOARD.txt) committed as a mid-run snapshot: re-check them. Next session: check `transactions`
   (spend since 1,079.49), probe + contact-sheet its files, last frame vs the ENDFRAME, then LOG/REGISTER + commit.
Credits: IMG 48 (balance 1,079.49 before VID). Keep 500 at week's end.

PROGRESS, NIGHT OF 7 OCT (Claude, Homie asleep, delegated; every pick PROVISIONAL):
- JOB 1 DONE (44 cr): the side walls are BUILT OUT FROM THE MASTER (tools/ship_buildout.py): v1 grey canvas FAILED (NBP
  mirrored the strip into a V); v2 = a geometric guide (the master's own perspective) PASSED: rail, bulwark, gun scale, planks
  and light continue across both seams (seam step = the master's own). States re-made on the new sides (magic, sunset, night;
  wreck = day sides), seams colour-matched (ship_seams.py --colour-only + new tools/ship_skymatch.py; SUNSET's side glare
  at the inner edge failed twice in prompts -> tamed by script). NEW CURRENT WALLS = T9 S7_ship/3_walls/seamed_v2/<state>/,
  layers 5_layers/seamed_v2/, review: 6_review/S7-SHIP_light_arc_preview_SEAMED_v3.mp4 + _all_states_contact_SEAMED_v3.jpg.
- JOB 2 DONE (4 cr): new first frame S7-INTRO-F1-ASTERN take 34a41ccb (from astern-quarter, stern windows + wake toward
  camera, red-ochre band, no gilding, gull at the top of a wingbeat); its Union-Jack-like ensign painted plain white by script;
  hazed: T9 S7_ship/2_intro/S7-INTRO-F1-ASTERN_v1_34a41ccb_haze.png (aerial_haze.py --ship-km 1.5 + a colour-keyed gull mask,
  new --subject-mask option). IMG total 48 cr, balance 1,079.49.
- SESSION 2 (VID): a fresh sub-agent runs the intro redo (cap 450). Unfinished at wrap: see MORNING REVIEW 3.

THE TASK, RIGHT NOW (7 Oct, MacBook): TWO SESSIONS, IN THIS ORDER. Ship sequence (Sc 7-8). Read docs/PLAN-SHIP-INTRO.md.

SESSION 1 = IMG (this one). Load house-rules (+ references/findings-image.md) and scenecraft-v1. MODE = IMG.
  JOB 1: THE SEAMS, PROPERLY. Homie (7 Oct, on 6_review/S7-SHIP_light_arc_preview_SEAMED_v2.mp4): "the seams are still not
  fully aligned… you can tell the ship's edges are a bit off." He is right. tools/ship_seams.py (6 Oct) made the rail HEIGHTS
  and the sky/sea COLOUR meet, but a script can't fix what is left, because LEFT and RIGHT are separate generations, not
  continuations of CENTRE. Seen at the seams of 3_walls/seamed_v1/day (Claude, 7 Oct):
    1. SCALE: the side walls' guns and bulwark planks are ~1.3x bigger than CENTRE's at the seam (closer camera).
    2. RAIL ANGLE: the heights meet but the rail kinks into a V at each seam.
    3. DOUBLES: a gun on both sides of each seam; the deck planks run different ways.
    4. LIGHT: RIGHT's deck is bright sun where CENTRE's edge is shade; the rail caps differ in tone.
  ROUTE TO TRY (untested, probe first, ~4 cr): build each side wall OUTWARD FROM THE MASTER. The 21:9 deck master
  (1_deck_master/S7-SHIP-ROOM_v2_f5180ed8.png, 3168x1344) holds ~464 px of TRUE continuation beyond the CENTRE crop on each
  side. Make a 4:3 canvas per side with that strip at its INNER edge (the edge that meets CENTRE), the rest flat neutral grey,
  and run an NBP edit (scenecraft Plate D): "fill the grey area, continuing the deck, bulwark, guns, rigging, sea and sky
  of the strip outward; keep the strip exactly". Then crop/scale so the strip lands pixel for pixel next to CENTRE.
  (5 Oct's failures, LOG: outpaint_image ignored the size and re-centred; side walls generated from a reference re-showed
  the bow. This route differs: the real pixels sit IN the canvas at the seam.) PASS = at both seams the rail cap, bulwark
  height, gun size, plank direction and light continue; no object cut by a seam. Two failed versions = stop, report to Homie.
  If it passes: re-make the side walls' light states (magic, sunset, night) as the same proven NBP edits, then
  ship_states.py / ship_seams.py (colour only) / ship_layers.py, and a new 6_review arc preview for Homie.
  JOB 2: a NEW FIRST FRAME for the intro redo (docs/VID-BRIEF-S7-INTRO-v2.md): the Medusa from ASTERN/quarter, sailing away,
  small, OUR red-ochre ship (no gilding, white ensign), a herring gull mid-wingbeat (wings UP or DOWN, not a flat glide),
  hazed by tools/aerial_haze.py like F1.

SESSION 2 = VID (fresh chat). Load house-rules (+ findings-video.md) and shotcaller-v1. MODE = VID. Do
  docs/VID-BRIEF-S7-INTRO-v2.md: the intro REDO from Job 2's frame, ending ON the deck plate
  (4_intro_video/endframe/S7-SHIP-C_day_16x9_ENDFRAME.png; Seedance end_image untested). Then the sea loops as ONE sea.

STATE: Homie APPROVED the five light states and their timing (day, magic hour in Louise's sky, sunset, night, wreck); the
intro v1 is REJECTED. Current walls = T9 S7_ship/3_walls/seamed_v1/ until Job 1 replaces their sides. CENTRE is final in
every state (it is never re-made: only LEFT and RIGHT change).
Credits: balance 1,127.49. Job 1 + 2 ~60 cr; intro redo cap 450; keep 500 at the end of the week. One job at a time,
get_cost first, transactions after. Media: the T9 mounts at /Volumes/DMD T9 (SOTR/HF/SOTR_MEDIA). Python deps:
pip install --target <scratchpad>/py numpy pillow opencv-python-headless, then PYTHONPATH=<scratchpad>/py.

HISTORY (6 Oct morning and night, superseded by the block above):
(was THE TASK, 6 Oct morning, IMG): THE SHIP SEQUENCE (Sc 7-8), a side quest APPROVED by Homie: "make
the calls and go ahead". READ docs/PLAN-SHIP-INTRO.md FIRST (sources, Sahaj's notes decoded, designed-for-destruction,
Sahaj's angle, credits). Higgsfield credits EXPIRE 6 Oct: spend them today, one job at a time, no waste.
STATE (updated as work goes): v1 rejected (two masts). v2 DONE: 4 takes in T9 04_WORKING_FILES/S7_ship/1_deck_master/;
CHOSEN (Claude) = S7-SHIP-ROOM_v2_f5180ed8 (one foremast, bow closest, both sides big). INTRO-F1 v1 DONE: 3 takes in 2_intro/
(the 4th, 66ad98e8, was still rendering); CHOSEN = S7-INTRO-F1_v1_1714a32e (the Medusa dead centre on the horizon). The gull
CHECKED = goeland argente (Larus argentatus), the lead species of Homie's link: every field mark right (Homie: "imperative").
Homie's notes 5 Oct: VOLUMETRIC HAZE in the distance, real physics, the ship NOT so clear from beside the bird, DOF; IN POST
(credits precious): tools/aerial_haze.py (Koschmieder haze by true sea distance + thin-lens DOF, gull kept sharp), applied to
the START FRAME before the video. Sahaj's angle seen (Desktop/VID-20261005-WA0016.mp4): ONE continuous camera across the
three walls -> walls are CUT FROM ONE PLATE (tools/ship_walls.py), outpaint sideways to keep the full height.
Night-shift auto-resume: blocked by the safety check; Homie restarts the session himself from THIS file.
DONE since: haze/DOF on F1 (2_intro/S7-INTRO-F1_v1_1714a32e_haze.png). THE THREE WALLS ARE ASSEMBLED (v1, 0 cr):
T9 04_WORKING_FILES/S7_ship/3_walls/assembled_v1/ (LEFT 260b6359 + CENTRE from master f5180ed8 + RIGHT 972c8b09, one horizon;
tools/ship_assemble.py --hz-c 0.387). One-plate cutting + outpaint FAILED (LOG). AWAITING HOMIE'S LOOK CHECK (Claude decides if away).
DONE 5 Oct night: SUNSET state of all three walls, chosen + assembled on one horizon: 3_walls/assembled_sunset_v1/
(C b3696a61, L 17bd1936, R 68744df0; real-size sun after one patch). NIGHT prompts WRITTEN, NOT RUN: prompts/S7-SHIP-{C,L,R}-NIGHT.txt
(same edit layout, only the Change line; inputs C media f51d98e7, L f2172e8e, R d81781ae; 2 takes each = 12 cr).
NEXT (IMG): 1) show Homie assembled_v1 (day) + assembled_sunset_v1; 2) run NIGHT, then MAGIC HOUR (patch the Change line);
3) the WRECK on CENTRE (foremast snapped and fallen forward over the bow, rigging slack, water on deck): an edit of the day
CENTRE; 4) layers (tools/ship_layers.py). Then a VID session: the intro flight from 2_intro/S7-INTRO-F1_v1_1714a32e_haze.png
(4 s probe first), sea loops per light, the mast falling, the rowboats + snap. Then 4K of what Homie approves.
LOUISE'S REFERENCE IMAGES (Homie, 5 Oct night): 4 images pasted in chat were TOO BIG to read (>2000 px). Ask Homie for their
file path; read them downscaled (ffmpeg -vf scale=1600:-1) before more look work.
THEN VID (fresh session, house-rules VID + shotcaller-v1): intro flight from the HAZED F1 (4 s probe, then ~15 s + a landing
Sequel), sea loops per light, the foremast falls forward, the rowboats + snap. Then 4K of what's approved.
Credits spent 5 Oct ship session: 60 (NBP 56, outpaint 4). Balance ~1,577.
OVERNIGHT 6 Oct (Claude, Homie asleep, delegated: "finish everything we agreed"; every pick below is PROVISIONAL, for his review):
- LOUISE'S IMAGES READ (~/Downloads/IMG-20261005-WA0019/20/22.jpg + the WhatsApp screenshot): "the sky over the Charente River on my
  last night in France. This is where the Méduse set sail from." Lavender-blue twilight, rose cirrus, a near-full moon. USED AS THE
  MAGIC HOUR SKY, and the NIGHT moon became the same FULL moon (was a crescent) so the evening has one moon.
- ALL FOUR LIGHT STATES DONE, on ONE geometry (T9 S7_ship/3_walls/): assembled_v1 (DAY), assembled_magic_v1, assembled_sunset_v2,
  assembled_night_v2. NEW tools/ship_align.py + ship_states.py warp every state onto the day walls (<1 px): NBP had reframed the
  CENTRE edits by up to 16%, which a light crossfade would show as a jump. Old unaligned sets kept (sunset_v1, night_v1).
- LAYERS: 5_layers/day/ (ship RGBA + sea/sky mask per wall; states reuse the day masks).
- WRECK on CENTRE DONE: v2 take 40936720 (splintered stump, the yard fallen across the deck, wet deck), 3_walls/assembled_wreck_v1/
  + 5_layers/wreck_v1/. v1 kept a standing pole at the bow; v2 fixed it with one sentence (LOG).
- IMG LIST DONE (night, magic hour, wreck, layers). 36 cr (18 NBP takes; balance 1,541.49). NOW: the VID sub-agent, docs/VID-BRIEF-S7-INTRO.md (cap 600 cr).
  Details: LOG.md 2026-10-06 rows. CHECK if the credits really expire today (6 Oct) and when. Mac kept awake by caffeinate.
- VID (night 6 Oct) DONE, 414 cr of 600 (balance 1,127.49), all PROVISIONAL for Homie: REVIEW CUT = T9 S7_ship/4_intro_video/
  S7-INTRO_review_v1.mp4 (22.4 s, 1800x1080, sound) + S7-INTRO_review_v1_3walls_4680.mp4 (cut to the DAY deck walls). FLIGHT v2
  (b37921bd, 1080p): smooth follow, the ship grows, the gull meets her HEAD-ON (the model drew her bow, not her stern); its
  Union-Jack-like masthead flag painted WHITE by script (_flagwhite.mov); trimmed at f346 (an end rush). LANDING v2 Sequel
  (4140a014): over the bow rail, lands, stands 3 s (deck matches our walls), rises, wing over the lens. CHECKED BY THE PARENT SESSION: the deck only PARTLY matches our walls (red bulwarks, guns,
  rope coils, but a turned BALUSTRADE rail and a dark banded mast; the flight's hull is dark with GILDED bands vs our red-ochre):
  the dissolve onto the deck walls lands on a different-looking ship. Homie to judge: head-on
  vs astern; the ship's gilded 18th-c. bow; the quick last-2-frame wing wipe (v1 draft 4ff856e8 has a slower one, ruffled wings).

PREVIOUS (5 Oct, latest): SCENES 1+10 DONE AND IN 01_FINAL_FOR_SHOW. 01 IS THE COMPLETE CLIENT UPLOAD (S1, S4, S5, S6, S9, S10).
Ask Homie which is next; recommend 1 (it's the next production job), and 2 when the PC is next on.
1. IMG — THE SURPRISE SCENE (Scene 8), parked behind the gallery. Start from BIBLE.md / the script PDF; LOOK first, nothing
   invented (look decisions go to Homie with a recommendation).
2. ON THE PC: run tools/reorg_2026-10-05.py D:/SOTR run (Scenes 4/5), copy S1 (the whole 04_WORKING_FILES/S1_gallery +
   02_APPROVED_BUILDING_BLOCKS/S1_gallery + the gallery files now in 01_FINAL_FOR_SHOW) from the T9 to D: (sha256: the T9's
   SHA256SUMS_2026-10-05_gallery.txt), superseded/S1_gallery too.
DONE 5 Oct: gallery walls re-hung centred (LIT/DARK v3), 1080 full-length show files + 4K loops, the floor files with the
puddle FLOW (Homie: "fine"), promoted by tools/promote_gallery_2026-10-05.py (log: T9/SOTR/HF/PROMOTE_GALLERY_2026-10-05_moves.tsv),
client readme + SOTR_MEDIA/README.txt updated. Homie's open question answered: the dark files never go to full black (the
operator's fade does that before Scene 2).
STATE: all S1 media on the T9 (master), REORGANISED 5 Oct (REGISTER 'HANDOVER REORG'): 04_WORKING_FILES/S1_gallery/
(00_STATUS_READ_ME.txt, 1_READY_for_show_build/, 2_PUDDLE_RETURN_in_progress/ = new takes go here),
02_APPROVED_BUILDING_BLOCKS/S1_gallery/. Scenes 4 + 5 are now IN 01_FINAL_FOR_SHOW. ON THE PC: run
tools/reorg_2026-10-05.py D:/SOTR run (Scenes 4/5), then copy S1 from the T9 to D: (sha256). Credits: 222 spent
5 Oct (VID + POST), balance ~1,637. CREDITS (Homie): keep enough for ALL the gallery's video generations AND upscales, and LEAVE
500 AT THE END OF THE WEEK. Mac: pip --target <scratch>/py numpy pillow opencv-python-headless
(+ pypdf to read the script PDF: ~/Documents/SOTR/2026 RMIT Dev 'Secret of the Raft' Workhop Draft V1.pdf); the T9 mounts at
/Volumes/DMD T9 (media under SOTR/HF/SOTR_MEDIA).
The surprise scene (Scene 8, IMG) is parked behind these.

WHERE IT LIVES (D:\SOTR\SOTR_MEDIA = C:\Users\Homie\Documents\SOTR_MEDIA, a junction; README.txt is the map):
- 01_FINAL_FOR_SHOW/  the client delivery (00_READ_ME_FIRST.txt explains it): S6_<WALL>_wars.mov and
  S9_b<beat>_<WALL>_<world>.mov, sorted = script order; 2_BACKUP_LOOPS_for_operator/ (salon IN/HOLD/OUT, court single
  strikes, studio HOLD loops); 3_HD_1080_fallback/.
- 02_APPROVED_BUILDING_BLOCKS/ generated sources · 03_CLEAN_MASTERS_no_edge/ the _CLEAN masters ·
  04_WORKING_FILES/ edge kits, recipes, 4K records, superseded/.
- No versions in show names; REGISTER.md's "SHOW FOLDER" table maps each to its version.
  A new version keeps the SAME show name; the old file goes to 04_WORKING_FILES/superseded/.
- Meeting docs: SOTR_MEDIA/06_PRESENTATIONS/ (one-pager PDF), docs/MEETING-ONE-PAGER-2026-09-26.html.
- Salon RIGHT, court CENTRE, studio LEFT (client, audience view, confirmed 2026-09-22).

HOW SCENE 9 WAS BUILT (reuse for other scenes; tools/ has each script, docstrings explain):
- Generated plates + loops (Seedance 2.5 / NBP), then finished BY SCRIPT into final files:
  render_wall.py, render_studio.py (--strokes: painting in brushstrokes), render_court.py
  (--scrim --burn), build_audio.py (every file carries the clips' own sound), loop_halo.py.
- The fragment edge: each world breaks on the side facing the stage centre, the whole time,
  ONE WAY only (edge_flow.py: a generated break frozen + its blocks drifting off, never
  reversing). Materials break as they really would: rooms like stone, paper burns
  (court_burn.py), paintings and the judge never break (LOOK D15/D16).
- clean_hold.py: removes a frozen smoky hold while stream-copying every other frame.
- Final-product rule: every file plays as-is; the operator only fades in/out.

CONNECTOR RULES (full list: PIPELINE.md):
- SUBMIT ONE GENERATION AT A TIME; check `transactions` after each (parallel calls got
  double-charged). A transport error can still mean it ran: check before resubmitting.
- Preflight with get_cost (count 2 reports ONE take's price). Edit video (`video_edit`) keeps
  framing <1 px, is billed by input length, media role `video_references`.
- If the server offers the "IN THE DARK" preset, resubmit with declined_preset_id
  24bae836-2c4a-48e0-89b6-49fcc0b21612. Never run a preset.
- Only @Image 1 / @Video 1 resolve in prompts; register tags live in headers only.
- Renders take ~6-10 min; wait with a background task, not a poll loop.

WORKING WITH HOMIE:
- Claude makes technical calls; look and story go to Homie WITH a recommendation.
- Every message about generating carries the FULL settings block (model, mode, reference,
  aspect, resolution, duration, quality, batch, sound, prompt file), never "as above".
- Regenerate or script rather than push fixes into his After Effects time.
- When he praises something, build on it; don't regenerate it. When he says "only X is wrong",
  change only X and prove the rest is identical.
- Optional extras that turn hard get dropped. No brick/cube breakups on non-masonry.
- Keep answers short and plain; he asks for simple summaries.
- Rename on approval, checksum every move, never delete (superseded/ keeps history).

LESSONS THAT KEEP REPEATING (details in LOG.md):
- Calming words freeze a clip; exaggeration words blow it up. Ask for motion vividly.
- A rewrite loses what worked: patch the one failing phrase, diff before running.
- A probe proves only what it contains: probe the hardest 4 s of the real input.
- When a fix fails twice for different reasons, ask what the design makes impossible.
- Prohibition kills performance: only ban what has actually appeared.
- Verify the FILE (probe + frame samples across the whole clip), not the filename.
- Every picture tool must carry the sound through.
- Don't invent look decisions and write them into LOCKED files as if decided.

BACKUP: the T9 SSD is G:, mirroring both folders at G:\SOTR\HF\. Repo: push, then git pull in
G:\SOTR\HF\SOTR_GENpipeline. Media: copy new files, verify by sha256, COPY NEVER MIRROR-DELETE.

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW", commit, push,
back up to the T9. Report credits spent this session.
```
