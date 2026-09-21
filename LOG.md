# LOG — SOTR

One row per generation. Change one thing at a time. After 15–20 attempts on one plate,
change the plate, not the sentence.

| Date | ID | v | Model | Changed | Verdict | Note |
|---|---|---|---|---|---|---|
| 2026-09-21 | S9-CRT-FIG | 3 | NBP | profile -> frontal, costume reduced, interior white banned | **FAIL — faces, and the hat went Napoleonic again** | Frontal and symmetry took. **Faces in all four**, variant 3 fully rendered with eyes and nose. **Root cause found: our own spec.** "No facial features" and "mouth open mid-proclamation" contradict each other; the model obeyed the mouth. In profile that was consistent (a mouth is a notch in the outline) — frontal it can only be interior detail, and it opens the door to eyes and nose. **A clause that was right under a condition that stopped being true.** Hat returned athwart = Napoleon, third version running. |
| 2026-09-21 | S9-CRT-FIG | 2 | NBP | costume corrected to naval officer | **FAIL — reads as Napoleon** | Institution now right, icon now wrong. Bicorne + tailcoat + sword + side profile is the Napoleon silhouette, and `BIBLE.md` bans Napoleonic motifs — this is the Bourbon state, not the Empire. **The historically accurate costume produced a historically wrong reading.** Second defect, independent: white collar, white buttons and fringed epaulette detail inside the black in **all four** variants — no longer seed variance, a real prompt fault. |
| 2026-09-21 | S9-CRT-FIG | 1 | NBP | first generation, 4 variants, 9:16 | **FAIL — wrong institution** | Prompt executed correctly; the *design* was wrong. See the finding below. Variants 1-2 closest to spec; v3 failed two-tone (tan field, grey in the figure), v4 carried interior detail and a face profile. Per LGEL, 1 bad in 4 is seed variance, not a prompt fault — not treated as defects. The toque rendered as a Victorian stovepipe in all four, which is moot now the toque is cut. |

---

## Sessions

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
