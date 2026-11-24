# HANDOFF 2026-11-24 — FINALS (S9 judge + S6 French, 4K)

From: RAFT7 star chat (handed off at ~162k tokens). Mode for the new chat: **POST**.

## THE QUESTION AT THE TOP

Homie wants **the final plan first**, then the renders. Do not render, upscale or promote before he says yes to the plan.

## Homie's message, verbatim (24 Nov 2026)

> The final audio has been provided from Darren "G:\SOTR\HF\Final changes\Final audio\the judge CUT DOWN 23112026.mov" I was told that there are no beats or key points that have been altered or changed, so our render will still stand as is. For the French wars scene, which is, I think, S6, everything has been approved. Everything also has been approved for this scene. So, I believe we are good to go with the 4K renders upscale map to alpha, everything else that's discussed. Tell me what the final plan is, and then we will get to rendering. Obviously, verify the sound in case there is any discrepancies, but should be okay

## What to do, in order

1. Read `CLAUDE.md`, then the judge handoffs `docs/HANDOFF-2026-11-22-EXT5.md`, `-M10p.md`, `-S9darren.md`, `-EXT4.md`, `-EXT4b.md`,
   and the S6 notes `docs/HANDOFF-2026-11-17-M8l.md`, `docs/BRIEF-MEETING8.md`, `docs/S6-FR-CUES.md`.
2. **Verify Darren's final audio** (`G:\SOTR\HF\Final changes\Final audio\the judge CUT DOWN 23112026.mov`) against the approved
   EXT5 review `04_WORKING_FILES/S9_gen_judge_review/S9_GENJUDGE_3wall_review_EXT5.mp4` (351.17 s): duration, cross-correlation
   lag (expect 0), the cut points (EXT4 cuts 183-189 s and 248-290 s), the gavel strike / b5 / b7 hit positions. Use the method of
   `tools/build_audio.py` / `tools/s9_darren_review.py`. Report any discrepancy with timecodes. Copy the file into the repo's media
   area first (never work on G: directly; checksum the copy).
3. **Write the final plan** for Homie (STE, short): every deliverable file, its source, its tool + flags
   (`tools/court_ext.py` env `EXT_E5=1`, `tools/s9_darren_review.py --e5`; `tools/render_s6.py --retime-fr` + the final/4K path,
   map dissolve to alpha as ink, RIGHT fleur-de-lis flag), resolution 4K 3840x2160, codec, sound (Darren's final mix embedded),
   clean master in 03 + edge version in `1_PLAY_THESE_IN_ORDER/`, superseded files to `04_WORKING_FILES/superseded/`.
   For any **paid upscale** give the full settings block (model, mode, reference, aspect, resolution, duration, quality, batch, sound)
   and the credit estimate (earlier estimate ~130 cr for the court beats; balance 2,443). Ask before any run over ~100 cr.
   S6 still waits on "the client's French-only audio" per M8; check whether that audio has arrived, or ask.
4. After Homie's yes: render with affinity FFFF3FFF, a watchdog on every detached render, `_tmp_` names, then audit, promote,
   REGISTER/LOG/NEW-SESSION/CLAUDE.md, commit, push, T9 backup (git pull in `G:\SOTR\HF\SOTR_GENpipeline` + sha256 copy of media).

## Open items carried over

- **Blades v2 style frames** (S9 raft b10): 3 frames in Blender 5.2 (A lamp shadow, B rim-lit arm, C smear glimpse), all three walls,
  correct grips, every tip on Agnes (bottom centre), arms only from top / top corners / outer sides. Cap 60 cr (0 spent). See
  `docs/HANDOFF-2026-11-22-RAFT6.md`. Not started. After the finals.
- **Water options**: DONE (A default, B/C/D in `5_FLOOR_only_if_a_floor_projector/S9_raft-water_OPTIONS_frame-rate/`, D preferred). Commit dd4ff9b.
- **Archive**: the old RAFT6 chat (local_bad01823) and local_ad693359 when idle (archive only). This RAFT7 chat is retitled "(old)".

## Rules to keep

STE replies. Never put media in the chat; open the folder in Explorer. Only what is asked; ask before upscales and promotions.
No hard deletes (`_DELETE_ME_` bin). The deny list is final.
