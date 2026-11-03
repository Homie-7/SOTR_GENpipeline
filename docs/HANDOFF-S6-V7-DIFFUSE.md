# S6 v7 change: diffuse away to alpha (Homie, 3 Nov, after reviewing the stills + clip)

Mode POST (script, 0 cr). Nothing edited yet.

## Homie's feedback
- The map is "much better". Zoom could be a bit more elegant ("but it's fine"). Caustic blur is fine, "it kind of dissolves".
- NEW IDEA: don't blend the map into Sahaj's first frame. Keep the watery diffusion, then let it DIFFUSE AWAY to
  transparency (not a fade to black/alpha-only), so whatever plate sits under it comes out as a clean plate. Or
  find a transition once Sahaj's final plate exists. "It becomes too watery, and dies away."

## Where to change (tools/render_s6.py, class MapJourneyV7, ~L1357-1546)
- `morph()` (L1451) currently ends with `canvas[:] = mapw*(1-m) + sear*m` (Sahaj's frame, `self.sah`, takes over).
  Replace the takeover by a matte: the liquefy (refraction `amp`, `sink`) continues, but the map's own coverage
  `cov = 1 - m` (patchy via `dnoise`, softened by `_low`) is the OUTPUT ALPHA; no Sahaj pixels.
- `draw()` also fades `alpha*(1-wash)` and the ocean base: the base and line must go with the same matte.
- Need an alpha path in output: `render_final` (L1976) writes ProRes 422 HQ rgb48le; add an alpha variant
  (prores_ks profile 4444, yuv444p10le/ yuva444p10le, premultiplied vs straight: decide and state) used only
  under a new flag (e.g. `--v7 --v7-alpha`); v6.2 and plain `--v7` must stay bit-identical (`cmp` a short range).
- Review mp4 (L2069, libx264, no alpha): composite over Sahaj's still frame (`self.sah[0]`) AND over a neutral
  grey, to show the alpha works. Stills the same way.
- Zoom elegance: `view()` (L1404) uses a log-rate zoom with a linear pin drift; ease the zoom start/end
  (smoothstep on `u`, keep never-stopping speed through the middle) and ease the pin move. Offer as part of the same stills.
- Timings: V7_W0 153, V7_M0 157, V7_M1 164 (water fully theirs), V7_VID_T 164. Under the new scheme the alpha should
  reach 0 by ~164; keep the course line fading with `fade` (L1509).

## Rules
Stills to Homie FIRST (send with SendUserFile), then a review clip. Output to
`SOTR_MEDIA/04_WORKING_FILES/S6_v7_map_option/` with `_tmp_` names, affinity FFFF3FFF for heavy renders, detached.
Nothing to 01_FINAL_FOR_SHOW, no upscale, 0 credits. Then LOG/REGISTER rows, update docs/NEW-SESSION.md, commit, T9 sync.
Open question to flag to Homie: premultiplied vs straight alpha for AE; the file stays a candidate until Sahaj's final plate.
