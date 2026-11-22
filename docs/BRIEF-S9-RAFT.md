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

## Homie, 2026-11-22 (on plan v2)
> Happy to do route a probe, but I am wondering if any stock footage or something else can be used to stylised or
> something? I have envato, whatever is easy and cheap

=> Route C offered: an Envato Elements top-down drone ocean clip (on his subscription, 0 cr), graded to moonlit night,
looped in the file. Route A probe stays the fallback. Waiting for his pick.

## Homie, 2026-11-22
> Sure, stock first, my envato is logged in on brave

=> Shortlist (Claude, from Envato thumbnails only; Homie downloads in Brave into
`SOTR_MEDIA/04_WORKING_FILES/S9_raft/stock/`; Claude then checks camera move, length, fps, grades + loops, 0 cr):
1. Baltic Sea Waves Top View — https://elements.envato.com/baltic-sea-waves-top-view-DHJHEAG (dark, straight down, foam veins)
2. Aerial Top View on Big Wave of Atlantic Ocean — https://elements.envato.com/aerial-top-view-on-big-wave-of-atlantic-ocean-U6VGS3Z (dark water, big white crest)
3. Turbulent Blue Ocean Water with Foamy Waves — https://elements.envato.com/a-slow-motion-view-of-the-wake-from-the-cruise-shi-WUJJV9V (rough, deep blue; it may be a ship wake from a moving camera)
4. Aerial View of Dark Ocean Water with Waves — https://elements.envato.com/waves-crashing-by-the-seashore-on-stormy-day-aeria-434JESP (very dark; may be near a shore)
5. Ocean Waves Aerial Birds Eye View Monochrome — https://elements.envato.com/aerial-top-down-view-of-large-waves-in-the-ocean-i-4UDFP2K (already B/W, stylised; waves roll one way like surf)
Rejected: turquoise/tropical, beaches, rocks, tilted views, flat calm (`top-view-of-sea-surface-5Q9URPU` too calm for "extreme danger").

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

## Homie, 2026-11-22 (night, his pick)
> It is late, at night, darkish blue open ocean, waves around  her but not tubulent. I chose this, can you work with it?
> "G:\SOTR\HF\Final changes\221126\aerial-view-of-turquoise-ocean-waters-2026-10-02-17-18-47-utc.mov"

=> Route C with HIS clip (not from the shortlist). Look: late night, darkish blue, open ocean, waves round her, NOT turbulent.

## Homie, 2026-11-22 (night, scope change)
> Dont worry about the raft and audio, they will follow our video and projection expert will handle it.
>
> I do want your help with daggers as that still hasnt been done by sahaj, we can have a crack at that. You know the silhouette's of shadowy daggers etc (accurate to history and setting) suggesting across all screens (center, left, right) that creates a sense of horror and dread, you can refer to the script and even look up the historical documentation of how things went so we can capture the vision and the mood.

=> Water: clean loop only (no raft mask, no sound in the deliverable; the projection expert does the raft fit).
=> DAGGERS: we build them (not Sahaj). Shadow silhouettes of period blades across LEFT, CENTRE, RIGHT. Horror and dread.
   History-accurate (Medusa raft, July 1816). Look agreed first: references, then 2-3 style frames, Homie picks.

## Homie, 2026-11-22 (night)
> Dont draw any holes, we will give them full video of the ocean and they will decide how to get the raft in there

=> Water deliverable = the FULL 16:9 ocean frame at 4K: no raft hole, no black bars, no edge fade, no sound
   (`tools/raft_water.py` default; `--envelope` / `--raft` keep the old FLOOR-PLAN framing for reference only).

## Homie, 2026-11-22 (night)
> Just know  that it is night only lit by moon light so it has to match the setting. What about the daggers now?

=> Water: moonlight is the ONLY light (no warm light, no sky glow). Blades: one cold moon source, shadows match it.

## Homie, 2026-11-22 (night, blade look)
> Old style sharp little dagger and sabers that the naval soldiers had back then. Nothing too literal, sugggestive only, may be in alpha so that it can be superimposed

=> BLADES = small sharp period daggers (naval dirk / poignard, sailor's knife) and sabres (infantry briquet An XI, boarding
   sabre An IX). Suggestive, not literal: soft, partial shadows, no detailed hands or bodies. Delivered as ALPHA (shadow
   matte with transparency) so the team can lay it over any picture. Style frames show each direction over a dim moon wall
   for the look, plus the alpha PNGs.

## Homie, 2026-11-22 (night, on style frames A/B/C)
> WE can be stylistic with it, an arm holding it coming out of dark or something, randomise, from a screen or two, its contained, the light will be on agnes, the water around her, rest of the stage is dark, you only see these stabbings in glimpses, stabbing. almost horror like. the can close in from all directions, but not at the same time. and then sudden attacks and stabbing, ganging, up, back to back, Do you catch my drift?, Also open the water file again for me so I can see is it in 4K or full HD

=> BLADES direction: stylised horror GLIMPSES. An arm holding a period blade comes out of the dark (arms ARE back,
   stylised, emerging from black, not literal anatomy). Randomised: one screen or two at a time, never all at once.
   Light is on Agnes + the water; the walls stay dark except the glimpse. Build: they close in from different walls in
   turn (one at a time) -> then sudden attacks, stabs ganging up, back to back, fast. Alpha deliverable stays.
=> Water: the 4K master is 3840x2160 (ProRes, 10.5 s loop); the 40 s preview is 1080 (review only).

## Homie, 2026-11-22 (late night, on blades animated test v1)
> I think the wipe that you're going after is pretty good but the hands just look really cheap They're all holding blades the wrong way you can see that the blade is not even pointing towards the actor so imagine the actor is standing on the bottom screen which is the bottom projector the blades only have to come from either the top left top right angles so nothing from bottom obviously so side or top because that's just how the sense of dread and the impact registers as the person is standing in the middle in the bottom and everything else is surrounding them the arms have to look a bit better it just looks cheap 2D animation the blades are not even aligned to the wrists and holding properly the blade should be pointing towards the actor agonist rather than being in line with the hand it just looks stupid like why is the blade pointing towards the person holding it just think about all of this don't just blindly make something

> Also, what is the frame rate of the water? Because it feels a bit stuttery

=> KEEP: the "wipe" (the glimpse timing / reveal idea of v1 is good).
=> FIX: arms look like cheap 2D animation. The blade must sit IN the fist, aligned with the wrist, and POINT AT AGNES
   (she stands at the bottom centre, on the floor projector). Never point back at the holder.
=> Directions: arms come only from the TOP, TOP-LEFT, TOP-RIGHT or the SIDES. Nothing from the bottom. She is in the
   middle at the bottom and everything surrounds her: that is where the dread and the impact register.
=> "Think about all of this, don't just blindly make something": references first, then style frames, then build.
=> Water: 24 fps. Cadence measured even (no dropped frames), so the stutter is 24 fps judder of sharp, fast-shutter
   drone frames with no motion blur. To test: blend source frames (shutter blur) at 24 fps, or a higher frame rate.
