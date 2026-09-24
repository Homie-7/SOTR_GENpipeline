# PIPELINE — how one world gets made

Every world (Salon, Studio, Court, and any added later) goes through the same steps, in
order. A step doesn't start until the one before it is approved.

```
 0 FPS         native rate (24 is fine), higher when a model offers it. No forced
               interpolation (7b). Small VFX additions in post stay optional (7c)
 1 CARD        write the cue card (SHOTCARDS.md)
 2 ROOM        one wide design image of the whole room          ← the ground truth
 3 FRONT       CENTRE wall, square-on       ┐
 4 LEFT        LEFT wall, square-on         ├ three cameras in one room
 5 RIGHT       RIGHT wall, square-on        ┘
 6 SEAM CHECK  all three side by side at 4:5:4 in the wide comp
 7 LOOPS       animate each wall on its own (ambient motion only)
 8 MASTER COMP one wide canvas: loops + everything room-wide
 9 APPROVE     at 1080p
10 UPSCALE     to 4K, then deliver to the projection-mapping software
```

## 1 · Card

Written in `SHOTCARDS.md` before any prompt. It lists what's on each wall, the light, what
moves, and how the world arrives and leaves.

## 2 · Room master — the step before the front camera

**One wide image of the whole room, seen from the audience's position, with all three
walls in view at once.** It's how the 2022 presentation renders show the set. No people.

Why this step comes first:

- **It's the design sign-off.** The director sees how the whole set reads before three
  walls get built.
- **It's the ground truth for the three cameras.** Materials, light direction, what sits
  on which wall, where the corners fall. LEFT, CENTRE and RIGHT are all derived from it,
  so they're one room by construction. On *First Day on the Job*, the room drifted every
  time a shot was built without the approved room plate as its reference. This step
  exists because of that.
- It's cheap: one image, and iterations cost minutes, not a wall rebuild.

It's never projected. It's a reference, not a deliverable.

## 3–5 · The three cameras

One room, three locked cameras, each square-on to its own wall (`STAGE.md` → "Render
approach"). **Order: FRONT (CENTRE), then LEFT, then RIGHT.**

- **FRONT** carries the room master as its reference.
- **LEFT** and **RIGHT** carry the room master and the approved FRONT: the room for
  content, the front wall for surface and light.
- The room's contents are written **once** in the card and quoted word for word in all
  three prompts. The prompts differ in only one paragraph: which wall the camera faces.
  That's the clone rule from the last production.

**Aspect ratios.** The walls are 4:3 (sides) and 5:3 (centre). The projection-mapping
software stretches and fits in the end, so exact ratios don't matter at generation. **The
content does.** Keep everything important inside a 4:3 or 5:3 safe area, whatever aspect
the model offers. Check which aspects each Higgsfield model supports before the first
generation, and log it here.

| Model | Aspect options offered | Setting used | Output size | Logged |
|---|---|---|---|---|
| Nano Banana Pro | *not yet captured* | 9:16, 2k | **1536 x 2752** | 2026-09-22, from S9-CRT-FIG |
| Soul Cinema | **21:9 available** (native), 1:1, 4:3, 3:4, 16:9, 9:16, 3:2, 2:3 — per LIRA; 21:9 native per Higgsfield | 21:9, 2k for room masters | 1.5k / 2k tiers; batch up to 4 | 2026-09-22, from sources, not a test |
| **Seedance 2.5** (video, image-to-video) | **21:9, 16:9, 4:3, 1:1, 3:4, 9:16** (captured 2026-09-24). Modes: References · Sequel · Prequel · Edit video, **no end-frame slot**. Also: batch 1–4, quality (High seen), sound on/off, an "Unlimited" toggle (not available on Homie's plan, 2026-09-24). Cost: **48 credits for 4 s at 1080p** (64 before a discount) | 9:16 | **1080 x 1920 · 24 fps · 4.04 s (97 frames)** · HEVC Main 10, `yuv420p10le`, ~5.4 Mb/s, AAC 32 kHz stereo | 2026-09-23, measured off `S9-CRT-STRIKE` v3, the project's first video generation |

**Seedance 2.5 notes, from the first run (2026-09-23).**
- **10-bit out of the box** (`yuv420p10le`), which is better than the 8-bit assumed. Worth
  keeping through the comp rather than flattening on import.
- **24 fps native**, so the whole master comp is 24 (`PIPELINE.md` 7b). No interpolation.
- **4:2:0 chroma** is a non-issue here: the court plate is effectively monochrome, the
  detail is carried in luma, and the comp thresholds it anyway.
- **Audio comes back populated, and that is deliberate (Homie, 2026-09-23):** he leaves
  generation audio ON so the sound designer has a scratch reference of the model's own
  timing. It is never used in the comp. Don't "fix" this by switching audio off.

**Soul Cinema cannot take a reference AND a prompt.** Higgsfield's help centre: *"When a reference image is attached, the prompt field becomes unavailable."* LIRA: one reference image. So steps 3–5 as written (each wall built on Soul Cinema from the room master, L/R with two references) **cannot be executed.** The room master is unaffected: it has no reference.

**WALL ROUTE — DECIDED 2026-09-22: Nano Banana Pro, reference-led.** NBP takes a prompt *with* references (up to 14), offers 4:3 and 16:9, and renders to 4K. LIRA sends location view changes to NBP with the new arrangement spelled out, and every approved LGEL plate was built on NBP with two references. GPT Image 2 was rejected: LIRA calls it "very dirty across the frame as a whole", which is the worst trait for a full projected wall, and it costs more. The video-walkthrough route (Cully) was rejected for this week: it is VID work, and LGEL found screenshots of a moving camera soft on every frame.
- **CENTRE**: NBP, 16:9, ref = approved room master. **LEFT / RIGHT**: NBP, 4:3, refs = room master + approved CENTRE.
- Each prompt states what every reference carries and what it does not (`house-rules` finding 3), describes only this wall's contents and camera (finding 1: prose re-describing the room overrides the reference), and spells out which wall and where the corners fall (LIRA).

**REFINED 2026-09-22, CONFIRMED same day: a wall references an approved sibling wall only if that sibling is ever live on stage beside it, not by default.** The original assumption was every world always shows all three walls together; the client's confirmed mapping has salon and studio each holding exactly one wall for their whole run (salon RIGHT, studio LEFT), so neither `S9-SAL-R` nor `S9-STU-L` has a sibling to seam-match — each references only its own room master. **CORRECTED 2026-09-23:** the court's climax (Q4→Q5) does not spread across all three walls either — the judge stays on CENTRE only throughout, per `LOOK.md` World 3 and `LOG.md` 2026-09-23 (a prior "tribunal of three" across all three walls was never a real decision). So no world in this production currently has two walls genuinely live together, and this rule has no live case yet.

## 6 · Seam check

Lay the three plates side by side in the wide comp at true proportion (4 : 5 : 4 widths).
The cornice line, dado line, wall finish and light temperature have to carry across both
seams. **And no object touches a seam.** Every object sits whole on its own wall, 300 mm
clear of the edge (`STAGE.md`). Test each wall alone as well: black out the other two,
and the wall should still read as a complete picture. **Nothing is approved until this
passes.**

## 7 · Loops

Each wall is animated as its own clip in Higgsfield, from its approved plate, with a
locked camera. **Ambient motion only:** candle flame, glints, dust, a curtain breathing.
These don't need to sync across walls, because nobody can tell two candles are out of
phase.

Every loop has to cycle cleanly, since QLab may hold it for minutes. Test first frame =
last frame where the model allows it; otherwise use a crossfade loop in the comp. Record
which method worked for each plate in `REGISTER.md`.

### 7b · Frame rate: native is fine, higher when it's free

**Decided 2026-09-21 (Homie): no forced interpolation.** If a model outputs 24 fps, we work
at 24. When choosing between models of similar quality, **prefer the one with the higher
native frame rate**. Seedance in Cinema Studio outputs 24 fps only (confirmed on *First Day
on the Job*). For any other model, check and log its fps on the first generation.

The whole master comp runs at one frame rate. If every loop is 24, the comp is 24.

**Interpolation to 60 is an option held open, not a step in the pipeline.** Use it only if
a specific loop clearly benefits and passes the checks below. If we do use it, the notes
below apply:

- **Why before the comp:** everything made in the comp (fades, fragment transitions, the
  court's scale jumps, light changes) then renders natively at 60 fps, with no
  interpolation artifacts. Only the generated footage gets interpolated.
- **Why at 1080p:** interpolating before the 4K upscale is about 4× cheaper, and it means
  the approved footage is what gets interpolated.
- **Why this material suits it:** locked cameras with small motion (dust, glints, slow
  light) are the easiest case for interpolation. **The one to watch is candle flame.**
  Fast, shape-changing motion can smear or warp. Check flames frame by frame on the first
  test. If they warble, keep the flame layer at native fps, or source flames as a separate
  composited element.
- **Interpolate across the loop point.** Append the clip's first frames to its end before
  interpolating, then trim. Otherwise the loop seam doesn't get in-between frames and
  hitches once per cycle.
- **24 → 60 is a 2.5× step**, not a clean doubling, so every output frame is synthesised.
  That's fine for AI interpolators, but it rules out simple frame blending.

**Tools, in order of preference:**

1. **Topaz Video AI** (Chronos / Apollo models). The best quality, and it also does the
   4K upscale in step 10, so one tool covers both.
2. **DaVinci Resolve**: Optical Flow retiming (free version), or Speed Warp (Studio).
   A good fallback that's already on most edit machines.
3. **RIFE** (open source, e.g. via Flowframes on Windows). Free and fast; quality is close
   to Topaz on low-motion shots like ours.

Don't use ffmpeg's `minterpolate` for finals. It tears on flame and fine detail.

**Test before committing:** run one salon loop through the chosen tool, check the flames
and the loop point, and log the result here. Then apply the same settings to every loop.

### 7c · VFX in post: an option, not the default

**Generation comes first. Get as much of the result as possible out of Higgsfield.**

Anything that's easy to add or fix in post (a flame element, drifting dust, a light
flicker or wash, a lens bloom on gilt) is available as an upgrade in the comp. Reach for
it when a generated loop is nearly right but missing one small thing, or when a generated
element can't be made to behave (flames that warble, dust that pops). Don't use it to
replace work that generation could have done.

Log every post addition against its plate in `REGISTER.md`, so the loop can be rebuilt if
the plate changes.

## 8 · Master comp — where "one entity" happens

**One wide canvas, 4680 × 1080 at 1080p (1440 + 1800 + 1440). The three walls sit side by
side at true proportion, on a single timeline.**

Everything that has to read as one event across three screens is made here, not in
Higgsfield:

- light changing across the whole room (dusk falling, a cloud crossing the studio)
- fragment transitions (salon candles lighting in, studio painting itself in)
- the court's strikes, one judge growing then cropped tighter, CENTRE only (optional light flash on LEFT/RIGHT at the climax — see `LOOK.md` World 3)
- the Raft painting's three stages on the studio canvas

Because it's one timeline, the three screens are in sync by construction. Generated clips
can't guarantee that, because each is its own render. **Split of labour: Higgsfield makes
the materials, the comp makes the moment.**

Delivery is either the one wide file or three synced slices from the same timeline,
whichever the mapping software prefers.

## 9–10 · Approve, upscale, deliver

Approve everything at 1080p. Upscale only the approved results, to 4K (wide canvas 9360 ×
2160). Don't upscale anything that isn't approved, because the upscale is the expensive
step. The mapping software handles the final stretch, keystone and blend across the real
surfaces.

## Sound

A separate sound designer works on top of the finished animation. **Our timing leads:**
the court's size jumps are timed to the drama, and the sound follows. Hand over the
master comp with the timecode of every key moment (each strike, each transition) marked,
so the sound can land on them.
