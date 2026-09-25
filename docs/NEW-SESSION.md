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
Load house-rules, declare MODE, then read CLAUDE.md, STAGE.md, PIPELINE.md, LOOK.md,
SHOTCARDS.md and docs/AUTONOMOUS-GEN.md before anything else. State in one line what you
loaded and which mode you're in.

This is SOTR: theatre projection backgrounds for Secret of the Raft, Scene 9, built in
Higgsfield. It is NOT a film. Live actors perform in front of three surfaces
(LEFT 4800x3600, CENTRE 6000x3600, RIGHT 4800x3600). Cameras are locked. Each surface
is a wall of the room, square-on, at true scale. No people in any plate. Cross-screen
events are built in the wide master comp (4680x1080), not generated.

THE TASK, RIGHT NOW (from 2026-09-25, VID session 4; 48 credits spent this session, balance
~3,154. Homie presents Scene 9 at a meeting on 2026-09-26 and expects changes and feedback, and has
MANY OTHER SCENES to come: preserve credits. Read the CREDITS rule in CLAUDE.md before any generation):

SCENE 9 IS DELIVERED as v3 in SOTR_MEDIA/01_FINAL_FOR_SHOW/ (00_READ_ME_FIRST.txt is current):
- THE FILES THAT PLAY are each wall's with_edge_effect/ files: salon *_edge2, studio *_v3_edge2,
  court *_edge3. The edge now moves ONE WAY only (Homie: the old ping-pong "looks like a cheap
  reverse loop"): tools/edge_flow.py freezes the generated broken edge and sends its blocks drifting
  off, new ones always coming. LOOK D16.
- STUDIO v3: the Raft is painted in BRUSHSTROKES (render_studio.py --strokes 3000), apex last. The
  canvas NEVER breaks (Homie: the canvas isn't a physical space); only the plaster beside it.
- COURT: the paper screen BURNS away at both sides (tools/court_burn.py, render_court.py --scrim
  --burn), creeping inward from beat 3 to 7; the judge always whole on top. Torn paper and cube
  blocks were both rejected: no brick/cube breakups on anything that isn't masonry.
- Every file carries its sound (build_audio.py). Old files in 03_TESTS_IN_PROGRESS/superseded/
  (edge_v2_pingpong/ holds the v2 edge files and the v2 studio clean masters). Nothing deleted.
- S9-CRT-BREAK v1 (48 credits) FAILED: the model reframed the screen into a hard rectangle with
  stacked cubes. Not used.

NEXT (ask Homie first):
1. His feedback from the 2026-09-26 meeting. Fix by script first; generate only with his go-ahead.
2. The studio candle arc (D6): beat 6 flaring, beat 9 steady and bright. Try a script version
   (boost / steady the approved loop's flicker) before any generation.
3. Still open: set dimensions, codec/container, the physical fit (pre-warp or playback?), beat
   timings from rehearsal. The client PDF is STALE.
4. Homie has MANY OTHER SCENES after this one. Credits are for them.

CONNECTOR RULES LEARNED THIS SESSION (full list: PIPELINE.md):
- SUBMIT ONE GENERATION AT A TIME and check `transactions` after each. Two parallel calls were
  duplicated and double-charged (2026-09-25).
- A transport error (ERR_NAME_NOT_RESOLVED) came back for a job that ran and was charged. Check
  `transactions` / `show_generations` before any resubmit.
- Edit video (`video_edit`) keeps framing <1 px and is billed by the INPUT length; Sequel/Edit
  media role is `video_references`.
- The server still offers the "IN THE DARK" preset: resubmit with declined_preset_id
  24bae836-2c4a-48e0-89b6-49fcc0b21612. Never run the preset.
- get_cost with count 2 reports ONE take's price.
- Uploaded media (reuse): salon comp loop 4afb0ccd-af6f-4d79-9255-f099561f1c5e; its first 4 s
  f912dd7c-18f6-4abb-bb24-196ab221af34; judge still 8e4f677b-0da7-4263-b4f9-46cf3b65a111; the judge
  reading loop af453982-3c99-4a13-8644-3b373a737ebe; lit plate c24b3532-2041-4b9d-aeb3-f4b938ff4e0f.
- Renders take ~6-10 min (30 s ~15 min). Wait with a background timer, not a poll loop.
- REFERENCE TOKENS: only @Image 1 / @Video 1 resolve; tags live in headers only.

WALL MAPPING IS CONFIRMED, not proposed. The client (audience-perspective, confirmed by
Homie): salon on RIGHT, Gericault's studio on LEFT, the judge on CENTRE ("the back
screen"), the raft a physical floor riser (out of scope, BIBLE.md). Combined with
LOOK.md's existing "solo wall" design for the salon, each world holds ONE wall for its
whole run, no exceptions - including the court, corrected 2026-09-23 (see below). Full
reasoning: LOG.md 2026-09-22 "major simplification" entry.

SCOPE IS: 2 wall plates (S9-SAL-R, S9-STU-L), 2 loops, 1 DARK edit, plus the salon snuff
clip (S9-SAL-R-SNUFF, added 2026-09-24). docs/WEEK-PLAN.md has the day-by-day schedule.

ALL SIX IMG ASSETS FOR THIS SCOPE ARE APPROVED (2026-09-23):
@fig_SOTR_judge_s9_v1, @loc_SOTR_salon_room_s9_v1, @loc_SOTR_studio_room_s9_v2
(night/candlelight; retagged from _v1 on 2026-09-24, the daylight version is the real v1),
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
SOTR_MEDIA/02_APPROVED_BUILDING_BLOCKS/clips/fig_SOTR_judge_strike_s9_v1.mp4. Seedance 2.5, image-to-video from the
approved still, 9:16 -> 1080x1920, 24 fps, 4.04s, HEVC 10-bit. THE STRIKE COMES TOWARD
CAMERA, not downward - changed with Homie after two downward versions failed structurally
(see LESSON 6). It carries a SANCTIONED WHITE KEYLINE around the gavel where it overlaps
the body, which is a deliberate carve-out in LOOK.md World 3 - do not "fix" it. One flagged
deviation: epaulette fringe returns as white hatching, needs a tracked comp patch.
Q5 no longer needs its own clip - it is further along the same travel. Its enlargement is
REDUCED, NOT GONE (corrected 2026-09-24): 3.2x working / 6.4x at 4K to fill the wall.
Upscale smoothly then threshold; the vector trace stays as the fallback.
THE 9:16 SOURCE IS STAYING VERTICAL (settled 2026-09-24 by measuring all 97 frames): the
figure leaves the frame only at the TOP and BOTTOM, never sideways, because a lunge toward
camera grows him vertically. Horizontal would make that worse and cost resolution. Comp
rule: the generated frame's bottom edge sits on the wall's floor line whenever his legs are
in frame. Details in LOOK.md World 3 step 3.

NEXT ACTIONS, IN ORDER:
1. Ask Homie the three questions at the top (snuff cut match, snuff smoke, studio v2).
2. Snuff: file the picked take; build the single delivered file (loop cycles + snuff).
3. Studio v2: file it on approval; offer the beat variants.
4. Homie's comp work (not Claude's): S9-SAL-R-PORTRAIT, S9-STU-L-PAINT1/2/3, the epaulette
   patch, the court cues Q1-Q5, and the studio's beat-driven candle arc if it isn't generated.
5. Still open: final set dimensions (v0.2 draft), codec/container spec, Soul Cinema's
   aspect menu (Seedance's is captured now). Q5's capper is STILL unconfirmed with Homie.
   The painting-grows idea (LOOK World 2) waits on the director's blocking.
   The client PDF is STALE since 2026-09-21 (a task chip was offered to rebuild it); don't
   let it go to the client as-is.

CLAUDE MAKES THE TECHNICAL CALLS, Homie directs (set 2026-09-22). Only look and story
decisions go to Homie, always with a recommendation. Confirm the Higgsfield credit
balance early; it was last logged around 4,500 on 2026-09-22 and is likely lower now. Seedance 2.5
costs ~12 credits a second at 1080p (48 for 4 s).

RETIRED FILES - do not run, headers explain why: prompts/S9-SAL-L.txt, S9-SAL-C.txt,
S9-STU-C.txt, S9-STU-R.txt. Each points to its replacement.

For each result Homie brings: judge it against the card, log one row in LOG.md, change
one thing at a time, and version the prompt file (v2, v3; never overwrite what produced
an approved asset). Log each model's aspect options in PIPELINE.md on first use (NBP: 9:16
2k -> 1536x2752. Seedance 2.5 menu CAPTURED 2026-09-24: 21:9 16:9 4:3 1:1 3:4 9:16, modes
References/Sequel/Prequel/Edit video, NO end-frame slot, 4:3 1080p -> 1664x1248. Soul
Cinema's menu is still uncaptured).

ALWAYS HAND OVER THE SETTINGS (Homie, 2026-09-23, reinforced 2026-09-24): EVERY message
about generating carries the FULL block (model, mode, reference file, aspect, resolution,
duration, quality, batch, sound, prompt file), never "as above", in chat AND the file
header.

REGENERATE OVER COMP (Homie, 2026-09-24): "If we can do a regeneration, we'll just do a
regeneration." Don't route fixes into his After Effects work. This overrides WEEK-PLAN's
"fix it in the comp" budget rule.

RENAME ON APPROVAL (Homie, 2026-09-24): the moment something is approved or finished,
rename it to its tag WITHOUT the @ and file it. Pending takes: 03_TESTS_IN_PROGRESS/<PROMPT-ID>_v<N>.mp4.
Rejects: rejected/. Checksum every move. Rules in SOTR_MEDIA/README.txt. He is the one typing them into Higgsfield. Mark anything unconfirmed
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
HEVC 10-bit, which is a real input to that decision), Soul Cinema's aspect-ratio menu
(Seedance's is captured). The snuff and the studio beat variants are the only generation work left. Never mix IMG
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
(9) CALMING WORDS FREEZE A CLIP; EXAGGERATION WORDS BLOW IT UP. Studio v1 ("gentle,
small, constant, as still as stone") came back a still image. v2 with vivid wording moved
4x as much. Snuff v1 ("full, clearly visible, higher, spreading") made cartoon clouds.
(10) A REWRITE LOSES WHAT WORKED. Snuff v2 was called "one change" but rewrote 4 blocks
and lost v1's snuff. Patch the failing phrase, keep every other word, diff before running.
(11) ONE TAKE CAN'T SEPARATE WORDING FROM LUCK. Use batch 2 at 4 s when that's the question.
(12) A PROBE PROVES ONLY WHAT IT CONTAINS. The 4 s break probe was a steady loop; the 30 s run
over reveal + hold + snuff failed on exactly the events the probe didn't have (360 credits).
Probe the hardest 4 s of the real input before going long.
(14) WHEN HOMIE SAYS SOMETHING WORKS, BUILD ON IT; DON'T REGENERATE IT. He called the approved
strike "spot on" and only disliked the repetition; new strike styles were generated anyway (an
older plan, D12) and rejected. Fix with script/comp on the praised asset first.
(15) EVERY PICTURE TOOL MUST CARRY THE SOUND. The first show files were all silent because the
tools read frames only. build_audio.py rebuilds it; check any new tool's output has audio.
(13) MAKE AN EFFECT EXIST FROM FRAME 0 WITH AN EDIT, NOT A SEQUEL. A Sequel starts on the
unbroken wall, so the break had to happen on camera, and the model plays that as a collapse with
gravity (rubble in 4 takes). Edit video put the break on the loop's own frames and it floated.
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
commit, push, back up to the T9. Report credits spent this session.
```
