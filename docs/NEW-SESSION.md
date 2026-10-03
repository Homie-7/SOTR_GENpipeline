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

THE TASK, RIGHT NOW (after Meeting 4; updated 2026-10-03 evening). docs/PLAN-MEETING4.md IS THE PLAN.
1. SCENE 6 FLAGS: DONE AS AN OPTION. v6 is built BESIDE v5 (Homie: "don't overwrite anything… present both"):
   `render_s6.py --v6` (v5 renders bit for bit without it). For the client: 04_WORKING_FILES/S6_flags_v6_preview/
   S6_v5_vs_v6_COMPARE.mp4 (A over B, M2/M4/M6) and 04_WORKING_FILES/S6_v6_option/ (v6 at 1080, three walls, sound).
   WAITING ON: Homie's view of v6, then the client's pick. If v6 is picked: 4K by script (render_s6 --final --v6 --scale
   2.0 with the 4K loops, ~4 h, affinity FFFF3FFF), then it replaces v5 under the SAME show names (v5 to superseded).
   The generated wear (S6-FLAG-WORN v1, 48 cr) FAILED on look; don't run the 360-cr pass unless Homie asks.
2. NEXT (MODE: POST, a fresh session): the Alps (remove "the birds" = probably the floating orbs; ASK Homie, the still is
   in 04_WORKING_FILES/meeting4_prep/), 3. the battlefield grade: OPTIONS BUILT 3 Oct (tools/grade_battlefield.py; LUTs + stills in 04_WORKING_FILES/
   S5_battlefield_grade/; Claude recommends A, amber dusk). WAITING ON Homie's pick + how the 4 different-length angles are used;
   then grade every angle and the cannonball overlays (alpha kept) by ffmpeg lut3d, ProRes, native 29.97, sound copied. Sources:
   F:\OrCha Drive\SOR Show Final\SOR SHOW\SOR Renders\Alps\ and ...\Camps\Exports\; outputs to D: (SOTR_MEDIA).
   Both 0 credits. The Higgsfield subscription ENDS on the 2nd (Nov; confirm).
CREDITS: 3 Oct budget 1,000, spent 48 (balance 2,267.66). "Very conservative, no wasted credits".
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
