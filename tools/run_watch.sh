#!/bin/bash
# FINALS 24 Nov: generic watchdog. Runs `python ARGS...` on affinity FFFF3FFF (tools/_launch_aff.ps1), log to $1.
# Relaunches up to 2 times when python dies without DONE. Prints one line per 600 frames, DONE, FAILED or GAVE UP.
# usage: bash tools/run_watch.sh LOG python-args...
LOG=$1; shift
for try in 1 2 3; do
  echo "launch $try: $*" >> "$LOG"
  powershell -NoProfile -ExecutionPolicy Bypass -File tools/_launch_aff.ps1 "$@" >> "$LOG" 2>&1
  rc=$?
  if tail -n 3 "$LOG" | grep -qE "${DONE_RE:-DONE}"; then echo "DONE (try $try): $(tail -n 1 "$LOG")"; exit 0; fi
  echo "DIED rc=$rc try $try: $(tail -n 3 "$LOG" | tr '\n' ' ')"
  grep -q "refusing" "$LOG" && { echo "FAILED: refusing (output exists)"; exit 1; }
done
echo "GAVE UP after 3 tries"; exit 1
