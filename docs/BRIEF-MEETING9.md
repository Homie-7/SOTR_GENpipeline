# BRIEF: Meeting 9, Scene 9 generated judge (started M9x, 2026-11-20)

Goal: the court judge on CENTRE as generated Seedance takes, reading idle under Darren's lines, strikes on the cues,
no hard cuts, review composite at 720p before any upscale. Earlier notes verbatim: `docs/HANDOFF-2026-11-20-M9t.md`;
causes: `docs/S9-JUDGE-M9u-DIAGNOSIS.md`.

## Decisions
- One size per file, no zoom cuts inside a file (M9u diagnosis of Homie's LEAN notes).
- **The judge gets closer each appearance, ending on the torso** (Homie, M9x): b3 Q1 full figure small, b5cut Q2,
  b7 Q4 head-and-chest for the whole beat. Black between beats hides the size change.

## Homie's feedback, verbatim
- 2026-11-20 (M9x): "the judge just gets closer and closer. And the last time it's just like he's basically just his
  torso, so I'm imagining you're still keeping that level of scale by just fixing the things around it and the changes
  we are making, For example, in the full version around 4 minutes and 59 seconds, you see him basically just torso.
  That is what I want., you just have to make sure that now the hard cut edges are visible"
  (read as: keep the torso scale, with no hard cuts.)
- 2026-11-20 (M9x, on the FLOW review, with two stills: gavel head cut off at the left of the outstretched arm; a loose
  blob under the scroll): "The edges are still killing the image in terms of hammer and everything. Like you can see it
  cutting off because of it being a vertical silhouette. Around 3 minutes and 38 seconds, I see a bit of an artifact
  under the paper he's holding. Animation is still completely off. It just he's talking at some points and he's not
  talking at some points. You can see the lips moving at random points when he's when the audio is going, the voiceover
  is going, there's no mouth movement, but then suddenly there is mouth movement. It looks inconsistent. Can we get rid
  of the lip movement entirely? Just have his head moving? That's it. Yeah, there's artifacts everywhere, including 3:46.
  Yeah, so get rid of the left movement completely. Fix all of these artifacts that are occurring here and there. Fix
  that image cutting off. I don't know how will you do it if you need to generate it in horizontal or something, just do
  that. But yeah, it's clearly not looking right. Although the blends between the gavel hitting and him resting into his
  position are much more smooth now, so there are no hard cuts. But yeah, I need you to figure this out. Now, do you
  think you can do this within the remaining credits or do you want me to swap account"
  (KEEP: the smooth strike/rest blends. FIX: no lip movement at all, head moves only; no clipped gavel/arms, generate
  horizontal if needed; no loose blobs/artifacts.)
- 2026-11-20 (M9x, approving the two 16:9 takes, 105 + 28 = 133 cr of 142.3): "Make an exception and turn off the sound
  in this one so that the mouth does not move. Make sure you also figure it out with prompting so that there is no mouth
  movement. If it stays within budget then you can go ahead and generate."
  (DECISION: sound OFF for the v8 READ and v9 RAISE takes only, an exception to the sound rule; the prompt must also hold
  the mouth closed. GO, within 142.3 cr.)
- 2026-11-21 (M9z, on the FLOW2 review, with a still of the b7 torso at ~4:57: the scroll a soft lumpy mitten-shaped blob):
  "the 3:29 morph is absolutely disgraceful you can literally see him almost like water color fade away and then come back
  there is no continuity, same around 4:01. Around 4:57 i see off morphing aND ARTIFACTS. After two days of working and
  spending nearly 500 or more Higgsfield credits, this is an unacceptable result. We are almost there, but I need you to
  fix these errors. You can clearly see it frame by frame. How did you miss this? Are you able to fix this or not? Because
  these issues looks horrific"
  (FIX: no morph/dissolve that fades the figure (3:29, 4:01: the sdf_morph raise->strike joins in b5cut); no off-morphing
  or artifacts in b7 (4:57, scroll shape). CHECK FRAME BY FRAME across every join, every frame, not every 2nd frame at +-6.
  Still saved: `04_WORKING_FILES/S9_gen_judge_review/_HOMIE_NOTE_FLOW2_457_still.webp`.)
- 2026-11-21 (M10a, after the diagnosis): "An update from Darren, he has done some sound design changes and has added some
  more changes to the thing. So you will be referring to this file here "G:\SOTR\HF\the judge TO BE CUT DOWN 21112026.mov"
  The voiceover finishes saying sufficient number of lifeboats, Quite a bit of pause before the left screen with the
  painting comes up, Get rid of the part between one minute and 49 seconds to one minute and 57 seconds, Those frames are
  pointless with the studio and the judge. We can just bring in the painting rather than having the studio and the judge.
  But everything stays aligned with the sound design. I simply mean that having those few seconds as the painting is better
  than to have the judge and the studio. In terms of your diagnosis and how to fix things, you will have to make that
  decision because I lose track when you say V5, B1, or things like that. I have connected to a new Higgsfield account. If
  you must use it, check if the connected account is running, Whatever makes it cheaper and better, but those issues
  absolutely have to be sorted"
  (DECISIONS: new mix = the 21112026 .mov; review 1:49-1:57 shows the LEFT painting instead of studio + judge, sound
  timing unchanged; Claude decides the fix; credits allowed on the new account if that is better; talk to him in plain
  words, no take codes.)
- 2026-11-21 (M10c): "Ping me when the review is ready and open in explorer" (PushNotification when the FLOW3 review is
  checked and Explorer is open.) Asked what 4K of the updated show files will cost (answered ~130 cr for the three court
  beats, ~150-180 with the court backup loops; not approved). Then: "Because I need to keep at least 1500 hf credits after
  this project is finished" (DECISION: hard floor 1,500 cr on the new account; 3,000 now, so at most ~1,500 more for
  everything left, 4K included.)

- 2026-11-21 (M10e): FLOW5 review built (b5 FLOW5 FULL, b3 FLOW3, b7 FLOW5, Darren uncut mix), checked; waiting for Homie notes. No upscale or promotion without his yes.
- 2026-11-21 (Homie, on the FLOW5 review, verbatim): "at 3:27 you can see the paper in hand morphe and change direction,
  very obvious flaw. then he proceeds to hit himself in the head with the gavel. May be having him do nothing or just
  continuing the reading/holding paper is the way? What do you propose because this wont do. 3:38 there is a sharp
  transition where you see the silhouette change shape. 4:00 hits himself in the head again! the framerate at 5:23 area
  feels off, is everything right here? 5:30, I can see a sharp cut to another silhouette, because we are so close, we can
  see it more clearly. 5:35, sharp cut and hits himself in the head again. We have gone through so many iterations,
  credit spending and yet something so simple and relatively easy to do is turning out to be such a tedious and low
  quality output. I need to you rethink, replan and critically audit this and fix all this."
  (FLOW5 REJECTED. He wants a critical audit, a new plan, a proposal, then the fix. He floats: judge does nothing / just
  keeps reading or holding the paper. The gavel-crosses-the-head moment, which M10d/M10e called "part of the approved
  strike", reads to him as the judge hitting himself: that is a flaw in the stitched result.)
