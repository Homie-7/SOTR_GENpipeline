# SOTR stage history (moved out of CLAUDE.md 2026-11-20, Homie approved the trim)

Newest first. The live state is CLAUDE.md "Current stage" and docs/NEW-SESSION.md.

### 2026-11-20 (VID/POST, PC): MEETING 9, S9 judge generated, LEAN review built (M9m-M9t). Probe 35 + v3 105 + v4 35 + v5 28 + v6 140 + v7 56 cr.

- Warp idle rejected; judge is generated Seedance 2.5 takes around the approved strike. v6 READ (bc52970f) and v7 STILL (663c6da9) passed;
  `tools/court_gen_lean.py` built the lean b3/b5cut/b7 and `S9_GENJUDGE_3wall_review_LEAN.mp4` (MIDDLE blur 0.48, flow-warp joins). Review only.

### 2026-11-03, CONSOLIDATED WRAP (POST, PC): MEETING 6 IS DONE. Court 144.4 cr, gallery 0, S6 0 = 144.4 cr.

- **S9 court behind the parchment** (17 files, 4K) and **S1/S10 RIGHT gallery v6** (David's Napoleon) and **S6 v14 map** (ProRes 4444 alpha, 165 s, native 4K) are all in `01_FINAL_FOR_SHOW`, D: and T9 sha256-verified, old files in `superseded/`, repo pushed (T9 clone at the same HEAD). Nothing is open; don't change unless Homie asks. `docs/NEW-SESSION.md` has the status. Unneeded media sits in dated `_DELETE_ME_2026-11-03` bins (D:, T9, `04_WORKING_FILES/*`) for Homie to empty.

### 2026-11-03, latest (POST/script, PC): S6 v14 MAP IS FINAL IN THE SHOW. 0 cr.

- Homie approved v14. S6 show files are now ProRes 4444 with ALPHA, 165 s: v6.2 to 130 s, then the v14 map (v7 look from ~135 s), clear at the end (Sahaj's water goes underneath in the comp). 4K play, 1080 fallback, CLEAN (1080); old in `superseded/S6_v6.2_pre_v14map/`; WhatsApp 06_S6 remade. `render_s6.py --warm`. Don't change unless Homie asks.

### 2026-11-03, later (POST/script, PC): S6 v7 map FIXED for review (stills + clip sent). 0 cr.

- `render_s6.py --v7`: dark engraved ocean under the whole room (LEFT never black), thicker brighter course line (running 148.5 -> 164,
  never finishing), zoom/liquefy stretched (W0 153, M1/VID_T 164). Stills `S6_v7_map_option/stills_v9/`, clip `S6_v7_map_clip_v9_146-164.mp4`.
  v6.2 still bit-identical without --v7 (stills 100 s, 150 s). RIGHT v5 gallery show files DONE (`_tmp_*` binned to `_DELETE_ME_2026-11-03`).

### 2026-11-03 (POST/script, PC): MEETING 6 BUILT as candidates, for Homie's review. 0 cr.

- S6 v7 (`render_s6.py --v6 --v7`): per-element map->sea morph (sky/horizon/sea each their own), v6.2 unchanged. S1/S10 RIGHT =
  David's Napoleon (`gallery_rehang.py --reshape`), all files in `04_WORKING_FILES/S1_gallery/3_RIGHT_DAVID_v4/`. S9 judge
  behind paper: `tools/court_behind_paper.py`, stills + A2 clip in `S9_court_behind_paper/`. Nothing in 01_FINAL_FOR_SHOW; see
  `docs/NEW-SESSION.md`.

### 2026-11-03 (PREP, PC): MEETING 6 (31 Oct) -> three changes, planned in `docs/PLAN-MEETING6.md`. 0 cr.

- Ours (Homie): S6 map v7 across all three walls, zooming toward Senegal, the sea washing in from the sides into
  Sahaj's first frame (`05_REFERENCE_UPLOADS/S6_handoff_Sahaj/`); S1/S10 RIGHT = David's *Napoleon Crossing the Alps*;
  S9 judge behind the parchment (+ an optional smoke-figure test). Order S6, S1, S9; stills to Homie first. Not built yet.

### 2026-10-09 (VID + script + POST, MacBook): INTRO v8 + IDLES v3 (ship-free sea), built from 4K sources. 933 cr; balance 1.62.

- Idles: the still ship over a generated ship-free sea per light (`tools/s7_seaplate.py`, `s7_idle.py --world`): nothing to
  erase; 5 s loops; day's sea still drifts sideways (accepted). Intro v8: a new flight with no image reference (one ship)
  into v6's boarding from f44 (`tools/dedup_frames.py`, `s7_intro_join.py`). All six sources upscaled (ByteDance +
  `upscale_restore.py`, now `apad`). Homie rejected v7 (from astern) and v6.1 (speed-up): "we can work with this".
- Superseded ship media binned to T9 `SOTR/HF/_DELETE_ME_2026-10-09/`. **The PC's job: `docs/PC-HANDOVER-2026-10-09.md`**
  (make D: match the T9; the ship's only copy is on the T9 until then). Review list: `docs/NEW-SESSION.md`.

### 2026-10-08 (VID + script, MacBook, Higgsfield CLI): HOMIE'S TWO ROUTE-A ISSUES FIXED. 315 cr. Then a FILE CLEANUP.

- Cleanup: T9 `04_WORKING_FILES` 413 -> 4.6 GB, 412 GB in `SOTR/HF/_DELETE_ME_2026-10-08/` for Homie to empty; **the PC
  must run `tools/cleanup_2026-10-08.py --pass 2` on D:** (header) or the T9 sync copies it all back. The intro's
  landing no longer freezes the water (`s7_intro_3walls.py --trim 2 --xfade 0.25`).

- Intro v6: the boarding generated BACKWARDS from the deck canvas and played reversed (`prompts/S7-INTRO-REV.txt`),
  the flight a backward video_extension into it (`S7-INTRO-LEADIN.txt`): lands exactly on the walls, no morph. Idles v2:
  no ship pixels roll with the sea (`tools/s7_worldfill.py`, `s7_idle.py` v2). For Homie's review: `docs/NEW-SESSION.md`.

### 2026-10-07, night (IMG -> VID, Homie asleep, delegated): SIDE WALLS BUILT OUT FROM THE MASTER; new astern start frame. 48 cr IMG.

- Seams: `tools/ship_buildout.py` (guide canvas -> NBP -> registered onto the master's true pixels), states re-made,
  `tools/ship_skymatch.py`; **current walls = T9 `S7_ship/3_walls/seamed_v2/`** (PROVISIONAL). Intro start frame
  `2_intro/S7-INTRO-F1-ASTERN_v1_34a41ccb_haze.png`. The VID redo sub-agent was unfinished at wrap: MORNING REVIEW in `docs/NEW-SESSION.md`.

### 2026-10-06, day (IMG/script, MacBook): Homie APPROVED the ship's 5 light states; REJECTED the intro; walls re-made as ONE scene.

- His note "a complete cohesive single scene, they all need to align" -> `tools/ship_seams.py`: rails meet at both seams,
  sky/sea matched to CENTRE; **current walls = T9 `S7_ship/3_walls/seamed_v1/`**. Intro redo = a VID session from
  `docs/VID-BRIEF-S7-INTRO-v2.md` (real wingbeats, distance changing, from astern, ending ON the deck plate). 0 cr.

### 2026-10-06, overnight (IMG -> VID by a fresh sub-agent, Homie asleep, delegated): THE SHIP SEQUENCE's states + the intro. 450 cr.

- IMG (36 cr): NIGHT, MAGIC HOUR (Louise's Charente sky: one full moon), WRECK, layers; every state warped onto the day walls
  (new `tools/ship_align.py`, `ship_states.py`: NBP had reframed CENTRE edits by up to 16%). VID (414 cr): the intro flight +
  landing Sequel, review cut in T9 `S7_ship/4_intro_video/`. ALL PROVISIONAL: Homie's review list is at the top of
  `docs/NEW-SESSION.md` (lead issue: the video's gilded ship vs our red-ochre deck walls).

### 2026-10-05, latest (POST, MacBook): SCENES 1 + 10 DONE AND IN 01_FINAL_FOR_SHOW. The client upload is complete. 6 cr.

- Promoted by `tools/promote_gallery_2026-10-05.py` (19 show files sha256-verified): the gallery's 9 show files in
  `1_PLAY_THESE_IN_ORDER/`, 6 4K loops in `2_BACKUP_LOOPS_for_operator/`, 4 floor files (the puddle FLOW) in folder 5.
  Next (docs/NEW-SESSION.md): IMG, the surprise scene (Scene 8); the PC to sync S1 from the T9.

### 2026-10-05 (POST, MacBook): THE GALLERY SHOW FILES APPROVED (Homie: "we can call it finished").

- Homie: paintings centred on every wall (`tools/gallery_rehang.py`, LIT/DARK v3); "full length at 1080 only", 4K as 32 s
  backup loops (`tools/gallery_show.py`: tour 15:00, blackout bank by bank + dark 5:00, S10 5:00). In
  `04_WORKING_FILES/S1_gallery/3_SHOW_FILES_1080_for_review/`, NOT yet in 01_FINAL_FOR_SHOW (file management later).
- The puddle: his notes done by script (`puddle_comp.py --flow-from --debubble`), awaiting him. T9 = full client delivery.

### 2026-10-05 (VID, MacBook): THE PUDDLE RETURN on the dark floor, composited (v6), AWAITING HOMIE. 216 cr.

- Seedance v4 (dome), v5 (flat film), v6 10 s: drops, a pause, it spreads by itself, but overshoots off the frame (3rd time =
  structural): the stop is scripted (`puddle_comp.py --end 6.8 --ease-src 0.6 --hold`, + the glimmer). Review in
  `04_WORKING_FILES/S1_gallery/2_PUDDLE_RETURN_in_progress/`. Open: Homie's verdict, incl. the pool's ROUND shape (~1.25 m).
- `puddle_comp` got a dark-wood noise floor (its fixed threshold read 10% of dry dark oak as water); new `tools/puddle_measure.py`.

### 2026-10-05 (files): HANDOVER REORG. Scenes 4 + 5 are IN the show folder; the gallery is NOT done yet.

- Homie asked for production-ready files. `01_FINAL_FOR_SHOW` now holds S4 + S5 (Rich dusk plays; Cold dusk in
  `4_CLIENT_OPTION_S5_cold_dusk/`; floors in `5_FLOOR_only_if_a_floor_projector/`) beside S6 + S9. The gallery's working
  folder is split (`1_READY_for_show_build/`, `2_PUDDLE_RETURN_in_progress/`, `00_STATUS_READ_ME.txt`). Unused takes in
  `T9/SOTR/HF/_DELETE_ME_2026-10-05/`. `tools/reorg_2026-10-05.py`; **the PC runs it on D: next time** (REGISTER).
- **The puddle return and the gallery show files are still to make** (VID, then POST).

### 2026-10-05, late (IMG, MacBook): THE NEW GALLERY FLOOR = dark oak Versailles parquet (a650a2ac). 8 cr.

- Homie picked option A; "I'm happy with the floor". His worry, the baked reflections, is handled by new `tools/floor_desheen.py`
  (glare subtracted; the plate every tool builds from is `floor/S1-GAL-FLOOR_v2_a650a2ac_desheen.png`). The drawn spill reads on
  dark oak by its reflections (`gallery_floor.py --wet-gain 2.5`). The Seedance patch is recut from it (`05_REFERENCE_UPLOADS/`).
- **The drawn VANISH rebuilt and APPROVED** (Homie: v1's even shrink was "a cheap animation scaling back"; v2 "Yep, I like it"):
  `gallery_floor.py --vanish dewet --vanish-s 3.5` (frays, holes, islands, a damp ghost). The teal glimmer stays on the RETURN only.
- **Homie: keep enough credits for ALL the gallery's video generations and upscales** (+ 500 at the week's end).
- **Next (docs/NEW-SESSION.md): VID, the puddle returns on the new floor; then POST, the gallery show files.**

### 2026-10-05, evening (VID, MacBook): THE PUDDLE RETURN tried 3 ways; Homie's TEAL EDGE GLIMMER (script) OK'd. 276 cr.

- Generated water on a close floor patch, composited by new `tools/puddle_comp.py`. v2's drops read as rain and v3's whole-pool
  teal read as gel: both rejected. Agreed: 2-3 drops, then it wells up by itself and lies still; the glow = a subtle teal
  glimmer on the waterline only (`--glimmer`, lit + blackout), "I think it's fine". Homie: "the gallery takes precedence".
- **Next (docs/NEW-SESSION.md): IMG a darker gallery floor** (pale oak = "cheap townhouse"; rec. dark oak parquet), **then VID
  the new water on it, and POST the gallery show files.**

### 2026-10-05 (IMG, MacBook): SCENES 1+10, THE LOUVRE GALLERY, built (walls LIT + DARK, floor + puddle). 64 cr.

- New add-on (Homie): one build serves Scene 1 and 10; CENTRE = the Raft, LEFT = Louis XVI + Marie-Antoinette, RIGHT =
  Napoléon; real public-domain paintings pinned by script; ONE room light across all walls (Homie: "cohesive as a single
  space"); the floor + the puddle on the script's beats. Homie: "Gallery seems to be alright". Media on the T9 only.
- Next (docs/NEW-SESSION.md): a VID session for a hyper-real dripping/building puddle; then the surprise scene (rec. 8).
- Mac tools: `tools/gallery_wall.py`, `gallery_floor.py`, `gallery_dark.py`. Leave 500 credits at the end (Homie).

### 2026-10-04, evening (POST): Scenes 4 and 5 DONE. Camps PRIMARY = rich dusk, SECONDARY = Cold dusk (client picks).

- Alps A4 approved. Camps: Front ground flicker fixed (`tools/deflicker_ground.py`), a carved-plume sky-mask defect fixed
  (v5 masks); Homie: "can we consider the camps fully done?" Cold dusk (C2) renders unattended, then T9 + shutdown.
- **Homie: "Just make the things that I asked you to make"**: no unrequested upscales or show-folder changes (memory).

### 2026-10-04, day (POST): S6 v6.2 IS THE SHOW (4K). Alps A4 + camps N rendered; the camps birds removed. 40.08 cr.

- **Scene 6 v6.2 replaced v5** under the same names (4K play, 1080 fallback, CLEAN); v5 in `superseded/S6_v5/`. ByteDance
  timed out on the 165 s walls (refunded): **clips over ~2 min are upscaled in two overlapping halves**, joined, restored.
- Alps (A4) and camps (N) done, for Homie with H.264 review copies. **Camps birds removed** by `tools/debird.py` (Homie:
  the near circling ones; far dots and birds crossing smoke/cloud stay). Next: Homie's review, then S4/S5 as show files.

### 2026-10-04, morning (POST): Homie's verdicts. S6 v6.2 REPLACES v5; studio canvas edge APPROVED; Alps = 050422 renders, natural grade; camps = RICH DUSK.

- C (cold dusk) was "extremely dull"; the camps go to option N (only the red soil turns to earth), exposure matched 100%
  across all four angles ("imperative"). The Alps switch to the clean `Renders (050422)` set. Renders running; the
  S6 4K + promotion is next. Full handover: `docs/NEW-SESSION.md`.

### 2026-10-03, night (VID -> POST, Homie asleep, delegated): S6 v6.2, the studio canvas edge IN THE SHOW, S5 + S4 graded. 19.29 cr.

- S6 v6.2: the CENTRE flag tears into ragged scraps (Homie: v6.1 was "office paper through a shredder"). Option beside v5.
- Scene 9 studio: `edge_flow.py --canvas-edge` (ragged plaster lip + canvas edge in shadow), promoted 4K + 1080 under the
  same names; old in `superseded/studio_pre_canvas_edge/`. S5 camps: C + `grade_battlefield.py match`. S4 Alps: S4 (C's
  stock in daylight) + match + Despeck, from `New Renders/Alps` (to confirm with Homie, and what "the birds" are).
  Review list: `docs/NEW-SESSION.md`. If everything finishes before he's back: wrap, T9, then shut the PC down (Homie).

### 2026-10-03, third part (VID): SCENE 6 v6 = THE FLAG OPTION, BESIDE v5 (both go to the client). 48 cr.

- Homie: "don't overwrite anything… the second version… present both". `render_s6.py --v6` (v5 bit-identical without it):
  A worn cloth (script), B M4 as faded coloured light on linen, C M6 = the colours drain/flood back/drain (1814-1815),
  then CENTRE dark, RIGHT the white flag, LEFT a tricolour cut into pieces. `--check` clean.
- Files only in `04_WORKING_FILES/`: `S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4` (for the client), `S6_v6_option/`
  (1080 show files). The Edit-video wear (S6-FLAG-WORN v1, 48 cr) failed on look (slit holes like mouths): not used,
  the 360-cr pass not run. **Homie approved the v6 design (3 Oct, late) with 3 notes** (reveal glitch, centre exit to
  shreds, Napoléonistes rethink): `docs/NEW-SESSION.md`. Scene 5: grade options on the REAL renders, Claude recommends C.

### 2026-10-03, second part: MEETING 4 NOTES -> `docs/PLAN-MEETING4.md`. Flags first (1,000 cr today, conservative).

- Client: the Scene 6 flags too strong/graphic; soften, weather them, show the monarchist/Napoleonic instability
  (researched: the tricolour holds the king's white; white 1814, tricolour 1815, white 1815-30; flags cut up and
  burned; the White Terror = why Agnès leaves). Then the Alps (remove "birds") and the battlefield grade (too red),
  Homie's 2022 Unreal renders on F:. Floor plan parked. Nothing generated before Homie picks the flag concept.

### 2026-10-03 (PREP): a floor-projection plan, ready in case it's needed.

- A floor projector is NOT confirmed. If it is, `docs/FLOOR-PLAN.md` is the plan: floor as floor (light pools,
  the judge's shadow, smoke, ash, the Scene 6 route + sea), top-down, no pre-warp, the mapping guy fits it; 19 extra
  files, nothing approved changes. Homie: judge's shadow YES, carpet OUT, scratch sound only (sound designer).

### 2026-10-02, second part (POST): FULL CLEANUP + NEW FOLDER LAYOUT. Upload `01_FINAL_FOR_SHOW/` to the client.

- Homie: "Delete everything unnecessary… do a full project cleanup, recompartmentalize everything… which folder do I
  need to upload to the client". **`SOTR_MEDIA` 117 GB + 96 GB archive -> 80 GB**, same on the T9 (272 -> 80 GB).
  New layout in the Folders rule above. Unneeded media in `_DELETE_ME_2026-10-02\` on both drives (D: 134 GB,
  T9 193 GB) for Homie to empty (Claude doesn't hard-delete). Kept set sha256-identical on D: and the T9.
- Repo: retired tools (render_s6 v1-v3, break_strip, fracture_edge_proto, make_client_pdf, reorg scripts),
  prompts for retired walls / rejected takes, and finished plans removed (in git history). `render_s6.py` reads
  Scene 6's loops from `02_APPROVED_BUILDING_BLOCKS/S6_generated/`. Script: `tools/cleanup_2026-10-02.py`.

### 2026-10-02 (POST): FINISHED. T9 backup complete; Homie is taking it to the client.

- Homie: "I think we'll call it finished." Nothing changes unless he comes back with client notes.
- **T9 fully in line with D:** show folder by `promote_4k.py --t9-only` (0 mismatches), then every other new or changed
  media file (124, 37 GB, sha256; the T9's older copies kept in `superseded/t9_replaced_2026-10-02/`). All 21 show and
  backup files probed: 4K ProRes HQ, 24 fps, sound. 0 credits. Details: `LOG.md` 2026-10-02.

### 2026-10-01 (POST): SCENES 6 AND 9 DONE, THE SHOW FOLDER IS 4K (07:57). T9 sync pending (drive away).

- **The PC hard-crashes under all-core load** (WHEA 18, CPU Core 7; 00:58 and 05:14 today, also in August). Every heavy
  job now runs with **affinity FFFF3FFF** (off Core 7) and writes to `_tmp_` names (memory: pc-core7-crash).
- **4K layout (Homie delegated), DONE:** folders 1 (play) and 2 (backup loops) of `01_FINAL_FOR_SHOW` are 4K under the
  same names; their 1080 files are in `01_FINAL_FOR_SHOW/4_HD_1080_same_files/`. By `upscale_4k/promote_4k.py`, gated on
  every `upscale_check.py` VERDICT. 81.30 credits today (59.35 of them expiring bonus credits).
- **Studio candle arc:** v4 withdrawn (floor under the wall: the long takes came back reframed), v5 fixed by
  `tools/plate_align.py`. Homie: b9 v5 approved (in the show), b6 stays v3 (v5 "feels more like the exposure going up and
  down"). `3_CLEAN_no_edge` stays 1080 ("the only files that matter are the ones that will be in the show").
  Handover: `docs/NEW-SESSION.md` (first job when the T9 is back: `promote_4k.py --t9-only`).

### 2026-09-30, fourth part (POST/VID): Scene 9 at 4K, the studio candle arc, pipeline v3 adopted, overnight 4K render.

- **Scene 9 at 4K:** all 8 show files upscaled (ByteDance + `upscale_restore.py --clamp 2`), in
  `03_TESTS_IN_PROGRESS/upscale_4k/`; the approved 1080 files untouched. Checked ones are faithful (flicker, motion,
  sound identical). **Found: this network intercepts DNS**; downloads only via `tools/fetch.py` (memory).
- **Studio candle arc (LOOK D6) built as v4** (not yet approved): beat 6 flares (a generated 10 s take), beat 9 steady
  and brightest (a 30 s take calmed + lifted by script). `render_studio.py --primer-from` keeps one light scale.
- **Pipeline v3 adopted forward only** (standing rules above). **Overnight:** Scene 6 at 4K + T9 backup
  (`OVERNIGHT_2026-09-30.sh`). Credits today 1,849.

### 2026-09-30, third part (VID): SCENE 6 APPROVED (v5) and filed. 4K upscale route chosen.

- **Scene 6 v5 approved** (Homie: "It's looking fantastic… no complaints"). Show files
  `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_LEFT/CENTRE/RIGHT_wars.mov` (start all three together) + `_CLEAN`
  copies; README updated; v4 in `03_TESTS_IN_PROGRESS/superseded/S6_final_v4/`. Don't change Scene 6 unless Homie asks.
- **4K route (Claude's call, Homie delegated):** ByteDance video upscale "aigc" 4k, then `tools/upscale_restore.py`
  (the upscale's fine detail + the approved source's light and motion). Topaz ticks every 1.25 s (keyframes);
  ByteDance alone damps the flicker. ~0.08 credits per second. Stills: ByteDance (the only option).
- **Every ProRes encode now uses `-qscale:v 2`** (the default rate adds frame-to-frame shimmer). **Downloads go
  through `tools/fetch.py`** (the CDN truncates files that still probe fine).
- **Credits today: Homie raised the cap to 2,000 for 2026-09-30, no per-run ask.** Spent this part: 10.4.
- **The Scene 6 4K render runs when Homie goes to sleep** (his words), ~4 h at full load.

### 2026-09-30, second part (VID): Scene 6 show files v4 rendered, Homie "almost perfect"; v5 rendering.

- Sequels checked (PASS), loops built, `S6_final/` v4 = three full-HD ProRes files with sound. Homie's five notes
  and the answers are the last block of `LOOK.md` Scene 6; v5 (bigger subject-centred prints, flakes behind the
  pictures, the tear riding the cloth in two fluttering pieces) renders to `03_TESTS_IN_PROGRESS/S6_final_v5/`.
  0 credits this part. Next steps: `docs/NEW-SESSION.md`.
- **Long renders run DETACHED** (`nohup … &`): a background shell with a timeout can kill a 60-minute render.

### 2026-09-30 (VID): Scene 6 animatic APPROVED; generated flag + smoke; the final render is set up.

- **Animatic v4 approved by Homie**, checked line by line against the script (no deviations); `LOOK.md` Scene 6 LOCKED.
- **Generated (864 credits this session, balance ~4,290):** S6-FLAG v1 (take A chosen) + a 30 s Sequel; S6-SMOKE v1 +
  a 30 s Sequel. `render_s6.py` now carries them (`GenFlag`, `GenSmoke`, `LoopReader`), `tools/s6_loops.py` loops
  them, and `--final` writes `S6_LEFT/CENTRE/RIGHT.mov` (full HD ProRes 422 HQ + the clips' sound). Tested on 4 s: works.
- **At wrap the two 30 s takes were still downloading** (the CDN connection kept failing TLS handshakes). Next steps:
  `docs/NEW-SESSION.md`. Upscaling is parked (Homie: later). The pipeline v3 update is parked until Scene 6 is approved.

### 2026-09-28, fourth part (PREP): Scene 6 animatic v4 built, for Homie's review.

- Homie on v3: "near perfect". v4 = one burn front across all three walls (`RoomBurn`: no wall burns
  ahead of its neighbour, no hard edge at a seam), the flag rips from the middle, a wider map of Africa.
  `S6-ANIMATIC_v4.mp4`; `--check` clean. 0 credits.

### 2026-09-28, third part (PREP): Scene 6 animatic v3 built, for Homie's review.

- `S6-ANIMATIC_v3.mp4` answers Homie's five v2 notes (`LOOK.md` Scene 6, "What v3 does"). New in
  `tools/render_s6.py`: ClothFlag, PaperBurn + Ash, MapJourney, and `--check` (overlap measured, clean). 0 credits.

### 2026-09-28, second part (PREP): Scene 6 started. Animatic v2 reviewed; v3 next.

- **Client notes (via Homie):** Scene 6 is a movement scene with fragmented spoken word; float imagery
  over it (maps of Africa, the French flag, people fleeing). It's Homie's; the script calls it "The
  Napoleonic Wars" (`BIBLE.md` Scene 6). Built as an animatic first, by script, 0 credits:
  `tools/render_s6.py`, sources in `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/S6_public_domain/`.
- **Homie's decisions:** Goya's etchings for the fleeing people (no stick figures, no photos), era 1816,
  all three walls, no framed/rectangular pictures anywhere, objects never straddle a seam.
- **Next: v3** from Homie's five notes (end of `LOOK.md` Scene 6). Handover: `docs/NEW-SESSION.md`.

### 2026-09-28: SCENE 9 APPROVED by Homie. Next: other scenes, or feedback on 9.

- **Every Scene 9 show file is approved** ("All of these files have been approved. Good work.").
  Don't change any of it unless Homie asks. The show folder is `SOTR_MEDIA/01_FINAL_FOR_SHOW/`
  (play `1_PLAY_THESE_IN_ORDER/` top to bottom); `REGISTER.md` maps each file to its version.
- **Last changes before approval (2026-09-26):** the frozen smoke in the salon's dusk hold removed
  (`tools/clean_hold.py`, every other frame bit-identical), and the show folder reorganised around
  the script. Meeting one-pager: `SOTR_MEDIA/06_PRESENTATIONS/`.
- **Credits:** 48 across the 25-28 September sessions (one failed court take). Balance ~3,154.
- The Scene 9 open items (set dimensions, codec, pre-warp, rehearsal timings, the studio candle arc)
  wait on the team and Homie; see `docs/NEW-SESSION.md`.

### 2026-09-25, fourth session (VID): v3, the edge flows one way, the Raft is painted in strokes, the court burns.

- **No more ping-pong** (Homie: "a cheap reverse loop"). `tools/edge_flow.py` freezes each generated
  broken edge and sends its blocks drifting off one way, forever; `break_strip.py` is retired.
- **Studio v3:** brushstroke painting (`render_studio.py --strokes`); the canvas never breaks.
- **Court:** the paper screen burns away (`tools/court_burn.py`); torn paper and cubes both rejected.
  Materials break the way they really would (`LOOK.md` D16).
- **Credits: 48 this session** (one court Edit-video take, failed, unused). Homie presents on
  2026-09-26 and needs credits for feedback and other scenes.

### 2026-09-25, third session (VID): Scene 9 delivered as v2, with sound and the edge on every wall.

- **Show files v2** in `SOTR_MEDIA/01_FINAL_FOR_SHOW/`: every file carries its generated **sound**
  (`build_audio.py`); **the files that play are `with_edge_effect/`**, the fragment edge on the
  whole time (`LOOK.md` D15). The court = the approved strike on the new **lit-scrim field**.
- **Salon break = an Edit-video pass (v5 B)**, laid on by `break_strip.py` (D14). **Studio break =
  S9-STU-L-BREAK v1**, the canvas protected. **Court** = torn paper by script.
- **Rejected by Homie:** the new strikes (B3/B5) and the reading loop's use; one judge confirmed.
- **Credits: 1,080 in the day; ~660 bought nothing.** Homie: unacceptable. New standing rule
  (Credits, above). Nothing deleted: old/silent files are in `03_TESTS_IN_PROGRESS/superseded/`.

### 2026-09-24, second session (VID): every wall has finished clean files; the fragment edge is found.

- **Homie delegated all remaining decisions** ("just make decisions"): `LOOK.md` D1-D10 (beat
  lengths from the script, delivery format, the studio's painting stages per the script, the
  court never fragments, the Q5 capper is in, Claude builds the composites).
- **Finished clean files for all three walls** in `SOTR_MEDIA/01_FINAL_FOR_SHOW/<wall>/`: salon b2-3,
  b8 and IN/HOLD/OUT; studio b4/b6/b9 with the Raft growing; court b3/b5/b7 and strikes.
  Tools: `render_wall.py`, `render_studio.py`, `render_court.py`.
- **Fragment edge = Control-style floating blocks along the whole inner side** (Homie's art
  direction). Higgsfield can do it: wither v3 A has the look but dropped Gérard and drifted
  the framing; next is the same wording as a Sequel from the loop. Effects only in `01_FINAL_FOR_SHOW/<wall>/with_edge_effect/`.
- **960 of 1,000 credits spent.** The connector works; `PIPELINE.md` has its map and traps.

### 2026-09-24 (VID) — Salon loop approved. Studio loop works. Snuff on v3. Higgsfield connected for Claude.

- **`@loc_SOTR_salon_R_loop_s9_v1` approved.** Its halo flicker is boosted 3x by script
  (the generated halos breathed ~2-3%, too little to read from the seats). The comp file
  is `02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_loop_s9_v1_comp.mov`.
- **Studio loop v2 works but isn't approved yet** (`loops/S9-STU-L-LOOP_v2.mp4`). v1 came back
  still, because its prompt was full of calming words. v2 asks for a candle guttering in a
  draught, and the light swing went from 4% to 17%.
- **`S9-SAL-R-SNUFF` added** (Homie): smoke from the snuffed wicks, for both salon exits.
  v1's snuff was good but its smoke became cartoon clouds. v2 rewrote too much and lost the
  snuff. v3 still made puff-headed smoke. **Restructured to v4 with Homie**: the clip is the
  exit itself, from the lit plate (see the transitions exception in Standing rules). Written, not run.
- **Look decisions** (LOOK.md Worlds 1 and 2): on the salon wall the halos breathe, and the
  mirror and curtains are gone; the studio's light follows the drama across beats 4/6/9; the
  painting grows while Géricault paints (pending the director).
- **Seedance 2.5 menu captured** (`PIPELINE.md`): there's no end-frame slot, so loops close with
  a crossfade (`tools/loop_halo.py`). 4:3 at 1080p gives 1664x1248.
- **Media renamed and filed**: no `@` in filenames, rejects in `04_REJECTED/`. The studio room
  master is **retagged v2** (the daylight one is the real v1); the rename map is in `LOG.md`.
- **The Higgsfield connector** was added by Homie. It loads in the next session, which starts with the
  connector gate in `docs/AUTONOMOUS-GEN.md`.
- **Found:** the client PDF has been stale since 2026-09-21. Don't send it until it's rebuilt.

### 2026-09-23 (VID) — The court strike is approved. Only the two loops are left to generate.

`@fig_SOTR_judge_strike_s9_v1` approved from `prompts/S9-CRT-STRIKE.txt` v3, on **Seedance
2.5** (image-to-video from the approved still, 9:16 → 1080x1920, 24 fps, 4.04 s, HEVC
10-bit). **The strike comes TOWARD CAMERA, not downward** — decided with Homie after two
downward versions failed for one structural reason: a gavel strike is a movement in depth
onto a bench, and this design has neither, so "down" could only mean down across the body,
where a second black shape on a one-tone silhouette stops existing.

Two things about this asset that a later session will otherwise get wrong. **It carries a
sanctioned white keyline** around the gavel where it overlaps the figure — a deliberate
carve-out in `LOOK.md` World 3, not the banned incidental white, and **it is not
reproducible from the v3 prompt string, which bans it** (trap warning at the top of the
prompt file). And **the epaulette fringe comes back as white hatching** — that one *is* the
old banned defect, flagged for a tracked comp patch, not a regeneration.

**Q5 needs no separate generation** — the capper is further along the same travel. Its
enlargement is **reduced, not gone** (corrected 2026-09-24): measured at 3.2× working and
6.4× at 4K for the gavel to fill the wall, a fraction of enlarging the raised-pose gavel,
and a thresholded two-tone shape survives it far better than video. The vector trace stays
as the fallback. The capper itself is still unconfirmed with Homie — it isn't in the script.

**Vertical vs horizontal, settled 2026-09-24 by measurement, not argument.** Homie asked
whether the 9:16 source would run out of frame as the comp zooms in. Every one of the 97
frames was measured. The figure never touches the left edge and only briefly the right;
where it does leave the frame is **top and bottom** — because a man lunging toward camera
grows up and down, not sideways. A horizontal frame would add room where none is needed,
remove it where it is, and cost ~44% of the linear resolution on the figure exactly at the
zoom cues. See `LOOK.md` World 3 step 3 for the floor-line placement rule that hides the
leg, and `REGISTER.md` for the two small paint jobs.

**What's left to generate: `S9-SAL-R-LOOP` and `S9-STU-L-LOOP`.** Neither prompt is
written. Everything else outstanding is compositing.

### 2026-09-23 — All six IMG assets for this scope approved. Next: compositing, then a VID session for loops and the court strike.

**Studio room master regenerated under night/candlelight and approved** (var 1 of 4),
superseding the 2026-09-22 daylight approval. Both wall plates then ran and are approved:
`@loc_SOTR_salon_R_s9_v1` and `@loc_SOTR_studio_L_s9_v1` (the latter needed a crop fix —
floor was visible below the canvas's support blocks in every generated variant; fixed by
trimming the frame to the skirting line, not regenerating). `@loc_SOTR_salon_R_dark_s9_v1`
(the NBP edit for the salon's unlit state) is also approved, with one flagged non-blocking
deviation: the dusk light reads slightly brighter on the wrong edge, treated as
comp-correctable rather than a blocker. Full checklist each asset was judged against, and
what's flagged as known-but-accepted, is in `REGISTER.md`'s 2026-09-23 entries.

**IMG generation work for the confirmed scope is done.** What's left is compositing
(the Gérard portrait onto the salon frame, the Raft painting's three stages onto the
studio canvas — see `REGISTER.md`'s Composited cues) and a separate VID session for the
two loops and `S9-CRT-STRIKE`.

### 2026-09-22 — Wall assignment CONFIRMED. Scope cut from 6 wall plates to 2. Judge and salon room master approved; studio room master needs regenerating.

**The client confirmed the beat map** (audience-perspective): salon on RIGHT, studio on
LEFT, the judge on CENTRE ("the back screen"), the raft a physical floor riser (out of
scope, `BIBLE.md`). Combined with `LOOK.md`'s pre-existing "solo wall" design for the
salon, this collapsed each world to **one confirmed wall** instead of three — see
`SHOTCARDS.md`'s beat table and `LOG.md` 2026-09-22 for the full reasoning.

`@fig_SOTR_judge_s9_v1` approved, comp fix done. `@loc_SOTR_salon_room_s9_v1` approved.
**Active wall prompts are now `prompts/S9-SAL-R.txt` and `prompts/S9-STU-L.txt`** — the
old L/C/R-per-world set is retired (removed 2026-10-02; in git history).

**One thing still blocks the studio:** `@loc_SOTR_studio_room_s9_v1` is **superseded** —
the light changed from daylight to night/candlelight (see `LOG.md`) — and must be
regenerated from `prompts/S9-STU-ROOM.txt` v3 and re-approved before `S9-STU-L` can run.
The salon has no equivalent block; `S9-SAL-R` is ready now. The rest of this paragraph is
the 2026-09-21 state and still holds.

### 2026-09-21 — All three looks LOCKED. Cards and IMG prompts written.

Scope: **Court Martial, Salon, Géricault's studio** (Scene 9), deadline about a week from
21/09. `LOOK.md` is locked for all three worlds, `SHOTCARDS.md` has the cards, and
`prompts/` has every IMG prompt. **Next: IMG. Homie playtests the prompts and brings the
results back to review, log and iterate.** Loops and the court strike come later, in a VID
session. Homie's standing preference: the worlds are ours to shape, not literal copies.
The Windows PC handover (`docs/HANDOVER-WINDOWS.md`) is done and was retired 2026-10-02.

