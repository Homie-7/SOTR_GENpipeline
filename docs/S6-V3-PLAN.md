# Scene 6 animatic v3: the build plan (written 2026-09-28, PREP, before any code changed)

**BUILT the same day** (`tools/render_s6.py` v3). What changed from this plan in the build: the map is centred on
longitude −18 (not −12), and Africa dissolves before the frame edges; burns on the side walls ignite just
past the inner edge (1.06 w), with a larger warp, so the front is ragged rather than straight; WATERLOO and
the Medusa were retimed after `--check` and the stills. What v3 does is recorded in `LOOK.md` Scene 6.

Diagnosis of v2 (frames pulled across the whole of `S6-ANIMATIC_v2.mp4`), then the fix for each of Homie's five notes.
`tools/render_s6.py` is still v2. Before editing it, copy it to `render_s6_v2.py` so v2 can be rebuilt.

## 1. Flag = a real cloth
**Why v2 fails:** the edge mask is built in SCREEN space, so the silhouette never moves. The stripes are 40 px soft blends, so they
read as blurred. Only the shading moves.
**Fix (`ClothFlag`):** a rest rectangle in cloth coordinates, with a forward displacement D(u,v,t) made of travelling waves from hoist
to fly. The amplitude is 0.18+0.82·u^1.3, so the fly end flaps harder. dy = vertical flutter; dx = sway along the length, which bends
the stripes. Render by inverse mapping: c = s − D(c), 3 fixed-point iterations, then remap. **Alpha, stripes, weave, tear, bleach
and burn are all computed in cloth coordinates**, so the outline ripples and everything travels with the folds. Crisp 1–2 px stripe
seams. The top and bottom edges are defined (ripple visible), the hoist dissolves into the smoke (no pole), the fly end frays.
Tear = the two halves pulled apart (pick the left-half or right-half solution per pixel). A frayed edge, no ember glow.

## 2. One picture, one word, never overlapping
New M2 order (the flag recedes into the smoke 38.5–42.5 so CENTRE is free):
Austerlitz L 41 (burns 46) · Wagram R 43.5 (48.5) · **Iéna C 46** (53) · Eylau L **50.0** (55.5) · Friedland R **52.5** (57.5).
Caption lines move to match: Eylau 50.0, Friedland 52.5, "We fought for France" 55, "Nous avons cru" 57, "We believed" 58.5.
Pictures sit high (centre fy≈0.36, height ≈560 full-res px); each word goes in the dark below its picture (fy≈0.80–0.82).
Waterloo gets smaller (height 640, cy 0.36), with its word at 0.82. M6: the side flags sit in fy 0.05–0.62, with the words at 0.82.
Flag burn moves to 130.5–135.5 (L/R to 136). Goya pl. 41 on CENTRE runs 136.5–143.5 (gone 147). The map inks in at 147.5.
"1816" goes in the dark open Atlantic on the map's left. Drop the Azores so nothing passes under it.
**Add `--check`:** render at 0.25 scale every 0.25 s, record the coverage of every tagged blit (pic:/word:) and report any
picture–picture or word–picture overlap. The colour walls, smoke, flakes and embers are fields and don't count.

## 3. Always moving
Every picture gets a constant, linear (not eased) scale of about 1%/s plus a slight upward drift. Store it at 1.5x with a light
pre-blur to stop the hatching from shimmering. Words get a 0.5%/s scale. The colour walls' mottling drifts. The ship approaches
slowly and bobs.

## 4. A physical, consistent burn
Port `court_burn.py`'s layering (approved by Homie): brown scorch soaking ahead, a black char band of varying width, a pale ash lip,
a thin sharp rim with hot spots crawling along it, glowing veins, and a small bloom only. Front: v = |P − P0| + fixed paper warp −
R(t), with **R linear in time** and the warp fixed in the paper. Ignition is always on the side facing the stage centre (LEFT burns
from its right edge, RIGHT from its left, CENTRE from its middle), matching the colour-wall burn Homie liked. **Flakes leave the rim
along (P − P0)/|P − P0|, the direction the front travels, and rise.** They are court-style: textured and tumbling, cooling from
ember to grey. The paper-erosion flakes stop once a picture starts burning. The ghosted families fade into the haze and don't burn.

## 5. The map: tighter, moving, the journey
Crop the Atlantic coast only: a frame 32° of latitude high, fixed at centre longitude −12. The frame pans south at a constant
1.82°/s from 147 to 161.5 (centre lat 39.4 → 13.0). The route draws at a constant speed from 149 to 157.5, with a glowing point at
its head (fy 0.15 → 0.63). Pre-render one large map canvas once and crop it per frame. Bellin geometry: 30.3 px/° in x and
33.2 px/° in y on the 3672x4355 original. The route runs from (−9.5, 47) at px (1042, 508) to Senegal at px (840, 1535).

Then: render at 0.5 → `SOTR_MEDIA/03_TESTS_IN_PROGRESS/S6_animatic/S6-ANIMATIC_v3.mp4`, check the file (probe + contact sheets +
`--check`), and send it to Homie. 0 credits.
