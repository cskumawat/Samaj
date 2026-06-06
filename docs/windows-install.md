# Windows Install and Run

Samaj must always run inside the project-local `.venv`.

## Start

```bat
start.bat
```

`start.bat`:

- Creates `.venv` if missing.
- Activates `.venv`.
- Upgrades pip inside `.venv`.
- Installs or updates `requirements.txt`.
- Uses `.samaj` for project-local runtime files.
- Starts `python -m samaj`.
- Writes `.samaj\samaj.pid`.
- Writes logs under `.samaj\logs`.

For development dependencies:

```bat
start.bat --dev
```

## Stop

```bat
stop.bat
```

`stop.bat` reads `.samaj\samaj.pid` and stops only a matching `python -m samaj`
process whose executable is this project's `.venv\Scripts\python.exe`.

## Verification Commands

```bat
.\.venv\Scripts\python.exe -m samaj --doctor
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy samaj
```
