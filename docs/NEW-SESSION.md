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
Load house-rules, declare MODE, then read CLAUDE.md, STAGE.md, PIPELINE.md, LOOK.md and
SHOTCARDS.md before anything else. State in one line what you loaded and which mode
you're in.

This is SOTR: theatre projection backgrounds for Secret of the Raft, Scene 9, built in
Higgsfield. It is NOT a film. Live actors perform in front of three surfaces
(LEFT 4800x3600, CENTRE 6000x3600, RIGHT 4800x3600). Cameras are locked. Each surface
is a wall of the room, square-on, at true scale. No people in any plate. Cross-screen
events are built in the wide master comp (4680x1080), not generated.

THE TASK, RIGHT NOW (from 2026-09-21): IMG. Start on S9-SAL-ROOM, the salon
room master. All three looks are LOCKED (LOOK.md) and the cards are written
(SHOTCARDS.md). The IMG prompts are in prompts/. Homie playtests them in Higgsfield
and brings the results back; you never generate.

ONE ASSET EXISTS: @fig_SOTR_judge_s9_v1, the judge silhouette, at testing. It took
four prompt versions. Two gates before it goes to approved: Homie checks variant 3 at
full resolution, and the white epaulette fringe gets filled in the comp (it survived
being banned by name twice, so it is an object prior - paint it, do not retry it).

S9-SAL-ROOM is the expensive one. Every salon wall derives from it, and it is the
first real test of the locked Soul Cinema routing for plates. WATCH FOR ONE THING:
if the three walls come back looking assembled from fragments rather than one room,
that is the exact failure that moved LGEL's plate lane off Soul Cinema. Do not
iterate on wording - say so and move the lane to NBP.

Run order (PIPELINE.md): S9-SAL-ROOM → S9-SAL-C → L → R → seam check → DARK edits.
Then S9-STU-ROOM → C → L → R → seam check. S9-CRT-FIG any time.

For each result Homie brings: judge it against the card, log one row in LOG.md, change
one thing at a time, and version the prompt file (v2, v3; never overwrite what produced
an approved asset). Log each model's aspect options in PIPELINE.md on first use.
Watch the known risks: the salon's CENTRE mirror (fallback after two fails: mirror-glazed
doors), prompt length (~2,000-character cap), and walls drifting from the room master.

Standing preference: the worlds are ours to shape. Adapt references to what works on
stage and say what changed and why. The era law and STAGE.md still hold.

Whole-objects rule: no object or figure ever straddles a seam. Every wall is a complete
composition on its own. Only architecture lines, light and colour carry across. Check
every playtest for it: black out the other two walls and this one should still read.
Floor projection is parked, not ruled out; it may come back after the walls.

The client direction PDF exists (docs/SOTR-Scene9-Projection-Direction.pdf, local only,
rebuilt by tools/make_client_pdf.py). If a look decision changes, update the PDF too.

Still open: the wall-by-beat map (needs director sign-off), final set
dimensions (v0.2 draft), codec for the mapping software, and the aspect-ratio options
each model offers, which PIPELINE.md wants logged on first use and which is still not
captured after three asks. Working folder is now decided: C:\Users\Homie\Documents\SOTR_MEDIA\ Loop prompts and S9-CRT-STRIKE
wait for a VID session. Never mix IMG and VID in one session.

The Windows PC is set up (2026-09-21): skills installed, both repos cloned, source
folder audited, working folder created. docs/HANDOVER-WINDOWS.md is history now, not
a to-do. Homie works from the prompt FILES - give him a path and the settings, never
paste a long prompt into chat.

THREE LESSONS FROM THE JUDGE, they will repeat on the plates:
(1) When the pose, reference structure or register changes, re-read the WHOLE spec for
clauses that silently depended on the old state. Three of four failures were exactly
that.
(2) Accuracy and legibility are different axes. A historically correct costume read as
Napoleon, which BIBLE.md bans. Check both, separately.
(3) When a defect survives being banned by name, change the NOUN, not the negation.
Three versions forbade facial features and got faces; asking for "a shape cut from
black paper" instead of a man got none.

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW",
commit, push.
```
