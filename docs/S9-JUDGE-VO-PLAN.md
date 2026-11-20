# S9 judge to Darren's voiceover: plan (M9q, 2026-11-20). Put to Homie, NOT approved, 0 cr spent.

Inputs: `docs/S9-JUDGE-LINES.md` (his lines, cued per beat-file frame), diagnosis sheets
`04_WORKING_FILES/S9_gen_judge_review/_DIAG_quality_seam_{1_asbuilt,2_fixtest}.png` (+ `_DIAG_seamtest/`).
Approved strike `fig_SOTR_judge_strike_s9_v1` unchanged, keyline kept; opaque warm blended look (never pitch black).

## Quality drop + seam: script fixes, 0 cr (diagnosed, measured)
- Cause 1 (the drop): our `compose_opaque` closeness blur. Strike ends sharp (edge 5.6 px); RETURN ramps the blur
  to "far" in half a second, and the idle sits at the far blur (edge ~18 px, 3.4x softer). Not the 720p source
  (the threshold equalises them; 1080p buys ~2%).
- Cause 2 (the frame switch): the 2-frame crossfade from the frozen f96 hold into RETURN flips the shape in one frame.
- Fix: the generated frames get ONE steady blur level (recommended: middle, ~10 px edge, like approved f67), eased
  over ~1 s out of the strike and ~1 s into f40; the crossfade is replaced by an eased shape match (test: join
  IoU 0.967 -> 0.992, biggest jump 1.0 -> 0.30 px, inside normal motion). His approved strike frames untouched.
  Decision for Homie: middle (recommended) / fully sharp (1.0; idle edges look cut-out) / leave as built.

## Performance per beat (motivated, not word by word)
- b3: strike on the knock -> RETURN -> READS his findings (looks up to the court / back to the paper, no nod,
  no sigh, feet planted) to f706 -> STILL (breathing only) to the end, f960.
- b5cut: strike f25 ("Two") -> RETURN -> reads -> on "Order! There will be order" (f428) he brandishes the gavel
  up and HOLDS IT ALOFT (new RAISE-ORDER) -> strikes on "Three" (f546, the existing knock) -> RETURN -> reads ->
  "Order! Order! Listen out! Get the traitors out of the court!" (f867-1009): gavel-hand jabs, then a sweeping
  "get them out" wave (new GET-OUT) -> reads -> RAISE -> strike f1278 on "Order!", final "Order!" (f1342) under the
  held gavel -> RETURN -> STILL to the end.
- b7: strike f23 -> RETURN -> reads -> RAISE -> capper strike f388 (as shipped) -> black.
- The v3 idle (sharp nod, lean, leg shift) goes. Existing RETURN (v4) and RAISE (v5) bridges stay.

## Takes (one job at a time, look at each before the next)
Common: Seedance 2.5 (seedance_2_5) · omni_reference · 9:16 · 720p · bitrate standard · batch 1 · sound ON ·
rest pose = `S9-CRT-IDLE_v1_probe_LASTFRAME.png` (upload d0876d26). 7 cr/s at 720p (LOG: 35/5 s, 105/15 s, 28/4 s).
| # | take | start / end image | duration | cr |
|---|---|---|---|---|
| A | v6 READ: reading while he speaks; look up to the court / back to the paper; breathing; no nod, no lean, feet planted | rest / rest | 20 s | 140 |
| B | v7 STILL: after the dialogue; calm hold at rest, breathing only, head to the paper | rest / rest | 11 s | 77 |
| C | v8 RAISE-ORDER: head up to the court, gavel brandished up and held aloft, alive | rest / approved f40 | 6 s | 42 |
| D | v9 GET-OUT: head up, two gavel-hand jabs (no blow), sweeping wave to the side, back to reading | rest / rest | 7 s | 49 |
Total 308 cr. Balance 338.3 -> ~30.3. M9 judge total 308 -> 616 (agreed ~350). Order: A first (proves the no-nod
idle); if A fails, stop and report before B-D.
Speaking-idle need ~41.6 s (b3 20 s, b5 7.8 + 5.3 + 5.8 s, b7 2.8 s): A's 20 s covers b3 without repeating; the b5/b7
pieces take different sections, 1-2 minutes apart.

## REVISED after Homie (M9q, see BRIEF): LEAN PLAN, 196 cr
- RUN: A v6 READ 20 s (140 cr), then B v7 STILL 8 s (56 cr). One at a time; look at A before B.
- A's prompt: town-crier reading, breathing, head down to the paper and up to the court (forward) a few times at
  steady, unhurried moments; NO nod, NO lean, NO step or weight shift, feet planted; ends on the rest pose.
  Place A's look-ups on b5 "Order! There will be order" (f428) and "Order! Order! ... Get the traitors out" (f867-1009).
- B's prompt: calm hold at rest, breathing only, head down to the paper. b3 still (10.6 s) = B 8 s + A's quiet end.
- DROPPED: C (existing RAISE v5 starts f436, lift lands under "There will be order"), D (gesture risk; Homie: not needed).
- Script fixes (0 cr): one steady middle blur for generated frames (eased ~1 s at the strike ends), eased shape match
  instead of the 2 f crossfade (see _DIAG_ sheets). Then rebuild the 720p review, look, show in Explorer.
