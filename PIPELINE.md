# PIPELINE — how one world gets made

Every world (Salon, Studio, Court, and any added later) goes through the same steps, in
order. A step doesn't start until the one before it is approved.

```
 0 FPS         60 fps delivery. Generate native, interpolate loops before the comp (7b)
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

## 6 · Seam check

Lay the three plates side by side in the wide comp at true proportion (4 : 5 : 4 widths).
The cornice line, dado line, wall finish and light temperature have to carry across both
seams. **Nothing is approved until this passes.**

## 7 · Loops

Each wall is animated as its own clip in Higgsfield, from its approved plate, with a
locked camera. **Ambient motion only:** candle flame, glints, dust, a curtain breathing.
These don't need to sync across walls, because nobody can tell two candles are out of
phase.

Every loop has to cycle cleanly, since QLab may hold it for minutes. Test first frame =
last frame where the model allows it; otherwise use a crossfade loop in the comp. Record
which method worked for each plate in `REGISTER.md`.

### 7b · Frame rate: generate at native, interpolate to 60

**Delivery target is 60 fps.** Generate at whatever the model outputs natively. Seedance in
Cinema Studio only outputs 24 fps (confirmed on *First Day on the Job*). For any other model,
check and log its fps on the first generation. Then interpolate each approved loop to 60
**before it goes into the comp**:

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

## 8 · Master comp — where "one entity" happens

**One wide canvas, 4680 × 1080 at 1080p (1440 + 1800 + 1440). The three walls sit side by
side at true proportion, on a single timeline.**

Everything that has to read as one event across three screens is made here, not in
Higgsfield:

- light changing across the whole room (dusk falling, a cloud crossing the studio)
- fragment transitions (salon candles lighting in, studio painting itself in)
- the court's silhouette growing across the walls
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
