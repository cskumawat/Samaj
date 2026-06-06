# Installation

## Requirements

- Python 3.11 or newer
- A desktop environment capable of running PySide6

## Required Virtual Environment

Samaj must always use the local project virtual environment named `.venv`.
Do not install dependencies globally and do not use `pip --user` for project
dependencies.

## Windows

Start Samaj:

```bat
start.bat
```

Install development dependencies and start Samaj:

```bat
start.bat --dev
```

Stop the project-local Samaj process:

```bat
stop.bat
```

`start.bat` creates and activates `.venv`, installs or updates requirements
inside `.venv`, uses `.samaj` for runtime files, and launches `python -m samaj`.
`stop.bat` stops only a matching process from this project's `.venv`.

## Linux and Kali Linux

Start Samaj:

```bash
./start.sh
```

Install development dependencies and start Samaj:

```bash
./start.sh --dev
```

Stop Samaj:

```bash
./stop.sh
```

These scripts also use `.venv` and `.samaj` under the project directory.

## Manual Setup

Manual setup is allowed only when it still uses `.venv`:

```bat
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Verify

```bat
.\.venv\Scripts\python.exe -m samaj --doctor
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy samaj
```
