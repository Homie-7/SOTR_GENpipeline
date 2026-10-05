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

THE TASK, RIGHT NOW (5 Oct, evening, IMG, MacBook): THE SHIP SEQUENCE (Sc 7-8), a side quest APPROVED by Homie: "make
the calls and go ahead". READ docs/PLAN-SHIP-INTRO.md FIRST (sources, Sahaj's notes decoded, designed-for-destruction,
Sahaj's angle, credits). Higgsfield credits EXPIRE 6 Oct: spend them today, one job at a time, no waste.
STATE (updated as work goes): v1 rejected (two masts). v2 DONE: 4 takes in T9 04_WORKING_FILES/S7_ship/1_deck_master/;
CHOSEN (Claude) = S7-SHIP-ROOM_v2_f5180ed8 (one foremast, bow closest, both sides big). INTRO-F1 v1 DONE: 3 takes in 2_intro/
(the 4th, 66ad98e8, was still rendering); CHOSEN = S7-INTRO-F1_v1_1714a32e (the Medusa dead centre on the horizon). The gull
CHECKED = goeland argente (Larus argentatus), the lead species of Homie's link: every field mark right (Homie: "imperative").
Homie's notes 5 Oct: VOLUMETRIC HAZE in the distance, real physics, the ship NOT so clear from beside the bird, DOF; IN POST
(credits precious): tools/aerial_haze.py (Koschmieder haze by true sea distance + thin-lens DOF, gull kept sharp), applied to
the START FRAME before the video. Sahaj's angle seen (Desktop/VID-20261005-WA0016.mp4): ONE continuous camera across the
three walls -> walls are CUT FROM ONE PLATE (tools/ship_walls.py), outpaint sideways to keep the full height.
Night-shift auto-resume: blocked by the safety check; Homie restarts the session himself from THIS file.
DONE since: haze/DOF on F1 (2_intro/S7-INTRO-F1_v1_1714a32e_haze.png). THE THREE WALLS ARE ASSEMBLED (v1, 0 cr):
T9 04_WORKING_FILES/S7_ship/3_walls/assembled_v1/ (LEFT 260b6359 + CENTRE from master f5180ed8 + RIGHT 972c8b09, one horizon;
tools/ship_assemble.py --hz-c 0.387). One-plate cutting + outpaint FAILED (LOG). AWAITING HOMIE'S LOOK CHECK (Claude decides if away).
NEXT IMG (cheap, tonight): the light states of the three walls as NBP text-only edits (magic hour, red sunset, purple night) and
the WRECK state (foremast snapped, rigging slack, water on deck), then layers (tools/ship_layers.py).
THEN VID (fresh session, house-rules VID + shotcaller-v1): intro flight from the HAZED F1 (4 s probe, then ~15 s + a landing
Sequel), sea loops per light, the foremast falls forward, the rowboats + snap. Then 4K of what's approved.
Credits spent this session: 44 (NBP 40, outpaint 4). Mac kept awake by caffeinate.

PREVIOUS (5 Oct, latest): SCENES 1+10 DONE AND IN 01_FINAL_FOR_SHOW. 01 IS THE COMPLETE CLIENT UPLOAD (S1, S4, S5, S6, S9, S10).
Ask Homie which is next; recommend 1 (it's the next production job), and 2 when the PC is next on.
1. IMG — THE SURPRISE SCENE (Scene 8), parked behind the gallery. Start from BIBLE.md / the script PDF; LOOK first, nothing
   invented (look decisions go to Homie with a recommendation).
2. ON THE PC: run tools/reorg_2026-10-05.py D:/SOTR run (Scenes 4/5), copy S1 (the whole 04_WORKING_FILES/S1_gallery +
   02_APPROVED_BUILDING_BLOCKS/S1_gallery + the gallery files now in 01_FINAL_FOR_SHOW) from the T9 to D: (sha256: the T9's
   SHA256SUMS_2026-10-05_gallery.txt), superseded/S1_gallery too.
DONE 5 Oct: gallery walls re-hung centred (LIT/DARK v3), 1080 full-length show files + 4K loops, the floor files with the
puddle FLOW (Homie: "fine"), promoted by tools/promote_gallery_2026-10-05.py (log: T9/SOTR/HF/PROMOTE_GALLERY_2026-10-05_moves.tsv),
client readme + SOTR_MEDIA/README.txt updated. Homie's open question answered: the dark files never go to full black (the
operator's fade does that before Scene 2).
STATE: all S1 media on the T9 (master), REORGANISED 5 Oct (REGISTER 'HANDOVER REORG'): 04_WORKING_FILES/S1_gallery/
(00_STATUS_READ_ME.txt, 1_READY_for_show_build/, 2_PUDDLE_RETURN_in_progress/ = new takes go here),
02_APPROVED_BUILDING_BLOCKS/S1_gallery/. Scenes 4 + 5 are now IN 01_FINAL_FOR_SHOW. ON THE PC: run
tools/reorg_2026-10-05.py D:/SOTR run (Scenes 4/5), then copy S1 from the T9 to D: (sha256). Credits: 222 spent
5 Oct (VID + POST), balance ~1,637. CREDITS (Homie): keep enough for ALL the gallery's video generations AND upscales, and LEAVE
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
