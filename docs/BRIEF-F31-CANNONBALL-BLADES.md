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

## Homie feedback, 2026-11-25 (F34, verbatim)

"I agree with the flash scene settings. Obviously, else you only want to see the arms and blades and nothing else, not the whole person as it's supposed to be suggestive. Also, make sure that the arms are not like the character looks a bit zombie-like. We want to make sure that they are still people of the ship. So, I think soldiers or whatever the script calls for.

I'm happy to go with it not sure how you will incorporate this with lightning flash but I want transparent video so we can just trigger them manually in QLab. So it'll most likely have to be four different video files, all alpha, that we can trigger by locking sounds with them. I think?

With the explosion, I feel like it looks a bit generic and not really matching the atmosphere. So think about what the camp scene looks like, the colors and everything, the explosion needs to look realistic how it would be from an actual cannonball. We also need to see some kind of debris and ground stuff lying around and everything. I want the explosion to take over the entire screen rather than just center and a bit of left and right and bottom. The explosion should take over all four projector screens and then dissolve into a nice clean smoke, which can then transition us to the next scene. This kind of just looks like a cheap fade that we did using the explosion. Take a time with it if you need to, but that's what I'm after. Have a rethink about how this needs to be done"

Notes: knife scene = ARMS AND BLADES ONLY (no whole figures; the F1-F3 full-body cut-outs are retired), arms not zombie-like (ship's people / soldiers per BIBLE.md). Deliverable = FOUR separate ALPHA video files (ProRes 4444), one per flash, which Homie triggers by hand in QLab with sounds: HIS explicit exception to the final-product rule for this cue. Explosion = rethink: realistic 1816 cannonball impact matched to the S5 camps look/colours, debris + earth thrown up, fills ALL FOUR walls, then clears into clean smoke that carries into S6. Not the luma-keyed generic fireball + fade of review v1.

## F35 star chat decisions (2026-11-25)

### Knife scene, arms + blades (style frames, v2 of S9-RAFT-KNIFE-SF)
- Why the arms read zombie-like: the v1 knife prompt said "starving castaway, gaunt, hunched, thin bare arms", and still A's
  arm is veiny and gaunt. v2 drops every starving/gaunt word. The arms are STRONG, healthy working arms of the ship's people
  (BIBLE: soldiers and sailors of the Medusa, 1816): one SOLDIER (dark blue wool coat sleeve, red or white cuff/turnback, brass
  button, the briquet of still D) and one SAILOR (rolled striped or plain linen shirt sleeve, tarred cuff, a sailor's knife, the
  grip of still A). A fist that grips, not a claw; no long nails, no grey skin, no bulging veins, no reaching spread fingers.
- Same light as A/D: one hard cold blue-white flash from high above, pure black field (luma key). No word "lightning" (bolt lesson).
  Every blade points down toward lower centre (Agnes). Entries from top / top corners / side edges only.
- Four frames = four alpha files: F1 the SOLDIER arm alone from the upper-LEFT, F2 the SAILOR arm alone from the upper-RIGHT,
  F3 BOTH arms from the two top corners, closer together, F4 ONE arm close and large from the top (the murder). Distance is
  done by script (scale + a slight softness for F1/F2, full size F4), not by the prompt.
- Route: reference edits on still D (soldier) and still A (sailor) to keep the approved look; 2 cr each, ~8-10 cr.
- Flash files: ProRes 4444 alpha, CENTRE 1920x1080 (and 4K), each ~1.5 s: a 2-3 flicker in (lightning shape, 60-120 ms
  peaks), a hold of ~0.4 s, fall to transparent. Starts and ends fully transparent so QLab can trigger it at any time.

### Explosion rethink (plan before any video spend)
- Look first: sample the S5 show files (all four walls) for colour, light and ground: the impact must sit in that world.
- Shape: ball in from RIGHT, impact on the ground CENTRE/FLOOR, a black-powder burst (short orange flash, then grey-brown
  smoke and a column of EARTH, turf, stones and splinters thrown up and falling), the dust wave rolls out over all FOUR walls
  until each is full; then it settles to an even clean smoke that IS Scene 6's opening smoke.
- Route to test: image-to-video per wall from each S5 wall's real last frame (Seedance 2.5, locked camera), the same event
  timed on all four, so each wall's debris is its own and the smoke reaches full frame on all of them. Style frames first:
  2-3 stills (impact peak on CENTRE, dust wave on LEFT/RIGHT, the clean smoke end) as image edits of the S5 last frames.

## Homie feedback, 2026-11-25 (F36, verbatim)

"All four and probe at 480p. However, get rid of that light spot from E3. We want this to be just silhouettes coming along with lightning. So, the desk stat you did where there was a bunch of silhouettes tabbing randomly, it appeared very nicely with a bit of lightning effect around it. I'm not sure how you'll do it, but yeah, think of it as silhouettes hidden in lightning and they start from far and then come close. So, yeah, go ahead and do that. I'm gonna step away for a few hours, so continue working and building. Do not spend a stupid amount of credits. I still want 2000 credits left by the end of all of this"

Notes: knife = all four v2 frames (F1-F4), the F3 top light spot removed ("E3" = F3). Look = SILHOUETTES HIDDEN IN LIGHTNING, like the earlier test with many silhouettes stabbing at random with a lightning effect around them (the blades animation test); far (F1/F2) -> close (F4). Explosion = CENTRE probe at 480p draft. Credit floor: balance must stay >= 2,000 cr at the end.

## Homie feedback, 2026-11-25 (F38, verbatim)

"With the knife files alpha, I like the overall feel and the effect. There's two things that I'd like to do. First of all, there are holes in the silhouette. So you can see the dagger or the sword not fully connecting. There's holes in the arm or the clothing

I need you to fix that so it looks like a perfect proper image. Darken the silhouette a bit more because I think we still see a lot of clarity

One more thing that I would like is for the smoke or the lighting effect and everything to be clean enough that It should not touch the edges of the screen. So, for instance, if there is a central image with two hands holding their weapons, the edges should not touch the left and right. Same way, if it's over the right screen, it should not touch the left edge and things like that. They should be nice and dissolved in the middle, or not necessarily middle, but not really interloping with any other screens

I would also like the arms and the arms to have a bit of movement. So maybe like a very subtle animation that they are moving or just coming down or going up or something just so that it doesn't look like a static image in the lightning

For the cannonball, I quite like the drop and explosion and the quality of fidelity is pretty good. However, it's not selling the impact the way we want it. It needs to be fast, it needs to be violent. It, like I said, the explosion has to take over the entire four screens pretty much within a second or second and a half. So it just comes and boom, and then you see it going off. Yeah, so I'm happy for you to adjust the duration the way you think it looks more realistic, but it cannot be slow. And the ending would be the smoke dissipating, and then the embers and everything flying off and coming around, and then the smoke kind of settles into the first frame of The next scene so that we can match all of that Perfectly.

Fix all that. We are in the right direction"

(Screenshot attached by Homie: the F3 flash, both arms; holes show in the sleeves and the sabre blade is not joined to the hand guard.)

Notes: knife v2 = solid silhouettes (no holes, blade joined to the hand), darker (less inner detail), the glow/smoke fades out before the frame edges (no wall touches its neighbour), a subtle arm motion over the flash. Explosion v2 = fast and violent: fills all four walls within 1-1.5 s of impact, then the smoke thins, embers fly, and it settles on Scene 6's first frame exactly. Duration is Claude's call; not slow.

## Homie F39 notes (2026-11-25, verbatim; screenshot of knife F3 v2 in `docs/img/F39_homie_knife_F3.png`)

"With the explosion, I see that the ball is now coming from slightly another angle. Can we make it so that it comes from somewhere? I'm not sure where it should come from, to be honest, because I don't like overlapping screens. Ideally, if it just came from somewhere towards the tents are, so you kind of don't see it coming, and then suddenly it starts appearing in your vision because it was far, and now it's coming through the sky or something. I'm happy for you to think about what is more realistic and do that

The explosion is good, but it's still not big enough, It's almost like it's going in slow motion, so yeah, I just while it looks realistic and nice, it just doesn't speak the same amount of impact

And once the ball hits the smoke and everything is settling too slow. Is that an artistic choice because you want to match the flares or the rocks with the flares? Also, how does it sync up with the next scene? Because I see a harsh cut to the moving smoke.

That transition, if the whole rocks and everything, and the debris kind of slowing down and turning into the particles and the smoke for the next one, but it has to be seamless.

The knives are almost perfect. I really like most of them except for the ones where there's two hands at the same time. I feel like the hand is kind of cutting off at the wrong point. Can you create a separation between them? So we see two separate hands very clearly. Maybe offset their position a little bit so they're not like fist bumping, Make sure the cut is very clean and in the middle instead of because right now I feel like the cut is towards the arm with the longer knife and it kind of cuts between his hands yeah just keep them separate and clean, That I think mags are perfect

What's next? How are you going to do this, I need this finished before midnight"

- 2026-11-25 (F40, Homie, verbatim): "For your context, these arms with knives will be on the center screen and the left and right screens, depending on what the showrunner wants. They will not be on the water because that's where the actor is. The idea is that the actor is facing these arms looming over her, so that's just how it is"
  -> Knife flashes are WALL files only (CENTRE / LEFT / RIGHT, showrunner's choice). No FLOOR version.

- 2026-11-25 (F40, Homie, verbatim, NEW RULE): "Remember, the cannonball has to be a transparent file that overlays with the existing CAMS file so that I can just give it to them and it just perfectly aligns. Yeah, so keep that in mind"
  -> The cannonball deliverable is an ALPHA overlay (ProRes 4444) on top of `S5_CENTRE_camps.mov`, frame-aligned, handed over as is. Open (F41): at which timecode in the camps file does the ball land?

- 2026-11-25 (F41, Homie, verbatim, on probe v3): "You can see a clear cut where the cannonball appears. You basically like switch to a different point in that camp scene, and then the ball falls and the explosion happens. And then, after it's settling down, you can see another very hard cut to the frame that is starting of the next scene, so we very clearly see a very hard cut. I have very clearly said this before that the cannonball explosion has to be an alpha file so that we can overlay it with the camp scene. So we don't have to necessarily match things or do something with it, but for some reason that's just not registering with you. I'm not sure what's happening. The explosion itself, however, is really good. I like the speed, I like the impact, the debris and everything. It's just not coming along that well. Do you think a fade to black would help? I also noticed that the scene 6 starts at a very hard, very clear frame, like there is no ease in, or like from black to slowly fade into the smoke. So, clearly, the idea was that the smoke is the first frame. I'm wondering whether the explosion can happen and then we create some kind of temporary thing where it's just the embers and the smoke, and then that kind of gives rise to the scene six intro, which can then be faded in. I'm just thinking out loud: what do you think is the best way to do this? But yeah, the explosion and everything has to be an alpha. I'm sorry, it just can't be part of the camp scene because I can't give you an exact duration on when the explosion needs to happen, so we cannot match frame like that."
  -> CORRECTION of the F40 reading: the overlay is NOT tied to a camps timecode. It is a free alpha file the operator fires at ANY moment over the camps file. Nothing in it may depend on the camps picture. Keep the v3 explosion (speed, impact, debris).
