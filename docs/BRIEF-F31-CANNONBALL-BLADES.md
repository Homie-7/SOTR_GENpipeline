# Brief F31 (25 Nov 2026): Scene 5 cannonball + Scene 9 looming blades

## Homie, 2026-11-25 (verbatim)
> The subtle looming of hands with daggers/swords that we discussed in previous sessions.
> Script calls for a cannonball flying in and exploding during the camps scene. We made it on the fly last time during
> the showing but it was all done in resolume using random assets (F:\OrCha Drive\SOR Show Final\Renders (050422)). We
> realised that we won't be able to do any of that this time as there is no render that exists for the explosion. I
> believe the explosion is what takes us to the S6 with the whole smoke and french wars and all?
> Are you able to solve these issues economically and within today?

## Findings (Claude, 25 Nov)
- The 2022 explosion DOES exist as a render with alpha: `F:\OrCha Drive\SOR Show Final\SOR SHOW\SOR Renders\Camps\Exports\`
  `Front_/Left_/Bottom_CannonballExplosion.mov` (qtrle ARGB, 1920x1080, 29.97, 7.37 s, own sound). No RIGHT version.
  Also `Cannonball 080422.wav` (2022 sound) and an EXR sequence `Renders (050422)\Camps\Cannonball\` (150 f).
- What it does: a ball flies in (~0-2.5 s), flash + embers (~3 s), black smoke (~3-4.5 s), then the smoke CLEARS back to
  the battlefield and leaves debris. It is ungraded (does not match the approved rich-dusk grade).
- Our show files: S5 (430.8 s, 1080 25 fps) has no explosion. S6 opens on black with red-brown smoke and embers
  (LOOK.md: "Scene 6's first frame is that smoke"). So yes, the explosion is the bridge, but today the bridge is missing.
- Review: `SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/2022_reference/REVIEW_2022_explosion_over_S5_then_S6_start.mp4`.
- Blades: v1 (`04_WORKING_FILES/S9_raft/blades_anim_v1/`) rejected for cheap 2D arms; his v1 "wipe" timing kept.
  v2 rules in `docs/BRIEF-S9-RAFT.md` + `docs/BLADES-V2-REFS.md`. Nothing of v2 built.

## Proposed (waiting for Homie)
- Cannonball, 0 cr, script: grade the 2022 overlays with the S5 rich-dusk LUTs, lay them over the S5 battlefield per
  wall, then hold and thicken the smoke to darkness so the last frame IS Scene 6's first frame. Sound from the 2022 files.
- Blades, <=60 cr: 3 style frames of arm + period blade silhouettes (correct grip, tip on Agnes) as generated stills
  (~3-5 cr each), alpha by script; the "looming" (grow out of the dark, like a lamp shadow) animated by script, 0 cr.

## Homie, 2026-11-25 (verbatim, later)
> The original cannon ball that we had came in from right screen and landed right in the middle blowing up across the
> entire 4 screens. you can see how it was done in this documentation video alongside the actors at about 1:26
> "F:\OrCha Drive\SOR Documentation Video\06. Outputs\20220504_SOR show_V06.mp4"

## Findings 2 (Claude, 25 Nov)
- V06 is 1:28 long; the explosion is at ~1:05-1:11 (ball top right, full-screen yellow fireball, white-out).
- The 2022 Resolume asset is `Renders (050422)\Camps\CB_Explosion\Cannonball+Explosion.mov` (qtrle ARGB 1920x1080,
  29.97, 8.24 s, own sound): a black ball flies in, hits near camera, the fireball FILLS THE FRAME, fire -> black smoke,
  then the smoke clears. Also `Explosion_Alpha.mov` (4096x2160 alpha, 5.5 s, a small mid-air burst) and
  `Explosion.mov` (same burst on green). The green-screen version suggests a stock pack: licence/source not known.
- Sheets in `SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/2022_reference/`.

## Revised plan (waiting for Homie)
- Cannonball, 0 cr, script: ball enters on RIGHT, lands CENTRE; the 2022 fireball spreads over LEFT/CENTRE/RIGHT/FLOOR;
  fire falls into black smoke + embers and does NOT clear, so the last frame = Scene 6's first frame. Graded to the
  rich-dusk look. Built into the S5 files with the 2022 sound. 30 s review first, then the 4K files on his yes.
