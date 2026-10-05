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
