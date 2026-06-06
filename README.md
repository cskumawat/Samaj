# Samaj

Samaj is a safety-first Python GUI platform for lawful, authorized security
learning, defensive assessment planning, evidence management, and reporting
workflows.

Samaj is for lawful, educational, defensive, authorized bug bounty, internal
red-team, blue-team, research, and lab use only.

## Current Status

This repository currently implements Phase 0, Phase 1, and the Phase 2
foundation only:

- Phase 0: project planning, safety documentation, architecture skeleton,
  settings, audit logging, safety policy, and Anti-Hallucination primitives.
- Phase 1: PySide6 GUI shell with permanent safety banner, sidebar navigation,
  dashboard, settings page, logs page, and Windows launch/stop scripts.
- Phase 2 foundation: SQLite/SQLAlchemy persistence, CRUD services, basic
  Project Manager GUI, neutral Tool Catalog / Knowledge Registry intake,
  disclaimer acceptance, OS support mapping fields, static-only Safe Analysis
  Lab foundation, proxy database foundation, project-local runtime paths, and
  modern Samaj theme/logo foundation.

Catalog tools are not executable. External tool execution, active recon,
active scanning, plugin execution, AI provider calls, report export automation,
dynamic malware analysis, live proxy testing, and proxy-chain execution are not
implemented in this phase.

## Safety Rules

- Safe Mode is ON by default.
- Anti-Hallucination Mode is ON and forced by settings.
- The GUI safety banner is permanent:
  `SAFE MODE: ON | ANTI-HALLUCINATION: ON | SCOPE REQUIRED | AUTHORIZED USE ONLY`
- Findings must not be invented.
- Evidence, severity, and impact must not be guessed.
- Any future active test must require written scope, policy checks, command
  preview, user confirmation, rate limits, and audit logging.

Read [SECURITY_SCOPE.md](SECURITY_SCOPE.md) and
[ANTI_HALLUCINATION.md](ANTI_HALLUCINATION.md) before extending Samaj.

## Tool Catalog Disclaimer

Samaj includes a neutral Tool Catalog / Knowledge Registry intake for the
complete pasted tool inventory.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

A tool appearing in Samaj's catalog does not mean Samaj endorses it, supports
it, verifies it, recommends it, installs it, executes it, or grants permission
to use it.

The catalog is AI-suggested/publicly-known, not handmade, and not verified by
Samaj unless an entry explicitly says `Verified by developer: yes`. It may
contain dual-use, offensive-capable, lab-only, unknown, outdated, commercial,
unmaintained, unsafe, jurisdiction-restricted, or AI-suggested tools.

Explicit checkbox acceptance is required before catalog import or tool detail
viewing in the GUI or database service. See
[TOOL_CATALOG_DISCLAIMER.md](TOOL_CATALOG_DISCLAIMER.md).

## Catalog Fields

Every catalog entry is stored as knowledge-entry-only intake with these fields:

- Tool name
- Category
- Subcategory
- Description
- Catalog status: `knowledge-entry-only`
- Support status: `not implemented unless adapter exists`
- Safety note
- License note
- Official URL
- Install notes
- User notes
- AI-suggested: `yes` or `no`
- Verified by developer: `yes` or `no`
- OS support mapping for Windows, Kali Linux, Linux, and macOS
- Adapter availability
- Scope, Safe Mode, admin/root, network, and API-key notes

Unknown values remain explicitly marked as unknown or not verified. Samaj does
not fill missing facts by guessing.

## Safe Analysis Lab

Safe Analysis Lab does not execute malware on the host and must not be treated
as a complete malware sandbox until dynamic VM isolation is separately
implemented and tested.

The current lab foundation is static-only. It can copy a selected local file to
project-local quarantine, calculate hashes, identify simple file signatures,
extract printable strings, record static indicators, and create a Markdown
learning report. It does not run the sample and does not perform network
activity.

## Proxy Database

Proxy features must not be used for illegal activity, abuse, bypassing bans,
bypassing rate limits, unauthorized scraping, credential attacks, or hiding
unauthorized activity.

The current proxy foundation only parses, deduplicates, and stores proxy
inventory records in the local SQLite database. Live proxy testing and proxy
chain execution are not implemented.

## Installation

Python 3.11 or newer is required.

Samaj must always be created, installed, tested, and run inside the local
project virtual environment named `.venv`. Never install Samaj dependencies
globally and do not use `pip --user` for this project.

### Windows

Use the provided launcher:

```bat
start.bat
```

`start.bat` creates `.venv` if needed, activates it, upgrades pip inside
`.venv`, installs or updates `requirements.txt` inside `.venv`, starts the
Samaj GUI, and writes process metadata under `.samaj`.

For development dependencies:

```bat
start.bat --dev
```

To stop the running Samaj GUI process started from this project:

```bat
stop.bat
```

`stop.bat` reads `.samaj\samaj.pid` and only stops a matching
`python -m samaj` process whose executable is this project's
`.venv\Scripts\python.exe`.

### Linux and Kali Linux

Use the shell launcher:

```bash
./start.sh
```

For development dependencies:

```bash
./start.sh --dev
```

Stop a running Samaj process from the same project:

```bash
./stop.sh
```

The Linux scripts also use the project-local `.venv` and `.samaj` directories.

## Manual Development Commands

Manual setup is allowed only when it still uses `.venv`:

```bat
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

Run the doctor:

```bat
.\.venv\Scripts\python.exe -m samaj --doctor
```

Run tests and checks:

```bat
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy samaj
.\.venv\Scripts\python.exe -m compileall -q samaj tests
```

## Architecture

- `samaj/config`: defaults, settings, and safety policy.
- `samaj/core`: safety checks, Anti-Hallucination primitives, audit logging,
  OS detection, project-local paths, and future execution boundaries.
- `samaj/db`: SQLAlchemy database models, initialization, compatibility schema
  repair, and CRUD services.
- `samaj/gui`: PySide6 GUI shell, theme, logo assets, catalog gate, static lab
  page, proxy database page, and views.
- `samaj/lab`: static-only Safe Analysis Lab foundation.
- `samaj/proxy`: proxy parsing, policy, database import, and non-live chain
  preview foundation.
- `samaj/tools`: neutral Tool Catalog manifest, loader, OS support mapping, and
  knowledge-base helpers.
- `samaj/modules`: placeholders for later feature modules.
- `samaj/plugins`: future plugin system.
- `samaj/ai`: future AI provider wrappers and prompt guards.
- `tests`: unit, safety, Anti-Hallucination, GUI, and integration tests.

## Documentation

- [docs/tool-catalog.md](docs/tool-catalog.md)
- [docs/tool-disclaimer.md](docs/tool-disclaimer.md)
- [docs/os-support.md](docs/os-support.md)
- [docs/safe-analysis-lab.md](docs/safe-analysis-lab.md)
- [docs/proxy-module.md](docs/proxy-module.md)
- [docs/theme-and-branding.md](docs/theme-and-branding.md)
- [docs/windows-install.md](docs/windows-install.md)
- [docs/kali-install.md](docs/kali-install.md)

## Roadmap Boundary

See [ROADMAP.md](ROADMAP.md). Phase 3 is active scope enforcement and must not
be mixed into the current Phase 2 foundation work.

The requested tool list is tracked in
[docs/tool_catalog_roadmap.md](docs/tool_catalog_roadmap.md) and
`samaj/tools/catalog_manifest.json`. These entries are cataloged for future
phase planning only. Samaj does not claim they are installed, supported, tested,
bundled, safe, recommended, endorsed, licensed, or executable.

## Legal Disclaimer

Users are responsible for ensuring they have written authorization, defined
scope, legal approval, licensing rights, and permission before performing any
security testing. The maintainers do not authorize or encourage illegal
activity.
