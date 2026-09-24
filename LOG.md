# LOG — SOTR

One row per generation. Change one thing at a time. After 15–20 attempts on one plate,
change the plate, not the sentence.

| Date | ID | v | Model | Changed | Verdict | Note |
|---|---|---|---|---|---|---|
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
