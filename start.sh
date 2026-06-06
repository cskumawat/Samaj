#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VENV_DIR="$ROOT/.venv"
PYTHON_EXE="$VENV_DIR/bin/python"
RUN_DIR="$ROOT/.samaj"
LOG_DIR="$RUN_DIR/logs"
PID_FILE="$RUN_DIR/samaj.pid"
OUT_LOG="$LOG_DIR/samaj-gui.out.log"
ERR_LOG="$LOG_DIR/samaj-gui.err.log"
REQUIREMENTS_FILE="requirements.txt"

if [[ "${1:-}" == "--dev" ]]; then
  REQUIREMENTS_FILE="requirements-dev.txt"
fi

mkdir -p "$LOG_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required." >&2
  exit 1
fi

if [[ ! -x "$PYTHON_EXE" ]]; then
  echo "Creating local Python virtual environment at $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
export PYTHONNOUSERSITE=1
export SAMAJ_DATA_DIR="$RUN_DIR"
export SAMAJ_SETTINGS_PATH="$RUN_DIR/settings.json"

"$PYTHON_EXE" -m pip install --upgrade pip
"$PYTHON_EXE" -m pip install -r "$REQUIREMENTS_FILE"

if [[ -f "$PID_FILE" ]]; then
  existing_pid="$(cat "$PID_FILE" || true)"
  if [[ "$existing_pid" =~ ^[0-9]+$ ]] && kill -0 "$existing_pid" >/dev/null 2>&1; then
    command_line="$(ps -p "$existing_pid" -o command= || true)"
    if [[ "$command_line" == *"$PYTHON_EXE -m samaj"* ]]; then
      echo "Samaj is already running with PID $existing_pid."
      exit 0
    fi
  fi
  rm -f "$PID_FILE"
fi

nohup "$PYTHON_EXE" -m samaj >"$OUT_LOG" 2>"$ERR_LOG" &
pid="$!"
sleep 2
if ! kill -0 "$pid" >/dev/null 2>&1; then
  echo "Samaj exited during startup. Last stderr lines:" >&2
  tail -20 "$ERR_LOG" >&2 || true
  exit 1
fi

echo "$pid" > "$PID_FILE"
echo "Samaj started with PID $pid."
echo "Logs: $OUT_LOG and $ERR_LOG"
