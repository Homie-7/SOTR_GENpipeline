# THE FINAL PLAN: 4K finals of the S9 judge and S6 French (2026-11-24)

Mode POST. Written by the star chat. **Nothing is rendered, upscaled or promoted until Homie says yes.**
Credit balance 2,443. Floor 1,500.

## 1. Sound check of Darren's final file

File: `G:\SOTR\HF\Final changes\Final audio\the judge CUT DOWN 23112026.mov`.
Local copy: `SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review/darren_final_23112026/` (sha256 `0dc9ae27…e4cd423`, same as G:).

| Check | Result |
|---|---|
| Length | 351.17 s, 8,428 f at 24 fps. The same as EXT5. |
| Picture | Our EXT5 picture (SSIM mean 0.997). |
| Sound format | pcm_s24le 48 kHz stereo (better than the EXT5 aac). |
| Cut points | The same (183-189 s and 248-290 s on the uncut clock). |
| Finding One (79.6-106.8 s) | Same. Lag 0. |
| Finding Two (185.1-198.9 s) | +0.26 s later (6 frames). OK. |
| "Order! There will be order in the court!" (EXT5 201.2-204.1 s) | **Removed** in the final. |
| Finding Three | **Moved.** "Three," at 207.84 s (+1.4 s), a 3 s pause, then "that the accused…" at 211.90 s (**+4.4 s**). It ends at 221.10 s (+4.3 s). |
| "Order! Order! … get the traitors out … high seas!" | **+2.0 s later** (222.58 s, was 220.60 s). It ends at 237.0 s (was 234.1 s). |
| b5 gavel strike | The gavel sound is at 237.17 s. The picture impact is at 236.95 s. **The sound is 5 frames late.** |
| "Order! Order!" after the strike | 239.40 s. Same. |
| Verdict (276.1-289.3 s) | Same. |
| b7 hit | The sound is at 290.79 s. The picture contact is at 290.90 s. **The sound is 3 frames early.** |
| 0-77 s | The music is gone. The level is about -43 dBFS (was -27). |
| 342-351 s | Darren put sound under the b7 fade to black. EXT5 was silent there. |

**Conclusion.** The sound is a new mix, and three beats moved between 199 s and 238 s.
The picture look-up on "Order! Order!" now comes 2 s before the words.
The strike and the hit are 5 and 3 frames from the new sound.
These are small fixes in `tools/court_ext.py` (positions only, 0 cr), but they change approved picture. Homie decides (Q1, Q2).

## 2. S9 judge, 4K final (paid)

### 2a. Re-time to the final mix (only if Homie says yes to Q1/Q2), 0 cr
- Move the look-up splice (`EXT_LOOKUP`) +2.0 s, so it starts on "Order! Order!" at 222.58 s.
- Move the b5 strike 5 frames later (picture impact on 237.17 s), or move the sound slice 5 frames earlier.
- Move the b7 hit 3 frames earlier, or move the sound slice 3 frames later.
- Rebuild the 720p review with Darren's final sound. Homie looks at it before any upscale.

### 2b. Upscale (Higgsfield), paid
Settings block, one job per file, one job at a time:

| Setting | Value |
|---|---|
| Model | ByteDance video upscale (`bytedance_video_upscale`) |
| Mode | preset `aigc` |
| Reference file | `S9_b3_*_GENJUDGE` (40 s), `S9_b5_CENTRE_court_GENJUDGE_EXT5_FULL` (101 s, uncut), `S9_b7_CENTRE_court_GENJUDGE_EXT5` (20 s); all 1800x1080 |
| Aspect | 5:3 in, 16:9 out (crop back after) |
| Resolution | 4k |
| Frame rate | 24 fps |
| Duration | 40 s / 101 s / 20 s (b5 is under the ~117 s time-out) |
| Quality | default |
| Batch | 1 |
| Sound | none in the job; sound is added after |
| Prompt file | none (upscale only) |

Credits: about **130 cr** for b3 + b5 + b7. With the 4 strike backup loops: **150-180 cr**. Precedent: 3 Nov, 7 files, 144.4 cr. This is over 100 cr, so it needs Homie's yes (Q3).

### 2c. After the upscale, 0 cr
1. Download with `tools/fetch.py`.
2. `tools/upscale_restore.py --size 3600x2160 --clamp 2`. The CENTRE wall is **3600x2160, not 3840**.
3. `tools/upscale_check.py` (temporal stability).
4. Cut b5 to the show cut (248-290 s uncut clock) after the upscale.
5. Sound: a slice of Darren's final mix for each beat, `pcm_s24le` 48k, stream copy for the picture. Check each slice with a correlation (lag 0).
6. Encode ProRes HQ (`prores_ks -profile:v 3`, yuv422p10le).
7. Make the 1080 twins (1800x1080) for `3_HD_1080_fallback/` and the CLEAN masters for `03_CLEAN_MASTERS_no_edge/`.
8. The old files go to `04_WORKING_FILES/superseded/` with their version.

## 3. S6 French, 4K final (map to alpha), 0 cr

Approved: the French review ("It's perfect", 20 Nov), the flag and the ink.
It is a native render, not an upscale. Renders run with affinity FFFF3FFF, a watchdog and `_tmp_` names.

```
python tools/render_s6.py OUTDIR --scale 2.0 --final --v6 --v7 --v7-feather --v7-alpha --warm 10 --retime-fr
```
- Output: ProRes 4444, straight alpha (yuva444p10le), LEFT 2880x2160, CENTRE 3600x2160, RIGHT 2880x2160. 2,910 f, 121.25 s.
- The map dissolves to alpha as ink from 112.78 s to 120.25 s.
- Time: about 3.5-4.5 h (UNCONFIRMED).
- Sound: mux `G:\SOTR\HF\Final changes\Sc 6 wars 4 Homie FASTER READ NO ENGLISH.wav` with `-c:v copy -c:a pcm_s24le`.
- The same command with `--scale 1.0` gives the 1080 files and the CLEAN masters.
- One check first: the fleur mask is calibrated on the 1080 flag. I will test one 4K frame before the full render.
- The old v14 English files (165 s) go to `superseded/`.

## 4. Promotion (after Homie looks at the finals)
- Show files to `01_FINAL_FOR_SHOW/1_PLAY_THESE_IN_ORDER/`, with the same show names.
- Update `00_READ_ME_FIRST.txt`: S6 is now 2:01 with the ink from about 1:53; new S9 lengths.
- REGISTER, LOG, NEW-SESSION, CLAUDE.md stage; commit; push; T9 copy with sha256.

## 5. Questions for Homie
- **Q1.** The "Order! Order!" line is 2 s later in Darren's final mix. Do I move the look-up to the new words? (Recommended: yes, 0 cr.)
- **Q2.** The strike sound is 5 frames late and the hit sound is 3 frames early. Do I move the picture to the sound? (Recommended: yes, 0 cr.)
- **Q3.** Do I spend about 130 cr (150-180 cr with the strike backups) on the S9 upscale?
- **Q4.** Do I start the S6 4K render now (0 cr, about 4 h)? It does not depend on Q1-Q3.
