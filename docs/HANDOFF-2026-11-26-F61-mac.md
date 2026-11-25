# HANDOFF 2026-11-26, F61 (Mac, off the T9) -> next chat

Read `CLAUDE.md`, `docs/T9-RESUME.md`, `docs/HANDOFF-2026-11-26-F60-T9.md`, then this file. Mode POST/script. 0 cr. Promote nothing.
Task (Homie F58, verbatim): "match the speed and saturation of left bottom and right with the center".

## Mac setup (done once, scratch venv may be gone)
- `export SOTR_MEDIA="/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA"`. System python is 3.9; use a 3.12 venv:
  `uv venv <dir> --python /opt/homebrew/bin/python3.12 && uv pip install --python <dir>/bin/python numpy opencv-python`.
- A no-join test render takes ~2 min on this Mac (M5 Pro). Logs live next to the output folder (`v8testN.log`).
- `git status` shows ~327 modified files: CRLF/LF only (exFAT + Mac). Content is equal. Do NOT commit them; stage only real files.

## Results this chat (in `$SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/`)
- `v8test3` = test-2 flags + `--front-tau 12`. Front covers LEFT by f136 (was f151). Speed f133-153 L/R/FL 7.0/5.2/1.4 vs C 2.55
  (was 14.9/11.4/1.3); f153-173 L 5.8 vs C 2.7 (R, FL pass). Sat PASS. End speeds = S6. Seams unchanged (5.95/4.37/9.00).
- New flag `--abs-lo` (v8b, `tools/cannon_fallback.py`): before the takeover all walls drift at ramp_lo x CENTRE S6 speed
  (absolute), then each eases to its own S6 speed. `v8test4` = test3 flags + `--ramp-lo 0.25 --abs-lo`: NO change on LEFT (~6).
- Dense measure (`tools/flow_dense.py <dir> 133 173`, block-match every 2 f): LEFT dx -11,-11,-7,-3 (burst out) then steady +5..+7;
  CENTRE +2..+3; RIGHT +7,+9 then +1..+3; FLOOR +0..+1 rising to +5. LEFT match is weak (smoke std 8.7, best/zero err ~close).
- Harness (`tools/flow_parts_test.py`, run from repo root with SOTR_MEDIA set): the SMOKE FIELD alone, with the exact burst +
  `--abs-lo` drift, moves L/C/R/FL at 2.8/3.4/3.3/3.2 px/f in t=22-62. So the extra LEFT motion is NOT the field/drift/burst.

## Open: what makes LEFT read +6? Suspects, in order
1. Embers (LEFT/RIGHT 60->260 + 40 burst, bright points on low-contrast smoke dominate the SAD block-match). Test: env/flag to
   draw no embers, re-measure. If it is the embers, it may be a MEASURE artefact (mask bright points in flow_stats), not motion.
2. The shared shake (to ~f152) on a low-texture wall.
3. The front mask fm edge on the far-left part of LEFT (rf - dist small there).
Decide: if the eye sees no extra LEFT motion (frames looked steady to me at f150/153, f160/163), fix the MEASURE, not the picture.
Then the final: test flags + `--join` -> `fallback_v8` (PC also made one: compare, rename the PC one `fallback_v8_pc`).
Then the wrap list in `docs/HANDOFF-2026-11-26-F60-T9.md` step 4.
