# S9 b10 BLADES v2: references, grips, aim (RAFT6, 2026-11-22)

Homie's notes (BRIEF-S9-RAFT.md, last section): keep the WIPE (v1 glimpse timing). The arms read as cheap 2D animation.
The blade sits in the fist, in line with the wrist, and points AT AGNES. Arms come from the top, top-left, top-right or
the sides, never the bottom. "Think about all of this, don't just blindly make something."

## 1. What was wrong in v1 (seen on blades_anim_v1/_stills_sheet.jpg)
- Arms are constant-width tubes with flat ends: no shoulder, elbow, wrist taper or fist mass.
- The blade angle is random relative to the forearm; several tips point away from Agnes.
- One arm enters from the bottom-right with the blade up and back.
- The motion is a rigid slide; no wind-up, no strike, no recoil.

## 2. Aim and entry per wall (Agnes = bottom centre, on the floor projector)
| Wall | Entry edges allowed | Blade direction (tip) |
|---|---|---|
| LEFT | top, top-left corner, left (outer) side | down and to the right (towards the stage centre) |
| CENTRE | top, top-left, top-right corners | straight down to bottom centre |
| RIGHT | top, top-right corner, right (outer) side | down and to the left |
The tip vector is computed per stab from the hand position to a fixed aim point below the bottom edge of the wall
(Agnes's position in stage space), so every blade converges on her. Never an entry from the bottom edge (asserted).

## 3. Grips (period-correct, 1816 Medusa raft)
- REVERSE / ice-pick: the blade leaves the LITTLE-FINGER side of the fist; overhead downward stab. For the dirk,
  the clasp knife, a bayonet held as a spike. Fist knuckles face the viewer or away; the blade continues the
  forearm line downward.
- SABRE / hammer thrust: the blade leaves the THUMB side; wrist cocked so the blade continues the forearm line.
  For the briquet (D knuckle bow round the fingers), the boarding sabre An IX (iron shell guard over the knuckles).
- The boarding axe is a chop (haft in the fist, head beyond), used once at most.
- Arms wear torn 1816 sleeves: sailor's shirt (loose, ragged cuff), soldier's coat cuff (one arm: the 4 executioners
  = 3 sailors + 1 soldier, RESEARCH doc). No modern details.

## 4. Mood references (public domain, all before 1819)
- Robertson's Fantasmagorie (Paris, 1797+): a projected figure that GROWS as the lamp moves in. This is the model for
  the "lamp shadow" look: soft edge, size change, sudden.
- Seraphin's ombres chinoises (Palais-Royal, 1784+): hard cut-out shadows, clean profile.
- Goya, Los Desastres de la Guerra (1810-1820): arms and blades in raking light out of black.
- Gericault, studies for The Raft / Mutiny on the Raft (Harvard Art Museums 1943.824): the knife fight on the raft.

## 5. Route
- Script route first (0 cr). Blender 5.2 is installed: model an organic arm (shoulder-elbow-wrist, sculpted fist,
  torn sleeve) + the period blades (profiles from tools/blade_frames.py), render a TRUE cast shadow on a wall plane
  from a near lamp (real perspective, soft penumbra, motion blur), alpha out. Wind-up -> strike -> recoil animation.
- Generated route only if Blender cannot reach the look: full settings block + estimate first, cap 60 cr.

## 6. Style frames for Homie's pick (next step)
- A LAMP SHADOW: a hard-to-soft cast shadow on the dark wall, growing as it strikes (Fantasmagorie).
- B RIM-LIT ARM: the arm itself out of black, cold moon rim on the sleeve, fist and blade edge (Goya).
- C SMEAR GLIMPSE: B with a heavy motion smear; only the strike frame is sharp (the "wipe" at its fastest).
Each frame shows all three walls, correct grips, every tip on Agnes.
