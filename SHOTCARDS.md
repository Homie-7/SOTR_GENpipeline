# CUE CARDS — Scene 9

Cards come before prompts. The ID here is the same ID used in `LOG.md`, `REGISTER.md` and
`prompts/<ID>.txt`.

**ID scheme:** `S9-<WORLD>-<WALL>` for plates, where WORLD is `SAL` / `STU` / `CRT` and WALL
is `L` / `C` / `R`. Loops add `-LOOP`, and composited cues add `-Q<n>`.

---

## Deliverables at a glance

| ID | What | Made in | Depends on | Status |
|---|---|---|---|---|
| S9-SAL-ROOM | Salon room master, all three of the room's own walls in one wide design image (never projected) | Higgsfield (image) | LOOK salon locked | **approved** |
| S9-SAL-R | Salon's one active wall (the portrait), plays on the physical RIGHT flat | Higgsfield (image) | S9-SAL-ROOM approved | prompt ready |
| S9-SAL-R-LOOP | Salon loop (candles, glints) | Higgsfield (video) | S9-SAL-R | not started |
| S9-SAL-R-DARK | Salon, candles unlit, dusk only. NBP edit of the approved LIT plate | Higgsfield (image edit) | S9-SAL-R approved | prompt ready (template) |
| S9-SAL-R-PORTRAIT | Gérard's Louis XVIII (public domain) composited into the frame | compositing | S9-SAL-R | source verified |
| ~~S9-SAL-C, S9-SAL-L~~ | The room's other two walls (mirror, window) — **not needed**, the salon never shows more than one wall | — | — | retired 2026-09-22 |
| S9-STU-ROOM | Studio room master, all three of the room's own walls (never projected) | Higgsfield (image) | LOOK studio locked | regenerating (light changed to night) |
| S9-STU-L | Studio's one active wall (the canvas, re-staged as a side-wall elevation), plays on the physical LEFT flat | Higgsfield (image) | S9-STU-ROOM approved | prompt ready |
| S9-STU-L-LOOP | Studio loop (dust, candlelight, canvas edge) | Higgsfield (video) | S9-STU-L | not started |
| S9-STU-L-PAINT1/2/3 | Raft painting in three stages on the canvas | compositing | S9-STU-L | not started |
| ~~S9-STU-C, S9-STU-R~~ | The room's other two walls (window, shelves) — **not needed**, the studio never shows more than one wall | — | — | retired 2026-09-22 |
| S9-CRT-FIG | Naval officer silhouette, frontal, bare featureless head, gavel raised, scroll | Higgsfield (image) | LOOK court locked ✓ | **approved** |
| S9-CRT-STRIKE | One gavel strike, black on white | Higgsfield (video, image-to-video) | S9-CRT-FIG approved | prompt in a VID session |
| S9-CRT-Q1…Q5 | The five strike cues at growing scale (Q4/Q5 the only moment all three walls carry one world) | compositing | S9-CRT-STRIKE | not started |
| Transitions | Salon candle-in/out, studio paint-in/bleach, court hard cut | compositing | all plates | not started |

**Simplified 2026-09-22, after the client's wall assignment.** Each world holds one wall for
its whole run (the court's climax excepted), so the build is now **2 room masters (design
reference only, never projected), 2 wall plates, 2 loops, 1 figure and 1 strike** — down
from the 6 wall plates and 6 loops this table listed yesterday, since three walls per room
were never going to be shown in performance. Workflow in `PIPELINE.md`.

---

## Which world goes on which wall, beat by beat — CONFIRMED 2026-09-22

**From the client, via Homie, audience-perspective confirmed:** salon on the audience's
RIGHT, Géricault's studio on the LEFT, the judge on the back screen (CENTRE). The raft is
physical — a riser in the middle of the floor, not a wall — and stays out of scope
(`BIBLE.md`).

**Each world holds exactly one wall for its whole run, no exceptions except the court's own
climax.** `LOOK.md` already called the portrait wall the salon's "solo wall" before this
was confirmed — beats 2 and 8 never used more than one wall in the first place. The change
is which physical wall: RIGHT, not LEFT. The studio simplifies the same way: one wall,
carrying the canvas — its dramatic centre, and at 4.7 m on a 4.8 m flat, close to true
scale filling it — rather than splitting canvas/window/shelves across three.

| Beat | Fragment | LEFT (studio) | CENTRE (court) | RIGHT (salon) |
|---|---|---|---|---|
| 2 | Salon: the letter | black | black | **Salon** (candles in) |
| 3 | Court: "One!" | black | **Court Q1** | salon dims |
| 4 | Studio: the head | **Studio** (paints in, PAINT1) | black | black |
| 5 | Court: "Two!", "Three!" | studio bleaches | **Court Q2 → Q3** | black |
| 6 | Studio: "Vingt!" | Studio (PAINT2) | black | black |
| 7 | Court: the verdict | black (optional light flash, see below) | **Court Q4 → Q5** | black (optional light flash, see below) |
| 8 | Salon: "Mais bien sûr" | black | black | **Salon** |
| 9 | Studio: "I will bring down…" | **Studio (PAINT3)** | black | black |

**CORRECTED 2026-09-23:** the court's climax is one judge on CENTRE only, growing then
cropped tighter with each strike, never spreading to LEFT or RIGHT — see `LOOK.md` World 3
and `LOG.md` 2026-09-23. A prior version had the climax spread across all three walls as a
"tribunal of three"; that was never a real decision and is reverted. No two worlds ever
share a wall, and the court no longer breaks that rule either — every beat, including the
climax, plays on one wall. LEFT and RIGHT may optionally carry a light/colour flash at Q4→Q5
to sell the room-wide impact (within the seam rule: only light and colour may cross), but
that's an open comp suggestion, not locked — confirm with Homie before building it.

---

## S9-SAL — The Salon · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Rococo salon in a royalist château, 1817, evening. `LOOK.md` → World 1 (LOCKED) |
| **Wall** | **One active wall — the portrait — plays on physical RIGHT** (confirmed 2026-09-22). The room's own mirror and window walls are part of the room master for reference and design sign-off only; they are never projected |
| **In frame** | No people. The mirror reflects an empty room |
| **Camera** | Locked. Square to the wall, eye level 1.6 m, floor to 3.6 m, no floor visible |
| **Scale anchors** | Dado 0.9 m · mantel 1.1 m · sconce centres 1.9 m · panel tops and window head 3.2 m |
| **States** | LIT (generated) · DARK (NBP edit of the approved LIT: candles unlit, dusk only) |
| **Loop motion** | LIT only. Candle flames, glints on gilt, a soft stir of candlelight in the mirror, a faint breath in the curtains. Keep 300 mm clear of each seam |
| **Enters / exits** | The comp reveals LIT through DARK one candle at a time, gilt first · candles snuff out, back to DARK |
| **Model** | Soul Cinema (room master, plates) · NBP (DARK edits) |

**Room contents. Quote this word for word in the room master prompt.** Since the salon
plays on a single confirmed wall (`S9-SAL-R.txt`), that prompt is reference-led off the
approved room master instead (`PIPELINE.md` 3–5) rather than quoting this text directly —
this quote's job now is the room master and the design sign-off.

> A rectangular salon with flat walls meeting at square corners. Ivory panels framed in gilt
> mouldings, their tops at 3.2 metres, stand above a gilt dado rail at 0.9 metres with plain
> panelling below. Back wall: a white marble chimneypiece, mantel at 1.1 metres with two
> gilt candelabra of lit candles; above it a tall gilt-framed trumeau mirror rises to 3.2
> metres, its old glass giving back a soft, dim reflection of the empty candlelit salon. Left wall: a full-length royal portrait of a Bourbon king in blue velvet
> coronation robes sown with gold fleurs-de-lis, in a heavy carved gilt frame. Right wall: a tall French window, head at 3.2 metres, crimson
> silk curtains drawn closed, a thin line of blue-grey dusk along their edges. Each of these
> is flanked by two-branch gilt sconces of lit candles at 1.9 metres. Every feature sits
> whole on its own wall, with plain panelling near every corner.

## S9-STU — Géricault's studio · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Faubourg-du-Roule studio, 1818–19, two in the morning, candlelit. `LOOK.md` → World 2 (LOCKED) |
| **Wall** | **One active wall — the canvas, re-staged as a side-wall elevation — plays on physical LEFT** (confirmed 2026-09-22). At 4.7 m wide on a 4.8 m flat it nearly fills it: the canvas becomes the room. The window and shelves are part of the room master for reference only; they are never projected |
| **In frame** | No people. No remains, only studies on paper |
| **Camera** | Locked. Square to the wall, eye level 1.6 m, floor to 3.6 m, no floor visible |
| **Scale anchors** | Canvas 0.2–3.4 m high, 4.7 m wide (~3:2), close to true scale on the 4.8 m flat |
| **Light** | One source, motivated by the room's own candle (on the window's sill, per the room master) but shown off-frame on the active wall: warm light falling hard across the canvas, dying to deep umber at the wall's far edge. 2am, candlelit. *Changed 2026-09-22 from daylight — see LOOK.md and LOG.md* |
| **Loop motion** | Dust in the candlelight, the canvas's raw edge catching a flicker. The candle (off-frame) dimming and swelling is a light pass in the master comp (replaces the cloud, 2026-09-22, and the room's own guttering-candle motion, which lived on the now-retired window wall). Keep 300 mm clear of each seam |
| **Enters / exits** | Paints itself in, charcoal to colour, through brushstroke masks · bleaches back to raw canvas, the edges breaking into particles |
| **Model** | Soul Cinema. The painting is composited (PAINT1/2/3) |

**Room contents. Quote this word for word in the room master prompt only.** Since the
studio plays on a single re-staged wall (`S9-STU-L.txt`), that prompt does not quote this
text — it composes a new elevation of the canvas alone. This quote's job now is the room
master: the design sign-off and the materials/light reference every wall is checked against.

> A large rectangular studio with flat walls meeting at square corners, at two in the
> morning. Raw grey lime plaster walls, stained and patched, above a worn wooden skirting.
> Back wall: a huge stretched canvas, 3.2 metres high and 4.7 metres wide, its bottom edge
> 0.2 metres up on wooden blocks, primed flat warm off-white, entirely blank, square to the
> wall, with plain plaster around it. Right wall: a tall north window of small square
> panes, sill at 1.2 metres, rising past 3.6 metres, a dark night sky and a thin moon
> beyond the glass; pencil and oil studies of arms, legs and hands pinned to the plaster
> between 1.2 and 2.4 metres, just visible; on the sill, a candle burning in a tin holder
> beside a red-stained rag — the room's only light. Left wall: rough pine shelves at 1.4
> and 2.2 metres holding white plaster casts of antique heads and a hand, and a small
> wooden scale model of a raft; three canvases lean face to the wall beneath, nearly lost
> in the dark. Every object sits whole on its own wall, with bare plaster near every
> corner.

## S9-CRT — The Court Martial · LOCKED 2026-09-21

| | |
|---|---|
| **World** | Abstract. Pure black silhouette on a bone-white backlit field. `LOOK.md` → World 3 (LOCKED) |
| **Figure** | A **naval officer** of 1817, **facing the audience square-on**, full length, symmetrical. **Bare, completely featureless head — no hat.** High collar, squared shoulders with fringed epaulettes, long coat falling straight, planted stance. **No sword, no tails, no mouth.** Gavel raised clear of the head in the right hand, scroll held out in the left. **One unbroken mass of solid black — no white or grey inside the outline, no eyes, nose, mouth, hair or hat.** *v1 robed judge: wrong institution. v2 profile: Napoleon. v3 hat: Napoleon again. All corrected 2026-09-21 — see `LOOK.md` and `LOG.md`. The gavel is deliberate licence* |
| **Action** | S9-CRT-STRIKE: image-to-video from S9-CRT-FIG. Locked camera, one hard strike, then hold. **The prompt is written in a VID session.** Thresholded to pure black and white in the comp |
| **Cues** | Q1 about 1.2 m, CENTRE → Q2 about 2.4 m → Q3 fills CENTRE, head cropped → Q4 push-in crop on the same figure, chest and head filling CENTRE, gavel huge → Q5 the gavel alone fills CENTRE, coming down from its top edge, then cut to black. **One judge throughout (corrected 2026-09-23 — `BIBLE.md` says "only the Judge is animated"; a prior "tribunal of three" was never a real decision, see `LOG.md`).** He never leaves CENTRE, so he never approaches a seam. Each size is a hard jump on the strike, with a shudder on the field |
| **Q5 risk** | A gavel filling a whole wall is a 5–10× enlargement. Upscale the strike to 4K first. Fallback for Q5 only: a vector trace of the still, rotated by keyframes |
| **Sound link** | Our timing leads. The scale jumps are timed to the drama, and the separate sound designer places the gavel hits on them. Mark each jump's timecode at handover |
| **Voice** | Pre-recorded (the Judge's actor also plays Sarah, who is on stage). No lip sync: it's a silhouette |
