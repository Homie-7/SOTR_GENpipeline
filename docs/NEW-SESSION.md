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

THE TASK, RIGHT NOW (from 2026-09-23): IMG scope for Scene 9 is DONE. Next session should
be VID, in a fresh chat - see NEXT ACTIONS.

WALL MAPPING IS CONFIRMED, not proposed. The client (audience-perspective, confirmed by
Homie): salon on RIGHT, Gericault's studio on LEFT, the judge on CENTRE ("the back
screen"), the raft a physical floor riser (out of scope, BIBLE.md). Combined with
LOOK.md's existing "solo wall" design for the salon, each world holds ONE wall for its
whole run, no exceptions - including the court, corrected 2026-09-23 (see below). Full
reasoning: LOG.md 2026-09-22 "major simplification" entry.

SCOPE IS: 2 wall plates (S9-SAL-R, S9-STU-L), 2 loops, 1 DARK edit. docs/WEEK-PLAN.md has
the day-by-day schedule.

ALL SIX IMG ASSETS FOR THIS SCOPE ARE APPROVED (2026-09-23):
@fig_SOTR_judge_s9_v1, @loc_SOTR_salon_room_s9_v1, @loc_SOTR_studio_room_s9_v1
(regenerated under night/candlelight, supersedes the daylight version),
@loc_SOTR_salon_R_s9_v1, @loc_SOTR_salon_R_dark_s9_v1, @loc_SOTR_studio_L_s9_v1.
Full details and known non-blocking deviations (canvas proportion, DARK light direction):
REGISTER.md and LOG.md, 2026-09-23 entries.

CORRECTED 2026-09-23: the court's climax was never a "tribunal of three" - that was
invented by a prior session, not a real decision, and is reverted. BIBLE.md says "only the
Judge is animated" - one figure throughout, CENTRE only. The growth is now built around the
script's actual beats: THREE appearances (beat 3, beat 5, beat 7), not five isolated hits -
the studio takes CENTRE to black twice in between (beats 4 and 6). Full structure:
LOOK.md World 3, SHOTCARDS.md S9-CRT Cues row, LOG.md 2026-09-23 (two entries - the
tribunal correction, and the growth restructure that followed it).

NEXT ACTIONS, IN ORDER:
1. Compositing (not Higgsfield generation, do this in either mode or a separate session):
   S9-SAL-R-PORTRAIT (Gerard's Louis XVIII onto the portrait frame) and S9-STU-L-PAINT1/2/3
   (the Raft painting's three stages onto the canvas). Both source images are verified in
   REGISTER.md, not yet composited.
2. VID session (fresh chat, never mixed with IMG): loops (S9-SAL-R-LOOP, S9-STU-L-LOOP) and
   S9-CRT-STRIKE. The strike prompt should build from the corrected three-appearance growth
   above - one generated clip, locked camera, one strike, reused via comp scale/crop for all
   five cues. Q5 (gavel fills the whole wall) is an invented capper, not scripted - confirm
   with Homie it's still wanted before building it in.
3. Still open: final set dimensions (v0.2 draft), codec/container spec, Soul Cinema's
   aspect-ratio options (uncaptured) - see docs/WEEK-PLAN.md.

CLAUDE MAKES THE TECHNICAL CALLS, Homie directs (set 2026-09-22). Only look and story
decisions go to Homie, always with a recommendation. Confirm the Higgsfield credit
balance early - it was last logged around 4,500 on 2026-09-22, likely lower now.

RETIRED FILES - do not run, headers explain why: prompts/S9-SAL-L.txt, S9-SAL-C.txt,
S9-STU-C.txt, S9-STU-R.txt. Each points to its replacement.

For each result Homie brings: judge it against the card, log one row in LOG.md, change
one thing at a time, and version the prompt file (v2, v3; never overwrite what produced
an approved asset). Log each model's aspect options in PIPELINE.md on first use (Soul
Cinema's is still uncaptured - NBP's is logged: 9:16 2k -> 1536x2752).

Watch the known risks: prompt length (~2,000-character cap), walls drifting from the
room master. The salon mirror risk (camera square-on to a mirror) is now MOOT - the
mirror wall is retired, never built.

Standing preference: the worlds are ours to shape. Adapt references to what works on
stage and say what changed and why. The era law and STAGE.md still hold.

Whole-objects rule: no object or figure ever straddles a seam. Every wall is a complete
composition on its own. Only architecture lines, light and colour carry across. No world
in this production currently shows more than one wall at once (corrected 2026-09-23 - the
court doesn't either), so the seam-check step has no live case right now. Floor projection
is parked, not ruled out; it may come back after the walls.

The client direction PDF exists (docs/SOTR-Scene9-Projection-Direction.pdf, local only,
rebuilt by tools/make_client_pdf.py). If a look decision changes, update the PDF too.

Still open: final set dimensions (v0.2 draft), codec and file-container spec for the
mapping software (docs/WEEK-PLAN.md has the questions to ask), Soul Cinema's aspect-ratio
options (still uncaptured). Loop prompts and S9-CRT-STRIKE wait for a VID session. Never
mix IMG and VID in one session.

The Windows PC is set up (2026-09-21): skills installed, both repos cloned, source folder
audited, working folder created. docs/HANDOVER-WINDOWS.md is history now, not a to-do.
Homie works from the prompt FILES - give him a path and the settings, never paste a long
prompt into chat.

LESSONS THAT WILL KEEP REPEATING:
(1) When the pose, reference structure or register changes, re-read the WHOLE spec for
clauses that silently depended on the old state.
(2) Accuracy and legibility are different axes - check both, separately (the judge's
naval costume read as Napoleon; check new content the same way).
(3) When a defect survives being banned by name, change the NOUN, not the negation.
(4) A locked design can already contain the answer to a question that seems open - the
salon's "solo wall" was written before the wall-mapping question was even asked, and
turned out to already be the answer.
(5) When a technical constraint conflicts with an existing design, bring the conflict back
to Homie with a recommendation - don't resolve it unilaterally and write it into a LOCKED
file as if decided. The court's "tribunal of three" was invented this way (a fix for the
whole-objects rule, dressed up with historical justification, never actually decided with
Homie) and stood for two days before he questioned it himself. Traced and reverted
2026-09-23 - see LOG.md. "Nothing gets invented about the look" (CLAUDE.md) applies even
when the invention is a reasonable-sounding technical fix.

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW",
commit, push.
```
