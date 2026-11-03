# Handoff 3 Nov 2026: Homie's feedback on the Meeting 6 candidates (POST/script, PC, 0 credits)

State: commit 061bd02 pushed. Candidates are in `D:\SOTR\SOTR_MEDIA\04_WORKING_FILES\` (C: `SOTR_MEDIA` is a junction) and copied to the T9.
Read first: `docs/NEW-SESSION.md` ("THE TASK, RIGHT NOW (3 Nov, wrap)"), `docs/PLAN-MEETING6.md`, `CLAUDE.md` standing rules.
Rules: affinity FFFF3FFF + `_tmp_` names + detached for heavy jobs; never hard-delete (use dated `_DELETE_ME_`); nothing to `01_FINAL_FOR_SHOW`; no upscales unasked; stills to Homie first; sound rides in every file; commit only your own files (end with `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`), push, `git pull` in `G:\SOTR\HF\SOTR_GENpipeline`, copy new media to the T9 with sha256 (`C:\Users\Homie\AppData\Local\Temp\cp.py <folder under SOTR_MEDIA>`), wrap with REGISTER/LOG/CLAUDE.md/NEW-SESSION updates.

## Homie's feedback (verbatim, 3 Nov)

S6 v7 map (`tools/render_s6.py --v6 --v7`, `S6_v7_map_option/`):
- "The zoom and the motion animation is really fast. I quite liked how it was in the beginning. We just needed to zoom in further rather than creating a whole new thing."
- "The line animation that shows the trajectory of the ship starts too late. I don't think we need to wait that long. What we had earlier was pretty good. We just simply needed to zoom in."
- "I wanted to zoom in across all three screens. If we are going to zoom this much, otherwise, the left plane is just black."
- "I don't like the caustics or whatever this transition was, it just kind of looks really ugly and bad."
- "But it did give me this idea of how the map of Africa kind of starts liquefying, and you can see the refractions and everything. Can we do it in a way where the map starts becoming liquefied, and then you see it as if you're seeing it through water, so it's kind of dissolving. Kind of start looking at the water. I can ask Sahaj to keep the camera towards the water only in his render, so that we start with looking at the water and then the camera goes up, looking at the horizon and the sky. That's just a thought. But if nothing, we can at least have the map and everything dissolving, and don't end or freeze the trajectory line like that. I want it to keep animating throughout, at a pace so that by the time the map dissolves away alongside the line, it looks natural and reaches the point we want it to reach WITHOUT actually finishing the whole path."

So for v7 next: (1) go back to the EARLIER (pre-v7-morph) pacing: slower zoom, line starts early, only zoom further; zoom across ALL THREE walls so LEFT is never black; (2) drop the caustic/per-element morph look; replace with the map LIQUEFYING (refraction/warp), seen through water, dissolving into the water; (3) the trajectory line keeps animating the whole time, paced to arrive at the target point as the map dissolves, never finishing the full path, never freezing. Optional note for Sahaj: start his render looking down at the water, then tilt up to horizon and sky (a request for him, not something to build). Stills first, then a short clip.

S9 judge behind paper: "I'm happy with the judge being behind the paper parchment texture. It's pretty good." Approved direction (A1/A2 look). Decide with the A2 clip which level to keep; wiring the other beats (3/5/7) is optional follow-up, ask only if needed.

S1/S10 RIGHT David's Napoleon (`gallery_rehang.py --reshape`, `S1_gallery/3_RIGHT_DAVID_v4/`): "the border of the frame in the bottom is not good at all. See how nice and even the frame is on the left, right, and top, but the bottom is just a flat little weird thing? Every other painting across all walls seemed fine, but this painting's frame is bad. Fix that." Fix the bottom border of the re-sliced frame (the 9-slice `reslice()` bottom strip) so it matches the even left/right/top moulding; rebuild RIGHT LIT/DARK v4, seam pictures and show files; send a still first.

Deliver by stills first, then clips. Report credits (0 expected).
