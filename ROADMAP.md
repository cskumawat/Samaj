# Roadmap

## Phase 0: Planning and Safety Foundation

Status: implemented.

Delivered:

- README
- SECURITY_SCOPE.md
- ANTI_HALLUCINATION.md
- DEVELOPMENT.md
- ROADMAP.md
- THREAT_MODEL.md
- FREEZE_CHECKLIST.md
- Safety policy
- Settings model
- Audit logger
- Anti-Hallucination primitives
- Project skeleton

## Phase 1: Core App and GUI Shell

Status: implemented.

Delivered:

- PySide6 app entrypoint
- Main window
- Logo-aware sidebar navigation
- Dashboard view
- Settings view
- Logs view
- Permanent Safe Mode and Anti-Hallucination banner
- Placeholder screens for later phases
- Windows `start.bat` and `stop.bat`
- Tests for defaults, safety behavior, audit logs, and GUI shell behavior

## Phase 2: Database, Catalog, Lab, Proxy, and Theme Foundation

Status: foundation implemented.

Delivered:

- SQLite database
- SQLAlchemy ORM models
- Additive SQLite schema repair for current foundation columns
- Project CRUD
- Scope CRUD
- Asset CRUD
- Finding CRUD
- Evidence CRUD
- Audit CRUD
- Basic Project Manager GUI
- Complete neutral Tool Catalog / Knowledge Registry intake
- 45 catalog categories and 1,620 catalog entries
- Tool Catalog disclaimer gate and acceptance timestamp/version field
- Catalog OS support mapping fields
- Static-only Safe Analysis Lab foundation
- Proxy database foundation
- Modern Samaj theme and logo asset foundation
- Linux/Kali `start.sh` and `stop.sh` script foundation
- Tests for catalog, database, disclaimer, OS detection, static lab, proxy DB,
  theme assets, and GUI shell behavior

Still planned:

- Alembic revision files
- Full GUI CRUD for scope, assets, findings, evidence, and audit records
- Database backup workflow
- Data retention and cleanup automation

## Phase 3: Scope Enforcement

Status: planned, not implemented.

Planned:

- Project-backed scope checker
- Out-of-scope checker
- Action policy checker
- Rate limit manager
- GUI confirmation dialog

## Phase 4: Recon Foundation

Status: planned, not implemented.

Planned:

- Passive recon module
- DNS resolver
- HTTP probe
- Asset deduplication
- Source tracking
- Result parser

## Phase 5 And Later

Status: planned, not implemented.

Later phases include OSINT, HTTP security review, screenshots, manual testing
workbench, safe executable tool registry, reporting, AI integration, plugin
system, dynamic VM lab work, QA hardening, and public release work.

## Tool Catalog Roadmap

Status: catalog intake complete, implementations planned later.

The user-supplied broad tool list is stored in
`samaj/tools/catalog_manifest.json` and documented in
`docs/tool_catalog_roadmap.md`. The catalog currently contains 45 categories
and 1,620 tool entries.

All entries are neutral knowledge records. They are not installed, supported,
tested, bundled, safe, recommended, endorsed, licensed, executable, or permitted
by Samaj.
