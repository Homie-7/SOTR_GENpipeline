# PLAN: Final changes (client folder `G:\SOTR\HF\Final changes`, 20 Nov 2026). PREP, 0 credits. AWAITING HOMIE'S GO-AHEAD.

Inputs (4 files; nothing else arrived): script `Draft V2.pdf`, `Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav`,
`the judge TO BE CUT DOWN 19112026.mov`, `00_PRODUCTION_REF_Scene7-8.mp4` (15 Nov, "embracingearth.space").
Evidence: `docs/HANDOFF-2026-11-20-M9b.md`, `M9c.md`; measurements below by this chat's helpers (20 Nov).
Show dates: re-ingest Mon 23 Nov, showing Thu 26 Nov.

## S1 / S10 gallery, S4 Alps, S5 camps
- Changed: script V2 = copy-edits only (commas, accents, typos). No content change.
- Do: nothing. Already done: in `01_FINAL_FOR_SHOW`. Open: none. Credits: 0.

## S6 wars (French cut)
- Changed: V2 S6 = Agnès alone in French as one run; Amina's English echoes and the beats/Silence are cut. The three English
  lines that stay ("You're leaving France?", "Where are you going?", "Away from here!") are exactly Darrin's wav.
  Darrin confirmed the wav (same file as 17 Nov, sha256 match): NO new audio is coming.
- Already done: `render_s6.py --retime-fr` (TMAP to the wav, `docs/S6-FR-CUES.md`; L/É/F hold ~9 s, was 17.6, Louise's note);
  RIGHT flag = white with gold fleurs-de-lis on the generated cloth; whole map dissolves to clear alpha as ink.
  Fleur flag + ink stills APPROVED (17 Nov). On-wall words (battles, LIBERTÉ/ÉGALITÉ/FRATERNITÉ, WATERLOO, MONARCHISTES,
  NAPOLÉONISTES) all still in V2: no wall change.
- Do:
  1. Update `LINES` (render_s6.py ~l.109) to V2 text. It feeds ONLY the review caption strip (`caption()`), never the walls:
     drop Amina's V1 echoes, "là où" -> "où", "de liberté, d'égalité et de fraternité", tag the 3 English lines [EN].
  2. Render the review at scale 0.5 (`--final --retime-fr`), detached + watchdog + auto-relaunch, affinity FFFF3FFF, `_tmp_`
     names, into `04_WORKING_FILES/S6_french_review/`.
  3. Build `06_S6_wars_FRENCH_review.mp4` (WhatsApp-style side-by-side, Darrin's wav, V2 captions). Look at it myself, then
     open Explorer for Homie. NOT the 4K/1080/CLEAN finals (Homie 17 Nov). Nothing into `01_FINAL_FOR_SHOW`.
- Ending into Sahaj (the "bird flying into the ship"): no separate new clip exists on any drive (searched G:, D:, Downloads,
  Desktop, Documents). It IS beat A "Fly-in" of the S7-8 production ref (0-58 s: gulls over a sunlit sea, a ship on the
  horizon, flying in to land on the deck grating), and matches frame for frame Sahaj's fly-in we already hold
  (`05_REFERENCE_UPLOADS/S6_handoff_Sahaj/A_flyin_m07v3_unity_03oct_ROOM.mp4`, 90 s; v14's sea was built to his f0001).
  How we finish the map, per the ref:
  - Timing: our S6 ends clear at 121.25 s; Sahaj's clip plays underneath from its frame 1 (ref beat A cue 0:00, 58 s long in
    the ref's cut vs 90 s in his file).
  - Framing: in the ref the fly-in is CENTRE + floor only, the side walls BLACK. Our ink dissolve runs on all three walls,
    so LEFT and RIGHT dissolve to clear over black, CENTRE to clear over Sahaj's sea. Keep as built.
  - Colour at the join: Sahaj's first frame is a bright sunlit sea/sky; our map is a dark engraved ocean. The ink dissolve
    hides the difference (no hard cut). To check in the review composite: show the last 8 s of S6 over Sahaj's f0001 on
    CENTRE so Homie sees the join.
  - Alpha: unchanged (ProRes 4444, fully clear for the last 1 s). Sahaj needs nothing from us.
- Open: (a) confirm beat A of the ref is the clip he meant; (b) review composite with the join over Sahaj's frame: yes/no.
- Credits: 0 (script only).

## S7 ship / S8 aground (the production reference)
- Changed: the client's/Sahaj's 8:12 production reference (15 Nov) lays out S7-S8 on CENTRE + FLOOR only (side areas black):
  A Fly-in, B0 At anchor ("20 s take x4"), B1 Full sail, B1b Big swell ("50 s take; 85 s to record"), B2 Slowing,
  B3 Calm indigo sea ("45 s take; 95 s to record"), CS Sandbank (AI draft), C3 Mast break (AI final 1080p), DN Aground at
  twilight (AI draft), D2 Rowboats leave 1-2 (AI drafts 12/20 Oct), E Ship to raft (15 Nov), F1 Rowboats tow, sabre cut
  (v26 drafts), F1b, H Night, star loop ("hold until cued"). Only Sahaj is named. The deck is a 3D/Unity ship.
- Do: NOTHING until Homie answers. Our S7 work (intro v8, idles v3, 5 light states, seamed walls) is not in this ref.
- Open (for Homie): who owns S7/S8 now (Sahaj, with the "AI" beats by someone)? Are our S7 files dropped? Do the side walls
  need anything in S7/S8 (the ref has them black)? Is the floor projector now confirmed (the ref uses one; `docs/FLOOR-PLAN.md`)?
- Credits: 0 until scoped.

## S9 court / salon / studio ("the judge TO BE CUT DOWN")
- Changed: the picture is OUR S9 preview (`WHATSAPP_3_wall_previews/08_S9_aftermath.mp4`, SSIM 0.99) with a NEW client sound
  mix (our preview had no speech; theirs has the judge recorded in English). Their mix is DIGITAL SILENCE at
  114-117 s (a pause), 250-290 s (40 s) and 354-399 s (45 s, nothing after 354).
  Speech: judge 80-107 (finding One), 191-246 (findings Two-Four, "Order!", "get the traitors out", tow rope), 329-333
  ("loss of life", the verdict). Their sound is on our timeline (lag 0-0.09 s where it matches).
- Read (preview clock -> our files): 250-290 = the tail of court b5 (`S9_b5_CENTRE_court.mov`, 101 s, ~190-291);
  354-399 = the end of salon b8 (16 s) and all of studio b9 (`S9_b9_LEFT_studio.mov`, 40.2 s).
- Do (proposed, after Homie confirms the intent):
  1. Court b5: cut from 101 s to ~60 s (end ~4 s after the last "Order!" at 246), rebuilt from clean, same show name, old to
     `superseded/`. 0 cr.
  2. b8 / b9: either unscored or cut. Do nothing until answered.
  3. A new 3-wall preview on THEIR sound for review only.
- Already done: all S9 files in the show (approved 28 Sep; court behind the parchment, Meeting 6).
- Open (for Homie): is "cut down" = drop the silent stretches (b5 tail; b8 tail + b9)? Is their mix the show sound or a
  sketch? Are the S9 files still triggered per beat (then only b5's length changes)?
- Credits: 0 (re-edit only).

## Credits, total
0 for everything above. Only S7/S8, if it becomes ours, could need generation: scoped after Homie answers.
