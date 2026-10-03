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

THE TASK, RIGHT NOW (after 2026-10-02; MODE: whatever the client's notes need). THE JOB IS FINISHED (Homie, 2026-10-02:
"I think we'll call it finished"). He is meeting the client and will come back only if more is needed. DON'T CHANGE ANYTHING
unless he asks. Scenes 6 and 9 are approved, 4K, cleaned up and backed up to the T9 (sha256-identical, 2026-10-02).
THE CLIENT DELIVERY = SOTR_MEDIA/01_FINAL_FOR_SHOW/ (upload the whole folder): 1_PLAY_THESE_IN_ORDER (11, 4K) +
2_BACKUP_LOOPS_for_operator (10, 4K) + 3_HD_1080_fallback (the same 21 at 1080). Studio b9 = candle arc v5, b6 = v3.
CLEANUP 2026-10-02: the media was recompartmentalised (SOTR_MEDIA/README.txt is the map) and everything unneeded went to
D:\SOTR\_DELETE_ME_2026-10-02 and G:\SOTR\HF\_DELETE_ME_2026-10-02 for Homie to empty. If they're still there, they're his;
don't use anything in them (D:\SOTR\CLEANUP_2026-10-02_moves.tsv lists every move if something has to come back).
IF HOMIE COMES BACK: start by asking what the client said. Client notes = a new version under the SAME show name: rebuild
clean from 02_APPROVED_BUILDING_BLOCKS with tools/ (recipes in 04_WORKING_FILES/build_recipes/; their paths are
pre-cleanup, the README has the map) -> 03_CLEAN_MASTERS_no_edge (old file to 04_WORKING_FILES/superseded/), the edge on
top (04_WORKING_FILES/edge_kits/) -> 01, then 4K by the 2026-10-01 route (ByteDance + upscale_restore + upscale_check
VERDICT; records in 04_WORKING_FILES/4K_records/), then the T9. A new scene = PREP first (card, look with Homie), v3 stack
(CLAUDE.md standing rules). New tests go in a new 04_WORKING_FILES/<name>/ folder.
The PC crashes under all-core load (memory pc-core7-crash): every heavy job runs with affinity FFFF3FFF.
IF A FLOOR PROJECTOR IS CONFIRMED: follow docs/FLOOR-PLAN.md (ready, not started; the judge's shadow is a YES, no carpet).
OPTIONAL, NOT DONE (Homie: no extra work): a v5 version of the b9 studio backup HOLD loop (the v3 one is ~24% dimmer).
Open with the team: set dimensions, codec (three 4K ProRes files at once in Scene 6 is heavy; the 1080 set is the fallback),
pre-warp, rehearsal timings.
CREDITS: 0 on 2026-10-02; 81.30 on 2026-10-01. Credits: ask above ~100 per run; one at a time; `transactions` after each.

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
