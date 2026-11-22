# BRIEF — S9 RAFT beats (b1 open ~40 s, b10 close ~30 s)

Opened 2026-11-22. Status: PLAN ONLY, waiting for Homie's choices. 0 cr spent.

## Producer note (relayed by Homie, 2026-11-22, verbatim excerpt)
> Agnes appears in two short bursts on the raft at both the beginning and the end of this scene. She will be in the middle
> of the stage while the other scenes play around her in turn. She will now be positioned on a physical raft set piece,
> built by Kate. We will need a little water surrounding her to establish that she's floating out in the open sea, along
> with sound design that conveys extreme danger and the screams and cries of the people around her.
> She needs to be stabbed at the end of the scene. We could repeat the projected shadows of the daggers and sabres Sahaj
> creates at the end of Scene 8 along with SFX.
> I don't believe any of this should affect the timing of the other elements (palace, judge, Gericault's studio).

Script: start RAFT ~40 s (moonlight, crashing waves, biscuit torn away); end RAFT ~30 s (barely alive, a shadow with a
sabre, four still images = four stabs, tossed off, blackness).

## Homie, 2026-11-22
> Go through it and give me the most economical and best possible way to do this. This has an actor involved so water
> has to be hyperreal-ish I think?

## Homie, 2026-11-22 (later)
> The perspective is top to down, in the bottom projector

=> The water is a FLOOR file (floor projector, top-down, orthographic, true scale; `docs/FLOOR-PLAN.md` rules: 16:9 frame,
envelope 10,057 x 4,350 mm, top of picture = upstage, mostly dark, brightness cap, no pre-warp). The S7 horizon sea below
does NOT fit a top-down view; it stays only as the look/colour reference (moonlit, dark teal, glints).

## Plan v2 (top-down, 2026-11-22) — recommended
1. Water: ONE Seedance 2.5 top-down probe of a moonlit night sea (4 s, ~48 cr, unconfirmed), then on Homie's yes one
   ~15 s take looped (~180 cr, unconfirmed) for b1 (~40 s) and b10 (~30 s). Total ~230 cr. Script fallback (0 cr): a dark
   scripted swell with moving moon glints (Homie has called drawn water "cheap" before, so generated is the default).
2. Script (0 cr): raft footprint masked black (no water light on the raft or Agnes), a soft foam/wash line where the water
   meets the raft edge (sells "floating" most), brightness cap, seat preview from 3 seats (`tools/stage_preview.py`, FLOOR-PLAN step 3).
3. Stab: Sahaj's S8 dagger/sabre shadows played by the FLOOR projector, so they fall across the raft and Agnes from above.
   Four still frames, hard cut on each hit, then black. 0 cr.
4. Sound: the take's sea sound as scratch; screams, cries, danger are Darren's.
Needs: Kate's raft footprint + position on the floor; Sahaj's S8 shadow file (alpha if possible); Darren's raft audio.

## Plan proposed (2026-11-22, superseded by v2: assumed walls)
- Water: reuse our own moonlit night sea take `04_WORKING_FILES/S7_ship/9_seaplate/S7-SEA-IDLE_night_v2_6f1a54ec.mp4`
  (+ its 4K `_UP4K_402a31e9`), Seedance, photoreal, ship-free, already upscaled. 0 cr. Recut per wall with the horizon
  lowered to a crouched eye on a raft; kept dark (brightness cap) so the stage light on Agnes wins. Rougher sea only if the
  calm take reads too calm: one Seedance take from the same plate, ~10 s looped, ~120-180 cr, on Homie's yes.
- Rejected: the 2019 Houdini `oceanBSurface_1109.mp4` (stylised teal CG, 4096x3112 equirect): not real enough beside an actor.
- Stab: reuse Sahaj's S8 dagger/sabre shadows (his file), cut as four still frames on four hits, then black. 0 cr.
- Sound: the take's own sea sound as scratch (house rule); screams, cries and danger are Darren's.

## Open questions
1. Floor projector confirmed? (Water on the floor round the raft is the strongest read; else walls only.)
2. Sahaj's S8 shadow file (alpha if possible) and which surface the shadows fall on.
3. Darren's raft audio / cue lengths for b1 and b10.
