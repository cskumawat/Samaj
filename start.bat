@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

set "ROOT=%CD%"
set "VENV_DIR=%ROOT%\.venv"
set "PYTHON_EXE=%VENV_DIR%\Scripts\python.exe"
set "ACTIVATE_BAT=%VENV_DIR%\Scripts\activate.bat"
set "RUN_DIR=%ROOT%\.samaj"
set "LOG_DIR=%RUN_DIR%\logs"
set "PID_FILE=%RUN_DIR%\samaj.pid"
set "OUT_LOG=%LOG_DIR%\samaj-gui.out.log"
set "ERR_LOG=%LOG_DIR%\samaj-gui.err.log"
set "REQUIREMENTS_FILE=requirements.txt"
set "PYTHONNOUSERSITE=1"
set "SAMAJ_DATA_DIR=%RUN_DIR%"
set "SAMAJ_SETTINGS_PATH=%RUN_DIR%\settings.json"

if /I "%~1"=="--dev" set "REQUIREMENTS_FILE=requirements-dev.txt"

if not exist "%RUN_DIR%" (
    mkdir "%RUN_DIR%"
    if errorlevel 1 exit /b 1
)
if not exist "%LOG_DIR%" (
    mkdir "%LOG_DIR%"
    if errorlevel 1 exit /b 1
)

if not exist "%PYTHON_EXE%" (
    echo Creating local Python virtual environment at "%VENV_DIR%"...
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv "%VENV_DIR%"
    ) else (
        python -m venv "%VENV_DIR%"
    )
    if errorlevel 1 (
        echo Failed to create .venv. Ensure Python 3.11 or newer is installed.
        exit /b 1
    )
)

call "%ACTIVATE_BAT%"
if errorlevel 1 (
    echo Failed to activate "%ACTIVATE_BAT%".
    exit /b 1
)

echo Upgrading pip inside .venv...
"%PYTHON_EXE%" -m pip install --upgrade pip
if errorlevel 1 exit /b 1

echo Installing/updating %REQUIREMENTS_FILE% inside .venv...
"%PYTHON_EXE%" -m pip install -r "%REQUIREMENTS_FILE%"
if errorlevel 1 exit /b 1

echo Starting Samaj GUI from .venv...
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$ErrorActionPreference = 'Stop';" ^
  "$root = (Resolve-Path '.').Path;" ^
  "$python = Join-Path $root '.venv\Scripts\python.exe';" ^
  "$runDir = Join-Path $root '.samaj';" ^
  "$logDir = Join-Path $runDir 'logs';" ^
  "$pidFile = Join-Path $runDir 'samaj.pid';" ^
  "$outLog = Join-Path $logDir 'samaj-gui.out.log';" ^
  "$errLog = Join-Path $logDir 'samaj-gui.err.log';" ^
  "New-Item -ItemType Directory -Force -Path $logDir | Out-Null;" ^
  "if (Test-Path $pidFile) {" ^
  "  $rawPid = Get-Content $pidFile -ErrorAction SilentlyContinue | Select-Object -First 1;" ^
  "  if ($rawPid -match '^\d+$') {" ^
  "    $existing = Get-CimInstance Win32_Process -Filter \"ProcessId=$rawPid\" -ErrorAction SilentlyContinue;" ^
  "    if ($existing -and $existing.ExecutablePath -eq $python -and $existing.CommandLine -match '-m\s+samaj') {" ^
  "      Write-Host \"Samaj is already running with PID $rawPid.\";" ^
  "      exit 0;" ^
  "    }" ^
  "  }" ^
  "  Remove-Item $pidFile -Force -ErrorAction SilentlyContinue;" ^
  "}" ^
  "$process = Start-Process -FilePath $python -ArgumentList @('-m','samaj') -WorkingDirectory $root -RedirectStandardOutput $outLog -RedirectStandardError $errLog -PassThru;" ^
  "Start-Sleep -Seconds 2;" ^
  "$live = Get-Process -Id $process.Id -ErrorAction SilentlyContinue;" ^
  "if (-not $live) {" ^
  "  Write-Host 'Samaj exited during startup. Last stderr lines:';" ^
  "  if (Test-Path $errLog) { Get-Content $errLog -Tail 20 };" ^
  "  exit 1;" ^
  "}" ^
  "Set-Content -Path $pidFile -Value $process.Id -Encoding ascii;" ^
  "Write-Host \"Samaj started with PID $($process.Id).\";" ^
  "Write-Host \"Logs: $outLog and $errLog\";"

exit /b %ERRORLEVEL%
