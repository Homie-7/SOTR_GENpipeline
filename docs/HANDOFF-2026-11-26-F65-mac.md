# HANDOFF 2026-11-26 F65 (Mac on the T9, POST/script, 0 cr)

## Homie's open question (ask FIRST, in STE)
Promote the v10 4K files to the show as they are, or first fix the CENTRE (darker smoke, embers matched; 0 cr script change, ~10 min)?

## State
- v10 (`04_WORKING_FILES/S5_cannonball/fallback_v10/`, `--take-mode none`, committed in 7bf652e) CHECKED: no 7 s change (CENTRE frame diff f140-265 max 3.46 at f140, median 0.88). Seams L|C 6.03, C|R 4.88, C|F 6.88.
- Weak point told to Homie: CENTRE = real v4 smoke (clear cloud shapes, top edge, big embers) beside soft script smoke on L/R; at f165 mid luma C 55 vs L 36 / R 34; equal by ~f240. Strip: `fallback_v10/strip_LCR_f140-220.jpg`.
- 4K: `fallback_v10_4K/S5-CANNON-FALLBACK_{LEFT,CENTRE,RIGHT,FLOOR}_4K.mov` = ffmpeg lanczos 3840x2160 from the 1080 mp4, prores_ks profile 3 (422 HQ) yuv422p10le, 25 fps, 316 f, pcm_s24le 48k; `_SHA256.txt`. Camps show files are 1920x1080 ProRes 25 fps; S6 is 4K 4444 24 fps.
- Finder was opened on the 4K folder for Homie (open -R).
- Old star chat local_e258bbbd would not archive (live work). Archive it if it is idle.

## Next
1. If Homie says promote: copy the 4 files to `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S05_the-camps/` with show names, no version (e.g. `S5_<WALL>_cannon.mov`; ask nothing more than he gave), update `00_READ_ME_FIRST.txt` + `_SHA256.txt`, REGISTER row. Copy to D: later on the PC with sha256.
2. If "fix CENTRE": in `tools/cannon_fallback.py` (CRLF), dim the CENTRE smoke mid band toward L/R luma over f113-240 and match ember radius across walls; re-render v11 (~5 min), recheck, re-run the 4K step.
3. Wrap: LOG/REGISTER/NEW-SESSION/CLAUDE.md with HEAD EOL only (hash-object + update-index --cacheinfo; never commit the ~327 CRLF-only files).

Mac setup: `export SOTR_MEDIA="/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA"`; venv `/private/tmp/claude-501/-Volumes-DMD-T9-SOTR-HF-SOTR-GENpipeline/828ece47-1c79-43a6-9674-6ec4c13e7215/scratchpad/venv/bin/python` (numpy, opencv).
