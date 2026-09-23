# LOG — SOTR

One row per generation. Change one thing at a time. After 15–20 attempts on one plate,
change the plate, not the sentence.

| Date | ID | v | Model | Changed | Verdict | Note |
|---|---|---|---|---|---|---|
| 2026-09-23 | S9-STU-L | 1 | NBP | first wall plate off the approved night-light room master, 4:3 | **PASS (crop fix applied)** | Light falloff correct in all four variants on measurement (candle side brighter, dying to umber toward the far edge). All four failed "no floor visible below the skirting" — floor showing beneath the canvas's support blocks. First re-crop (Homie) fixed it centrally but left a sliver in the bottom corners; final crop trims to the base of the blocks, verified floor-free at full res including the corners. Comp-cropped, not regenerated — static locked-camera plate, nothing to lose by trimming. Canvas ~1.28:1 vs the 1.46:1 target, same known non-blocking drift as the room master. Original uncropped generation kept at `SOTR_MEDIA/plates/studio/Original generation.jpeg` per Homie, not deleted. Saved `SOTR_MEDIA/plates/studio/@loc_SOTR_studio_L_s9_v1.jpg`. |
| 2026-09-23 | S9-SAL-R-DARK | 2 | NBP edit | candles unlit, light fallen to dusk, direction clause fixed (was "right", corrected to "left" to match the approved LIT plate's corner position) | **PASS, with a flagged deviation** | Batch of 4, "16" picked. Candles correctly unlit in all four (white wax, dark wick, no flame). Dado stayed plain, matching the approved LIT plate — no reversion. Corner position preserved. Light-direction fix did not fully land: measured brightness came back brighter on the RIGHT in all four, opposite of the corrected clause — subtle (2-14/255) and "16" is the most balanced. Treated as comp-correctable per `PIPELINE.md`'s own room-wide-light-is-a-comp-pass philosophy, not blocking. Saved `SOTR_MEDIA/plates/salon/@loc_SOTR_salon_R_dark_s9_v1.jpg`. |
| 2026-09-23 | S9-SAL-R | 3 | NBP | first wall plate off the approved room master, 4:3 | **PASS (two-pass review)** | Var "four" of 4 picked at full res: only variant with no floor visible AND ornate dado (vars "one"/"two" showed floor below the skirting, var "three" had no ornament anywhere on the dado). **First review pass wrongly approved the file** — missed that 3 of 4 below-dado panels came back ornate against the room master's plain treatment; Homie's own touch-up initially went the wrong direction (matched the ornate ones instead of the plain one). Caught on a second, deliberate pass checking the dado against the room master directly, not just against the prompt text. Corrected to plain, matching reference. Corner pilaster garland checked against the room master's own corner — matches; it's continuous trim so the 300mm seam-clearance rule (`STAGE.md`) doesn't apply to it. Portrait frame ~1.52:1 vs the real Gérard's 1.443:1, acceptable — it's a placeholder, composited later. 2400x1792. Saved `SOTR_MEDIA/plates/salon/@loc_SOTR_salon_R_s9_v1.jpg`. |
| 2026-09-23 | S9-STU-ROOM | 3 | Soul Cinema | light changed daylight -> night/candlelight, single candle only | **PASS** | Var 1 of 4 approved (batch of 4 reviewed at full res, all four cropped/inspected before picking). 2528x1088. Correct night sky + point of light through the window, candle + red-stained rag on the sill read clean, light dies to umber toward the far (left) corner as specified. Left wall: plaster cast hand and a genuinely recognizable small wooden raft model on the lower shelf (var 2's equivalent object read as a basket, not a raft - rejected on that). Right wall: pinned charcoal limb studies read as a legible 3x3 grid, not graffiti. Var 3 rejected as too dark/underexposed even after equal brightening - same "murky nothing on stage" risk that sent back the original daylight master. Canvas measures ~1.23:1 against the real 1.46:1 (narrower than v2's ~1.66:1 miss, same non-blocking flag - corrected at the wall-prompt stage, not the master). **Supersedes the 2026-09-22 daylight approval; `@loc_SOTR_studio_room_s9_v1` now points to this generation.** Saved `SOTR_MEDIA/plates/studio/@loc_SOTR_studio_room_s9_v1.png`; superseded daylight file kept at `loc_SOTR_studio_room_s9_v1.png` (no @), reference only. |
| 2026-09-22 | S9-CRT-FIG | 4 | - | full-resolution check of variant 3 | **APPROVED** | 1536x2752. Head, gavel, epaulettes clean. One white V at the throat reads as a clerical collar at large sizes; comp fill, logged in REGISTER. |
| 2026-09-22 | S9-SAL-ROOM | 2 | Soul Cinema | chandelier cut, mirror quiet, ivory/gold palette | **PASS** | Var 3 of 4 approved. 2528x1088. Full-res check clean: no chandelier, quiet mirror, true scale reads correctly against the 1.1m mantel. Saved. |
| 2026-09-22 | S9-STU-ROOM | 2 | Soul Cinema | light grey not blue, umber shade not black | **PASS** | Var 3 of 4 approved. 2528x1088. Grey daylight confirmed, no blue, umber corners. Studies read as paper. Canvas measures ~1.66:1 against the real 1.46:1 - flagged for the CENTRE wall prompt, not a reason to regenerate the master. Saved. |
| 2026-09-21 | S9-CRT-FIG | 4 | NBP | noun changed to a paper cut-out; hat cut; mouth cut | **PASS - variant 3 selected** | **Faces gone in all four.** The noun change is what did it: asking for "a shape cut from black paper" instead of a man rendered in black leaves no face to forbid. No hats, frontal, symmetrical, gavel clear of the head, scroll readable from outline alone, legs showing below the coat so it does not read as a robe. **One defect left:** epaulette fringe returns as white hatching. Banned by name in v3 and v4 and it survived both, so it is an object prior, not a wording fault - **fixed in the comp, not chased in generation** (LGEL lanyard precedent). Homie picked variant 3 over 1 on head shape. |
| 2026-09-21 | S9-CRT-FIG | 3 | NBP | profile -> frontal, costume reduced, interior white banned | **FAIL — faces, and the hat went Napoleonic again** | Frontal and symmetry took. **Faces in all four**, variant 3 fully rendered with eyes and nose. **Root cause found: our own spec.** "No facial features" and "mouth open mid-proclamation" contradict each other; the model obeyed the mouth. In profile that was consistent (a mouth is a notch in the outline) — frontal it can only be interior detail, and it opens the door to eyes and nose. **A clause that was right under a condition that stopped being true.** Hat returned athwart = Napoleon, third version running. |
| 2026-09-21 | S9-CRT-FIG | 2 | NBP | costume corrected to naval officer | **FAIL — reads as Napoleon** | Institution now right, icon now wrong. Bicorne + tailcoat + sword + side profile is the Napoleon silhouette, and `BIBLE.md` bans Napoleonic motifs — this is the Bourbon state, not the Empire. **The historically accurate costume produced a historically wrong reading.** Second defect, independent: white collar, white buttons and fringed epaulette detail inside the black in **all four** variants — no longer seed variance, a real prompt fault. |
| 2026-09-21 | S9-CRT-FIG | 1 | NBP | first generation, 4 variants, 9:16 | **FAIL — wrong institution** | Prompt executed correctly; the *design* was wrong. See the finding below. Variants 1-2 closest to spec; v3 failed two-tone (tan field, grey in the figure), v4 carried interior detail and a face profile. Per LGEL, 1 bad in 4 is seed variance, not a prompt fault — not treated as defects. The toque rendered as a Victorian stovepipe in all four, which is moot now the toque is cut. |

---

## Sessions

### 2026-09-22 — IMG, major simplification: each world confirmed to one wall

**Left/right convention confirmed by Homie: audience-perspective.** Facing the stage:
salon on the RIGHT, Géricault's studio on the LEFT, the judge on the back screen (CENTRE).
The raft is a physical riser in the middle of the floor, not a wall — stays out of scope
per `BIBLE.md`.

**Four reference images reviewed** (Homie's screenshot: a 2022 courtroom-engraving concept,
the wreck/raft concept already known from `Slide7.JPG`, a mountain panorama likely from a
different scene, and the Géricault studio concept already known from the 2022 deck).
Findings:

- **The raft concept image is the confirmation of "the raft... in the middle of the
  space":** a wraparound wreck/sea image across all three walls with a physical plinth on
  the floor, two figures standing on it. Matches the client's note exactly. Out of scope,
  but useful for when Raft is built.
- **The courtroom engraving is a real tension with the locked, approved judge design, and
  was NOT followed.** It's a literal historical courtroom; `LOOK.md`'s whole premise is
  that the court reads apart from the salon and studio by being abstract — *"none: graphic,
  no texture."* Following the engraving would discard four rounds of approved work to undo
  the one thing that makes Court legible as a different world. **Decision: judge design
  unchanged.** The one thing kept from it: a lone performer on a floor riser facing the
  projection — a staging idea, not a visual one, worth passing to the director for
  blocking, outside our own deliverable.

**MAJOR FINDING, before any of this: `LOOK.md` already called the portrait wall the
salon's "solo wall"** for beats 2 and 8 — the salon was never going to use more than one
wall at a time, under any version of the map. The client's correction was only ever about
*which* physical wall (RIGHT, not LEFT), not whether the salon needed one wall or three.

**DECIDED (Claude's recommendation, Homie: "go"): collapse each world to one wall,
confirmed, not proposed.**

| World | Wall | Reasoning |
|---|---|---|
| Salon | RIGHT | Already a solo-wall design; only the physical side changes |
| Studio | LEFT | The canvas (4.7 m) nearly fills a 4.8 m flat on its own — the canvas becomes the room, not a corner of it. Window and shelves were never load-bearing to the story |
| Court | CENTRE, expanding to all three at Q4→Q5 | Unchanged — already matches "judge on the back screen" as the default, with the climax as a designed exception, not a new contradiction |
| Raft | floor, out of scope | Confirmed physical, not projected |

**Cost/benefit:** the remaining build drops from up to six wall plates and six loops to
**two wall plates and two loops**, plus what's already done for Court. On a week-long
sprint starting its second day, this recovers a large share of the schedule.

**Files changed:**

- `CLAUDE.md` — the "one world = three cameras" standing rule amended: now "one room
  master, then as many cameras as that world actually uses," most worlds one.
- `STAGE.md` — "Cohesion across the three walls" section amended the same way; the seam
  check is scoped to walls that are genuinely live together (currently only Court's climax).
- `SHOTCARDS.md` — beat-by-wall table rewritten and marked CONFIRMED (was PROPOSED); the
  deliverables table cut from 6 wall plates/6 loops to 2/2; the salon and studio world
  cards' Walls rows point at the one confirmed wall each; the studio's Scale
  anchors/Light/Loop-motion rows resynced to the new single-wall composition; both room
  contents quotes' intro lines corrected (they're the room master's text now, not quoted
  into multiple wall prompts, since there is only one wall prompt each).
- `prompts/S9-SAL-R.txt` — **new active file.** Same content as the old `S9-SAL-L.txt` (the
  portrait wall) — v1 to v3 of *that* content is preserved, this is a retag, not a redesign.
  **One line changed:** the corner-with-back-wall direction is mirrored, because
  `STAGE.md`'s RIGHT flat is a mirror of LEFT — a photograph composed for physical LEFT
  would join the wrong side if played on physical RIGHT unmirrored.
- `prompts/S9-SAL-L.txt`, `S9-SAL-C.txt` — retired, point to `S9-SAL-R.txt`.
- `prompts/S9-STU-L.txt` — **new composition**, not a retag. Re-stages the canvas (was the
  room's own back-wall content) as a dedicated 4:3 side-wall elevation for the physical
  LEFT flat. Canvas proportion (4.7 × 3.2 m, ~1.46:1) stated explicitly, per the earlier
  finding that the room master's own canvas reads ~1.66:1 and can't be trusted for this.
  Light is the room's one candle, shown motivating the frame from off-frame, since the
  window itself no longer has room in a composition where the canvas dominates.
- `prompts/S9-STU-C.txt`, `S9-STU-R.txt` — retired, point to `S9-STU-L.txt`.
- `prompts/S9-SAL-DARK.txt` — simplified to the one active wall line; the mirror and
  window-wall DARK lines retired alongside their plates.
- `REGISTER.md` — pending-prompts table and composited-cue IDs (`S9-SAL-R-PORTRAIT`,
  `S9-STU-L-PAINT1/2/3`) updated to match.

**Still open, unchanged by this:** the studio room master itself still needs regenerating
under the night-light prompt (v3) and re-approving before `S9-STU-L` can run — that was
already true before this session and isn't resolved by the wall-mapping confirmation.

### 2026-09-22 — IMG, studio light changed to night; client wall assignment received — NOT yet applied

**FINDING — the studio's approved daylight may be wrong, from two independent production
sources neither of which is the script.** Homie added the production Gantt/dependency
spreadsheet to `SOTR_MEDIA`. Checked against the script directly first: Scene 9's studio
section has zero time-of-day text anywhere. But two other sources, independently:

- **Row M18, the MULTIMEDIAPROJECTION workstream — our own workstream — owner "Homie":**
  *"Scene 9: Géricault studio / painting / **moonlit window**."*
- **Row S22, the sound brief, owner Darrin:** *"Two in the morning. Horse and cart on
  cobblestones... Owls hooting."*

Both say night; `LOOK.md` (locked yesterday) said daylight. Real research point in
daylight's favour: painters historically work by daylight, not moonlight — north light is
prized because it's even and colour-true, not paintable-by. **Decided (Homie, via the
recommended option): combine both rather than pick one.** Night sky and a thin moon through
the window; the room lit by the single candle already on that sill in the locked card,
Géricault working obsessively at 2am. Uses an asset already in the design, satisfies both
sources, no source discarded.

**Changed:** `LOOK.md` (tying-together table, style prefix, room contents, loop motion — the
cloud-passing light-pass mechanism now runs on the candle guttering instead, same
mechanism, coherent motivation), `SHOTCARDS.md` (world header, Light row, room contents
quote, loop motion row), `prompts/S9-STU-ROOM.txt` → v3, `prompts/S9-STU-C.txt` and
`S9-STU-R.txt` → v3. All three re-measured under the 2,000-character cap after trimming.

**Cost: the approved studio room master is superseded, not usable as a reference anymore.**
Marked so in `REGISTER.md`. It must be regenerated from v3 and re-approved before either
wall prompt can actually run — nothing was wasted, since neither wall has been generated
yet, but the room master batch itself will need repeating.

**Honest trade noted:** `LOOK.md`'s tying-together table originally used light (warm/many
vs cold/one) to help separate the salon from the studio at a glance. Both are now
warm-toned. Contrast still holds on source count (many soft candles vs one hard candle),
and on finish (polished gilt vs raw patina) — but it's one fewer axis of separation than
before, worth watching for when the two plates sit side by side in review.

---

**SEPARATELY, and NOT yet acted on:** the client gave Homie a wall assignment directly —
*"the performance palace [salon] on the right, Géricault's studio on the left, the judge on
the back screen, and the raft — the woman on the raft — in the middle of the space."* This
is the first time ANY source has stated which physical wall each world uses, after this
session checked the script, the staging plan, the 2022 presentation and this Gantt file and
found nothing. Two real ambiguities before this can be written into `SHOTCARDS.md`:

1. **Left/right convention unconfirmed.** `STAGE.md`'s own diagram has never stated
   explicitly whether its LEFT/RIGHT are audience-perspective or performer's stage-left/
   right (mirrored) — this was never written down as a rule, only implied by an ASCII
   diagram. The client's phrasing ("if I'm facing it... on the right") reads as
   audience-perspective, matching the diagram's likely intent, but this is inference, not
   confirmation, and getting it backward would put the salon and studio on the wrong
   physical walls.
2. **Single wall vs primary wall unconfirmed.** Does "studio on the left" mean the studio
   ONLY ever uses the LEFT physical wall (which would orphan the canvas — currently CENTRE
   content, and the dramatic centrepiece of the whole world) and the window (currently
   RIGHT content)? Or does it mean LEFT is the studio's anchor/primary wall while it may
   still spread onto CENTRE as needed, closer to what the proposed map already assumed for
   other worlds? The proposed map already has the court doing exactly this (CENTRE
   primary, spreading to all three at the climax) without contradiction.

**Not applied to any file pending clarification.** Recommended to Homie: get the client's
own exact words or a marked-up diagram rather than a third-hand paraphrase, since this
determines physical wall content for two already-approved assets and is expensive to
reverse if misread.

### 2026-09-22 — IMG, folders confirmed clean; three wall prompts pre-written

**Folder check (Homie asked for a clean-up):** nothing was actually out of place. The six
loose files were the same six from the interrupted search, already sorted last entry.
`SOTR_MEDIA` matches its own naming scheme exactly — no renaming or moving needed.

**Best-course-of-action call: prep the three walls the proposed map implies, at zero
credit cost, while sign-off is pending; do not prep or generate the other three until
they're confirmed needed.** Rewrote `S9-SAL-L`, `S9-STU-C`, `S9-STU-R` reference-led for
NBP (v2). `S9-SAL-C`, `S9-SAL-R`, `S9-STU-L` marked NOT REWRITTEN / PENDING, their old
Soul-Cinema-style text flagged stale so nobody runs it by mistake.

**Refinement while writing them:** a wall only references an approved sibling wall if that
sibling is ever live on stage beside it. Under the proposed map the salon's LEFT is never
shown next to another salon wall, so `S9-SAL-L` references only the room master — one
reference, not two. The studio's CENTRE and RIGHT do appear together (beats 4, 6, 9), so
`S9-STU-R` still references the approved `S9-STU-C` for exact finish-matching, and must
run after it. Logged in `PIPELINE.md`.

**Canvas proportion correction carried into the prompt itself:** `S9-STU-C` now states the
canvas as "4.7 x 3.2 metres, a proportion close to 3:2, taller relative to its width than
the reference shows" — an explicit, stated override of what the room master actually shows,
not a drift. This is the one place prose is allowed to override a reference (`house-rules`
finding 1 bans re-narrating what the reference already carries correctly; it does not ban
correcting a stated, known error in it).

**All three still gated on the beat map sign-off**, which has not happened yet. Not run.

### 2026-09-22 — IMG, source images resolved

**Homie's files checked first, as the paused session asked.** The six files in
`SOTR_MEDIA/` from the interrupted search were the same six, not new ones.
`Louis_XVIII_of_France_in_Coronation_Robes,_by_François_Gérard.jpg` (1500x2165) verified
by visual match against the known painting — composition, robes, throne, crown and sceptre
all correct. Moved to `SOTR_MEDIA/comp/Louis_XVIII_coronation_robes_Gerard.jpg`. The four
"cabinet de travail" files (wrong painting) and the low-res 1824 file deleted.

**Raft of the Medusa found clean, one search.** WGA08630 on Wikimedia Commons, the Web
Gallery of Art scan: 5907x4014, public domain (pre-1931), aspect 1.472:1 against the real
canvas's 1.458:1 — a clean uncropped scan. Downloaded to
`SOTR_MEDIA/comp/Raft_of_the_Medusa_Gericault_WGA08630.jpg`.

**Both composite sources now verified and in place** (`REGISTER.md`, Composited cues).
Unblocks S9-SAL-L (portrait frame proportion 1.443:1) and S9-STU-C (canvas proportion
1.46:1, not the room master's ~1.66:1) once the beat map confirms those walls are needed.

### 2026-09-22 — IMG session paused · both room masters approved

**Both room masters approved and saved** (details and full-res checks in `REGISTER.md`):
`@loc_SOTR_salon_room_s9_v1` and `@loc_SOTR_studio_room_s9_v1`, both from prompt v2 (v1
had the chandelier and the wrong studio light, both now fixed). Files in `SOTR_MEDIA/plates/`.

**Two facts needed before the wall prompts can be written, both correctly flagged before
any generation was spent:**
- The studio canvas in the room master measures roughly 1.66:1; the real Raft is 1.46:1
  (716 x 491 cm). The CENTRE wall prompt has to state the true proportion — the model will
  not infer it from the reference.
- The salon portrait frame needs to match the proportions of Gerard's actual coronation
  portrait, since that painting gets composited into it. The source image was needed before
  writing that prompt.

**SESSION INTERRUPTED — the source-image search failed repeatedly and was stopped by
Homie before it produced a clean result.** What is on disk in `SOTR_MEDIA/` (not
`SOTR_MEDIA/comp/`, where it belongs — misfiled by the failed attempts, not yet sorted):

- `Louis_XVIII_of_France_in_Coronation_Robes,_by_François_Gérard.jpg` — 1500x2165,
  **filename matches the correct painting**, but the source URL and licence were never
  logged and the file has not been verified as the right image. Treat as unverified.
- Four files titled *"Le roi Louis XVIII dans son cabinet de travail des Tuileries"* —
  **a different painting** (Louis XVIII at his desk, not in coronation robes). Downloaded
  by mistake during the retries. Not usable for this composite.
- `François_Gérard_-_Louis_XVIII_(1824).jpg` — 918x1260, low resolution, wrong year in the
  filename (the coronation portrait is c. 1814/1817). Not usable.
- **No Raft of the Medusa source image was found before the session was stopped.**

**Nothing lost.** The repo was clean and fully pushed at commit `e800a58` before this
happened — the retry failures never touched git, only local downloads. **Next session:
redo the source image search from scratch, cleanly**, verify each file against the real
painting (dimensions, artist, date, Wikimedia Commons licence) before saving, sort into
`SOTR_MEDIA/comp/`, delete the wrong-painting files, and only then write the two wall
prompts that depend on them (S9-SAL-L for the portrait frame, S9-STU-C for the canvas
proportion).

**Everything else in this session stands:** both room masters approved, wall route decided
(NBP, reference-led), week plan and beat-map-first scoping in place. Not blocked — the
portrait and Raft sourcing only gates two of the six possible wall prompts, and both of
those walls may turn out to be outside the signed-off beat map anyway.

### 2026-09-22 — IMG, first room masters · chandelier cut · studio light changed

| ID | Model | Verdict |
|---|---|---|
| S9-SAL-ROOM v1 | Soul Cinema 21:9 2k, batch 4 | **FAIL — design change, not a render fault.** All four read as one coherent room (Soul Cinema passes the LGEL fragment test for hyper-real rooms). Bourbon portrait fix held: no Napoleon. Best composition was var 3, but the chandelier is being cut. Open question for the re-run: walls read gold, not ivory |
| S9-STU-ROOM v1 | Soul Cinema 21:9 2k, batch 4 | **FAIL — light.** All four blue-teal with near-black corners, no umber. Var 3 most complete; var 1 has a red streak reading as blood, vars 1 and 4 have hanging shapes reading as real limbs. **Canvas square in all four instead of 4.7 x 3.2** — fixed at the wall stage, not here (one change per re-run) |

**Chandelier cut (Homie raised it, Claude agreed).** The script asks only for "an ornate
Louis XIV Salon" — the script PDF has no chandelier, mirror or candle. The chandelier never
lands on a projected wall; its only appearance would be as a reflection in the CENTRE
mirror, the hardest element in the room to animate and loop. Mirror kept as old dim glass.
Removed from the locked prefix, the room contents, the room master camera line, the loop
motion and the DARK template.

**Studio light line changed (Claude's call, Homie asked if the light was right).** Grey
rather than cold blue, landing on the back wall and canvas, fading to warm umber toward the
far corner. Projector black is grey, so near-black areas read as murky nothing on stage.
STU-L and STU-R now sit over the cap (2,065 / 2,051); they get rewritten reference-led for
NBP before they run, so they are not trimmed now.

**Budget.** Balance 4,999 before these two batches, 4,500 after: about 250 credits per Soul
Cinema batch of 4, to be confirmed from the Generate button. Walls will run in batches of 2.

### 2026-09-22 — IMG, Claude owns the technical calls; week plan set

**Homie's direction:** Claude is the expert on the sources and makes the technical calls;
Homie directs. Only look and story decisions go to Homie, always with a recommendation.

**Decided:** walls on **Nano Banana Pro, reference-led** (reasoning in `PIPELINE.md` 3-5).
Studio prompts reordered camera-first to match the salon. **Loops cut from 6 to 4** —
`LOOK.md` gives STU-C and STU-L no motion of their own. `docs/WEEK-PLAN.md` written.

### 2026-09-22 — IMG, source check before the salon (Homie's direction)

**Homie: stop experimenting where Joey, Cully and Higgsfield already answer.** Read before
the salon runs: `banana-pro-director-30` Mode 3 (grepped for DEPRECATED first — only the two
`house-rules` names), Cully's `LIRA SKILL.md` and project brief, and Higgsfield's Soul
Cinema help page.

**Decided (Homie): camera anchor first.** All four salon prompts reordered, no words changed, character counts identical. `LOOK.md` plate recipe updated. C/L/R headers now carry a ROUTE OPEN warning. Studio prompts to be reordered the same way when the studio is prepped.

**FINDING 1 — the wall plan was never checked against the platform.** Higgsfield: with a
reference attached, Soul Cinema's prompt field is disabled. LIRA: one reference. Every
C/L/R prompt was written as "Soul Cinema + room master reference" (L/R with two). Not
executable. Same failure shape as LGEL's `plate-3a.txt`: written without opening the source.
**Proven routes in the sources for other views of one room:** LIRA sends location view
changes to **GPT Image 2** (default) or **NBP with the new object arrangement spelled out**;
Cully's brief pulls angles from a **video walkthrough of the empty location, screenshotted,
then refined in Seedream or NBP**; LGEL used a **360 spin for geometry, then NBP with two
references**. Decide before S9-SAL-C. The room master is unaffected (no reference).

**FINDING 2 — two source grammars for plates, and only one fits a projected wall.**
`banana-pro-director-30` Mode 3 (cinema prose: anamorphic, handheld, oval bokeh, edge
falloff) is written for film stills; `STAGE.md` needs square-on, straight verticals, no
depth of field. LIRA's **Soul Cinema location template** is compatible: camera anchor first
("the hardest part; anchor it hard"), real-world genre terms (24mm, real estate interior
photo), optics/DOF kept off locations, one register line, emptiness stated positively.
`house-rules` gives scene plates to banana; `CLAUDE.md` puts `STAGE.md` above both, so
**LIRA's location template governs SOTR plates.** Flagged once, here.

**FINDING 3 — `LOOK.md`'s reason for leading with the style prefix does not apply.** It
cites `house-rules` finding 15, which is about a *stylised* register fighting photoreal text
(LGEL). SOTR's prefix is itself photographic; there is no competing register. LIRA puts the
camera anchor first. A condition that expired — yesterday's lesson.

**Also from Cully's brief:** locations are generated three-quarter, never frontal, because
a frontal wall is "flat wallpaper" the model can't read volume from. SOTR's walls must be
frontal (`STAGE.md`), which is one more reason the room master — a wide with volume — has
to exist and the walls should be derived from it rather than invented.

### 2026-09-22 — IMG, pre-flight on S9-SAL-ROOM · portrait made Bourbon

**Judge approved** at full resolution (1536 x 2752); Homie filled the white V at the throat,
which read as a clerical collar. Details in `REGISTER.md`.

**PRE-FLIGHT FINDING, before any salon credit was spent.** The locked room contents asked
for *"a king in coronation robes."* The best-known full-length French coronation portrait
is Gérard's *Napoleon in Coronation Robes* (1805) — the same painter as the Louis XVIII we
composite. A model asked for a French king in 1817 has a real chance of painting Napoleon,
and a Napoleon on a royalist salon wall is the judge's collision again, in the image the
director signs off. The composite covers it on the final LEFT wall; nothing covers it in
the room master.

**Changed (Homie approved a LOCKED edit):** the portrait is now *"a Bourbon king in blue
velvet coronation robes sown with gold fleurs-de-lis."* Fleurs-de-lis are the Bourbon mark;
bees would be Napoleon's. Ermine was offered and dropped to save characters — fleurs-de-lis
are the discriminator, and Napoleon wore ermine too. Updated word for word in
`SHOTCARDS.md` and all four salon prompts. To pay for it: the room master's camera
paragraph tightened (no meaning cut), and "perfectly" dropped from the C/L/R camera lines,
kept parallel. All four now under 2,000 characters.

### 2026-09-21 — IMG session close · first asset generated

**First generated asset in the production.** `@fig_SOTR_judge_s9_v1`, at `testing`.
Four prompt versions, four batches, and three of the four failures were **design errors
caught before they reached the expensive cues** — a robed judge would have been wrong on
all five, and a Napoleon would have been wrong three times over on Q4's tribunal.

**The pattern worth carrying forward, because it hit three times in one asset.** Each
failure was *a clause that was correct under a condition that had stopped being true*:

| | Clause | Condition that expired |
|---|---|---|
| v1 to v2 | robe and toque | never checked which court tried Chaumareys |
| v2 to v3 | bicorne, tailcoat, sword | correct dress, but the icon it built was Napoleon, which `BIBLE.md` bans |
| v3 to v4 | "mouth open mid-proclamation" | worked in profile as a notch in the outline; impossible frontal |

**Standing check from here on: when the pose, reference structure or register changes,
re-read the whole spec for clauses that silently depended on the old state.** Same shape as
`house-rules` finding 15 — a spec is silent about conditions that were constant across
every version that worked.

**Second finding: accuracy and legibility are different axes.** v2 was historically correct
and read as the wrong regime. Getting the history right is not the same as getting the
reading right, and the audience only ever sees the second one. Both matter and they must be
checked separately. This will apply to the salon and studio plates, which are full of
period detail nobody will consciously read.

**Third: change the noun, not the negation.** Three versions banned facial features by name
and got faces. One version asked for a paper cut-out instead of a man and got none. When a
defect survives being named, ask what the model thinks the object *is* (`house-rules` 5c).

**Working folder decided (Homie):** `C:\Users\Homie\Documents\SOTR_MEDIA\`, outside the repo, with its own
`README.txt` carrying the subfolder layout and the naming rule that matches `REGISTER.md`
tags. Recorded in `docs/SOURCES.md`.

**Windows PC set up this session:** git and Python 3.13 confirmed, `Precision-Pipeline`
cloned and its seven skills copied into `~/.claude/skills` (the installer crashed on
pre-existing symlinks pointing at an older unpacked copy — they were removed first), this
repo cloned, the source folder audited against `docs/SOURCES.md` and the Windows path
committed. Git identity set globally.

**Still not logged: the aspect-ratio options each model offers.** Asked for three times and
not yet captured. `PIPELINE.md` 3-5 wants it on first use.

**Next session is IMG and starts on `S9-SAL-ROOM`** — the salon room master, the ground
truth all three salon walls derive from, and the first real test of the locked Soul Cinema
routing.

### 2026-09-21 — IMG, every facial hook removed

**FINDING — the faces were specified, not hallucinated.** Three versions were spent asking
for "no facial features" while the same paragraph asked for **"mouth open
mid-proclamation."** The model obeyed the mouth, and having opened the head it filled in
eyes and a nose too. The clause was never wrong in itself — **in profile an open mouth is a
notch in the head's outline**, which is why it worked and why `LOOK.md` used to call the
nose and mouth "the only face there is." Turning the figure frontal made it impossible to
render in outline, and nobody went back to check which clauses depended on the old pose.

**This is the same failure shape as the Napoleon one, for the third time: a decision that
was correct under a condition, carried forward after the condition changed.** Worth
treating as a standing check — when a pose, reference structure or register changes, re-read
the whole spec for clauses that silently depended on the old state.

**Cutting the mouth costs nothing.** `SHOTCARDS.md` already rules out lip sync and
`BIBLE.md` requires the Judge's voice to be pre-recorded, since his actor is on stage as
Sarah. Homie's own call: avoid the mouth if we can, and we can.

**The hat is cut (Homie).** Top hat in v1, historically correct but Napoleonic in v2,
Napoleonic again worn athwart in v3. Three versions, three failures, one element. Per
`house-rules` finding 5c, a defect that survives a named instruction is usually what the
model thinks the object *is* — a wide two-cornered hat **is** the frontal Napoleon image.
A fourth wording attempt would have failed the same way. **A bare, featureless head is also
the most suggestive option and the truest to the idea: a faceless institution.** Epaulettes
and squared shoulders carry the military read without it.

**The noun changed too, and this is the mechanism that should hold.** v4 asks for **"a
single shape cut from black paper with scissors"** rather than a man rendered in black. We
had been asking for a person and then forbidding what persons have. A cut-out has no face
to begin with.

**Plan confirmed with Homie**, with two corrections: the growth is a **hard jump on each
strike, not a zoom** — cameras are locked and the scaling happens in the comp — and the
escalation changes kind twice: one man, bigger, too big for the frame, three of him, then
**no man at all, only the gavel** at Q5.

**Changed:** `LOOK.md` World 3, `SHOTCARDS.md` S9-CRT figure row and deliverables line,
`prompts/S9-CRT-FIG.txt` → v4. **One change, one mechanism:** remove every facial hook.

### 2026-09-21 — IMG, court figure turned frontal

**FINDING — accuracy and legibility are different axes, and here they pulled apart.** v2's
costume was correct for a Rochefort naval court martial and it read as **Napoleon**, which
`BIBLE.md` forbids: the court is the **Bourbon** state covering for its own, and an Imperial
read points the image at the wrong regime. Bicorne + tailcoat + sword + side profile is one
of the most over-determined silhouettes there is. Getting the history right is not the same
as getting the reading right, and the second one is what the audience sees.

**Decided with Homie: frontal, full figure, mass over costume.**

- **Frontal.** A profile figure has a direction and pushes the eye off CENTRE toward the
  next wall; these walls are symmetrical and a centred head-on figure sits right on them.
  It also puts the accusation on the audience, who sit where the public gallery sits, and
  the script has him reading "like a town crier" — a crier faces the crowd. Frontal breaks
  the Napoleon quote, which is a profile and three-quarter icon.
- **Cost accepted:** the bicorne loses legibility head-on (a narrow point rather than a
  wide crescent), and Q4's inward-facing composition is gone. Q4 is now three identical
  frontal judges, used as generated with **no mirroring** — closer to a real court martial
  panel facing the accused.
- **Mass over costume.** Costume specificity is what caused the collision. **Sword and
  coat tails cut.** Squared shoulders, fringed epaulettes and the raised gavel carry it.
- **Full length kept deliberately.** The growth only lands if he starts whole: contained at
  Q1, closing at Q2, outgrowing the frame at Q3, multiplying at Q4, gone at Q5 with only the
  gavel. Crop him early and Q3 has nowhere to go.

**DELIBERATE EXCEPTION to one-change-at-a-time.** v3 carries two changes: the pose/costume,
and an explicit ban on interior white detail. Justified because they sit on **independent
axes and are both independently visible in the return** — you can see at a glance whether
he is frontal and whether there is white inside the black, so attribution is not destroyed.
Logged as two separate rows so this stays honest rather than becoming a habit.

**Changed:** `LOOK.md` World 3 (figure, Q4 row, whole-objects rule), `SHOTCARDS.md` S9-CRT
figure row and Q4 cue, `prompts/S9-CRT-FIG.txt` → v3.

### 2026-09-21 — IMG, court figure reversed to a naval officer

**FINDING — the court figure was the wrong institution, and the prompt could never have
fixed it.** S9-CRT-FIG v1 asked for *"a French judge of 1817… a long judicial robe… a tall
cylindrical toque."* That is the dress of a **civil magistrate of the Palais de Justice**.
Chaumareys was tried at **Rochefort in February 1817 by a naval court martial** — a
*conseil de guerre maritime*, a panel of **naval officers in uniform**. A robed magistrate
presiding over a naval tribunal is not a costume error, it is the wrong body trying the
case. Four generations were spent before anyone checked, and no amount of wording would
have reached the right figure.

**Verified before rewriting** (`BIBLE.md` requires it): the Rochefort 1817 court martial
and its five counts; that Restoration naval full dress is *habit* + *épaulettes* + bicorne;
and that from about 1800 navies wore the bicorne **fore-and-aft** rather than athwart, for
wind resistance. That last one is a gift to this asset — fore-and-aft reads in strict
profile as a wide pointed crescent, where athwart would collapse to a small cap.

**The gavel stays.** It is an Anglo-American object and no French court has used one, but
the script writes it (`BIBLE.md` beat 3: *"Order! Order!" The gavel*), `BIBLE.md` makes the
play's version canon, and all five cues — the escalating strikes, the hard size jumps, the
room shudder — are built on it. Swapping in a *sonnette* would be purer history and would
gut the design. **Logged as deliberate licence, not an oversight**, so nobody re-opens it.

**Also fixed: v1's decision had no recorded reason.** The 2026-09-21 PREP session switched
from the naval officer to the robed judge and logged only *"a judge in a robe (not the naval
officer)"*. No why. That gap is what let the error survive into a generation.

**Changed:** `LOOK.md` World 3 figure, `SHOTCARDS.md` S9-CRT figure row, and
`prompts/S9-CRT-FIG.txt` → v2. **One change only** — the costume. Style prefix, framing,
gavel, scroll, pose and the two-tone treatment are all word for word as v1.


### 2026-09-21 — PREP, all three looks locked, cards and IMG prompts written

**Locked with Homie.** Salon: Soubise white-and-gold with crimson silk, a trumeau mirror on
CENTRE, LIT plus a DARK state made as an NBP edit, true scale with a 3.2 m panel line.
Louis XVIII's portrait on LEFT (the salon's solo wall), composited from Gérard. Studio: the
whole Raft painting scaled to a 3.2 × 4.7 m canvas (liberty taken so the apex reads at beat
9), window on RIGHT, limb studies only. Court: **a judge in a robe** (not the naval officer),
and the **strike is generated** as image-to-video from the still, with a Q5 fallback.

**house-rules conflicts, project files followed:** "three-quarter, never frontal" (STAGE
wants square-on), "rule of thirds" (walls are symmetrical). Also fixed LOOK's model routing
to Soul Cinema for plates and NBP for edits, and cut the prompts to the ~2,000-character cap.

**Written:** 9 IMG prompts plus the DARK template in `prompts/`, built from the locked
prefixes and room contents, and checked word for word against `LOOK.md` and
`SHOTCARDS.md`. **Nothing generated.** Homie playtests next.

**Standing preference (Homie):** the worlds are ours to shape, not literal copies of
references or history.

**Same session, Homie's direction:** (1) **every object lives whole on one wall.** Nothing
straddles a seam. Each wall is a complete composition, and only architecture, light and
colour cross. Written into CLAUDE.md, STAGE.md and the seam check in PIPELINE.md, and added
to the room contents of every prompt. (2) The court's Q4/Q5 broke that rule, so they became
a **tribunal of three**: whole judges on L and R (R mirrored) striking in unison, and at Q5
each wall gets its own gavel. (3) **Floor projection is parked, not ruled out.**

**Client document:** `docs/SOTR-Scene9-Projection-Direction.pdf` (7 pages, plain language,
no names, Scene 9 only), built by `tools/make_client_pdf.py`. It's gitignored and kept
local; the builder is in git. Homie sends it himself.

**Open:** The wall-by-beat map
needs director sign-off. Aspect ratios per model still unlogged. Loop prompts and
S9-CRT-STRIKE wait for a VID session.

### 2026-09-21 — PREP, setup

Read the full source folder: the workshop script, work schedule, visual references, 2022
presentation, staging plan v0.2, UE5/Unity snapshots and both 2022 dev-showing videos.
Scope set with Homie: Scene 9 Court Martial, Salon and Studio, in about one week. Staging:
three surfaces (L 4800 × 3600, C 6000 × 3600, R 4800 × 3600, flats at 25°), cameras
locked. Decided: walls-as-walls rendering, transitions in compositing, the Raft painting
composited. Proposed, **not locked**: all three world looks, the naval-officer silhouette,
the wall-by-beat map.

Same day, Homie's direction: work at 1080p and upscale approved results to 4K. No projector
spec needed, because the mapping software does the final fit. Sound is a separate designer,
and our timing leads. Goal: one cohesive video across three screens. Adopted Homie's order
(cards, then front, left, right) and added two things: a **room master** before the front
camera, and a **wide-canvas master comp** (4680 × 1080) where every cross-screen event is
built. Written up as `PIPELINE.md`.

Frame rate: native is fine (24 OK), higher when a model offers it. No forced
interpolation. Post VFX is an optional upgrade; generation comes first.

Salon research: the Cooper Hewitt Restoration salon (buff and blue, restrained) against
the script and references (old-regime gilt, Hôtel de Soubise). Recommended gilt. Four open
choices logged in `LOOK.md`. Found Homie's 2022 studio concept (Slide 9), the only prior
Scene 9 visual, and noted it as the studio's starting layout. Added
`docs/HANDOVER-WINDOWS.md` for the PC.
