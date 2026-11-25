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

## Homie, 2026-11-25 (verbatim, third)
> Do you think that is an even better way to do the cannonball or you think your way is the best. Given we have new
> abilities such Higgsfield and whatnot, do you think we can make a cannonball animation from scratch, but just like
> this, so that it can be triggered as an alpha on top and then the smoke and everything kind of transitions to new scene?
> What do you think is the best approach
>
> The blades had a review that it doesn't have to be so much aggressive stabbing all over the place, it's just a
> threatening situation where it's kind of almost looming here and there, so it's almost like imagine if it was just
> lightning or something. Every time the lightning happens, you just see a hand or two, and slowly, slowly them getting
> closer. It's just like the threat of this is going to happen, which then eventually leads to the murder.

## Proposal 3 (Claude, 25 Nov, waiting for Homie)
- Cannonball = a triggered cue file per surface (ProRes 4444 alpha over S5), ending FULLY OPAQUE on Scene 6's first
  frame, so the change to S6 is in the file (a cut from an identical frame), not a playback crossfade. Needs Homie's OK
  to use alpha-over-S5 layering in playback (the 24 Sep "no QLab" rule).
  Ball flight by script (0 cr). Fireball generated on pure black (Seedance 2.5, locked; 1819 round shot, black powder),
  keyed by luminance: 720p 8 s probe = 56 cr, 1080p 8 s = 128 cr. Black smoke = Scene 6's own opening smoke through a
  growing matte (0 cr). LEFT/RIGHT/FLOOR = the same fire offset + flash light (0 cr). Fallback: the 2022 fireball (0 cr,
  licence unknown).
- Blades = lightning reveals: a flash lasts 0.1-0.3 s, so a still is physically right inside it. 4-6 generated stills
  (Nano Banana Pro, 2 cr each) of 1-2 hands with period blades in hard top flash on black; script does the flash shape,
  the dark between, and the approach (closer each flash), last flash at the murder.

## Homie, 2026-11-25 (after a call with the client), verbatim

"I just spoke with the client and the way they described the knife scene was that they imagine it to be a small thing kind of in a distance and then it slowly gradually comes up and then becomes this big looming presence that is extremely threatening

I don't think they are thinking of more than two people, so maybe two to three at most. Historically speaking, there were knife fights every day on that ship, so we can take some inspiration from that, but they're not expecting much. It just has to be this. I do like my idea of lightning, and every time there's lightning, you see this looming dagger-holding hand or something. Or we can even go with some level of silhouette, just like the Judge, but nothing too crazy.

What do you think can work with this? I don't think we need to go left and right in this, we can probably just have it in the center screen."

### Proposal 4 (F33 star chat, waits for Homie's yes)
- CENTRE only. Two figures (three at most). Lightning reveals; black between flashes.
- The approach is the distance changing per flash: (1) FAR: two small silhouettes with knives at the far end of the raft, lit
  from behind by the flash (a sky and bolt are fine here); (2) MID: the same two, waist-up silhouettes, bigger, nearer;
  (3) CLOSE: one arm and dagger from the top, looming over the frame, the hand lit (still A is this already).
  Last flash = the murder. Silhouettes = the same language as the Judge.
- Make: 2 new style frames (FAR, MID), about 4-8 cr, then a script review (flicker, scale per flash). Blades v2 B/C/D are
  not needed for this (one hand only at the close stage); the bolt problem stops mattering in FAR/MID (sky in frame).

## Homie, 2026-11-25 (reply to Proposal 4), verbatim
"Yes, can we do this in alpha and may be both at the same time is much, How about we start with one lightning shows one guy on one side, the other on another side at another lightning, and then they kind of coalesce together at another lightning, and then finishes with the closed version, something like that, rather than just having them both at the same time, it just looks a bit silly and you don't give any suspense by showing them both at the same time?"
"Also, where's the explosion at? What happened to that"

### Proposal 5 (agreed shape): CENTRE only, ALPHA file (ProRes 4444) over the raft scene. Flash 1 = man 1 alone, far, one side.
Flash 2 = man 2 alone, far, the other side. Flash 3 = both together, nearer, centre. Flash 4 = the close looming dagger (still A),
at the murder. Black (transparent) between flashes. Style frames: 3 new stills (man 1 far, man 2 far, both mid), silhouettes.

## Homie feedback, 2026-11-25 (F33 star chat)

- On blades stills A + D: "These two are good, but I want to see the full saber."
  -> D redone as a reference edit with the whole sabre in frame: `04_WORKING_FILES/S9_raft/blades_v2/S9-RAFT-BLADES-SF_v3_D_fullsabre_7ec27fce.png` (2 cr). Waiting for his look.
- Knife-scene style frames (Proposal 5) built: `04_WORKING_FILES/S9_raft/knife_sf_v1/` (F1 man 1 left, v1b F2 man 2 right, F3 both nearer; black cut-outs on white, inverse-luma alpha). Waiting for his pick.
