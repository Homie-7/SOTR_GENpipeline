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

THE TASK, RIGHT NOW (4 Oct, overnight). docs/PLAN-MEETING4.md IS THE PLAN. MODE: POST (S4, S5), VID done (S6).
FOR HOMIE TO REVIEW (everything below was built on his delegation while he slept):
1. SCENE 6 v6.2 (the option beside v5): the CENTRE flag now TEARS INTO RAGGED SCRAPS that tumble away (his note on v6.1's
   "office shredder" streamers); everything else as v6.1 (reveal fix, Napoléonistes tattered). 04_WORKING_FILES/
   S6_v6_option/ + S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4. 4K + promote ONLY when he says v6 replaces v5.
2. SCENE 9 STUDIO CANVAS EDGE: DONE AND IN THE SHOW (his "make the changes in the final file itself"): ragged plaster lip
   beside the canvas + the canvas edge sunk into shadow at its corners, b4/b6/b9 + HOLD loops, 4K + 1080, checks PASS.
   Old files in 04_WORKING_FILES/superseded/studio_pre_canvas_edge/ (swap back if he dislikes it).
3. SCENE 5 CAMPS: grade C ("cold dusk") + the angle match (sky/ground per angle to one target, seam ramps) ->
   04_WORKING_FILES/S5_battlefield_grade/C_matched/S5_camps_<angle>_C.mov (1080, 25 fps, sound). Check the four side by
   side (Left|Front|Right, Bottom under). Open: 4K (~140 cr); the old cannonball overlays (Camps/Exports, qtrle+alpha).
4. SCENE 4 ALPS: grade S4 (C's stock in daylight, so Alps -> camps reads as one film) + angle match + Despeck (small
   specks/orbs in the sky replaced by their +-1 s median) -> 04_WORKING_FILES/S4_alps_grade/S4_matched/. ASK HOMIE:
   (a) the current Alps = New Renders/Alps (3:36, used, as the camps) or SOR Renders/Alps/AlpsF..mp4 (2:00, 29.97, orbs)?
   (b) "the birds" = ? (no birds seen in the New Renders; the 2:00 exports have glowing orbs). Lens flares: ignore (Homie).
5. Then: show files for Scenes 4/5 (names, 4K, delivery), the Scene 5 -> 6 join (Scene 6 opens on red-brown smoke; C is
   cold: check the cut), the floor plan (parked).
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
