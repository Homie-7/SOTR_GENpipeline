# Resume the S5 cannon work on another computer, off the T9 (F58, 2026-11-26)

The T9 (`SOTR/HF/` on the drive) holds a git clone of this repo (`SOTR_GENpipeline/`) and a copy of the media
(`SOTR_MEDIA/`). Everything the cannon fallback script reads is on it (checked by sha256 with `tools/t9_sync.py`).

## Steps

1. Plug in the T9. Open a terminal in `<T9>/SOTR/HF/SOTR_GENpipeline`.
2. Run `git pull` (gets any newer commit from GitHub; the T9 clone is already current at the time of this note).
3. Point the scripts at the T9 media (the default path is the PC's `C:/Users/Homie/Documents/SOTR_MEDIA`):
   - Windows PowerShell: `$env:SOTR_MEDIA = "G:/SOTR/HF/SOTR_MEDIA"` (use the T9's drive letter on that computer)
   - Mac: `export SOTR_MEDIA=/Volumes/T9/SOTR/HF/SOTR_MEDIA` (use the T9's volume name)
4. Needs: Python 3.11+, `pip install numpy opencv-python`, and `ffmpeg` on the PATH.
5. Render (CPU only, 0 credits; ~6 min for the 4 walls, ~20 min more with `--join`):
   `python tools/cannon_fallback.py "$SOTR_MEDIA/04_WORKING_FILES/S5_cannonball/fallback_v8" --join`
   On the PC, `bash tools/run_watch.sh LOG tools/cannon_fallback.py OUT --join` adds the watchdog and the CPU
   affinity (Windows only). On another computer, run python directly. The script refuses an output folder that
   exists: pick a new name (`fallback_v8b`) for a re-run.
6. The output is written straight to the T9. When back on the PC, copy it to D: with sha256 (reverse of
   `tools/t9_sync.py`: set `SOTR_MEDIA` to the T9 and `SOTR_T9` to `C:/Users/Homie/Documents/SOTR_MEDIA`).

## Where the work stands

Read `docs/HANDOFF-2026-11-26-F58.md` (the task) and `docs/HANDOFF-2026-11-26-F59.md` (the v8 approach), and the
latest F58 notes in `docs/BRIEF-F31-CANNONBALL-BLADES.md`. Homie's F58 ask: L/R/FLOOR smoke follow the CENTRE's
speed and saturation curve over time (v8 in `tools/cannon_fallback.py`). The render log prints a "v8 CURVES" table;
L/R/FLOOR must track CENTRE within ~10%. Promote nothing.
