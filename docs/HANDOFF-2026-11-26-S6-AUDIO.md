# Handoff 2026-11-26 — S6 audio sync check (Mac on T9, POST, 0 cr)

Homie, 26 Nov, verbatim: "New task, there's been an issue. I'm told that the scene 6's latest renders don't match
the latest audio from Darren. Can you find out what's happening"

Job: FIND THE CAUSE and report it to Homie in STE. Do not render, re-time or spend credits without his yes.

## Found so far (old chat, before handoff)
- The only S6 French audio on the T9 is `Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` (121.25 s, 23,469,730 bytes).
  Two copies, same sha256 (46e4ba2d76d7069c…): `/Volumes/DMD T9/SOTR/Meeting notes/Nov 2026/` (17 Nov) and
  `/Volumes/DMD T9/SOTR/HF/Final changes/` (20 Nov). `tools/s6_fr_review.py` line 27 points at the `Final changes` copy.
- No newer S6 audio is on the T9. `HF/Final changes/Final audio/` (24 Nov) holds only `the judge CUT DOWN 23112026.mov` (S9).
  So if Darren sent a newer S6 track, we do not have it yet (WhatsApp / email / Google Drive?).
- `docs/S6-FR-CUES.md`: TMAP built from that wav (faster-whisper). It notes the track still had 3 English lines.
  CLAUDE.md M8 (17 Nov) said "Next: the client's French-only audio -> retime". F25 muxed `*_FRsound.mov`; F28 promoted
  S6 French to `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/S06_Napoleonic-wars/`.

## Next checks
1. Ask Homie (one question) which file is "the latest audio from Darren", and where it is, if it is not on the T9.
   Also check Gmail / Google Drive connectors read-only for a Darren S6 audio after 17 Nov.
2. Check the promoted S06 files: duration (2910 f?), fps, the embedded audio. Correlate the embedded audio with the wav
   (`tools/build_audio.py` style). Lag 0 + same length = renders match the 17 Nov wav.
3. If Darren has a newer track: compare it with the 17 Nov wav (length, word times by faster-whisper vs the TMAP knots).
   Report what moved. A fix = a new TMAP + `render_s6.py --retime-fr` re-render (0 cr, script) on Homie's yes.
4. Log one LOG row; commit with the HEAD-EOL method (see CLAUDE.md / earlier handoffs); push.

## Other open items
- PC sync of the 26 Nov S5 files: `docs/HANDOFF-2026-11-26-F68-PC-SYNC.md` (Homie does it on the PC).
- Old chat local_19fb2067 must be archived from the sidebar by Homie (the app refused the archive).
