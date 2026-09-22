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
- **One world = one room master, then three cameras.** The room master (never projected)
  comes first, then FRONT (CENTRE), LEFT, RIGHT, all built from it. Nothing gets approved
  until all three are laid out side by side and the seams line up.
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

## Current stage

### 2026-09-22 — First asset approved (the judge). Next: S9-SAL-ROOM.

`@fig_SOTR_judge_s9_v1` is approved and its comp fix is done (see `REGISTER.md`). The rest of the
paragraph below is the 2026-09-21 state and still holds.

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
