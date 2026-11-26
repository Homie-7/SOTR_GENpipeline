# HANDOFF 2026-11-26 — S6 alignment (part 3)

Mode: POST, Mac on T9, 0 credits. Replies to Homie in ASD-STE100 (~/.claude/CLAUDE.md).

## QUESTION FOR HOMIE (top)
Where do the show people see the 4K S6 go out of line with the approved review: sound vs picture, or the S7 sea
coming in late? A time in the file helps. Also: may the read-me get an S7 start cue (start S7 at 1:52.5 of S6)?

## Homie (verbatim, 26 Nov)
- "06_s6_wars_french_review was the file they said was good as a composite but they are saying the final 4k renders arent aligning"
- "we added a couple of seconds of fade from black but i was told it all aligns, I believe 2:01 in total. Can you reverify and check"

## Proved (LOG rows a358541, 3354918)
- `the judge CUT DOWN 23112026.mov` = our S9 EXT5 review + Darrin's S9 cut. No S6 audio in it.
- S6 show files, 4K + 1080, 3 walls: 2910 f, 121.25 s (2:01), start 0. Sound = 17 Nov wav, lag 0, r 1.0 after 2 s.
- Fade-in touches frames 0-47 only. Frames 48-2909 are packet-identical to
  `04_WORKING_FILES/superseded/S6_wars_FR_nofade/` on all 3 4K walls (full framemd5).
- Approved review (`tools/s6_fr_review.py`, M9k 20 Nov) = 128.25 s: 121.25 s S6 + 7 s tail. Sahaj's sea plays UNDER
  the ink dissolve from 112.5 s. The 4K show file ends in clear alpha at 121.25 s and the read-me
  (`01_FINAL_FOR_SHOW/00_READ_ME_FIRST.txt` lines 142-152) gives no S7 start time.
  => Prime suspect: if S7 starts after S6 ends, the sea comes 8.75 s later than in the review.
- Other suspect: 4K used `--v6 --v7 --v7-feather --v7-alpha --warm 10`; the review flags are unknown. The review mp4 and
  `render_scale05/` are on PC D: only (T9 folders empty since 25 Nov), so no picture compare on the Mac.

## Next
1. Get Homie's answer. If he says yes, add the S7 cue to the read-me (+ `_SHA256.txt` unchanged, the read-me is not hashed? check).
2. If the problem is picture vs review: get the review mp4 onto the T9 (or work on the PC) and compare cue frames.
3. No render, re-time or spend without his yes.
4. Archive the old chats `local_19fb2067` and `local_3fc05c0b` (refused twice: "live work"); else Homie archives from the sidebar.
