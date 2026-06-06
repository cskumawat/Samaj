#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

VENV_PYTHON="$ROOT/.venv/bin/python"
RUN_DIR="$ROOT/.samaj"
LOG_DIR="$RUN_DIR/logs"
PID_FILE="$RUN_DIR/samaj.pid"
SHUTDOWN_LOG="$LOG_DIR/shutdown.log"

mkdir -p "$LOG_DIR"
echo "$(date -Is) Stopping Samaj GUI process for this project..." >> "$SHUTDOWN_LOG"

if [[ ! -f "$PID_FILE" ]]; then
  echo "No Samaj PID file found."
  echo "$(date -Is) No PID file found." >> "$SHUTDOWN_LOG"
  exit 0
fi

pid="$(cat "$PID_FILE" || true)"
if [[ ! "$pid" =~ ^[0-9]+$ ]]; then
  rm -f "$PID_FILE"
  echo "Invalid PID file removed."
  echo "$(date -Is) Invalid PID file removed." >> "$SHUTDOWN_LOG"
  exit 0
fi

if ! kill -0 "$pid" >/dev/null 2>&1; then
  rm -f "$PID_FILE"
  echo "No Samaj GUI process found for this project."
  echo "$(date -Is) Stale PID removed: $pid." >> "$SHUTDOWN_LOG"
  exit 0
fi

command_line="$(ps -p "$pid" -o command= || true)"
if [[ "$command_line" != *"$VENV_PYTHON -m samaj"* ]]; then
  rm -f "$PID_FILE"
  echo "PID does not match this project's Samaj process. Removed stale PID."
  echo "$(date -Is) PID mismatch removed: $pid." >> "$SHUTDOWN_LOG"
  exit 0
fi

kill "$pid"
rm -f "$PID_FILE"
echo "Stopped Samaj GUI process $pid."
echo "$(date -Is) Stopped PID $pid." >> "$SHUTDOWN_LOG"
