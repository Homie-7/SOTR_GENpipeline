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

THE TASK, RIGHT NOW (5 Oct, evening): TWO JOBS, ONE SESSION EACH (the mode rule). Ask Homie which first; recommend 1.
1. VID — SCENES 1+10, THE PUDDLE RETURNS, HYPER-REAL. Homie (5 Oct): "have the puddle appear as if water was dropping on it
   and then slowly, slowly building rather than just magically appearing… I want this to look hyper-real." The script:
   "The water disappears. Then it mysteriously returns, glowing." Build it as a generated clip: top-down onto the
   approved oak floor plate (04_WORKING_FILES/S1_gallery/floor/S1-GAL-FLOOR_v1_a4ea7b7a.png), locked camera: drops fall
   from above and splash, bead, join, the pool slowly spreads; then the glow rises from inside it (the painting-melt
   render's sea-teal, Final Animations/Painting melt + Ocean loop/paintingMelt_1109.mp4). shotcaller-v1 under SOTR rules;
   probe 4 s first (seedance_2_5, omni_reference, the floor plate as reference). PLACEMENT (checked 5 Oct): the floor file's
   TOP = upstage = the CENTRE wall (FLOOR-PLAN.md); the puddle sits ~1.0 m out from CENTRE, centred under the Raft
   ("mopping the floor in front of… The Raft"). The scripted floor (tools/gallery_floor.py, finished/floor_v1/) stays the
   frame for it: SPILL_HOLD / VANISH are fine; RETURN_GLOW is the cheap one to replace; the glow loops may be replaced
   by a Sequel of the generated return. Then the walls' DARK still has the puddle's teal at CENTRE's foot (gallery_dark.py).
2. IMG — THE SURPRISE SCENE: Homie (5 Oct): "See if we can surprise the client by addressing one more scene." Claude's
   recommendation: SCENE 8, "The Medusa runs aground" (unassigned; script pp.16-18): dusk at sea, the frigate grinding on
   the sandbank, the lifeboats in the distance, "the deep red light of sunset", "the light fades… beneath them, the image
   of the raft begins to emerge" (a floor moment), the ropes SNAP, "the sea washes over the raft… from blue to crimson".
   Era <= 1816. CHECK FIRST with Homie: Scene 7 (the deck of the frigate) is Sahaj's; does 8 share his deck?
STATE (5 Oct, evening): SCENES 1+10 GALLERY — Homie: "Gallery seems to be alright". All in T9 04_WORKING_FILES/S1_gallery/:
- finished/S1-GAL-<C,L,R>_LIT_v2_* (one room light, gallery_wall.py --room-light), S1-GAL_LIT_v2_SEAM_4680x1080.png;
  DARK by script (gallery_dark.py) S1-GAL-*_DARK_v1_*; floor_v1/ (floor stills + 6 ProRes clips, silent);
  S1-GAL_REVIEW_walls+floor_*.jpg. LOOK.md "Scenes 1 + 10", SHOTCARDS.md, LOG/REGISTER 5 Oct. Frames checked against
  the Louvre (Salle Mollien: gilded frames, wood floor, RED walls; ours are warm grey by the "clean modern" brief; red is a
  script-only change if Homie wants it). Nothing is in the show folder yet; not upscaled.
- The melt render is Final Animations/Painting melt + Ocean loop/paintingMelt_1109.mp4 (360, 4096x3112, 25 fps, 20 s):
  an ARCHED gilt frame (ours are rectangular), the script's blackout sits between.
- The T9 is the master for 04_WORKING_FILES/S1_gallery/ (copy to D: by hand + sha256 when back on the PC).
- Mac python: numpy/Pillow/opencv are NOT installed system-wide; install to the session scratchpad
  (`python3 -m pip install --target <scratch>/py numpy pillow opencv-python-headless`, PYTHONPATH=<scratch>/py).
  Paths with spaces ("DMD T9") break flag arrays: symlink the T9 to a no-space path in the scratchpad.
CREDITS: balance 2,143.49 (5 Oct). Homie: plenty this week but LEAVE 500 AT THE END. ONE job at a time; `transactions` after each.
ByteDance video upscale fails beyond ~15 min of processing per job (refunded): split long clips (tools/upscale_pieces.py).

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
