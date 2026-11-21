# S9 judge, FLOW5 audit (M10f, 2026-11-21, POST/script, 0 cr)

Checked every frame at 24 fps (sheets in the M10f scratchpad; re-make with `tools/_joinsheet_m10d.py`), plus a frame-difference
scan of the whole of b5 and b7 and of review 5:15-5:45 (duplicate / dropped frame test).

## Homie's timestamps -> cause
Review layout: C b5 from 189.75 s, C b7 from 322.92 s (`_LOG_review_FLOW5.txt`).

| Homie | where | what is on screen | cause |
|---|---|---|---|
| 3:27 paper morphs + flips | b5 436-466 | read -> raise join; scroll changes shape over ~30 frames | distance-field morph between two different generated takes |
| 3:27 then hits his head | b5 540-547 (3:32) | in 2-3 frames the front-facing judge becomes a DIFFERENT figure seen from behind, arm and gavel drawn across the back of his head, light outline inside the body | the old "approved strike" cut-out is a different drawing from the generated judge; dropped in mid-raise |
| 3:38 shape change | b5 ~590-620 | back-view strike figure flow-warped back into the front-facing judge | same mismatch, reverse direction |
| 4:00 hits head again | b5 1168 morph + 1272-1279 swap (4:03) | as 3:27 | as 3:27 |
| 5:23 frame rate | b7 0-23 | NO dropped or duplicate frames (file and review both clean, 24/1). The beat opens with the arm hanging up and drifting slowly for ~19 frames, then the whole strike snaps in 2-3 frames into the back-view figure | slow-then-snap motion of the mismatched strike reads as a stutter |
| 5:30 cut to another silhouette | b7 90-100 (5:26-5:27) | back-view figure warps into the front figure, ghost gavel across the face at 97-98 | strike -> return join |
| 5:35 cut + head | b7 278-312 morph (scroll lumps), 385-390 swap (5:39) | as 3:27 | as 3:27 |

## Why our checks missed it
- Joins sampled every 2nd frame at +-6 and the rest at 6 fps; the swap takes 2-3 frames.
- The strike frames were exempt as "approved", so the switch to a different figure was never judged as a join.
- Checks looked for edge/blob artefacts, not "does this read as one person doing one thing".

## Root cause
Three different drawings of the judge (generated read take, generated raise take, old approved strike cut-out) are stitched
together 4-8 times per appearance. Every stitch is a morph or a swap. No join method fixes a swap between two different figures.

## Options put to Homie (M10f)
A (recommended, 0 cr): no raise / strike on screen. Each appearance = the silent read take (v8, 15 s, start=end on the same rest
  frame, so its loop point is near-identical frames), head turns only, gavel knocks in Darren's sound only. Only joins: v8's own loop
  point. Check every frame of every loop point at 24 fps before showing.
B (~70-105 cr per take): one uncut generated front-view take holding read -> strike -> back to read, used for the strikes; still
  joined to the read at the rest pose. Settings would be: Seedance 2.5, omni_reference, start=end `S9-CRT-IDLE_REST_16x9.png`,
  16:9, 720p, 10-15 s, standard, batch 1, sound OFF (7 cr/s: 10 s = 70 cr, 15 s = 105 cr). Risk: the model's own strike may still
  cross the head; a strike can't be checked before paying.
C: A now; B later only if he wants a strike seen.
WAITING for Homie's pick. Nothing built.
