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

`house-rules` and the vendored skills come from `Precision-Pipeline` (see `README.md`).
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
- **Nothing moves across a seam.** Keep hard detail about 300 mm clear of every edge.
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

### 2026-09-21 — PREP. Repo scaffolded, Scene 9 understood, looks PROPOSED not locked.

Scope: **Court Martial, Salon, Géricault's studio** (Scene 9). Deadline is about one week.
The system is set up: `PIPELINE.md`. Resolution is settled (1080p work, 4K upscale). Sound is
out of scope (separate designer, our timing leads). **Next: go through each world with
Homie, one at a time.** Lock the look, write the card, then IMG.

**SALON is in discussion.** Research is done and the four open choices are in `LOOK.md` →
World 1. The Windows PC handover is `docs/HANDOVER-WINDOWS.md`.

## Session close

On `wrap`: append to `REGISTER.md` and `LOG.md`, save final prompts to `prompts/<ID>.txt`,
**update `docs/NEW-SESSION.md` → "THE TASK, RIGHT NOW,"** commit, push, and report what
changed.
