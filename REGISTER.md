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
| S9-SAL-ROOM | `prompts/S9-SAL-ROOM.txt` | `@loc_SOTR_salon_room_s9_v1` | — |
| S9-SAL-C / L / R | `prompts/S9-SAL-{C,L,R}.txt` | `@loc_SOTR_salon_{C,L,R}_s9_v1` | ROOM, then C |
| S9-SAL-*-DARK | `prompts/S9-SAL-DARK.txt` (template) | `@loc_SOTR_salon_{C,L,R}_dark_s9_v1` | each approved LIT plate |
| S9-STU-ROOM | `prompts/S9-STU-ROOM.txt` | `@loc_SOTR_studio_room_s9_v1` | — |
| S9-STU-C / L / R | `prompts/S9-STU-{C,L,R}.txt` | `@loc_SOTR_studio_{C,L,R}_s9_v1` | ROOM, then C |
| ~~S9-CRT-FIG~~ | `prompts/S9-CRT-FIG.txt` v4 | `@fig_SOTR_judge_s9_v1` | Judge silhouette. Naval officer of 1817, frontal, bare featureless head, gavel raised, scroll. Black on bone-white, 9:16, 1536x2752 | **approved** 2026-09-22 | Asset v1, from prompt v4 (v1-v3 failed: wrong institution, then Napoleon, then faces). NBP, no reference. Variant 3 of 4, picked by Homie on head shape; others in `rejected/`. **Full-resolution check (2026-09-22):** head edge clean, no features; gavel clear of the head; epaulettes solid black on this variant, so the predicted fringe fix is not needed. **COMP FIX DONE 2026-09-22 (Homie): white V at the throat filled black, checked clean at full resolution.** The file in `SOTR_MEDIA` is the fixed version; the raw generation is in Higgsfield history only. Why it mattered: Black figure + long coat + bare head + white notch at the throat reads as a clerical collar; invisible at Q1, centre-wall at Q3. Fixed in the comp, not regenerated. No stress test: written for characters that must survive motion; this is a locked-camera two-tone silhouette (project files over `house-rules`, per `CLAUDE.md`). Next use: first frame of S9-CRT-STRIKE (VID) |

## Wall plates

| Tag | World | Wall | Seam check | Status | Notes |
|---|---|---|---|---|---|
| | | | | | |

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
| | | | |
