#!/bin/bash
# NIGHT SHIFT: resume the working Claude Code session every 30 min (launchd), so a usage-limit stop doesn't waste the
# night (Homie, 5 Oct 2026: "every 30 mins run a command and see if the usage has been reset and then it starts again").
#
#   tools/night_shift.sh            one tick (launchd calls this every 1800 s)
#   tools/night_shift.sh --check    environment check only: T9, CLI, auth (a tiny fresh call, never the session)
#
# A tick does NOTHING when: the STOP file exists; it is past STOP_AT; another tick is still running; or the session's
# transcript changed in the last 20 min (the session is alive, so two copies would collide). Otherwise it resumes the
# session headless in the same 'auto' permission mode, with the night-shift brief below. If the usage limit is still
# on, the call just fails and the next tick tries again.
# STOP IT: touch "$REPO/NIGHT_SHIFT_STOP"   or   launchctl unload ~/Library/LaunchAgents/com.homie.sotr-nightshift.plist
export PATH=/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
REPO=/Users/homie/Documents/SOTR_GENpipeline
SESSION=aaee6a9e-0782-4fa5-b344-6b742ecc43ad
TRANSCRIPT=/Users/homie/.claude/projects/-Users-homie-Documents-SOTR-GENpipeline/$SESSION.jsonl
CLAUDE=$(ls -d /Users/homie/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude 2>/dev/null | tail -1)
STOP_AT=202610061000          # YYYYMMDDhhmm: Higgsfield credits expire 6 Oct; no ticks after 10:00
LOG=$REPO/../SOTR_night_shift.log
LOCK=/tmp/sotr_night_shift.lock
cd "$REPO" || exit 1
say() { echo "$(date '+%F %T') $*" >> "$LOG"; }

if [ "$1" = "--check" ]; then
  say "CHECK: claude=$CLAUDE"
  ls "/Volumes/DMD T9/SOTR/HF/SOTR_MEDIA/04_WORKING_FILES/S7_ship" >/dev/null 2>&1 && say "CHECK: T9 readable" || say "CHECK: T9 NOT readable"
  out=$("$CLAUDE" -p "Reply with the single word OK." --model haiku 2>&1 | tail -1)
  say "CHECK: headless reply: $out"
  exit 0
fi
[ -f "$REPO/NIGHT_SHIFT_STOP" ] && { say "skip: STOP file"; exit 0; }
[ "$(date +%Y%m%d%H%M)" -gt "$STOP_AT" ] && { say "skip: past $STOP_AT"; exit 0; }
if [ -f "$LOCK" ] && kill -0 "$(cat "$LOCK")" 2>/dev/null; then say "skip: a tick is still running"; exit 0; fi
age=$(( $(date +%s) - $(stat -f %m "$TRANSCRIPT") ))
[ "$age" -lt 1200 ] && { say "skip: session active (transcript ${age}s old)"; exit 0; }
echo $$ > "$LOCK"
say "RESUME (transcript idle ${age}s)"
"$CLAUDE" -p --resume "$SESSION" --permission-mode auto \
  "NIGHT SHIFT (automated resume by tools/night_shift.sh; Homie is asleep and delegated the calls). Continue the ship \
sequence exactly where you stopped: docs/NEW-SESSION.md 'THE TASK, RIGHT NOW' and docs/PLAN-SHIP-INTRO.md. Keep every \
rule: AUTONOMOUS-GEN pre-flight, ONE Higgsfield job at a time, get_cost first, check transactions after, a 4 s probe \
before any long take, stop a line of work after two failed versions of the same defect, never delete. Higgsfield \
credits expire 6 Oct, so spend them on the plan, not on retries. Before you stop for any reason: update LOG.md, \
REGISTER.md and NEW-SESSION.md, commit and push, back up new media to the T9 (it is the media's home here). When the \
plan is finished or nothing useful is left, create the file NIGHT_SHIFT_STOP in the repo root." >> "$LOG" 2>&1
say "tick ended (exit $?)"
rm -f "$LOCK"
