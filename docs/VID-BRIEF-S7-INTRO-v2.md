# VID BRIEF v2 — S7 intro flight, REDO (Homie's review, 6 Oct 2026)

Supersedes `docs/VID-BRIEF-S7-INTRO.md` (v1: its review cut was rejected). Read v1 for the connector facts; everything
below overrides it.

## Homie's verdict on v1 (verbatim, 6 Oct)
*"The intro video is a fail because the bird is not even flapping. We're just kind of randomly seeing it glide. It never
really goes far or close to the camera, it just keeps flying. It looks extremely AI generated. We approach the ship from the
front rather than somewhere else, and then we sit on the front deck border of it. Like the whole point is to land inside the
last frame where the scene will continue. So we should be where the _strip_wreck_v1 angle is. Redo the thing again, make it
more believable."*

## What that means (the brief)
1. **The bird flies like a real herring gull.** Real wingbeats (deep, steady flaps, roughly 3 a second, in bouts) with short
   glides between them, banking, the body rising and dropping with each stroke, the tail and the wingtips flexing. Never a
   rigid glider sliding across the frame.
2. **The distance to camera CHANGES.** It comes close (filling a good part of the frame, a wing passing near the lens),
   pulls ahead and away (small against the sea), then comes back. A living subject, not a sticker at a fixed distance.
3. **Believable, not AI.** Real capture: a following camera with weight and small corrections (a boat or a drone keeping
   pace), real sea texture and spray, real light on feathers. Nothing glossy, no locked perfect framing on the bird.
4. **Approach from ASTERN or the quarter, not head-on.** The ship sails AWAY from us; we catch up from behind and to one side,
   pass up along her side, and come over the rail at the stern/quarterdeck heading FORWARD. (v1 met her head-on and landed
   on the bow rail: rejected.)
5. **The last frame IS the deck plate.** The camera comes aboard and settles into the deck POV that the three walls show:
   aft of the foremast, looking forward along the deck to the bow (the `_strip_wreck_v1` / `assembled_v1` angle, in DAY
   light: the wreck happens later). The intro's final frame = our CENTRE wall exactly, so the cut to the three walls is
   invisible. The gull flies on out of frame or lands out of the way; the plate is empty at the end.
6. **The ship = OUR ship.** Red-ochre bulwarks, plain wooden rail cap, guns, the single foremast with its furled yard, an
   1816 French frigate: NO gilding, NO baroque balustrade, NO dark hull with gold bands (v1's ship did not match the deck).
   Masthead/ensign: plain white (Bourbon), never red-white-blue.

## The END FRAME (made, 0 cr)
`/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship/4_intro_video/endframe/S7-SHIP-C_day_16x9_ENDFRAME.png`
(1920x1080: the deck master f5180ed8 at 16:9; its centre 1800 px = the CENTRE wall, mean diff 0.5). Seedance 2.5 has an
`end_image` role in `omni_reference` mode (v1 found `start_image` held frame 0 this time; `end_image` is UNTESTED: test it).

## Suggested route (the VID session decides, logs why)
- **Shot A, the flight** (omni_reference, start_image = a NEW first frame or the hazed F1 re-done from astern; the ship
  reference = the deck walls + Baugean for the hull): the gull flapping, distance changing, catching the ship from astern.
- **Shot B, coming aboard** (omni_reference, start_image = A's last frame, end_image = the ENDFRAME): over the quarterdeck
  rail, along the deck, settling into the plate. Sequel mode can't take an end_image, so B is omni_reference, not a Sequel.
- A new first frame for A (an NBP still, the ship from astern-quarter, small, the gull mid-wingbeat) is IMG work: make it in
  an IMG session first, or ask Homie whether a quick IMG step inside the VID session is acceptable (house-rules MODE rule).
- **Option to raise with Homie if flapping fails twice:** motion transfer (motiondojo / Genjutsu) from REAL herring-gull
  flight footage, which carries real wingbeats. Needs a licensed or own clip.
- Probe cheap first: 480p drafts (v1 showed a 15 s draft costs 45 cr, less than a 4 s 1080p probe, and the finalize keeps
  the motion). Finalize only a draft that passes. Stop after two failed versions of the same defect.

## Checks after every run (in addition to v1's)
Count wingbeats per second over the clip (must flap, in bouts); measure the gull's size in frame over time (must vary by
>3x); ship from astern (stern windows / wake toward camera), no gilding, white flag only; the LAST frame vs the ENDFRAME
(mean abs diff, landmark positions within 1%).

## Budget
Balance 1,127.49 (6 Oct, after v1). Keep 500 at the end of the week (Homie). Cap for the redo: 450 cr. One job at a time,
get_cost first, transactions after.

## Also queued for this VID session (after the intro, if budget allows)
**Side-wall sea loops that move as ONE sea with CENTRE** (Homie: "while they are animated, it all looks like a single
scene"): the same swell direction, speed and scale on all three walls; the flight's side walls hold the DAY sea. Loops are
generated on the SEAMED walls (`3_walls/seamed_v1/`), never the old assembled ones.
