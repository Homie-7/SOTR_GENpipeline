# BRIEF: Meeting 8 changes (Nov 2026)

Source folder: `G:\SOTR\Meeting notes\Nov 2026\` (meeting PDF, client flag screenshot, `Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav`).

## Homie's words, verbatim

### 2026-11-17

> So, we are now in the final stages where everything is being put on large screens and tested out for the final showing. We are working with sound designers and they are currently figuring out the score, voiceover, etc. And one of the major decisions that have been made is that the English parts will be cut off, and we are only working off the French stuff. So, obviously, we'll have to adjust the timing, pacing, get rid of a lot of things, etc. So, that's kind of where things are going. I have attached a folder here which has some meeting notes, some general breakdown of what the scenes should look like. There's also a request that the monarchist's flag should be changed. So, I'm attaching a screenshot from the client. Look at that, and find that flag and replace that with the plain white one. Obviously, pacing-wise, we are getting rid of all of the English stuff. I'm also attaching a sound design sample for your pacing reference. So, this sound design has the music and also the voiceovers, so you need to match everything to this in terms of duration and everything

> There will be changes for the scene four, I believe, where the judge Studio and salon is, We will work on that when it comes through.

> Go through it and tell me what you think needs to be done and then once that plan is ready we'll move forward

> For the Africa map transitioning into Sahaj's S7 clip, I just don't think we'll be able to get that final render from him anytime soon. So, I'm wondering whether the liquefaction we have at the moment for the Africa map is pretty good, the animation is spot on, everything is great. We already wrapped that up. I know that we kind of go into a transparency in the final render. Is that still the case? I'm just wondering if we want that just going into alpha, or do you think it'll be nice if it kind of becomes this watery thing that we already have? But then it's almost like it dissolves away. So, you know how, like, you put ink drops or something in water, and then it just kind of spreads and spreads, and then just kind of fully dissolves, becoming completely clear again in alpha so that the bottom scene can be adjusted in QLab. What do you think about that?

## Client (Louise, WhatsApp 4 Nov 2026, screenshot in the source folder)

1. "Could we shorten the time on the frames liberté égalité fraternité?"
2. "Although it is technically correct to have a white flag would it be possible to put in this flag as the monarchist flag?"
   The flag in her picture is WHITE WITH GOLD FLEURS-DE-LIS (the Bourbon royal banner), not plain white. Ours is plain white now.

## Meeting 8 (15 Nov) points that touch us

- English text and dialogue to come out of the battle sequence (S6), leaving the French. (On screen, every S6 word is already
  French; the English is only the time the old cut gave to Amina's lines.)
- Louise wanted to judge cuts projected, in the space; Homie (17 Nov) now says match the French track.
- Darrin's music starts when the map of Africa appears and runs through the ocean and the birds.
- Content ingestion Tue 17 / Wed 18 Nov; plotting Thu 19; notes over the weekend; re-ingest Mon 23; showing Thu 26 Nov.

## The new track (measured 17 Nov)

`Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav`: 121.25 s, 48 kHz stereo. The current S6 (v14) runs 165 s, built for the old track.
Rough cue map (faster-whisper, segment-level; to be refined word by word):

| Line | old s | new s |
|---|---|---|
| Après vingt-trois années de guerre | 18.0 | ~0-2 (check) |
| Pour nos braves... la victoire | 32.0 | 25.5 |
| Austerlitz ... Friedland, nous avons cru | 41-57 | 32.1-42.7 |
| La famine, les exécutions, la mort | 59.5-69 | 43.7-49.7 |
| Liberté, Égalité, Fraternité | 79-101 | 50.1-57.7 |
| Napoléon ... Waterloo, vaincu | 96-107.5 | 57.7-67.7 |
| Humilié ! Exilé ! ... mon pays | 110 | 67.7-74.7 |
| La France est divisée. Monarchistes ! Napoléonistes ! dangereuse | 121-131 | 74.7-84.7 |
| Alors... je pars | 137 | 84.7 |
| Oui, je dois partir ... Loin d'ici | 141-157 | 90.7-102.7 |
| the map + liquefy + dissolve | 147.5-165 | ~100-121.25 |

## Decisions

- 2026-11-17, Homie: "What I want from you is the WhatsApp-like scene composite that we've been making, so I can show it to them, and then based on that, we'll see if we want to change anything or not. But don't do the entire final thing, just create that side-by-side composite first"
  -> the deliverable now = the side-by-side WhatsApp review composite of the French S6 (like WhatsApp 06_S6), NOT the 4K/1080/CLEAN finals.
- 2026-11-17, Homie: "Fleur-de-lis flag" -> the RIGHT Monarchistes flag becomes white with gold fleurs-de-lis (Louise's picture).
- 2026-11-17, Homie: "Feel free to research the flag on the internet and see if you can find like a nice image of it. Also, just remember that the physics and the dirtiness and everything still has to stay as is"
  -> a good public-domain fleur-de-lis for the pattern; the generated cloth motion and the v6 wear/dirt stay exactly as v14.
- 2026-11-17, Homie: "The English can stay. If Darrin has kept it, that means we have to keep"
  -> the three English lines in Darrin's track stay; they are captioned as spoken.
- 2026-11-17, Homie (typed into the setup chat by mistake, relayed verbatim): "Remember, the entire map has to dissolve away so that it looks like the whole thing just turned into ink and dissipated or something. Just make sure it's done tastefully"
  -> the WHOLE map (land, sea, line, name) turns to ink and dissipates to clear alpha; tasteful, not a wipe.
- 2026-11-17, Homie (same relay, verbatim): "With the new flag, make sure that the texture and the flag physics are aligned and that it doesn't look like an overlay, just the way the French flag moves nicely in seams. You want to make sure that all of those icons or logos that are on the flag also move with the physics properly. It should look like it's a singular piece of cloth"
  -> the fleurs must ride the generated cloth's motion exactly like the tricolour's seams do (same cloth coordinates), lit and folded by the cloth; one piece of cloth, no overlay.
- 2026-11-17, Homie: "I just heard from the client that there will be an updated audio with just the French in it. So the look will have to match the visuals with the audio. That doesn't mean we can't run our tests, but just letting you know that there's going to be an updated audio"
  -> a NEW French-only track is coming (the three English lines out). When it lands: re-transcribe, rebuild the TMAP knots in `S6-FR-CUES.md` and `render_s6.py --retime-fr`, re-cut the review. The flag and ink look tests carry over unchanged (they don't depend on timing).
- 2026-11-17, Homie: "Make sure something like this happens, you're on top of it, and you run it automatically because otherwise I'm gone thinking that things are running but then nothing's happening"
  -> every render gets a watchdog (done / failed / launcher dead) and is relaunched automatically (memory `watch-renders`).
- 2026-11-17, Homie, on rendering the review now vs waiting: "do you think we should just wait for the original or the final version that comes through?"
  -> agreed: the review composite WAITS for the French-only track (no cut on audio that's about to change).
- 2026-11-17, Homie, on the fleur flag stills (80.5-84, the x-locked fleurs) and the ink v2 stills (113-120): "Stills OK"
  -> the fleur flag and the ink dissolve LOOK are APPROVED as stills. Next = the new audio -> retime -> review composite.
