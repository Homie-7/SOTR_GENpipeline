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

THE TASK, RIGHT NOW (from 2026-09-22): IMG. Both room masters are APPROVED.
Next: sort the portrait/Raft source images Homie just added to SOTR_MEDIA (see below),
then write and run the wall prompts for whichever walls the signed-off beat map uses.

THREE ASSETS EXIST, all approved: @fig_SOTR_judge_s9_v1 (judge silhouette),
@loc_SOTR_salon_room_s9_v1 and @loc_SOTR_studio_room_s9_v1 (room masters, never
projected - reference only). Full details and file paths in REGISTER.md.

CLAUDE MAKES THE TECHNICAL CALLS, Homie directs (set 2026-09-22). Only look and
story decisions go to Homie, always with a recommendation. docs/WEEK-PLAN.md is
the schedule; Homie has 4,500 Higgsfield credits, confirm the balance early.

BEAT MAP MUST BE SIGNED OFF BEFORE BUILDING MORE WALLS. The proposed map
(SHOTCARDS.md) only ever shows the salon on LEFT and the studio on CENTRE and RIGHT
- under it only 3 of 6 possible walls, 2 of 4 loops and 1 of 3 DARK edits ever get
built. Get this from the director before spending on S9-SAL-C/R or S9-STU-L.

WALL ROUTE DECIDED: Nano Banana Pro, reference-led (room master as reference), not
Soul Cinema - Soul Cinema disables its prompt field when a reference is attached.
Reasoning in PIPELINE.md 3-5.

INTERRUPTED LAST SESSION, CHECK FIRST: a search for the Gerard portrait and Raft
source images failed repeatedly and was stopped mid-way. Files landed loose in
SOTR_MEDIA/ (not SOTR_MEDIA/comp/ where they belong), and most are the WRONG
painting (Louis XVIII at his desk, not in coronation robes) or unverified. Homie
has since added more images to SOTR_MEDIA - look at those FIRST before searching
again. Full detail in LOG.md, 2026-09-22 "session paused" entry.

Studio canvas proportion check needed before S9-STU-C: room master canvas reads
~1.66:1, real Raft is 1.46:1 (716x491cm) - state the true proportion explicitly
in that prompt, do not trust the reference for it.

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
