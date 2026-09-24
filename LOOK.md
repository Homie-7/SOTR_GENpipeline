# LOOK — Scene 9

**Status: ALL THREE WORLDS LOCKED 2026-09-21.** Each world gets decided one at a time, with Homie. When a
world is locked, change its heading to `LOCKED <date>` and paste its style prefix into every
prompt for that world, word for word.

Default register: **hyper-real**, the way real, well-lit period interiors look. The court is
the exception because it's abstract by design.

---

## The idea that ties the three together

The three worlds are the people who decided how Agnès's story got told. **The court**
writes the official lie. **The salon** laughs at it. **The studio** refuses it and paints
the truth. They should be told apart instantly, even as fragments, by **light and finish**:

| World | Light | Finish | Base field | Accent (with its real source) | Counter-note |
|---|---|---|---|---|---|
| **Salon** | warm candlelight, many sources, symmetrical | **polish**: gilt, mirror, silk, immaculate | ivory boiserie, cream and gold | crimson silk (upholstery, curtains) | the cold grey of dusk behind drawn curtains |
| **Studio** | one candle at 2am, hard fall-off into dark | **patina**: dust, stains, raw plaster, chaos | umber dark, candle-gold, bone | dried-blood red (a rag, the palette) | the candle IS the light, not an accent |
| **Court** | a flat backlit field | none: graphic, no texture | bone-white | none | the silhouette itself, pure black |

The salon and studio are both period Paris interiors, so light and finish have to do the
separating. Warm polish against cold patina.

---

## World 1 — THE SALON · LOCKED 2026-09-21

### Decisions (Homie, 2026-09-21)

| # | Choice | Decision | Why |
|---|---|---|---|
| 1 | Palette | **White-and-gold boiserie (the Soubise model)**, with crimson silk on curtains and upholstery only | A light base keeps it apart from the studio's dark umber. Red walls would compete with the studio's dried-blood red, and dark damask loses detail at projector black levels. Candlelit evening keeps the ivory at an amber mid-tone, so the walls don't throw white light onto the actors |
| 2 | Centre wall | **A trumeau**: a tall gilt mirror over a white marble chimneypiece. It reflects the empty salon behind the viewer, including the chandelier | The room's one window of depth, and it puts the crystal and candle motion on CENTRE. **Risk:** a camera square-on to a mirror is looking at its own position. Describe the reflection positively (an empty room, the chandelier, far sconces). **Fallback after two failed generations:** mirror-glazed double doors |
| 3 | Plate states | **LIT, plus a DARK state made as an NBP edit of the approved LIT plate** (CHANGE the light, PRESERVE everything else) | The geometry matches, so the comp can reveal LIT through DARK one candle at a time. Only LIT is looped. **Fallback if the edit drifts:** grade LIT down in the comp |
| 4 | Scale | **True scale.** Dado rail 0.9 m, tops of the tall panels **3.2 m**, mantel 1.1 m, sconces 1.9 m, window head 3.2 m. Doors would be 2.8 m, but they sit on the audience wall and aren't seen | The 3.2 m panel line gives the seam check a second continuous line inside the 3.6 m crop. The richest elements (mirror, portrait, sconces, gilt) sit between 1 and 3.2 m |

**2026-09-22 (Homie + Claude, after the first room master): no chandelier.** The script asks only for "an ornate Louis XIV Salon"; the chandelier was ours. It hangs mid-room, so it never lands on a projected wall — its only appearance would be as a reflection in the CENTRE mirror, the hardest thing in the room to animate and loop (many small crystal highlights and flames, doubled). The mirror stays, as old dim glass with a soft reflection of the empty candlelit room. Candles stay: they are the "slowly revealed" mechanism. Decision 2 below is amended accordingly.

**The room is rectangular.** The real Salon de la Princesse is oval, so it's the reference for
the finish, not the plan. Seams have to fall on square corners. Its name isn't used in any
prompt, because the model would build the oval.

### Research (2026-09-21)

- **What a real Restoration salon looked like** is lighter and more restrained than most
  people picture. Hilaire Thierry's *Salon in the Restoration Taste* (Cooper Hewitt, early
  1820s, probably the Duchesse de Berry's apartment at Saint-Cloud) has **buff walls banded
  in blue**, floor-to-ceiling windows with afternoon light, a gilded tea service, rock
  crystal vases, a chandelier, and a chair and canapé in the new post-1814 style.
- **What the script and references ask for** is older and louder. The script says "an
  ornate Louis XIV Salon." The two `INSPO/Sc 9` references are a red-damask
  Versailles-style room, and the white-and-gold **Salon de la Princesse, Hôtel de Soubise**
  (Boffrand, 1735–40): oval, gilded boiserie, mirror glass set into the panelling, painted
  overdoors. That room is where aristocratic Paris gathered before the Revolution.
- **The fork, resolved:** old-regime gilt. A royalist in 1817 sitting in a surviving
  pre-Revolution Rococo room is historically plausible, since the Restoration was nostalgic
  for exactly that. It's also what the script asks for and what the audience reads at a
  glance.
- **Fact check on the court.** The real verdict (Rochefort, 1817) convicted Chaumareys of
  incompetent navigation and of abandoning the ship before everyone was off. He got three
  years, and lost his rank and Légion d'honneur. He was acquitted of abandoning the raft.
  The play's full acquittal is licence; `BIBLE.md` keeps the play's version.

### The walls (true scale, 3.6 m crop)

**Where.** Marie-Louise's salon in a royalist château, 1817, evening. An old 1730s Rococo
room, kept immaculate.

- **CENTRE**: the trumeau. A white marble chimneypiece (mantel 1.1 m, a pair of gilt
  candelabra on it), with the mirror rising above it to 3.2 m. Two sconces at 1.9 m, one on
  each side.
- **LEFT**: a full-length **portrait of Louis XVIII** in coronation robes, in a heavy gilt
  frame, with a sconce on each side. LEFT is the salon's solo wall (beats 2 and 8), so the
  king who "loves his loyal subjects" is behind Marie-Louise when she reads the letter.
  **The painting itself is composited, not generated:** François Gérard's coronation
  portrait (c. 1814, public domain). A generator paints its own wrong king, which is the
  same rule as the Raft. Confirm the source image before the comp.
- **RIGHT**: a tall French window (head at 3.2 m), crimson silk curtains drawn, a thin line
  of cold dusk at their edges, with a sconce on each side. That's the counter-note.
- **Below the dado, and near every corner:** plain panelling. Nothing is painted at the
  floor line, where it would collide with real props, and hard detail stays 300 mm clear
  of the seams.

**Motion for the loops (LIT only).** Candle flames, glints moving across crystal and gilt,
a soft stir of candlelight in the old mirror glass, a faint drift of warm air in the curtains. Nothing
else.

**AMENDED 2026-09-24 (Homie + Claude): what moves on the ONE wall we build.** The list above
was written for three walls. The mirror and curtains are on retired walls, so they're out.
The portrait wall moves **the six flames, and the warm halo each sconce throws on the panels,
breathing with them**, plus glints on the gilt nearby. The halo is the part that matters: a
flame is about 27 mm at true scale, a dot from the seats, while each halo is about 650 mm
across. The outer panels and corners stay steady, so the wall never flickers as a whole.
**The salon's candles are calm on purpose.** The studio's one candle struggles; the salon's
many candles are composed. It's the same light source behaving in opposite ways.

**How it arrives.** "Slowly revealed," as the script says. The comp reveals LIT through
DARK one candle at a time, and the gilt catches first. **How it leaves.** The candles snuff
out, and it returns to DARK. **REVISED 2026-09-24 after three takes (Homie): the snuff clip IS the exit.** It starts on
the lit plate, the left sconce goes out and then the right, a beat apart, the room settles into
dusk, and an incense-thin wisp trails from each wick. It continues the lit loop inside the same delivered file (2026-09-24: no playback fixes; `CLAUDE.md`), and Gérard is composited over it as over the loop.
The paragraph below records the first plan. **Added 2026-09-24 (Homie): smoke from the snuffed wicks.**
A short generated clip from the approved DARK plate (`S9-SAL-R-SNUFF`) with pale smoke
rising from the six wicks, thinning and gone. It's material, not a generated transition:
the comp times the snuff and cuts into the clip. Serves both exits (beat 3, and after beat 8).

**References.** `INSPO/Sc 9`: the white-and-gold oval salon (Hôtel de Soubise). For
hyper-real period Paris interiors, *Assassin's Creed Unity*.

---

## World 2 — GÉRICAULT'S STUDIO · LOCKED 2026-09-21

### Decisions (Homie, 2026-09-21)

| # | Choice | Decision | Why |
|---|---|---|---|
| 1 | The canvas | **The whole painting, scaled down.** The canvas is 3.2 × 4.7 m (the real one is 4.9 × 7.2 m), standing on blocks on CENTRE with plaster around it | At beat 9 Géricault and Sarah step back and look at it. They need the whole composition, including the figure waving at its apex. At true scale the wall would show only the bottom 3.6 m. **Liberty taken on purpose** |
| 2 | The window | **On RIGHT.** The studio lives on CENTRE and RIGHT in the beat map | The light source sits beside the painting. Light falls from right to left across the room |
| 3 | The morgue | **Studies only**: pencil and oil studies of limbs pinned around the window. There are no remains in any plate | The rotting head is a real prop in the actor's hands (beat 4). The plates set the obsession without competing with it. The audience is 13+ |

**2026-09-22 — light line changed.** The first room master came back blue-teal with near-black corners and no umber at all. `LOOK.md` asks for grey daylight and raw umber, and projector black is grey, so large near-black areas read as murky nothing on stage. Still one window, still directional from the right; now grey rather than cold blue, landing clearly on the back wall and canvas, and fading to warm umber shade toward the far corner.

**The painting is composited, never generated.** The CENTRE plate is a blank, flat, primed
canvas, square-on, so the comp can corner-pin the real *Raft* (public domain, 1819) onto it
in three stages: PAINT1 charcoal lines (beat 4), PAINT2 half painted (beat 6), PAINT3 almost
finished (beat 9).

### The walls (true scale apart from the canvas, 3.6 m crop)

**Where.** Géricault's studio in the Faubourg-du-Roule, Paris, 1818–19. A big, bare,
working room.

- **CENTRE**: the blank primed canvas, 3.2 × 4.7 m, bottom edge 0.2 m up on blocks, with
  bare plaster showing around it (at least 300 mm clear of each seam).
- **RIGHT**: a tall north window of small panes (sill 1.2 m, running out past the crop), a
  dark night sky and a thin moon beyond the glass. Studies of arms, legs and hands pinned
  around it, just visible. On the sill, a guttering candle in a tin holder beside a
  red-stained rag — **this candle is the room's only light source**, not an accent.
- **LEFT**: rough pine shelves at 1.4 and 2.2 m with plaster casts and the small scale model
  of the raft, and canvases leaning face to the wall below, nearly lost in the dark — the
  candlelight barely reaches this far.

**Motion for the loops.** Dust drifting in the candlelight on RIGHT. The candle gutters in a
draft, so the light dims and swells across the room (on all three walls, so it's done as a
light pass in the master comp, not generated per wall — same mechanism as the cloud it
replaces, 2026-09-22). That's all.

**AMENDED 2026-09-24 (Homie + Claude).** The "all three walls" reason for doing the light
only in the comp is gone, because the studio has one wall. Dust alone is 3–9 mm on the wall,
too small to read from the seats. So the candle's light is **split by speed**:
- **Generated (`S9-STU-L-LOOP`):** a small, fast, even shimmer of flame light over the
  canvas and the plaster relief, plus the dust. It stays constant, so the clip loops.
- **Comp:** the slow, cue-timed dim-and-swell, multiplied on top.

**The comp light follows the drama (Homie, 2026-09-24):**

| Beat | Line | Candle |
|---|---|---|
| 4 | the head, "I must have the likeness" | low and unsteady |
| 6 | "Vingt!… I will show it all!" | flares with his rage |
| 9 | "The injustice will be made visible for all to see" | steady and at its brightest as he and Sarah step back to look |

It fits "the artist makes the invisible visible" (below).

**The painting grows while he paints (Homie, 2026-09-24, pending the director).** The script
has Géricault painting as he talks. So instead of three jumps, the comp reveals the painting
slowly during each studio beat, arriving at PAINT1, PAINT2 and PAINT3 respectively. **This
depends on the director's blocking** (where he paints on the wall, and whether strokes appear
near his brush), so confirm with the director before building it.

**References.** Géricault's own studies (*Severed Limbs*, 1818). Rembrandt-style studio
light. *Layers of Fear*.

**Homie's 2022 concept** (`2022 Presentation…/Slide9.JPG`) was the starting point. It
put the window on CENTRE, a huge head study on LEFT, and the Raft dissolving into black
particles on RIGHT. The locked version keeps its fragment language (particle dissolve →
used for the bleach-out) and reorganises the walls around the beat map.

**How it arrives.** It paints itself in: charcoal lines first, then colour, through
brushstroke-shaped masks. The artist is the one who makes the invisible visible (Amina's
line: "l'invisible devient visible"). **How it leaves.** It bleaches back to raw
canvas, the edges breaking into particles (from the 2022 concept).

---

## World 3 — THE COURT MARTIAL · LOCKED 2026-09-21 (abstract)

**The idea** (Homie's): a solid black silhouette of the judge. **With every gavel strike
it gets bigger**, until the verdict fills the room.

**The figure (CORRECTED 2026-09-21: a naval officer, not a robed judge).** Chaumareys was
tried at Rochefort in 1817 by a **naval court martial** — a panel of naval officers in
uniform. The robe and toque of the first version were civil-magistrate dress and the wrong
institution entirely. See `LOG.md`, 2026-09-21 IMG.

**FRONTAL, not profile (Homie, 2026-09-21).** He faces the audience square-on, full length,
symmetrical, centred. The profile version read as Napoleon — bicorne plus tailcoat plus
sword plus side-on is that icon almost exactly, and `BIBLE.md` bans Napoleonic motifs
because this is the **Bourbon** state, not the Empire. Head-on breaks the quote. It also
suits symmetrical walls: a profile figure has a direction and pushes the eye off CENTRE
toward the next wall, where frontal puts the accusation on the audience, who sit exactly
where the public gallery sits. He reads his findings "like a town crier" — a crier faces
the crowd.

**Mass over costume.** The court is abstract by design, and costume specificity is what
caused the Napoleon collision. What carries the figure is **squared shoulders, fringed
epaulettes and the raised gavel**, not tailoring. High collar, a long coat falling straight,
planted stance. **No sword and no coat tails.** Gavel raised high in the right hand and held
clear of the head, an unrolled scroll out in the left.

**NO HAT (Homie, 2026-09-21). A bare, completely featureless head.** The bicorne was cut
after three versions of the same failure — top hat, then Napoleonic, then Napoleonic again
worn athwart. A wide two-cornered hat is the frontal Napoleon image and is welded to it;
that is an object prior, not a wording problem, and a fourth attempt at describing it would
have failed the same way. The bare head is also the **most suggestive** option and the
truest to the idea: the court is a faceless institution, so give it no face at all. The
epaulettes and squared shoulders carry the military read on their own.

**NO MOUTH. This was the real cause of the faces.** The spec said "no facial features" and
"mouth open mid-proclamation" in the same breath, and the model obeyed the second. In
profile that was consistent — an open mouth is a notch in the head's outline, which is why
this worked before. **Frontal, a mouth can only exist as interior detail**, and once the
model opens that door it adds eyes and a nose with it. The clause was correct under a
condition that stopped being true when the figure turned frontal. `SHOTCARDS.md` already
rules out lip sync and the Judge's voice is pre-recorded, so nothing needs his mouth: it
costs the design nothing to cut it.

**Ask for a cut-out, not a man.** The prompt's primary noun is now **a shape cut from black
paper**, not a person rendered in black. `house-rules` finding 5c: a defect that survives a
named instruction is usually what the model thinks the object *is*. A man has a face; a
paper cut-out does not.

**One unbroken mass of solid black. No white, no grey, no line anywhere inside the
outline** — v2 and v3 returned white collars, white buttons and fringed epaulette detail
across all variants, so these are banned by name in the prompt. Every feature is carried by
the silhouette's edge alone. **No eyes, no nose, no mouth, no hair, no hat.**

**ONE CARVE-OUT, ADDED 2026-09-23 (Homie): a white separation keyline where the gavel
crosses the body.** In `S9-CRT-STRIKE` the gavel drives toward camera and passes in front
of the figure, where black-on-black would erase it. The approved clip carries a clean white
cut-line around the gavel **only while it overlaps the figure** — it is absent in the
raised opening pose, where the gavel is already clear against open white. Keep that
conditional behaviour: the line exists to separate two black shapes, so it appears only
where two black shapes overlap.

**This does not loosen the rule above, and the distinction is the point.** The banned white
is *incidental rendered detail* — collars, buttons, fringe — which makes the shape read as
a man rather than as cut paper. A deliberate separation gap does the opposite: keyed onto
the bone-white field it reads as field showing through, the gavel lifting off the figure as
a separate piece of paper. That is the shadow-play language this world is built on.
**Nothing else gets a keyline.** If white appears anywhere other than between the gavel and
the body, it is the old defect and it is still banned.

**Full length is kept deliberately.** The growth only works if he starts whole: contained
at Q1, closing at Q2, outgrowing the frame at Q3, cropped tighter still at Q4, and gone at
Q5 with only the gavel left. Crop him early and Q3 has nowhere to go.

**The gavel is deliberate licence, not an error.** No French court has ever used one — a
president used a handbell or his voice. But the script writes "The gavel" (`BIBLE.md` beat
3), `BIBLE.md` makes the play's version canon, and all five cues are built on the strike.
Recorded here so it is not re-opened as a mistake.

**The field.** Bone-white, faintly lit from behind, like a lamp behind a scrim. That keeps
continuity with the 2022 dev showing's shadow play. The white reads as the verdict's paper
and the scroll.

**The growth — REVISED 2026-09-23, built from `BIBLE.md`'s actual beat structure, not
five isolated hits.** The script never gives the court five separate moments to appear —
it gives him **three appearances**, because Scene 9 is a four-way split and the studio
takes the CENTRE wall to black twice in between (beats 4 and 6). The growth rides on that
existing structure instead of inventing a new one:

| Appearance | Script beat | Moment(s) | Silhouette |
|---|---|---|---|
| **1** | Beat 3 | "Order! Order!" The gavel. Finding **One!** | small, about 1.2 m, CENTRE. One hard strike. |
| — | Beat 4 | Studio has the wall (the head, the hessian bag) | **CENTRE black** |
| **2** | Beat 5 | Gavel, Finding **Two!** ... Gavel, Finding **Three!**, a scuffle, "Get the TRAITORS out" — the judge loses control | reappears at **about 2.4 m** on "Two!", then **fills CENTRE, head cropped** on "Three!" — two hard jumps in the same continuous appearance, no black between them. The lack of a breath between the two is what sells "loses control" |
| — | Beat 6 | Studio has the wall again ("I will show it all!") | **CENTRE black** |
| **3** | Beat 7 | "An Act of God… CAN NOT be held responsible." | reappears biggest: a push-in crop on the same figure, chest and head filling CENTRE, gavel huge |
| **capper — INVENTED, not scripted** | after beat 7's line, before beat 8 (salon) | one more hard hit, no dialogue | **the gavel alone fills the whole wall**, coming down from CENTRE's top edge, then cut to black |

The capper is flagged because it isn't in the script — it's a visual beat added for impact
before the scene cuts to the salon's smug reply. Everything else above follows `BIBLE.md`
directly. Confirm the capper with Homie before it's treated as locked.

**CORRECTED 2026-09-23: one judge, not three.** `BIBLE.md` states plainly — "Only the
Judge is animated" — singular, and the script never mentions a panel. A prior session's
"tribunal of three" was never a decision Homie made: it was invented to solve the
whole-objects rule (below) for a version of Q4/Q5 that grew the figure past what CENTRE
could hold, then written into this file as if locked. It wasn't, and it's reverted. See
`LOG.md` 2026-09-23.

**Whole-objects rule (2026-09-21, Homie's direction) still holds, and is why the fix above
works without a workaround: the judge only ever occupies CENTRE, never spreading onto LEFT
or RIGHT, so he never approaches a seam to begin with.** "Bigger" past Q3 is achieved by
cropping tighter on the same figure (a push-in in the comp), not by making him wider than
one wall. LEFT and RIGHT can carry a light/colour flash at Q4–Q5 to sell the room-wide
impact — that's within the rule (only light and colour may cross a seam) — but that's a
comp suggestion, not locked; confirm with Homie before building it.

Each size is a **hard jump on the strike**, not a smooth grow. Every hit shakes the room.
A short shudder or flash on the field sells the impact.

**How it's made (decided 2026-09-21: a generated strike).**
1. **S9-CRT-FIG**: one still, black on bone-white, 9:16, gavel raised.
2. **S9-CRT-STRIKE**: image-to-video from that still. Locked camera, one strike. **CHANGED
   2026-09-23 (Homie): the strike comes TOWARD CAMERA, not downward.** The gavel drives
   forward out of the frame at the viewer, growing as it comes, and holds huge and close.
   A downward swing was tried twice and fails structurally, not for want of wording: a
   gavel strike is a movement in depth onto a bench, and this design has neither bench nor
   depth, so "down" can only mean down across the body — where a second black shape on a
   one-tone silhouette stops existing. Toward camera is the only direction that reads, and
   it puts the blow on the audience, which is what the frontal decision was already for.
   See `LOG.md` 2026-09-23 for both failures.
3. **In the comp:** threshold the clip to pure black and white (it kills edge boil), then
   **key the figure out and place it on a bone-white field built natively at CENTRE's 5:3.**
   The generated 9:16 frame is never shown; only the keyed figure is. Scale, place and
   retime once per cue. The white field and the impact shudder are made in the comp too.
   **Placement rule (measured 2026-09-24): at every cue where his legs are in frame (Q1–Q3),
   the generated frame's bottom edge sits exactly on the wall's bottom edge** — the stage
   floor (`STAGE.md`). From the lunge onward (frames 47–96) his front leg runs off the bottom
   of the generated frame, and this is what makes that cut invisible: the leg meets the
   floor. Placed anywhere higher, it reads as a leg sliced flat in mid-air.
4. **Q5's enlargement is REDUCED, not removed — corrected 2026-09-24.** On 2026-09-23 this
   step claimed the toward-camera change meant "no blow-up." Measured on the approved clip,
   that was wrong: for the gavel to fill CENTRE it still needs **3.2× at working resolution
   and 6.4× at 4K.** What *did* change is real: the gavel reaches the lens at several times
   the size it has in the raised pose, so the enlargement is a fraction of what it was, and
   **Q5 no longer needs a separate generation** — it is the same clip, further along its
   travel. And because the plate is thresholded to two tones, enlarge it smoothly *then*
   threshold, which yields clean curves at any size; that survives far better than
   continuous-tone video would. **The vector trace stays as the fallback** if the curves
   still step at 4K.

**How it arrives.** It slams in on the strike: a hard cut, no transition. Authority
doesn't fade in.

---

## Fragments — how the worlds share the walls

**The three physical walls are the fragments.** The salon can hold LEFT while the studio
assembles on RIGHT and CENTRE drops to black: three realities side by side. It's the most
legible version, and the cheapest one to build in a week. Breaking single walls into
shards is a refinement for later, if there's time.

Video-game references for the language:

- ***The Medium*** (2021): two realities on screen at once, side by side. That's the
  salon/studio split.
- ***Layers of Fear***: a painter's house that re-forms when you look away. Paintings run
  and rooms redraw themselves.
- ***Control*** (2019): architecture that slides, folds and reassembles panel by panel.
- ***Alan Wake 2***: scenes being rewritten over the top of reality. Here the court is
  rewriting history.
- ***What Remains of Edith Finch***: each story in one house told in its own visual style.

**Rule: each world arrives the way it thinks.** The salon shows off (candles, gilt). The
studio makes things visible (paint). The court imposes (a cut, a strike).

---

## Plate recipe (all walls)

- Model (per `house-rules` → `model-routing.md`): **Soul Cinema** for room masters and wall
  plates (locations), and **Nano Banana Pro** for edits of an existing frame (the DARK
  states, fixes). Confirm the aspect ratios each one offers on the first generation and log
  them in `PIPELINE.md`.
- **The camera anchor leads every plate prompt, then the style prefix, then the room contents**
  (changed 2026-09-22, Homie). This is Cully's LIRA Soul Cinema location template: the camera
  anchor is "the hardest part; anchor it hard." The earlier rule (prefix first) cited
  `house-rules` finding 15, which is about a stylised register fighting photoreal text; SOTR's
  prefix is itself photographic, so that condition never applied. Salon prompts reordered;
  studio prompts follow the same order when the studio is prepped.
- Room master first, then CENTRE, LEFT, RIGHT, per `PIPELINE.md`.
- Every prompt carries: the world's style prefix, the era line, "camera square to the wall,
  eye level 1.6 m, locked, no floor visible, wall from floor to 3.6 m," and the true-scale
  anchors (door height, dado height).
- **No people in any plate.** The actors are real.

## Style prefixes

Pasted word for word at the head of every prompt for that world.

### SALON · LOCKED 2026-09-21 (tightened the same day to fit the cap; chandelier removed 2026-09-22)

```
Hyper-real photograph of a grand Parisian salon in 1817: a 1730s Rococo room kept immaculate
by a royalist household. Carved boiserie painted ivory and cream, every moulding and
rocaille scroll picked out in bright burnished gold leaf, crimson silk curtains. Evening,
lit only by beeswax candles in gilt sconces and candelabra: warm amber light, soft
and even, the gilt glowing wherever the flames catch it, cool blue-grey dusk at the curtain
edges. Palette 60% ivory and cream, 30% burnished gold, 10% crimson silk. Hand-carved wood,
real gold leaf, old grey-silvered mirror glass, heavy silk with a deep sheen. Everything of
its period, before 1819. The room is empty and still.
```

### STUDIO · LOCKED 2026-09-21 (light line changed 2026-09-22)

```
Hyper-real photograph of a painter's working studio in Paris in 1818: a large bare rented
room, used hard, seen at two in the morning. Through the tall window on the right, a dark night sky and a thin moon; the room's only light is a single candle burning on the sill beside it, its warm glow falling hard across the canvas and dying into raw umber shadow toward the far left corner, the rest of the room barely visible. Palette 60% deep umber shadow and raw plaster, 30% warm candlelight on the canvas and sill, 10% dried-blood red on a rag and on the palette. Real surfaces: flaking lime plaster, charcoal smudges, oil paint crusted on wood, turpentine stains, dust on every ledge, scuffed pine. Everything of its period, before 1819. The room is empty and still.
```

### COURT · LOCKED 2026-09-21

```
Flat graphic image: one solid pure black silhouette on a bone-white field, like a shadow
cast on a lit paper screen. The black is flat and absolute with crisp clean edges. The white
is a warm bone tone, softly brighter at the centre, as if a lamp glows behind the paper. Two
tones only.
```

**Prompt length.** `house-rules` caps a prompt at about 1,500 to 2,000 characters. Prefix, camera
and room contents together land at about 1,900. Any new element has to replace words, not add
them.
