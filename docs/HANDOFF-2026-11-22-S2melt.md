# HANDOFF 2026-11-22: S2 painting melt, run Plan A (GO given)

Mode: POST/script. Read first: `SOTR_MEDIA/04_WORKING_FILES/S2_painting_melt_plan/BRIEF.md` and `PLAN.md` (section 3).
Homie said "Yes, run Plan A" (~60 cr). Balance 2,475, floor 1,500. Ask before any run over ~100 cr.

## Do
1. `tools/melt_reproject.py video SRC OUT WALL F0 F1 SCALE` for LEFT, CENTRE, RIGHT, FLOOR, all 500 f, scale 1 (native density).
   SRC = `F:\OrCha Drive\SOR DESK BACK UP\RMIT Black Box first show\Final Animations\Painting melt + Ocean loop\paintingMelt_1109.mp4` (read-only).
2. Melt part (f0-175, 0-7 s): retime 25->24 first (keep every frame), pad each surface to 16:9, upload (`tools/put_upload.py` + media_confirm),
   Topaz 2160p (`upscale_video`), one job at a time, download with `tools/fetch.py`, crop back. Test: Topaz job 203db763 = 5 cr / 2.4 s.
3. Sea part (f175-500): Lanczos to 4K locally. Join at a dark frame (6-7 s is dark).
4. Sound from the wavs in the source folder (no audio in the mp4). Composite the true Raft (as S1) on the opening hold, dissolve into the melt.
   Check the melt's frame against S1's frame first.
5. Clean masters only into `04_WORKING_FILES/S2_painting_melt_plan/planA/` (24 fps, ProRes 422 HQ + 1080 copies). No edge, no promotion.
6. Contact sheet, look at it, open Explorer for Homie. Wrap: LOG, REGISTER, NEW-SESSION, CLAUDE.md stage, commit, push, T9 (pull + sha256 copy).

## Known traps
- Topaz outputs 16:9 only and keeps 25 fps. ByteDance drops frames (not used).
- FLOOR frame = 1920x1080 with the envelope 1920x830 centred, black outside. Nadir pinch in the sea: note it, do not fix without Homie.
- T9 git shows `._pack` errors (macOS junk); the pull still works.
- Open questions still with Homie: rest of the cut-off message, sea hold length, floor projector.
- S9 judge EXT3 review is parked, waiting for his notes.
