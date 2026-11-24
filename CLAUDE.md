# Secret of the Raft — projection backgrounds

Project code `SOTR`. Era law: **nothing in any Scene 9 world is newer than 1819.**

These are theatre projection backgrounds, not a film. Live actors perform in front of them
on a three-surface set. The whole pipeline follows from that.

## State files — read before acting

| File | Authority |
|---|---|
| `STAGE.md` | **The set and the render spec.** Three surfaces, true scale, locked cameras, seams. Read before building any plate. |
| `PIPELINE.md` | **The 10 steps every world goes through**: card → room master → front/left/right → seam check → loops → master comp → approve → upscale. |
| `BIBLE.md` | The play, the Scene 9 structure, the era. |
| `LOOK.md` | Per-world look. Only sections marked `LOCKED` may go into a prompt. |
| `SHOTCARDS.md` | Cue cards and the deliverables list. Cards are written before prompts. |
| `REGISTER.md` | **Source of truth for what exists.** Not approved = can't be used as a reference. |
| `LOG.md` | Every generation, one row. |
| `prompts/` | Final text of every plate and loop, by ID. |
| `docs/NEW-SESSION.md` | The opener for a fresh session. **Update it on every wrap.** |

These outrank the `house-rules` skill. If one contradicts it, say so once, then follow the
file.

`house-rules` and the vendored skills come from `Precision-Pipeline` (see `README.md`). On the Mac it is cloned at `~/Documents/HF/Precision-Pipeline` but not installed; run its `bin/install.py` or read the skill from there.
Some of `house-rules` was written for *First Day on the Job*, a character film. **Where it
assumes characters, lipsync, or a moving camera, it doesn't apply here.** Its rules on
references, negation, iteration and logging still do.

## Mode

Declare **IMG**, **VID**, **PREP** or **POST** at the top of every session and hold it. Image and
video vocabularies poison each other, so one session never spans both. **POST** (added 2026-09-30 with pipeline
v3) is finishing an approved picture: upscales, the restore, grades, encodes, delivery. It follows
`house-rules/references/finishing.md` (keep the raw master; check any upscaler for temporal stability).

## Standing rules

- **MEDIA LIVES ON D: (Homie 2026-09-30, C: was 95% full: "migrate the whole thing to D drive").** `SOTR_MEDIA` is at
  `D:\SOTR\SOTR_MEDIA`; `C:\Users\Homie\Documents\SOTR_MEDIA` is a directory JUNCTION to it, so every tool, path and AE
  project still works. **The archive is gone (cleanup 2026-10-02, Homie: "delete everything unnecessary"):** history,
  rejects and old tests went to `D:\SOTR\_DELETE_ME_2026-10-02\` (and `G:\SOTR\HF\_DELETE_ME_2026-10-02\`) for Homie to
  delete; every move is in `D:\SOTR\CLEANUP_2026-10-02_moves.tsv`. Claude never hard-deletes: unneeded media goes to a
  dated `_DELETE_ME_` bin and Homie empties it. The repo stays on C: (small). Cross-drive moves are always
  `tools/archive_move.py` (copy, sha256, then remove). Check the junction exists before writing media
  (`D:\SOTR\_migration.log`).

- **Pipeline v3 is adopted FORWARD ONLY (Homie, 2026-09-30).** *"What's done is done, and if it's good enough,
  we don't need to redo something just because we updated our production system."* Precision-Pipeline 3.0.0
  (commit 1ccc580) is not changed from here. **Per-production exception:** SOTR's approved video prompts use
  cinema-director-v3's labelled blocks (SCENE / REFERENCE / FIRST FRAME / FORMAT / CAMERA / MOTION / LIGHTING /
  AUDIO / QUALITY / LOCKS), its image prompts the LIRA / NBP reference-led prose. **Any variant of an approved
  prompt keeps that layout** (patch one line, never a regrammar); the prompt files are self-contained, so the
  retired skills need no reinstall. **New scenes' new prompts use the v3 stack** (`scenecraft-v1` for plates,
  `shotcaller-v1` for video) under SOTR's rules. **House-rules v3 conflicts, SOTR wins:** generation audio stays
  ON (sound rides in every show file; not Override 12's silent generation), and SOTR's own `@Image 1` token rule
  stands (Override 14). Adopted from v3: POST mode (above), THE GATE (in `docs/AUTONOMOUS-GEN.md`'s pre-flight).

- **FINAL PRODUCT, NO PLAYBACK FIXES (Homie, 2026-09-24).** *"We are not going to rely on
  QLab or any projection software whatsoever. We are generating everything as a final
  product."* Every delivered file already plays correctly: joins, transitions, holds, fades
  and matching are built INTO the file. Ideally generated; if generation can't do it, mixed
  or composited into the file. Never close a problem with "QLab / the media server / the
  mapping software will handle it." This overrides every older line in `STAGE.md`,
  `PIPELINE.md`, `LOOK.md` and `SHOTCARDS.md` that hands content work to playback (loops
  "held by QLab", "QLab cuts to it", a playback crossfade). **Refined the same day (Homie):
  the fades at a file's very START and END are the show operator's**, so files start and end
  at full picture, with no fade-in or fade-out. **And each wall is a FRAGMENT of reality, not a
  hard rectangle:** whole on its outer side, breaking up toward the CENTRE of the stage (the
  2022 Slide 9 concept). **The edge is ON the whole time a wall is lit, on every wall**
  (Homie, 2026-09-25), and **the show plays the edge versions** (`1_PLAY_THESE_IN_ORDER/`). Depths
  are `LOOK.md` D15/D16: nothing animated or important ever breaks, and the break moves ONE WAY only.
  Built by script: `tools/edge_flow.py` (a generated Control-block break, frozen, its blocks drifting
  off; salon, studio) and `tools/court_burn.py` via `render_court.py --scrim --burn` (the court's
  paper burns). Retired: `break_strip.py` (ping-pong), `--edges` (torn paper), `--fragment-edge`. **Open with Homie:** (1) how a
  beat's length is set now that nothing holds a loop live, i.e. fixed-length files per
  beat, which need beat timings; (2) whether the physical fit onto the angled flats
  (keystone/warp) still happens in playback, or the files must be pre-warped.

- **Folders (Homie, 2026-09-24; restructured 2026-09-26; RECOMPARTMENTALISED 2026-10-02 at the cleanup).
  `SOTR_MEDIA/01_FINAL_FOR_SHOW/` IS THE CLIENT DELIVERY: upload the whole folder.** It holds
  `00_READ_ME_FIRST.txt` (client-facing, keep it current) and `_SHA256.txt`, `1_PLAY_THESE_IN_ORDER/` with ONE SUBFOLDER PER
  SCENE in script order (`S01_Au-Louvre`, `S02_painting-melt`, `S04_the-Alps`, `S05_the-camps`, `S06_Napoleonic-wars`,
  `S09_the-Aftermath`, `S10_back-at-the-Louvre`; hand-over reorg 2026-11-25, Homie: "so that I can just take one folder, hand
  it to the show people"), `2_BACKUP_LOOPS_for_operator/` (4K; no court loops), `3_HD_1080_fallback/` (S2 + S6 + S9 at 1080, same
  scene folders), `4_CLIENT_OPTION_S5_cold_dusk/`. FLOOR files live with their scene's files (Homie 2026-11-24: "No need to have separate folders for the floor projection, keep them with the final for show files where they apply."). Then `02_APPROVED_BUILDING_BLOCKS/` (every generated source the show is built from,
  incl. `S6_generated/`, `studio_b9_candle/`), `03_CLEAN_MASTERS_no_edge/` (the `_CLEAN` masters),
  `04_WORKING_FILES/` (edge kits, build recipes, 4K records, `superseded/`, and any new test folder; **8 Oct cleanup,
  Homie: "anything that isn't going to make it to the show and/or isn't needed to make adjustments and changes can be
  binned": it holds only recipes, chosen sources and live work (4.6 GB on the T9); `tools/cleanup_2026-10-08.py`**),
  `05_REFERENCE_UPLOADS/`, `06_PRESENTATIONS/`, `comp/` (Homie's After Effects area; never reorganise
  it). **No version numbers in show names**; the version lives in `REGISTER.md`. A new version takes
  the SAME show name and the old file goes to `04_WORKING_FILES/superseded/` with its version added.
  Map in `SOTR_MEDIA/README.txt`. Older rows below quote the old layout (`03_TESTS_IN_PROGRESS/`,
  `3_CLEAN_no_edge/`, `4_HD_1080_same_files/`, per-wall folders, `with_edge_effect/`).
- **Clean first, effects separate (Homie, 2026-09-24).** *"File management 101."* Every
  finished render is saved CLEAN (no effects) in `SOTR_MEDIA/03_CLEAN_MASTERS_no_edge/` and is
  never overwritten; a change is a new version (the old file to `superseded/`). Anything
  added on top (the fragment edge, any effect) is a SEPARATE file (`1_PLAY_THESE_IN_ORDER/`,
  `2_BACKUP_LOOPS_for_operator/`), rebuilt from clean. Homie can do the
  fragments in post himself, so the clean render is the deliverable that matters. Generated
  sources in `02_APPROVED_BUILDING_BLOCKS/` are never modified. `tools/render_wall.py` enforces this.
- **Sound rides in every show file (Homie, 2026-09-25).** *"Embed it within the file, don't get
  rid of any of the audio."* The generated clips' own sound, cut with the picture by
  `tools/build_audio.py` (verify with a correlation against the source). A scratch reference for
  the sound designer, not the sound design. Any new picture tool must carry it through.
- **Credits (Homie, 2026-09-25).** *"I trust you to generate things and try things out, but not
  at the cost of a thousand credits spent within an hour."* The 1,000 cap is a ceiling, not a
  target. Build on what he has praised before generating anything new; submit one job at a time.
- **Reference tokens in prompts (Homie, 2026-09-24).** Higgsfield resolves only `@Image 1`,
  `@Video 1`… (numbered by upload order). A register tag like `@loc_SOTR_salon_R_s9_v1` in a
  prompt body is NOT resolved; it's dead text. So register tags live in file HEADERS only.
  Prompt bodies say `@Image 1` / `@Video 1` for web runs, and plain words ("the attached
  clip") for connector runs until the API's token syntax is verified. This overrides
  `house-rules`' one-string-everywhere naming rule for prompt bodies.
- **Locked cameras, always.** No push, pan, tilt or drift in any generation. Motion only
  happens inside the image.
- **Walls as walls.** Each surface is the matching wall of the room, square-on, at true
  scale. The image's bottom edge is the stage floor, and no floor is visible
  (`STAGE.md`).
- **One world = one room master, then as many cameras as that world actually uses on
  stage.** The room master (never projected) comes first — a design sign-off and a
  materials/light reference, always built with all three of the room's own walls in view.
  **Amended 2026-09-22:** most worlds hold exactly one physical wall for their whole run
  (confirmed by the client — salon on RIGHT, studio on LEFT, court's default on CENTRE), so
  only that one wall gets built from the master. **Corrected 2026-09-23:** the court's
  climax was written as spreading to all three walls at Q4→Q5, but that was never a real
  decision (`BIBLE.md` specifies one judge; see `LOOK.md` World 3 and `LOG.md`). No world
  in this production currently shows more than one wall at once, so the seam-check step has
  no live case right now.
- **"One entity across three screens" is made in the master comp**, not in Higgsfield.
  Anything that has to read as a single event across walls is built on the wide canvas.
  Generated loops carry ambient motion only.
- **Work at 1080p, upscale approved results to 4K.** The mapping software does the final
  fit.
- **Every object lives whole on one wall.** Nothing straddles a seam: no half table on
  CENTRE and half on RIGHT. Each wall is composed to stand alone and render on its own,
  while the three still read as one room. Keep hard detail about 300 mm clear of every
  edge, and nothing moves across a seam. **Only light and colour may cross** (dusk
  falling, a cloud passing), and that's done in the master comp (`STAGE.md`).
- **No people in any plate.** The actors are real. The only figure is the court's
  silhouette.
- **Transitions and fragments are made in compositing, never generated.** Higgsfield makes
  clean, lit, loopable plates. **One exception (Homie, 2026-09-24): the salon's exit**
  (`S9-SAL-R-SNUFF`) is a generated clip that ends in dusk. In all three early runs the model
  insisted on staging the snuff itself. Since v7 it is generated as a **Sequel continuation
  of the lit loop**, so the delivered file is loop + snuff in one seamless render (no
  playback involved, per the final-product rule). Anything else still goes through the comp.
- **Negative prompts are not used.** Write what should be there. Put constraints in the
  positive body.
- **The Raft painting is composited, not generated.** It's public domain (1819). Generators
  paint their own wrong version.
- **Nothing gets invented about the look.** `LOOK.md` is decided one world at a time with
  Homie, and only locked sections are used.
- **Every prompt is handed over with its settings block (Homie, 2026-09-23).** Homie
  generates from the prompt files, so a path alone is not a handover. State **model ·
  aspect ratio · resolution · duration · sound** every time, in the chat message *and* in
  the file header. Anything not yet confirmed is written as unconfirmed, never guessed —
  these are the settings he types into Higgsfield, so a wrong one costs a generation.
  Duration and sound are omitted for IMG prompts; the other three always apply.
  **Reinforced 2026-09-24:** every message about generating carries the full block (model,
  mode, reference file, aspect, resolution, duration, quality, batch, sound, prompt file),
  never "as above".
- **Regenerate rather than comp (Homie, 2026-09-24).** *"If we can do a regeneration, we'll
  just do a regeneration."* Compositing is Homie's own After Effects time, so a fix that a
  regeneration can make goes into the next prompt version. This overrode `docs/WEEK-PLAN.md`'s (retired 2026-10-02)
  "fix it in the comp" budget rule. Script prep Claude does itself (`tools/loop_halo.py`) is
  not comp work.
- **Rename on approval (Homie, 2026-09-24).** The moment an asset is approved or finished,
  rename its file to the tag without the `@` and file it. Rules are in
  `SOTR_MEDIA/README.txt` and REGISTER's naming block.
- **Claude drives Higgsfield directly (2026-09-24)** through the claude.ai connector, within
  `docs/AUTONOMOUS-GEN.md`: generation only, 1,000 credits per session, pre-flight before
  every run, measure after every run, Homie approves.

## Current stage

### 2026-11-25, latest (POST/script, PC): F28, HAND-OVER REORG DONE + S9 JUDGE F25 4K + S6 FRENCH PROMOTED. 95.2 cr (balance ~2,341.85).

- `01_FINAL_FOR_SHOW/` = the hand-over folder (one subfolder per scene, `00_READ_ME_FIRST.txt`, `_SHA256.txt`); moves in `D:\SOTR\HANDOVER_2026-11-25_moves.tsv`
  (`tools/handover_2026-11-25.py`, `--t9` on G:). Old versions in `04_WORKING_FILES/superseded/`, tests in `_DELETE_ME_2026-11-25/`. Open: b4 trim for Darren's 183-189 s cut, CLEANs for S6 FR + court.

### 2026-11-25, earlier (POST/script, PC): F25, S9 JUDGE SNAPS FIXED + S6 FRENCH SOUND MUXED + T9 SYNCED. 0 cr (balance 2,443).

- `tools/court_ext.py` env `EXT_F25=1` fixes Homie's F24 notes (judge snap 3:49, paper snap 4:01) -> `S9_GENJUDGE_3wall_review_F25.mp4` (lag 0). S6 `*_FRsound.mov`
  in `S6_4K_final/` + `S6_1080_final/`. T9 synced (sha256). Q3 (S9 upscale ~130 cr) waits for Homie's number; nothing promoted.

### 2026-11-25, earlier (POST/script, PC): FINALS4, S6 FRENCH 4K + 1080 FINALS RENDERED; S9 F24 REVIEW BUILT. 0 cr (balance 2,443).

- `04_WORKING_FILES/S6_4K_final/` + `S6_1080_final/` (`render_s6.py --final --v6 --v7 --v7-feather --v7-alpha --warm 10 --retime-fr`,
  ProRes 4444 alpha, 2910 f each, NO sound yet). The French wav mux waits: it is only on the T9, and the T9 resets (UASP). Not promoted.
  Floor files folded into the play folders (D: only; T9 not mirrored). Q3 (S9 upscale ~130 cr) waits for Homie. Handoff `docs/HANDOFF-2026-11-24-FINALS4.md`.

### 2026-11-23, latest (POST/script, PC): RAFT7, S9 RAFT WATER OPTIONS IN THE SHOW. 0 cr (balance 2,443).

- Homie: all four frame rates as options, the showrunner decides; he prefers 60. B/C/D 63 s 4K files in
  `5_FLOOR_only_if_a_floor_projector/S9_raft-water_OPTIONS_frame-rate/` (A stays default) + CLEAN loops in 03. Blades v2 style frames NEXT (0 of 60 cr).

### 2026-11-22, earlier (POST/script, PC): RAFT5, S9 RAFT WATER v2 PROMOTED + BLADES v1 BUILT. 0 cr (balance 2,443).

- `tools/raft_water.py` v2 (integer source step) = a perfect loop; promoted with Homie's yes: `5_FLOOR_only_if_a_floor_projector/S9_b1-and-b10_FLOOR_raft-water.mov`
  (4K, 63 s) + HOLD loop in folder 2 + CLEAN in 03. `tools/blade_anim.py` b10 blades test v1 in `04_WORKING_FILES/S9_raft/blades_anim_v1/`: WAITING for his notes (cap 60 cr).

### 2026-11-22, earlier (POST/script, PC): M10p, S9 JUDGE EXT5 REVIEW BUILT (Homie's notes on EXT4). 0 cr (balance 2,443).

- `tools/court_ext.py` env `EXT_E5=1` (b5 strike on his gavel sound, b7 hit then fade to black over the echo, knocks +1 frame) + `tools/s9_darren_review.py --e5`
  (eased hsin fades 0.30 s / 0.50 s into his splices, JUDGE captions on faster-whisper) -> `S9_GENJUDGE_3wall_review_EXT5.mp4` (351.17 s, lag 0), audited at 24 fps.
  WAITING for Homie/Darren; nothing upscaled or promoted.

### 2026-11-22, earlier (POST/script, PC): M10o, S9 JUDGE EXT4 REVIEW BUILT (Darren's 22 Nov cuts). 0 cr (balance 2,443).

- `tools/court_ext.py` env `EXT_D22=1` (strike at 247.0 s uncut, played through the snip; b7 snap to black at the impact) + `tools/s9_darren_review.py --d22`
  (cuts 183-189 s, 248-290 s, straight splices, Darren's sound unchanged) -> `S9_GENJUDGE_3wall_review_EXT4.mp4` (351.17 s, lag 0) in `04_WORKING_FILES/S9_gen_judge_review/`.
  S6 map-to-ship preview in `04_WORKING_FILES/S6_map_to_ship_review/`. WAITING for Homie/Darren; nothing upscaled or promoted.

### 2026-11-22, later (POST, PC): S2 PAINTING MELT APPROVED + PROMOTED to `01_FINAL_FOR_SHOW/6_NEW_S2_PAINTING_MELT_play_in_show/` (own read-me) + CLEAN copies in 03. No edge version.

### 2026-11-22, later (POST/script, PC): M10m side task, S2 MELT PLAN A MASTERS BUILT. 32 cr (balance 2,443).

- Homie: "Yes, run Plan A". 4 Topaz jobs + `tools/melt_planA.py` -> LEFT/CENTRE/RIGHT/FLOOR `_CLEAN_4K/_1080.mov` in `04_WORKING_FILES/S2_painting_melt_plan/planA/reproj/`
  (24 fps, 20.83 s, sound in, true Raft on CENTRE). Checked. WAITING for Homie; nothing promoted. Handoff `docs/HANDOFF-2026-11-22-S2melt.md`.

### 2026-11-22 (POST/script, PC): M10m side task, S2 PAINTING MELT PLAN WRITTEN. 7 cr (balance 2,475).

- `tools/melt_reproject.py` maps the 2019 Houdini 360 melt onto LEFT/CENTRE/RIGHT + FLOOR. Topaz 2160p removes the baked h264 blocks; ByteDance does not.
  Plan + brief in `04_WORKING_FILES/S2_painting_melt_plan/`: Plan A reproject + Topaz (~60 cr) recommended; Plan B regen 4 x 20 s = 1,280 cr/set. WAITING for Homie.

### 2026-11-21, late night (VID/POST, PC): M10m, S9 JUDGE EXT3 LOOK-UP REVIEW BUILT. 56 cr (balance 2,482).

- Seedance 2.5 `video_extension` forward take v16fwd (job 8d958884, `prompts/S9-CRT-IDLE.txt` v16-FWD) gives the "Order! Order!" look-up; `tools/court_ext.py` env `EXT_LOOKUP`
  splices it (U1..U185 at out 859-1043, snap exit into R149); the strike at 1278 is unchanged. EXT2 accepted by Homie as fallback, kept aside.
- b5 `*_EXT3_FULL.mp4` + `S9_GENJUDGE_3wall_review_EXT3.mp4` built in `04_WORKING_FILES/S9_gen_judge_review/`, sync lag 0. WAITING for Homie's notes;
  nothing upscaled or promoted. Handoff `docs/HANDOFF-2026-11-21-M10n.md`.

### 2026-11-21, night (POST/script, PC): M10k, S9 JUDGE EXT2 REVIEW BUILT. 0 cr (balance 2,538).

- Grip-change ramp (motion-matched) + loop-wrap ease rendered: b3/b5cut FULL/b7 `*_EXT2*` + `S9_GENJUDGE_3wall_review_EXT2.mp4` in `04_WORKING_FILES/S9_gen_judge_review/`,
  audited at 24 fps, sync vs Darren's .mov lag 0. WAITING for Homie's notes; nothing upscaled or promoted. Handoff `docs/HANDOFF-2026-11-21-M10l.md`.

### 2026-11-21, evening (VID/POST, PC): M10g, S9 JUDGE EXT REVIEW BUILT. 434 cr this meeting (balance 2,538).

- The APPROVED strike is untouched; the read before it and the return after it are Seedance 2.5 `video_extension` takes (backward/forward,
  `prompts/S9-CRT-IDLE.txt` v12-v15), joined by `tools/court_ext.py` (hold-frame drop, seam dedupe, eased ECC reframe; no morph).
  b3/b5cut/b7 + `S9_GENJUDGE_3wall_review_EXT.mp4` in `04_WORKING_FILES/S9_gen_judge_review/`, every join checked at 24 fps.
  WAITING for Homie's notes; nothing upscaled or promoted. Handoff `docs/HANDOFF-2026-11-21-M10g.md`.

### 2026-11-21, later (POST/script, PC): M10e, S9 JUDGE FLOW5 REVIEW BUILT. 0 cr (balance 2,972).

- b5 FLOW5 FULL + `S9_GENJUDGE_3wall_review_FLOW5.mp4` (399 s, Darren's uncut mix, verify lag 0) built and eyed in `04_WORKING_FILES/S9_gen_judge_review/`.
  WAITING for Homie's notes; nothing upscaled or promoted. Handoff `docs/HANDOFF-2026-11-21-M10e.md`.

### 2026-11-21 (POST/script, PC): M9z, S9 JUDGE FLOW2 REVIEW BUILT. 0 cr (balance 9.3).

- `tools/court_gen_flow.py` (WIDE: v8 silent READ, v9 wide RAISE, sdf_morph joins, drop_blobs) -> `S9_GENJUDGE_3wall_review_FLOW2.mp4` (720p, `04_WORKING_FILES/S9_gen_judge_review/`). Sheets checked. Waiting for Homie's notes on the ~0.5 s raise->strike morph. Brief `docs/BRIEF-MEETING9.md`, handoff `docs/HANDOFF-2026-11-21-M9z.md`.

### 2026-11-20, later (POST/script, PC): M9x, S9 JUDGE FLOW REVIEW BUILT. 0 cr (balance 142.3).

- `tools/court_gen_flow.py` b3 Q1 / b5cut Q2 / b7 Q4 torso (closer each appearance, Homie M9x), one size per file, no hard cuts -> `S9_GENJUDGE_3wall_review_FLOW.mp4` (720p, `04_WORKING_FILES/S9_gen_judge_review/`). Waiting for Homie's notes + his yes/no on a 105 cr READ take. Brief `docs/BRIEF-MEETING9.md`.

### 2026-11-20, late (POST/script, PC): MEETING 9, S9 JUDGE LEAN REVIEW BUILT. 0 cr (balance 142.3).

- `tools/court_gen_lean.py` built b3/b5cut/b7 + `S9_GENJUDGE_3wall_review_LEAN.mp4` (720p review, in `04_WORKING_FILES/S9_gen_judge_review/`):
  v6 READ idle under Darren's lines, look-ups on "Order! Order!" / "Get the traitors out", v7 STILL after, MIDDLE blur 0.48,
  flow-warp joins. Sheets checked. WAITING for Homie's notes; nothing upscaled, nothing in 01_FINAL_FOR_SHOW. Handoff `docs/HANDOFF-2026-11-20-M9t.md`.

### 2026-11-20 (VID/POST, PC): MEETING 9, S9 JUDGE GENERATED.

- The warp idle is rejected; the judge becomes generated Seedance 2.5 takes (`prompts/S9-CRT-IDLE.txt`: v1 probe approved, v2 idle+strike,
  v3 idle), all starting/ending on one rest pose, opaque in front of the court. A whole Scene 9 review composite at 720p
  comes first; upscale after Homie sees it. Older stages: `docs/STAGE-HISTORY.md`.

### 2026-11-17 (POST/script, PC): MEETING 8, S6 FRENCH CUT. Flag + ink stills APPROVED; review composite waits for the new audio. 0 cr.

- English out (French only). `render_s6.py --retime-fr` retimes S6 to Darrin's French track (TMAP in `docs/S6-FR-CUES.md`); v14
  bit-identical without it. RIGHT flag = white with gold fleurs-de-lis on the generated cloth (`tools/fleur_mask.py`); map dissolves
  to alpha as ink. Next: the client's French-only audio -> retime -> side-by-side WhatsApp review only (no finals). Brief
  `docs/BRIEF-MEETING8.md`, handoff `docs/HANDOFF-2026-11-17-M8l.md`.

## Session close

On `wrap`: append to `REGISTER.md` and `LOG.md`, save final prompts to `prompts/<ID>.txt`,
**update `docs/NEW-SESSION.md` → "THE TASK, RIGHT NOW,"** commit, push, **back up to the
T9**, and report what changed.

### Backing up to the T9 (documented 2026-09-23)

Homie's Samsung T9 SSD, **drive `G:`**, mirrors both folders at `G:\SOTR\HF\`. It is the
**only** protection for generated media, since `.gitignore` keeps every image and video out
of git. The repo is backed up twice over (GitHub *and* the T9); the media is backed up once.

| What | How |
|---|---|
| `SOTR_GENpipeline` | It's a **real clone of the same origin**, not a file copy. `git push` here, then `git pull` inside `G:\SOTR\HF\SOTR_GENpipeline`. Never copy files over its `.git`. |
| `SOTR_MEDIA` | Plain copy of anything new, into the matching subfolder. **Verify with a checksum**, not a file listing. |

**Copy, never mirror-delete.** The T9 already holds at least one file that no longer exists
locally (`plates/studio/loc_SOTR_studio_room_s9_v1.png`, the superseded daylight master that
`LOG.md` says to keep). A destructive sync would take it out. That asymmetry is the backup
working, not drift to be tidied away.
