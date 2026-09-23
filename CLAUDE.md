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

Declare **IMG**, **VID** or **PREP** at the top of every session and hold it. Image and
video vocabularies poison each other, so one session never spans both.

## Standing rules

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
  clean, lit, loopable plates.
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

## Current stage

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

**Q5's blow-up risk is gone:** the capper is simply further along the same travel, so it
needs no separate generation and no vector trace. The capper itself is still unconfirmed
with Homie — it isn't in the script.

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
old L/C/R-per-world set is retired (files kept, headers point to the replacements).

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
The Windows PC handover is `docs/HANDOVER-WINDOWS.md`.

## Session close

On `wrap`: append to `REGISTER.md` and `LOG.md`, save final prompts to `prompts/<ID>.txt`,
**update `docs/NEW-SESSION.md` → "THE TASK, RIGHT NOW,"** commit, push, and report what
changed.
