# Starting a new session

Paste the block below as the first message of a fresh Claude Code chat, run from the
`SOTR_GENpipeline` folder. `CLAUDE.md` loads automatically. This block tells the session
what the task is right now.

**One session at a time.** Close the old chat first. Run `git pull` before starting and
`git push` at the end.

**This file goes stale unless it's updated on every wrap.** If it disagrees with
`CLAUDE.md` → "Current stage," `CLAUDE.md` wins. Fix this file, then act.

---

```
Load house-rules, declare MODE, then read CLAUDE.md, STAGE.md and LOOK.md before
anything else. State in one line what you loaded and which mode you're in.

This is SOTR: theatre projection backgrounds for Secret of the Raft, Scene 9, built in
Higgsfield. It is NOT a film. Live actors perform in front of three surfaces
(LEFT 4800x3600, CENTRE 6000x3600, RIGHT 4800x3600). Cameras are locked. Each surface
is a wall of the room, square-on, at true scale. No people in any plate.

THE TASK, RIGHT NOW (2026-09-21): PREP. Locking the SALON look.
Scope: Court Martial, Salon, Géricault's studio. Deadline about one week (from 21/09).
Order: SALON, then STUDIO, then COURT.

SALON is IN DISCUSSION. Read LOOK.md → World 1: research done, recommendation is
old-regime gilt (the Soubise model), and four open choices: palette, depth through the
mirror, LIT/DARK plate states, true scale against the 3.6 m crop. Settle them with Homie,
write the style prefix, mark LOCKED with the date, write the card in SHOTCARDS.md, then
switch to IMG for the room master (PIPELINE.md step 2).
Don't write a generation prompt for a world until it's locked.

STUDIO has a starting layout already: Homie's 2022 concept, Slide 9 (see LOOK.md → World 2).

The system is in PIPELINE.md: card → room master → FRONT → LEFT → RIGHT → seam check
→ loops → master comp (4680x1080 wide canvas) → approve at 1080p → upscale to 4K.
Sound is a separate designer; our timing leads. Projection-mapping software does the
final fit, so there's no projector spec to wait for.

Still open: final set dimensions (v0.2 draft), frame rate and codec for the mapping
software, and the working folder for media.

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW",
commit, push.
```
