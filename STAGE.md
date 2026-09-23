# STAGE — the set, and what every render has to fit

Source: `SOTR_RMIT26_Plan_DRAFT_v0.2.pdf` (12.09.26, marked draft, "reference only").
The numbers below come from that drawing. The shape is confirmed; the exact dimensions may
still move. **If the drawing changes, update this file before any plate is built.**

## The three surfaces

RMIT Black Box, 14000 × 6010 mm floor. Three projection surfaces form an open book facing
the audience:

```
                        BACK WALL
   ┌──────────────────────────────────────────────────────┐
   │              ┌──────── CENTRE ────────┐              │
   │         830 ─┤      6000 wide          ├─ 830       │
   │             ╱                            ╲            │
   │   LEFT     ╱ 4800                  4800 ╲   RIGHT     │
   │   flat    ╱  25° off square      25° off ╲  flat      │
   │          ╱                                ╲           │
   │         ╱____________ 10057 ______________╲          │
   └──────────────────────────────────────────────────────┘
                        AUDIENCE
```

| Surface | Size (W × H) | Aspect | Notes |
|---|---|---|---|
| **LEFT** flat | 4800 × 3600 mm | **4:3** | Free-standing, splayed 25° outward. Upstage edge sits 830 mm in front of the back wall. |
| **CENTRE** | 6000 × 3600 mm | **5:3** | The back wall between the two flats. Height assumed 3600 to match the flats; **unconfirmed**. |
| **RIGHT** flat | 4800 × 3600 mm | **4:3** | Mirror of LEFT. |
| All three, unfolded | 15600 × 3600 mm | 4.33:1 | Only useful for planning. Never generated as one image (see below). |

Each flat meets the back wall at **115°** (90° + 25°). The flats **don't touch** the back
wall: there is an 830 mm gap at each upstage corner, so from most seats each seam is also a
jump in depth.

## Render approach: walls as walls

**Each surface shows the matching wall of the room, square-on and at true scale.** The
physical set supplies the room's depth. We don't paint a perspective view into it.

- **LEFT** = the room's left wall, **CENTRE** = its back wall, **RIGHT** = its right wall.
- Camera square to the wall, eye level about 1.6 m, lens around 40–50° (near-elevation, low
  distortion). Converging perspective lines on a flat that is already angled would read as
  a double perspective.
- **True scale. The image's bottom edge is the stage floor.** A door is about 2.4 m, a dado
  rail about 0.9 m, a chair seat about 0.45 m. An actor who walks up to the wall has to
  stand at the right height against it.
- **No floor in the image**, or at most a thin skirting line. The real floor is the floor.
- **The frame's top edge is 3.6 m up the wall.** Taller rooms (the salon ceiling is 5 m+)
  are cropped there. Ceiling detail, like the chandelier, only appears if it hangs below
  3.6 m.
- **Seams fall on room corners.** The left edge of CENTRE and the right edge of LEFT are the
  same corner of the room. Keep hard detail (a picture frame, a window) about 300 mm clear
  of every seam edge.
- **Every object lives whole on one wall (Homie, 2026-09-21).** No table, painting, figure
  or piece of furniture is split between two surfaces. Each wall is its own complete
  composition, so it can be rendered, looped, swapped or blacked out on its own without
  leaving half an object behind. The three still read as a single image because they
  share the architecture (the lines that carry across the corners), the light and the
  palette, not because objects run across the seams. The physical set enforces the same
  thing: each seam is a 25° fold with an 830 mm depth jump.
  - **May cross a seam:** continuous architecture (dado, panel line, skirting), light,
    colour, grade, done as comp passes.
  - **Never crosses a seam:** any object, any figure, any motion.

**Why not one wide panorama sliced into three.** A single panoramic view only reads
correctly from the centre seats. The 830 mm gaps and the 25° flats would also need a full
projection-mapping warp. The walls-as-walls approach reads from every seat, and the seams
land where a room already has corners. The trade-off is less depth illusion. Rethink this
only if a scene needs a view out into distance (sea, horizon), which none of the three
current worlds do.

## Cohesion across the three walls

**Amended 2026-09-22.** The client confirmed each world holds exactly one physical wall for
its whole run — salon on RIGHT, studio on LEFT, the court's default on CENTRE — so most
worlds only ever build one wall, not three. The steps below still govern: step 1 always
happens (the room master is the design sign-off and the light/materials reference
regardless of how many walls get built from it); steps 2–4 only apply to a world that
genuinely shows more than one wall at once. **CORRECTED 2026-09-23: no world currently does
this.** The court's climax (Q4→Q5) was written as spreading across all three walls, but
that was never a real decision — `BIBLE.md` specifies one judge, and it stays on CENTRE
throughout. See `LOOK.md` World 3 and `LOG.md` 2026-09-23.

1. Build the **room master** first: one wide design image showing all three of the room's
   own walls at once. It's the ground truth and is never projected.
2. Build the world's **one confirmed wall** from it (or, for a world that genuinely shares
   the stage across walls, **CENTRE** first, then LEFT/RIGHT from the master plus the
   approved CENTRE — same cornice line, dado height, wall finish and light source).
3. Where two walls of the *same* world are live together, check the joins by laying them
   side by side at true proportion before either is approved. The cornice and dado lines
   have to meet across the seam. Skip this where a world holds only one wall — there is no
   neighbour to match.

Step by step in `PIPELINE.md`.

## Cameras and motion

- **Every camera is locked off. No push, no pan, no drift, ever.** The room must not move
  behind a live actor.
- Motion only happens **inside** the image: candle flame, glints on crystal, dust in window
  light, light slowly changing, a curtain breathing.
- **Keep motion away from the seams.** Each wall is animated as its own clip, so anything
  moving across a seam would tear.
- Each plate becomes a **seamless loop** that QLab holds for as long as the scene needs.
  The method (first frame = last frame, crossfade loop, or a still with a light overlay) is
  decided per plate. See `SHOTCARDS.md`.

## Fragments and transitions: built in compositing, not generated

The worlds cut in and out as fragments. The studio assembles on one wall while the salon
dissolves on another. **The transitions are built in the edit/compositing stage (After
Effects or the media server), from the clean plates. Higgsfield never generates them.**
Generated transitions can't be timed to a cue and can't be repeated exactly. Masks over
clean plates can.

Higgsfield's job is clean, fully lit, loopable wall plates. The fragmenting is design work
done on top. The visual language for it is in `LOOK.md`.

## Resolution and delivery (decided 2026-09-21)

- **Work at 1080p. Upscale approved results to 4K. Nothing gets upscaled until it's
  approved.**
- There's no fixed projector spec. **Projection-mapping software stretches, squashes and
  fits the final images** to the real surfaces, so exact pixel ratios don't matter. The
  content has to sit inside 4:3 / 5:3 safe areas.
- Master canvas: **4680 × 1080** (1440 + 1800 + 1440, the 4:5:4 proportion of the walls).
  At 4K that's **9360 × 2160**. Full workflow in `PIPELINE.md`.

## Still open

- [ ] **Floor projection: parked, not ruled out (Homie, 2026-09-21).** It's out of the
      current build. The 2022 concept had a projected carpet, so it may come back once the
      walls are done. If it does, it's a fourth surface with its own camera (top-down), the
      same whole-objects rule applies at the wall–floor edge, and light will spill onto the
      actors. For now, plates show no floor.

- [ ] Final set dimensions. The drawing is a v0.2 draft; the proportions above follow it.
- [x] Frame rate: **the model's native rate.** 24 is fine; take a higher rate when a model
      offers it. No forced interpolation. It's held open as an option (`PIPELINE.md` → 7b).
- [x] VFX in post: optional upgrades for small elements. Generation comes first
      (`PIPELINE.md` → 7c).
- [ ] Codec/container for the mapping software (e.g. ProRes vs HAP). Decide at first
      delivery.
