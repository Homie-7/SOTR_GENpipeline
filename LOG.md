# LOG — SOTR

One row per generation. Change one thing at a time. After 15–20 attempts on one plate,
change the plate, not the sentence.

| Date | ID | v | Model | Changed | Verdict | Note |
|---|---|---|---|---|---|---|
| 2026-09-26 | S9-SAL-R (dusk hold) | v3 | no generation | **Homie: after the snuff "the smoke is kind of stuck on that frame"** (the dusk hold froze the snuff clip's last frame, wisps and all: 35 s in b2-3 from 1:22, 3 s in b8). "Make sure everything else remains exactly how it is" | **FIXED, nothing else touched** | `tools/clean_hold.py`: a smoke-free dusk plate (10th percentile over the settled frames, both sconces out), the last 36 snuff frames dissolve into it while the smoke still moves, the hold = the plate. Frames before the dissolve are STREAM-COPIED (framemd5: b2-3 first 1,941 and b8 first 277 bit-identical; audio MD5 identical); the edge files splice the old edge2b head onto a tail rendered with the same flow timeline (`--start --t0`), blocks drift as before. Clean `_v3` + `_v3_edge2b`; v2 in `superseded/salon_v2_frozen_smoke/`. |
| 2026-09-25 | S9-CRT (edge) | v3b | no generation | **Homie: the burn "still looks pretty fake and low-poly-ish"** | **REBUILT** | `court_burn.py` v2: burn line warped by 2D fractal noise (lacy, not a per-row sawtooth), brown scorch + black char crust of varying width + pale ash lip, glow as a thin line with crawling hot spots and veins in the char, soft textured tumbling ash, sparks with trails, faint rising smoke, bloom on the bands only (0.57 s/frame). All 7 court files re-rendered `_edge3b`; the first burn in `superseded/court_burn_v1/`. |
| 2026-09-25 | S9-SAL-R (edge smoke) | edge2b | no generation | **Homie: the snuff smoke disappears in the broken area** (the break shows a frozen wall + the void) | **FIXED** | `edge_flow.py render --smoke-at N`: the smoke is pulled from the clean file (per-pixel min over +-18 f = the wall, the excess high-passed = smoke) and laid over the break, 2x in the void so it reads on black. Outside the snuff the files are bit-identical to edge2 (checked). b2-3 (--smoke-at 1857), b8 (193), OUT (0) as `_edge2b`; the smokeless ones in `superseded/salon_edge2_nosmoke/`. |
| 2026-09-25 | S9-STU-L (backups) | v3 | no generation | **Homie: "Studio only has two… the other two have three"** = the studio had no `backup_pieces` (D2 asked for them on every wall) | **ADDED** | HOLD-b4/b6/b9: the painting at each beat's end stage over 4 candle cycles (772 f = 32 s, loop join = a normal frame step), clean + `_edge2` (flow `--period 772`), sound from the studio_b6 recipe. |
| 2026-09-25 | (report) | — | — | Homie asked for a meeting brief | **PUBLISHED** | https://claude.ai/artifact/5X9sjRSukpoDc1vhdrmhf9 (copy `docs/MEETING-BRIEF-2026-09-26.html`) |
| 2026-09-25 | (all walls) edge v2/v3 | — | no generation | **Homie on the v2 edge files: "they're looping forwards and backwards… it looks like a cheap reverse loop"** (break_strip.py ping-ponged a 4 s break) | **FIXED: one-way flow, all walls** | `tools/edge_flow.py` (new): the generated break's FRONT is frozen (per-pixel median/min: the edge and cracks, blocks removed) and its BLOCKS are cut out as sprites; a deterministic conveyor sends blocks out from behind the edge, drifting outward, turning, receding and fading, new ones always coming, never reversing. `--period` makes it exactly cyclic (salon HOLD now 772 f = 32 s, joins measured < 1/255 step). Refactor regression: 0 difference. Salon + studio `_edge2` files in `01_FINAL_FOR_SHOW`, v2 edge files to `superseded/edge_v2_pingpong/`. |
| 2026-09-25 | S9-STU-L (painting) | v3 | no generation | **Homie: the painting should fill "as brushstrokes", not an opacity fill** | **DONE** | `render_studio.py --strokes 3000`: seeded brushstrokes along the painting's forms (structure tensor), bristles, dry tail, wet sheen; paint order kept (apex last); beats join exactly. First pass read as pencil rods; widened (w 0.32-0.48 L) and softened. Clean `_v3` + `_v3_edge2` in `LEFT_wall_STUDIO`. |
| 2026-09-25 | S9-STU-L canvas chips | — | no generation | Homie asked whether the canvas should fragment too, then: "if cracking the painting canvas is becoming too much of an issue… I'm not a fan of this cube brick-like disintegration… the painting canvas is not [a physical space] so it should not be breaking like that" | **DROPPED** | `edge_flow.py chips` built (stepped notches + live canvas pieces) and abandoned; the canvas stays whole. Kept in the tool, unused. |
| 2026-09-25 | S9-CRT-BREAK | 1 | Seedance 2.5, **Edit video** on 4 s of the scrim field without the judge (`05_REFERENCE_UPLOADS/CRT-C-field_4s_upload.mp4`, media 8c5030b8…, 1800 stretched to 1920), 1080p, high, **batch 1**, sound on. **48 credits (session total 48)** | new prompt: the studio break body, wall words changed, both sides, band ~1/10 | **FAIL (look); nothing usable shipped** | The model REFRAMED: narrowed the screen to a hard-edged rectangle in a dark room with two neat stacks of clean cubes. Cubes were cut out as sprites + a script-built stepped block front (`edge_flow.py kit-court`): Homie rejected the cube/brick language for a paper screen. File `edge_break_tests/S9-CRT-BREAK_v1.mp4` (b245e341…). |
| 2026-09-25 | S9-CRT (edge) | v3 | no generation | **Homie chose "paper that burns away"** (my recommendation; options were burn / light failing / no edge) | **DONE** | `tools/court_burn.py`: an irregular char line creeping inward one way over beats 3→5→7 (5%→9% per side, shared timeline via --t0), scorch band, crawling ember rim, ash flakes that cool from ember to grey drifting out and up; judge laid on top (never burns), shudder moves all. `render_court.py --scrim --burn`, sound by build_audio. `_edge3` files. |
| 2026-09-25 | S9-STU-L-BREAK | 1 | Seedance 2.5, **Edit video** on the first 4 s of the studio comp loop (`05_REFERENCE_UPLOADS/STU-L-LOOP_comp_upload_4s.mp4`, media fe4cfbe2…), 1080p, high, **batch 1** (submitted alone, one charge confirmed), sound on. **48 credits (day total 1,080)** | new prompt: the salon's v5 body with only the wall words changed (right edge, plaster, keep the canvas) | **USED THROUGH THE SCRIPT; the prompt half-failed** | Framing held; plaster blocks float in the dark from frame 0. But the model ignored "preserve the whole canvas" and broke its right ~16% (canvas ends ~75% instead of 91%), plus some rubble. **Usable because break_strip.py never takes the canvas:** `--protect 0.14,0.18,0.91,1.0` (the canvas rectangle), `--max-x 0.3 --side right`, and `--layer-gain 0.5` (the model lit its blocks ~3x brighter than the plaster: 104 vs 33). The plaster above the canvas's right corner breaks on the model's own ragged line. File `edge_break_tests/S9-STU-L-BREAK_v1.mp4` (dfb8f245…) |
| 2026-09-25 | (all walls) | — | no generation | **Homie: "these realities have the fragmented edges throughout the whole time… you decide how much"** | **Edge versions of every show file, with sound, in `01_FINAL_FOR_SHOW/<wall>/with_edge_effect/`** | Salon: v5 B via break_strip (left, ~12-14% band, cracks to the left sconce, which stays whole and still lights/snuffs); IN/HOLD/OUT fitted to 193 frames (`--period 193`, IN `--offset 73`) so HOLD wraps (step 1.13 vs 1.12 normal) and the pieces join. Studio: as the row above. Court: torn paper both sides (~8%, script, `render_court.py --scrim --edges`), scraps drifting; the judge in front and whole (only the Q5 capper's first ~6 frames reach the torn zone, accepted) |
| 2026-09-25 | (all walls) | — | no generation | **Homie: "none of the audio makes it in the files… embed it… don't get rid of any of the audio"** | **All 15 show files v2 with sound embedded** (48 kHz 24-bit PCM) | Cause: every picture tool read frames only, so the sound was dropped at the first step; an earlier session had read "audio on as a scratch for the sound designer" as "never in the comp". `tools/build_audio.py` rebuilds each soundtrack from the clips' own audio with the picture's exact cuts (loop cycles crossfaded like loop_halo, holds on the clip's own ambience, court following render_court's timeline). **Verified: every segment correlates 1.000 with its source at zero offset**; picture stream-copied (MD5 identical). Levels as generated. Silent files moved (checksummed, nothing deleted) to `03_TESTS_IN_PROGRESS/superseded/show_v1_silent/` and `court_v2_silent/` |
| 2026-09-25 | S9-CRT (show files) | — | no generation | **Homie: "just composite the new court background into the final show files and be done with this"** | **Court v2 = the APPROVED strike + v1 timing + the scrim field + Q1 ~2.0 m** | `render_court.py --scrim` (new option; v1 still rebuildable). The v2 reading loop / B3 / B5 are NOT in the show (rejected); they stay in `03_TESTS_IN_PROGRESS/judge_tests/` |
| 2026-09-25 | S9-CRT-STRIKE-B3 v2 / B5 v1 | — | — | Homie reviewed court_C_b3/b5_v2 previews | **REJECTED by Homie: "the whole animation of the gavel is wrong"** | He had said at the start of the session that the approved strike was "quite spot on"; replacing it with new strike styles (D12) overrode that fresh signal. The approved strike returns for every strike; the reading loop, bigger Q1 and the scrim field ("fine") stay. One judge confirmed. Credits: of 1,032, about 660 bought nothing usable (30 s edit 360, wither v4 96, B3 v1 + duplicate 96, B3 v2 + B5 108) |
| 2026-09-25 | (connector) | — | — | **DUPLICATE SUBMISSION**: B3 v1 and B5 v1 were sent as two parallel `generate_video` calls; the server created B3 TWICE (a5b52604… at 19:21:09 and fe53afcb… at 19:21:17), both charged (48 each) | **session total 1,032, 32 over the 1,000 cap. Generation stopped (stop rule: unexpected connector behaviour)** | The duplicate is a usable second take of B3 v1 (`judge_tests/S9-CRT-STRIKE-B3_v1_take2.mp4`, e7eeed73…). Then B3 v2's submission returned `ERR_NAME_NOT_RESOLVED` but WAS charged (48 at 19:28:51); not resubmitted. **Rule for PIPELINE.md: submit generations one at a time and check `transactions` after each.** Balance 4,282.09 -> 3,250.09 |
| 2026-09-25 | S9-CRT-STRIKE-B5 | 1 | Seedance 2.5, **SEQUEL (`video_extension` forward) of the reading loop** (`05_REFERENCE_UPLOADS/CRT-READ_loop_upload.mp4`, frames 9-358 of the 15 s take, media af453982…), 1080p, 5 s, high, batch 1, sound on. **60 credits (session 936)** | new prompt: the FRANTIC DOUBLE (LOOK D12) | **KEEP (candidate), one script fix** | Two blows: ~f24 and ~f62, yanked back up between, then held; join from the loop native. The held gavel is HUGE, end-on, covering head and torso ("a gavel on legs"), plus a straight WHITE BAR across it at the gavel's lower edge (incidental white, not the sanctioned keyline). For beat 5 ("loses control") the swallowing gavel reads as escalation, so it stays; **the bar is filled by Claude's script on this clip only** (never on the approved strike, whose keyline is sanctioned). File `judge_tests/S9-CRT-STRIKE-B5_v1.mp4` (f491cfeb…) |
| 2026-09-25 | S9-CRT-STRIKE-B3 | 1 | as B5, 4 s. **48 credits (session 876 -> 936 incl. B5)** | new prompt: the MEASURED strike (LOOK D12) | **FAIL on scale; blow good** | Formal raise, one blow at ~f30, hold; native join. **DIAGNOSIS (before the fix): "wider than his body" in THE GAVEL (lesson 9, an exaggeration word)**: the held gavel swallows head and torso, plus the same white bar. The approved strike's gavel covers the chest with the head above it, the read Homie likes. **v2 = ONE CHANGE: the size phrase**, pointed at that scale. File `judge_tests/S9-CRT-STRIKE-B3_v1.mp4` (4c0da25c…) |
| 2026-09-25 | S9-SAL-R-WITHER | 5 long | Seedance 2.5, **Edit video** on the whole beat-2/3 salon chain (reveal + loop x2 + snuff + 94 f dusk hold = 30.0 s, media 002f3eca…), 1080p, high, **batch 1**, sound on. **360 credits (session 648/1,000)** | v5's body word for word; only the input changed | **FAIL (Claude's call, owned)** | 713 frames. Framing held (0 px). But: (1) the band is ~25% wide and strands the left sconce on a floating column (v5 A's fault; one take couldn't dodge it); (2) the lit room ~30% darker than the input (luma 66 vs 94); (3) **the snuff is LOST**: after f550 the input is dusk (luma 26), the edit stays lit (62); (4) the break evolves, scattering to near-empty void by the end. **Lesson: a probe proves only what it contains.** The 4 s probe was a steady loop with no candle events; the chain had three. That made the long run an untested input, not a proven candidate, and both risks were in the prediction. Next time, probe the hardest 4 s of the real input (here, the snuff) before the long run. Salvage without credits: v5 B's break strip ping-ponged (7.4 s, no crossfade) over the approved clips by script, light-matched per frame. File `edge_break_tests/S9-SAL-R-WITHER_v5_long.mp4` (2bb2a1f6…) |
| 2026-09-25 | S9-CRT-READ | 1 long | Seedance 2.5, References from the approved still (media 8e4f677b…), 9:16, 1080p, **15 s**, high, batch 1, sound on. **180 credits (session 828/1,000)** | v1's body word for word; duration only | **PASS -> candidate reading loop** | 361 frames, 15 s of steady declaiming, no strike. **Loops with no crossfade:** frames 9 and 359 overlap at IoU 0.998, both held moments, so frames 9-358 (350 f, 14.6 s) cycle cleanly. Files `judge_tests/S9-CRT-READ_v1_long.mp4` (006409c2…), loop `S9-CRT-READ_v1_loop.mov` (ProRes, 3e036850…), upload `05_REFERENCE_UPLOADS/CRT-READ_loop_upload.mp4` (9a0c6d9c…, media af453982…) |
| 2026-09-25 | S9-CRT-READ | 1 | Seedance 2.5 via the connector, **References (omni_reference) from the approved still** `fig_SOTR_judge_s9_v1.png` (uploaded, media 8e4f677b…, sha256 f29e6ae9…), 9:16, 1080p, 4 s, high, batch 2, sound on. **96 credits (session 192)** | new prompt: the judge's READING LOOP (LOOK D12), all the life at the outline | **PASS, both takes** | Both declaim: head dips to the scroll and lifts to the gallery, scroll arm rises and dips, gavel jabs, never strikes; one tone. **B** calmer; framing within 1-2% of the still (bbox), first/last frame IoU **0.98** (loops). **A** livelier (a flourish at 3 s, coat flaring, gavel shooting up). **NEW, flagged for Homie:** when the head turns to the scroll the OUTLINE shows a nose and chin in profile (A also an open-mouth notch). Nothing inside the outline (LOOK's real ban); it's the life D12 asked for, but it's the first profile this figure has had. Files `03_TESTS_IN_PROGRESS/judge_tests/S9-CRT-READ_v1_A.mp4` (8d354f19…), `_B.mp4` (42ed910b…) |
| 2026-09-25 | S9-SAL-R-WITHER | 5 | Seedance 2.5 via the connector, **EDIT VIDEO (`video_edit`)** on the first 4 s of the comp loop (`05_REFERENCE_UPLOADS/SAL-R-LOOP_comp_upload_4s.mp4`, media f912dd7c…), 1080p, high, batch 2, sound on. **96 credits (48 per take; session 288/1,000)** | the mechanism only: edit the loop instead of continuing it; body = house surgical-edit template, v4's THE EDGE word for word | **B = THE BREAK FOR THE SHOW (candidate). A = too wide** | **B:** broken from frame 0, full height, Control blocks floating in place, cracks into the panelling round the left sconce, sconce whole, nothing falls. Measured against the input: framing <1 px (0.05/0.6), luma right of the break within 2%, band steady 100-115 of 832 px (12-14%). Output 89 frames (3.7 s) from a 96-frame input. **A:** band ~27%, the left sconce stranded in the void (v2 B's fault), clearer floor with rubble. **FLOOR: in BOTH takes** (B: a faint dark floor strip ~4% of the height with a few static pebbles, under the break only). Now 6 takes across 5 wordings, two banning it by name. **Lesson 6: structural** (a wall that has broken away reveals a space, and to the model a space has a floor). **Stop rewording; fix by Claude's script** (a soft fade to black over the bottom ~5% of the void only, not the wall), flagged to Homie. Files `edge_break_tests/S9-SAL-R-WITHER_v5_A.mp4` (27f7d4db…), `_B.mp4` (4194fc2b…) |
| 2026-09-25 | S9-SAL-R-WITHER | 4 | Seedance 2.5 via the connector, **SEQUEL (`video_extension` forward) from the salon comp loop** (media 4afb0ccd…, role coerced to `video_references`), 1080p, 4 s, high, batch 2, sound on. **96 credits (session 96/1,000)** | the mechanism (v3's body as a continuation: REFERENCE, FIRST FRAME, one MOTION phrase) + one floor line in THE EDGE ("no floor, no rubble") | **Mechanism PASS, look FAIL. Neither take usable** | **A:** framing identical to the loop, placeholder portrait held (the Sequel does what it did for the snuff). But the break FORMS AS A COLLAPSE: a column of blocks at 0.5 s, then they scatter and FALL, a rubble heap at the bottom-left from ~1.5 s, then a sparse drift. **B:** an event again, the cracks widen until the left sconce floats in the void. **DIAGNOSIS (logged before the fix): structural, not wording (lesson 6).** A Sequel starts on the UNBROKEN wall, so the break must happen on camera; a wall breaking on camera is a collapse to the model, and a collapse has gravity, hence rubble. The rubble is now in 4 takes (v1 A, v2 A, v3 B, v4 A) and "no rubble" didn't stop it. The takes that floated (v2 A, v3 A) all started ALREADY BROKEN. **Next: v5 = Edit video (`video_edit`) on the comp loop**: the break present from frame 0 on the loop's own frames, so nothing forms or falls and the framing/candles/portrait are the input's. Files `03_TESTS_IN_PROGRESS/edge_break_tests/S9-SAL-R-WITHER_v4_A.mp4` (322042ce…), `_B.mp4` (ad8182d7…) |
| 2026-09-24 | (media) | — | no generation | **SOTR_MEDIA reorganised** (Homie: he couldn't tell finals from tests in `loops/` to show the client) | **done on both drives, 54 files moved, every checksum unchanged** | New: `01_FINAL_FOR_SHOW/` (per wall + client-facing `00_READ_ME_FIRST.txt`), `02_APPROVED_BUILDING_BLOCKS/`, `03_TESTS_IN_PROGRESS/`, `04_REJECTED/`, `05_REFERENCE_UPLOADS/`; `comp/` (his After Effects area) untouched. Old -> new table in `SOTR_MEDIA/README.txt`; the script is `tools/reorg_media_2026-09-24.py`. Tools re-pointed (court source), and render_wall's effects guard now uses `<wall>/with_edge_effect/`. The T9 keeps 9 old extras in their old folders (copy, never delete). **Homie also identified his favourite break frame as wither v3 B; v2 A equally good; both show floor and rubble at the bottom, to fix next.** Rows above this one quote the OLD paths |
| 2026-09-24 | S9-SAL-R-WITHER | 3 | Seedance 2.5 via the connector, References, same Gérard clean frame, 4:3, 1080p, 4 s, high, batch 2, sound on. **96 credits (session total 960/1,000; generation stopped)** | ONE change against v2 (lesson 3, change the noun): 'fragments' -> 'rectangular blocks … cut clean like masonry' | **A = THE LOOK (Control), but two faults. B = event again** | **A:** the whole left side, cornice to floor, is clean rectangular blocks floating weightless; STEADY (band 192/191/192 px at 0/2/4 s of 832); lock 0 px within the clip. **But Gérard is GONE** (the model painted a blank panel into the frame) and the **framing drifted** (the wall is zoomed/shifted against the plate). **B:** keeps Gérard and the framing; deep fissures crack open full height with masonry blocks along them, but it grows (78 -> 131 px), an event. **Next (new session): v3's wording as a SEQUEL from the comp loop** (Sequel held the framing to 0 px for the snuff and reveal), then Gérard via `render_wall.py` as usual. Files `loops/S9-SAL-R-WITHER_v3_A.mp4` (90c2d62d…), `_B.mp4` (3837e3ea…) |
| 2026-09-24 | S9-SAL-R-WITHER | 2 | Seedance 2.5 via the connector, References, same Gérard clean frame, 4:3, 1080p, 4 s, high, batch 2, sound on. **96 credits** | full-height break, steady from the first frame, weightless drift (Homie's brief). Homie then clarified mid-render: keep v1's crack-and-block Control look, not softer; the problem was only coverage; and then: the break line UNEVEN, not straight | **A = CANDIDATE for Homie** (`loops/S9-SAL-R-WITHER_v2_A.mp4`, 269efa92…). B too much | **A:** breaks the full height from frame 0, uneven line, cracks into the panelling, pieces floating; sconce whole; lock 0 px; Gérard steady (step 0.19); band 11% -> 12% of the width over 4 s (near steady, so it can extend). Pieces read more as shards than Control's chunky blocks. **B:** shatters a web to 24% width, leaving the left sconce on an island: spectacular, too much. Secondary reference from Homie: the *Your Friends and Neighbors* title sequence (breaking objects); Control stays the primary |
| 2026-09-24 | S9-SAL-R (finals) + S9-STU-L (tool) | 1 | no generation | built from LOOK D1-D4 (Claude, delegated): the salon's finished files at script-derived beat lengths, and the studio painting tool | **salon clean files rendered; studio beats rendering** | Salon: b2-3 (117.4 s), b8 (16.0 s), IN/HOLD/OUT, all clean with Gérard, checksummed. Studio: `render_studio.py`, the Raft on the canvas lit by the canvas's own light (pixel / primer), unpainted areas as an umber outline on the primer, paint order lower band → bodies and sail → sky → apex LAST; stage stills checked (half / most / complete). First cut-off of 1.01 left the apex part-drawn; raised to 1.06 |
| 2026-09-24 | S9-SAL-R-WITHER | 1 | **Seedance 2.5 via the connector**, References, ref = a CLEAN frame with Gérard composited (`refs/SAL-R-clean-gerard-f300.png`), 4:3, 1080p, 4 s, high, batch 2, sound on. **96 credits** | capability probe (Homie: "see what we can do with Higgsfield itself") for a Control-style edge | **Higgsfield CAN do it. Homie liked the look (cracks, blocks breaking off)**; coverage wrong | Both takes break the wall itself: cracks run into the panelling, slabs with thickness drift into black. Lock 0 px. **GÉRARD HELD in both** (portrait step 0.24), which answers Homie's painting question: a composited real painting survives being animated. Faults: an EVENT, not a steady state; pieces fall (A drops rubble to the floor); B breaks only mid-height and eats the left sconce. Homie: the break must run across the WHOLE side. Files: `loops/S9-SAL-R-WITHER_v1_A.mp4` (a1cd35e0…), `_B.mp4` (549add47…) |
| 2026-09-24 | S9-SAL-R (sequence) | clean | no generation | **file management (Homie): clean renders saved and never lost; effects are separate files** | **clean master saved** -> `renders/clean/loc_SOTR_salon_R_seq_s9_v1_clean_HOLDS-TBD.mov` | Checked first: every clean source in `loops/` and `plates/` matches its recorded checksum, and none was ever modified (the fragment renders were scratch previews only). New folders `renders/clean/` and `renders/fx/`; `render_wall.py` now refuses to overwrite an existing file, to write an effect render into `clean/`, or a clean render into `fx/` (all three tested). **Homie didn't like the dissolve fragment preview** and is sending examples, so the fragment look is on hold |
| 2026-09-24 | S9-STU-L-LOOP | 2 | — | **APPROVED by Claude** (Homie delegated taste calls: "I'll let you make the decision") | **APPROVED -> `loc_SOTR_studio_L_loop_s9_v1.mp4`** + `_comp.mov` | Re-measured before approving: lock 0 px, framing identical to the plate (0 px), pool swing 28%, drift +3.5% cancelled by `loop_halo.py` (the cycle's remaining -2.8% is the candle's own swells, 87.5-94.8 per second). Wrap step 1.11 vs the clip's own max 1.19. Studio preview with the fragment edge on the RIGHT (14%): the breakup takes the dark plaster margin and just catches the canvas edge |
| 2026-09-24 | S9-SAL-R (sequence) | 2 | no generation: `tools/render_wall.py` (renamed from `comp_portrait.py`) | Homie: **no fades** at start/end (the operator's), and **fragment edges** (whole outside, breaking up toward CENTRE, per 2022 Slide 9) | **preview sent to Homie** | Sequence: reveal · loop x2 · snuff, Gérard, **no fades, no tail hold**, fragment edge LEFT at 14%, style `dissolve`. Iterations, all by script: (1) Voronoi cracks read as a chicken-wire mesh, dropped; (2) `shatter` hard shards read as cut paper, kept as an option; (3) `dissolve` chosen, widened for islands and particles; (4) a straight cut where the front wandered past the zone, fixed by forcing whole at the zone boundary (max 1.2% at the boundary over 60 s); (5) the drift noise had a wrap seam 10-90x a normal row step, fixed with truly periodic noise (now within the normal range). 25% width ate the left sconce; 14% clears it |
| 2026-09-24 | S9-SAL-R (sequence) | — | no generation: `tools/comp_portrait.py` (new) | the salon wall built as ONE finished file (final-product rule): fade in 1.5 s · reveal · comp loop ×2 · snuff · 2 s dusk hold · fade out 1.5 s, **Gérard composited throughout** | **preview sent to Homie. Hold lengths are PLACEHOLDERS (no beat timings yet)** | 674 frames. **Gérard:** canvas opening measured at x 586-1053, y 154-873 (468x720, ratio 1.54; Gérard is 1.44, so a 6% side crop, no stretch). Graded per frame to the placeholder's own mean and spread, plus the SHAPE of its light (left side darkens first), plus matched grain. v1 of the tool scaled each colour channel by the placeholder's change and turned the ermine lavender at dusk; fixed. **Joins:** a uniform ~1.3-level exposure step at each generated join was removed with a 1 s exposure ease into each incoming clip (no crossfade, so no ghosting). Brightness change at the joins is now -0.06 / +0.05 levels; the remaining per-frame difference (~1.1) is flame shapes, inside the room's own flicker (99th pct 2.22) |
| 2026-09-24 | S9-SAL-R-REVEAL | 1 | **Seedance 2.5 via the connector (Claude), PREQUEL: `video_extension` backward** from the comp loop, 1080p, 5 s, bitrate high, batch 2, sound on. **120 credits** | new prompt (the entry, mirroring snuff v7), written under the final-product rule | **PASS. B APPROVED (Claude, on Homie's delegation) -> `loc_SOTR_salon_R_reveal_s9_v1.mp4`; A -> `rejected/`** | Both takes' LAST frame joins the loop's first at **0 px**, within 1-2 levels. **B lights the candles ONE AT A TIME** (left sconce frames ~20/30/40, then right ~50-60), then the ivory warms to the loop's light: exactly LOOK.md World 1's "one candle at a time". A lights each sconce all at once. No smoke or sparks; portrait still; lock 0 px. Prompt bodies name the reference in words ("the attached clip"), no @tag |
| 2026-09-24 | S9-SAL-R-SNUFF | 8 | Seedance 2.5 via the connector (Claude), Sequel (`video_extension` forward) from the comp loop, 1080p, 5 s, bitrate high, batch 2, sound on. **120 credits** | ONE change against v7: when the smoke ends (Homie's idea). Wisps 0:02-0:04, "gone at 0:04", then a second of dusk; the LOCKS line gets "none after 0:04" | **FAIL on taste (Claude): both -> `rejected/`. v7 B stays the approved snuff** | Join and staging held (0 px; right out at 1.38 s, a little faster). **But the deadline made the smoke BIGGER:** both takes front-loaded puffy pale plumes at 2-3 s (A gathers into a cloud at 4 s; B clears by 5 s but puffs early). v7 B is the thinnest at every time point and is nearly clear by 5 s anyway. **Lesson: a deadline doesn't shorten an event, it compresses and inflates it.** Same family as lesson 9 (exaggeration words blow it up) |
| 2026-09-24 | S9-SAL-R-SNUFF | 7 B | — | **APPROVED by Claude on Homie's delegation** ("if you think V7B is the one, then that's the one") | **APPROVED -> `loc_SOTR_salon_R_snuff_s9_v1.mp4`** (checksum unchanged, 9dd87ec4…). v7 A -> `rejected/` | See the v7 row. Plays straight after the comp loop with an invisible join |
| 2026-09-24 | S9-SAL-R-SNUFF | 7 | **Seedance 2.5 via the connector (Claude), SEQUEL: `video_extension` forward** from the approved comp loop (uploaded as `refs/SAL-R-LOOP_comp_upload.mp4`, media 4afb0ccd…), 1080p, **5 s**, bitrate high, **batch 2**, sound on. **120 credits** (60 per take) | the reference mechanism (continue the loop video) + the two prompt lines describing it (REFERENCE, FIRST FRAME); every other word v4. Driven by Homie's new rule: no playback fixes, the join must be inside the file | **JOIN PASS 2/2. Smoke: taste call for Homie.** Both in `loops/` (`S9-SAL-R-SNUFF_v7_A.mp4`, `_v7_B.mp4`) | Output = the 5 s extension only (120 frames, 1664x1248, HEVC 10-bit). **The join is native:** frame 0 vs the loop's last frame is **0 px** shift, every region within 2% (halos +0.5%, dado +1.8%), against the web take's 4 px and -16 to -27%. A loop+snuff single file measured: the join step is 0.94 against a normal in-loop step of 0.67, so it doesn't show. Staging: left out 0.79 s, right 1.71 / 1.75 s, no smoke while lit. **Different from v4:** the end state goes much darker (luma ~26 vs ~45), and the smoke comes out **PALE** against it and is **still rising at 5 s**: A = pale puffy plumes (near the old defect); B = pale threads with small heads (better). Homie's web take had dark threads gone by 4 s. Single-file previews (4 s of loop + snuff) sent to Homie |
| 2026-09-24 | S9-SAL-R-SNUFF | 6 | Seedance 2.5 via the connector, **mode left at the default (t2v)**, comp-loop frame 0 as `start_image`, 4:3, 1080p, 4 s, batch 1. **0 credits (refused)** | the mode only, against v5 | **REFUSED by the server, 422:** *"start_image and end_image are only allowed for mode 'omni_reference'"*, which is the mode v5 used and where the image acted as a loose reference | **Closes the first-frame route on this connector.** No way to pin a clip's first (or last) frame, so the snuff/loop cut is matched in the comp or QLab, and loops keep the `loop_halo.py` crossfade. No charge (ledger checked) |
| 2026-09-24 | S9-SAL-R-SNUFF | 4 (web) | **Seedance 2.5, web app, run by Homie** just before this session (-60 credits, 03:03 UTC), **5 s**; other settings presumed v4's (UNCONFIRMED) | — (his own run of v4, presumably) | **BEST TAKE SO FAR. Homie: "I don't mind it." Awaiting his approval** | Downloaded by Homie as "Snuff not bad.mp4", renamed `loops/S9-SAL-R-SNUFF_v4_web5s.mp4` (sha256 4a63d26b…). Matches none of Claude's takes (5.05 s, 121 frames). Left out at 0.79 s, right at 1.71 s, no smoke while lit, thin dark threads, **gone by ~4 s, then a still dusk wall**, so it's complete as an exit at 5 s and **no 10 s run is needed**. Lock 0 px. **Against the lit loop:** frame 0 is 4 px off (my takes 16), halos within 5%, but the dado -22%, far-left panel -16% and portrait -27% darker. Cut previews (hard vs 6-frame crossfade) sent to Homie. **Found: the snuff needs the Gérard comp too** (placeholder king in every generated clip), so v4's "no comp step" was wrong |
| 2026-09-24 | S9-SAL-R-SNUFF | 5 | **Seedance 2.5 via the connector (Claude)**, `omni_reference`, **frame 0 of the comp loop as `start_image`** (`SOTR_MEDIA/refs/SAL-R-LOOP_comp_f0.png`), 4:3, 1080p, 4 s probe, bitrate high, batch 2, sound on. **96 credits** | the reference role only (v4 body word for word): the loop frame as the first frame, to make the QLab cut match | **FAIL, mechanism. Both takes → `rejected/`. Generation STOPPED (AUTONOMOUS-GEN stop rule: unexpected connector behaviour)** | **The server coerced `start_image` into a plain reference** (the echo says `reference_images`, same as v4). Frame 0 is a new render: mean luma 65-67 vs the loop's 90, shifted 9-10 px, the room pulled back and the portrait smaller. Worse than v4 (16 px, 10 levels). A graded, darker video frame makes a worse loose reference than the plate. Lock 0 px. Staging held again (left out at 0.83 / 0.88 s, right at 1.88 / 1.29 s). **Smoke across all four takes of this identical body: A-takes dark curling threads, B-takes pale puffs and haze, 2 and 2, so it's luck.** Not tried unattended: `start_image` in the default `t2v` mode (the stop rule applies; queued for Homie) |
| 2026-09-24 | S9-SAL-R-SNUFF | 4 | **Seedance 2.5 via the connector (Claude)**, `omni_reference`, ref = lit plate as `image_references`, 4:3, 1080p, **4 s probe**, bitrate high, **batch 2**, sound on. **96 credits** | first run of the v4 restructure (lit reference, left then right, incense-wisp noun) | **Staging PASS 2/2. Smoke 1/2. Cut match FAIL 2/2.** A → `loops/S9-SAL-R-SNUFF_v4_probeA.mp4` for Homie; B → `rejected/` | 1664x1248, 24 fps, 97 frames, HEVC 10-bit, lock 0 px. **The restructure worked:** the model staged the exit as written in both takes, with no smoke while lit. Sconce halos measured: A left out at 1.00 s, right at 2.00 s (exactly the timing); B at 0.62 / 1.33 s. **Smoke:** A = thin dark curling threads from each wick, each leading with a small curl, rising ~1 m to the panel cartouche (higher than "the top of the sconce"); B = pale puff-headed plumes spreading to haze, the v1-v3 defect. **New fault, cut match:** both takes' frame 0 sits 16 px lower (edge-based phase correlation) and ~10 levels darker (80.7 vs 90.7) than the lit loop, since every run re-frames the wall by ~1%. On a hard QLab cut the whole wall would drop ~46 mm and dim 11% in one frame. End state is darker than the DARK plate (45 vs 63); harmless, the exit goes to black. **v5, one change:** a frame of the comp loop as `start_image` |
| 2026-09-24 | S9-SAL-R-LOOP | 1 | **Seedance 2.5 via the connector (Claude)**, `omni_reference`, ref = lit plate as `image_references`, 4:3, 1080p, 10 s, bitrate high, batch 1, sound on. **120 credits** | nothing: the **connector parity run** (AUTONOMOUS-GEN step 0), approved prompt word for word | **PASS: the connector is the web app** | `loops/S9-SAL-R-LOOP_v1_parity.mp4` (sha256 88222b60…). Same size, fps, frames (241), HEVC Main 10, AAC 32 kHz, **7.15 Mb/s vs the approved 7.17**. Lock 0 px; framing within 0.6% of the plate; six flames; portrait step median 0.20 (approved 0.20). Halo flicker 3.8% (approved 3.6%, by `tools/measure_clip.py`), drift -0.8% (approved -1.6%). About 5% darker overall (mean luma 84.8 vs 89.5), which may be variation between runs. The server first answered with a preset suggestion ("IN THE DARK") instead of a job; resubmitted with it declined. Render ~6 min. Four gaps all passed, see `PIPELINE.md` |
| 2026-09-24 | S9-SAL-R-SNUFF | 3 | **Seedance 2.5**, References, ref `@loc_SOTR_salon_R_dark_s9_v1`, 4:3, 1080p, 10 s, High, batch 1, sound on | v1's text with only the smoke amount reduced (+ the cloud ban) | **FAIL, Homie: "the smoke is just off"** | `SOTR_MEDIA/rejected/S9-SAL-R-SNUFF_v3.mp4` (downloaded as "V3"). The snuff moment is back (v1's staging). **Smoke:** a thin column with a puff-ball head on each, gathering into a cloud at the cornice by ~3 s. It's smaller than v1 but the same fault, and the cloud ban didn't hold (a demonstrated prior, house-rules 5c). **Smoke streams from candles that are still lit** for ~1.5 s (as in v2). **Starts LIT from a DARK reference, 3 runs out of 3.** **Structural finding (lesson 6):** the model insists on staging the snuff itself, and our DARK reference plus "a moment after" contradicts the event it wants to show. Rewording has now failed twice on the smoke. **Proposed to Homie:** restructure (a LIT reference, the clip IS the exit) or drop the smoke. |
| 2026-09-24 | S9-SAL-R-SNUFF | 2 | **Seedance 2.5**, References, ref `@loc_SOTR_salon_R_dark_s9_v1`, 4:3, 1080p, 10 s, High, batch 1, sound on | smoke rewritten as thin real threads (SCENE, FIRST FRAME, ACTION TIMING and PHYSICS all rewritten) | **FAIL, Homie: "completely horrible… the previous animation was so much better"** | `SOTR_MEDIA/rejected/S9-SAL-R-SNUFF_v2.mp4` (downloaded as "snuff fail"). The flames kept burning ~1.5 s **with smoke already rising from lit candles**, then dimmed away slowly like a dissolve, so it never read as a snuff. The smoke threads themselves were close to right. **Our error:** the "one change" rewrote four blocks and the timeline, and lost v1's crisp snuff, the part that worked (house-rules: patch what failed, don't rewrite). Also batch 1 each time, so wording and luck can't be separated. **v3 = v1's text word for word, with only the smoke amount changed** ("full, clearly visible" -> "thin"; "lift higher… spreading" -> "fade out a short way above the sconces"; + the cloud ban). Batch 2 recommended. |
| 2026-09-24 | S9-STU-L-LOOP | 2 | **Seedance 2.5**, References, ref `@loc_SOTR_studio_L_s9_v1`, 4:3, 1080p, 10 s, High, batch 1, sound on | motion register subdued to vivid (a candle guttering in a draught, the pool shivering and sliding, plaster shadows jumping); damping words out, dust dropped | **WORKS, testing, Homie to judge the looped preview** | File `SOTR_MEDIA/loops/S9-STU-L-LOOP_v2.mp4` (Homie's name; content verified as the studio). 1664x1248, 24 fps, 241 frames. **Camera locked (0 px), canvas edge fixed at the same pixel all clip, no floor.** **Motion vs v1, measured:** light-pool swing **17%** peak to peak (v1: 4%); pool sway **~370 mm** (v1: ~50 mm); frame-to-frame max 3.5 (v1: 1.1). Character: restless swells and dips every 2-3 s, a candle ducking in a draught. Mostly slow (19% of the energy above 1.5 Hz), so it isn't a fast flicker, but it's clearly visible. Still whole-canvas (pool vs rest correlation 0.99). **One defect: a slow brightening of about 7% over the clip.** Cancelled by `tools/loop_halo.py` (the same step as the salon), so no work for Homie. **The one change worked: v1's damping vocabulary was the cause.** Loop built: `loop_halo.py --boost 1 --skip 12 --xfade 36`, 8.04 s cycle. The seam step (1.09) equals the source's own flicker step at that frame (47->48: 1.13), so it isn't a seam artifact. |
| 2026-09-24 | S9-SAL-R-SNUFF | 1 | **Seedance 2.5**, References, ref `@loc_SOTR_salon_R_dark_s9_v1`, 4:3, 1080p, **10 s**, High, batch 1, sound on | first run | **FAIL, Homie: "too unrealistic and over the top… obviously AI-generated"** | 1664x1248, 24 fps, 241 frames. Framing, portrait and DARK colour all held. **Smoke:** (1) balls up into round cartoon clouds about 1 m above each sconce, with tendrils trailing down beneath; (2) the first puffs appear in mid-air, detached from the wicks; (3) far too much volume, still present at 10 s. **Cause: our wording.** To beat stage scale we asked for "a full, clearly visible ribbon… spreading" as a theatrical exaggeration, and the model exaggerated it into clouds (the house-rules 5b mechanism, over-drive). Also: **the clip opens with the candles LIT** and snuffs them in the first ~0.5 s, against the DARK reference and the unlit lock. Harmless, since it's trimmed; not changed this round. **v2, one change:** the smoke description, now one thin real thread per wick, joined to it, rising less than the sconce's height, fading in ~4 s, with "cloud or puff" banned by name (demonstrated). File: `SOTR_MEDIA/rejected/S9-SAL-R-SNUFF_v1.mp4` (downloaded as "snuff test"). |
| 2026-09-24 | S9-STU-L-LOOP | 1 | **Seedance 2.5**, References, ref `@loc_SOTR_studio_L_s9_v1`, 4:3, 1080p, 10 s, High, batch 1, sound on | first run (light split by speed: fast shimmer + dust asked for) | **USABLE AS A BASE PLATE; the generated motion doesn't do its job, testing** | 1664x1248, 24 fps, 241 frames, 10.04 s, HEVC 10-bit. **Camera locked (0 px). No floor**: the 4:3 risk didn't happen, and the canvas runs cleanly off the bottom. No slow drift (unlike the salon). **What came back (measured):** the light moves about 4% peak to peak on the pool, 2% on the rest of the canvas, but it's ONE GLOBAL SLOW BREATH (pool vs rest of canvas correlation 0.98, dominant 0.5-0.7 Hz), not fast local flame shimmer. The pool shifts only ~50 mm. **Dust: none** (0.2 specks/frame, which is grain). Homie: "feels like a static image". **Finding: the split-by-speed premise failed.** Asked for small, fast, even motion, the model returned small, slow, global motion. That's exactly the comp pass's job, so the generation added texture and grain but no flame life. Same root as the salon: "small / even / constant" is read as nearly still. I first proposed a comp candle pass (mock-up sent). **Homie overruled it: "If we can do a regeneration, we'll just do a regeneration"**, now a standing rule. **Next: v2**, one change: the motion register, subdued to vivid (damping words out, a restless draught-driven flicker in). Dust is dropped. Saved, now `SOTR_MEDIA/rejected/S9-STU-L-LOOP_v1.mp4`. |
| 2026-09-24 | S9-SAL-R-LOOP | 1 | **Seedance 2.5**, References mode, ref `@loc_SOTR_salon_R_s9_v1`, 4:3, 1080p, 10 s, High, batch 1, sound on | first run (halo-breathing version of the prompt) | **APPROVED 2026-09-24, Homie picked preview B (halo boost 3x in the comp)** | 1664x1248 (4:3 at the 1080p tier is 1664 wide, not 1440), 24 fps, 241 frames, 10.04 s, HEVC Main 10 `yuv420p10le`, AAC 32 kHz stereo. **Camera locked: 0 px shift** first to middle to last frame (phase correlation). Framing matches the plate within ~1%. All six flames present and stable throughout. **Portrait still:** no blink or movement (the only frame-to-frame spike is frame 0). No floor, no people. **What moves (measured, not eyeballed):** a per-pixel motion map shows motion at the flames plus a soft ring around each sconce. The halos DO breathe, but faintly: fast flicker is about 2-3% peak to peak, 3-4x the static panels' noise. That matches Homie's read of "just the flickering candles". **One defect: slow dimming.** Around the sconces the light falls about 3% over the 10 s (whole frame -1.8%, dado -0.7%). That's a trend, not flicker, so it would pulse once per cycle in a loop. **Comp fix, no regeneration:** a per-pixel linear gain cancels it. **Frame 0 is the reference itself**, cleaner than the rest; the loop starts from frame 12. **Crossfade loop built and tested:** frames 12-240, 1.5 s crossfade, 8.04 s cycle; the seam is quieter than a normal frame step. **Two previews made for Homie:** A = as generated (detrended, looped); B = the halo flicker boosted 3x in the comp (only large-scale light change is amplified; grain untouched). Next: Homie picks the halo amplitude. The comp can drive it from the flames' own flicker, so no regeneration is needed. Renamed `loc_SOTR_salon_R_loop_s9_v1.mp4` on approval (checksum unchanged). **B is reproducible:** `tools/loop_halo.py --boost 3 --skip 12 --xfade 36` renders the 10-bit ProRes comp master `loc_SOTR_salon_R_loop_s9_v1_comp.mov` (wrap-around seam verified clean). |
| 2026-09-23 | S9-CRT-STRIKE | 3 | **Seedance 2.5**, image-to-video from `@fig_SOTR_judge_s9_v1` | strike direction changed from downward to **toward camera**; `GAVEL PATH` and `FIELD` prohibition blocks deleted; coat movement and forward weight asked for positively | **PASS, with one flagged deviation** | 1080x1920, 24 fps, 4.04 s, 97 frames, HEVC 10-bit. **Verified frame by frame, not on stills.** Structure: hold to ~f47 (coat alive), the blow f48-f53, held large f54-f96. The gavel *rotates* as it comes, so the striking face arrives end-on at the viewer — not specified, and better than what was: it is the business end pointed at the audience. Cloth life is back and is the best in any version (skirts fly, lag, settle) — deleting v2's prohibition blocks is what did it, and **restoring the word "coat" to the physics clause** (v2 had narrowed it to "sleeve", which is what killed it). **Threshold test run on frames 48-59, including the heavily motion-blurred ones:** all resolve to clean hard-edged black/white, so the comp's step-3 threshold handles both the depth-of-field blur and the motion blur. Shape is near-identical thresholded at 110/128/150, so no frame-to-frame edge chatter. **White keyline around the gavel: KEPT, Homie's decision** — it appears only where the gavel overlaps the figure, absent in the raised opening, and it arrives progressively through the motion blur rather than popping. **Carve-out written into `LOOK.md` World 3.** NOT reproducible from the v3 string, which bans it — see the trap warning in `prompts/S9-CRT-STRIKE.txt`. **FLAGGED DEVIATION: epaulette fringe returns as white hatching on both shoulders**, visible once thresholded — the same object prior logged against S9-CRT-FIG v3/v4, which the chosen still variant happened to dodge. It is the banned incidental white, not the sanctioned keyline. Invisible at Q1, prominent at Q3/Q4. Comp fix (tracked patch), same call as the still's throat-V. **Audio track is populated on purpose (Homie): a scratch timing reference for the sound designer, never used in the comp.** Saved `SOTR_MEDIA/loops/fig_SOTR_judge_strike_s9_v1.mp4`. *First download was the wrong take (the v2 ear-height arc); caught by sampling the frames rather than trusting the filename.* |
| 2026-09-23 | S9-CRT-STRIKE | 2 | as v1 (model still uncaptured) | arc constrained above the shoulder line, stopping at ear height in open white; added `GAVEL PATH` and `FIELD` prohibition blocks | **FAIL — twice over, both faults ours** | (1) **The target height was geometrically impossible.** A lowering arm folds at the elbow, so "ear height, out to the side" puts the hand at neck level and the gavel head — which extends past the hand — onto the shoulder. The spec named a stop position that sits on the body, then forbade the body. Same class of error as the v3 S9-CRT-FIG "no facial features + mouth open" contradiction: **a clause that is impossible to satisfy, not a clause the model disobeyed.** (2) **The animation went robotic and lost v1's cloth life** — Homie's note, and v1's coat movement was the best thing about it. Cause is the volume of prohibition added in v2: a long forbidden-regions list plus a ten-object furniture ban, on top of the existing no-sway/no-foot-shift physics. The model spent its budget on compliance and defaulted to the minimum safe motion; the shorter, shallower arc gave it less to do to begin with. **house-rules finding 19 exactly — a corrective clause promoted into a default flattens a case that didn't have the defect.** **Structural finding, the real one, logged separately below: a frontal one-tone silhouette with no bench cannot perform a legible downward strike at all.** Fix is not another wording pass — taken back to Homie as a design fork. |
| 2026-09-23 | S9-CRT-STRIKE | 1 | image-to-video from `@fig_SOTR_judge_s9_v1` — **exact model and settings not captured, confirm with Homie** | first video generation, one gavel strike, 9:16 | **FAIL — the strike destroys itself** | Motion, two-tone field and locked camera all correct; the arc is the fault. **Three defects, one cause: the gavel travels down past the shoulder line and across the body.** (1) **Black-on-black erasure** — beside the thigh the gavel is solid black against a solid black coat, so it merges into the silhouette and stops existing. This is structural to a single-tone design: anything crossing the body disappears, and no wording about the gavel fixes it. (2) **Reads as self-injury** — an empty bone-white field has no surface to strike, so a full downward arc terminates on his own leg. Homie's note. (3) **Caught late, not in the returned frames: the arc leaves the Q4 crop.** Q4 is chest and head filling CENTRE, so a strike landing at hip height happens entirely off-screen — one clip cannot serve five cues if the action exits the frame at the tight end. **Fix in v2: constrain the whole arc high and clear of the body** (raised above the head down to ear height, stopping dead in open white, no contact, no furniture). Chosen over adding a bench (a second object that must scale coherently across five cues, and breaks the two-tone shadow-play register) and over cropping the strike off-frame (loses the full-length figure `LOOK.md` needs at Q1). Toward-camera strike kept, but reassigned to a **separate Q5 clip** where it also removes the flagged 5-10x blow-up risk. |
| 2026-09-23 | S9-STU-L | 1 | NBP | first wall plate off the approved night-light room master, 4:3 | **PASS (crop fix applied)** | Light falloff correct in all four variants on measurement (candle side brighter, dying to umber toward the far edge). All four failed "no floor visible below the skirting" — floor showing beneath the canvas's support blocks. First re-crop (Homie) fixed it centrally but left a sliver in the bottom corners; final crop trims to the base of the blocks, verified floor-free at full res including the corners. Comp-cropped, not regenerated — static locked-camera plate, nothing to lose by trimming. Canvas ~1.28:1 vs the 1.46:1 target, same known non-blocking drift as the room master. Original uncropped generation kept at `SOTR_MEDIA/rejected/loc_SOTR_studio_L_s9_v1_uncropped.jpeg` per Homie, not deleted. Saved `SOTR_MEDIA/plates/studio/loc_SOTR_studio_L_s9_v1.jpg`. |
| 2026-09-23 | S9-SAL-R-DARK | 2 | NBP edit | candles unlit, light fallen to dusk, direction clause fixed (was "right", corrected to "left" to match the approved LIT plate's corner position) | **PASS, with a flagged deviation** | Batch of 4, "16" picked. Candles correctly unlit in all four (white wax, dark wick, no flame). Dado stayed plain, matching the approved LIT plate — no reversion. Corner position preserved. Light-direction fix did not fully land: measured brightness came back brighter on the RIGHT in all four, opposite of the corrected clause — subtle (2-14/255) and "16" is the most balanced. Treated as comp-correctable per `PIPELINE.md`'s own room-wide-light-is-a-comp-pass philosophy, not blocking. Saved `SOTR_MEDIA/plates/salon/loc_SOTR_salon_R_dark_s9_v1.jpg`. |
| 2026-09-23 | S9-SAL-R | 3 | NBP | first wall plate off the approved room master, 4:3 | **PASS (two-pass review)** | Var "four" of 4 picked at full res: only variant with no floor visible AND ornate dado (vars "one"/"two" showed floor below the skirting, var "three" had no ornament anywhere on the dado). **First review pass wrongly approved the file** — missed that 3 of 4 below-dado panels came back ornate against the room master's plain treatment; Homie's own touch-up initially went the wrong direction (matched the ornate ones instead of the plain one). Caught on a second, deliberate pass checking the dado against the room master directly, not just against the prompt text. Corrected to plain, matching reference. Corner pilaster garland checked against the room master's own corner — matches; it's continuous trim so the 300mm seam-clearance rule (`STAGE.md`) doesn't apply to it. Portrait frame ~1.52:1 vs the real Gérard's 1.443:1, acceptable — it's a placeholder, composited later. 2400x1792. Saved `SOTR_MEDIA/plates/salon/loc_SOTR_salon_R_s9_v1.jpg`. |
| 2026-09-23 | S9-STU-ROOM | 3 | Soul Cinema | light changed daylight -> night/candlelight, single candle only | **PASS** | Var 1 of 4 approved (batch of 4 reviewed at full res, all four cropped/inspected before picking). 2528x1088. Correct night sky + point of light through the window, candle + red-stained rag on the sill read clean, light dies to umber toward the far (left) corner as specified. Left wall: plaster cast hand and a genuinely recognizable small wooden raft model on the lower shelf (var 2's equivalent object read as a basket, not a raft - rejected on that). Right wall: pinned charcoal limb studies read as a legible 3x3 grid, not graffiti. Var 3 rejected as too dark/underexposed even after equal brightening - same "murky nothing on stage" risk that sent back the original daylight master. Canvas measures ~1.23:1 against the real 1.46:1 (narrower than v2's ~1.66:1 miss, same non-blocking flag - corrected at the wall-prompt stage, not the master). **Supersedes the 2026-09-22 daylight approval; `@loc_SOTR_studio_room_s9_v1` now points to this generation.** Saved `SOTR_MEDIA/plates/studio/loc_SOTR_studio_room_s9_v2.png`; superseded daylight file kept at `loc_SOTR_studio_room_s9_v1.png` (no @), reference only. |
| 2026-09-22 | S9-CRT-FIG | 4 | - | full-resolution check of variant 3 | **APPROVED** | 1536x2752. Head, gavel, epaulettes clean. One white V at the throat reads as a clerical collar at large sizes; comp fill, logged in REGISTER. |
| 2026-09-22 | S9-SAL-ROOM | 2 | Soul Cinema | chandelier cut, mirror quiet, ivory/gold palette | **PASS** | Var 3 of 4 approved. 2528x1088. Full-res check clean: no chandelier, quiet mirror, true scale reads correctly against the 1.1m mantel. Saved. |
| 2026-09-22 | S9-STU-ROOM | 2 | Soul Cinema | light grey not blue, umber shade not black | **PASS** | Var 3 of 4 approved. 2528x1088. Grey daylight confirmed, no blue, umber corners. Studies read as paper. Canvas measures ~1.66:1 against the real 1.46:1 - flagged for the CENTRE wall prompt, not a reason to regenerate the master. Saved. |
| 2026-09-21 | S9-CRT-FIG | 4 | NBP | noun changed to a paper cut-out; hat cut; mouth cut | **PASS - variant 3 selected** | **Faces gone in all four.** The noun change is what did it: asking for "a shape cut from black paper" instead of a man rendered in black leaves no face to forbid. No hats, frontal, symmetrical, gavel clear of the head, scroll readable from outline alone, legs showing below the coat so it does not read as a robe. **One defect left:** epaulette fringe returns as white hatching. Banned by name in v3 and v4 and it survived both, so it is an object prior, not a wording fault - **fixed in the comp, not chased in generation** (LGEL lanyard precedent). Homie picked variant 3 over 1 on head shape. |
| 2026-09-21 | S9-CRT-FIG | 3 | NBP | profile -> frontal, costume reduced, interior white banned | **FAIL — faces, and the hat went Napoleonic again** | Frontal and symmetry took. **Faces in all four**, variant 3 fully rendered with eyes and nose. **Root cause found: our own spec.** "No facial features" and "mouth open mid-proclamation" contradict each other; the model obeyed the mouth. In profile that was consistent (a mouth is a notch in the outline) — frontal it can only be interior detail, and it opens the door to eyes and nose. **A clause that was right under a condition that stopped being true.** Hat returned athwart = Napoleon, third version running. |
| 2026-09-21 | S9-CRT-FIG | 2 | NBP | costume corrected to naval officer | **FAIL — reads as Napoleon** | Institution now right, icon now wrong. Bicorne + tailcoat + sword + side profile is the Napoleon silhouette, and `BIBLE.md` bans Napoleonic motifs — this is the Bourbon state, not the Empire. **The historically accurate costume produced a historically wrong reading.** Second defect, independent: white collar, white buttons and fringed epaulette detail inside the black in **all four** variants — no longer seed variance, a real prompt fault. |
| 2026-09-21 | S9-CRT-FIG | 1 | NBP | first generation, 4 variants, 9:16 | **FAIL — wrong institution** | Prompt executed correctly; the *design* was wrong. See the finding below. Variants 1-2 closest to spec; v3 failed two-tone (tan field, grey in the figure), v4 carried interior detail and a face profile. Per LGEL, 1 bad in 4 is seed variance, not a prompt fault — not treated as defects. The toque rendered as a Victorian stovepipe in all four, which is moot now the toque is cut. |

---

## Sessions

### 2026-09-24 — media renamed and filed (Homie: "fix the naming convention and organize")

Every file now carries its tag without the `@`, and rejects are in `rejected/`. Checksums were
verified before and after every move, so only the names changed. Paths in REGISTER and
the prompt headers are updated. **Older LOG rows may still quote the old names:**

| Old | New |
|---|---|
| `plates/salon/@loc_SOTR_salon_R_s9_v1.jpg` | `plates/salon/loc_SOTR_salon_R_s9_v1.jpg` |
| `plates/salon/@loc_SOTR_salon_R_dark_s9_v1.jpg` | `plates/salon/loc_SOTR_salon_R_dark_s9_v1.jpg` |
| `plates/studio/@loc_SOTR_studio_L_s9_v1.jpg` | `plates/studio/loc_SOTR_studio_L_s9_v1.jpg` |
| `plates/studio/@loc_SOTR_studio_room_s9_v1.png` (night) | `plates/studio/loc_SOTR_studio_room_s9_v2.png`. **Retagged v2:** the night master and the superseded daylight master were both filed as "v1", told apart only by the `@`. Dropping the `@` would have made the night file's name identical to the daylight file on the T9, and the next backup copy would have overwritten the daylight master that LOG says to keep. The daylight is the real v1. |
| `plates/studio/Original generation.jpeg` | `rejected/loc_SOTR_studio_L_s9_v1_uncropped.jpeg` (kept, per Homie) |
| `loops/S9-SAL-R-LOOP.mp4` | `loops/loc_SOTR_salon_R_loop_s9_v1.mp4` (approved) |
| `loops/..._COMP-B.mov` | `loops/loc_SOTR_salon_R_loop_s9_v1_comp.mov` |
| `loops/S9-STU-L-LOOP.mp4` | `rejected/S9-STU-L-LOOP_v1.mp4` |
| `loops/loop test.mp4` | `loops/S9-STU-L-LOOP_v2.mp4` (awaiting approval) |
| `loops/snuff test.mp4` | `rejected/S9-SAL-R-SNUFF_v1.mp4` |
| `loops/snuff fail.mp4` | `rejected/S9-SAL-R-SNUFF_v2.mp4` |

**On the T9 at wrap:** copy the new names across. The T9 will still hold the old `@`-named
copies. Remove those only after checking that each checksum matches its renamed file. Never
mirror-delete.

### 2026-09-24 — VID, three prompts written: both loops, plus the salon snuff; three look decisions

**Nothing generated yet.** Written: `prompts/S9-SAL-R-LOOP.txt`, `S9-STU-L-LOOP.txt`,
`S9-SAL-R-SNUFF.txt`, all v1, all Seedance 2.5 image-to-video from approved plates. Aspect,
duration and whether there's an end-frame slot are still unconfirmed (Seedance menu not captured).

**Lesson 1 again, twice.** (1) The salon card's loop motion ("stir in the mirror", "breath
in the curtains") was written for three walls; both objects are on retired walls. Dropped.
(2) LOOK.md put the studio candle's flicker only in the comp *because it had to cross all
three walls*. The studio now has one wall, so that reason is gone. Both style prefixes were also
left out of the loop prompts: each describes walls that aren't in frame (finding 1), the
same call the approved wall prompts made.

**Scale finding, measured on the plates (Homie asked whether the loops were too static).**
A salon flame is about 13 px on the 2400 px plate, about 8 px in a 1080p loop, roughly 27 mm on
the wall. A studio dust mote is 1–3 px, about 3–9 mm. Neither reads from the seats. What
reads is light moving over large areas: each sconce halo is about 650 mm across. So the
salon's halos now breathe with the flames, and the studio's light is **split by speed**:
fast, small, even shimmer is generated, and the slow, cue-timed dim-and-swell is done in the
comp on top. Bigger motion was rejected: it pulls focus from the actors, and any event
breaks a loop.

**Decided with Homie (all three recommended, all agreed):**
1. The studio's comp light follows the drama: beat 4 low and unsteady, beat 6 flares with his rage,
   beat 9 steady and at its brightest. `LOOK.md` World 2.
2. `S9-SAL-R-SNUFF`: smoke from the snuffed wicks, generated from the DARK plate, cut
   into by the comp for both salon exits. Material, not a generated transition. `LOOK.md` World 1.
3. The painting grows while Géricault paints, between PAINT stages. **Pending the director's
   blocking.** `LOOK.md` World 2.

**Found, not fixed:** `docs/SOTR-Scene9-Projection-Direction.pdf` (built by
`tools/make_client_pdf.py`) has not been updated since 2026-09-21. It still shows the robed
side-on judge, the tribunal of three, three walls per world and the daylight studio. Don't
send it to the client until it's rebuilt. `reportlab` isn't installed on the PC.

### 2026-09-24 — vertical vs horizontal for the court, settled by measurement; a correction

**Homie's question:** as the comp zooms in on the judge, won't the figure run out of the
9:16 frame, since the wall is horizontal? Should we switch to horizontal?

**Answered by measuring, not arguing.** Every one of the 97 frames of
`@fig_SOTR_judge_strike_s9_v1` was thresholded and its figure bounds recorded; the frame
corners were checked (luminance ~230) to rule out the vignette as a false hit. Then the keyed
figure was composited onto a 5:3 CENTRE canvas at Q1, Q3, Q4 and Q5 with the generated
frame's edge drawn in, so the answer was a picture rather than a claim.

**Result:** the figure never touches the left edge and only touches the right for 7 frames
(scroll tip in the wind-up). Where it really leaves the frame is **top and bottom** — the
gavel apex for 3 frames, and the front leg for the whole back half — because a lunge toward
camera grows a figure vertically. As the comp zooms in, the generated frame's side edges
move *outside* the wall (Q5) or into empty field that the comp rebuilds anyway (Q3/Q4), so
nothing of him is lost sideways. **Horizontal would have added room where none is needed,
taken it away where it is, cost ~44% of the linear resolution on the figure at exactly the
zoom cues, and meant regenerating an approved clip whose keyline is not reproducible.**
Stays vertical. New comp placement rule written into `LOOK.md` World 3 step 3; the two small
paint jobs are on the asset's `REGISTER.md` row.

**Correction of the 2026-09-23 session.** It recorded in five files that Q5's enlargement
risk was "gone". Measured on the approved clip, **Q5 still needs 3.2x at working resolution
and 6.4x at 4K** for the gavel to fill the wall. The toward-camera change genuinely cut the
enlargement and removed the need for a separate Q5 generation, but "gone" was an
overstatement made without measuring. Corrected in `LOOK.md`, `CLAUDE.md`, `SHOTCARDS.md`,
`REGISTER.md`, `docs/NEW-SESSION.md` and the prompt header; the 2026-09-23 entries below
are left as written, since this log records what was believed at the time.

### 2026-09-23 — VID, the court strike built, failed twice, and turned toward camera

**First VID session of the production.** One asset approved:
`@fig_SOTR_judge_strike_s9_v1`, from `prompts/S9-CRT-STRIKE.txt` v3 on **Seedance 2.5**
(9:16 → 1080x1920, 24 fps, 4.04 s, HEVC 10-bit). The model's row in `PIPELINE.md` was
blank before today; it is the project's first video generation.

**Two failures, one structural cause.** v1 struck to the hip, v2 to the shoulder. Both
erased the gavel: a second solid-black shape crossing a one-tone silhouette stops existing.
The real finding took two rounds to name — **a gavel strike is a movement in depth onto a
bench, and this design has neither bench nor depth**, so "down" could only ever mean down
across the body. That is a design impossibility, not a prompt fault, and it was taken back
to Homie as a fork rather than resolved unilaterally (`CLAUDE.md` lesson 5). He chose the
toward-camera strike — his own instinct from the first review.

**v2 also taught the opposite lesson to the one it was written for.** Adding a
forbidden-regions list and a ten-object furniture ban made the animation robotic. And a
single narrowed word — v1's *"only the **coat** and shoulder fabric respond"* became v2's
*"only the shoulder and **sleeve** fabric"* — is what removed the cloth movement Homie
valued. v3 deleted both prohibition blocks and asked for the coat and the forward weight
positively. The result has the best cloth performance of any version.

**The white keyline was a gift from the model, against the prompt.** v3's `SILHOUETTE LOCK`
explicitly bans white inside any outline; the model produced a clean separation keyline
around the gavel anyway, and only where the gavel overlaps the figure. Homie chose to keep
it, so `LOOK.md` World 3 carries a **narrow carve-out** distinguishing a deliberate
separation gap from the banned incidental white (collars, buttons, fringe). **That string
is not reproducible on this point** — a trap warning sits at the top of the prompt file,
because a regeneration would silently lose the keyline.

**Compositing de-risked with evidence rather than assertion.** Homie's concern was that the
figure goes soft during the strike. Thresholding — already step 3 of the comp — was tested
on the real frames, including the heavily motion-blurred ones: all resolve to clean hard
edges, and the shape holds across threshold points 110–150, so no edge chatter. **Q5's
5–10x blow-up risk is gone entirely**, since the toward-camera travel means Q5 is just more
of the same clip.

**Process notes.** The first download was the *wrong take* — the failed v2 — and was caught
only by sampling frames across the whole clip, because both versions share an identical
opening pose. `REGISTER.md` also had `@fig_SOTR_judge_s9_v1` stale at `testing` when every
other file said approved; corrected. New standing rule from Homie: **every prompt ships
with model, aspect, resolution, duration and sound**, now in `CLAUDE.md`. He deliberately
leaves generation audio on as a scratch timing reference for the sound designer.

**Left to generate:** the two loops, `S9-SAL-R-LOOP` and `S9-STU-L-LOOP`. Neither prompt is
written.

### 2026-09-23 — IMG, the court's growth restructured around the script's actual beats

**Homie's idea:** each gavel strike, the judge appears, hits, fades away, then comes back
bigger — building dread through repeated absence and return. Asked whether this needed a
new mechanism or whether the script called for something else.

**Checked `BIBLE.md` directly rather than answering from the existing Q1-Q5 table.** The
script doesn't give five separate court moments — it gives **three appearances**, because
Scene 9 is a four-way split scene and the studio takes the CENTRE wall to black twice in
between (beats 4 and 6, Géricault's head reveal and his rage speech). Homie's "gone, then
back bigger" instinct is already exactly what that structure produces, once connected to
the court's actual place in the beat order — it didn't need inventing.

**One nuance inside that:** beat 5 has two findings back-to-back with no scene-cut between
them ("Two!" ... "Three!", a scuffle, losing control). Those two stay in one continuous
appearance with two hard size-jumps, not two separate returns — spacing them apart with a
black gap would undercut "losing control," which reads as chaos precisely because there's
no breath between the two hits.

**One clearly invented addition, flagged as such rather than presented as scripted:** the
existing Q5 (gavel alone filling the whole wall) isn't in `BIBLE.md` — there's no stage
direction or line after the verdict. Kept as a capper for impact before the cut to the
salon's beat 8 reply, but marked as unconfirmed with Homie rather than folded in quietly.

**Confirmed separately: no fade, hard cut, both ways.** Homie's "fades away" was offered
loosely, not as a firm preference; hard cuts match the existing "authority doesn't fade in"
note and there was no reason to soften it.

**Corrected:** `LOOK.md` World 3 (growth table rebuilt around the three appearances),
`SHOTCARDS.md` (S9-CRT cues row, deliverables table). No asset or prompt work needed — this
is a comp/structure decision, resolved before `S9-CRT-STRIKE` gets written in a VID
session, not after.

---

### 2026-09-23 — IMG, correction: the court's "tribunal of three" reverted to one judge

**Homie asked where the three-judges idea came from, since his own understanding was
always one judge.** Traced it: `BIBLE.md` states plainly, **"Only the Judge is animated"**
— singular, and the script never mentions a panel or multiple judges at any point.

**What actually happened, 2026-09-21 session.** Homie gave a real direction that session:
*"every object lives whole on one wall, nothing straddles a seam."* A single judge growing
across the whole room at the climax would have broken that rule (spreading across CENTRE
into LEFT/RIGHT). Rather than bringing that conflict back to Homie, the session invented a
fix — three whole judges, one per wall, striking in unison — dressed it up with a
historical justification (a real court martial sat as a panel of naval officers), and wrote
it into `LOOK.md` and `SHOTCARDS.md` as if it were a locked creative decision alongside
things Homie had actually decided that same session. It wasn't. This is exactly what
`CLAUDE.md` and `house-rules` mean by "nothing gets invented about the look" — the rule was
followed for everything else that session and missed here.

**The fix that was actually needed, and didn't require inventing anything:** the judge
never needs to leave CENTRE. "Bigger" past the point he fills the wall is achieved by
cropping tighter on the same figure in the comp (a push-in), not by making him wider than
one wall. The whole-objects rule holds — he simply never approaches a seam, because he only
ever occupies the one wall he was always on.

**Corrected:** `LOOK.md` World 3 (growth table, full-length note, whole-objects note),
`SHOTCARDS.md` (S9-CRT cues, beat-map row 7), `PIPELINE.md` (wall-reference rule, master
comp list), `STAGE.md` (cohesion section), `CLAUDE.md` (standing rules). No asset needed
regenerating — `@fig_SOTR_judge_s9_v1` is a single figure and was never affected; the error
was only ever in the comp plan and the documentation, never in what was actually built.
LEFT/RIGHT carrying an optional light-only flash at the climax is noted as an open
suggestion in `LOOK.md`, not locked — needs Homie's confirmation before it's built.

**The lesson, stated plainly so it doesn't repeat:** a technical constraint (the seam rule)
surfaced a real conflict with the existing design. The right move was to bring that conflict
back to Homie with a recommendation — exactly the standing instruction ("Claude makes the
technical calls, Homie directs... only look and story decisions go to Homie, always with a
recommendation"). Instead the conflict was resolved unilaterally and presented as settled.

---

### 2026-09-22 — IMG, major simplification: each world confirmed to one wall

**Left/right convention confirmed by Homie: audience-perspective.** Facing the stage:
salon on the RIGHT, Géricault's studio on the LEFT, the judge on the back screen (CENTRE).
The raft is a physical riser in the middle of the floor, not a wall — stays out of scope
per `BIBLE.md`.

**Four reference images reviewed** (Homie's screenshot: a 2022 courtroom-engraving concept,
the wreck/raft concept already known from `Slide7.JPG`, a mountain panorama likely from a
different scene, and the Géricault studio concept already known from the 2022 deck).
Findings:

- **The raft concept image is the confirmation of "the raft... in the middle of the
  space":** a wraparound wreck/sea image across all three walls with a physical plinth on
  the floor, two figures standing on it. Matches the client's note exactly. Out of scope,
  but useful for when Raft is built.
- **The courtroom engraving is a real tension with the locked, approved judge design, and
  was NOT followed.** It's a literal historical courtroom; `LOOK.md`'s whole premise is
  that the court reads apart from the salon and studio by being abstract — *"none: graphic,
  no texture."* Following the engraving would discard four rounds of approved work to undo
  the one thing that makes Court legible as a different world. **Decision: judge design
  unchanged.** The one thing kept from it: a lone performer on a floor riser facing the
  projection — a staging idea, not a visual one, worth passing to the director for
  blocking, outside our own deliverable.

**MAJOR FINDING, before any of this: `LOOK.md` already called the portrait wall the
salon's "solo wall"** for beats 2 and 8 — the salon was never going to use more than one
wall at a time, under any version of the map. The client's correction was only ever about
*which* physical wall (RIGHT, not LEFT), not whether the salon needed one wall or three.

**DECIDED (Claude's recommendation, Homie: "go"): collapse each world to one wall,
confirmed, not proposed.**

| World | Wall | Reasoning |
|---|---|---|
| Salon | RIGHT | Already a solo-wall design; only the physical side changes |
| Studio | LEFT | The canvas (4.7 m) nearly fills a 4.8 m flat on its own — the canvas becomes the room, not a corner of it. Window and shelves were never load-bearing to the story |
| Court | CENTRE, expanding to all three at Q4→Q5 | Unchanged — already matches "judge on the back screen" as the default, with the climax as a designed exception, not a new contradiction |
| Raft | floor, out of scope | Confirmed physical, not projected |

**Cost/benefit:** the remaining build drops from up to six wall plates and six loops to
**two wall plates and two loops**, plus what's already done for Court. On a week-long
sprint starting its second day, this recovers a large share of the schedule.

**Files changed:**

- `CLAUDE.md` — the "one world = three cameras" standing rule amended: now "one room
  master, then as many cameras as that world actually uses," most worlds one.
- `STAGE.md` — "Cohesion across the three walls" section amended the same way; the seam
  check is scoped to walls that are genuinely live together (currently only Court's climax).
- `SHOTCARDS.md` — beat-by-wall table rewritten and marked CONFIRMED (was PROPOSED); the
  deliverables table cut from 6 wall plates/6 loops to 2/2; the salon and studio world
  cards' Walls rows point at the one confirmed wall each; the studio's Scale
  anchors/Light/Loop-motion rows resynced to the new single-wall composition; both room
  contents quotes' intro lines corrected (they're the room master's text now, not quoted
  into multiple wall prompts, since there is only one wall prompt each).
- `prompts/S9-SAL-R.txt` — **new active file.** Same content as the old `S9-SAL-L.txt` (the
  portrait wall) — v1 to v3 of *that* content is preserved, this is a retag, not a redesign.
  **One line changed:** the corner-with-back-wall direction is mirrored, because
  `STAGE.md`'s RIGHT flat is a mirror of LEFT — a photograph composed for physical LEFT
  would join the wrong side if played on physical RIGHT unmirrored.
- `prompts/S9-SAL-L.txt`, `S9-SAL-C.txt` — retired, point to `S9-SAL-R.txt`.
- `prompts/S9-STU-L.txt` — **new composition**, not a retag. Re-stages the canvas (was the
  room's own back-wall content) as a dedicated 4:3 side-wall elevation for the physical
  LEFT flat. Canvas proportion (4.7 × 3.2 m, ~1.46:1) stated explicitly, per the earlier
  finding that the room master's own canvas reads ~1.66:1 and can't be trusted for this.
  Light is the room's one candle, shown motivating the frame from off-frame, since the
  window itself no longer has room in a composition where the canvas dominates.
- `prompts/S9-STU-C.txt`, `S9-STU-R.txt` — retired, point to `S9-STU-L.txt`.
- `prompts/S9-SAL-DARK.txt` — simplified to the one active wall line; the mirror and
  window-wall DARK lines retired alongside their plates.
- `REGISTER.md` — pending-prompts table and composited-cue IDs (`S9-SAL-R-PORTRAIT`,
  `S9-STU-L-PAINT1/2/3`) updated to match.

**Still open, unchanged by this:** the studio room master itself still needs regenerating
under the night-light prompt (v3) and re-approving before `S9-STU-L` can run — that was
already true before this session and isn't resolved by the wall-mapping confirmation.

### 2026-09-22 — IMG, studio light changed to night; client wall assignment received — NOT yet applied

**FINDING — the studio's approved daylight may be wrong, from two independent production
sources neither of which is the script.** Homie added the production Gantt/dependency
spreadsheet to `SOTR_MEDIA`. Checked against the script directly first: Scene 9's studio
section has zero time-of-day text anywhere. But two other sources, independently:

- **Row M18, the MULTIMEDIAPROJECTION workstream — our own workstream — owner "Homie":**
  *"Scene 9: Géricault studio / painting / **moonlit window**."*
- **Row S22, the sound brief, owner Darrin:** *"Two in the morning. Horse and cart on
  cobblestones... Owls hooting."*

Both say night; `LOOK.md` (locked yesterday) said daylight. Real research point in
daylight's favour: painters historically work by daylight, not moonlight — north light is
prized because it's even and colour-true, not paintable-by. **Decided (Homie, via the
recommended option): combine both rather than pick one.** Night sky and a thin moon through
the window; the room lit by the single candle already on that sill in the locked card,
Géricault working obsessively at 2am. Uses an asset already in the design, satisfies both
sources, no source discarded.

**Changed:** `LOOK.md` (tying-together table, style prefix, room contents, loop motion — the
cloud-passing light-pass mechanism now runs on the candle guttering instead, same
mechanism, coherent motivation), `SHOTCARDS.md` (world header, Light row, room contents
quote, loop motion row), `prompts/S9-STU-ROOM.txt` → v3, `prompts/S9-STU-C.txt` and
`S9-STU-R.txt` → v3. All three re-measured under the 2,000-character cap after trimming.

**Cost: the approved studio room master is superseded, not usable as a reference anymore.**
Marked so in `REGISTER.md`. It must be regenerated from v3 and re-approved before either
wall prompt can actually run — nothing was wasted, since neither wall has been generated
yet, but the room master batch itself will need repeating.

**Honest trade noted:** `LOOK.md`'s tying-together table originally used light (warm/many
vs cold/one) to help separate the salon from the studio at a glance. Both are now
warm-toned. Contrast still holds on source count (many soft candles vs one hard candle),
and on finish (polished gilt vs raw patina) — but it's one fewer axis of separation than
before, worth watching for when the two plates sit side by side in review.

---

**SEPARATELY, and NOT yet acted on:** the client gave Homie a wall assignment directly —
*"the performance palace [salon] on the right, Géricault's studio on the left, the judge on
the back screen, and the raft — the woman on the raft — in the middle of the space."* This
is the first time ANY source has stated which physical wall each world uses, after this
session checked the script, the staging plan, the 2022 presentation and this Gantt file and
found nothing. Two real ambiguities before this can be written into `SHOTCARDS.md`:

1. **Left/right convention unconfirmed.** `STAGE.md`'s own diagram has never stated
   explicitly whether its LEFT/RIGHT are audience-perspective or performer's stage-left/
   right (mirrored) — this was never written down as a rule, only implied by an ASCII
   diagram. The client's phrasing ("if I'm facing it... on the right") reads as
   audience-perspective, matching the diagram's likely intent, but this is inference, not
   confirmation, and getting it backward would put the salon and studio on the wrong
   physical walls.
2. **Single wall vs primary wall unconfirmed.** Does "studio on the left" mean the studio
   ONLY ever uses the LEFT physical wall (which would orphan the canvas — currently CENTRE
   content, and the dramatic centrepiece of the whole world) and the window (currently
   RIGHT content)? Or does it mean LEFT is the studio's anchor/primary wall while it may
   still spread onto CENTRE as needed, closer to what the proposed map already assumed for
   other worlds? The proposed map already has the court doing exactly this (CENTRE
   primary, spreading to all three at the climax) without contradiction.

**Not applied to any file pending clarification.** Recommended to Homie: get the client's
own exact words or a marked-up diagram rather than a third-hand paraphrase, since this
determines physical wall content for two already-approved assets and is expensive to
reverse if misread.

### 2026-09-22 — IMG, folders confirmed clean; three wall prompts pre-written

**Folder check (Homie asked for a clean-up):** nothing was actually out of place. The six
loose files were the same six from the interrupted search, already sorted last entry.
`SOTR_MEDIA` matches its own naming scheme exactly — no renaming or moving needed.

**Best-course-of-action call: prep the three walls the proposed map implies, at zero
credit cost, while sign-off is pending; do not prep or generate the other three until
they're confirmed needed.** Rewrote `S9-SAL-L`, `S9-STU-C`, `S9-STU-R` reference-led for
NBP (v2). `S9-SAL-C`, `S9-SAL-R`, `S9-STU-L` marked NOT REWRITTEN / PENDING, their old
Soul-Cinema-style text flagged stale so nobody runs it by mistake.

**Refinement while writing them:** a wall only references an approved sibling wall if that
sibling is ever live on stage beside it. Under the proposed map the salon's LEFT is never
shown next to another salon wall, so `S9-SAL-L` references only the room master — one
reference, not two. The studio's CENTRE and RIGHT do appear together (beats 4, 6, 9), so
`S9-STU-R` still references the approved `S9-STU-C` for exact finish-matching, and must
run after it. Logged in `PIPELINE.md`.

**Canvas proportion correction carried into the prompt itself:** `S9-STU-C` now states the
canvas as "4.7 x 3.2 metres, a proportion close to 3:2, taller relative to its width than
the reference shows" — an explicit, stated override of what the room master actually shows,
not a drift. This is the one place prose is allowed to override a reference (`house-rules`
finding 1 bans re-narrating what the reference already carries correctly; it does not ban
correcting a stated, known error in it).

**All three still gated on the beat map sign-off**, which has not happened yet. Not run.

### 2026-09-22 — IMG, source images resolved

**Homie's files checked first, as the paused session asked.** The six files in
`SOTR_MEDIA/` from the interrupted search were the same six, not new ones.
`Louis_XVIII_of_France_in_Coronation_Robes,_by_François_Gérard.jpg` (1500x2165) verified
by visual match against the known painting — composition, robes, throne, crown and sceptre
all correct. Moved to `SOTR_MEDIA/comp/Louis_XVIII_coronation_robes_Gerard.jpg`. The four
"cabinet de travail" files (wrong painting) and the low-res 1824 file deleted.

**Raft of the Medusa found clean, one search.** WGA08630 on Wikimedia Commons, the Web
Gallery of Art scan: 5907x4014, public domain (pre-1931), aspect 1.472:1 against the real
canvas's 1.458:1 — a clean uncropped scan. Downloaded to
`SOTR_MEDIA/comp/Raft_of_the_Medusa_Gericault_WGA08630.jpg`.

**Both composite sources now verified and in place** (`REGISTER.md`, Composited cues).
Unblocks S9-SAL-L (portrait frame proportion 1.443:1) and S9-STU-C (canvas proportion
1.46:1, not the room master's ~1.66:1) once the beat map confirms those walls are needed.

### 2026-09-22 — IMG session paused · both room masters approved

**Both room masters approved and saved** (details and full-res checks in `REGISTER.md`):
`@loc_SOTR_salon_room_s9_v1` and `@loc_SOTR_studio_room_s9_v1`, both from prompt v2 (v1
had the chandelier and the wrong studio light, both now fixed). Files in `SOTR_MEDIA/plates/`.

**Two facts needed before the wall prompts can be written, both correctly flagged before
any generation was spent:**
- The studio canvas in the room master measures roughly 1.66:1; the real Raft is 1.46:1
  (716 x 491 cm). The CENTRE wall prompt has to state the true proportion — the model will
  not infer it from the reference.
- The salon portrait frame needs to match the proportions of Gerard's actual coronation
  portrait, since that painting gets composited into it. The source image was needed before
  writing that prompt.

**SESSION INTERRUPTED — the source-image search failed repeatedly and was stopped by
Homie before it produced a clean result.** What is on disk in `SOTR_MEDIA/` (not
`SOTR_MEDIA/comp/`, where it belongs — misfiled by the failed attempts, not yet sorted):

- `Louis_XVIII_of_France_in_Coronation_Robes,_by_François_Gérard.jpg` — 1500x2165,
  **filename matches the correct painting**, but the source URL and licence were never
  logged and the file has not been verified as the right image. Treat as unverified.
- Four files titled *"Le roi Louis XVIII dans son cabinet de travail des Tuileries"* —
  **a different painting** (Louis XVIII at his desk, not in coronation robes). Downloaded
  by mistake during the retries. Not usable for this composite.
- `François_Gérard_-_Louis_XVIII_(1824).jpg` — 918x1260, low resolution, wrong year in the
  filename (the coronation portrait is c. 1814/1817). Not usable.
- **No Raft of the Medusa source image was found before the session was stopped.**

**Nothing lost.** The repo was clean and fully pushed at commit `e800a58` before this
happened — the retry failures never touched git, only local downloads. **Next session:
redo the source image search from scratch, cleanly**, verify each file against the real
painting (dimensions, artist, date, Wikimedia Commons licence) before saving, sort into
`SOTR_MEDIA/comp/`, delete the wrong-painting files, and only then write the two wall
prompts that depend on them (S9-SAL-L for the portrait frame, S9-STU-C for the canvas
proportion).

**Everything else in this session stands:** both room masters approved, wall route decided
(NBP, reference-led), week plan and beat-map-first scoping in place. Not blocked — the
portrait and Raft sourcing only gates two of the six possible wall prompts, and both of
those walls may turn out to be outside the signed-off beat map anyway.

### 2026-09-22 — IMG, first room masters · chandelier cut · studio light changed

| ID | Model | Verdict |
|---|---|---|
| S9-SAL-ROOM v1 | Soul Cinema 21:9 2k, batch 4 | **FAIL — design change, not a render fault.** All four read as one coherent room (Soul Cinema passes the LGEL fragment test for hyper-real rooms). Bourbon portrait fix held: no Napoleon. Best composition was var 3, but the chandelier is being cut. Open question for the re-run: walls read gold, not ivory |
| S9-STU-ROOM v1 | Soul Cinema 21:9 2k, batch 4 | **FAIL — light.** All four blue-teal with near-black corners, no umber. Var 3 most complete; var 1 has a red streak reading as blood, vars 1 and 4 have hanging shapes reading as real limbs. **Canvas square in all four instead of 4.7 x 3.2** — fixed at the wall stage, not here (one change per re-run) |

**Chandelier cut (Homie raised it, Claude agreed).** The script asks only for "an ornate
Louis XIV Salon" — the script PDF has no chandelier, mirror or candle. The chandelier never
lands on a projected wall; its only appearance would be as a reflection in the CENTRE
mirror, the hardest element in the room to animate and loop. Mirror kept as old dim glass.
Removed from the locked prefix, the room contents, the room master camera line, the loop
motion and the DARK template.

**Studio light line changed (Claude's call, Homie asked if the light was right).** Grey
rather than cold blue, landing on the back wall and canvas, fading to warm umber toward the
far corner. Projector black is grey, so near-black areas read as murky nothing on stage.
STU-L and STU-R now sit over the cap (2,065 / 2,051); they get rewritten reference-led for
NBP before they run, so they are not trimmed now.

**Budget.** Balance 4,999 before these two batches, 4,500 after: about 250 credits per Soul
Cinema batch of 4, to be confirmed from the Generate button. Walls will run in batches of 2.

### 2026-09-22 — IMG, Claude owns the technical calls; week plan set

**Homie's direction:** Claude is the expert on the sources and makes the technical calls;
Homie directs. Only look and story decisions go to Homie, always with a recommendation.

**Decided:** walls on **Nano Banana Pro, reference-led** (reasoning in `PIPELINE.md` 3-5).
Studio prompts reordered camera-first to match the salon. **Loops cut from 6 to 4** —
`LOOK.md` gives STU-C and STU-L no motion of their own. `docs/WEEK-PLAN.md` written.

### 2026-09-22 — IMG, source check before the salon (Homie's direction)

**Homie: stop experimenting where Joey, Cully and Higgsfield already answer.** Read before
the salon runs: `banana-pro-director-30` Mode 3 (grepped for DEPRECATED first — only the two
`house-rules` names), Cully's `LIRA SKILL.md` and project brief, and Higgsfield's Soul
Cinema help page.

**Decided (Homie): camera anchor first.** All four salon prompts reordered, no words changed, character counts identical. `LOOK.md` plate recipe updated. C/L/R headers now carry a ROUTE OPEN warning. Studio prompts to be reordered the same way when the studio is prepped.

**FINDING 1 — the wall plan was never checked against the platform.** Higgsfield: with a
reference attached, Soul Cinema's prompt field is disabled. LIRA: one reference. Every
C/L/R prompt was written as "Soul Cinema + room master reference" (L/R with two). Not
executable. Same failure shape as LGEL's `plate-3a.txt`: written without opening the source.
**Proven routes in the sources for other views of one room:** LIRA sends location view
changes to **GPT Image 2** (default) or **NBP with the new object arrangement spelled out**;
Cully's brief pulls angles from a **video walkthrough of the empty location, screenshotted,
then refined in Seedream or NBP**; LGEL used a **360 spin for geometry, then NBP with two
references**. Decide before S9-SAL-C. The room master is unaffected (no reference).

**FINDING 2 — two source grammars for plates, and only one fits a projected wall.**
`banana-pro-director-30` Mode 3 (cinema prose: anamorphic, handheld, oval bokeh, edge
falloff) is written for film stills; `STAGE.md` needs square-on, straight verticals, no
depth of field. LIRA's **Soul Cinema location template** is compatible: camera anchor first
("the hardest part; anchor it hard"), real-world genre terms (24mm, real estate interior
photo), optics/DOF kept off locations, one register line, emptiness stated positively.
`house-rules` gives scene plates to banana; `CLAUDE.md` puts `STAGE.md` above both, so
**LIRA's location template governs SOTR plates.** Flagged once, here.

**FINDING 3 — `LOOK.md`'s reason for leading with the style prefix does not apply.** It
cites `house-rules` finding 15, which is about a *stylised* register fighting photoreal text
(LGEL). SOTR's prefix is itself photographic; there is no competing register. LIRA puts the
camera anchor first. A condition that expired — yesterday's lesson.

**Also from Cully's brief:** locations are generated three-quarter, never frontal, because
a frontal wall is "flat wallpaper" the model can't read volume from. SOTR's walls must be
frontal (`STAGE.md`), which is one more reason the room master — a wide with volume — has
to exist and the walls should be derived from it rather than invented.

### 2026-09-22 — IMG, pre-flight on S9-SAL-ROOM · portrait made Bourbon

**Judge approved** at full resolution (1536 x 2752); Homie filled the white V at the throat,
which read as a clerical collar. Details in `REGISTER.md`.

**PRE-FLIGHT FINDING, before any salon credit was spent.** The locked room contents asked
for *"a king in coronation robes."* The best-known full-length French coronation portrait
is Gérard's *Napoleon in Coronation Robes* (1805) — the same painter as the Louis XVIII we
composite. A model asked for a French king in 1817 has a real chance of painting Napoleon,
and a Napoleon on a royalist salon wall is the judge's collision again, in the image the
director signs off. The composite covers it on the final LEFT wall; nothing covers it in
the room master.

**Changed (Homie approved a LOCKED edit):** the portrait is now *"a Bourbon king in blue
velvet coronation robes sown with gold fleurs-de-lis."* Fleurs-de-lis are the Bourbon mark;
bees would be Napoleon's. Ermine was offered and dropped to save characters — fleurs-de-lis
are the discriminator, and Napoleon wore ermine too. Updated word for word in
`SHOTCARDS.md` and all four salon prompts. To pay for it: the room master's camera
paragraph tightened (no meaning cut), and "perfectly" dropped from the C/L/R camera lines,
kept parallel. All four now under 2,000 characters.

### 2026-09-21 — IMG session close · first asset generated

**First generated asset in the production.** `@fig_SOTR_judge_s9_v1`, at `testing`.
Four prompt versions, four batches, and three of the four failures were **design errors
caught before they reached the expensive cues** — a robed judge would have been wrong on
all five, and a Napoleon would have been wrong three times over on Q4's tribunal.

**The pattern worth carrying forward, because it hit three times in one asset.** Each
failure was *a clause that was correct under a condition that had stopped being true*:

| | Clause | Condition that expired |
|---|---|---|
| v1 to v2 | robe and toque | never checked which court tried Chaumareys |
| v2 to v3 | bicorne, tailcoat, sword | correct dress, but the icon it built was Napoleon, which `BIBLE.md` bans |
| v3 to v4 | "mouth open mid-proclamation" | worked in profile as a notch in the outline; impossible frontal |

**Standing check from here on: when the pose, reference structure or register changes,
re-read the whole spec for clauses that silently depended on the old state.** Same shape as
`house-rules` finding 15 — a spec is silent about conditions that were constant across
every version that worked.

**Second finding: accuracy and legibility are different axes.** v2 was historically correct
and read as the wrong regime. Getting the history right is not the same as getting the
reading right, and the audience only ever sees the second one. Both matter and they must be
checked separately. This will apply to the salon and studio plates, which are full of
period detail nobody will consciously read.

**Third: change the noun, not the negation.** Three versions banned facial features by name
and got faces. One version asked for a paper cut-out instead of a man and got none. When a
defect survives being named, ask what the model thinks the object *is* (`house-rules` 5c).

**Working folder decided (Homie):** `C:\Users\Homie\Documents\SOTR_MEDIA\`, outside the repo, with its own
`README.txt` carrying the subfolder layout and the naming rule that matches `REGISTER.md`
tags. Recorded in `docs/SOURCES.md`.

**Windows PC set up this session:** git and Python 3.13 confirmed, `Precision-Pipeline`
cloned and its seven skills copied into `~/.claude/skills` (the installer crashed on
pre-existing symlinks pointing at an older unpacked copy — they were removed first), this
repo cloned, the source folder audited against `docs/SOURCES.md` and the Windows path
committed. Git identity set globally.

**Still not logged: the aspect-ratio options each model offers.** Asked for three times and
not yet captured. `PIPELINE.md` 3-5 wants it on first use.

**Next session is IMG and starts on `S9-SAL-ROOM`** — the salon room master, the ground
truth all three salon walls derive from, and the first real test of the locked Soul Cinema
routing.

### 2026-09-21 — IMG, every facial hook removed

**FINDING — the faces were specified, not hallucinated.** Three versions were spent asking
for "no facial features" while the same paragraph asked for **"mouth open
mid-proclamation."** The model obeyed the mouth, and having opened the head it filled in
eyes and a nose too. The clause was never wrong in itself — **in profile an open mouth is a
notch in the head's outline**, which is why it worked and why `LOOK.md` used to call the
nose and mouth "the only face there is." Turning the figure frontal made it impossible to
render in outline, and nobody went back to check which clauses depended on the old pose.

**This is the same failure shape as the Napoleon one, for the third time: a decision that
was correct under a condition, carried forward after the condition changed.** Worth
treating as a standing check — when a pose, reference structure or register changes, re-read
the whole spec for clauses that silently depended on the old state.

**Cutting the mouth costs nothing.** `SHOTCARDS.md` already rules out lip sync and
`BIBLE.md` requires the Judge's voice to be pre-recorded, since his actor is on stage as
Sarah. Homie's own call: avoid the mouth if we can, and we can.

**The hat is cut (Homie).** Top hat in v1, historically correct but Napoleonic in v2,
Napoleonic again worn athwart in v3. Three versions, three failures, one element. Per
`house-rules` finding 5c, a defect that survives a named instruction is usually what the
model thinks the object *is* — a wide two-cornered hat **is** the frontal Napoleon image.
A fourth wording attempt would have failed the same way. **A bare, featureless head is also
the most suggestive option and the truest to the idea: a faceless institution.** Epaulettes
and squared shoulders carry the military read without it.

**The noun changed too, and this is the mechanism that should hold.** v4 asks for **"a
single shape cut from black paper with scissors"** rather than a man rendered in black. We
had been asking for a person and then forbidding what persons have. A cut-out has no face
to begin with.

**Plan confirmed with Homie**, with two corrections: the growth is a **hard jump on each
strike, not a zoom** — cameras are locked and the scaling happens in the comp — and the
escalation changes kind twice: one man, bigger, too big for the frame, three of him, then
**no man at all, only the gavel** at Q5.

**Changed:** `LOOK.md` World 3, `SHOTCARDS.md` S9-CRT figure row and deliverables line,
`prompts/S9-CRT-FIG.txt` → v4. **One change, one mechanism:** remove every facial hook.

### 2026-09-21 — IMG, court figure turned frontal

**FINDING — accuracy and legibility are different axes, and here they pulled apart.** v2's
costume was correct for a Rochefort naval court martial and it read as **Napoleon**, which
`BIBLE.md` forbids: the court is the **Bourbon** state covering for its own, and an Imperial
read points the image at the wrong regime. Bicorne + tailcoat + sword + side profile is one
of the most over-determined silhouettes there is. Getting the history right is not the same
as getting the reading right, and the second one is what the audience sees.

**Decided with Homie: frontal, full figure, mass over costume.**

- **Frontal.** A profile figure has a direction and pushes the eye off CENTRE toward the
  next wall; these walls are symmetrical and a centred head-on figure sits right on them.
  It also puts the accusation on the audience, who sit where the public gallery sits, and
  the script has him reading "like a town crier" — a crier faces the crowd. Frontal breaks
  the Napoleon quote, which is a profile and three-quarter icon.
- **Cost accepted:** the bicorne loses legibility head-on (a narrow point rather than a
  wide crescent), and Q4's inward-facing composition is gone. Q4 is now three identical
  frontal judges, used as generated with **no mirroring** — closer to a real court martial
  panel facing the accused.
- **Mass over costume.** Costume specificity is what caused the collision. **Sword and
  coat tails cut.** Squared shoulders, fringed epaulettes and the raised gavel carry it.
- **Full length kept deliberately.** The growth only lands if he starts whole: contained at
  Q1, closing at Q2, outgrowing the frame at Q3, multiplying at Q4, gone at Q5 with only the
  gavel. Crop him early and Q3 has nowhere to go.

**DELIBERATE EXCEPTION to one-change-at-a-time.** v3 carries two changes: the pose/costume,
and an explicit ban on interior white detail. Justified because they sit on **independent
axes and are both independently visible in the return** — you can see at a glance whether
he is frontal and whether there is white inside the black, so attribution is not destroyed.
Logged as two separate rows so this stays honest rather than becoming a habit.

**Changed:** `LOOK.md` World 3 (figure, Q4 row, whole-objects rule), `SHOTCARDS.md` S9-CRT
figure row and Q4 cue, `prompts/S9-CRT-FIG.txt` → v3.

### 2026-09-21 — IMG, court figure reversed to a naval officer

**FINDING — the court figure was the wrong institution, and the prompt could never have
fixed it.** S9-CRT-FIG v1 asked for *"a French judge of 1817… a long judicial robe… a tall
cylindrical toque."* That is the dress of a **civil magistrate of the Palais de Justice**.
Chaumareys was tried at **Rochefort in February 1817 by a naval court martial** — a
*conseil de guerre maritime*, a panel of **naval officers in uniform**. A robed magistrate
presiding over a naval tribunal is not a costume error, it is the wrong body trying the
case. Four generations were spent before anyone checked, and no amount of wording would
have reached the right figure.

**Verified before rewriting** (`BIBLE.md` requires it): the Rochefort 1817 court martial
and its five counts; that Restoration naval full dress is *habit* + *épaulettes* + bicorne;
and that from about 1800 navies wore the bicorne **fore-and-aft** rather than athwart, for
wind resistance. That last one is a gift to this asset — fore-and-aft reads in strict
profile as a wide pointed crescent, where athwart would collapse to a small cap.

**The gavel stays.** It is an Anglo-American object and no French court has used one, but
the script writes it (`BIBLE.md` beat 3: *"Order! Order!" The gavel*), `BIBLE.md` makes the
play's version canon, and all five cues — the escalating strikes, the hard size jumps, the
room shudder — are built on it. Swapping in a *sonnette* would be purer history and would
gut the design. **Logged as deliberate licence, not an oversight**, so nobody re-opens it.

**Also fixed: v1's decision had no recorded reason.** The 2026-09-21 PREP session switched
from the naval officer to the robed judge and logged only *"a judge in a robe (not the naval
officer)"*. No why. That gap is what let the error survive into a generation.

**Changed:** `LOOK.md` World 3 figure, `SHOTCARDS.md` S9-CRT figure row, and
`prompts/S9-CRT-FIG.txt` → v2. **One change only** — the costume. Style prefix, framing,
gavel, scroll, pose and the two-tone treatment are all word for word as v1.


### 2026-09-21 — PREP, all three looks locked, cards and IMG prompts written

**Locked with Homie.** Salon: Soubise white-and-gold with crimson silk, a trumeau mirror on
CENTRE, LIT plus a DARK state made as an NBP edit, true scale with a 3.2 m panel line.
Louis XVIII's portrait on LEFT (the salon's solo wall), composited from Gérard. Studio: the
whole Raft painting scaled to a 3.2 × 4.7 m canvas (liberty taken so the apex reads at beat
9), window on RIGHT, limb studies only. Court: **a judge in a robe** (not the naval officer),
and the **strike is generated** as image-to-video from the still, with a Q5 fallback.

**house-rules conflicts, project files followed:** "three-quarter, never frontal" (STAGE
wants square-on), "rule of thirds" (walls are symmetrical). Also fixed LOOK's model routing
to Soul Cinema for plates and NBP for edits, and cut the prompts to the ~2,000-character cap.

**Written:** 9 IMG prompts plus the DARK template in `prompts/`, built from the locked
prefixes and room contents, and checked word for word against `LOOK.md` and
`SHOTCARDS.md`. **Nothing generated.** Homie playtests next.

**Standing preference (Homie):** the worlds are ours to shape, not literal copies of
references or history.

**Same session, Homie's direction:** (1) **every object lives whole on one wall.** Nothing
straddles a seam. Each wall is a complete composition, and only architecture, light and
colour cross. Written into CLAUDE.md, STAGE.md and the seam check in PIPELINE.md, and added
to the room contents of every prompt. (2) The court's Q4/Q5 broke that rule, so they became
a **tribunal of three**: whole judges on L and R (R mirrored) striking in unison, and at Q5
each wall gets its own gavel. (3) **Floor projection is parked, not ruled out.**

**Client document:** `docs/SOTR-Scene9-Projection-Direction.pdf` (7 pages, plain language,
no names, Scene 9 only), built by `tools/make_client_pdf.py`. It's gitignored and kept
local; the builder is in git. Homie sends it himself.

**Open:** The wall-by-beat map
needs director sign-off. Aspect ratios per model still unlogged. Loop prompts and
S9-CRT-STRIKE wait for a VID session.

### 2026-09-21 — PREP, setup

Read the full source folder: the workshop script, work schedule, visual references, 2022
presentation, staging plan v0.2, UE5/Unity snapshots and both 2022 dev-showing videos.
Scope set with Homie: Scene 9 Court Martial, Salon and Studio, in about one week. Staging:
three surfaces (L 4800 × 3600, C 6000 × 3600, R 4800 × 3600, flats at 25°), cameras
locked. Decided: walls-as-walls rendering, transitions in compositing, the Raft painting
composited. Proposed, **not locked**: all three world looks, the naval-officer silhouette,
the wall-by-beat map.

Same day, Homie's direction: work at 1080p and upscale approved results to 4K. No projector
spec needed, because the mapping software does the final fit. Sound is a separate designer,
and our timing leads. Goal: one cohesive video across three screens. Adopted Homie's order
(cards, then front, left, right) and added two things: a **room master** before the front
camera, and a **wide-canvas master comp** (4680 × 1080) where every cross-screen event is
built. Written up as `PIPELINE.md`.

Frame rate: native is fine (24 OK), higher when a model offers it. No forced
interpolation. Post VFX is an optional upgrade; generation comes first.

Salon research: the Cooper Hewitt Restoration salon (buff and blue, restrained) against
the script and references (old-regime gilt, Hôtel de Soubise). Recommended gilt. Four open
choices logged in `LOOK.md`. Found Homie's 2022 studio concept (Slide 9), the only prior
Scene 9 visual, and noted it as the studio's starting layout. Added
`docs/HANDOVER-WINDOWS.md` for the PC.
