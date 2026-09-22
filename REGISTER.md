# REGISTER — SOTR

Source of truth. If an asset isn't on this list and approved, it can't be used as a
reference or delivered.

**Naming:** `@loc_SOTR_<world>_<wall>_s9_v<N>` (e.g. `@loc_SOTR_salon_C_s9_v1`) ·
`@fig_SOTR_judge_s9_v<N>` · loops add `_loop`. New versions never overwrite old ones.

**Status:** `draft` → `testing` → `approved` → `retired`. A wall is only `approved` once
its three-wall seam check passes (`STAGE.md`).

---

## Prompts ready, nothing generated yet (2026-09-21)

Not assets. Nothing below can be used as a reference until it's generated, logged and
approved. Run in `PIPELINE.md` order; each row waits for the one it depends on.

| ID | Prompt | Tag it will get | Waits for |
|---|---|---|---|
| ~~S9-SAL-ROOM~~ | `prompts/S9-SAL-ROOM.txt` v2 | `@loc_SOTR_salon_room_s9_v1` | **approved 2026-09-22 — see Wall plates below** |
| S9-SAL-L | `prompts/S9-SAL-L.txt` v2, NBP reference-led | `@loc_SOTR_salon_L_s9_v1` | **beat map sign-off** (proposed map needs this wall) |
| S9-SAL-C / R | `prompts/S9-SAL-{C,R}.txt` | `@loc_SOTR_salon_{C,R}_s9_v1` | **NOT rewritten — pending beat map** (proposed map never uses these) |
| S9-SAL-*-DARK | `prompts/S9-SAL-DARK.txt` (template) | `@loc_SOTR_salon_{C,L,R}_dark_s9_v1` | each approved LIT plate + beat map |
| S9-STU-C | `prompts/S9-STU-C.txt` v2, NBP reference-led | `@loc_SOTR_studio_C_s9_v1` | **beat map sign-off** (proposed map needs this wall) |
| S9-STU-R | `prompts/S9-STU-R.txt` v2, NBP reference-led | `@loc_SOTR_studio_R_s9_v1` | **beat map sign-off** + approved S9-STU-C |
| S9-STU-L | `prompts/S9-STU-L.txt` | `@loc_SOTR_studio_L_s9_v1` | **NOT rewritten — pending beat map** (proposed map never uses this) |
| ~~S9-CRT-FIG~~ | `prompts/S9-CRT-FIG.txt` v4 | `@fig_SOTR_judge_s9_v1` | Judge silhouette. Naval officer of 1817, frontal, bare featureless head, gavel raised, scroll. Black on bone-white, 9:16, 1536x2752 | **approved** 2026-09-22 | Asset v1, from prompt v4 (v1-v3 failed: wrong institution, then Napoleon, then faces). NBP, no reference. Variant 3 of 4, picked by Homie on head shape; others in `rejected/`. **Full-resolution check (2026-09-22):** head edge clean, no features; gavel clear of the head; epaulettes solid black on this variant, so the predicted fringe fix is not needed. **COMP FIX DONE 2026-09-22 (Homie): white V at the throat filled black, checked clean at full resolution.** The file in `SOTR_MEDIA` is the fixed version; the raw generation is in Higgsfield history only. Why it mattered: Black figure + long coat + bare head + white notch at the throat reads as a clerical collar; invisible at Q1, centre-wall at Q3. Fixed in the comp, not regenerated. No stress test: written for characters that must survive motion; this is a locked-camera two-tone silhouette (project files over `house-rules`, per `CLAUDE.md`). Next use: first frame of S9-CRT-STRIKE (VID) |

## Wall plates

| Tag | World | Wall | Seam check | Status | Notes |
|---|---|---|---|---|---|
| `@loc_SOTR_salon_room_s9_v1` | Salon | ROOM (reference only, never projected) | n/a | **approved** | Soul Cinema 21:9 2k, batch 4, var 3 of 4 picked. 2528x1088. No chandelier (cut — script only says "an ornate Louis XIV Salon"; the chandelier never lands on a wall and its mirror reflection was the hardest thing in the room to loop). Mirror reads as quiet old glass. Ivory-and-gold palette confirmed, not gold walls. Portrait wall carries the frame the real Gerard gets composited into — placeholder face reads generic/feminine, irrelevant once composited. Saved `SOTR_MEDIA/plates/salon/loc_SOTR_salon_room_s9_v1.png` |
| `@loc_SOTR_studio_room_s9_v1` | Studio | ROOM (reference only, never projected) | n/a | **approved** | Soul Cinema 21:9 2k, batch 4, var 3 of 4 picked. 2528x1088. Light corrected from cold blue to grey daylight fading to warm umber (v1 had near-black corners with no umber - projector black is grey, so that would have read as murky nothing on stage). Studies on paper confirmed (not remains). **Canvas measures ~1.66:1, real Raft is 1.46:1 (716x491cm) - the CENTRE wall prompt must state the correct proportion explicitly, this master is a reference only.** Saved `SOTR_MEDIA/plates/studio/loc_SOTR_studio_room_s9_v1.png` |

## Loops

| Tag | From plate | Loop method | Length | Status | Notes |
|---|---|---|---|---|---|
| | | | | | |

## Figures

| Tag | What | Status | Notes |
|---|---|---|---|
| `@fig_SOTR_judge_s9_v1` | Judge silhouette. Naval officer of 1817, frontal, bare featureless head, gavel raised, scroll. Black on bone-white, 9:16 | **testing** | **Asset v1, from prompt v4** — v1–v3 of the prompt failed (wrong institution, then Napoleon, then Napoleon again plus faces). NBP, 9:16, 2k, no reference. **Variant 3 of 4 selected by Homie** on head shape; the other three are in `rejected/`. **Two gates before `approved`:** (1) Homie checks it at full resolution — white inside the outline at the shoulders, clean head edge, gavel separated from the head by white; (2) the epaulette fringe returns as white hatching and is **fixed in the comp, not in generation** — banned by name across two versions and it survived, so it is an object prior (`house-rules` 5c) and the LGEL lanyard precedent applies: paint it, don't retry it. No stress test: that rule is written for characters that must survive motion, and this is a locked-camera two-tone silhouette with no face (project files over `house-rules`, per `CLAUDE.md`) |

## Composited cues

| ID | Built from | Status | Notes |
|---|---|---|---|
| S9-SAL-L-PORTRAIT | `SOTR_MEDIA/comp/Louis_XVIII_coronation_robes_Gerard.jpg` | **source verified, not yet composited** | Gerard's *Louis XVIII in Coronation Robes*, seated, ermine and fleurs-de-lis robes, gilt throne. 1500x2165, aspect 1.443:1 (h:w). Verified 2026-09-22 by visual match against the known painting (composition, robes, throne, crown and sceptre on the cushion all correct). Public domain (pre-1931). **The portrait frame in S9-SAL-L must be built to this proportion.** He is seated, not standing - card says "full-length," which this satisfies, but flag to the director since it is more static than a standing pose. Resolution is modest for a large composite; revisit if the frame reads large on the final wall |
| S9-STU-C-PAINT1/2/3 | `SOTR_MEDIA/comp/Raft_of_the_Medusa_Gericault_WGA08630.jpg` | **source verified, not yet composited** | Web Gallery of Art scan via Wikimedia Commons, 5907x4014, aspect 1.472:1 (w:h), matching the real canvas's 1.458:1 (716x491cm) to within 1% - a clean uncropped scan. Public domain (pre-1931). **The S9-STU-C wall prompt must state the canvas as 1.46:1**, not the ~1.66:1 the room master returned |
