# S9 judge: M9u diagnosis of Homie's LEAN-review notes (2026-11-20). 0 cr spent. Waiting on Homie's credit OK.

Measured on `S9_b5_CENTRE_court_GENJUDGE_LEAN_DARREN-CUT.mp4` and the sources (scratch scripts, 0 cr).

| Note | Physical cause (measured) | Fix | Credits |
|---|---|---|---|
| Quality jump strike vs idle | Contrast is the same (figure core 22-28, field 115-134). The gap is edge sharpness: strike frames at the lens are composited at closeness 1.0 (edge grad 113), every generated idle at CL_MID 0.48 (grad ~80). The strike is also native 1080x1920 with a keyline; the idles are 720p upscaled x1.5. | One sharpness for the whole judge: idles near 0.85-1.0, with a contour clean-up (blur + re-threshold of the 720p mask) so the upscale does not stair-step; strike frames unchanged. | 0 |
| Cut to a zoomed-in image at slam 3 | `court_gen.KNOCKS`: b5 switches Q2 (s 0.50) -> Q3 (s 0.65) on the knock at f546, a +30 % scale jump; b7 opens at Q4 (head/chest push-in) and cuts to Q5 (gavel fills the wall) on the capper. That is the old LOOK D8 "hard jump per strike" design. | One size per beat, never changed inside a file; b7 at a floor size, capper without the Q5 cut. | 0 |
| Hard cuts (e.g. just before slam 3) | The f96 hold (24 frozen frames) then RETURN; the RAISE (U) -> approved f40 join; idle segments jumping back to an earlier R6 frame. Plus the scale jump. | Rebuild with no freeze, longer flow-warp joins, no backward jumps in the idle (one continuous take per stretch). | 0 |
| Gavel cut off at the frame edge | The sources are 9:16. The approved strike's gavel leaves its frame at A f42-48 (right) and f48-50 (top); the RAISE bridge U at f32-45 (left). On the 1800-wide wall the 9:16 frame is only 540-700 px wide, so its edge is a straight line through the gavel. R6/R7/T never touch an edge. | A (approved, animation unchanged): rebuild the clipped gavel tip from a rigid gavel template taken from an unclipped frame (script). U: same, or regenerate at 16:9 (4 s = 28 cr). | 0 (or 28) |
| Mouth not in sync | The v6 READ take was generated with sound ON; the model gave him jaw motion at its own times. | Mouth absent (Homie's second option): new take with lips sealed. | needs generation |
| Breaths / sighs too strong | v6/v7 shoulder heave; v6 rest frames are 2-7k px off f0 from breathing alone. | Prompt "barely perceptible breathing"; script can also damp it (partial warp toward a rest frame). | 0 partial / in the new take |
| Reading idle, not breathing and waiting | v6/v7 are mostly a held pose with two head lifts. | New READ take: eyes/head follow the lines down the page, small head tilts, paper shifts, maybe a page turn, mouth closed, feet planted, rest-to-rest. 16:9 framing so nothing ever crops. | 15 s = 105 cr (7 cr/s, 720p) |

Proposal put to Homie: 0-cr rebuild of everything above now; ONE new 15 s reading take (105 cr, balance 142.3 -> ~37) after his OK; the U regen (28 cr) only if the template fix on U fails.
