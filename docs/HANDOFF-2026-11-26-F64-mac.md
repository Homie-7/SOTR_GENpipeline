# HANDOFF 2026-11-26 F64 (Mac on the T9, POST/script, 0 cr)

## Homie's open question (answer FIRST, in STE)
"Will that look accurate enough, will it match with the other screens seamlessly" (about v10).

## Homie's words this round (verbatim)
- F63: "the linear wipe in the center is unacceptable and too obvious. We are almost out of time, what do you recommend we do. wewont do a blend just the scene with explosion that fades to black and then the s6 will come up from fade"
- F64 (on v9): "the fade at 7 seconds is still very obvious. there has to be a better way to do this. we are almost there, try your best and fix it. then we will do a 4k version of it and call it a day"

## State
- v9 (`04_WORKING_FILES/S5_cannonball/fallback_v9/`, `--take-mode dissolve`): REJECTED. The 7 s change = the CENTRE takeover (out f151-201 at 25 fps): real v4 smoke (bright, sharp) swaps for script smoke (soft, brown). No dissolve can hide two different smokes.
- v10 = NO takeover: `--take-mode none` (new, in `tools/cannon_fallback.py`, NOT yet committed at the time of writing; commit it). CENTRE keeps the real v4 smoke to the fade to black (its colour grades to S6 red via gain_c over t 40-140); L/R/FLOOR stay at the v4 speed (no wind ramp). Rendering at handoff:
  `tools/cannon_fallback.py $SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/fallback_v10 --grow 6 --burst 3 --burst-tau 12 --ramp-lo 0.25 --front-tau 12 --abs-lo --take-mode none`, log `S5_cannonball/fallback_v10.log`. If the folder is incomplete, re-run it (about 5 min).
- No JOIN (Homie: no blend; S6 show files already start from black).

## Next
1. Check v10: log seams (v8 had L|C 5.91, C|R 4.38, C|F 9.00), contact.jpg, a CENTRE strip f140-220 (no change at 7 s), the L/R next to the CENTRE (same speed, same colour). Answer Homie's question with the numbers.
2. If it is good: Homie wants a 4K version, then "call it a day". Find how 4K was made for the S5/S6 walls (upscale of script output; 0 cr route first; any credit spend needs his number). Then promote on his yes (show name, no version in the name, old to `superseded/`), sha256, copy back to D: later on the PC (rename the PC's own `fallback_v8` to `fallback_v8_pc` first).
3. Wrap: LOG/REGISTER/NEW-SESSION/CLAUDE.md. Stage docs with the HEAD line endings only (about 327 files show CRLF-only changes; never commit those). The trick: `git hash-object -w` the doc normalised to HEAD's EOL + `git update-index --cacheinfo`.

## Mac setup
`export SOTR_MEDIA="/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA"`; python 3.12 venv at the old chat's scratchpad `.../828ece47-.../scratchpad/venv/bin/python` (may be gone: `uv venv <dir> --python /opt/homebrew/bin/python3.12 && uv pip install --python <dir>/bin/python numpy opencv-python`). `tools/cannon_fallback.py` is CRLF: edit with Edit or python newline=''.
