# HANDOFF 2026-11-22 RAFT4 (S9 raft: blades animated test v1 built, waiting for Homie's notes)

QUESTION FOR HOMIE (at the top): his notes on the blade animated test v1 (timing, size, how much light, how many stabs).

Read first: `CLAUDE.md`, `docs/BRIEF-S9-RAFT.md` (his words verbatim; last section = blade direction),
`docs/RESEARCH-S9-RAFT-BLADES.md`, then `docs/HANDOFF-2026-11-22-RAFT3.md` for the water state.

State:
- BLADES v1 (0 cr): `tools/blade_anim.py OUT [--seed N] [--stills t1,t2]` imports the period shapes from
  `tools/blade_frames.py`. 28 s @ 24 fps: phase 1 close in (single-wall emerges 1.5-13 s), phase 2 sudden attacks
  (seeded stabs, 2 walls at once or 2 arms ganging on one wall, never 3 walls lit; asserted), phase 3 four still
  images = four stabs (C briquet, L clasp knife, R dirk, C boarding sabre), then black. Walls dark; a dim cold moon
  pool + ICE edge glint only round the glimpse. KSCALE 1.45 (shadow size), POOL_PEAK 0.30.
- Output: `SOTR_MEDIA/04_WORKING_FILES/S9_raft/blades_anim_v1/`: `S9_b10_BLADES_{LEFT,CENTRE,RIGHT}_anim_v1_ALPHA.mov`
  (ProRes 4444 straight alpha, 1440/1800/1440 x 1080, no sound) + `S9_b10_BLADES_3wall_review_v1.mp4` (1920x1080)
  + `schedule_v1.txt` + `_still_*.png` test frames. Check the render log `render_v1.log` says DONE.
- WATER v2: PERFECT LOOP, PROMOTED (Homie's yes). v1 had a 1-frame hitch (step 1.998 rounded); `raft_water.py` now locks an
  integer step. Show: `01_FINAL_FOR_SHOW/5_FLOOR_only_if_a_floor_projector/S9_b1-and-b10_FLOOR_raft-water.mov` (63 s = 6 loops,
  silent 48 kHz) + `2_BACKUP_LOOPS_for_operator/..._HOLD_loop.mov` + `03_CLEAN_MASTERS_no_edge/..._loop_CLEAN_4K.mov`. Read-me,
  REGISTER, LOG updated. sha256 verified. T9 copy at the wrap.
- Stabbing budget (Homie): max 50-60 cr. 0 spent. Script route first; full settings block before any paid run.
- Committed at the RAFT5 wrap; media backed up to the T9.
- S9 judge EXT5 review still WAITING for Homie's notes (`docs/HANDOFF-2026-11-22-M10p.md`).
- Rules: no credits/upscales/promotions without his yes; Explorer, no media in chat; affinity FFFF3FFF + watchdog
  (launcher needs `powershell -ExecutionPolicy Bypass -File`). Balance 2,443 cr, 0 spent.
- Old chat to archive: "(old) SOTR S9 raft blades anim - handed off 2026-11-22".
