#!/usr/bin/env bash
set -euo pipefail

VENV_DIR=".venv"
REQ="requirements.txt"

echo "Select target environment:"
echo "  1) macOS / Linux (bash)"
echo "  2) Windows (.bat)"
read -r -p "Enter 1 or 2: " CHOICE

if [ "$CHOICE" = "1" ]; then
  # macOS / Linux flow: create venv if missing, install requirements, run app using the venv python
  PY=python3
  if ! command -v "$PY" >/dev/null 2>&1; then
    if command -v python >/dev/null 2>&1; then
      PY=python
    else
      echo "Python not found. Install Python first." >&2
      exit 1
    fi
  fi

  if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv in $VENV_DIR..."
    "$PY" -m venv "$VENV_DIR"
  fi

  PIP="$VENV_DIR/bin/pip"
  PY_VENV="$VENV_DIR/bin/python"

  echo "Upgrading pip..."
  "$PIP" install --upgrade pip

  if [ -f "$REQ" ]; then
    echo "Installing requirements from $REQ..."
    "$PIP" install -r "$REQ"
  else
    echo "No requirements.txt found; skipping pip install."
  fi

  echo "Launching app with $PY_VENV..."
  exec "$PY_VENV" app.py

  elif [ "$CHOICE" = "2" ]; then
  # Windows: create a .bat launcher file and try to run it if cmd.exe exists.
  BAT_FILE="local_app.bat"
  cat > "$BAT_FILE" <<'BAT'
@echo off
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
if exist requirements.txt (
  pip install -r requirements.txt
)
python app.py
BAT

  echo "Wrote $BAT_FILE."

  if command -v cmd.exe >/dev/null 2>&1; then
    echo "Running $BAT_FILE via cmd.exe..."
    cmd.exe /c "%CD%\%BAT_FILE%"
  else
    echo "cmd.exe not found on this machine."
    echo "To run on Windows, copy this folder to a Windows machine and run the created $BAT_FILE from Command Prompt."
  fi

else
  echo "Invalid choice. Exiting." >&2
  exit 2
fi