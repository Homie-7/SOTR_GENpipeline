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

THE TASK, RIGHT NOW (from 2026-09-23, one day behind schedule but scope halved so it's absorbable — docs/WEEK-PLAN.md): IMG.

WALL MAPPING IS CONFIRMED, not proposed. The client (audience-perspective, confirmed by
Homie): salon on RIGHT, Gericault's studio on LEFT, the judge on CENTRE ("the back
screen"), the raft a physical floor riser (out of scope, BIBLE.md). Combined with
LOOK.md's existing "solo wall" design for the salon, each world holds ONE wall for its
whole run - the court's own climax excepted (Q4->Q5, all three at once, already designed).
Full reasoning: LOG.md 2026-09-22 "major simplification" entry.

SCOPE IS NOW: 2 wall plates (S9-SAL-R, S9-STU-L), not 6. 2 loops, not 6. 1 DARK edit, not
3. docs/WEEK-PLAN.md has the revised day-by-day schedule.

FOUR ASSETS EXIST: @fig_SOTR_judge_s9_v1 (approved) and @loc_SOTR_salon_room_s9_v1
(approved) are done. @loc_SOTR_studio_room_s9_v1 is SUPERSEDED - the light changed from
daylight to night/candlelight (Gantt + sound brief both said "two in the morning" /
"moonlit window", neither is in the script) - it must be regenerated from
prompts/S9-STU-ROOM.txt v3 and re-approved before S9-STU-L can run. Full details:
REGISTER.md.

NEXT ACTIONS, IN ORDER:
1. Regenerate S9-STU-ROOM (v3, night/candlelight), review at full resolution, approve.
2. Run S9-SAL-R.txt (ready now, no dependency) and S9-STU-L.txt (once its room master is
   approved). Both are Nano Banana Pro, reference-led off the approved room master.
3. Review each at full resolution against its card in SHOTCARDS.md.
4. S9-SAL-R-DARK once S9-SAL-R is approved (NBP edit template, prompts/S9-SAL-DARK.txt).

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
composition on its own. Only architecture lines, light and colour carry across. Seam
checks are now needed only where two walls of the SAME world are genuinely live together
- currently only the court's own climax (Q4->Q5). Floor projection is parked, not ruled
out; it may come back after the walls.

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

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW",
commit, push.
```
