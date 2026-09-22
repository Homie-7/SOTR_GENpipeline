# LOG — SOTR

One row per generation. Change one thing at a time. After 15–20 attempts on one plate,
change the plate, not the sentence.

| Date | ID | v | Model | Changed | Verdict | Note |
|---|---|---|---|---|---|---|
| 2026-09-22 | S9-CRT-FIG | 4 | - | full-resolution check of variant 3 | **APPROVED** | 1536x2752. Head, gavel, epaulettes clean. One white V at the throat reads as a clerical collar at large sizes; comp fill, logged in REGISTER. |
| 2026-09-21 | S9-CRT-FIG | 4 | NBP | noun changed to a paper cut-out; hat cut; mouth cut | **PASS - variant 3 selected** | **Faces gone in all four.** The noun change is what did it: asking for "a shape cut from black paper" instead of a man rendered in black leaves no face to forbid. No hats, frontal, symmetrical, gavel clear of the head, scroll readable from outline alone, legs showing below the coat so it does not read as a robe. **One defect left:** epaulette fringe returns as white hatching. Banned by name in v3 and v4 and it survived both, so it is an object prior, not a wording fault - **fixed in the comp, not chased in generation** (LGEL lanyard precedent). Homie picked variant 3 over 1 on head shape. |
| 2026-09-21 | S9-CRT-FIG | 3 | NBP | profile -> frontal, costume reduced, interior white banned | **FAIL — faces, and the hat went Napoleonic again** | Frontal and symmetry took. **Faces in all four**, variant 3 fully rendered with eyes and nose. **Root cause found: our own spec.** "No facial features" and "mouth open mid-proclamation" contradict each other; the model obeyed the mouth. In profile that was consistent (a mouth is a notch in the outline) — frontal it can only be interior detail, and it opens the door to eyes and nose. **A clause that was right under a condition that stopped being true.** Hat returned athwart = Napoleon, third version running. |
| 2026-09-21 | S9-CRT-FIG | 2 | NBP | costume corrected to naval officer | **FAIL — reads as Napoleon** | Institution now right, icon now wrong. Bicorne + tailcoat + sword + side profile is the Napoleon silhouette, and `BIBLE.md` bans Napoleonic motifs — this is the Bourbon state, not the Empire. **The historically accurate costume produced a historically wrong reading.** Second defect, independent: white collar, white buttons and fringed epaulette detail inside the black in **all four** variants — no longer seed variance, a real prompt fault. |
| 2026-09-21 | S9-CRT-FIG | 1 | NBP | first generation, 4 variants, 9:16 | **FAIL — wrong institution** | Prompt executed correctly; the *design* was wrong. See the finding below. Variants 1-2 closest to spec; v3 failed two-tone (tan field, grey in the figure), v4 carried interior detail and a face profile. Per LGEL, 1 bad in 4 is seed variance, not a prompt fault — not treated as defects. The toque rendered as a Victorian stovepipe in all four, which is moot now the toque is cut. |

---

## Sessions

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
