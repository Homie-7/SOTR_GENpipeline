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

- **FINAL PRODUCT, NO PLAYBACK FIXES (Homie, 2026-09-24).** *"We are not going to rely on
  QLab or any projection software whatsoever. We are generating everything as a final
  product."* Every delivered file already plays correctly: joins, transitions, holds, fades
  and matching are built INTO the file. Ideally generated; if generation can't do it, mixed
  or composited into the file. Never close a problem with "QLab / the media server / the
  mapping software will handle it." This overrides every older line in `STAGE.md`,
  `PIPELINE.md`, `LOOK.md` and `SHOTCARDS.md` that hands content work to playback (loops
  "held by QLab", "QLab cuts to it", a playback crossfade). **Refined the same day (Homie):
  the fades at a file's very START and END are the show operator's**, so files start and end
  at full picture, with no fade-in or fade-out. **And each wall is a FRAGMENT of reality, not a
  hard rectangle:** whole on its outer side, breaking up toward the CENTRE of the stage (the
  2022 Slide 9 concept). **The edge is ON the whole time a wall is lit, on every wall**
  (Homie, 2026-09-25), and **the show plays the `with_edge_effect` files**. Depths are `LOOK.md`
  D15: nothing animated or important ever breaks. Built by script: `tools/break_strip.py` lays a
  generated Control-block break (an Edit-video pass, D14) over the finished files (salon, studio);
  `tools/render_court.py --scrim --edges` tears the court's paper. (The old `render_wall.py
  --fragment-edge` dissolve was not liked and is retired.) **Open with Homie:** (1) how a
  beat's length is set now that nothing holds a loop live, i.e. fixed-length files per
  beat, which need beat timings; (2) whether the physical fit onto the angled flats
  (keystone/warp) still happens in playback, or the files must be pre-warped.

- **Folders (Homie, 2026-09-24; RESTRUCTURED 2026-09-26, "we have so many files I am getting
  confused"): `SOTR_MEDIA/01_FINAL_FOR_SHOW/` holds ONLY the files for the show**, in three folders:
  `1_PLAY_THESE_IN_ORDER/` (the 8 show files, with the edge, `S9_b<beat>_<WALL>_<world>.mov`, in
  script order), `2_BACKUP_LOOPS_for_operator/`, `3_CLEAN_no_edge/` (`_CLEAN` masters). **No version
  numbers in show names**; the version lives in `REGISTER.md`. A new version takes the SAME show
  name and the old file goes to `03_TESTS_IN_PROGRESS/superseded/` with its version added. The
  per-wall folders and `with_edge_effect/` below are the old layout. Client-facing
  `00_READ_ME_FIRST.txt` (keep it current). Meeting documents go in `06_PRESENTATIONS/`. Then
  `02_APPROVED_BUILDING_BLOCKS/`, `03_TESTS_IN_PROGRESS/`, `04_REJECTED/`,
  `05_REFERENCE_UPLOADS/`. `comp/` is Homie's After Effects area; never reorganise it. Map and
  old-to-new paths are in `SOTR_MEDIA/README.txt`.
- **Clean first, effects separate (Homie, 2026-09-24).** *"File management 101."* Every
  finished render is saved CLEAN (no effects) in `SOTR_MEDIA/01_FINAL_FOR_SHOW/<wall>/` and is never
  overwritten or deleted; a change is a new version. Anything added on top (the fragment
  edge, any effect) is a SEPARATE file in `01_FINAL_FOR_SHOW/<wall>/with_edge_effect/`, rebuilt from clean. Homie can do the
  fragments in post himself, so the clean render is the deliverable that matters. Generated
  sources in `02_APPROVED_BUILDING_BLOCKS/` are never modified. `tools/render_wall.py` enforces this.
- **Sound rides in every show file (Homie, 2026-09-25).** *"Embed it within the file, don't get
  rid of any of the audio."* The generated clips' own sound, cut with the picture by
  `tools/build_audio.py` (verify with a correlation against the source). A scratch reference for
  the sound designer, not the sound design. Any new picture tool must carry it through.
- **Credits (Homie, 2026-09-25).** *"I trust you to generate things and try things out, but not
  at the cost of a thousand credits spent within an hour."* The 1,000 cap is a ceiling, not a
  target. Build on what he has praised before generating anything new; submit one job at a time.
- **Reference tokens in prompts (Homie, 2026-09-24).** Higgsfield resolves only `@Image 1`,
  `@Video 1`… (numbered by upload order). A register tag like `@loc_SOTR_salon_R_s9_v1` in a
  prompt body is NOT resolved; it's dead text. So register tags live in file HEADERS only.
  Prompt bodies say `@Image 1` / `@Video 1` for web runs, and plain words ("the attached
  clip") for connector runs until the API's token syntax is verified. This overrides
  `house-rules`' one-string-everywhere naming rule for prompt bodies.
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
  clean, lit, loopable plates. **One exception (Homie, 2026-09-24): the salon's exit**
  (`S9-SAL-R-SNUFF`) is a generated clip that ends in dusk. In all three early runs the model
  insisted on staging the snuff itself. Since v7 it is generated as a **Sequel continuation
  of the lit loop**, so the delivered file is loop + snuff in one seamless render (no
  playback involved, per the final-product rule). Anything else still goes through the comp.
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
  **Reinforced 2026-09-24:** every message about generating carries the full block (model,
  mode, reference file, aspect, resolution, duration, quality, batch, sound, prompt file),
  never "as above".
- **Regenerate rather than comp (Homie, 2026-09-24).** *"If we can do a regeneration, we'll
  just do a regeneration."* Compositing is Homie's own After Effects time, so a fix that a
  regeneration can make goes into the next prompt version. This overrides `docs/WEEK-PLAN.md`'s
  "fix it in the comp" budget rule. Script prep Claude does itself (`tools/loop_halo.py`) is
  not comp work.
- **Rename on approval (Homie, 2026-09-24).** The moment an asset is approved or finished,
  rename its file to the tag without the `@` and file it. Rules are in
  `SOTR_MEDIA/README.txt` and REGISTER's naming block.
- **Claude drives Higgsfield directly (2026-09-24)** through the claude.ai connector, within
  `docs/AUTONOMOUS-GEN.md`: generation only, 1,000 credits per session, pre-flight before
  every run, measure after every run, Homie approves.

## Current stage

### 2026-09-25, fourth session (VID): v3, the edge flows one way, the Raft is painted in strokes, the court burns.

- **No more ping-pong** (Homie: "a cheap reverse loop"). `tools/edge_flow.py` freezes each generated
  broken edge and sends its blocks drifting off one way, forever; `break_strip.py` is retired.
- **Studio v3:** brushstroke painting (`render_studio.py --strokes`); the canvas never breaks.
- **Court:** the paper screen burns away (`tools/court_burn.py`); torn paper and cubes both rejected.
  Materials break the way they really would (`LOOK.md` D16).
- **Credits: 48 this session** (one court Edit-video take, failed, unused). Homie presents on
  2026-09-26 and needs credits for feedback and other scenes.

### 2026-09-25, third session (VID): Scene 9 delivered as v2, with sound and the edge on every wall.

- **Show files v2** in `SOTR_MEDIA/01_FINAL_FOR_SHOW/`: every file carries its generated **sound**
  (`build_audio.py`); **the files that play are `with_edge_effect/`**, the fragment edge on the
  whole time (`LOOK.md` D15). The court = the approved strike on the new **lit-scrim field**.
- **Salon break = an Edit-video pass (v5 B)**, laid on by `break_strip.py` (D14). **Studio break =
  S9-STU-L-BREAK v1**, the canvas protected. **Court** = torn paper by script.
- **Rejected by Homie:** the new strikes (B3/B5) and the reading loop's use; one judge confirmed.
- **Credits: 1,080 in the day; ~660 bought nothing.** Homie: unacceptable. New standing rule
  (Credits, above). Nothing deleted: old/silent files are in `03_TESTS_IN_PROGRESS/superseded/`.

### 2026-09-24, second session (VID): every wall has finished clean files; the fragment edge is found.

- **Homie delegated all remaining decisions** ("just make decisions"): `LOOK.md` D1-D10 (beat
  lengths from the script, delivery format, the studio's painting stages per the script, the
  court never fragments, the Q5 capper is in, Claude builds the composites).
- **Finished clean files for all three walls** in `SOTR_MEDIA/01_FINAL_FOR_SHOW/<wall>/`: salon b2-3,
  b8 and IN/HOLD/OUT; studio b4/b6/b9 with the Raft growing; court b3/b5/b7 and strikes.
  Tools: `render_wall.py`, `render_studio.py`, `render_court.py`.
- **Fragment edge = Control-style floating blocks along the whole inner side** (Homie's art
  direction). Higgsfield can do it: wither v3 A has the look but dropped Gérard and drifted
  the framing; next is the same wording as a Sequel from the loop. Effects only in `01_FINAL_FOR_SHOW/<wall>/with_edge_effect/`.
- **960 of 1,000 credits spent.** The connector works; `PIPELINE.md` has its map and traps.

### 2026-09-24 (VID) — Salon loop approved. Studio loop works. Snuff on v3. Higgsfield connected for Claude.

- **`@loc_SOTR_salon_R_loop_s9_v1` approved.** Its halo flicker is boosted 3x by script
  (the generated halos breathed ~2-3%, too little to read from the seats). The comp file
  is `02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_loop_s9_v1_comp.mov`.
- **Studio loop v2 works but isn't approved yet** (`loops/S9-STU-L-LOOP_v2.mp4`). v1 came back
  still, because its prompt was full of calming words. v2 asks for a candle guttering in a
  draught, and the light swing went from 4% to 17%.
- **`S9-SAL-R-SNUFF` added** (Homie): smoke from the snuffed wicks, for both salon exits.
  v1's snuff was good but its smoke became cartoon clouds. v2 rewrote too much and lost the
  snuff. v3 still made puff-headed smoke. **Restructured to v4 with Homie**: the clip is the
  exit itself, from the lit plate (see the transitions exception in Standing rules). Written, not run.
- **Look decisions** (LOOK.md Worlds 1 and 2): on the salon wall the halos breathe, and the
  mirror and curtains are gone; the studio's light follows the drama across beats 4/6/9; the
  painting grows while Géricault paints (pending the director).
- **Seedance 2.5 menu captured** (`PIPELINE.md`): there's no end-frame slot, so loops close with
  a crossfade (`tools/loop_halo.py`). 4:3 at 1080p gives 1664x1248.
- **Media renamed and filed**: no `@` in filenames, rejects in `04_REJECTED/`. The studio room
  master is **retagged v2** (the daylight one is the real v1); the rename map is in `LOG.md`.
- **The Higgsfield connector** was added by Homie. It loads in the next session, which starts with the
  connector gate in `docs/AUTONOMOUS-GEN.md`.
- **Found:** the client PDF has been stale since 2026-09-21. Don't send it until it's rebuilt.

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

**Q5 needs no separate generation** — the capper is further along the same travel. Its
enlargement is **reduced, not gone** (corrected 2026-09-24): measured at 3.2× working and
6.4× at 4K for the gavel to fill the wall, a fraction of enlarging the raised-pose gavel,
and a thresholded two-tone shape survives it far better than video. The vector trace stays
as the fallback. The capper itself is still unconfirmed with Homie — it isn't in the script.

**Vertical vs horizontal, settled 2026-09-24 by measurement, not argument.** Homie asked
whether the 9:16 source would run out of frame as the comp zooms in. Every one of the 97
frames was measured. The figure never touches the left edge and only briefly the right;
where it does leave the frame is **top and bottom** — because a man lunging toward camera
grows up and down, not sideways. A horizontal frame would add room where none is needed,
remove it where it is, and cost ~44% of the linear resolution on the figure exactly at the
zoom cues. See `LOOK.md` World 3 step 3 for the floor-line placement rule that hides the
leg, and `REGISTER.md` for the two small paint jobs.

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
**update `docs/NEW-SESSION.md` → "THE TASK, RIGHT NOW,"** commit, push, **back up to the
T9**, and report what changed.

### Backing up to the T9 (documented 2026-09-23)

Homie's Samsung T9 SSD, **drive `G:`**, mirrors both folders at `G:\SOTR\HF\`. It is the
**only** protection for generated media, since `.gitignore` keeps every image and video out
of git. The repo is backed up twice over (GitHub *and* the T9); the media is backed up once.

| What | How |
|---|---|
| `SOTR_GENpipeline` | It's a **real clone of the same origin**, not a file copy. `git push` here, then `git pull` inside `G:\SOTR\HF\SOTR_GENpipeline`. Never copy files over its `.git`. |
| `SOTR_MEDIA` | Plain copy of anything new, into the matching subfolder. **Verify with a checksum**, not a file listing. |

**Copy, never mirror-delete.** The T9 already holds at least one file that no longer exists
locally (`plates/studio/loc_SOTR_studio_room_s9_v1.png`, the superseded daylight master that
`LOG.md` says to keep). A destructive sync would take it out. That asymmetry is the backup
working, not drift to be tidied away.
