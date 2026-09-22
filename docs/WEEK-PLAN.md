# WEEK PLAN — Scene 9, 22 to 28 September 2026

Set 2026-09-22, revised 2026-09-22 (wall mapping confirmed — see below). Every session
follows this; update it on wrap.

## Division of labour

- **Claude:** every technical call from the sources (Joey, Cully/LIRA, Higgsfield, LGEL),
  every prompt file, full-resolution review of every saved result, the register and log.
- **Homie:** generation in Higgsfield, saving picks to `SOTR_MEDIA`, the look calls,
  director sign-offs, the master comp in After Effects, the Topaz upscale.

## Budget rules (from LGEL)

- **One batch of 4 per attempt.** Expect one keeper in four. Pick the best and move.
- **Three batches on a plate without a keeper = change the route, not the words.**
- **A defect the comp can fix in minutes is fixed in the comp**, never regenerated.

## Scope — CONFIRMED 2026-09-22, cut from 6 wall plates to 2

The client confirmed (audience-perspective) the salon plays on RIGHT, the studio on LEFT,
the judge on CENTRE ("the back screen"), and the raft is a physical floor riser — out of
scope. Combined with `LOOK.md`'s existing "solo wall" design for the salon, **each world
holds exactly one wall for its whole run**, the court's own climax excepted (Q4→Q5, all
three at once — already designed, not a new exception). Full reasoning in `LOG.md`
2026-09-22.

That means the build is now: **2 room masters** (design reference only, never projected),
**2 wall plates** (`S9-SAL-R`, `S9-STU-L`), **2 loops**, **1 DARK edit**, plus the court
figure and strike already in progress. Down from up to 6 wall plates, 6 loops, 3 DARK
edits — roughly a day and 1,500–2,000 credits recovered.

## Days

| Day | Mode | Work | Who |
|---|---|---|---|
| **Mon 22** | IMG | Room masters run, wall mapping confirmed by the client, both salon and studio simplified to one wall each. Studio room master needs one more regeneration (light changed to night — see `LOG.md`); salon's `S9-SAL-R` is ready to run now | Homie generates · Claude reviews |
| **Tue 23** | IMG | `S9-STU-ROOM` regenerated and approved. `S9-SAL-R` and `S9-STU-L` generated and approved. No seam check needed — each world holds one wall alone | both |
| **Wed 24** | IMG | Fixes. `S9-SAL-R-DARK` (NBP edit; fallback: grade LIT down in the comp). Both plates approved | both |
| **Thu 25** | VID | New session. `S9-CRT-STRIKE` + 2 loops (`S9-SAL-R-LOOP`, `S9-STU-L-LOOP`) | both |
| **Fri 26** | VID + comp | Loop retries. Comp starts: Gérard portrait onto `S9-SAL-R`, Raft PAINT1–3 onto `S9-STU-L`, court Q1–Q5 (the one moment all three walls carry one world) | Homie comp · Claude cue sheet |
| **Sat 27** | comp | Transitions, light passes, cue timecodes for sound. Topaz 4K upscale of approved material | Homie |
| **Sun 28** | — | Delivery to the mapping software. Buffer — larger now that scope has shrunk | Homie |

## Dependencies outside this repo

- **Source images — DONE.** Gérard's *Louis XVIII in Coronation Robes* and Géricault's
  *Raft*, both verified public domain, high resolution, in `SOTR_MEDIA/comp/`.
- **Delivery spec from whoever runs the projection, before Sat:** codec (ProRes vs HAP), and
  the file container — one wide 9360 x 2160 file or three slices, and whether they want
  16:9 files. A 16:9 container is an export setting (wall at its true shape inside, the
  rest black); it never changes generation. Walls are generated at their own shape: L/R
  4:3, C 16:9 trimmed to 5:3.
- Worth raising with the set team, not urgent: does the physical floor already plan for a
  riser/plinth for the raft (out of scope for us, but relevant to the set as a whole)?
