# S9: the judge's lines against our court beat files

0 cr. Measured 2026-11-20 on the audio of `S9_GENJUDGE_3wall_review_APPROVEDSTRIKE.mp4` (24 fps, 8698 frames, 362.42 s), which carries Darren's mix on our new clock. ASR: faster-whisper `medium`, `language=en`, word timestamps (the S6 recipe used `small`, `fr`). **The judge speaks English** (a first pass with `fr` hallucinated French); no gloss needed. Corrected by energy (10-50 ms RMS) where whisper was unsure (p < 0.5, marked "unsure").

Review time = beat start + frame/24. Beat start on the review: b3 frame 1857 (77.375 s), b5cut frame 4554 (189.75 s), b7 frame 6868 (286.167 s, = mix 322.917 minus the 36.75 s cut). Beat length: b3 960 f (40 s), b5cut 1542 f, b7 480 f.


## b3  (starts at review 77.375 s, frame 1857; file length 40.00 s = 960 frames)

| review s | beat frames | who | text | note |
|---|---|---|---|---|
| 78.92 | 37 | GAVEL KNOCK | strike impact, beat frame 37 |  |
| 80.20-85.40 | 68-193 | JUDGE | "In the matter of the criminal indictment of Capitaine Hugues du Roi de Chaumarin," | start by energy: whisper says 79.6 (p 0.15) but 79.0-80.1 is the knock tail + room; voice onset ~80.2 |
| 86.00-89.08 | 207-281 | JUDGE | "previously Captain of the Frigate La Meduse," |  |
| 89.60-92.70 | 293-368 | JUDGE | "my findings of fact are, one," | "one," 92.32-92.70, whisper p 0.3 |
| 92.86-106.78 | 372-706 | JUDGE | "the accused exercised appropriate leadership and evacuated the passengers and crew in a controlled and timely manner, from the sinking ship to a makeshift raft, in the absence of a sufficient number of lifeboats." | energy drops to the -40 dB room bed at ~106.45 |

**Dialogue ends** at review 106.78 s = beat frame 706 (of 960).

Silences > 1 s (no speech):
- 77.38-80.20 s = frames 0-68 (2.8 s): beat start to first word
- 106.78-117.38 s = frames 706-960 (10.6 s): after dialogue: -40 dB bed to beat end

## b5cut  (starts at review 189.750 s, frame 4554; file length 64.25 s = 1542 frames)

| review s | beat frames | who | text | note |
|---|---|---|---|---|
| 190.79 | 25 | GAVEL KNOCK | strike impact, beat frame 25 |  |
| 190.92-191.68 | 28-46 | JUDGE | "Two," | whisper p 0.09; energy burst 190.3-191.7 confirms |
| 191.98-198.34 | 54-206 | JUDGE | "that the accused, consistent with Regulation 262-B of the French Naval Code," | number/"262-B" unsure |
| 198.94-204.78 | 221-361 | JUDGE | "made adequate provision of food and water for the passengers and crew of the raft." |  |
| 207.60-208.10 | 428-440 | JUDGE | "Order!" (shout, -10 dB) | whisper says 207.86; energy onset 207.6 |
| 208.46-210.62 | 449-501 | JUDGE | "There will be order in the court." |  |
| 212.50 | 546 | GAVEL KNOCK | strike impact, beat frame 546 |  |
| 213.00-213.32 | 558-566 | JUDGE | "Three," |  |
| 213.56-223.34 | 571-806 | JUDGE | "that the accused, consistent with Regulation 74 of the said naval code, gave orders to a subordinate to tow the said raft." | "74" unsure |
| 225.88-226.78 | 867-889 | JUDGE | "Order!" (shout 1) | energy 226.05-226.65 |
| 227.42-228.28 | 904-925 | JUDGE | "Order!" (shout 2) | energy 227.0-228.3 |
| 228.56-229.16 | 931-946 | JUDGE/other | "Listen out!" | p 0.44; short burst at 228.5-229.3, may be crowd |
| 229.64-231.80 | 957-1009 | JUDGE | "Get the traitors out of the court!" | energy bursts ~231.0-231.6 (-10 dB); clear |
| 232.30-240.44 | 1021-1217 | UNCLEAR (heckler/crowd?) | "But the trouble to accidental misadventure broke and set the rafters free of the high seas!" | whisper p 0.1-0.5; energy only -27 dB with sparse bursts (233.5, 236.0, 240.3-240.5); likely a second voice or crowd, text not trustworthy |
| 243.00 | 1278 | GAVEL KNOCK | strike impact, beat frame 1278 |  |
| 243.04-243.94 | 1279-1301 | JUDGE | "Order!" | energy 243.0-243.95 |
| 245.58-246.34 | 1340-1358 | JUDGE | "Order!" (final, loudest) | energy 245.5-246.4 |

**Dialogue ends** at review 246.34 s = beat frame 1358 (of 1542).

Silences > 1 s (no speech):
- 189.75-190.92 s = frames 0-28 (1.2 s): beat start
- 204.78-207.60 s = frames 361-428 (2.8 s): gap
- 210.62-213.00 s = frames 501-558 (2.4 s): gap
- 223.34-225.88 s = frames 806-867 (2.5 s): gap
- 240.44-243.04 s = frames 1217-1279 (2.6 s): gap
- 243.94-245.58 s = frames 1301-1340 (1.6 s): gap (1.6 s)
- 246.34-254.00 s = frames 1358-1542 (7.7 s): after last Order!: crowd murmur -26 dB, fading to digital silence ~253.9

## b7  (starts at review 286.167 s, frame 6868; file length 20.00 s = 480 frames)

| review s | beat frames | who | text | note |
|---|---|---|---|---|
| 287.13 | 23 | GAVEL KNOCK | strike impact, beat frame 23 |  |
| 287.22-301.68 | 25-372 | JUDGE | "[In] concluding, [I] know/note that there was a regrettable loss of life as a result of an act of God, for which the [appease?] cannot, cannot be held responsible." | words 1-4 and "appease" low p (0.2-0.4): read as uncertain; word times by whisper, "cannot, cannot" 296.72-297.76 / 298.16-299.58, "responsible" 300.7-301.68 |
| 302.33 | 388 | GAVEL KNOCK | strike impact, beat frame 388 |  |

**Dialogue ends** at review 301.68 s = beat frame 372 (of 480).

Silences > 1 s (no speech):
- 286.17-287.22 s = frames 0-25 (1.1 s): beat start (gavel at 287.125)
- 301.68-306.17 s = frames 372-480 (4.5 s): after dialogue

## Notes and doubts
- Gavel knocks against speech: b3 knock at 78.92 s precedes the first word by ~1.3 s. b5 knock 546 (212.5 s) sits 0.5 s before "Three,"; knock 1278 (243.0 s) lands on the first "Order!" of the closing pair, which has no separate knock at 245.58. b7 knock 23 (287.125 s) coincides with the room burst just before "In concluding"; knock 388 (302.33 s) falls ~0.65 s AFTER the last word "responsible" (energy burst 302.35-302.9).
- b5 first "Order!" at 207.6 has no knock; b5 "Order! Order!" 225.9-228.3 has no knock (strikes at frames 25, 546, 1278 only).
- b5 232.3-240.44: unclear (likely a second voice/crowd); do not cue the judge to it.
- The earlier doc (S9-IDLE-JUDGE-OPTIONS.md) listed b3 voice from 79.6; energy says ~80.2.
- Raw words: scratch `words_en.json` (not saved to the repo).
