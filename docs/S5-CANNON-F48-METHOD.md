# S5 cannonball option B, F48 method: "GLOW BRIDGE + ONE WIDE TAKE" (assessment 2026-11-25)

Read first: CLAUDE.md, docs/BRIEF-F31-CANNONBALL-BLADES.md (F46 + F47 notes verbatim), docs/HANDOFF-2026-11-25-F48.md.

## 1. Why mirror_v2 had a jump cut on CENTRE (measured, F48)
The CENTRE wall cut from the real camps file (1920x1080 ProRes, 25 fps) to the v4 TAKE at take f1. The take does NOT
reproduce its start image:
- resolution: the take is 854x480 (480p draft), upscaled 2.25x -> the sharp grass texture goes soft at once;
- colour: mean BGR camps last (71.9, 93.8, 124.7) vs take f1 (70.1, 90.3, 118.6): red -6, the frame drops darker/cooler;
- content: Seedance redraws the frame (tree groups and tents move, horizon detail changes); MAD 13.4, blurred MAD 8.7
  (camps frame-to-frame MAD is 0.4). Phase correlation shows a ~28 px vertical offset at 1080.
- the ball is already in the sky at take f1 (it pops in).
Rule from this: **never show a generated take's pre-impact frames as a continuation of a show file.** Every generation
re-draws the start frame. A cut is only invisible under a full-light event.
Also: the camps walls are NOT one panorama (LEFT hills, CENTRE plain to the sun, RIGHT hills + tents, FLOOR top-down
ground), so no wide take can continue all four camps pictures; the takeover must hide the change of picture.

## 2. Why the takeover failed so far
- walls_v1: four generations = four different events, times and grades. Unfixable by timing alone.
- mirror: one event, exact seams, but symmetry reads as a kaleidoscope (and floor as a reflection). Dead.
- Common gap: the moment of cut was not one LIGHT event; CENTRE showed a fireball on an intact plain while the other
  walls were already smoke (Homie's screenshot).

## 3. Proposed method
A. **Before impact: the real show files on all four walls.** No generated frames. The ball on CENTRE is composited onto
   the real camps CENTRE frames (keyed from the take as a dark disc: take minus its own f0, plus motion blur, scaled to 1080).
   No jump cut is possible: the camps picture continues unbroken until the light.
B. **Impact = ONE light (Homie's glow idea).** A warm yellow-white glow starts at the impact point on CENTRE and spreads
   over all four walls within ~3-4 frames, computed in ONE stage coordinate space (distance from the impact point across
   L|C|R + FLOOR), so it is one light source crossing the seams (CLAUDE.md: light may cross). It peaks near-white on all
   walls on the SAME frames. Every wall cuts to the blast under the peak.
C. **After the glow: ONE wide take, cut into contiguous windows (no mirror).** One Seedance take at 21:9 shows the whole
   event: the explosion starts in the centre and the ground breaks (what Homie liked in v4), then the blast and smoke run
   outward to both sides and up past the top. Map: LEFT | CENTRE | RIGHT = three contiguous thirds of one horizontal band
   of the take (anamorphic 1.5x horizontal stretch so the band keeps ~65% of the frame height); FLOOR = the same take's
   ground BELOW the band, under the CENTRE third, NOT flipped (the nearer ground continues toward the audience; the
   vertical stretch is the floor's foreshortening). Result: seams are continuous because it is one picture, all walls are
   the same frame (time-aligned), one grade (colour-matched), no symmetry.
   The start image of the wide take = the CENTRE camps last frame placed in the centre third of a 21:9 canvas (squeezed
   1/1.5) and outpainted to 21:9, so the look and grade stay the camps dusk.
D. End: the take darkens to embers/black; eased fade to black (S6 files fade in from black).
E. Sound: the take's own sound on every wall file (sound rides in every file).

Cost and limits: 480p 21:9 band = 1120x480 -> each wall window ~373x316 px, a soft draft (judge timing, seams, flow only).
A final needs the 1080p take (2520x1080 -> windows 840x709, ~2.3x to 1080, 4.6x to 4K via Topaz; smoke tolerates it,
sharp debris less). Honest risk: the side walls will be softer than the 16:9 v4 CENTRE.

## 4. Probe plan
1. Outpaint the squeezed CENTRE canvas to 21:9 (estimate first, ~2-5 cr).
2. Seedance 2.5, start image = that canvas, 21:9, 480p draft, 10 s, sound ON, batch 1: ~30 cr. Prompt = v4 layout
   (labelled blocks), patched: wide view, impact at the exact centre, blast spreads to BOTH side edges and the top.
3. `tools/cannon_glow.py` (new, 0 cr): steps A-E -> 4 wall drafts + stage review (L|C|R over FLOOR + S6 heads),
   contact sheet, measure (seam MAD, glow peak frame per wall, CENTRE pre-impact MAD vs camps = 0).
   Folder: `04_WORKING_FILES/S5_cannonball/glow_v1/`. Open with explorer.exe. WAIT for Homie. Promote nothing.
Total ~35 cr (balance 1,993.85 -> ~1,959; floor 1,500).
