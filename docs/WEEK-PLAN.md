# WEEK PLAN — Scene 9, 22 to 28 September 2026

Set 2026-09-22. Every session follows this; update it on wrap.

## Division of labour

- **Claude:** every technical call from the sources (Joey, Cully/LIRA, Higgsfield, LGEL),
  every prompt file, full-resolution review of every saved result, the register and log.
- **Homie:** generation in Higgsfield, saving picks to `SOTR_MEDIA`, the look calls,
  director sign-offs, the master comp in After Effects, the Topaz upscale.

## Budget rules (from LGEL)

- **One batch of 4 per attempt.** Expect one keeper in four. Pick the best and move.
- **Three batches on a plate without a keeper = change the route, not the words.**
- **A defect the comp can fix in minutes is fixed in the comp**, never regenerated.

## Scope, trimmed to what LOOK.md actually animates

Loops: **4, not 6** — S9-SAL-C, S9-SAL-L, S9-SAL-R (candle flames, glints, curtains) and
S9-STU-R (dust in the window light, the candle stub). `LOOK.md` gives the studio's CENTRE
and LEFT no motion of their own: CENTRE is the canvas the painting is composited onto, and
the cloud is a light pass in the comp across all three walls. They ship as stills.

## Days

| Day | Mode | Work | Who |
|---|---|---|---|
| **Mon 22** | IMG | S9-SAL-ROOM and S9-STU-ROOM (independent, run both). Claude writes the six NBP wall prompts against the approved masters. **Both masters to the director for design sign-off** | Homie generates · Claude reviews |
| **Tue 23** | IMG | Salon C → L → R, seam check. Studio C → L → R, seam check | both |
| **Wed 24** | IMG | Fixes. Salon DARK × 3 (NBP edits; fallback: grade LIT down in the comp). All plates approved | both |
| **Thu 25** | VID | New session. S9-CRT-STRIKE + 4 loops, loop method per plate | both |
| **Fri 26** | VID + comp | Loop retries. Comp starts: Gérard portrait, Raft PAINT1–3, court Q1–Q5. **Beat-by-wall map signed off by the director by today** — it drives the comp | Homie comp · Claude cue sheet |
| **Sat 27** | comp | Transitions, light passes, cue timecodes for sound. Topaz 4K upscale of approved material | Homie |
| **Sun 28** | — | Delivery to the mapping software. Buffer | Homie |

## Dependencies outside this repo

- Director: room-master sign-off (Mon/Tue), beat-by-wall map (by Fri).
- Gérard's *Louis XVIII in Coronation Robes* and Géricault's *Raft*: public-domain source
  images at the highest resolution available, before Fri.
- **Delivery spec from whoever runs the projection, before Sat:** codec (ProRes vs HAP), and the
  file container — one wide 9360 x 2160 file or three slices, and whether they want 16:9 files.
  A 16:9 container is an export setting (wall at its true shape inside, the rest black); it never
  changes generation. Walls are generated at their own shape: L/R 4:3, C 16:9 trimmed to 5:3
  (Homie asked 2026-09-22; generating at 16:9 would squash the 4:3 flats or waste a quarter of
  every frame).
