#!/bin/bash
# RAFT5 water motion watchdog (run from the repo root): DONE, failure, or a dead job (relaunch once).
D=/c/Users/Homie/Documents/SOTR_MEDIA/04_WORKING_FILES/S9_raft/water_motion_test
declare -A fin; declare -A tries; declare -A seen
while true; do
  alldone=1
  for t in ${TAGS:-B24blur C48 D5994flow}; do
    [ -n "${fin[$t]}" ] && continue; alldone=0; L=$D/_LOG_$t.txt
    if grep -qE "Traceback|Error" "$L"; then echo "$t FAILED: $(tail -n 3 "$L" | tr '\n' ' ')"; fin[$t]=1; continue; fi
    if grep -q DONE "$L"; then echo "$t $(grep DONE "$L")"; fin[$t]=1; continue; fi
    m=$(stat -c %Y "$L"); now=$(date +%s)
    if [ $((now - m)) -gt 900 ]; then
      tries[$t]=$(( ${tries[$t]:-0} + 1 ))
      if [ ${tries[$t]} -le 1 ]; then echo "$t STALLED (log 15 min old) -> relaunch"; powershell -NoProfile -ExecutionPolicy Bypass -File tools/_launch_water_motion.ps1 -Tags $t >/dev/null
      else echo "$t STALLED twice, giving up"; fin[$t]=1; fi
    fi
  done
  [ $alldone = 1 ] && { echo "ALL FINISHED"; exit 0; }
  sleep 30
done
