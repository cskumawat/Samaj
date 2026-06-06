# Linux and Kali Linux Install and Run

Samaj must always run inside the project-local `.venv`.

## Start

```bash
./start.sh
```

`start.sh`:

- Creates `.venv` if missing.
- Activates `.venv`.
- Upgrades pip inside `.venv`.
- Installs or updates `requirements.txt`.
- Uses `.samaj` for project-local runtime files.
- Starts `python -m samaj`.
- Writes `.samaj/samaj.pid`.
- Writes logs under `.samaj/logs`.

For development dependencies:

```bash
./start.sh --dev
```

## Stop

```bash
./stop.sh
```

`stop.sh` reads `.samaj/samaj.pid` and stops a matching process started from the
project-local `.venv`.

## Scope

Kali Linux support in this phase means startup and metadata foundations only.
Catalog tools are not installed, executed, supported, tested, or recommended.
