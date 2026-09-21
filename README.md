# SOTR_GENpipeline

Projection backgrounds for **Secret of the Raft** (ReAction Theatre, RMIT Black Box 2026),
built in Higgsfield. Project code `SOTR`.

This repo holds the markdown only: canon, staging spec, look, cue cards, prompts, log.
Images and video never go in git (see `.gitignore`).

## Scope (as of 2026-09-21)

Scene 9, "The Aftermath". Three worlds, owned by Homie:

1. **Court Martial**: an abstract black silhouette of the judge
2. **The Salon**: Marie-Louise's Restoration salon
3. **Géricault's studio**: Paris, 1818–19

Once these three land, more scenes may be added. The deadline for these three is about one
week from 2026-09-21.

## Files

| File | What it is |
|---|---|
| `CLAUDE.md` | Loads automatically in Claude Code. Rules, authority order, current stage. |
| `STAGE.md` | **The set and the render spec.** Three surfaces, locked cameras, true scale. Read first. |
| `PIPELINE.md` | The 10 steps every world goes through, from card to 4K delivery. |
| `BIBLE.md` | The play: story, characters, Scene 9 structure, era. |
| `LOOK.md` | Per-world look, and the fragment-transition language. |
| `SHOTCARDS.md` | Cue cards. Every plate and loop, by ID. |
| `REGISTER.md` | What exists and what's approved. |
| `LOG.md` | Every generation, one row. |
| `prompts/` | Final prompt text, by cue ID. |
| `docs/NEW-SESSION.md` | Paste-in opener for a fresh Claude Code session. |
| `docs/SOURCES.md` | Where the source material lives (not in git). |
| `tools/make_client_pdf.py` | Builds the client direction PDF (the PDF itself stays out of git). |

## Setting up on another machine

**Windows PC:** follow `docs/HANDOVER-WINDOWS.md`. Mac or anything else:

The production skills (`house-rules`, `banana-pro-director-30`, `cinema-director-v3`, etc.)
live in the separate `Precision-Pipeline` repo. Install them once:

```bash
git clone https://github.com/Homie-7/Precision-Pipeline.git
cd Precision-Pipeline && python3 bin/install.py     # symlinks skills into ~/.claude/skills
npm install -g @anthropic-ai/claude-code            # if `claude` isn't found
```

Then:

```bash
git clone https://github.com/Homie-7/SOTR_GENpipeline.git
cd SOTR_GENpipeline && claude
```

Paste the block from `docs/NEW-SESSION.md` as the first message.
