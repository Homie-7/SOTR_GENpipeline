#!/bin/bash
# M10b FLOW3 watchdog: one line per log change (progress every 120 frames), DONE, failure, or a dead python with no DONE.
D=/c/Users/Homie/Documents/SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review
declare -A last; declare -A fin; declare -A PIDS=([3]=${P3:-45304} [5]=${P5:-49476} [7]=${P7:-46728})
while true; do
  alldone=1
  for b in ${BEATS:-3 5cut 7}; do
    L=$D/_LOG_FLOW3_b$b.txt
    [ -n "${fin[$b]}" ] && continue
    alldone=0
    t=$(tail -n 1 "$L" 2>/dev/null)
    if grep -qE "Traceback|Error|failed|refusing" "$L" 2>/dev/null; then echo "b$b FAILED: $(tail -n 3 "$L" | tr '\n' ' ')"; fin[$b]=1; continue; fi
    if echo "$t" | grep -q DONE; then echo "b$b DONE: $t"; fin[$b]=1; continue; fi
    if [ "$t" != "${last[$b]}" ]; then last[$b]="$t"; case "$t" in *"0 frames"*) n=${t%% *}; [ $((n % 600)) -eq 0 ] && echo "b$b $t";; esac; fi
    pid=${PIDS[$b]}; n=$(tasklist //FI "PID eq $pid" //NH | grep -c python)
    if [ "${n:-0}" = "0" ]; then sleep 5; grep -q DONE "$L" || { echo "b$b LAUNCHER DEAD (no python, no DONE): $t"; fin[$b]=1; }; fi
  done
  [ $alldone = 1 ] && { echo "ALL FINISHED"; exit 0; }
  sleep 30
done
