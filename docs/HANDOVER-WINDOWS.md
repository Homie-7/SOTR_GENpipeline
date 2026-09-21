# Handover: continuing on the Windows PC

Everything that matters lives in this repo, except two things that git can't carry: **the
production skills** (a separate repo) and **the source folder** (copyrighted script and
media). The one-time setup below covers both. After that, every session is just "pull,
open, paste."

---

## One-time setup (about 15 minutes)

### 1. Tools

Install these if they aren't already there. Accept the defaults.

- **Git for Windows**: https://git-scm.com. It includes Git Bash, which is what you should
  use for the commands below.
- **Python 3**: https://python.org. Tick "Add python.exe to PATH" during install.
- **Node.js LTS**: https://nodejs.org.
- **Claude Code**, in Git Bash:
  ```bash
  npm install -g @anthropic-ai/claude-code
  claude --version
  ```

### 2. The production skills (house-rules and the vendored skills)

```bash
cd ~/Documents
git clone https://github.com/Homie-7/Precision-Pipeline.git
cd Precision-Pipeline
python bin/install.py --copy
```

`--copy` is the Windows mode: skills are **copied** into `~/.claude/skills/`, not linked. So
**if the skills change on the Mac later**, run `git pull` in `Precision-Pipeline`, then
`python bin/install.py --copy` again.

### 3. This repo

```bash
cd ~/Documents
git clone https://github.com/Homie-7/SOTR_GENpipeline.git
```

### 4. The source folder

**Not in git.** Copy the whole Mac folder `/Users/homie/Documents/SOTR/` to the PC (SSD,
OneDrive, whatever's easiest). **Put it at `Documents\SOTR\`**, so the layout matches
`docs/SOURCES.md`. It's about 210 MB, with two dev-showing videos, the script, the
schedule, the staging plan and the reference images.

Then add the Windows path to `docs/SOURCES.md` and commit it, so both machines know where
it lives.

### 5. The client PDF (optional)

`docs/SOTR-Scene9-Projection-Direction.pdf` is the direction document for the client. PDFs
are gitignored, so it **doesn't come with the clone**. Either copy it across with the
source folder, or rebuild it on the PC:

```bash
pip install reportlab
python tools/make_client_pdf.py docs/SOTR-Scene9-Projection-Direction.pdf
```

To change the wording, edit `tools/make_client_pdf.py` and rebuild. Its rules: plain
language, no dashes, no names, Scene 9 only.

### 6. Higgsfield

Higgsfield comes in through the claude.ai connector on your account. **Log into Claude Code
with the same account** you use on the Mac, then in a session run `/mcp` to confirm
Higgsfield is listed and connected. If it isn't, reconnect it in claude.ai → Settings →
Connectors.

---

## Every session

```bash
cd ~/Documents/SOTR_GENpipeline
git pull
claude
```

Paste the block from `docs/NEW-SESSION.md` as the first message. At the end, type `wrap`.
Claude updates the log and the handover, commits and pushes.

**One machine at a time.** Push on the Mac before opening on the PC, and the other way
round. Two sessions editing this repo at once silently overwrite each other.

## What doesn't travel through git

| Thing | How it gets to the PC |
|---|---|
| Source folder (script, plans, references) | Copy by hand, step 4 |
| Generated plates and loops | SSD or OneDrive, see below |
| The client PDF | Copy it, or rebuild it (step 5) |
| Claude's memory from the Mac | Doesn't need to travel. The standing decisions are in `CLAUDE.md`, `STAGE.md` and `docs/NEW-SESSION.md` |

## Where generated media goes

Pick one working folder for plates and loops (outside the repo, since media never goes in
git), and record it in `docs/SOURCES.md` → "Working folder." If you move between machines,
the media travels by SSD or OneDrive, the same way *First Day on the Job* worked. The repo
only carries the text.
