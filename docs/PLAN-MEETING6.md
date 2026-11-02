# PLAN — Meeting 6 changes (team meeting 31 Oct 2026, RMIT Black Box)

Written 2026-11-03 with Homie. Source: `G:\SOTR\Meeting notes\2026 TEAM MEETING 6 Minutes (Meeting 6).pdf`.
Development begins **18 Nov 2026**. Three tasks are confirmed ours; everything else in the minutes is other people's
or unconfirmed (don't touch it: Scene 8 rowboats/ropes/raft = Sahaj; the "2026" file-naming convention = Simon, not
adopted; skirting board, cantinière, projection on actors = decided in the space).

**Mode: POST / script.** All three are script work on approved material, 0 generation credits. **Credits: last
recorded balance 1.62 (9 Oct). Check it before anything that costs (4K upscales).** Homie's standing rules hold:
clean masters never overwritten, a new version under the SAME show name with the old one to
`04_WORKING_FILES/superseded/`, sound rides in every file, files start and end at full picture, nothing promoted to
`01_FINAL_FOR_SHOW/` and nothing upscaled until Homie approves (memory "only what's asked").

**Order:** 1. Scene 6 (the biggest, needs the most review rounds; send stills early). 2. Scene 1 Napoleon (while
Homie reviews S6). 3. Scene 9 judge. Each task: stills to Homie first, then the render.

---

## 1. Scene 6 — the map takes over the room, and hands over to Sahaj's sea

**Now (v6.2, in the show):** `tools/render_s6.py --v6` (165 s, 4680x1080 timeline). M7 (2:16): Goya's
*Escapan entre las llamas* on CENTRE (136.5-143.5 s); then Goya p44/p45 (the fleeing families) on LEFT/RIGHT
(138-157 s) drifting toward the ship; `MapJourney` on **CENTRE only** from `MAP_T0` = 147.5 s ("Loin !"), panning
south at `MAP_SPEED` while the Medusa's course draws down the coast; "1816" (150-154 s); the Baugean Medusa
engraving comes in ~157-160 s ("(The Medusa appears on the horizon.)").

**Homie's brief (3 Nov):** the next scene is us at sea (Sahaj's bird flight), so the map hands over to the sea.
"As the dotted line is animating towards Senegal… like the way a satellite map zooms… you start zooming into the
African continent, and the line doesn't actually make it all the way to Senegal because we're suggesting that it's
on the way, but we already emphasize Senegal's location… somewhere around 75% progress, we will transition into the
ocean." He likes how the trajectory animates toward Senegal: keep that. When the map comes on, **the music comes in**
("the journey begins"): a dramatic, cinematic start after the quick recap of the wars.

### Decisions (Homie, 3 Nov)

1. **The map fills ALL THREE walls** (not CENTRE only): "conveys the grandness of the African continent", and the
   visual noise helps the water mix in. The map is a field (like the smoke), so it may cross seams; the **course
   line, its glowing head and the Senegal marker are objects**: they stay inside CENTRE, out of the 90 px guard.
2. **Satellite-style zoom** into West Africa, continuous, constant rate in log-scale (it never stops moving: LOOK
   Scene 6 rule "nothing is ever static"). Start wide enough to read Africa as a continent across the room; end
   close on the Senegal coast.
3. **Senegal is marked from the start of the zoom:** a soft glowing point at Saint-Louis + "Sénégal" in the Bellin
   map's own engraved lettering style (not a modern font). The line heads for it and **never arrives**: the
   transition starts at ~75% of the course distance (Rochefort -> Saint-Louis).
4. **CUT:** Goya p44 + p45 (the families on LEFT/RIGHT) and the Baugean Medusa engraving (+ its swell).
   "When the African map is on, nothing else is on the left and right." **KEEP:** Goya *Escapan entre las llamas*
   on CENTRE, and the "1816" title (in the open Atlantic, now on the full-room map).
5. **Scene end: Claude's call.** Recommended: keep `DUR` = 165 s and the map's entrance on "Loin !" (147.5 s: the
   music cue). Zoom 147.5 -> ~157 s ("Away from here!") reaching 75%; the water 157 -> ~163 s; the last ~2 s are
   Sahaj's clean frame, moving (see below). Retime if the stills say otherwise; the dialogue table is at the top of
   `render_s6.py`.
6. **The hand-off to Sahaj.** Reference (a ROUGH render; his scene will change, but the light and the water are
   right): `SOTR_MEDIA/05_REFERENCE_UPLOADS/S6_handoff_Sahaj/A_flyin_m07v3_unity_03oct_ROOM.mp4` (copied from
   Homie's Desktop, sha256 2aaaedcc…). Live sim (Homie's Brave): https://stage4d.embracingearth.space/stage/#m07v3
   - Layout, measured: 1920x1008, 24 fps, 90 s. A caption bar rows 0-29; **the three walls = rows 30-472
     (1920x443)**, aspect 4.334 = our 4680x1080 (4.333), so his strip maps straight onto our canvas; the seams fall
     at x 591 / 1329 (our LEFT 1440 | CENTRE 1800 | RIGHT 1440). Below: a FLOOR trapezoid (ignore it: no floor
     projector is confirmed; FLOOR-PLAN.md).
   - **Use his FIRST frame** (t = 0, `A_flyin_m07v3_f0001_WALLS_1920x443.png`): bright overcast day, horizon ~56%
     down the walls, the ship small at the horizon dead centre, three small gulls, the sun's glitter right of centre
     (CENTRE right half into RIGHT). It's the cleanest frame and it's where his scene starts, so our last frame =
     his first frame and his file can follow ours cut-free. For the last ~2 s, play his first seconds (moving water),
     not a freeze.
   - Upscale his strip to 4680x1080 for the draft (Lanczos; it's a placeholder). **When Sahaj delivers his final
     render, re-do the hand-off from his real first frame** (ask Homie for it; note it in REGISTER as provisional).
7. **The water: from the sides (everyone's preference), done cleanly — Claude's recommendation after seeing his
   render.** His sea is ONE continuous horizon across all three walls, so the water should arrive as HIS sea, not
   a separate effect:
   - At ~75% the sea enters from the **outer edges of LEFT and RIGHT** and washes inward over the map toward the
     Senegal marker: a soft, wide, wet front with a little foam at its leading lip (take the foam/glitter texture
     from his own water), never a hard wipe or a cartoon wave.
   - Behind the front the map **wets**: for a beat it stays visible under the water, darkening and refracting as
     the paper soaks (physical, D16 "materials break the way they really would"), then sinks into his sea.
   - His sea's lower band arrives first; his **sky clears in from the top** like mist burning off as the two fronts
     meet on CENTRE. The exposure jump from the dark map to his bright day is the music's "journey begins": let it
     rise over the water's ~6 s, not snap.
   - The course line and Senegal are the last things under water (they are on CENTRE, where the fronts meet).
   - Test this first as 6 stills (e.g. 150, 155, 157, 159, 161, 163 s at `--scale 0.5`). If the side fronts look
     busy against the map's lettering, the fallback to show Homie is **B: the map's own Atlantic comes alive** (the
     sea on the map turns to his water in place, then the land floods from the coast) — stills of both side by side.
8. **Build it as `--v7`** in `render_s6.py`, OFF by default, so v6.2 still renders bit for bit (the pattern `--v6`
   used; verify with a short `cmp` render of a v6.2 range). Run `--check` (overlaps) on v7. Sound: v6.2's sound
   carries through unchanged (Darrin/Louise score this moment separately; it's a scratch track); at the hand-off,
   cross-fade into Sahaj's clip sound only if his file has sound — check.
9. **Deliver for review** at 1080 into `04_WORKING_FILES/S6_v7_map_option/` (three walls + a side-by-side review
   mp4 of 2:10-2:45). 4K for the show = ByteDance aigc in two overlapping halves per wall + `upscale_restore.py
   --clamp 2` (as v6.2, ~40 credits): **only after Homie approves, and only with credits**.

---

## 2. Scene 1 (+ 10) — Napoleon on horseback replaces Ingres on RIGHT

**Painting:** Jacques-Louis David, *Napoleon Crossing the Alps* (*Bonaparte franchissant le Grand-Saint-Bernard*).
Five versions, 1801-1805 (era OK). **Recommended: the Château de Malmaison version (1801, 261 x 221 cm)**, the first
and the best known (yellow-orange cloak, rearing grey-white horse; the Charlottenburg copy has a red cloak). Get the
highest-resolution public-domain scan (Wikimedia Commons; download via `tools/fetch.py`, the DNS rule), save as
`02_APPROVED_BUILDING_BLOCKS/S1_gallery/paintings/src_SOTR_napoleon_david_alps_malmaison.jpg` (keep the Ingres source).
Homie: "I'm happy for you to pick the best version that you think is accurate"; "everything that the gallery will
require that painting to be in, we'll have to update".

**The catch: the frame's shape.** The RIGHT plate's gilt frame was generated around Ingres's portrait (~2.6 x 1.6 m,
tall and narrow); David's is ~2.6 x 2.2 m (much wider). Options, in order:
- **A (recommended, 0 credits): rebuild the frame by script.** A 9-slice of the existing carved frame: keep the four
  corners, stretch/tile the side rails to the new aspect, re-lay the warm light pool and drop shadow from the room
  model (`gallery_wall.py --room-light`), hang centred on the same centre line (`gallery_rehang.py`). Size: real
  height if it fits the 3.6 m wall with the room's margins (the Raft sets the scale: it's hung ~3 m high on CENTRE;
  Napoleon should sit visibly smaller than the Raft and match LEFT's pair's hanging line).
- B: regenerate the RIGHT plate with David as the reference (NBP, ~8 credits): only if A's frame looks stretched.
**Inputs:** `04_WORKING_FILES/S1_gallery/1_READY_for_show_build/walls/S1-GAL-R_LIT_v3_*` (native, 1440x1080,
2880x2160, frames json) and `S1-GAL-R_DARK_v3_*`; the room light `S1-GAL_room_light_v2.json`. Tools: `gallery_wall.py`,
`gallery_rehang.py`, `gallery_dark.py`, `gallery_show.py`. Read `LOOK.md` "Scenes 1 + 10" and the gallery
`00_STATUS_READ_ME.txt` first.
**Everything that shows RIGHT gets rebuilt (same names):** `S1-GAL-R_LIT` and `_DARK` v4 at 1080 and 4K (the 4K plate
exists, the painting is pinned from its scan: **no upscale needed**); the SEAM pictures; the show files
`S1_a_RIGHT_gallery.mov`, `S1_b_RIGHT_gallery-blackout.mov`, `S10_RIGHT_gallery.mov` (1080, full length) and the
backup loops `S1-and-S10_RIGHT_gallery_LIT_HOLD_loop.mov`, `S1_RIGHT_gallery_DARK_HOLD_loop.mov` (4K). LEFT/CENTRE
are untouched (the blackout runs bank by bank, so check RIGHT's timing still matches by building from the same
`gallery_show.py` recipe). Floors unaffected. Also refresh the `FOR DARRIN` / WhatsApp previews (`share_previews.py`)
once approved. Review: a still of the three walls (LIT + DARK) to Homie first.

---

## 3. Scene 9 — the judge behind the parchment

**Now:** `render_court.py --scrim --burn` = the judge's black silhouette laid ON the lit-scrim field ("a lamp behind
paper"), the paper burning away at both sides. Show files: `S9_b3/b5/b7_CENTRE_court.mov` + backup loops
`S9_b3/b5/b7_CENTRE_court_strike-size1..4.mov`. Minutes: "Experiment with placing the judge behind the parchment
paper so he is less defined." Homie: Claude decides the method; the defaults below.

**A (the main test, by script):** he becomes a SHADOW cast through the paper, not a figure on it.
- Soften him (blur), lift his black to the paper's shadow tone (a warm dark grey, not 0), and lay the paper's own
  fibre/grain and the lamp glow OVER him (he is behind it), so the paper reads continuous across him.
- Depth: a real shadow on paper is sharpest where the body is closest. **Test both:** (a1) the same softness
  throughout; (a2) he sharpens as he lunges toward us on the strike, softening again after.
- Check: the sanctioned white keyline round the gavel (LOOK World 3) must not become a glowing halo; the paper burn
  at the sides must still read as burning the paper he's behind.
- Three softness levels as stills (same frame, e.g. b3 hold + a strike peak) to Homie before any render.

**B (Homie's optional idea, try it if A works):** a figure of SMOKE, like the underworld in Christopher Nolan's
*The Odyssey* (2026): clearly our judge in shape, ethereal, made of smoke. Homie: **"it has to be very distinctly
clear what this character is, his outfit, etc."**, and "if you think it's not worth it, don't worry about it".
By script: keep the silhouette's interior shapes (epaulettes, fringe, coat line, hat) as a dense core, and let only
its EDGES go to smoke (advected noise; the S6 generated smoke loop in `02_APPROVED_BUILDING_BLOCKS/S6_generated/` is a
real-smoke texture to drive it), rising gently, never eating the outline. Drop it if the outfit stops reading
(memory "drop hard extras"). One still beside A.

Deliver for review in `04_WORKING_FILES/S9_court_behind_paper/`. The approved strike, its timing and the burn stay.

---

## Wrap for each task

REGISTER + LOG rows; `docs/NEW-SESSION.md` "THE TASK, RIGHT NOW"; CLAUDE.md Current stage (one short block);
commit, push, `git pull` in `G:\SOTR\HF\SOTR_GENpipeline`; new media copied to the T9 `G:\SOTR\HF\SOTR_MEDIA\` with sha256.
