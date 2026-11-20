# M9w: launch the three FLOW beats detached, affinity FFFF3FFF (Core 7 off), logs beside the outputs.
param([string[]]$Beats = @('3','5cut','7'))
$repo = 'C:\Users\Homie\Documents\SOTR_GENpipeline'
$dir  = 'C:\Users\Homie\Documents\SOTR_MEDIA\04_WORKING_FILES\S9_gen_judge_review'
$names = @{ '3'='S9_b3_CENTRE_court_GENJUDGE_FLOW.mp4'; '5cut'='S9_b5_CENTRE_court_GENJUDGE_FLOW_DARREN-CUT.mp4'; '7'='S9_b7_CENTRE_court_GENJUDGE_FLOW.mp4' }
foreach ($b in $Beats) {
  $out = Join-Path $dir $names[$b]
  $log = Join-Path $dir ("_LOG_FLOW_b$b.txt")
  $p = Start-Process -FilePath 'cmd.exe' -ArgumentList "/c python tools\court_gen_flow.py render `"$out`" --beat $b > `"$log`" 2>&1" -WorkingDirectory $repo -WindowStyle Hidden -PassThru
  Start-Sleep -Milliseconds 1500
  Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" | ForEach-Object { (Get-Process -Id $_.ProcessId).ProcessorAffinity = [IntPtr][long]4294918143; "b$b python pid $($_.ProcessId)" }
  $p.ProcessorAffinity = [IntPtr][long]4294918143
  "b$b cmd pid $($p.Id) -> $out"
}
