#!/bin/bash
# M10d FLOW5 watchdog (auto-relaunch x2, run from the repo root): one line per log change (progress every 120 frames), DONE, failure, or a dead python with no DONE.
D=/c/Users/Homie/Documents/SOTR_MEDIA/04_WORKING_FILES/S9_gen_judge_review
declare -A last; declare -A tries; declare -A fin; declare -A PIDS=([3]=${P3:-45304} [5]=${P5:-49476} [7]=${P7:-46728} [5cut]=${P5:-0})
while true; do
  alldone=1
  for b in ${BEATS:-3 5cut 7}; do
    L=$D/_LOG_FLOW5_b$b.txt
    [ -n "${fin[$b]}" ] && continue
    alldone=0
    t=$(tail -n 1 "$L" 2>/dev/null)
    if grep -qE "Traceback|Error|failed|refusing" "$L" 2>/dev/null; then echo "b$b FAILED: $(tail -n 3 "$L" | tr '\n' ' ')"; fin[$b]=1; continue; fi
    if echo "$t" | grep -q DONE; then echo "b$b DONE: $t"; fin[$b]=1; continue; fi
    if [ "$t" != "${last[$b]}" ]; then last[$b]="$t"; case "$t" in *"0 frames"*) n=${t%% *}; [ $((n % 600)) -eq 0 ] && echo "b$b $t";; esac; fi
    pid=${PIDS[$b]}; n=$(tasklist //FI "PID eq $pid" //NH | grep -c python)
    if [ "${n:-0}" = "0" ]; then sleep 5; grep -q DONE "$L" || {
      tries[$b]=$(( ${tries[$b]:-0} + 1 ))
      if [ ${tries[$b]} -le 2 ]; then
        echo "b$b LAUNCHER DEAD at: $t -> relaunch ${tries[$b]}"
        np=$(powershell -NoProfile -ExecutionPolicy Bypass -File tools/_launch_flow5_m10d.ps1 -Beats $b | grep "python pid" | tail -n 1 | awk '{print $NF}')
        PIDS[$b]=$np; last[$b]=""
      else echo "b$b LAUNCHER DEAD twice, giving up: $t"; fin[$b]=1; fi; }; fi
  done
  [ $alldone = 1 ] && { echo "ALL FINISHED"; exit 0; }
  sleep 30
done
