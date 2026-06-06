# Freeze Checklist

## Phase 0 Freeze Checklist

- [x] README present
- [x] SECURITY_SCOPE.md present
- [x] ANTI_HALLUCINATION.md present
- [x] DEVELOPMENT.md present
- [x] ROADMAP.md present
- [x] Threat model present
- [x] Project skeleton present
- [x] Settings load with Safe Mode ON
- [x] Anti-Hallucination Mode defaults ON and is forced ON
- [x] Safety policy loads
- [x] Audit logger creates records
- [x] `start.bat` present
- [x] `stop.bat` present
- [x] `.venv` created in the project root
- [x] Runtime dependencies installed inside `.venv`
- [x] Tests passed from `.venv` in the target environment
- [x] `start.bat` verified in the target environment
- [x] `stop.bat` verified in the target environment
- [ ] Manual review complete

## Phase 1 Freeze Checklist

- [x] PySide6 GUI entrypoint present
- [x] Main window present
- [x] Sidebar navigation present
- [x] Dashboard present
- [x] Settings page present
- [x] Logs page present
- [x] Safe Mode banner present
- [x] Anti-Hallucination banner present
- [x] Banner cannot be hidden through normal widget calls
- [x] Placeholder views are labeled as not implemented
- [x] Windows `start.bat` launches through `.venv`
- [x] Windows `stop.bat` stops only this project app process
- [x] `start.bat` verified in the target environment
- [x] `stop.bat` verified in the target environment
- [x] GUI launched in the target environment
- [x] Tests passed from `.venv` in the target environment
- [ ] Basic UX manual review complete

Do not freeze Phase 1 until test and manual launch status are verified.
Do not freeze any phase if dependencies were installed or tests were run outside `.venv`.

## Phase 2 Freeze Checklist

- [x] SQLite database initializes
- [x] SQLAlchemy models present
- [x] Project CRUD service present
- [x] Scope CRUD service present
- [x] Asset CRUD service present
- [x] Finding CRUD service present
- [x] Evidence CRUD service present
- [x] Audit CRUD service present
- [x] Basic Project Manager GUI present
- [x] Tool catalog intake stored phase-wise
- [x] Tool catalog entries marked knowledge-entry-only
- [x] Tool catalog support status defaults to `not implemented unless adapter exists`
- [x] Tool catalog entries stored as neutral knowledge registry intake
- [x] Tool catalog disclaimer document present
- [x] Tool catalog disclaimer added to README.md
- [x] Tool catalog disclaimer added to SECURITY_SCOPE.md
- [x] Complete pasted tool names preserved in the catalog manifest
- [x] Tool catalog DB field `user_accepted_tool_disclaimer_at` present
- [x] Tool catalog DB field `user_accepted_tool_disclaimer_version` present
- [x] GUI requires explicit checkbox acceptance before catalog import/detail viewing
- [x] Offensive-capable/lab-only/unknown/AI-suggested entries are not blocked at catalog-entry creation solely for that reason
- [x] OS support mapping fields present
- [x] Safe Analysis Lab static-only foundation present
- [x] Safe Analysis Lab disclaimer documented
- [x] Proxy database foundation present
- [x] Proxy safety disclaimer documented
- [x] Modern Samaj theme/logo foundation present
- [x] Tests passed from `.venv` in the target environment after latest Phase 2 foundation changes
- [x] `start.bat` verified after latest Phase 2 foundation changes
- [x] `stop.bat` verified after latest Phase 2 foundation changes
- [ ] Basic UX manual review complete
- [ ] Phase 2 freeze approved
