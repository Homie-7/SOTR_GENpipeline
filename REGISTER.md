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
| S9-CRT-FIG | `prompts/S9-CRT-FIG.txt` | `@fig_SOTR_judge_s9_v1` | — |

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
| | | | |

## Composited cues

| ID | Built from | Status | Notes |
|---|---|---|---|
| | | | |
