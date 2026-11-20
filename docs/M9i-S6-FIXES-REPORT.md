# M9i: S6 French fixes report (2026-11-20, helper; not committed)

All changes are in `tools/render_s6.py` and run only with `--retime-fr`. 0 credits. Nothing went into 01_FINAL_FOR_SHOW. Nothing was committed, the long review render was not launched, and Explorer was not opened.

## What changed

- **New code**
  - `t_new_of` / `t_old_of` (inverse and forward TMAP).
  - `cues_fr(ctx, wash, gy)`, which returns the French washes, words and burn groups.
  - `CW_OUT_FR = 61.1`, which drives the colour wall out through `S['cw_out']`.
  - `class RoomBurnIn` (the burn front comes in from both outer edges).
  - `class BurnGroup` (one shared RoomBurn per group; `fit()` sets R0/R1 to the members' D range).
- **Changed classes**
  - `PaperBurn(field=)`.
  - `Wash(clock='new', group=)`.
  - `Word(clock='new', fade_out=)`.
- **Flag**
  - `GenFlag._v6_maps(a, vc)`: under FR, the fleur holes use the cloth rows from `_vcoord`.
  - `_fl_calibrate()` was split out, so fl_H0 is calibrated first and `fl_vc` is cached per frame.
- **Clock**
  - Pictures come in at word − 0.35 (in 1.4). Words fade in at the word onset (fade 0.6), at the onsets given.
  - The Waterloo field, the ravages and p41 are placed by inverse TMAP and keep their real durations.
  - Austerlitz burns off L 35.6-37.1 and Wagram burns off R 36.9-38.4.
  - No Goya words were added: v14 has none, so their times are used only for the pictures.
- **Burn groups** (new seeds)
  - Battles: seed 7131, 40.6-43.9, inside-out.
  - Goya: RoomBurnIn, seed 7132, 50.0-52.6, outside-in.
  - Waterloo: seed 7143, 70.5-74.0, inside-out.

## Bit-identical proof (FR off): PASS

I rendered stills at t = 50, 100 and 150, overGrey and overSahaj, at `--scale 0.5 --v6 --v7 --v7-feather --v7-alpha`.

- HEAD (`git show HEAD:` copy) and the final code agree: all 6 PNGs are array-identical, and their sha256 hashes match too.
- The proof was re-run on the final code after every FR-only edit.

## Burn measurements

These are the times at which each wall has 50% of its picture alpha left. The L-R figure is the absolute difference in remaining alpha fraction between LEFT and RIGHT, per frame across the window.

| Group | Centre 50% | Left 50% | Right 50% | L-R max | L-R mean |
|---|---|---|---|---|---|
| Battles | 41.17 | 42.96 | 42.96 | 0.124 | 0.019 |
| Goya | 52.25 | 50.83 | 50.79 | 0.098 | 0.025 |
| Waterloo | 71.12 | 73.0 | 73.08 | 0.104 | 0.020 |

- **Battles:** L and R are clear at about 43.7, before the famine picture comes in at 45.03.
- **Waterloo:** C is clear by about 71.4, before flagC's reveal at about 72.4.
- **Inside-out timing:** in the inside-out groups, C goes first and L/R follow about 1.8 s later, together and mirror-symmetric, while the front crosses the dark gap. One front cannot reach all three walls at once. If C should hold longer, that is a follow-up.

## Flag check

- Homie's screenshot has no timestamp. I compared RIGHT at new 81.5 vs 83.5, crop at `<scratchpad>\flagpair.png`.
- The holes keep their place against the neighbouring fleurs and seams while the cloth rises. They ride the cloth and no longer slide vertically.

## Alpha at the end

- At 119 s, overGrey is 117-119 (mean 117.99).
- At 121 s, overGrey is flat 118.
- At both times, 0 px differ from the grey. The map has fully gone to alpha.

## Stills and contact sheet

- The stills are in `D:\SOTR\SOTR_MEDIA\04_WORKING_FILES\S6_french_review\stills_M9h\`: 18 times, overGrey and overSahaj each.
- The contact sheet is `00_contact_sheet.jpg` in the same folder.
- I looked at every row. Nothing needed fixing.
- At 63.3, Waterloo comes in inside the colour wall's centre burn hole while L blue and R red still hold. This follows the v14 design (burn_M5), with the colour walls going out at 61.1.

## Housekeeping

The HEAD scratch copy `tools/_scratch_render_s6_head.py` was moved to `D:\SOTR\_DELETE_ME_2026-11-20\repo_scratch\`.
