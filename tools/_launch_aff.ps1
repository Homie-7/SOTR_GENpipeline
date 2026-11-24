# Run python with the given args on affinity FFFF3FFF (Core 7 off; the 5950X WHEA crash). Exit code passes through.
$p = Start-Process python -ArgumentList $args -NoNewWindow -PassThru
$null = $p.Handle
try { $p.ProcessorAffinity = [IntPtr][long]4294918143 } catch { Write-Output "affinity not set: $_" }
$p.WaitForExit()
exit $p.ExitCode
