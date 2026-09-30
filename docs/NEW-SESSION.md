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

THE TASK, RIGHT NOW (2026-10-01; MODE: POST). SCENES 6 AND 9 ARE APPROVED; this is their 4K finishing.
FIRST: did the PC crash again? `Get-WinEvent` System Id 41 / WHEA 18 (memory: pc-core7-crash; every heavy job runs with
affinity FFFF3FFF, off Core 7). Then READ, in SOTR_MEDIA/03_TESTS_IN_PROGRESS/upscale_4k/: queue5.log (4K of the fixed
b2-3/b8/b3/b5 + the b9 check; must end QUEUE5 FINISHED), lane0.log + lane1.log (4K of the 10 backup loops, 8 Scene 9
clean masters, the candle arc v5), results_v3.txt (one VERDICT per file), finish_4k.log + promote_4k.log.
IF promote_4k.log ends "PROMOTE 4K FINISHED" (T9 mismatches 0): 01_FINAL_FOR_SHOW folders 1-3 ARE 4K (same names), the
approved 1080 set is in 01_FINAL_FOR_SHOW/4_HD_1080_same_files/, README replaced. Check a few 4K show files in a player,
then REGISTER (mark done), LOG, commit, push, T9 repo pull.
IF "GATE FAILED": nothing moved; the failing file is named. Look at its .check.txt (upscale_4k/BACKUP|CLEAN/), fix
(re-restore, or re-upscale ~0.08 cr/s), then `python promote_4k.py --dry`, then without --dry. A crash mid-lane: rerun the
lane (`lane_v3.sh 0|1`, it skips finished files; _tmp_ files are partial, delete-bin them).
WAITING ON HOMIE: the studio candle arc v5 (studio_candle_arc/loc_SOTR_studio_L_b6_s9_v5_edge2.mov + b9; LOOK D6: b6
flares, b9 steady and brightest). v4 was withdrawn (floor under the wall; tools/plate_align.py fixed it; LOG). On approval:
replace S9_b6/b9 in the show folder (4K from upscale_4k/CANDLE_v5/, 1080 in 4_HD_1080_same_files/; the _CLEAN from the
v5 clean), the v3 files to superseded/, REGISTER, README ("COMING NEXT" line goes).
Homie 2026-10-01: Scene 6 (1080) reviewed, "happy with them"; the Raft painting at 4K "fine"; the 4K layout delegated
("these are all just 4K in the play these in order folder"). After Scenes 6 and 9 the job is likely done unless the
client comes back. Open with the team (unchanged): set dimensions, codec (4K ProRes x3 at once is heavy; the 1080 set is
the fallback), pre-warp, rehearsal timings.
CREDITS 2026-10-01: 81.30 (21.95 overnight 4K of the fixed files + 59.35 of Homie's expiring bonus credits on the rest
of the show folder's 4K). Nothing generated. Credits: ask above ~100 per run; one at a time; `transactions` after each.

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
