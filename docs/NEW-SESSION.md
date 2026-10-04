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

THE TASK, RIGHT NOW (5 Oct): A NEW SCENE, BUILT ON THE MACBOOK PRO. Ask Homie which scene and its brief first.
MODE: declare it for the new scene (IMG for plates first, VID after; never both in one chat). New scenes' prompts use the
v3 stack (scenecraft-v1 plates, shotcaller-v1 video) under SOTR's rules (CLAUDE.md standing rules).
THE MAC SETUP (no F: drive, no D: drive: work from the T9 only; the new scene has no dependencies on F:):
- Repo: `git pull` the Mac clone (or `git clone https://github.com/Homie-7/SOTR_GENpipeline.git`). The T9 also holds a
  clone at <T9>/SOTR/HF/SOTR_GENpipeline (find the mount with `ls /Volumes`).
- Skills: Precision-Pipeline at ~/Documents/HF/Precision-Pipeline, NOT installed: run its `bin/install.py` (README.md).
- Media: write the new scene's files to <T9>/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/<new scene folder>/ (same layout as D:).
  THE T9 IS THE MASTER for that folder until it is copied back to the PC's D:\SOTR\SOTR_MEDIA (copy + sha256, never
  mirror-delete; on the PC tools/backup_t9.py copies D: -> T9 only, so the reverse copy is by hand / a new script).
- Windows-only, IGNORE on the Mac: the Core 7 affinity rule, PowerShell launches, the D: junction, F:/Unreal renders,
  tools/backup_t9.py's paths. The Higgsfield CDN downloads still go through tools/fetch.py if on the same home network
  (DNS interception, memory dns-interception).
- Source script/PDFs: /Users/homie/Documents/SOTR/ (docs/SOURCES.md). BIBLE.md has the play's scenes.
STATE (all finished, committed dbce80f, T9 backed up 221 GB, 0 mismatches, 4 Oct 23:59):
- Show folder 01_FINAL_FOR_SHOW = Scenes 6 (v6.2, 4K) and 9. Unchanged.
- Scene 4 Alps APPROVED: 04_WORKING_FILES/S4_alps_grade_v2/A4_matched/. Scene 5 camps DONE: PRIMARY rich dusk
  S5_battlefield_grade/S5_PRIMARY_rich_dusk/ (approved), SECONDARY Cold dusk S5_SECONDARY_cold_dusk/ (client chooses).
  Neither is in the show folder or upscaled (Homie: not needed).
- Homie, 4 Oct: "Just make the things that I asked you to make" (memory only-what-asked): no unrequested next steps.
CREDITS: balance ~2,207 (keep >= 1,500). Ask above ~100 per run; ONE job at a time; `transactions` after each.
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
