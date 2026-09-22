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
| **Studio** | one cold north window, hard fall-off into dark | **patina**: dust, stains, raw plaster, chaos | grey daylight, raw umber, bone | dried-blood red (a rag, the palette) | one stub of warm candle |
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

**How it arrives.** "Slowly revealed," as the script says. The comp reveals LIT through
DARK one candle at a time, and the gilt catches first. **How it leaves.** The candles snuff
out, and it returns to DARK.

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
- **RIGHT**: a tall north window of small panes (sill 1.2 m, running out past the crop), grey
  sky. Studies of arms, legs and hands pinned around it. On the sill, a guttering candle
  stub beside a red-stained rag, which is the warm note and the red.
- **LEFT**: rough pine shelves at 1.4 and 2.2 m with plaster casts and the small scale model
  of the raft, and canvases leaning face to the wall below. It's lit square-on by the
  window opposite.

**Motion for the loops.** Dust drifting in the window light on RIGHT. Cloud passing, so the
daylight dims and returns (on all three walls, so it's done as a light pass in the master
comp, not generated per wall). The guttering candle stub. That's all.

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

**Full length is kept deliberately.** The growth only works if he starts whole: contained
at Q1, closing at Q2, outgrowing the frame at Q3, multiplying at Q4, and gone at Q5 with
only the gavel left. Crop him early and Q3 has nowhere to go.

**The gavel is deliberate licence, not an error.** No French court has ever used one — a
president used a handbell or his voice. But the script writes "The gavel" (`BIBLE.md` beat
3), `BIBLE.md` makes the play's version canon, and all five cues are built on the strike.
Recorded here so it is not re-opened as a mistake.

**The field.** Bone-white, faintly lit from behind, like a lamp behind a scrim. That keeps
continuity with the 2022 dev showing's shadow play. The white reads as the verdict's paper
and the scroll.

**The growth.**

| Strike | Script moment | Silhouette size |
|---|---|---|
| 1 | Opening "Order!" and finding One | small, about 1.2 m tall, CENTRE only |
| 2 | Finding Two | about 2.4 m, CENTRE |
| 3 | Finding Three, "Get the TRAITORS out" | fills CENTRE, head cropped |
| 4 | The judge loses control | **the tribunal of three:** two more judges appear, each whole on LEFT and RIGHT. All three face the audience and strike together |
| 5 | "…CAN NOT be held responsible." | **each wall fills with its own gavel**, huge, coming down from that wall's top edge. All three strike at once, then cut to black |

**Whole-objects rule (2026-09-21).** No judge and no gavel is ever split across a seam. The
court is overwhelming because three whole judges strike in unison, not because one breaks
the frame. It's also closer to history: a court martial sat as a panel. One figure makes
all three, used as generated on every wall — **the figure is frontal, so no mirroring is
needed.** Three identical judges staring straight out is closer to a real court martial
panel facing the accused than the earlier inward-facing arrangement.

Each size is a **hard jump on the strike**, not a smooth grow. Every hit shakes the room.
A short shudder or flash on the field sells the impact.

**How it's made (decided 2026-09-21: a generated strike).**
1. **S9-CRT-FIG**: one still, black on bone-white, 9:16, gavel raised.
2. **S9-CRT-STRIKE**: image-to-video from that still. Locked camera, one strike: the gavel
   comes down hard, then holds. The prompt gets written in a **VID** session, not here.
3. **In the comp:** threshold the clip to pure black and white (it kills edge boil), then
   scale, place and retime it once per cue. The white field and the impact shudder are made
   in the comp too.
4. **The one risk is Q5.** A gavel filling a whole wall is an enlargement of about
   5–10×, and 1080p video will soften at that size. Upscale the strike to 4K first. If it's
   still soft, Q5 alone uses a vector trace of the still, rotated by keyframes.

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
room, used hard. Grey north daylight from one high window on the right falls across the room onto the canvas and fades into warm raw umber shade toward the far left corner. Palette 60% cool grey daylight and raw
plaster, 30% raw umber and deep shadow, 10% dried-blood red on a rag and on the palette.
Real surfaces: flaking lime plaster, charcoal smudges, oil paint crusted on wood, turpentine
stains, dust on every ledge, scuffed pine. One stub of candle is the only warm note.
Everything of its period, before 1819. The room is empty and still.
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
