@echo off
setlocal EnableExtensions

cd /d "%~dp0"

set "PYTHONNOUSERSITE=1"
set "RUN_DIR=%CD%\.samaj"
set "LOG_DIR=%RUN_DIR%\logs"
set "SHUTDOWN_LOG=%LOG_DIR%\shutdown.log"

if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
echo %DATE% %TIME% Stopping Samaj GUI process for this project...>>"%SHUTDOWN_LOG%"

echo Stopping Samaj GUI process for this project...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference = 'Stop';" ^
  "$root = (Resolve-Path '.').Path;" ^
  "$python = Join-Path $root '.venv\Scripts\python.exe';" ^
  "$pidFile = Join-Path $root '.samaj\samaj.pid';" ^
  "$processes = @();" ^
  "if (Test-Path $pidFile) {" ^
  "  $rawPid = Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1;" ^
  "  if ($rawPid -match '^\d+$') {" ^
  "    $candidate = Get-CimInstance Win32_Process -Filter \"ProcessId=$rawPid\" -ErrorAction SilentlyContinue;" ^
  "    if ($candidate -and $candidate.ExecutablePath -eq $python -and $candidate.CommandLine -match '-m\s+samaj') {" ^
  "      $processes += $candidate;" ^
  "    }" ^
  "  }" ^
  "}" ^
  "if (-not $processes) {" ^
  "  $processes = Get-CimInstance Win32_Process | Where-Object { $_.ExecutablePath -eq $python -and $_.CommandLine -match '-m\s+samaj' };" ^
  "}" ^
  "if (-not $processes) {" ^
  "  if (Test-Path $pidFile) { Remove-Item $pidFile -Force -ErrorAction SilentlyContinue };" ^
  "  Add-Content -Path (Join-Path $root '.samaj\logs\shutdown.log') -Value 'No matching Samaj process found.';" ^
  "  Write-Host 'No Samaj GUI process found for this project.';" ^
  "  exit 0;" ^
  "}" ^
  "foreach ($process in $processes) {" ^
  "  Stop-Process -Id $process.ProcessId -ErrorAction Stop;" ^
  "  Add-Content -Path (Join-Path $root '.samaj\logs\shutdown.log') -Value \"Stopped PID $($process.ProcessId).\";" ^
  "  Write-Host \"Stopped Samaj GUI process $($process.ProcessId).\";" ^
  "}" ^
  "if (Test-Path $pidFile) { Remove-Item $pidFile -Force -ErrorAction SilentlyContinue };"

exit /b %ERRORLEVEL%
