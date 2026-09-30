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

THE TASK, RIGHT NOW (2026-09-30, end of day; MODE: POST):
SCENES 6 AND 9 ARE APPROVED AND IN 01_FINAL_FOR_SHOW/. Pipeline v3 adopted FORWARD ONLY. Nothing old is redone.
AN OVERNIGHT CHAIN RAN: SOTR_MEDIA/03_TESTS_IN_PROGRESS/OVERNIGHT_2026-09-30.sh, log OVERNIGHT_2026-09-30.log beside it.
It: restores the 4K S6 flag/smoke loops (S6_generated/4K/) -> renders Scene 6 at 4K from the approved v5 script into
03_TESTS_IN_PROGRESS/S6_final_4K/ (render.log there; ~5-6 h) -> waits for court b5 + the studio v4 build -> copies
everything new to the T9 with sha256. READ THE LOG FIRST: it must end "OVERNIGHT FINISHED" with "mismatches 0".
ALSO OVERNIGHT: Scene 9 fixes (Homie: salon edge artifacts; the judge floating after the slam):
SOTR_MEDIA/03_TESTS_IN_PROGRESS/scene9_fix_v4/FIX.sh, log FIX.log: rebuilt salon edge + court files, auto-checked,
promoted into 01_FINAL_FOR_SHOW under the same names (approved ones -> superseded/scene9_v3_pre_fix/), then T9.
READ FIX.log: every line PROMOTED (or HELD BACK + why), ends "FIX + T9 FINISHED", mismatches 0.
STEPS NOW:
0. Look at the promoted files in a player (the sconce by the salon break at ~1:00 in b2-3; b8's snuff at ~0:08; court
   b5 at 1:18 feet on the floor), update REGISTER's SHOW FOLDER table (salon v4 edge, court v3 placement), README if
   needed. The 4K versions of the changed files (b2-3, b8, b3, b5) must be redone from the new files (cheap).
   Studio v4 b6's edge was rendered before the edge fix: re-render it with edge_flow.py v3 before showing Homie.
1. Scene 6 4K: probe the three files (3600/2880 x 2160, 3,960 f, sound), contact sheet every 10 s, compare frames to
   the approved 1080 v5 (01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_*_wars.mov). A crash means a rerun (no resume yet).
2. Scene 9 4K: all 8 in upscale_4k/<name>_4K.mov. Checked so far (LOG): b8, b6, b4 (+ sound on 5). Check b2-3, b3, b5,
   b7, b9 the same way (PSNR back to 1080, geometry, motion, sound, crops).
3. Studio candle arc v4 (LOOK D6): studio_candle_arc/loc_SOTR_studio_L_b6_s9_v4.mov (+_edge2) and b9. Check them
   (build.log), then SEND TO HOMIE for approval: beat 6 = generated 10 s flare take; beat 9 = the 30 s take calmed
   (loop_halo --boost 0.4) + lifted (candle_beat --lift 1.08,0.25). On approval: they replace S9_b6/b9 in the show
   folder (v3 to superseded/), REGISTER, README; 4K them like the rest.
4. Then with Homie: the 4K folder layout/names; his studio-painting texture call (finishing.md warning); next scene.
CREDITS 2026-09-30: 1,849 spent (864 S6 generations, 49 upscales, 936 candle arc: 360 of it wasted on a 30 s B6
take that lost its surges, see LOG). Homie: "just because you have credits to use doesn't mean you waste them."
Balance ~3,390.
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
