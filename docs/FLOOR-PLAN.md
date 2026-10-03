# FLOOR PLAN — only if a floor projector is confirmed

**Status: CONTINGENCY, not started (2026-10-03).** Nothing about a floor projector is confirmed. This is the plan that's
ready to go if it is. Nothing approved changes: the floor is extra files that play beside the wall files.

**Homie's brief (2026-10-03):** *"In the end it will still be a video in 1080/4k that the projection mapping guy will
manage. We don't need to overdo anything… we can add things that sit well with what we already have. Floor projection
is also weird to view from an audience perspective, so think about warping."*

**Decided (Homie, 2026-10-03):**
- **The judge's shadow on the floor: YES.**
- **The salon carpet: OUT.** Light pools do that job.
- **Sound:** floor files may carry scratch sound, but the sound designer does the real sound. Scratch only where the
  floor adds a new event (the sea); otherwise a silent track.

---

## 1. The viewing problem, and the rule that solves it

**What the audience actually sees.** A seated eye is about 1.1–1.2 m up. On flat seating, a spectator 6 m from the floor
sees it at ~11°, so its 4.35 m depth looks about **5 times shallower** than it is: the whole floor reads as a thin band.
Front rows see it steeper and bigger; back rows see a sliver, often behind heads. Consequences:

- **Depth detail disappears.** A circle on the floor reads as a thin ellipse; text, faces, pictures and the map of Africa
  would be unreadable from most seats. Width (left–right) reads at full size.
- **Every seat sees it differently.** An anamorphic image (stretched to look right from one "design eye", like the
  Unity ship deck) is right from one seat and bent from all the others. That's the trap we avoided on the walls.

**The rule: FLOOR AS FLOOR (the same idea as walls-as-walls).** Only put on the floor things that really lie on a floor:
**light pools, shadows, water, smoke, ash, and a line on a map.** These look right from every seat with no warping,
because in life we always see them foreshortened. A real pool of candlelight or a real shadow is squashed by the
viewing angle too, and the eye accepts it. So:

- Render the floor **top-down, orthographic, at true scale**. **No pre-warp, no anamorphosis.** The real geometry does
  the perspective, exactly as it would for a real shadow.
- **The mapping guy fits it.** We deliver a plain rectangle; he keystones / warps it to wherever his projector hangs.
- **Nothing the story needs lives only on the floor.** Back rows may not see it. The floor extends what the walls say.
- **Mostly dark, brightness capped.** The floor projector also lights the performers from above and the floor bounces
  up into the walls' blacks. Every floor file stays under a peak-brightness cap (set at the preview, step 4).
- **No text, no pictures, no figures** (the judge's shadow is a shadow, not a figure).
- **The wall–floor fold is forgiving.** Mapping won't line up to the millimetre, so nothing has to meet the wall
  exactly: pools and shadows start soft at the foot of their wall; the Scene 6 route crosses the fold inside a soft glow.
- **The floor never breaks.** No fragment edge (it's the ground, and the actors stand on it). So clean = show file.

## 2. Format

- **Frame:** a standard 16:9 video, 1920x1080 or 3840x2160 (Homie: the mapping guy manages it). The floor's envelope,
  **10,057 x 4,350 mm (the 3 Oct blocking's "floor wedge")**, sits in it at true proportion, full width, centred
  (1920x830 / 3840x1660 of picture), black above and below. **Top of the picture = upstage** (the CENTRE wall),
  bottom = the audience.
- **No baked mask.** The final shape isn't confirmed, so content is kept inside a safe area (the wedge between the two
  flats' bases, 300 mm in from every edge) and fades softly to black outside it; the mapping guy masks the rest.
- **Same frame count and first frame as each wall twin,** ProRes 422 HQ `-qscale:v 2`, 24 fps, like every show file.
- **Rendered by script straight at 4K** (soft fields need no upscaler, 0 credits). 1080 copies for the fallback set.
- **For the mapping guy:** `FLOOR_calibration_grid.mov/.png`: the envelope, a 1 m grid, the centre line, the two flats'
  base lines, the safe area, the design-eye mark. He lines it up once; every floor file then sits right.

## 3. What would be made

### Scene 6 — one file, `S6_FLOOR_wars.mov` (2:45, the same timeline as the three walls, started with them)

| Movement | Floor | Built from |
|---|---|---|
| M1 | Battle smoke pooling low across the floor, embers | the approved generated smoke (`GenSmoke`), 0 credits |
| M2–M3 | near black; faint drift; the burns' ash starts to settle | the Ash code |
| M4 | the blue / white / red walls spill coloured light onto the floor at the foot of each wall (light only) | the colour walls |
| M5–M6 | the room burn's ash falls and settles on the floor, cooling from ember to grey | the RoomBurn front |
| M7 | the Medusa's red route comes off CENTRE through a soft glow at the fold and runs **downstage toward the audience** (south = toward them), then the floor becomes **dark sea**, slow swell rolling downstage under the Medusa on the horizon; held into Scene 7 | the route (script) + a **scripted sea** |

**The map of Africa itself stays on CENTRE** (Homie's first idea was to continue it on the floor): from the seats it would
be a squashed, unreadable shape. **The route line and the sea** carry the journey onto the floor instead; a line
and water read from every seat.

**The sea: scripted first, generated only if it looks fake.** At that viewing angle a dark scripted swell reads like water;
a generated top-down sea (Seedance 2.5, 4 s probe 48 cr, then a 30 s Sequel 360 cr) is the fallback, asked for first.
**The last frame must hand over to Scene 7's opening floor** (the team's ship deck): ask what it is.

### Scene 9 — one floor file per show file, same lengths (`S9_b<beat>_FLOOR_<world>.mov`)

| File | Length | Floor |
|---|---|---|
| `S9_b2-3_FLOOR_salon` | 1:57 | warm candle pools at the foot of the RIGHT flat, growing as the candles light, gone at the snuff; dusk |
| `S9_b3_FLOOR_court` | 0:40 | **the judge's shadow** (below) at size 1 |
| `S9_b4_FLOOR_studio` | 1:12 | the candle's pool at the foot of the LEFT flat, low and unsteady |
| `S9_b5_FLOOR_court` | 1:41 | the shadow at "Two!", longer at "Three!" |
| `S9_b6_FLOOR_studio` | 0:32 | the candle pool flickering |
| `S9_b7_FLOOR_court` | 0:20 | the shadow reaching the front edge at the verdict; the capper: the gavel's shadow sweeps the whole floor, then black |
| `S9_b8_FLOOR_salon` | 0:16 | the pools snap back lit, then snuff |
| `S9_b9_FLOOR_studio` | 0:40 | the candle pool steady and at its brightest |

**The pools are driven by their own wall file's light** (the brightness of each sconce / the candle, measured per frame
from the clean master), so they flicker and snuff in sync by construction, with no hand timing. They follow the flats'
splayed base lines (25° off square, `STAGE.md`).

**The judge's shadow (YES, Homie).** The court is shadow theatre: a lamp behind the paper screen. Light through the
screen carries on downstage, so the figure throws a long shadow forward across the floor, from the foot of CENTRE toward
the audience, inside a dim warm glow. Every size jump on the wall makes the shadow longer at the same frame; it shudders
on each strike like the field. It falls over the raft riser in the middle of the floor: the official lie laid over the
survivors. Built by script from the matte `render_court.py` already makes (a projective cast from the lamp point onto the
floor plane), so it is the wall's own performance, frame for frame. The riser's height bends the shadow the way a real
shadow would bend; that's correct, not a fault.

**Backup twins (10):** every piece in `2_BACKUP_LOOPS_for_operator/` gets its floor twin (salon IN / HOLD / OUT pools,
studio HOLD pools, court strike shadows at sizes 1–4), so the operator can still swap pieces.

**Total:** 1 + 8 + 10 = **19 floor files**, plus the calibration grid.

## 4. Steps, in order

1. **Trigger: the floor projector is confirmed.** Ask the team for: the floor's final shape and size; the raft riser's
   footprint and height; the seating (rake, distance of the first and last rows); 1080 or 4K; one file per floor or
   anything else the mapping guy prefers; Scene 7's opening floor; whether the playback can run 4 streams in Scene 6.
2. **PREP (0 credits):** floor spec into `STAGE.md` (its parked floor item), a floor section in `LOOK.md` (DRAFT until
   Homie locks it), cards in `SHOTCARDS.md`, the calibration grid.
3. **The seat preview (0 credits):** a new `tools/stage_preview.py` renders the three walls + the floor in perspective
   **from three seats** (front row, middle, back; seated eye 1.15 m). This is how we judge "weird to view" before
   building anything. **Proof clips for Homie:** court beat 5 (the shadow) and Scene 6 M7 (route + sea), each seen from the
   three seats. Set the brightness cap here. Homie signs off or drops it.
4. **Tools (0 credits):** `tools/floor_light.py` (pools driven by a wall file's light), `tools/court_shadow.py` (the cast
   shadow), a floor layer in `render_s6.py` (smoke, ash settling, colour spill, route, sea).
5. **Render** the 19 files clean at 4K + 1080 (the PC: affinity FFFF3FFF). **Checks:** frame count and first frame =
   the wall twin; nothing outside the safe area; under the brightness cap; the seat preview of every file from three
   seats; sound per the rule above.
6. **Approve (Homie), then file:** `01_FINAL_FOR_SHOW/4_FLOOR_only_if_floor_projector/` with its own `1_PLAY`,
   `2_BACKUP` and `3_HD_1080` folders and the calibration grid, README updated (play each floor file with its wall
   file); masters in `03_CLEAN_MASTERS_no_edge/floor/`; REGISTER, LOG, the T9.

**Cost:** 0 credits (everything scripted), or ~410 if the scripted sea doesn't pass and a generated one is approved.
**Time:** about two sessions: one for steps 2–3 (the preview decides whether it's worth it), one for 4–6.

## 5. What this plan deliberately leaves out

The map image, text, pictures, figures, the salon carpet, anything anamorphic, anything bright under the performers,
anything the story depends on, and any change to an approved wall file.
