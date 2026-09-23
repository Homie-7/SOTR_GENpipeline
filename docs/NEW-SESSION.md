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

THE TASK, RIGHT NOW (from 2026-09-23, VID session): IMG scope is DONE and S9-CRT-STRIKE is
DONE and APPROVED. What is left in VID is the TWO LOOPS: S9-SAL-R-LOOP and S9-STU-L-LOOP.
Neither prompt is written yet. Stay in VID for them; start a fresh chat.

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

S9-CRT-STRIKE IS APPROVED (2026-09-23) -> @fig_SOTR_judge_strike_s9_v1, saved at
SOTR_MEDIA/loops/fig_SOTR_judge_strike_s9_v1.mp4. Seedance 2.5, image-to-video from the
approved still, 9:16 -> 1080x1920, 24 fps, 4.04s, HEVC 10-bit. THE STRIKE COMES TOWARD
CAMERA, not downward - changed with Homie after two downward versions failed structurally
(see LESSON 6). It carries a SANCTIONED WHITE KEYLINE around the gavel where it overlaps
the body, which is a deliberate carve-out in LOOK.md World 3 - do not "fix" it. One flagged
deviation: epaulette fringe returns as white hatching, needs a tracked comp patch.
Q5 no longer needs its own clip or the vector trace - it is further along the same travel.

NEXT ACTIONS, IN ORDER:
1. VID, THIS IS THE ONLY GENERATION WORK LEFT: S9-SAL-R-LOOP and S9-STU-L-LOOP. Both
   prompts still need writing, off the approved wall plates. Ambient motion only, locked
   camera, and they must cycle cleanly because QLab may hold them for minutes
   (PIPELINE.md 7). Salon: candle flames, glints on gilt, a breath in the curtains. Studio:
   dust in candlelight, the canvas edge catching a flicker - the candle's dim-and-swell is
   a comp light pass, NOT generated. Seedance 2.5, and ask Homie for its aspect menu, which
   is still the one uncaptured field in PIPELINE.md.
2. Compositing (either mode, or its own session): S9-SAL-R-PORTRAIT (Gerard's Louis XVIII
   onto the portrait frame), S9-STU-L-PAINT1/2/3 (the Raft's three stages onto the canvas),
   the epaulette patch on the strike, and the court cues Q1-Q5. Sources verified in
   REGISTER.md, nothing composited yet.
3. Still open: final set dimensions (v0.2 draft), codec/container spec, Soul Cinema's
   aspect-ratio options (uncaptured) - see docs/WEEK-PLAN.md. Q5's capper is STILL
   unconfirmed with Homie - it is not in the script.

CLAUDE MAKES THE TECHNICAL CALLS, Homie directs (set 2026-09-22). Only look and story
decisions go to Homie, always with a recommendation. Confirm the Higgsfield credit
balance early - it was last logged around 4,500 on 2026-09-22, likely lower now.

RETIRED FILES - do not run, headers explain why: prompts/S9-SAL-L.txt, S9-SAL-C.txt,
S9-STU-C.txt, S9-STU-R.txt. Each points to its replacement.

For each result Homie brings: judge it against the card, log one row in LOG.md, change
one thing at a time, and version the prompt file (v2, v3; never overwrite what produced
an approved asset). Log each model's aspect options in PIPELINE.md on first use (NBP: 9:16
2k -> 1536x2752. Seedance 2.5: 9:16 -> 1080x1920, 24fps, HEVC 10-bit. Soul Cinema's and
Seedance's MENUS are both still uncaptured - ask Homie).

ALWAYS HAND OVER THE SETTINGS (Homie, 2026-09-23, now a standing rule in CLAUDE.md): every
prompt ships with MODEL, ASPECT RATIO, RESOLUTION, DURATION and SOUND, in the chat message
and in the file header. He is the one typing them into Higgsfield. Mark anything unconfirmed
as unconfirmed rather than guessing. Note he deliberately leaves generation AUDIO ON as a
scratch timing reference for the sound designer - do not switch it off.

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
mapping software (docs/WEEK-PLAN.md has the questions to ask - note Seedance hands back
HEVC 10-bit, which is a real input to that decision), Soul Cinema's and Seedance's
aspect-ratio menus. The two loop prompts are the only generation work left. Never mix IMG
and VID in one session.

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
(6) Some defects are STRUCTURAL, not wording faults, and no number of prompt passes will
shift them. The judge could not strike downward because a gavel strike is a movement in
DEPTH onto a bench, and this design has neither bench nor depth - so "down" could only mean
down ACROSS the body, where a second black shape on a one-tone silhouette stops existing.
Two versions failed before that was named. When a fix fails twice for different-looking
reasons, stop rewording and ask what the design makes impossible.
(7) PROHIBITION KILLS PERFORMANCE. v2 of the strike added a long forbidden-regions list and
a ten-object furniture ban, and the animation went robotic - the model spent its budget on
compliance and defaulted to minimum safe motion. Worse, narrowing one word ("only the COAT
and shoulder fabric respond" -> "only the shoulder and SLEEVE fabric") is what removed the
cloth life Homie liked. Ask for movement positively; only ban what has actually appeared.
(8) VERIFY THE FILE, NOT THE FILENAME. The first download of the approved strike was the
wrong take - the failed v2 - and the opening pose is identical in both, so stills looked
right. Sampling frames across the whole clip caught it. Probe and frame-sample every
delivered clip before registering it.

BACKUP: Homie's Samsung T9 SSD is drive G:, and both folders mirror at G:\SOTR\HF\. It is
the ONLY backup of generated media, since .gitignore keeps images and video out of git.
The repo copy there is a real clone of the same origin - push locally, then git pull inside
G:\SOTR\HF\SOTR_GENpipeline. Never copy files over its .git. Media is a plain copy into the
matching subfolder, verified by checksum. COPY, NEVER MIRROR-DELETE: the T9 holds at least
one file that no longer exists locally (the superseded daylight studio master, which LOG.md
says to keep), and a destructive sync would remove it. Full note in CLAUDE.md.

ON WRAP: update REGISTER.md and LOG.md, update THIS file's "THE TASK, RIGHT NOW",
commit, push, back up to the T9.
```
