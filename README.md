# Samaj

Samaj is an open-source Python GUI platform for authorized bug bounty, defensive red-team, recon, evidence management, and security reporting.

Samaj is built with safety-first design:
- Scope enforcement
- Safe Mode ON by default
- Anti-Hallucination Mode ON by default
- Audit logging
- Evidence-based findings
- No fake results
- No unauthorized testing

## Current Status

This repository currently implements Phase 0, Phase 1, and the Phase 2 database foundation:

- Phase 0: planning, safety documentation, architecture skeleton, settings, audit logging, safety policy, and anti-hallucination primitives.
- Phase 1: PySide6 GUI shell with a permanent safety banner, sidebar navigation, dashboard, settings page, and logs page.
- Phase 2: SQLite/SQLAlchemy persistence, CRUD services for projects, scope items, assets, findings, evidence, audit records, and a basic Project Manager GUI.

The following are planned but not implemented yet: database migrations with Alembic revision files, full GUI CRUD for every entity, recon modules, OSINT modules, external tool execution, plugin execution, AI provider calls, report export, and release freeze automation.

## Safety Scope

Samaj is only for lawful, authorized, defensive cybersecurity work. It must not be used for unauthorized access, credential theft, phishing, malware, botnets, persistence, DDoS, data theft, authentication bypass, or testing assets without written permission.

Every active test must require scope confirmation, a policy check, rate limiting, command preview, user confirmation, and audit logging before execution. Those execution paths are not implemented in Phase 1.

Read [SECURITY_SCOPE.md](SECURITY_SCOPE.md) before using or extending this project.

## Anti-Hallucination Mode

Anti-Hallucination Mode is always ON. Samaj must not invent results, evidence, severity, or impact. AI-assisted output must distinguish observed facts, inferences, hypotheses, recommendations, and items needing manual verification.

Read [ANTI_HALLUCINATION.md](ANTI_HALLUCINATION.md) for the rules enforced by the Phase 0 primitives in `samaj/core/anti_hallucination.py`.

## Who Samaj Is For

- Authorized bug bounty researchers
- Internal security teams
- Defensive red-team operators
- Blue-team validation teams
- Security students working in legal labs
- Consultants performing scoped assessments
- Organizations tracking security posture

## Installation

Python 3.11 or newer is required.

Samaj must always be created, installed, tested, and run inside the local project
virtual environment named `.venv`. Do not install Samaj dependencies globally and
do not use `pip --user` for project dependencies.

On Windows, use the provided launcher:

```bat
start.bat
```

`start.bat` creates `.venv` if needed, activates it, upgrades pip inside `.venv`,
installs or updates `requirements.txt` inside `.venv`, starts the Samaj GUI, and
writes process metadata under `.samaj`.

For development dependencies before launching the GUI:

```bat
start.bat --dev
```

To stop the running Samaj GUI process started from this project:

```bat
stop.bat
```

`stop.bat` reads `.samaj\samaj.pid` and only stops a matching `python -m samaj`
process whose executable is this project’s `.venv\Scripts\python.exe`.

Manual setup is allowed only when it still uses `.venv`:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

## Quick Start

Launch the GUI:

```bat
start.bat
```

Run the command-line doctor:

```bash
.\.venv\Scripts\python.exe -m samaj --doctor
```

Run tests:

```bash
.\.venv\Scripts\python.exe -m pytest
```

Run lint and type checks:

```bash
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy samaj
```

## Features Implemented In Phase 0/1

- Repository skeleton for future modules
- Safety scope documentation
- Anti-hallucination documentation and validation primitives
- Threat model
- Development guide and roadmap
- Pydantic settings model
- JSON settings persistence
- Safe Mode default ON
- Anti-Hallucination Mode forced ON
- Audit log creation
- PySide6 main window shell
- Permanent GUI banner: `SAFE MODE: ON | AUTHORIZED TESTING ONLY | ANTI-HALLUCINATION: ON`
- Sidebar navigation
- Dashboard, Settings, and Logs views
- Project Manager GUI with create, edit, list, and archive
- SQLite database initialization
- SQLAlchemy models for projects, scope, assets, findings, evidence, and audit records
- CRUD service helpers for Phase 2 entities
- Phase-wise external tool catalog intake with 1,100 requested entries, all marked planned/not supported yet
- Placeholder views for later modules, clearly marked as not implemented

## Tool Catalog / Knowledge Registry Disclaimer

Samaj includes a neutral Tool Catalog / Knowledge Registry intake for the complete
pasted tool inventory. This is not a support matrix.

Tool Catalog entry ≠ tool support, tool endorsement, tool safety, recommendation,
operational support, permission to use, installation, testing, licensing
approval, or Samaj-built functionality.

The catalog is AI-suggested/publicly-known, not handmade, and not verified by
Samaj. It may contain dual-use, offensive-capable, lab-only, unknown, outdated,
commercial, unmaintained, unsafe, or jurisdiction-restricted tools.

The catalog is provided only for educational, research, defensive, authorized bug
bounty, internal red-team, blue-team, and lab purposes. Samaj does not endorse
illegal use. The user alone is responsible for authorization, legality,
licensing, installation, configuration, safe operation, scope compliance, rate
limits, local policy compliance, third-party terms, and consequences.

Explicit checkbox acceptance of [TOOL_CATALOG_DISCLAIMER.md](TOOL_CATALOG_DISCLAIMER.md)
is required before catalog import, tool detail viewing, or catalog use in the GUI
or database service.

## Architecture

Samaj is organized into clear layers:

- `samaj/config`: defaults, settings, and safety policy.
- `samaj/core`: safety checks, anti-hallucination primitives, audit logging, and future command execution boundaries.
- `samaj/gui`: PySide6 GUI shell and views.
- `samaj/db`: Phase 2 SQLAlchemy database models, initialization, and CRUD services.
- `samaj/tools/catalog_manifest.json`: phase-wise tool catalog intake, not a support matrix.
- `samaj/modules`: future feature modules.
- `samaj/tools`: future safe tool registry.
- `samaj/plugins`: future plugin system.
- `samaj/ai`: future AI provider wrappers and prompt guards.
- `tests`: unit, safety, anti-hallucination, and GUI tests.

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for setup, architecture, testing, and phase rules.

Core development rules:

1. Do not implement active testing without scope enforcement.
2. Do not run external commands outside the safe command runner.
3. Do not create findings without evidence.
4. Do not mark severity without reasoning.
5. Do not claim planned modules are implemented.
6. Keep Safe Mode and Anti-Hallucination Mode visible in the GUI.
7. Use only the project `.venv` for install, test, and run commands.
8. Verify `start.bat` and `stop.bat` before freezing any phase.

## Roadmap

See [ROADMAP.md](ROADMAP.md). Phase 3 is active scope enforcement and must not be mixed into Phase 2 database foundation work.

The requested large tool list is tracked in [docs/tool_catalog_roadmap.md](docs/tool_catalog_roadmap.md) and `samaj/tools/catalog_manifest.json`. These entries are cataloged for future phase planning only. Samaj does not claim they are installed, supported, tested, bundled, safe, recommended, endorsed, licensed, or executable.

## Screenshots

Screenshots are not included yet. This is not verified yet on every desktop platform.

## Legal Disclaimer

Samaj is provided for lawful, authorized, defensive security work only. Users are responsible for ensuring they have written authorization, defined scope, legal approval, and permission before performing any security testing. The maintainers do not authorize or encourage illegal activity.
