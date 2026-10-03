# PLAN — the client's notes from Meeting 4 (3 Oct 2026)

**Deadline: the Higgsfield subscription ends on the 2nd (November; confirm).** Balance 2,315.66 credits (Ultra),
3 Oct. **Homie's budget: 1,000 credits today, "very conservative and careful, no wasted credits".**
**Order (Homie): 1. the Scene 6 flags (they need generations), 2. the Alps, 3. the battlefield grade.**
The floor projection (`docs/FLOOR-PLAN.md`) is parked. Meeting notes: `SOTR_MEDIA/06_PRESENTATIONS/2026 RMIT SOTR -
Meeting 4.docx.pdf` (section 6 is ours).

---

## 1. SCENE 6 — THE FLAGS (first)

### What the client said (meeting notes §6, Louise and Simon)
"The flags currently appear quite strong and graphic against the darker background." Suggestions:
**softening the colours · more historically textured and weathered flags · movement between monarchist and
republican/Napoleonic imagery · conflict and political instability rather than static symbols.** Homie: the flag's
history "is not that clear"; "one side becomes all bluish, one side all white" (the Liberté walls and the split).
**Kept, liked:** the historical images, the maps, the battle text, the journey toward the ship.

### What it does now (approved v5)
- **M2 (0:07–0:42):** a clean, saturated, modern-looking tricolour fills CENTRE (the generated S6-FLAG, blue restored by
  script).
- **M4 (1:18–1:41):** three FLAT full-wall fields, bright blue / white / red, with LIBERTÉ, ÉGALITÉ, FRATERNITÉ.
- **M6 (2:00–2:16):** the CENTRE tricolour tears; its right half bleaches to white; a tricolour on LEFT
  ("Napoléonistes"), a white flag on RIGHT ("Monarchistes"); all burn.

### The history (researched 3 Oct; sources at the end)
1. **The tricolour holds the king's colour.** 1789: Paris's militia wore blue and red (the city's colours); Lafayette
   added the Bourbon **white** between them. The white in the middle of the tricolour IS the monarchy's colour.
2. **1814:** Napoleon abdicates; the Bourbon king returns; the **plain white flag** replaces the tricolour; the imperial
   eagles are destroyed by royal order.
3. **March 1815, the Hundred Days:** Napoleon returns; the tricolour comes back.
4. **June–July 1815:** Waterloo; the king returns again; **white again until 1830.** In September 1815, 93 eagles and
   their flags are destroyed at Bourges; regiments **cut their own flags into pieces or burned them** rather than
   surrender them.
5. **1815–16, the Second White Terror:** royalist mobs kill Bonapartists and republicans, especially in the south;
   ~6,000 tried, ~70,000 officials purged. **This is why "La France est dangereuse pour moi" (Agnès) and why she
   leaves in 1816.** The audience needs this link; it's what makes the split matter.

So the flag didn't simply tear in two: **it changed colour three times in two years, and the people who kept the wrong
one were hunted.** That's the "instability" the client asks for, and it's true.

### Proposed (Claude's recommendation, for Homie's yes / change)
- **A. One weathered cloth.** The M2 tricolour becomes a **battle-worn regimental colour**: faded silk (indigo to slate,
  madder red to brick), smoke-stained, frayed, holed, a tarnished fringe; **no lettering** (generators write gibberish).
  Made by an **Edit-video pass on the approved S6-FLAG** so the cloth, its folds and its motion stay the ones Homie
  approved; the stains and holes move WITH the folds (physical, not a slide-over texture). Softer by grade on top.
- **B. M4 softened.** No flat colour fields. Each wall becomes **coloured light in the smoke, dim and textured** (like
  dyed linen held to a lamp), the words kept. Script, 0 credits.
- **C. M6 rebuilt on the history: "the flag that can't hold its colours."** After Waterloo, on CENTRE, the same worn
  cloth **loses its blue and red in blotches, like dye running out**, leaving the king's white (the white that was
  always in the middle); the colour **fights back** and drains again (instability, 1814 → 1815 → 1815) and the cloth is
  left white. Then **the split, as it happened:** on LEFT, **pieces of a cut-up tricolour** drift in the smoke
  ("Napoléonistes", the regiments that cut their flags rather than give them up); on RIGHT, **the plain white flag**
  ("Monarchistes"). Then all burn, as now. Script on the generated cloth, 0 credits.
- ~~D. Small dates~~: **dropped (Homie, 3 Oct: "we don't want the small dates").**
- **DECIDED (Homie, 3 Oct): flags only** ("the flag is what we are trying to work on"); no eagle / fleur-de-lis
  prints. **A, B and C approved as the concept** ("happy with your recommendations"). The free preview (step 1) still
  comes before any credit is spent; Homie checks it, then the 48-credit probe.

### Steps and credits
1. **Free preview (0 cr):** M2, M4, M6 with B and C built by script on the CURRENT cloth plus a softening grade, three
   walls side by side, Scene 6 animatic-style. **Homie picks / changes the concept. Nothing is generated before this.**
2. **The weathered cloth, probe (48 cr):** `video_edit` on the first 4 s of `S6-FLAG_v2.mp4` (approved), 1080p, sound on,
   one take. Measure: framing <1 px vs the input, motion kept, the colours faded not changed, no pole, no text.
   Homie sees it.
3. **The full cloth (360 cr):** the same wording on all of `S6-FLAG_v2.mp4` (30 s); loop it (`s6_loops.py`, from the
   edited take alone if the 4 s probe and the 30 s pass don't match at the join).
4. **Re-tune `GenFlag`** (its keying looks for clean white/red/blue), render **S6 v6** at 1080 (show + clean), Homie
   approves.
5. **4K:** upscale the new flag loop (ByteDance, ~3 cr) and re-render Scene 6 at 4K by script (`render_s6 --final`,
   ~4 h, affinity FFFF3FFF); promote under the SAME names, v5 to `04_WORKING_FILES/superseded/`; T9.
**Total ≈ 410 credits** (408 + ~3), inside today's 1,000. Stop rules (`AUTONOMOUS-GEN.md`): two failed takes on the same
defect, stop and ask.

### Watch
Scene 6 opens out of Scene 5's red-brown smoke. If the battlefield's grade changes (task 3), check that the join still
matches; re-grade Scene 6's first seconds only if it doesn't.

---

## 2. SCENE 4 — THE ALPS: remove "the birds"

- **The current files (Homie):** `F:\OrCha Drive\SOR Show Final\SOR SHOW\SOR Renders\Alps\` `AlpsF/L/R/B.mp4`
  (1920x1080 H.264 8-bit, 29.97 fps, 2:00, sound). B = the floor angle. New renders go to D: (`SOTR_MEDIA`).
- **What they probably mean (to confirm):** soft glowing **orbs drifting near the lens** (defocused particles, white and
  green), seen in AlpsF; no actual birds are visible in any of the four files. Still:
  `SOTR_MEDIA/04_WORKING_FILES/meeting4_prep/ALPS_orbs_AlpsF_0m30s.jpg`. **Ask Homie** before building; Louise is also
  preparing notes on the Alps.
- **Method (0 credits):** the camera is locked, so each orb is removed by replacing only its pixels with the same
  pixels from neighbouring frames where the orb isn't (a masked temporal median); everything else stays bit-for-bit
  the original. A Higgsfield edit was ruled out: billed by length (~1,440 cr per 2-min angle) and it repaints the whole
  picture. Re-rendering in Unreal (project on the T9) is the fallback if the orbs cover too much.
- **Deliver:** ProRes 422 HQ, native 29.97, with the sound, as `S4_<WALL>_alps.mov` (+ the floor angle kept separately,
  the floor is unconfirmed); 4K by the usual route if Homie wants (~40 cr).

## 3. SCENE 5 — THE BATTLEFIELD: the grade is too red

- **The current files (Homie):** `F:\...\SOR Renders\Camps\Exports\`: `Camp_Front.mp4` (4:33), `Left.mp4` (2:38),
  `Right.mp4` (0:36), `Bottom.mp4` (0:12), and the cannonball explosion overlays `*_CannonballExplosion.mov` (QuickTime
  RLE with alpha, 7.4 s). **The four angles have different lengths: ask Homie how they're used.** The sky also carries
  birds (dark specks); leave them unless asked.
- **Method (0 credits):** three grade options as stills (less red toward a smoky amber dusk; a cooler grey-smoke dusk; a
  midway), **Homie picks**, then the same grade by script on every angle and on the explosion overlays (alpha kept), so
  the cannonball still sits in the picture. Fire and embers keep their orange.
- **Then check the Scene 6 join** (see Watch, above).
- **Deliver:** as Scene 4.

## Questions for Homie (none block the flag preview)
1. ~~The flag concept~~: A–C approved, flags only (3 Oct). Homie checks the free preview before credits.
2. The Alps "birds" = the floating orbs? (the still)
3. The battlefield: how the four different-length angles are used; which of three grades.
4. Scenes 4 and 5 into `01_FINAL_FOR_SHOW` as show files (ProRes, native 29.97), and 4K?

## Sources (flag history)
- [Flag of France (Wikipedia)](https://en.wikipedia.org/wiki/Flag_of_France) · [Cockade of France](https://en.wikipedia.org/wiki/Cockade_of_France)
- [How a desperate 1789 compromise gave France its tricolour](https://historycollection.com/french-revolution-flag-tricolor-origin-history/)
- [First Restoration](https://en.wikipedia.org/wiki/First_Restoration) · [Bourbon Restoration](https://en.wikipedia.org/wiki/Bourbon_Restoration)
- [French regimental flags under the First Empire (FOTW)](https://www.crwflags.com/fotw/flags/fr%5Er_1e.html)
- [Second White Terror](https://en.wikipedia.org/wiki/Second_White_Terror)
