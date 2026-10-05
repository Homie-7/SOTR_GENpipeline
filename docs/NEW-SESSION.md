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

THE TASK, RIGHT NOW (5 Oct, latest): SCENES 1+10. THE FLOOR IS DONE (IMG, 8 cr). TWO JOBS LEFT, ONE MODE PER SESSION.
Homie: "the gallery takes precedence". Ask which; recommend 2 (the water), then 3.
1. DONE — THE NEW FLOOR: aged dark oak parquet de Versailles, take a650a2ac (Homie: "I'm happy with the floor"). His worry was the
   REFLECTIONS: the takes had the laylight's glare baked in; tools/floor_desheen.py subtracts it (--tol 0.02) ->
   04_WORKING_FILES/S1_gallery/1_READY_for_show_build/floor/S1-GAL-FLOOR_v2_a650a2ac_desheen.png = THE plate every tool
   builds from (--dry). The drawn spill on dark oak reads by its
   reflections: gallery_floor.py --wet-gain 2.5. DRY/SPILL/VANISH in 1_READY_for_show_build/floor/. VANISH v2 = --vanish dewet --vanish-s 3.5
   (Homie: v1's even shrink was "a cheap animation scaling back"; v2 frays, breaks into islands, leaves a damp ghost): APPROVED ("Yep, I like it")
   (review: finished/floor_v2/S1-GAL-FLOOR_VANISH_REVIEW_spill-vanish-dry_full+zoom.mp4). The floor is now ~1/3 of v1's brightness.
2. VID — THE PUDDLE RETURNS (S1-GAL-PUDDLE-RETURN, prompts/ file has v1-v3 + results; LOG 5 Oct). AGREED WITH HOMIE: the script
   has NO drops ("The water disappears. Then it mysteriously returns, glowing", mid-dialogue) and v2's drops read as RAIN, too
   busy for sound: so 2-3 drops, a pause, then the water WELLS UP BY ITSELF to the spill's size (~1.5 x 0.9 m), STOPS, lies still.
   THE PATCH IS READY: 05_REFERENCE_UPLOADS/S1-GAL-PUDDLE-RETURN_ref_patch_v2floor_1920x1080.png (sha 7761cdc1…) +
   patch_geom_v2floor.json (same 3.0 x 1.69 m geometry, centred x 0, 1.0 m from CENTRE; NOT yet uploaded to Higgsfield: upload it,
   the old media beb40508 is the pale oak). Seedance 2.5 References 16:9 1080p, probe 4 s (48) then ~10 s (120); the model keeps
   SPREADING past what is asked (v2, v3): end the take when the pool reaches size (--end) and HOLD the last frame (--hold).
   Dark oak = new risk: the water reads by REFLECTION here, not darkening; puddle_comp measures the water vs the take's OWN dry
   frames, so check its pool mask still finds the waterline on dark wood (it was tuned on pale oak).
   THE GLOW = Homie's teal EDGE GLIMMER by script, OK'd ("I think it's fine"): tools/puddle_comp.py --glimmer (lit gain 0.55,
   --dark 1.1, --loop 8), --dry = the de-sheened v2 plate. Whole-pool glow (v3, a Sequel) REJECTED. Server offers the "3D RENDER"
   preset: declined_preset_id 5a77643c-b6cc-4efd-bdc6-ab8ff48dfa82.
3. POST — THE GALLERY SHOW FILES (0 cr, script): the three walls (LIT v2 / DARK v1) as finished files like Scene 9's: the tour
   hold, the blackout bank by bank, the DARK hold (CENTRE foot: the puddle's teal now = the edge glimmer's faint light), Scene
   10's "Light is suddenly restored"; + the floor files from 1 and 2. Nothing in the show folder yet; no upscales unless asked.
STATE: all S1 media on the T9 (master), REORGANISED 5 Oct (REGISTER 'HANDOVER REORG'): 04_WORKING_FILES/S1_gallery/
(00_STATUS_READ_ME.txt, 1_READY_for_show_build/, 2_PUDDLE_RETURN_in_progress/ = new takes go here),
02_APPROVED_BUILDING_BLOCKS/S1_gallery/. Scenes 4 + 5 are now IN 01_FINAL_FOR_SHOW. ON THE PC: run
tools/reorg_2026-10-05.py D:/SOTR run (Scenes 4/5), then copy S1 from the T9 to D: (sha256). Credits: 8 spent
5 Oct late (IMG), balance ~1,859. CREDITS (Homie): keep enough for ALL the gallery's video generations AND upscales, and LEAVE
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
