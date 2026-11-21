# M10d: launch FLOW4 beats (raw v8 READ, v10 raise that ends on the f40 pose, flow-warp joins) detached, affinity FFFF3FFF (Core 7 off).
param([string[]]$Beats = @('5cut','7'))
$repo = 'C:\Users\Homie\Documents\SOTR_GENpipeline'
$dir  = 'C:\Users\Homie\Documents\SOTR_MEDIA\04_WORKING_FILES\S9_gen_judge_review'
$names = @{ '5cut'='S9_b5_CENTRE_court_GENJUDGE_FLOW4_FULL.mp4'; '7'='S9_b7_CENTRE_court_GENJUDGE_FLOW4.mp4' }
$extra = @{ '5cut'='--full --raise-v10'; '7'='--raise-v10' }
foreach ($b in $Beats) {
  $out = Join-Path $dir $names[$b]
  $log = Join-Path $dir ("_LOG_FLOW4_b$b.txt")
  $p = Start-Process -FilePath 'cmd.exe' -ArgumentList "/c python tools\court_gen_flow.py render `"$out`" --beat $b $($extra[$b]) > `"$log`" 2>&1" -WorkingDirectory $repo -WindowStyle Hidden -PassThru
  Start-Sleep -Milliseconds 1500
  Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" | ForEach-Object { (Get-Process -Id $_.ProcessId).ProcessorAffinity = [IntPtr][long]4294918143; "b$b python pid $($_.ProcessId)" }
  $p.ProcessorAffinity = [IntPtr][long]4294918143
  "b$b cmd pid $($p.Id) -> $out"
}
