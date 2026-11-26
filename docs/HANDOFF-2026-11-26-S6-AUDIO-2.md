# HANDOFF 2026-11-26 — S6 audio mismatch (part 2)

Mode: POST, Mac on T9, 0 credits. Replies to Homie in ASD-STE100 (see ~/.claude/CLAUDE.md).
NOTE: at handoff time the T9 drive ("/Volumes/DMD T9") was NOT mounted. Ask Homie to mount it if it is still missing.
Copy this file to `docs/HANDOFF-2026-11-26-S6-AUDIO-2.md` in the repo when T9 is back.

## Homie's task (verbatim)
"New task, there's been an issue. I'm told that the scene 6's latest renders don't match the latest audio from Darren. Can you find out what's happening"

## Homie's answer (verbatim, 26 Nov)
"'/Volumes/DMD T9/SOTR/HF/Final changes/Final audio/the judge CUT DOWN 23112026.mov' This was the latest audio that darrin shared."

## What is proved (part 1)
- Promoted show files `SOTR_MEDIA/01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars/S6_{CENTRE,LEFT,RIGHT}_wars.mov`
  (25 Nov 22:13, ProRes 24 fps, 2910 f, 121.25 s, pcm_s24le 48k 2ch) match
  `HF/Final changes/Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` (121.25 s, sha256 46e4ba2d76d7069c…) exactly:
  lag 0 on all 3 walls, r = 1.0 in every 10 s window after 2 s. Only difference: the approved 2 s fade-in (F43/F44).
- That wav is the one Darrin sent on 17 Nov (Gmail "War sequence AUDIO": "use it as a guide for your visual pacing").
- Drive has no newer "Sc 6 wars" file. Other newer Darrin files: "Map to ship 24112026.mov" (23 Nov), "ship 25112026.mov/.wav" (24 Nov).
- 1080 fallback S06 copy: not checked.

## Next steps
1. Probe `the judge CUT DOWN 23112026.mov` (ffprobe length, streams). Its name says S9 (judge), not S6. Find out if it holds S6 wars audio (listen-check by xcorr against the S6 wav).
2. If it holds S6 audio: decode mono 8 kHz f32, FFT cross-correlate against the S6 wav and the show files, plus per-window corrcoef. numpy venv:
   `/private/tmp/claude-501/-Volumes-DMD-T9-SOTR-HF-SOTR-GENpipeline/828ece47-1c79-43a6-9674-6ec4c13e7215/scratchpad/venv/bin/python -I` (system python3 has no numpy). Report offset and timing changes.
3. If it is S9 only: tell Homie in STE that this file is the S9 judge audio, that the S6 renders match the only S6 audio Darrin sent (17 Nov wav), and ask which S6 audio the person who reported it means.
4. Do not render, re-time or spend without Homie's yes. Copy media, never delete.
5. Add a LOG.md row, commit only own files with the HEAD-EOL method, push.
6. Archive old chat local_19fb2067 ("(old) ★ SOTR (S5 alternate promote) - handed off 2026-11-26") if stopped; if refused, tell Homie to archive it from the sidebar. Archive the chat that wrote this handoff (local_3fc05c0b's child, "S6 audio" live chat) once the new one runs.
