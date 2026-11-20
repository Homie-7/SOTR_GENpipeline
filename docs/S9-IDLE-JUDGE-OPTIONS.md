# S9: the idle judge, options drawn from Darren's mix (measured 2026-11-20). PROPOSAL ONLY, 0 cr.

Mix: `G:\SOTR\HF\Final changes\the judge TO BE CUT DOWN 19112026.mov`. All times are on **his mix clock** (our current
S9 clock). After the b5 cut, b7 moves earlier by the cut (`docs/S9-DARREN-CUT.md`). The method was a scratch numpy
pass: loudness, spectral-flux onsets and an autocorrelation for pulse, then faster-whisper `small` with word times.
Each idle hold = the raised pose after a strike block (57 blow frames + 24 held = 3.4 s after the cue).

## What is audible under each hold

| Hold | Range (s) | What is there |
|---|---|---|
| b3 | 81.8-117.4 | **The judge's own voice** (79.6-106.5): "In the matter of... my findings of fact are **One** (91.5). The accused exercised appropriate leadership... lifeboats" (106.0). Then a low, dull bed at -42 dB (106.8-113, 20% under 300 Hz, no words), fading to silence by about 116.5. |
| b5a | 193.6-233.5 | His voice: "**Two** (190.7)... food and water... (204.1)". Then "**Order**, there will be order in the court" (207.1-210.0). Then "**Three** (212.3)... a subordinate... the raft" (222.7). Then "**Order, order**, ... get the traitors out of the court" (225.7-231.3). Between his lines a **crowd murmur** holds at -22 dB: no intelligible words, centroid about 900 Hz, never silent. |
| b5b | 236.8-245.5 | A line from 231.7 to 239.8 ("...the raft... the high seas"; **the speaker is unclear**, it may be a heckler). Then a **crowd surge** from 240.3 to 244.0, at -18 dB with more low end and hiss (shouting). Then "**Order, order!**" at 244.1 and 245.1 (the loudest point, 246.2). |
| b5c | 248.8-254.0 | The crowd after the last "Order!" (-18 dB), then his fade to digital silence (-56 dB by 249-253). |
| b7 | 326.8-338.9 | The verdict, nearly unbroken (323.8-337.3): "...a regrettable **loss of life** (328.1)... an act of **God** (330.9)... **cannot, cannot** (333.2, 334.8) be held **responsible** (337.3)". Then a short crowd reaction (338.2) before the capper (338.9). |

- **No rhythmic pulse anywhere.** The best autocorrelations are 0.17-0.25, which is speech syllables (0.35 s), not a beat.
- The only slow swell is the speech phrasing, about 3.6-4.2 s in b5.
- **No hard gavel transients in his mix.** The loud peaks (198.1, 212.5, 226.2, 243.1, 246.2) rise only 2-11 dB in 30 ms, with little high end: they are vocal emphasis, not wood.
- So the holds are not ambience. **They are a man speaking over a restless room.**

## Options (all by script, from the approved strike `fig_SOTR_judge_strike_s9_v1`)

- **Locked camera, one figure.** Every move is a local warp of the grey source before the threshold, so the figure stays two-tone. The behind-paper softening (`court_behind_paper.py`, A2 level 2) is applied after, as now.
- **Found in the source:** frames 0-36 of the approved strike already hold a small generated stir before the blow. 3-10% of the silhouette's pixels change, almost all at rows 1000-1600 (the coat skirts and hands). The head is still. That is real cloth motion we can reuse forward-only (never ping-ponged; Homie called reverse loops cheap).

**A. "He reads" (his voice drives his body).**
- **Breath:** a breath before each line. The shoulders and chest rise by about 0.6% over 1.0 s, then settle over 2 s. Cues: 92.4, 190.2, 206.6, 211.8, 225.1, 243.6, 323.2.
- **Nods:** a small head dip on each stressed word, the head pivoting about the neck by at most 1.5 degrees (about 4 px at 1080), over 0.3 s. Cues: One 91.5, Two 190.7, Three 212.3, Order 207.1 / 225.7 / 244.1, God 330.9, cannot 333.2 / 334.8, responsible 337.3.
- **Under the rest of his words:** a tiny head motion driven by his loudness envelope (0.25 s smoothed).
- **Build:** `cv2.remap` on the head and chest regions of the RAISED frame, keyed from a cue list taken from these word times.

**B. "The court stirs" (the room drives the scene).**
- **Paper and lamp:** the crowd bed drives the paper and the lamp. The paper's grain shifts by 1-2 px, and the lamp's gain is modulated by the crowd's level (`lamp_gain` plus the mix envelope), so 240.3-244.0 visibly unsettles the light.
- **The judge's lean:** on each "Order" he leans 1-2% toward the room (a torso shear from the feet, the feet pinned to the floor line). Cues: 207.1, 225.7, 244.1.
- **The coat:** source frames 0-36 play forward once, so the coat skirts swing. Cues: 207.7, 226.2, 246.2. Then a 0.5 s blend on the grey back to frame 0.
- **b3 and b7:** the paper and lamp only, plus the one 338.2 reaction.

**C. Both, kept small (recommended).**
- A's breath and the word nods carry b3 and b7, because there he is reading, alone.
- B's lean and coat stir land only on the three "Order"s in b5, and the crowd surge (240.3-244.0) moves the lamp.
- **b3's quiet tail (106.8-117) stays near still:** the breaths alone, slowing as the sound fades. The stillness then reads as intended.
- **A true head turn** (a profile change) cannot be made convincingly by warp. If Homie wants one, it is a Seedance image-to-video from the approved still. That costs about 48 cr per take, by the earlier court edit-video take; **unverified**, so estimate it first. Budget 2-3 takes, about 100-150 cr. Not recommended.

**Recommendation: C.** It is tied to what is audible (his words, the room's "Order" moments) and costs 0 cr. It reuses the approved cloth motion. A 15 s still-and-clip test on 204-219 (two breaths, "Order", the lean, "Three") would show the look before any beat file is touched.

**Flags for the cut** (`docs/S9-DARREN-CUT.md`):
- The planned 2nd b5 strike at 233.5 lands mid-line, on "court,". The words are "Order, order" at 225.7-227.2 (peak 226.2), which may be the truer cue.
- b3's strike (78.4) falls before his "One" (91.5).
