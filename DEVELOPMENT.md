# Development Guide

## Phase Boundary

This repository currently contains Phase 0, Phase 1, and the Phase 2
foundation.

Phase 0 covers:

- Planning documentation
- Safety scope
- Anti-Hallucination rules
- Threat model
- Project skeleton
- Settings
- Safety policy
- Audit logging

Phase 1 covers:

- PySide6 application shell
- Main window
- Sidebar navigation
- Dashboard
- Settings page
- Logs page
- Permanent safety and Anti-Hallucination banner
- Windows start/stop scripts

Phase 2 foundation covers:

- SQLite database initialization
- SQLAlchemy models
- CRUD services for projects, scope, assets, findings, evidence, and audit records
- Basic Project Manager GUI
- Neutral Tool Catalog / Knowledge Registry intake
- Tool Catalog disclaimer acceptance
- OS support mapping fields
- Static-only Safe Analysis Lab foundation
- Proxy database foundation
- Modern Samaj theme and logo foundation
- Linux/Kali start/stop script foundation

Do not implement Phase 3 or later work in this phase. Active scope
enforcement, recon, OSINT, external commands, executable tool adapters, live
proxy testing, proxy-chain execution, dynamic malware analysis, plugins, AI
providers, and reporting automation remain planned.

## Setup

All installation, testing, and execution must use the project virtual
environment named `.venv`. Do not install dependencies globally and do not use
`pip --user` for project dependencies.

Windows launcher:

```bat
start.bat
```

`start.bat` creates and activates `.venv`, installs or updates requirements
inside `.venv`, starts the GUI, and records the process ID under `.samaj`.

Install development dependencies before launching:

```bat
start.bat --dev
```

Linux/Kali launcher:

```bash
./start.sh
```

Manual setup, if needed:

```bat
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
```

## Run

```bat
start.bat
```

Stop the GUI process started from this project:

```bat
stop.bat
```

## Test

```bat
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m mypy samaj
.\.venv\Scripts\python.exe -m compileall -q samaj tests
.\.venv\Scripts\python.exe -m samaj --doctor
```

## Architecture

Samaj uses a layered structure:

- `samaj/config`: configuration defaults, settings persistence, and safety policy constants.
- `samaj/core`: safety decisions, Anti-Hallucination validation, OS detection, audit logging, and future execution boundaries.
- `samaj/db`: SQLAlchemy models, database initialization, compatibility repair, and CRUD services.
- `samaj/gui`: PySide6 shell, views, theme, logo assets, and non-executing foundation pages.
- `samaj/lab`: static-only Safe Analysis Lab foundation.
- `samaj/proxy`: proxy parsing, policy, database storage, and non-live preview helpers.
- `samaj/tools`: Tool Catalog manifest, loader, disclaimer, OS support mapping, and knowledge-base helpers.
- `samaj/modules`: placeholders for later feature modules.
- `samaj/plugins`: placeholders for Phase 12 plugin work.
- `samaj/ai`: placeholders for Phase 11 AI provider work.

## Safety Requirements For New Work

Every active feature must answer these questions before implementation:

1. What asset or target can this touch?
2. How is scope verified?
3. How is authorization recorded?
4. How is rate limiting enforced?
5. What evidence is collected?
6. How is the action audited?
7. How does Safe Mode affect the feature?
8. How does Anti-Hallucination Mode prevent unsupported claims?

If the answer is missing, the feature is not ready to implement.

## Anti-Hallucination Requirements For New Work

Every AI-generated or assisted statement must be tagged as one of:

- Observed fact
- Inference
- Hypothesis
- Recommendation
- Needs manual verification

Findings cannot be confirmed without evidence. Severity cannot be assigned
without reasoning. Unknowns must be labeled as unknowns.

Catalog metadata must not be guessed. Unknown support, OS compatibility,
license, safety, and install status must remain unknown until verified.

## Tool Catalog Intake

The requested phase-wise tool catalog is stored in
`samaj/tools/catalog_manifest.json` and documented in
[docs/tool_catalog_roadmap.md](docs/tool_catalog_roadmap.md). Do not treat
catalog entries as implemented support.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

## Freeze Rule

Only ask for a phase freeze after:

- Tests were run.
- Tests were run from `.venv`.
- `start.bat` was verified.
- `stop.bat` was verified.
- Failures are fixed or documented.
- Manual launch status is recorded.
- Known limitations are listed.
- The freeze checklist is updated.
