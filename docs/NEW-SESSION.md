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

THE TASK, RIGHT NOW (4 Oct, morning). MODE: POST. Homie's weekly model limit is near: finish TODAY, and right.
DECIDED BY HOMIE (4 Oct): (a) Scene 6 v6.2 REPLACES v5 in the show; (b) the Scene 9 studio canvas edge is APPROVED (in the
show); (c) Alps = the CLEAN `F:/OrCha Drive/SOR Show Final/Renders (050422)/Alps/` renders, grade A4 "natural daylight"
(S4_alps_v2_FOR_HOMIE.jpg, row 2); (d) camps = option N "RICH DUSK" (S5_options_v4_FOR_HOMIE.jpg: only the red soil
turns to earth; sky/sun/light as rendered; fires = the original flame cores by position, no warm pool). EXPOSURE MATCHED
FULLY across all four angles is imperative (MATCH_EXP 1.0 in grade_battlefield.py). He found C "extremely dull".
RUNNING AT HANDOVER (detached, affinity FFFF3FFF; logs in C:/Users/Homie/AppData/Local/Temp/claude/C--Users-Homie-Documents-SOTR-GENpipeline/15f546ce-6f02-4c65-a43e-4e27570918e5/scratchpad/):
  - s4v2.log: Alps A4 renders -> 04_WORKING_FILES/S4_alps_grade_v2/A4_matched/S4_alps_<front|left|right|bottom>.mov
    (29.97 fps native, first 30 warm-up frames dropped, --despeck = the birds, sound). Front done 08:04.
  - s5n.log: camps N renders, start after S4V2_ALL_DONE -> S5_battlefield_grade/N_matched/S5_camps_<angle>.mov
    (New Renders/Camps, 25 fps, ~1 h per angle).
NEXT, IN ORDER:
1. SCENE 6 v6.2 -> SHOW: uploads ready (04_WORKING_FILES/S6_v6_option/uploads/*.mp4, HEVC crf 12). media_upload ->
   tools/put_upload.py -> media_confirm -> CDN size check -> ByteDance upscale_video aigc 4k 24 fps, ONE AT A TIME,
   `transactions` after each (~13 cr per wall) -> tools/fetch.py -> upscale_restore.py --clamp 2 (--size 2880x2160 sides,
   3600x2160 CENTRE) -> upscale_check.py VERDICT -> promote under the SAME names: 4K into 01_FINAL_FOR_SHOW/
   1_PLAY_THESE_IN_ORDER/S6_<WALL>_wars.mov, 1080 into 3_HD_1080_fallback/1_PLAY…, a copy into 03_CLEAN_MASTERS_no_edge/
   S6_<WALL>_wars_CLEAN.mov; every v5 file to 04_WORKING_FILES/superseded/S6_v5/ (sha256 every move). The studio run of
   3 Oct is the template (S9_studio_canvas_edge/: JOBS_4K.txt, the job script pattern; give ffmpeg </dev/null in loops).
2. When the Alps + camps renders finish: verify frames/sound, a side-by-side sheet (L|F|R, Floor under) per scene, and
   1:1 crops of the floor (no speckle). Make H.264 REVIEW COPIES (crf 18) beside the ProRes: D: is a spinning HDD and the
   7-min ProRes HQ (217 Mb/s) stalled in his player. Show Homie.
3. Then (ask): Scenes 4/5 as show files (names S4_/S5_<WALL>_<world>.mov, the floor angle separately), 4K (~0.08 cr/s),
   the cannonball (050422 Camps/Cannonball EXR + CB_Explosion), the Scene 5 -> 6 join (S6 opens on red-brown smoke).
NOTES: grade_battlefield.py now has options N/N2/N3 (camps) and A4 (Alps), FirePass(pool=False) = flame cores only,
soft air masks for the Alps, the camps sky masks refined per pixel near the horizon (mask_<a>_v2.png = the C-era masks),
Despeck, the frame-count bound. The camps Front sky has birds (left; --despeck removes them if asked).
CREDITS: 3-4 Oct: 48 + 19.29 spent; balance ~2,248 (keep >= 1,500, Homie) (the S6-FLAG-WORN Edit-video test, look fail). Balance 2,267.66.
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
