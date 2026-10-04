# REGISTER — SOTR

Source of truth. If an asset isn't on this list and approved, it can't be used as a
reference or delivered.

**Naming:** `@loc_SOTR_<world>_<wall>_s9_v<N>` (e.g. `@loc_SOTR_salon_C_s9_v1`) ·
`@fig_SOTR_judge_s9_v<N>` · states and loops go before `_s9`: `_dark`, `_loop` (e.g.
`@loc_SOTR_salon_R_loop_s9_v1`). New versions never overwrite old ones.
**Files (Homie, 2026-09-24): renamed and filed the moment an asset is approved.** The file is
the tag **without the `@`**. The `@` is for prompts and the register, never a filename.
Unapproved takes sit in `03_TESTS_IN_PROGRESS/` as `<PROMPT-ID>_v<N>` (the prompt version that made them), and
rejected takes move to `04_REJECTED/` under the same name. A comp-ready render sits beside its
source as `<tag>_comp.mov`.

**Status:** `draft` → `testing` → `approved` → `retired`. A wall is only `approved` once
its three-wall seam check passes (`STAGE.md`).

---

## Prompts ready, nothing generated yet (2026-09-21)

Not assets. Nothing below can be used as a reference until it's generated, logged and
approved. Run in `PIPELINE.md` order; each row waits for the one it depends on.

| ID | Prompt | Tag it will get | Waits for |
|---|---|---|---|
| ~~S9-SAL-ROOM~~ | `prompts/S9-SAL-ROOM.txt` v2 | `@loc_SOTR_salon_room_s9_v1` | **approved 2026-09-22 — see Wall plates below** |
| ~~S9-SAL-R~~ | `prompts/S9-SAL-R.txt` v3, NBP reference-led | `@loc_SOTR_salon_R_s9_v1` | **approved 2026-09-23 — see Wall plates below** |
| ~~S9-SAL-L, S9-SAL-C~~ | retired | — | not needed — the salon is confirmed to a single wall (RIGHT). S9-SAL-L.txt was the same portrait-wall content, retagged; S9-SAL-C.txt (mirror wall) is unused |
| ~~S9-SAL-R-DARK~~ | `prompts/S9-SAL-DARK.txt` v2 (light direction fixed 2026-09-23), NBP edit | `@loc_SOTR_salon_R_dark_s9_v1` | **approved 2026-09-23 — see Wall plates below**. The template's other tags (`{C,L}`) stay unused — salon never shows those walls |
| ~~S9-STU-L~~ | `prompts/S9-STU-L.txt` v1, NBP reference-led, new composition | `@loc_SOTR_studio_L_s9_v1` | **approved 2026-09-23 — see Wall plates below** |
| ~~S9-STU-C, S9-STU-R~~ | retired | — | not needed — the studio is confirmed to a single wall (LEFT). The canvas (was C) is now that wall's whole content; the window wall (was R) is unused |
| ~~S9-CRT-FIG~~ | `prompts/S9-CRT-FIG.txt` v4 | `@fig_SOTR_judge_s9_v1` | Judge silhouette. Naval officer of 1817, frontal, bare featureless head, gavel raised, scroll. Black on bone-white, 9:16, 1536x2752 | **approved** 2026-09-22 | Asset v1, from prompt v4 (v1-v3 failed: wrong institution, then Napoleon, then faces). NBP, no reference. Variant 3 of 4, picked by Homie on head shape; others in `04_REJECTED/`. **Full-resolution check (2026-09-22):** head edge clean, no features; gavel clear of the head; epaulettes solid black on this variant, so the predicted fringe fix is not needed. **COMP FIX DONE 2026-09-22 (Homie): white V at the throat filled black, checked clean at full resolution.** The file in `SOTR_MEDIA` is the fixed version; the raw generation is in Higgsfield history only. Why it mattered: Black figure + long coat + bare head + white notch at the throat reads as a clerical collar; invisible at Q1, centre-wall at Q3. Fixed in the comp, not regenerated. No stress test: written for characters that must survive motion; this is a locked-camera two-tone silhouette (project files over `house-rules`, per `CLAUDE.md`). Next use: first frame of S9-CRT-STRIKE (VID) |

## Wall plates

| Tag | World | Wall | Seam check | Status | Notes |
|---|---|---|---|---|---|
| `@loc_SOTR_salon_room_s9_v1` | Salon | ROOM (reference only, never projected) | n/a | **approved** | Soul Cinema 21:9 2k, batch 4, var 3 of 4 picked. 2528x1088. No chandelier (cut — script only says "an ornate Louis XIV Salon"; the chandelier never lands on a wall and its mirror reflection was the hardest thing in the room to loop). Mirror reads as quiet old glass. Ivory-and-gold palette confirmed, not gold walls. Portrait wall carries the frame the real Gerard gets composited into — placeholder face reads generic/feminine, irrelevant once composited. Saved `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/stills/loc_SOTR_salon_room_s9_v1.png` |
| `@loc_SOTR_studio_room_s9_v2` *(retagged 2026-09-24, was filed as `_v1` under an `@` filename; the daylight version is the real v1)* | Studio | ROOM (reference only, never projected) | n/a | **approved 2026-09-23** | Soul Cinema 21:9 2k, batch 4, var 1 of 4 (regenerated from `prompts/S9-STU-ROOM.txt` v3, night/candlelight). 2528x1088. Full-res check clean: correct dark night sky + point of light through the window, single candle + red-stained rag on the sill, light dies to umber toward the far corner. Left wall: plaster cast hand and a clearly recognizable small wooden raft model. Right wall: pinned charcoal limb studies read as a legible grid. **Supersedes the 2026-09-22 daylight approval** (see LOG.md 2026-09-22 — a Gantt task in our own workstream and the sound brief both described the scene as "two in the morning" / "moonlit window", neither of which is in the script). Saved `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/stills/loc_SOTR_studio_room_s9_v2.png`; the superseded daylight generation is the true **v1**, kept as `loc_SOTR_studio_room_s9_v1.png` (now on the T9 only) for reference — do not use as a wall-prompt source. Canvas proportion note (~1.23:1 vs real 1.46:1) still applies to `S9-STU-L` |
| `@loc_SOTR_salon_R_s9_v1` | Salon | RIGHT (the salon's one active wall) | n/a — solo wall, no neighbour to match | **approved 2026-09-23** | NBP 4:3 2k, batch 4, var "four" picked (no floor visible, ornate dado, corner + full cornice in frame; vars "one"/"two" showed floor, var "three" had blank/plain dado throughout). 2400x1792. **Two-pass review:** first pass caught 3 of 4 below-dado panels rendered ornate against the room master's plain treatment — Homie's first touch-up went the wrong direction (made the 4th panel ornate to match); corrected on the second pass to plain, matching the room master. Portrait frame proportion ~1.52:1 vs the real Gérard's 1.443:1 — acceptable, it's a placeholder (see `S9-SAL-R-PORTRAIT`, not yet composited). Corner pilaster garland checked against the room master's own corner treatment — matches, and is continuous trim, not a discrete object, so the 300mm seam clearance doesn't apply (`STAGE.md`). Sconces soft and even, not blown out. Saved `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/stills/loc_SOTR_salon_R_s9_v1.jpg` |
| `@loc_SOTR_salon_R_dark_s9_v1` | Salon | RIGHT, DARK state | n/a — solo wall | **approved 2026-09-23** | NBP edit of the approved LIT `S9-SAL-R`, batch 4, "16" picked. 2000x1493. Candles correctly unlit (white wax, dark wick, no flame) in all four variants. Dado stayed plain, matching the approved LIT plate — no reversion to ornate. Corner-with-back-wall position preserved at the frame's left edge. **Known deviation:** the fixed prompt asked for the cool dusk light to read strongest at the LEFT edge (toward the corner/window side); measured brightness on all four variants came back brighter on the RIGHT instead — subtle (2 to 14 points of 255, "16" is the most balanced at ~2) but consistently the wrong direction. Treated as comp-correctable (`PIPELINE.md` already treats room-wide light shifts as a master-comp pass, not a generation-exact requirement) rather than blocking approval. Saved `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/stills/loc_SOTR_salon_R_dark_s9_v1.jpg` |
| `@loc_SOTR_studio_L_s9_v1` | Studio | LEFT (the studio's one active wall) | n/a — solo wall, no neighbour to match | **approved 2026-09-23** | NBP 4:3 2k, batch 4, ref: approved night-light room master. Light falloff direction correct in all four variants (candle side brighter, dying to umber toward the far edge — measured, not eyeballed). **Two-pass fix:** original batch all showed visible floor below the canvas's support blocks, against "no floor visible below the skirting." Homie's first re-crop removed the floor centrally but left a sliver visible in the bottom corners beside the canvas. Final crop trims the frame's bottom edge to the base of the support blocks — verified floor-free at full resolution, in the corners specifically, not just centrally. Comp-cropped, not regenerated (locked-camera static architectural plate, no motion to preserve). Canvas measures ~1.28:1 against the real 1.46:1 target — same known, non-blocking drift already flagged on the room master. **The original uncropped generation is kept at `SOTR_MEDIA/04_REJECTED/loc_SOTR_studio_L_s9_v1_uncropped.jpeg`, at Homie's request — do not delete.** Final saved as `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/stills/loc_SOTR_studio_L_s9_v1.jpg` |

## Loops

| Tag | From plate | Loop method | Length | Status | Notes |
|---|---|---|---|---|---|
| `@loc_SOTR_salon_R_loop_s9_v1` | `@loc_SOTR_salon_R_s9_v1` | **crossfade in the comp** (Seedance 2.5 has no end-frame slot): frames 12-240, 1.5 s (36-frame) crossfade. Wrap-around seam measured quieter than a normal frame step | 10.04 s source · **8.04 s cycle** | **approved 2026-09-24 (Homie, preview B)** | Seedance 2.5, References, 4:3 -> 1664x1248, 24 fps, HEVC 10-bit, audio populated (scratch). Camera locked (0 px), portrait still, six flames stable. Source: `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_loop_s9_v1.mp4` (renamed from `S9-SAL-R-LOOP.mp4`, sha256 889da4b3…, unchanged). **Post additions (PIPELINE 7c), all in `tools/loop_halo.py --boost 3 --skip 12 --xfade 36`:** (1) drop frames 0-11 (frame 0 is the reference image); (2) cancel the ~3% slow dimming with a per-pixel linear gain; (3) **halo flicker boosted 3x** (only the blurred, large-scale light change; the flames and grain are untouched). Halo swing goes from ~3 to ~9/255, far panels stay ~2; (4) crossfade loop. **Comp master:** `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_loop_s9_v1_comp.mov`, ProRes 422 HQ 10-bit, 1664x1248, 193 frames, one cycle, loops end to end. Rebuild with the command above if the plate or amplitude changes |
| `@loc_SOTR_studio_L_loop_s9_v1` | `@loc_SOTR_studio_L_s9_v1` | crossfade by `loop_halo.py --boost 1 --skip 12 --xfade 36` (it also cancels v2's drift) | 10.04 s source · **8.04 s cycle** | **approved 2026-09-24 (Claude, on Homie's delegation of taste calls)** | `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_studio_L_loop_s9_v1.mp4` (was `S9-STU-L-LOOP_v2.mp4`, sha256 5351f5ec…). Seedance 2.5, References, 4:3 1664x1248. Lock 0 px, framing identical to the plate, candle pool swing ~26-28%. **Comp master:** `loc_SOTR_studio_L_loop_s9_v1_comp.mov` (ProRes 422 HQ 10-bit, 193 frames). Wrap step 1.11, at the clip's own fastest dip (1.19). v1 (near-still) in `04_REJECTED/`. Fragment edge: `render_wall.py --fragment-edge right --fragment-width 0.14` |
| `@loc_SOTR_salon_R_snuff_s9_v1` | the approved comp loop (Sequel continuation) | none needed: continues the loop natively | 5.0 s, 120 frames | **approved 2026-09-24 (Claude, delegated by Homie)** | `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_snuff_s9_v1.mp4` (was `S9-SAL-R-SNUFF_v7_B`, sha256 9dd87ec4…). The salon's exit: left sconce out at 0.79 s, right at 1.75 s, thin pale threads nearly clear by 5 s, ends in dark dusk. Join into it: 0 px, within 2%. Prompt `S9-SAL-R-SNUFF.txt` v7. v8 (smoke deadline) was worse and is in `04_REJECTED/`. Carries the placeholder portrait: Gérard goes on via `tools/render_wall.py` |
| `@loc_SOTR_salon_R_reveal_s9_v1` | the approved comp loop (Prequel, ends on its first frame) | none needed: leads into the loop natively | 5.0 s, 120 frames | **approved 2026-09-24 (Claude, delegated by Homie)** | `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_reveal_s9_v1.mp4` (sha256 4734dde3…). The salon's entry: dusk, then the candles light one at a time (left sconce, then right), the room warms to the loop's light. Replaces the planned comp reveal from DARK. Prompt `S9-SAL-R-REVEAL.txt` v1 |
| *(pending, LEAD)* `S9-SAL-R-SNUFF_v4_web5s` -> will be `@loc_SOTR_salon_R_snuff_s9_v1` | `@loc_SOTR_salon_R_s9_v1` (lit) | none. A one-shot exit, played once from a QLab cue; QLab holds the last frame (still dusk) | 5.05 s, 121 frames | **Homie: "I don't mind it." Awaiting approval** | `SOTR_MEDIA/03_TESTS_IN_PROGRESS/runner_up_takes/S9-SAL-R-SNUFF_v4_web5s.mp4` (sha256 4a63d26b…). Homie's own web run (prompt presumed v4, unconfirmed). Left out 0.79 s, right 1.71 s, thin dark threads gone by ~4 s. **Needs, before the show:** (1) Gérard composited over the placeholder portrait, darkening as the sconces go out (part of `S9-SAL-R-PORTRAIT`, Homie's comp); (2) the cut from the lit loop matched: frame 0 is 4 px off, and the dado/far-left panel are 16-22% darker (halos match). Hard cut vs 6-frame QLab crossfade previews were sent to Homie. Can't be solved by regeneration: this connector can't pin a first frame (`LOG.md` v6) |
| *(pending)* `S9-SAL-R-SNUFF_v4_probeA` | `@loc_SOTR_salon_R_s9_v1` (lit) | none. A one-shot exit clip, played once from a QLab cue, not looped | 4.05 s **probe**, not the 10 s candidate | **testing, awaiting Homie (taste). Blocked on the cut match** | `SOTR_MEDIA/03_TESTS_IN_PROGRESS/runner_up_takes/S9-SAL-R-SNUFF_v4_probeA.mp4` (sha256 b4195799…). Run by Claude through the connector, 2026-09-24. Left sconce out at 1.00 s, right at 2.00 s, no smoke while lit, dark curling incense-like threads rising ~1 m. **Known fault:** frame 0 sits 16 px low and ~11% darker than the lit loop, so a hard QLab cut would jump. The fix is undecided (`docs/NEW-SESSION.md`). Siblings: v4 B, v5 A and v5 B in `04_REJECTED/` |
| *(test, not an asset)* `S9-SAL-R-LOOP_v1_parity` | `@loc_SOTR_salon_R_s9_v1` | — | 10.05 s | **connector parity test, passed.** Not for use | `SOTR_MEDIA/03_TESTS_IN_PROGRESS/connector_test/S9-SAL-R-LOOP_v1_parity.mp4` (sha256 88222b60…). The approved prompt re-run through the connector to prove it matches the web app (`LOG.md`, `PIPELINE.md`). Keep it as the run-to-run variation sample for this prompt (about 5% darker than the approved take). A spare second take of the approved loop if Homie ever wants one |

**Renders (Homie, 2026-09-24: clean first, effects separate):**

| File | What | Status |
|---|---|---|
| `03_TESTS_IN_PROGRESS/superseded/loc_SOTR_salon_R_seq_s9_v1_clean_HOLDS-TBD.mov` | The salon wall, clean: reveal · comp loop x2 · snuff, Gérard composited throughout, no effects, no fades. ProRes 422 HQ 10-bit, 1664x1248, 626 frames (26.1 s), sha256 eb78a97e… | **structure master. Hold lengths are PLACEHOLDERS** until the beat timings exist; the final gets a new version, and this one is kept |
| `01_FINAL_FOR_SHOW/RIGHT_wall_SALON/loc_SOTR_salon_R_b2-3_s9_v1.mov` | **Salon, beats 2→3, the finished file** (LOOK D1-D3): reveal · lit hold (9 loop cycles, beat 2 ≈ 75 s) · snuff at the start of beat 3 · dusk held 35 s (beat 3's "salon dims"). Gérard throughout. 2,817 frames, 117.4 s, ProRes 422 HQ 10-bit, sha256 fb9d233c… | **v1, clean. Timing from script word counts; re-version if rehearsal differs** |
| `01_FINAL_FOR_SHOW/RIGHT_wall_SALON/loc_SOTR_salon_R_b8_s9_v1.mov` | **Salon, beat 8**: already lit (no reveal, D3), 1 loop cycle (~8 s, beat 8 ≈ 9 s) · snuff · 3 s dusk. 385 frames, 16.0 s, sha256 48645f69… | **v1, clean** |
| `01_FINAL_FOR_SHOW/RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_IN_s9_v1.mov` / `_HOLD_` / `_OUT_` | The safety set (D2), with Gérard: IN = reveal (120 f), HOLD = one seamless loop cycle (193 f, loops end to end), OUT = snuff (120 f). sha256 1eb7dd79… / 26b8282f… / e49867bd… | **v1, clean** (for a live operator if the actors run long or short) |
| `01_FINAL_FOR_SHOW/LEFT_wall_STUDIO/loc_SOTR_studio_L_b4_s9_v1.mov` / `_b6_` / `_b9_` | **Studio beats 4 / 6 / 9** (LOOK D4-D6): the approved candle loop (9 / 4 / 5 cycles ≈ 72 / 32 / 40 s) with the Raft on the canvas via `render_studio.py`, growing half → most → complete over each beat's first 20 s, the apex figure last. Beat 4: 1,737 frames (ee594550…); beat 6: 772 (7220becf…); beat 9: 965 (0887ea4a…) | **v1, clean.** The candle arc (6 flares, 9 steady and bright) is still the approved loop: new versions when the D6 variants are generated. Known: the unpainted apex reads as a slightly regular oval in beat 6 |
| `01_FINAL_FOR_SHOW/CENTRE_wall_COURT/fig_SOTR_judge_C_b3_s9_v1.mov` / `_b5_` / `_b7_` | **Court beats 3 / 5 / 7 on CENTRE** (LOOK World 3, D7-D9) via `render_court.py`, 1800x1080 (5:3), 24 fps: Q1 strike (b3, 40 s, 960 f) · Q2 strike, jump to Q3 on "Three!", Q3 strike on "Order!" (b5, 101 s, 2,424 f) · Q4 push-in strike, then the Q5 capper (the gavel alone fills the wall) and black (b7, 20 s, 480 f). Two-tone, epaulette fringe patched, the keyline kept, field falls to dark at L/R. sha256 b9d9ba09… / aedefdb2… / 4f90824d… | **v1, clean. Cue times estimated from the script (D1)** |
| `01_FINAL_FOR_SHOW/CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strikeQ1_s9_v1.mov` … `strikeQ4` | One strike per size (raised · blow · held at the lens 1 s · back to raised), 117 frames each, for a live operator. sha256 d863b5cf… / c1cc8f71… / 8a56f7ed… / 201cb571… | **v1, clean** |

**SHOW FILES v2, 2026-09-25 (supersede every v1 row above; v1 files moved, checksummed, to
`03_TESTS_IN_PROGRESS/superseded/show_v1_silent/`, nothing deleted):**

| Files in `01_FINAL_FOR_SHOW/` | What changed from v1 | Status |
|---|---|---|
| `RIGHT_wall_SALON/loc_SOTR_salon_R_b2-3_s9_v2.mov`, `_b8_`, `backup_pieces/_IN_/_HOLD_/_OUT_` | **sound embedded** (`build_audio.py`); picture stream-copied, MD5 identical to v1 | **clean masters, v2** |
| `LEFT_wall_STUDIO/loc_SOTR_studio_L_b4/b6/b9_s9_v2.mov` | sound embedded; picture identical | **clean masters, v2** |
| `CENTRE_wall_COURT/fig_SOTR_judge_C_b3/b5/b7_s9_v2.mov`, `backup_pieces/…strikeQ1-Q4_s9_v2.mov` | **the approved strike and v1 timing, on the lit-scrim field** (D13), Q1 ~2.0 m, sound embedded (`render_court.py --scrim`). The silent scrim render is in `superseded/court_v2_silent/` | **clean masters, v2** (Homie: "just composite the new court background… and be done") |
| every wall's `with_edge_effect/…_v2_edge.mov` (15 files) | **THE FILES THAT PLAY** (LOOK D15): the fragment edge on, with sound. Salon: v5 B via `break_strip.py`; studio: `S9-STU-L-BREAK` v1 via `break_strip.py --protect` (canvas never touched); court: torn paper (`render_court.py --scrim --edges`) | **v2 edge, for Homie's review** |

**Tools added 2026-09-25:** `build_audio.py` (soundtracks), `break_strip.py` (generated break over a finished file; `--side --protect --period --offset --layer-gain`), `render_court.py --scrim --edges`, `render_court_v2.py` (the rejected reading/strike experiment; kept).

**Show files v3 (2026-09-25, same day, after Homie's notes; nothing deleted, v2 edge files in `03_TESTS_IN_PROGRESS/superseded/edge_v2_pingpong/`):**

| Files in `01_FINAL_FOR_SHOW/` | What changed | Status |
|---|---|---|
| `RIGHT_wall_SALON/with_edge_effect/…_b2-3/_b8_s9_v2_edge2.mov`, `backup_pieces/…IN/HOLD/OUT_s9_v2_edge2.mov` | **one-way edge** (`edge_flow.py`, kit from WITHER v5 B): no ping-pong; HOLD = 772 f (32 s) exactly cyclic; sha256 b2-3 810c217f…, b8 9ea28179…, IN 85a9314c…, HOLD fff81b80…, OUT e3a0f183… | **THE FILES THAT PLAY** |
| `LEFT_wall_STUDIO/loc_SOTR_studio_L_b4/b6/b9_s9_v3.mov` | **brushstroke painting** (`render_studio.py --strokes 3000`), sound by build_audio; sha256 b4 72a6708a…, b6 428bc6ce…, b9 73af0b85… (v2 clean in `superseded/edge_v2_pingpong/LEFT_wall_STUDIO/clean_v2/`) | **clean masters, v3** |
| `LEFT_wall_STUDIO/with_edge_effect/…_v3_edge2.mov` | one-way plaster edge (kit from STU-L-BREAK v1, canvas protected, `--layer-gain 0.6 --count 34 --life 30 --speed 5`); sha256 b4 fe5876c8…, b6 05382294…, b9 21423b9d… | **THE FILES THAT PLAY** |
| `CENTRE_wall_COURT/with_edge_effect/…_s9_v2_edge3.mov` (+ Q1-Q4) | **the paper burns away** (`court_burn.py`, `render_court.py --scrim --burn`), judge whole on top; sha256 b3 2181ba32…, b5 1b2e7e97…, b7 b8bbc23f…, Q1 b36a9b9f…, Q2 7d1cd962…, Q3 a8dac3ce…, Q4 c5858696… (silent renders in `superseded/court_v3_silent/`) | **THE FILES THAT PLAY** |

**v3.1 (same day), THE FILES THAT PLAY:** salon `…b2-3/b8/OUT_s9_v2_edge2b.mov` (smoke over the break), studio `backup_pieces/…HOLD-b4/b6/b9_s9_v3.mov` + `with_edge_effect/backup_pieces/…_edge2.mov`, court `…_edge3b.mov` (burn v2). sha256: b2-3 8fc2bd91…, b8 bc03ec38…, OUT 64146d27…, HOLD-b4 98e73b1b… / edge e77979dc…, HOLD-b6 f218a194… / 8c361338…, HOLD-b9 1547d6f7… / 74ddeb1f…, court b3 833f1bf6…, b5 0a48f9cd…, b7 31a72c36…, Q1 6deba268…, Q2 ae64f4b0…, Q3 1054f38d…, Q4 3a349090….

**v3.2 (2026-09-26), salon:** `loc_SOTR_salon_R_b2-3_s9_v3.mov` (34f6677e…), `_b8_s9_v3.mov` (19298436…), `with_edge_effect/…b2-3_s9_v3_edge2b.mov` (e8a35c30…), `…b8_s9_v3_edge2b.mov` (1f9aebde…): the dusk hold without frozen smoke (`tools/clean_hold.py`); every frame before the fix bit-identical to v2. **THE FILES THAT PLAY** (salon).

**2026-09-28: ALL SCENE 9 SHOW FILES APPROVED BY HOMIE** (the table below is the approved set).

**SHOW FOLDER UPDATE, 2026-09-30/10-01 (same names).** The replaced files: `D:/SOTR/SOTR_MEDIA_ARCHIVE/03_TESTS_IN_PROGRESS/superseded/scene9_v3_pre_fix/` (all but one), and the salon HOLD's in `D:/SOTR/SOTR_MEDIA/03_TESTS_IN_PROGRESS/superseded/scene9_v3_pre_fix/`. Homie's notes: salon edge "weird artifacts", the judge "floating" after the slam. `scene9_fix_v4/FIX.log` has every sha256.

| Show file | New version | What changed |
|---|---|---|
| `1_PLAY_THESE_IN_ORDER/S9_b2-3_RIGHT_salon.mov`, `S9_b8_RIGHT_salon.mov`; `2_BACKUP_LOOPS_for_operator/S9_b3-and-b8_RIGHT_salon_OUT_snuff.mov`, `S9_b2_RIGHT_salon_HOLD_loop.mov` | salon v3, **edge v4** (`edge_flow.py` render v3) | black specks / the notch by the sconce filled from the clean picture, a soft wall/void edge, no navy smoke ghosts at the snuff. Clean masters (`3_CLEAN_no_edge/`) unchanged |
| `1_PLAY_THESE_IN_ORDER/S9_b3_CENTRE_court.mov`, `S9_b5_CENTRE_court.mov`; strikes size1-3 in `2_BACKUP…`; their `_CLEAN` files | **court v3 placement** (`render_court.py`, `FEET_Y`) | the raised pose's feet on the floor line (was ~95 px above at Q3), the gavel back in frame. Court b7 / size4 unchanged |
| `1_PLAY_THESE_IN_ORDER/S6_*_wars.mov` | Scene 6 v5 | (filed 2026-09-30) |

**SHOW FOLDER, 2026-09-26 (reorganised; names carry no version, this table does). THE FILES THAT PLAY are in `1_PLAY_THESE_IN_ORDER/`.**

| Show file (in `01_FINAL_FOR_SHOW/`) | Version | Was |
|---|---|---|
| `1_PLAY_THESE_IN_ORDER/S6_LEFT_wars.mov`, `S6_CENTRE_wars.mov`, `S6_RIGHT_wars.mov` (added 2026-09-30) | Scene 6 v5 | `03_TESTS_IN_PROGRESS/S6_final_v5/S6_<WALL>.mov` |
| `3_CLEAN_no_edge/S6_<WALL>_wars_CLEAN.mov` (added 2026-09-30) | Scene 6 v5 (no edge: same picture) | copies of the above |
| `1_PLAY_THESE_IN_ORDER/S9_b2-3_RIGHT_salon.mov` | salon v3, edge2b | `RIGHT_wall_SALON/with_edge_effect/loc_SOTR_salon_R_b2-3_s9_v3_edge2b.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b3_CENTRE_court.mov` | court v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/fig_SOTR_judge_C_b3_s9_v2_edge3b.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b4_LEFT_studio.mov` | studio v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/loc_SOTR_studio_L_b4_s9_v3_edge2.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b5_CENTRE_court.mov` | court v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/fig_SOTR_judge_C_b5_s9_v2_edge3b.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b6_LEFT_studio.mov` | studio v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/loc_SOTR_studio_L_b6_s9_v3_edge2.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b7_CENTRE_court.mov` | court v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/fig_SOTR_judge_C_b7_s9_v2_edge3b.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b8_RIGHT_salon.mov` | salon v3, edge2b | `RIGHT_wall_SALON/with_edge_effect/loc_SOTR_salon_R_b8_s9_v3_edge2b.mov` |
| `1_PLAY_THESE_IN_ORDER/S9_b9_LEFT_studio.mov` | studio v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/loc_SOTR_studio_L_b9_s9_v3_edge2.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b2_RIGHT_salon_IN_candles-light.mov` | salon IN v2, edge2 | `RIGHT_wall_SALON/with_edge_effect/backup_pieces/loc_SOTR_salon_R_IN_s9_v2_edge2.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b2_RIGHT_salon_HOLD_loop.mov` | salon HOLD v2, edge2 | `RIGHT_wall_SALON/with_edge_effect/backup_pieces/loc_SOTR_salon_R_HOLD_s9_v2_edge2.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b3-and-b8_RIGHT_salon_OUT_snuff.mov` | salon OUT v2, edge2b | `RIGHT_wall_SALON/with_edge_effect/backup_pieces/loc_SOTR_salon_R_OUT_s9_v2_edge2b.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b3_CENTRE_court_strike-size1.mov` | court Q1 v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ1_s9_v2_edge3b.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b4_LEFT_studio_HOLD_loop.mov` | studio HOLD-b4 v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b4_s9_v3_edge2.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b5_CENTRE_court_strike-size2.mov` | court Q2 v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ2_s9_v2_edge3b.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b5_CENTRE_court_strike-size3.mov` | court Q3 v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ3_s9_v2_edge3b.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b6_LEFT_studio_HOLD_loop.mov` | studio HOLD-b6 v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b6_s9_v3_edge2.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b7_CENTRE_court_strike-size4.mov` | court Q4 v2, edge3b | `CENTRE_wall_COURT/with_edge_effect/backup_pieces/fig_SOTR_judge_C_strikeQ4_s9_v2_edge3b.mov` |
| `2_BACKUP_LOOPS_for_operator/S9_b9_LEFT_studio_HOLD_loop.mov` | studio HOLD-b9 v3, edge2 | `LEFT_wall_STUDIO/with_edge_effect/backup_pieces/loc_SOTR_studio_L_HOLD-b9_s9_v3_edge2.mov` |
| `3_CLEAN_no_edge/S9_b2-3_RIGHT_salon_CLEAN.mov` | salon v3 | `RIGHT_wall_SALON/loc_SOTR_salon_R_b2-3_s9_v3.mov` |
| `3_CLEAN_no_edge/S9_b3_CENTRE_court_CLEAN.mov` | court v2 | `CENTRE_wall_COURT/fig_SOTR_judge_C_b3_s9_v2.mov` |
| `3_CLEAN_no_edge/S9_b4_LEFT_studio_CLEAN.mov` | studio v3 | `LEFT_wall_STUDIO/loc_SOTR_studio_L_b4_s9_v3.mov` |
| `3_CLEAN_no_edge/S9_b5_CENTRE_court_CLEAN.mov` | court v2 | `CENTRE_wall_COURT/fig_SOTR_judge_C_b5_s9_v2.mov` |
| `3_CLEAN_no_edge/S9_b6_LEFT_studio_CLEAN.mov` | studio v3 | `LEFT_wall_STUDIO/loc_SOTR_studio_L_b6_s9_v3.mov` |
| `3_CLEAN_no_edge/S9_b7_CENTRE_court_CLEAN.mov` | court v2 | `CENTRE_wall_COURT/fig_SOTR_judge_C_b7_s9_v2.mov` |
| `3_CLEAN_no_edge/S9_b8_RIGHT_salon_CLEAN.mov` | salon v3 | `RIGHT_wall_SALON/loc_SOTR_salon_R_b8_s9_v3.mov` |
| `3_CLEAN_no_edge/S9_b9_LEFT_studio_CLEAN.mov` | studio v3 | `LEFT_wall_STUDIO/loc_SOTR_studio_L_b9_s9_v3.mov` |
| `3_CLEAN_no_edge/backups/S9_b2_RIGHT_salon_IN_candles-light_CLEAN.mov` | salon IN v2 | `RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_IN_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b2_RIGHT_salon_HOLD_loop_CLEAN.mov` | salon HOLD v2 | `RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_HOLD_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b3-and-b8_RIGHT_salon_OUT_snuff_CLEAN.mov` | salon OUT v2 | `RIGHT_wall_SALON/backup_pieces/loc_SOTR_salon_R_OUT_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b3_CENTRE_court_strike-size1_CLEAN.mov` | court Q1 v2 | `CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strikeQ1_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b4_LEFT_studio_HOLD_loop_CLEAN.mov` | studio HOLD-b4 v3 | `LEFT_wall_STUDIO/backup_pieces/loc_SOTR_studio_L_HOLD-b4_s9_v3.mov` |
| `3_CLEAN_no_edge/backups/S9_b5_CENTRE_court_strike-size2_CLEAN.mov` | court Q2 v2 | `CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strikeQ2_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b5_CENTRE_court_strike-size3_CLEAN.mov` | court Q3 v2 | `CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strikeQ3_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b6_LEFT_studio_HOLD_loop_CLEAN.mov` | studio HOLD-b6 v3 | `LEFT_wall_STUDIO/backup_pieces/loc_SOTR_studio_L_HOLD-b6_s9_v3.mov` |
| `3_CLEAN_no_edge/backups/S9_b7_CENTRE_court_strike-size4_CLEAN.mov` | court Q4 v2 | `CENTRE_wall_COURT/backup_pieces/fig_SOTR_judge_C_strikeQ4_s9_v2.mov` |
| `3_CLEAN_no_edge/backups/S9_b9_LEFT_studio_HOLD_loop_CLEAN.mov` | studio HOLD-b9 v3 | `LEFT_wall_STUDIO/backup_pieces/loc_SOTR_studio_L_HOLD-b9_s9_v3.mov` |
| `Scene9_One-Pager_dark.pdf` | meeting one-pager 2026-09-26 | `Scene9_One-Pager_dark.pdf` |

**Tools added (v3):** `edge_flow.py` (one-way break flow; `kit`, `kit-court`, `chips`, `render`), `court_burn.py`, `render_studio.py --strokes`, `render_court.py --burn/--flow`. `break_strip.py` is retired (ping-pong).

**Court tool:** `tools/render_court.py` (beats and single strikes from the approved strike clip).

**Studio tool:** `tools/render_studio.py` puts the Raft on the canvas at a stage (D4), lit by the canvas's own light, growing over `--grow` seconds. Beat cut-offs 0.45 / 0.80 / 1.06.

**Composite tool:** `tools/render_wall.py` builds a wall's finished file: any sequence of clips, Gérard (or any real painting) lit by the clip's own light, exposure-matched joins, fades and holds built in. Salon canvas opening: `--rect 586,154,468,720`.

**Reference files (not assets), `SOTR_MEDIA/05_REFERENCE_UPLOADS/`, added 2026-09-24:** `SAL-R-LOOP_comp_f0.png`, frame 0 of the approved salon comp loop, 1664x1248 (sha256 831918…). Uploaded as Higgsfield media `af61efa9-…` for snuff v5. The lit plate is Higgsfield media `c24b3532-2041-4b9d-aeb3-f4b938ff4e0f`.

## Candidates from 2026-09-25 (VID session 3), awaiting Homie

Nothing below is approved. Nothing new went into `01_FINAL_FOR_SHOW/`. Paths are under
`SOTR_MEDIA/03_TESTS_IN_PROGRESS/`. On approval: rename to the tag (no `@`), move to
`02_APPROVED_BUILDING_BLOCKS/clips/`, then render the ProRes finals.

| File | What | Would become | Status |
|---|---|---|---|
| `edge_break_tests/S9-SAL-R-WITHER_v5_B.mp4` (4194fc2b…) | **The salon break**: an Edit-video pass on 4 s of the comp loop. Control blocks floating in place from frame 0, full height, band 12-14%, framing <1 px, left sconce whole (LOOK D14) | `loc_SOTR_salon_R_break_s9_v1` | **candidate**. Its faint floor strip is faded out by script |
| `salon_break_previews/salon_R_b8_break_v1_PREVIEW.mp4` (5c8f1edf…) / `_b2-3_` | v5 B carried onto the clean b8 / b2-3 files by `tools/break_strip.py` (ping-pong 7.4 s, lit per frame by the base, left sconce and Gérard from the base). H.264 previews | ProRes into `01_FINAL_FOR_SHOW/RIGHT_wall_SALON/with_edge_effect/` | **preview**. The snuff checked on b8: the blocks dim to dusk with the room |
| `judge_tests/S9-CRT-READ_v1_loop.mov` (3e036850…), from `_long.mp4` (006409c2…) | **The judge's reading loop** (D12): frames 9-358 of a 15 s References take from the approved still, 350 f, loops with no crossfade (IoU 0.998) | `fig_SOTR_judge_read_s9_v1` | **candidate**. Flag: profile nose/chin at the OUTLINE when he turns to the scroll (nothing inside the outline) |
| `judge_tests/S9-CRT-STRIKE-B3_v2.mp4` (6eee7caf…) | **The measured strike** (beat 3), a Sequel of the reading loop: formal raise, blow at f43, the gavel head side-on across the chest, head above, pure two-tone, no bar | `fig_SOTR_judge_strike_b3_s9_v1` | **REJECTED by Homie 2026-09-25** ("the whole animation of the gavel is wrong") |
| `judge_tests/S9-CRT-STRIKE-B5_v1.mp4` (f491cfeb…) | **The frantic double** (beat 5), a Sequel of the reading loop: blows at f24 and f64, the held gavel end-on and huge | `fig_SOTR_judge_strike_b5_s9_v1` | **REJECTED by Homie 2026-09-25**. The incidental white bar is closed by `render_court_v2.py` (this clip only; never the approved strike's sanctioned keyline) |
| `court_v2_previews/court_C_b3_v2_PREVIEW.mp4` (cfa447f1…) / `_b5_` (1e32c83d…) / `_b7_` (c1e8c224…) | **Court beats 3/5/7, v2** via `tools/render_court_v2.py` (D12-D13): reading between strikes, one strike style per beat, Q1 ~2.0 m, the lit-scrim field with shadow-theatre courtroom shadows | — | **REJECTED (the strikes); the scrim field went into the show files instead** |

**New tools:** `tools/render_court_v2.py` (v1 `render_court.py` kept so the v1 renders can be
rebuilt); `tools/break_strip.py` (a generated break laid over a finished wall file).

## Figures

| Tag | What | Status | Notes |
|---|---|---|---|
| `@fig_SOTR_judge_s9_v1` | Judge silhouette. Naval officer of 1817, frontal, bare featureless head, gavel raised, scroll. Black on bone-white, 9:16, 1536x2752 | **approved** 2026-09-22 | *Row corrected 2026-09-23: this said `testing` with two gates outstanding, but both had already closed on 2026-09-22 and `LOG.md`, `CLAUDE.md` and `docs/NEW-SESSION.md` all carried it as approved. Gate 1 (full-resolution check) passed; gate 2 turned out not to apply, because the selected variant returned solid black epaulettes with no fringe. The throat-V comp fix was done the same day.* **Asset v1, from prompt v4** — v1–v3 of the prompt failed (wrong institution, then Napoleon, then Napoleon again plus faces). NBP, 9:16, 2k, no reference. **Variant 3 of 4 selected by Homie** on head shape; the other three are in `04_REJECTED/`. **Two gates before `approved`:** (1) Homie checks it at full resolution — white inside the outline at the shoulders, clean head edge, gavel separated from the head by white; (2) the epaulette fringe returns as white hatching and is **fixed in the comp, not in generation** — banned by name across two versions and it survived, so it is an object prior (`house-rules` 5c) and the LGEL lanyard precedent applies: paint it, don't retry it. No stress test: that rule is written for characters that must survive motion, and this is a locked-camera two-tone silhouette with no face (project files over `house-rules`, per `CLAUDE.md`) |

| `@fig_SOTR_judge_strike_s9_v1` | Judge's gavel strike, **toward camera**. One blow, locked camera. Image-to-video from `@fig_SOTR_judge_s9_v1`. 1080x1920, 24 fps, 4.04 s, HEVC 10-bit. File: `SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/fig_SOTR_judge_strike_s9_v1.mp4` | **approved** 2026-09-23, with one flagged deviation | **Asset v1, from prompt v3** (v1 struck to the hip, v2 to the shoulder — both erased the gavel against the black coat; see `LOG.md`). Seedance 2.5, 9:16, 1080p, seeded from the approved still. Verified frame by frame: hold to f47, blow f48-f53, held large f54-f96. The gavel rotates as it travels, arriving face-on to the viewer. **Threshold test passed on the motion-blurred frames** — the comp's step-3 threshold resolves both the depth-of-field softness and the motion blur to clean hard edges, and the shape is stable across threshold points 110-150, so no edge chatter. **Carries a sanctioned white keyline** where the gavel overlaps the figure (`LOOK.md` World 3 carve-out, Homie 2026-09-23) — **not reproducible from the v3 prompt string, which bans it**; see the trap warning in `prompts/S9-CRT-STRIKE.txt` before any regeneration. **FLAGGED DEVIATION: epaulette fringe returns as white hatching on both shoulders.** This is the banned incidental white, not the sanctioned keyline — the S9-CRT-FIG object prior (`house-rules` 5c), which the chosen still variant happened to dodge and which the video did not. Invisible at Q1, prominent at Q3/Q4. **Comp fix, not a regeneration**, same call as the still's throat-V; needs a tracked patch since the shoulders move. Audio track is populated deliberately (Homie): a scratch timing reference for the sound designer, never used in the comp. **Serves Q1-Q5** — Q5 is further along the same travel, so it needs no separate generation. *Corrected 2026-09-24: this row originally said Q5 also no longer needed the vector-trace fallback. Measured, Q5 still needs 3.2x (working) / 6.4x (4K); reduced, not removed, and the vector trace stays as the fallback.* **FRAME-EDGE AUDIT, 2026-09-24 (all 97 frames measured):** the figure never touches the left edge (47 px minimum clearance). It leaves the generated frame in three places, all small: **(a) front leg off the BOTTOM, f47-f96** — harmless under the placement rule in `LOOK.md` World 3 step 3 (frame bottom on the wall's floor line whenever the legs are in shot), no paint needed; **(b) gavel apex off the TOP, f48-f50** — 3 motion-blurred frames at the fastest point of the swing, visible only at Q1/Q2 where the whole figure is in shot. Paint the blur shape back in, or drop the frames — a dropped smear frame at the apex of a whip reads as speed; **(c) scroll tip off the RIGHT, f42-f48** — 7 frames in the wind-up, visible Q1-Q3. Paint. Both paint jobs sit alongside the epaulette patch in the comp. **None of this is fixed by going horizontal**: the figure leaves the frame vertically, because a lunge toward camera grows him up and down |

## Composited cues

| ID | Built from | Status | Notes |
|---|---|---|---|
| S9-SAL-R-PORTRAIT | `SOTR_MEDIA/comp/Louis_XVIII_coronation_robes_Gerard.jpg` | **source verified, not yet composited** | Gerard's *Louis XVIII in Coronation Robes*, seated, ermine and fleurs-de-lis robes, gilt throne. 1500x2165, aspect 1.443:1 (h:w). Verified 2026-09-22 by visual match against the known painting (composition, robes, throne, crown and sceptre on the cushion all correct). Public domain (pre-1931). **The portrait frame in S9-SAL-R must be built to this proportion.** He is seated, not standing - card says "full-length," which this satisfies, but flag to the director since it is more static than a standing pose. Resolution is modest for a large composite; revisit if the frame reads large on the final wall |
| S9-STU-L-PAINT1/2/3 | `SOTR_MEDIA/comp/Raft_of_the_Medusa_Gericault_WGA08630.jpg` | **source verified, not yet composited** | Web Gallery of Art scan via Wikimedia Commons, 5907x4014, aspect 1.472:1 (w:h), matching the real canvas's 1.458:1 (716x491cm) to within 1% - a clean uncropped scan. Public domain (pre-1931). **The S9-STU-L wall prompt must state the canvas as 1.46:1**, not the ~1.66:1 the room master returned — done, see `prompts/S9-STU-L.txt` |

---

## Scene 6 · The Napoleonic Wars (from 2026-09-28)

Tags for Scene 6 follow the same scheme with `_s6`: `@fx_SOTR_flag_s6_v<N>`, `@fx_SOTR_smoke_s6_v<N>`,
`@fig_SOTR_exiles_s6_v<N>` (none generated yet). The sourced prints are not generated assets: they
are public-domain material, logged by file and checksum in the folder's `_manifest.json`.

| File | What | Status |
|---|---|---|
| `02_APPROVED_BUILDING_BLOCKS/S6_public_domain/` (17 images + `_manifest.json`) | The five battles + Waterloo (1805-1816 prints), Goya pl. 15/18/30/50, maps (Delisle 1707, Bellin 1740s), Baugean's frigate; the 1818 raft plates for later scenes only. Licences: Public domain / CC0 (manifest) | **sourced 2026-09-28** (Homie's go-ahead) |
| `03_TESTS_IN_PROGRESS/S6_animatic/S6-ANIMATIC_v1.mp4` (b2619ee4…, 2340x598, 24 fps, 3,960 f, 2:45) | The whole scene, three walls, half size with a caption strip; placeholders for the flag, smoke and silhouettes. `tools/render_s6.py` | **for Homie's review** |
| `03_TESTS_IN_PROGRESS/S6_animatic/S6-ANIMATIC_v2.mp4` (7097d511…, 2340x598, 24 fps, 3,960 f, 2:45) | v2 after Homie's notes: cloth flag, frameless washes with flaking edges, the tear, Goya exiles, the glowing continent. `tools/render_s6.py` (v1 rebuildable with `render_s6_v1.py`) | **for Homie's review** |
| `02_APPROVED_BUILDING_BLOCKS/S6_public_domain/` (+4) | Goya pl. 41, 44, 45 (fleeing; Met, CC0) and the Natural Earth 1:50m countries outline (public domain), added to `_manifest.json` | **sourced 2026-09-28** |
| `03_TESTS_IN_PROGRESS/S6_animatic/S6-ANIMATIC_v3.mp4` (3bf52e05…, 2340x598, 24 fps, 3,960 f, 2:45) | v3 after Homie's five notes on v2: a real moving cloth, one picture + one word apart (measured by `--check`), constant motion, the physical burn with ash following the front, the coast-and-route map. `tools/render_s6.py` (v2 rebuildable with `render_s6_v2.py`) | **for Homie's review** |
| `03_TESTS_IN_PROGRESS/S6_animatic/S6-ANIMATIC_v4.mp4` (dbd8ba1e…, 2340x598, 24 fps, 3,960 f, 2:45) | v4 after Homie's v3 notes: one burn across all three walls (RoomBurn), the flag rips from the middle, a wider map of Africa. `tools/render_s6.py` (v3 rebuildable with `render_s6_v3.py`) | **APPROVED 2026-09-30** (the Scene 6 look and timing; checked against the script) |
| `03_TESTS_IN_PROGRESS/S6_generated/S6-FLAG_v1_A.mp4` (48855276…, 1920x1080, 97 f) / `_B.mp4` | S6-FLAG probe, batch 2. **A chosen** (no pole, most motion); B has a flagpole | A: **candidate** (the Sequel's source); B: rejected |
| `03_TESTS_IN_PROGRESS/S6_generated/S6-SMOKE_v1.mp4` (40fb5c5e…, 2206x946, 97 f) | S6-SMOKE probe: rolling smoke drifting left to right; ground strip cropped by script | **candidate** (the Sequel's source) |
| `03_TESTS_IN_PROGRESS/S6_generated/S6-FLAG_v2.mp4`, `S6-SMOKE_v2.mp4` | The 30 s Sequels (jobs 565ac6ac… / 2bf6407a…): flag 58a7e1e4… 1920x1080, smoke 7e614fa0… 2206x946, 720 f each | **checked 2026-09-30: PASS** (each continues from its probe; flag no pole) |
| `03_TESTS_IN_PROGRESS/S6_generated/S6-FLAG_loop.mov`, `S6-SMOKE_loop.mov` | Probe + Sequel joined and crossfade-looped by `tools/s6_loops.py` (781 f = 32.54 s each, ProRes 422 HQ + the clips' sound; smoke bottom 8% cropped). Read by `render_s6.py` | **built 2026-09-30** |
| `03_TESTS_IN_PROGRESS/superseded/S6_final_v4/S6_LEFT/CENTRE/RIGHT.mov` (+ `S6_scratch_sound.wav`; was `S6_final/`) | Scene 6 show files **v4**: 1440/1800/1440x1080, 3,960 f, 2:45, ProRes 422 HQ 10-bit, 48 kHz 24-bit | **reviewed by Homie: "almost perfect", five notes -> v5** |
| `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_LEFT/CENTRE/RIGHT_wars.mov` (sha256 97e7e0f3… / 7e79c671… / 1b2d1dd3…; was `03_TESTS_IN_PROGRESS/S6_final_v5/`) + `_CLEAN` copies in `3_CLEAN_no_edge/`; scratch sound stays in `S6_final_v5/` | Scene 6 show files **v5** (bigger, subject-centred pictures; flakes behind pictures; the tear riding the cloth in two fluttering pieces). 1440/1800/1440x1080, 3,960 f, 2:45 | **APPROVED 2026-09-30** (Homie: "It's looking fantastic… no complaints from the V5") |

| `03_TESTS_IN_PROGRESS/upscale_tests/` | The 4K upscale route test (2026-09-30): `salon_loop_topaz2160.mp4`, `salon_loop_bytedance4k_aigc.mp4`, `salon_loop_bd4k_restored*.mov` (`tools/upscale_restore.py`), `court_b7_upload.mp4` + its ByteDance 4K. Decision in LOG | **tests** |

| `D:/SOTR/SOTR_MEDIA/03_TESTS_IN_PROGRESS/S6_final_4K/S6_LEFT/CENTRE/RIGHT.mov` | Scene 6 at 4K: 2880/3600/2880 x 2160, 3,960 f, ProRes 422 HQ q2, sound identical to v5 (corr 1.000); from the approved v5 script with the 4K-restored flag/smoke loops | **for Homie's review** (checked 2026-10-01: every section matches v5; only random ash/ember placement differs) |
| `…/upscale_4k/<name>_4K.mov` (8) | Scene 9 at 4K (ByteDance + upscale_restore --clamp 2). b2-3, b8, b3, b5 redone 2026-10-01 from the FIXED 1080 files (pre-fix 4K in `03_TESTS_IN_PROGRESS/superseded/upscale_4k_pre_fix/`); checks in `queue5.log` (b2-3, b8, b3, b7 PASS by hand; b5, b9 VERDICT lines) | **checked; go into the show folder via `promote_4k.py`** |
| `…/upscale_4k/BACKUP/`, `CLEAN/` (`<name>_4K.mov` + `.check.txt`) | 4K of the 10 backup loops and 8 Scene 9 clean masters (JOBS_v3.txt, 47.77 cr, 2026-10-01); VERDICTs in `results_v3.txt` | **checked overnight; promoted if all pass** |
| **SHOW FOLDER IS 4K (2026-10-01 07:57, Homie delegated):** `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/` (11) and `2_BACKUP_LOOPS_for_operator/` (10) = 4K (2880x2160 side walls, 3600x2160 back wall), same names, sound; their approved 1080 files = `01_FINAL_FOR_SHOW/4_HD_1080_same_files/<same folder>/` (renamed, byte-identical). `3_CLEAN_no_edge/` stays 1080 (Homie: only show files matter). sha256 of all 43: `upscale_4k/MANIFEST_4K_2026-10-01.txt`. Verified after: all 21 4K files = their 1080 twin's frame count, with sound; spot frames right | `promote_4k.py` (log `promote_4k.log`); checks: `queue5.log`, `results_v3.txt`, one hand-diagnosed override (`overrides_v3.txt`: b9 v5, the calmest clip, light levels identical) | **DONE; T9 DONE 2026-10-02** (`promote_4k.py --t9-only`, mismatches 0, after the 43 local files re-verified against the manifest; the T9's old b9 v3 play + clean kept in `G:/…/03_TESTS_IN_PROGRESS/superseded/t9_pre4k/`) |
| `1_PLAY_THESE_IN_ORDER/S9_b9_LEFT_studio.mov` (+ its 1080 in `4_HD…`, `3_CLEAN_no_edge/S9_b9_LEFT_studio_CLEAN.mov`) | **studio v5** = the candle arc's beat 9 (the 30 s take calmed + lifted, put back on the approved framing by `tools/plate_align.py`); sources `03_TESTS_IN_PROGRESS/studio_candle_arc/loc_SOTR_studio_L_b9_s9_v5(_edge2).mov`; v3 in `03_TESTS_IN_PROGRESS/superseded/studio_b9_v3/` | **APPROVED 2026-10-01** (Homie: "Looks fine") |
| `…/studio_candle_arc/loc_SOTR_studio_L_b6_s9_v5(_edge2).mov` | the candle arc's beat 6 v5 (the flare take) | **not used** (Homie: reads as exposure going up and down; beat 6 stays v3) |
| `2_BACKUP_LOOPS_for_operator/S9_b9_LEFT_studio_HOLD_loop.mov` | still the v3 candle (~24% dimmer than b9 v5) | optional v5 rebuild NOT done (Homie: no extra work) |
| `D:/SOTR/SOTR_MEDIA_ARCHIVE/` | superseded (to 2026-09-30), 04_REJECTED, old test folders, upscale tests (74.6 GB, sha256-verified; `MOVED_*.txt`) + `_SAFE_TO_DELETE_duplicates_and_intermediates/` (25 GB of exact duplicates and rebuildable scratch) | archive |

## 2026-10-02 · CLEANUP AND NEW LAYOUT (supersedes every media path above)

Homie: "Delete everything unnecessary. Only keep what we need… recompartmentalize everything." Every path in the rows
above is the pre-cleanup address; the map below is current. Unneeded media is in `D:\SOTR\_DELETE_ME_2026-10-02\` and
`G:\SOTR\HF\_DELETE_ME_2026-10-02\` for Homie to empty; `D:\SOTR\CLEANUP_2026-10-02_moves.tsv` lists every move.
The kept set (139 files, 80 GB) is sha256-identical on D: and the T9.

| Path (SOTR_MEDIA/…) | What | Status |
|---|---|---|
| `01_FINAL_FOR_SHOW/` | **THE CLIENT DELIVERY: upload this whole folder.** README + `1_PLAY_THESE_IN_ORDER/` (11, 4K) + `2_BACKUP_LOOPS_for_operator/` (10, 4K) + `3_HD_1080_fallback/` (was `4_HD_1080_same_files/`) | **delivery** |
| `02_APPROVED_BUILDING_BLOCKS/stills/`, `clips/`, `S6_public_domain/` | unchanged | approved |
| `02_APPROVED_BUILDING_BLOCKS/S6_generated/` | S6-FLAG v1 A + v2, S6-SMOKE v1 + v2 (generated), their loops (`render_s6.py` reads these) and `4K/` loops | approved (moved from `03_TESTS_IN_PROGRESS/S6_generated/`) |
| `02_APPROVED_BUILDING_BLOCKS/studio_b9_candle/` | S9-STU-L-B9 v1 takes (generated) + `B9_candle_965f(_aligned).mov`, the candle studio b9 v5 is painted on | approved (from `studio_candle_arc/`) |
| `03_CLEAN_MASTERS_no_edge/` | the `_CLEAN` masters, 1080 (was `01_FINAL_FOR_SHOW/3_CLEAN_no_edge/`) | masters |
| `04_WORKING_FILES/edge_kits/kit_salon.npz`, `kit_studio.npz` | the frozen breaks edge_flow.py draws the edges from (kit_court / kit_studio_chips: rejected looks, binned) | working |
| `04_WORKING_FILES/build_recipes/` | the .sh scripts that built the current show files (pre-cleanup paths; map in `SOTR_MEDIA/README.txt`) | records |
| `04_WORKING_FILES/4K_records/` | `promote_4k.py`, `MANIFEST_4K_2026-10-01.txt`, check results | records |
| `04_WORKING_FILES/superseded/studio_b9_v3/` | the previous studio b9 (play + clean), the one fallback kept | superseded |
| `04_WORKING_FILES/S6-ANIMATIC_v4_approved.mp4` | the animatic Scene 6's look was approved on | reference |
| `05_REFERENCE_UPLOADS/` | the salon/studio loop references only (court READ / field and the salon chain uploads binned) | reference |
| `06_PRESENTATIONS/`, `comp/` | unchanged | — |
| **Binned** | the whole `SOTR_MEDIA_ARCHIVE` (superseded to 09-30, `04_REJECTED`, tests, upscale tests, the safe-to-delete set); studio b6 v5 (not used) and v4 (floor); upscale raws, upload transcodes, the unused clean 4Ks, the pre-fix 4Ks; S6 animatics v1-v3, S6-FLAG v1 B; scene9_fix previews; intermediates and logs; on the T9 also the pre-09-24 layout leftovers | for Homie to delete |
| `04_WORKING_FILES/S9-ANIMATIC_v1.mp4` (2026-10-03) | Scene 9 whole, for review: the eight show files on the three walls in script order + the script's lines + their sound (`tools/s9_animatic.py`) | **for Homie** (review only, not a show file) |

## 2026-10-04 · Scene 6 v6.2 IN THE SHOW (4K) + Scenes 4/5 graded (Alps A4, camps N, the camps birds removed)

**SHOW FOLDER UPDATE (same names): Scene 6 = v6.2** (Homie, 4 Oct: "S6 v6.2 REPLACES v5"). The `## 2026-10-02` table's S6 rows now read v6.2.

| Path (SOTR_MEDIA/…) | What | Status |
|---|---|---|
| `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S6_LEFT/CENTRE/RIGHT_wars.mov` (sha256 21191345… / 428f670d… / f9f41b82…) | **Scene 6 v6.2 at 4K**: 2880/3600/2880x2160, 3,960 f, 24 fps, ProRes 422 HQ q2, 48 kHz 24-bit sound = the 1080's (corr 1.000). ByteDance aigc 4k in two overlapping halves per wall, joined, `upscale_restore.py --clamp 2` (LOG 4 Oct) | **IN THE SHOW** (v6.2 approved by Homie 4 Oct) |
| `01_FINAL_FOR_SHOW/3_HD_1080_fallback/1_PLAY_THESE_IN_ORDER/S6_<WALL>_wars.mov` + `03_CLEAN_MASTERS_no_edge/S6_<WALL>_wars_CLEAN.mov` (ae51ec57… / 2eddf365… / 5352541f…) | Scene 6 v6.2 at 1080 (= `04_WORKING_FILES/S6_v6_option/S6_<WALL>_wars.mov`, byte-identical; Scene 6 has no edge, so CLEAN = the same picture) | **IN THE SHOW** |
| `04_WORKING_FILES/superseded/S6_v5/S6_<WALL>_wars_v5_4K.mov`, `_v5_1080.mov`, `_CLEAN_v5_1080.mov` | the nine replaced v5 files | superseded |
| `04_WORKING_FILES/S6_v6_option/` | the v6.2 1080 masters, `uploads/` (full walls, failed at ByteDance), `uploads_halves/`, `4K/raw/` (the six halves + the joined intermediates), `JOBS_4K.txt`, `promote_s6_v62.py` + `.log` | records |
| `04_WORKING_FILES/S4_alps_grade_v2/A4_matched/S4_alps_<front|left|right|bottom>.mov` | **Scene 4 Alps, A4 natural daylight** (Homie's pick), from `F:/OrCha Drive/SOR Show Final/Renders (050422)/Alps/`, full exposure match, Despeck, 1920x1080 ProRes 422 HQ, 29.97 fps, 5,190 f (173.2 s), sound | **for Homie** (not yet a show file) |
| `04_WORKING_FILES/S4_alps_grade_v2/A4_matched/review/` | `S4_alps_A4_SHEET.jpg` (L|F|R, floor under, 4 times), `_floor_1to1_t*.png`, **`S4_alps_<a>_REVIEW.mp4`** (H.264 crf 18 + AAC: plays from the HDD) | for Homie |
| `04_WORKING_FILES/S5_battlefield_grade/N_matched/S5_camps_<a>.mov` | **Scene 5 camps, N rich dusk** (Homie's pick), `New Renders/Camps`, full match, 25 fps, 10,770 f (430.8 s), sound. Birds still in | the graded master (kept) |
| `04_WORKING_FILES/S5_battlefield_grade/N_nobirds/S5_camps_<front|left|right>.mov` + `_smokemap.png` | **the camps with the birds removed** (`tools/debird.py`, Homie 4 Oct), everything else the graded master through a 16-bit path, sound copied. The floor has no sky: `N_matched/S5_camps_bottom.mov` is its file | **for Homie** |
| `04_WORKING_FILES/S5_battlefield_grade/N_nobirds/review/` | `S5_camps_<a>_REVIEW.mp4` (H.264 crf 18 + AAC; the floor's from N_matched), `S5_camps_N_SHEET.jpg`, floor crops | for Homie |

## 2026-10-03 (late night) · S6 v6.2 (the organic tear) + Scene 9 studio canvas edge IN THE SHOW + S5/S4 grades

| Path (SOTR_MEDIA/…) | What | Status |
|---|---|---|
| `04_WORKING_FILES/S6_v6_option/S6_CENTRE_wars.mov` (sha256 2eddf365…) | **S6 v6.2 CENTRE**: the flag tears into ~15 ragged scraps that tumble away (`_v6_shred`), 3,960 f; LEFT/RIGHT/sound byte-identical to v6.1 (cmp) | **for Homie** (the option beside v5) |
| `04_WORKING_FILES/S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4` | v5 over v6.2, rebuilt | for Homie / the client |
| `04_WORKING_FILES/superseded/S6_v6_option_v6.1/` | v6.1 CENTRE (streamers) + its comparison | superseded |
| `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S9_b4/b6/b9_LEFT_studio.mov` (4K, sha d5093694… / 34f270ad… / 88415564…) + `2_BACKUP_LOOPS_for_operator/S9_b4/b6/b9_LEFT_studio_HOLD_loop.mov` (4K, d468b3fe… / afeb820b… / c66b935d…) + the same 6 at 1080 in `3_HD_1080_fallback/` (e5b8275d… / d724df1e… / d0ca198f… / 3a79f57b… / c668a39d… / 97fab273…) | **studio edge v4 = the canvas edge fix** (Homie: the canvas's hard edge "is going to be a problem… make the changes in the final file itself"): `edge_flow.py --canvas-edge 1503,229,1525,1248` (a ragged plaster lip beside the canvas, the canvas edge sunk into shadow at its corners; the canvas never breaks). Same recipe otherwise (b9 reproduced bit-exact without the flag; b4/b6 also pick up the 09-30 edge_flow v3 fixes). 4K: ByteDance aigc + `upscale_restore.py --clamp 2`, all PASS (b9 by the same hand-diagnosed override as 10-01: `S9_studio_canvas_edge/4K/OVERRIDE_b9.txt`). 19.29 cr | **IN THE SHOW** (Claude, on Homie's "make the changes in the final file"; reversible) |
| `04_WORKING_FILES/superseded/studio_pre_canvas_edge/` | the 12 replaced files (`_4K_v3/v5`, `_1080_v3/v5`) | superseded |
| `04_WORKING_FILES/S9_studio_canvas_edge/` | the 1080 builds, `uploads/`, `4K/` (+ `raw/`), `JOBS_4K.txt`, `_regress/` | records |
| `04_WORKING_FILES/S5_battlefield_grade/C_matched/S5_camps_<front|left|right|bottom>_C.mov` + `S5_match_C.json` | **Scene 5 graded C + the angle match** (`grade_battlefield.py match/render`), 1920x1080 ProRes 422 HQ, 25 fps, 10,770 f (430.8 s), the source's sound, first 30 frames (warm-up) dropped. Right/Bottom: the good 10,770 f stream-copied out of an overrun render (see LOG) | **DONE, for Homie** |
| `04_WORKING_FILES/S4_alps_grade/S4_matched/S4_alps_<angle>_S4.mov` + `S5_match_S4.json` + `_new/` (soft air masks, samples) | **Scene 4 (Alps) graded S4 = C's stock in daylight + angle match + Despeck** (the birds), from `New Renders/Alps`, 5,370 f (214.8 s) each, sound. Despeck replaced 17.9 / 57.9 / 6.7 / 0 px per frame (F/L/R/B) | **DONE, for Homie** |

## 2026-10-03 (night) · Scene 6 v6.1: Homie's three notes on v6, built (still an option beside v5)

| Path (SOTR_MEDIA/…) | What | Status |
|---|---|---|
| `04_WORKING_FILES/S6_v6_option/S6_LEFT/CENTRE/RIGHT_wars.mov` (sha256 ae51ec57… / 699602816… / 5352541f…) | **Scene 6 v6.1 at 1080**: `render_s6.py --final --v6` (fray fix + frayed foot, CENTRE torn to shreds 2:04.4-2:07.8, Napoléonistes tattered), 3,960 f, ProRes 422 HQ 10-bit, 48 kHz sound + `S6_scratch_sound.wav` | **for Homie** (the client chooses v5 or v6) |
| `04_WORKING_FILES/S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4` | v5 (top) over v6.1 (bottom) from the 1080 show files, M2 0:05-0:44 + M4/M5 1:17-1:53 + M6 1:53-2:19, 2340x1080, 1:41, no sound | **for Homie / the client** |
| `04_WORKING_FILES/superseded/S6_v6_option_v6.0/` | the v6.0 files (`_v6.0` added) and the v6.0 comparison/preview | superseded |

## 2026-10-03 · Scene 6 v6: THE MEETING 4 FLAG OPTION, beside v5 (nothing of v5 changed)

Homie: "Make sure you don't overwrite anything. This is just the second version… present both of these and see which
one they want to use." v5 stays the show's Scene 6 in `01_FINAL_FOR_SHOW`; v6 lives only in `04_WORKING_FILES/`.
`render_s6.py --v6` builds it (without the flag v5 renders bit for bit as before: three stills compared, identical).

| Path (SOTR_MEDIA/…) | What | Status |
|---|---|---|
| `04_WORKING_FILES/S6_flags_v6_preview/S6_v5_vs_v6_COMPARE.mp4` | v5 (top) over v6 (bottom), M2 0:05-0:44 + M4 1:17-1:53 + M6 1:53-2:19 back to back, 2340x1196, 1:41, caption strip, no sound | **for Homie / the client** |
| `04_WORKING_FILES/S6_flags_v6_preview/S6_v6_flags_PREVIEW.mp4` | the same three moments, v6 only, 2340x598 | for review |
| `04_WORKING_FILES/S6_flags_v6_preview/S6-FLAG-WORN_v1.mp4` (3f97708e…, 1920x1080, 89 f, HEVC 10-bit + AAC) | Edit video on the first 4 s of S6-FLAG_v2 (`prompts/S6-FLAG-WORN.txt`, job 351a10f9…, 48 cr) | **not used** (look fail: slit holes like mouths, camouflage blue, banded red; LOG) |
| `04_WORKING_FILES/S6_flags_v6_preview/S6-FLAG-WORN_compare.jpg` | input / Edit-video test / the script's wear, side by side | reference |
| `05_REFERENCE_UPLOADS/S6-FLAG_v2_first4s_upload.mp4` (d3efcda7…, media 1edaa210…) | the test's input: S6-FLAG_v2 f0-95, H.264 crf 10 + AAC | reference |
| `04_WORKING_FILES/S6_v6_option/S6_LEFT/CENTRE/RIGHT_wars.mov` (sha256 964bb483… / dd0bbe24… / a71622d2…) | **Scene 6 v6 at 1080**: three synced walls, 3,960 f, 2:45, ProRes 422 HQ 10-bit, 48 kHz 24-bit sound (mean -31 dB, peak -1.7) + `S6_scratch_sound.wav` | **design approved by Homie 3 Oct; 3 notes to fix** (`docs/NEW-SESSION.md`) |
| `04_WORKING_FILES/S5_battlefield_grade/` | Scene 5 grade: `S5_<A|B|C>_ground/sky.cube`, `_new/` (sky masks, fire placements, sample frames), `S5_grade_ALL_OPTIONS.jpg`, `test_front_C_10s.mov` (C, 250 f), `v1_old_Exports_renders/` (v1, made on the wrong, older files) | options for Homie; Claude recommends C |
