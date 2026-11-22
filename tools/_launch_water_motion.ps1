# RAFT5: water motion tests (shutter blur / 48 / 59.94 flow), detached, affinity FFFF3FFF (Core 7 off).
param([string[]]$Tags = @('B24blur','C48','D5994flow'))
$repo = 'C:\Users\Homie\Documents\SOTR_GENpipeline'
$dir  = 'C:\Users\Homie\Documents\SOTR_MEDIA\04_WORKING_FILES\S9_raft\water_motion_test'
$src  = 'G:\SOTR\HF\Final changes\221126\aerial-view-of-turquoise-ocean-waters-2026-10-02-17-18-47-utc.mov'
$args_ = @{ 'B24blur'='--fps 24 --shutter 2'; 'C48'='--fps 48'; 'D5994flow'='--fps 59.94 --flow' }
foreach ($t in $Tags) {
  $log = Join-Path $dir ("_LOG_$t.txt")
  $p = Start-Process -FilePath 'cmd.exe' -ArgumentList "/c python tools\raft_water_motion.py `"$src`" `"$dir`" --tag $t $($args_[$t]) > `"$log`" 2>&1" -WorkingDirectory $repo -WindowStyle Hidden -PassThru
  Start-Sleep -Milliseconds 1500
  Get-CimInstance Win32_Process -Filter "ParentProcessId=$($p.Id)" | ForEach-Object { (Get-Process -Id $_.ProcessId).ProcessorAffinity = [IntPtr][long]4294918143; "$t python pid $($_.ProcessId)" }
  $p.ProcessorAffinity = [IntPtr][long]4294918143
}
