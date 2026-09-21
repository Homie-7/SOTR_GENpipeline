# CUE CARDS — Scene 9

Cards come before prompts. The ID here is the same ID used in `LOG.md`, `REGISTER.md` and
`prompts/<ID>.txt`.

**ID scheme:** `S9-<WORLD>-<WALL>` for plates, where WORLD is `SAL` / `STU` / `CRT` and WALL
is `L` / `C` / `R`. Loops add `-LOOP`, and composited cues add `-Q<n>`.

---

## Deliverables at a glance

| ID | What | Made in | Depends on | Status |
|---|---|---|---|---|
| S9-SAL-ROOM | Salon room master, all three walls in one wide design image (never projected) | Higgsfield (image) | LOOK salon locked | prompt ready |
| S9-SAL-C | Salon, centre wall plate | Higgsfield (image) | S9-SAL-ROOM approved | prompt ready |
| S9-SAL-L | Salon, left wall plate | Higgsfield (image) | S9-SAL-C approved | prompt ready |
| S9-SAL-R | Salon, right wall plate | Higgsfield (image) | S9-SAL-C approved | prompt ready |
| S9-SAL-{L,C,R}-LOOP | Salon loops (candles, glints) | Higgsfield (video) | each plate | not started |
| S9-SAL-{L,C,R}-DARK | Salon, candles unlit, dusk only. NBP edit of each approved LIT plate | Higgsfield (image edit) | each LIT plate approved | prompt ready (template) |
| S9-SAL-L-PORTRAIT | Gérard's Louis XVIII (public domain) composited into the LEFT frame | compositing | S9-SAL-L | not started |
| S9-STU-ROOM | Studio room master (never projected) | Higgsfield (image) | LOOK studio locked | prompt ready |
| S9-STU-C | Studio, centre wall (blank primed canvas, 3.2 × 4.7 m) | Higgsfield (image) | S9-STU-ROOM approved | prompt ready |
| S9-STU-L | Studio, left wall (casts, raft model) | Higgsfield (image) | S9-STU-C approved | prompt ready |
| S9-STU-R | Studio, right wall (north window, studies) | Higgsfield (image) | S9-STU-C approved | prompt ready |
| S9-STU-{L,C,R}-LOOP | Studio loops (dust, daylight) | Higgsfield (video) | each plate | not started |
| S9-STU-C-PAINT1/2/3 | Raft painting in three stages on the canvas | compositing | S9-STU-C | not started |
| S9-CRT-FIG | Naval officer silhouette, frontal, bare featureless head, gavel raised, scroll | Higgsfield (image) | LOOK court locked ✓ | prompt ready |
| S9-CRT-STRIKE | One gavel strike, black on white | Higgsfield (video, image-to-video) | S9-CRT-FIG approved | prompt in a VID session |
| S9-CRT-Q1…Q5 | The five strike cues at growing scale | compositing | S9-CRT-STRIKE | not started |
| Transitions | Salon candle-in/out, studio paint-in/bleach, court hard cut | compositing | all plates | not started |

Two rooms × (1 master + 3 walls), plus the court. That's **2 room masters, 6 wall plates
(+3 salon DARK edits), 6 loops, 1 figure and 1 strike**, then the master comp. Workflow in `PIPELINE.md`.

---

## Which world goes on which wall, beat by beat — PROPOSED

Proposal only. This is the director's call and needs sign-off. Performers need to know
which wall they're playing against.

| Beat | Fragment | LEFT | CENTRE | RIGHT |
|---|---|---|---|---|
| 2 | Salon: the letter | **Salon** (candles in) | black | black |
| 3 | Court: "One!" | salon dims | **Court Q1** | — |
| 4 | Studio: the head | — | **Studio** canvas (PAINT1) | **Studio** (paints in) |
| 5 | Court: "Two!", "Three!" | — | **Court Q2 → Q3** | studio bleaches |
| 6 | Studio: "Vingt!" | — | Studio (PAINT2) | Studio |
| 7 | Court: the verdict | **Court Q4 → Q5** (tribunal) | **Court Q4 → Q5** | **Court Q4 → Q5** (tribunal) |
| 8 | Salon: "Mais bien sûr" | **Salon** | black | black |
| 9 | Studio: "I will bring down…" | — | **Studio (PAINT3)** | **Studio** |

The salon lives stage-left and the studio lives stage-right. They only meet at CENTRE, and
the court breaks through all three.

---

## S9-SAL — The Salon · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Rococo salon in a royalist château, 1817, evening. `LOOK.md` → World 1 (LOCKED) |
| **Walls** | C: trumeau, a gilt mirror over a marble chimneypiece, reflecting the chandelier · L: portrait of Louis XVIII (composited), sconces · R: French window, crimson curtains drawn, dusk at the edges, sconces |
| **In frame** | No people. The mirror reflects an empty room |
| **Camera** | Locked. Square to the wall, eye level 1.6 m, floor to 3.6 m, no floor visible |
| **Scale anchors** | Dado 0.9 m · mantel 1.1 m · sconce centres 1.9 m · panel tops and window head 3.2 m |
| **States** | LIT (generated) · DARK (NBP edit of the approved LIT: candles unlit, dusk only) |
| **Loop motion** | LIT only. Candle flames, glints on crystal and gilt, the chandelier in the mirror, a faint breath in the curtains. Keep 300 mm clear of each seam |
| **Enters / exits** | The comp reveals LIT through DARK one candle at a time, gilt first · candles snuff out, back to DARK |
| **Model** | Soul Cinema (room master, plates) · NBP (DARK edits) |

**Room contents. Quote this word for word in every salon prompt.** Only the camera paragraph
changes between prompts (the clone rule, `PIPELINE.md` 3–5). The prompts in `prompts/` are
built from this text.

> A rectangular salon with flat walls meeting at square corners. Ivory panels framed in gilt
> mouldings, their tops at 3.2 metres, stand above a gilt dado rail at 0.9 metres with plain
> panelling below. Back wall: a white marble chimneypiece, mantel at 1.1 metres with two
> gilt candelabra of lit candles; above it a tall gilt-framed trumeau mirror rises to 3.2
> metres, reflecting the empty salon, lit sconces and the lower tiers of a lit crystal
> chandelier. Left wall: a full-length royal portrait of a king in coronation robes in a
> heavy carved gilt frame. Right wall: a tall French window, head at 3.2 metres, crimson
> silk curtains drawn closed, a thin line of blue-grey dusk along their edges. Each of these
> is flanked by two-branch gilt sconces of lit candles at 1.9 metres. Every feature sits
> whole on its own wall, with plain panelling near every corner.

## S9-STU — Géricault's studio · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Faubourg-du-Roule studio, 1818–19, grey north daylight. `LOOK.md` → World 2 (LOCKED) |
| **Walls** | C: blank primed canvas 3.2 × 4.7 m, the painting composited in three stages · R: north window, pinned limb studies, candle stub and red rag on the sill · L: shelves of casts, raft model, canvases leaning face to the wall |
| **In frame** | No people. No remains, only studies on paper |
| **Camera** | Locked. Square to the wall, eye level 1.6 m, floor to 3.6 m, no floor visible |
| **Scale anchors** | Canvas 0.2–3.4 m high · window sill 1.2 m · shelves 1.4 and 2.2 m · studies 1.2–2.4 m |
| **Light** | One source: the window on RIGHT. Light falls right to left |
| **Loop motion** | R: dust in the window light, the guttering candle stub. All walls: the cloud passing is a light pass in the master comp. Keep 300 mm clear of each seam |
| **Enters / exits** | Paints itself in, charcoal to colour, through brushstroke masks · bleaches back to raw canvas, the edges breaking into particles |
| **Model** | Soul Cinema. The painting is composited (PAINT1/2/3) |

**Room contents. Quote this word for word in every studio prompt.**

> A large rectangular studio with flat walls meeting at square corners. Raw grey lime
> plaster walls, stained and patched, above a worn wooden skirting. Back wall: a huge
> stretched canvas, 3.2 metres high and 4.7 metres wide, its bottom edge 0.2 metres above
> the floor on wooden blocks, primed a flat warm off-white, entirely blank, square to the
> wall, with plain plaster around it. Right wall: a tall north window of small square panes,
> sill at 1.2 metres, rising past 3.6 metres, grey sky beyond; pencil and oil studies of
> arms, legs and hands are pinned to the plaster around it between 1.2 and 2.4 metres; on
> the sill, a stub of candle burning in a tin holder beside a red-stained rag. Left wall:
> rough pine shelves at 1.4 and 2.2 metres holding white plaster casts of antique heads and
> a hand, and a small wooden scale model of a raft; three stretched canvases lean face to
> the wall beneath. Every object sits whole on its own wall, with bare plaster near every
> corner.

## S9-CRT — The Court Martial · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Abstract. Pure black silhouette on a bone-white backlit field. `LOOK.md` → World 3 (LOCKED) |
| **Figure** | A **naval officer** of 1817, **facing the audience square-on**, full length, symmetrical. **Bare, completely featureless head — no hat.** High collar, squared shoulders with fringed epaulettes, long coat falling straight, planted stance. **No sword, no tails, no mouth.** Gavel raised clear of the head in the right hand, scroll held out in the left. **One unbroken mass of solid black — no white or grey inside the outline, no eyes, nose, mouth, hair or hat.** *v1 robed judge: wrong institution. v2 profile: Napoleon. v3 hat: Napoleon again. All corrected 2026-09-21 — see `LOOK.md` and `LOG.md`. The gavel is deliberate licence* |
| **Action** | S9-CRT-STRIKE: image-to-video from S9-CRT-FIG. Locked camera, one hard strike, then hold. **The prompt is written in a VID session.** Thresholded to pure black and white in the comp |
| **Cues** | Q1 about 1.2 m, CENTRE → Q2 about 2.4 m → Q3 fills CENTRE → Q4 tribunal of three: whole judges on L and R, all three facing the audience, striking in unison (frontal figure, no mirroring) → Q5 each wall filled by its own gavel coming down from its top edge, then cut to black. No figure or gavel ever crosses a seam. Each is a hard jump on the strike, with a shudder on the field |
| **Q5 risk** | A gavel filling a whole wall is a 5–10× enlargement. Upscale the strike to 4K first. Fallback for Q5 only: a vector trace of the still, rotated by keyframes |
| **Sound link** | Our timing leads. The scale jumps are timed to the drama, and the separate sound designer places the gavel hits on them. Mark each jump's timecode at handover |
| **Voice** | Pre-recorded (the Judge's actor also plays Sarah, who is on stage). No lip sync: it's a silhouette |
