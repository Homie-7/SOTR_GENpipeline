# AUTONOMOUS-GEN — how Claude runs Higgsfield unattended without wasting credits

Set 2026-09-24 with Homie. He connected Higgsfield as a claude.ai connector
(`https://mcp.higgsfield.ai/mcp`) so Claude can generate while he's away. **Scope:
generation only.** Compositing stays his. **Budget: 1,000 credits per session, hard stop.**
His brief: *"be as efficient as possible… the prompts you generate will basically improve."*

This file is the system. Read it before the first Higgsfield call of any session.

---

## 0 · First session only: the connector gate (nothing else runs until it passes)

1. **List the tools** the Higgsfield connector exposes and their parameters. Record them in
   `PIPELINE.md`.
2. **Check the four gaps.** Any "no" is a stop: tell Homie and keep using the web app.
   - References mode with a **local image**, or a Higgsfield-hosted copy of the plate
   - Every setting we use: **4:3, 10 s, 1080p, quality High, batch, sound on**
   - It returns the **full file** (1664x1248, HEVC 10-bit), not a preview
   - It reports the **cost** per run, or the balance before and after
3. **Parity test (~120 credits).** Re-run `prompts/S9-SAL-R-LOOP.txt` exactly as it was
   approved. Compare it with `02_APPROVED_BUILDING_BLOCKS/clips/loc_SOTR_salon_R_loop_s9_v1.mp4`: same size, fps and
   bit depth, the same camera lock, flame count, and halo-motion level within the normal
   variation between runs. Pass = the MCP is the same tool as the web app. Log it.

## 1 · Before every run: the pre-flight (it costs nothing and catches most waste)

- [ ] **One change** against the last version, named in the file header. A rewrite of
  several blocks counts as many changes (the snuff v2 lesson, below).
- [ ] **Diff the prompt body** against the previous version. Only the intended lines differ.
- [ ] The prompt body is **under 2,000 characters**.
- [ ] **Reference = the approved plate** by its current filename (no `@` in filenames).
- [ ] The settings match the file header: model, aspect, resolution, duration, quality,
  batch, sound.
- [ ] **Predict the result in one line** before running it ("expect the halos to swing about
  2x"). A run with no prediction teaches nothing.
- [ ] **Credits:** the running total plus this run stays at or under 1,000.

## 2 · Spend in the cheapest order

1. **Probe short.** Test a new wording at **4 s (~48 credits)** before committing to 10 s
   (~120). Motion character, lock, framing and object behaviour all show in 4 s. Only
   drift and loop behaviour need the full length.
2. **Batch 2 when the question is luck.** If a result might be chance (a good snuff in one
   take), batch 2 at 4 s (~96) answers it for less than one 10 s rerun.
3. **Batch 1 when the question is wording.** One change, one take, measure.
4. **Full 10 s only for a candidate**, meaning a probe that already passed.
5. **Never regenerate for something `tools/loop_halo.py` fixes by script**: slow drift,
   the first-frame reference copy, looping, amplitude. That isn't Homie's comp work, and
   it costs no credits.

## 3 · After every run: measure, don't eyeball

The same checks every time, from the saved file:
- probe: size, fps, frames, bit depth, audio
- **camera lock** (phase correlation, first/middle/last frame, must be 0 px)
- **framing against the plate** (landmark positions within about 1%)
- **motion by region** (flicker by speed after removing the drift, swing, sway, a motion
  heat-map), compared with the last version's numbers
- **object checks** (flame count, a still portrait, a blank canvas, no floor, no people)
- a contact sheet of frames across the whole clip (lesson 8: never judge from one frame)
- for loops: a loop preview built with `loop_halo.py`, with the join checked

**The metrics catch technical faults. They don't catch taste.** "Over the top" and "looks
AI" were Homie's eye on the snuff, and nothing measured flagged them. So any result that
passes the numbers goes to Homie as a preview; it's never approved by Claude.

## 4 · Stop rules

- **1,000 credits spent**, so stop and write the handover.
- **Two failed versions on the same defect for different-looking reasons**, so stop
  rewording and ask what the design makes impossible (lesson 6), then take it to Homie.
- **Any look or story question** is queued for Homie with a recommendation. It's never
  resolved unattended (lesson 5).
- **Anything unexpected from the connector** (errors, a changed menu, a cost jump) means
  stop.

## 5 · Filing (standing rule, Homie 2026-09-24)

- An untested or pending take goes in `03_TESTS_IN_PROGRESS/<PROMPT-ID>_v<N>.mp4`.
- A rejected take moves to `04_REJECTED/<PROMPT-ID>_v<N>.mp4`.
- **Approved by Homie:** rename it to the tag without the `@`
  (`loc_SOTR_<world>_<wall>_loop_s9_v<N>.mp4`), render `<tag>_comp.mov` with
  `loop_halo.py` if it's a loop, and add it to REGISTER.
- Checksum every move. Every run gets a LOG row, including its credit cost.

## 6 · What today taught (the prompt-writing rules this system enforces)

| Lesson | Evidence |
|---|---|
| **Calming words freeze a clip.** "gentle, small, constant, steady, as still as stone" is read as "don't move". Ask for the motion vividly; the camera lock alone holds the frame | studio v1: 4% global breath, "a static image". v2 with vivid wording: 17% swing, 370 mm sway |
| **Exaggeration words blow it up.** "full, clearly visible, higher, spreading" becomes cartoon volume | snuff v1: clouds a metre above the sconces |
| **A rewrite loses what worked.** Patch the one failing phrase and keep every other word | snuff v2 rewrote 4 blocks and lost v1's crisp snuff |
| **One take can't separate wording from luck** | every run today was batch 1, so the snuff v1 result is unexplained |
| **Seedance adds drift over 10 s** (salon -3%, studio v2 +7%), and frame 0 is a copy of the reference | fixed by `loop_halo.py`, never regenerate for it |
| **Seedance may start the scene before the reference** (the snuff clips open LIT from a DARK reference) | harmless, trimmed; note it rather than fight it |
| **Scale check before judging motion:** a flame is about 8 px and a dust mote 1-3 px in a 1080p loop. Anything under about 50 px moving reads as still from the seats | salon halos, studio dust |
