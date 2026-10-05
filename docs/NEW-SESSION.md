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

THE TASK, RIGHT NOW (6 Oct, after Homie's review; NEXT SESSION = VID, MacBook): REDO THE SHIP INTRO. Load house-rules
(+ references/findings-video.md) and shotcaller-v1, MODE = VID, then read docs/VID-BRIEF-S7-INTRO-v2.md (the whole job, from
Homie's verdict), docs/PLAN-SHIP-INTRO.md, docs/AUTONOMOUS-GEN.md, PIPELINE.md (connector), prompts/S7-INTRO-FLIGHT.txt +
S7-INTRO-LAND.txt (v1, what failed), and the top LOG.md rows.
HOMIE'S REVIEW (6 Oct):
  - THE INTRO v1 = FAIL: "the bird is not even flapping… just kind of randomly seeing it glide. It never really goes far or
    close to the camera… looks extremely AI generated. We approach the ship from the front… then we sit on the front deck
    border. The whole point is to land inside the last frame where the scene will continue. So we should be where the
    _strip_wreck_v1 angle is. Redo the thing again, make it more believable." -> brief v2: real wingbeats, the distance to
    camera changes, approach from ASTERN/quarter, come aboard and END EXACTLY ON THE DECK PLATE (end frame made: T9
    S7_ship/4_intro_video/endframe/S7-SHIP-C_day_16x9_ENDFRAME.png; Seedance end_image UNTESTED), our red-ochre ship (no gilding).
  - THE LIGHT STATES: "I approve all the states and times" (day, magic hour, sunset, night, wreck). BUT: "This is a complete
    cohesive single scene, so they all need to align… while they are animated it all looks like a single scene." FIXED (0 cr,
    same day): tools/ship_seams.py -> T9 S7_ship/3_walls/seamed_v1/<day|magic|sunset|night|wreck>/ = THE CURRENT WALLS. The
    side walls' rail now meets CENTRE's at both seams (it stepped 72 / 111 px), the half cathead on the RIGHT seam removed,
    sky and sea colour matched to CENTRE (zone medians, 50-70% less mismatch). Layers rebuilt: 5_layers/seamed_v1/. Review:
    6_review/S7-SHIP_light_arc_preview_SEAMED_v2.mp4 + S7-SHIP_all_states_contact_SEAMED_v2.jpg. Cloud shapes still change at
    the seams (the fold and gap hide it). The old assembled_* sets are superseded (kept).
  - Every animated piece from now on (sea loops, the mast fall, rowboats) is built on seamed_v1 and moves as ONE sea across
    the three walls (same swell direction, speed and scale).
NEXT after the intro: side-wall sea loops (one sea), the mast fall, rowboats + snap, 4K of what Homie approves.
Credits: balance 1,127.49 (6 Oct). Redo cap 450. Keep 500 at the end of the week.

HISTORY (6 Oct morning and night, superseded by the block above):
(was THE TASK, 6 Oct morning, IMG): THE SHIP SEQUENCE (Sc 7-8), a side quest APPROVED by Homie: "make
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
DONE 5 Oct night: SUNSET state of all three walls, chosen + assembled on one horizon: 3_walls/assembled_sunset_v1/
(C b3696a61, L 17bd1936, R 68744df0; real-size sun after one patch). NIGHT prompts WRITTEN, NOT RUN: prompts/S7-SHIP-{C,L,R}-NIGHT.txt
(same edit layout, only the Change line; inputs C media f51d98e7, L f2172e8e, R d81781ae; 2 takes each = 12 cr).
NEXT (IMG): 1) show Homie assembled_v1 (day) + assembled_sunset_v1; 2) run NIGHT, then MAGIC HOUR (patch the Change line);
3) the WRECK on CENTRE (foremast snapped and fallen forward over the bow, rigging slack, water on deck): an edit of the day
CENTRE; 4) layers (tools/ship_layers.py). Then a VID session: the intro flight from 2_intro/S7-INTRO-F1_v1_1714a32e_haze.png
(4 s probe first), sea loops per light, the mast falling, the rowboats + snap. Then 4K of what Homie approves.
LOUISE'S REFERENCE IMAGES (Homie, 5 Oct night): 4 images pasted in chat were TOO BIG to read (>2000 px). Ask Homie for their
file path; read them downscaled (ffmpeg -vf scale=1600:-1) before more look work.
THEN VID (fresh session, house-rules VID + shotcaller-v1): intro flight from the HAZED F1 (4 s probe, then ~15 s + a landing
Sequel), sea loops per light, the foremast falls forward, the rowboats + snap. Then 4K of what's approved.
Credits spent 5 Oct ship session: 60 (NBP 56, outpaint 4). Balance ~1,577.
OVERNIGHT 6 Oct (Claude, Homie asleep, delegated: "finish everything we agreed"; every pick below is PROVISIONAL, for his review):
- LOUISE'S IMAGES READ (~/Downloads/IMG-20261005-WA0019/20/22.jpg + the WhatsApp screenshot): "the sky over the Charente River on my
  last night in France. This is where the Méduse set sail from." Lavender-blue twilight, rose cirrus, a near-full moon. USED AS THE
  MAGIC HOUR SKY, and the NIGHT moon became the same FULL moon (was a crescent) so the evening has one moon.
- ALL FOUR LIGHT STATES DONE, on ONE geometry (T9 S7_ship/3_walls/): assembled_v1 (DAY), assembled_magic_v1, assembled_sunset_v2,
  assembled_night_v2. NEW tools/ship_align.py + ship_states.py warp every state onto the day walls (<1 px): NBP had reframed the
  CENTRE edits by up to 16%, which a light crossfade would show as a jump. Old unaligned sets kept (sunset_v1, night_v1).
- LAYERS: 5_layers/day/ (ship RGBA + sea/sky mask per wall; states reuse the day masks).
- WRECK on CENTRE DONE: v2 take 40936720 (splintered stump, the yard fallen across the deck, wet deck), 3_walls/assembled_wreck_v1/
  + 5_layers/wreck_v1/. v1 kept a standing pole at the bow; v2 fixed it with one sentence (LOG).
- IMG LIST DONE (night, magic hour, wreck, layers). 36 cr (18 NBP takes; balance 1,541.49). NOW: the VID sub-agent, docs/VID-BRIEF-S7-INTRO.md (cap 600 cr).
  Details: LOG.md 2026-10-06 rows. CHECK if the credits really expire today (6 Oct) and when. Mac kept awake by caffeinate.
- VID (night 6 Oct) DONE, 414 cr of 600 (balance 1,127.49), all PROVISIONAL for Homie: REVIEW CUT = T9 S7_ship/4_intro_video/
  S7-INTRO_review_v1.mp4 (22.4 s, 1800x1080, sound) + S7-INTRO_review_v1_3walls_4680.mp4 (cut to the DAY deck walls). FLIGHT v2
  (b37921bd, 1080p): smooth follow, the ship grows, the gull meets her HEAD-ON (the model drew her bow, not her stern); its
  Union-Jack-like masthead flag painted WHITE by script (_flagwhite.mov); trimmed at f346 (an end rush). LANDING v2 Sequel
  (4140a014): over the bow rail, lands, stands 3 s (deck matches our walls), rises, wing over the lens. CHECKED BY THE PARENT SESSION: the deck only PARTLY matches our walls (red bulwarks, guns,
  rope coils, but a turned BALUSTRADE rail and a dark banded mast; the flight's hull is dark with GILDED bands vs our red-ochre):
  the dissolve onto the deck walls lands on a different-looking ship. Homie to judge: head-on
  vs astern; the ship's gilded 18th-c. bow; the quick last-2-frame wing wipe (v1 draft 4ff856e8 has a slower one, ruffled wings).

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
