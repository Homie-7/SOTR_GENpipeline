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

THE TASK, RIGHT NOW (3 Oct, late). docs/PLAN-MEETING4.md IS THE PLAN. MODE: VID (S6), POST (S5).
1. SCENE 6 v6: HOMIE APPROVED THE DESIGN ("will 100% go with this": the worn smoky torn flag, M4, the centre colour
   switching). Built beside v5 (`render_s6.py --v6`; v5 bit-identical without it). Files: 04_WORKING_FILES/S6_v6_option/
   (1080, 3 walls, sound) and S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4. HIS NOTES = THE NEXT JOB (GenFlag._v6_*):
   a. GLITCHY REVEAL/EXIT: straight horizontal "clipping lines" whenever a v6 flag appears or disappears (v5 eased cleanly).
      Likely cause: _v6_fray() finds each ROW's fly edge from `a > 0.5` AFTER the reveal mask, so rows pop on and off. Fix:
      take the fray from the keyed alpha BEFORE the reveal/hoist masks. Check stills at 116-119 s and 124-129 s.
   b. CENTRE flag exit (~124.8-128.8 s, as the Monarchistes flag comes in): it lingers. Homie: TEAR IT TO SHREDS instead
      of dissolving (Claude's call how: physical, one way, the pieces carried off in the smoke; no cube/brick look).
   c. NAPOLEONISTES (LEFT, cut=...): cut lines + pieces drifting while the cloth still flutters as one flag doesn't read,
      and its bottom border glitches. Rethink, sticking to the script ("Napoléonistes !", a tricolour on LEFT): e.g. the
      tricolour whole but tattered, or the same shredding language as (b). Decide, build, show stills.
   Then re-render 04_WORKING_FILES/S6_v6_option/ (render_s6.py OUT --final --v6 --scale 1.0, ~80 min, affinity FFFF3FFF);
   4K + promote under the SAME show names (v5 to superseded) ONLY when Homie says v6 replaces v5.
2. SCENE 5 BATTLEFIELD (POST): the REAL files are F:\OrCha Drive\SOR Show Final\SOR SHOW\SOR Renders\New Renders\Camps\
   <Front|Left|Right|Bottom>\*.mov (DXV 1920x1080, 25 fps, 7:12, all equal, PCM sound). Homie asked Claude to choose.
   CLAUDE'S RECOMMENDATION: C "cold dusk" (the script, Sc 3: "the day is late; it is eerie, smoky, and cold", north Italy
   near the Alps; the renders are a hot orange sunset). tools/grade_battlefield.py v2: sky mask + ground/sky LUTs + a
   firelight pass (the fires are the only warmth); the first 30 frames (render warm-up) dropped; sound carried.
   Stills: 04_WORKING_FILES/S5_battlefield_grade/S5_grade_ALL_OPTIONS.jpg; 10 s test of Front in C: test_front_C_10s.mov
   (79 s per 250 frames = ~57 min per angle with fires). TO DO: Homie confirms C (or A/B); render the four angles one at a
   time (affinity FFFF3FFF) into that folder; check whether the old cannonball overlays (Camps/Exports, qtrle+alpha) are
   still used. Offer: 4K (~140 cr), a thin battle haze from S6-SMOKE (tested, subtle).
   HOMIE (3 Oct): ALL FOUR ANGLES MUST READ AS ONE SCENE split into four cameras (Unreal rendered them with different
   exposure/colour). After the grade: measure each angle's SKY and GROUND (mean level + colour balance, and the horizon
   band where walls meet), then a per-angle correction (exposure + white balance, separately for sky and ground via the
   sky mask) toward ONE shared target, so the sky, the ground and the light flow from wall to wall. Check with the four
   graded frames side by side (Left | Front | Right, Bottom under) before rendering.
3. THE ALPS ("remove the birds" = the floating orbs?): ask Homie; not started.
CREDITS: 3 Oct: 48 spent (the S6-FLAG-WORN Edit-video test, look fail). Balance 2,267.66.
The floor plan (docs/FLOOR-PLAN.md) is PARKED. Scene 9 is unchanged. The client delivery stays 01_FINAL_FOR_SHOW.
The PC crashes under all-core load (memory pc-core7-crash): every heavy job runs with affinity FFFF3FFF.
Credits: ask above ~100 per run; one at a time; `transactions` after each.

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
