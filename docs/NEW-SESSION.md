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

THE TASK, RIGHT NOW (2026-09-30, end of session; MODE: VID):
FINISH SCENE 6: three full-HD show files from the approved animatic + the generated flag and smoke.
Scene 9 is approved; don't touch it. Upscaling is parked (Homie: later; files as they are is fine).
- DONE: animatic v4 APPROVED (Homie, 2026-09-30), checked line by line against the script, LOOK.md Scene 6 LOCKED.
- DONE: generated S6-FLAG v1 (take A chosen: no pole) and S6-SMOKE v1 (4 s probes), then 30 s SEQUELS of each
  (jobs 565ac6ac-02ff-4e32-b9d2-7f6ec69bdd43 flag, 2bf6407a-4eb6-448d-bc16-51d587412b77 smoke). 864 credits
  this session; balance ~4,290. Prompts: prompts/S6-FLAG.txt, S6-SMOKE.txt (v2 = the Sequels).
- DONE: tools/render_s6.py carries them (GenFlag: keys the flag off black, restores the blue the firelight
  darkened, rip/bleach/white flag/RoomBurn as approved; GenSmoke: the clip as the smoke density, the animatic's
  colours). tools/s6_loops.py joins probe + Sequel and crossfade-loops them (picture + sound). `--final` writes
  S6_LEFT/CENTRE/RIGHT.mov (1440/1800/1440 x 1080, ProRes 422 HQ 10-bit, 48 kHz 24-bit scratch sound). Tested on 4 s.
STEPS NOW:
1. DONE at wrap: S6-FLAG_v2.mp4 (58a7e1e4…, 1920x1080) and S6-SMOKE_v2.mp4 (7e614fa0…, 2206x946) are complete,
   720 frames / 30.0 s each, and on the T9. They hold ONLY the continuation (not the 4 s probe), so step 3's
   probe + Sequel join is right.
2. Check them (lesson: verify the FILE): probe, a contact sheet across the whole 30 s, the flag has NO pole and
   the same framing as take A, the smoke still drifts left to right. Does the Sequel output START with take A's
   frames? If yes, don't concatenate twice (s6_loops.py joins probe + Sequel).
3. Loops: python tools/s6_loops.py S6-FLAG_v1_A.mp4 S6-FLAG_v2.mp4 S6-FLAG_loop.mov
          python tools/s6_loops.py S6-SMOKE_v1.mp4 S6-SMOKE_v2.mp4 S6-SMOKE_loop.mov --crop-bottom 0.08
   (in S6_generated/; render_s6.py reads exactly those two names). Delete nothing; _test_*_loop.mov were probe-only tests.
4. python tools/render_s6.py - --check --scale 0.25  (must be clean), then stills at 14,30,105,123,127,133,152.
5. Final: python tools/render_s6.py <OUTDIR> --final --scale 1.0   (~70-90 min; run in background).
   Check the three files (probe, frames across the whole 2:45, sound). Send to Homie for approval.
6. On approval: file them (propose 01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_<WALL>.mov, sorts before S9),
   REGISTER, LOG, commit, push, T9 (copy + sha256, never mirror-delete).
7. THEN ask Homie: "Ready for the pipeline v3 update?" (PARKED by Homie 2026-09-30: Precision-Pipeline v3.0.0,
   commit 1ccc580; his full instructions are in the 2026-09-30 chat; don't start until he says yes, and list
   proposed changes before editing anything).
Credits: ask above ~100 per run; one generation at a time; check `transactions` after each.

WHERE SCENE 9 LIVES (SOTR_MEDIA/01_FINAL_FOR_SHOW/, 00_READ_ME_FIRST.txt explains it):
- 1_PLAY_THESE_IN_ORDER/  the 8 show files S9_b<beat>_<WALL>_<world>.mov, sorted = script order
- 2_BACKUP_LOOPS_for_operator/  salon IN/HOLD/OUT, court single strikes, studio HOLD loops
- 3_CLEAN_no_edge/  the same pictures without the edge (_CLEAN masters)
- No versions in show names; REGISTER.md's "SHOW FOLDER" table maps each to its version.
  A new version keeps the SAME show name; the old file goes to 03_TESTS_IN_PROGRESS/superseded/.
- Meeting docs: SOTR_MEDIA/06_PRESENTATIONS/ (one-pager PDF), docs/MEETING-*.html.
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
