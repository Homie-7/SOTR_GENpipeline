# HANDOFF 2026-11-22 RAFT6 (S9 raft: water motion tests rendering; blades v2 plan set)

Star chat RAFT6 started 22 Nov. Remote Control on. The old chat "(old) SOTR S9 raft blades anim - handed off 2026-11-22"
(local_ad693359) did NOT archive: the app says it still has live work (a Remote Control client). Try again; archive only.

## Task 1, WATER STUTTER (in progress, 0 cr)
- Answer for Homie: 24 fps. `raft_water.py` v2 = every 2nd frame of the 59.94 fps drone clip (speed 0.8). Cadence even.
  Cause = 24 fps judder of sharp, fast-shutter frames with no motion blur. On a 60 Hz projector 24 fps also gets 3:2 pulldown.
- New `tools/raft_water_motion.py` (imports `grade()` from raft_water.py, same source span src 0..~599, same 2 s smoothstep
  wrap). Launcher `tools/_launch_water_motion.ps1` (affinity FFFF3FFF), watchdog `tools/_watch_water_motion.sh`.
- Three 4K ProRes loop tests rendering to `SOTR_MEDIA/04_WORKING_FILES/S9_raft/water_motion_test/` (logs `_LOG_<tag>.txt`):
  B24blur = 24 fps, shutter 2 (mean of src 2k, 2k+1), 252 f / C48 = 48 fps, every source frame, 504 f /
  D5994flow = 59.94 fps, speed 0.8, DIS optical-flow in-betweens, 629 f. A = the approved v2 master (no re-render).
- DONE 22:12: wraps clean (A 1.03, B 1.00, C 1.13, D 1.13 x median step); review_1080 + grid built, folder opened for Homie. WAITING for his pick + the floor projector rate.
  (2) look at them yourself (contact sheet + flow artefacts on D, foam ghosting); (3) make 1080 review files, each at its own
  rate, 2 loops, same names + a 2x2 grid (A/B/C/D) at 59.94; (4) open the folder in Explorer for Homie and ask him to pick.
  Note to Homie: ask what rate the floor projector / media server runs (60 Hz -> D is the smooth one; 48 judders on 60 Hz).
  No promotion without his yes; on yes: same show name, old file to `04_WORKING_FILES/superseded/` with v2 added.

## Task 2, BLADES v2 (plan; nothing built yet, 0 of 60 cr)
- v1 faults seen on `blades_anim_v1/_stills_sheet.jpg`: tube arms with flat ends, blade angles random, one arm from the
  bottom-right with the blade pointing up and back. Keep the v1 WIPE (glimpse timing/schedule).
- Geometry rule: aim point = Agnes at bottom centre (on the floor). CENTRE wall: blades point down to bottom-centre.
  LEFT wall: point down-right. RIGHT wall: point down-left. Entry only from top, top-outer corner or the OUTER side
  (LEFT wall: top/top-left/left; RIGHT wall: top/top-right/right; CENTRE: top, top corners). Never from the bottom.
- Grip rule: blade in the fist, line of the blade through the wrist line, tip to Agnes. Two true grips: REVERSE (ice-pick,
  blade out of the little-finger side, overhead downward stab: daggers, clasp knife, bayonet held as a spike) and
  SABRE/HAMMER thrust (briquet, boarding sabre: blade out of the thumb side, wrist cocked so the blade continues the forearm).
- Route found: Blender 5.2 is installed (`C:\Program Files\Blender Foundation`). Plan = real 3D shadow: an organic arm
  (skin-modifier skeleton shoulder-elbow-wrist + sculpted fist, torn 1816 shirt/coat sleeve), the period blade extruded
  from `tools/blade_frames.py` profiles, a near lamp (Fantasmagorie "grow") casting onto a wall plane, shadow catcher
  -> alpha. Real perspective, soft penumbra, motion blur. 0 cr. Generated route (image silhouettes / Seedance) only if
  Blender fails; full settings block first, cap 60 cr.
- Order (Homie: "think about all of this, don't just blindly make something"): (1) reference board with links + a grip/aim
  diagram per wall; (2) 2-3 style frames (e.g. A hard lamp shadow, B moon-rim lit arm out of black, C motion-smear glimpse);
  (3) Homie picks; (4) build v2 on the v1 schedule.

## UPDATE 22 Nov late (RAFT6 -> RAFT7 handoff)
- Water tests DONE and shown (review_1080 + 2x2 grid at 59.94). Homie asked "are they all perfect loops?" -> answered YES
  (wrap / median step: A 1.03, B 1.00, C 1.13, D 1.13). He does not seem to know the projector rate (his words:
  "Know the frame rate of the projector"). Claude recommended D (59.94 flow). WAITING for his pick. On his yes:
  re-render the show file (63 s = 6 loops) + HOLD loop + CLEAN at the chosen rate with raft_water_motion.py logic,
  same show names, old v2 files to `04_WORKING_FILES/superseded/` with `_v2` added, sha256, read-me + REGISTER update.
- Blades v2: refs note committed (`docs/BLADES-V2-REFS.md`). NEXT = 3 style frames (A lamp shadow, B rim-lit arm,
  C smear glimpse) via Blender 5.2 (0 cr), all three walls, correct grips, tips on Agnes. Then his pick.
- Wrap still owed: REGISTER, NEW-SESSION, CLAUDE.md current stage, push, T9 (git pull in G: clone + sha256 copy of
  `S9_raft/water_motion_test/` and anything new).
- Old chats to archive: this one (RAFT6) and "(old) SOTR S9 raft blades anim" (local_ad693359, had a Remote Control client).

## RAFT7 note (22 Nov, late)
- RAFT7 star chat started, Remote Control on, read in. Homie: "We will stop for now ... We will work on this tomorrow."
- Nothing built, 0 cr. Water pick still open. Blades v2 style frames not started (Blender 5.2 at
  `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`; v1 code in `tools/blade_anim.py`, profiles in `tools/blade_frames.py`).
- Not archived yet: RAFT6 (was still running) and local_ad693359 (app: still has live work). Retry tomorrow.
