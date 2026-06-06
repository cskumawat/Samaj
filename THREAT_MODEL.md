# Threat Model

## Scope

This threat model covers the Phase 0/1 Samaj application skeleton and the
Phase 2 foundation:

- Local settings
- Local audit logs
- Safety policy
- Anti-hallucination primitives
- PySide6 GUI shell
- SQLite database
- SQLAlchemy CRUD services
- Phase-wise external tool catalog intake

It does not cover future active testing modules, external tool execution, plugin execution, or AI providers because those are not implemented yet.

## Assets

- User settings
- Audit logs
- Authorization notes entered in future phases
- Evidence metadata in future phases
- Report content in future phases
- API keys in future phases

## Trust Boundaries

- GUI input to application logic
- Settings file on local disk
- Audit log file on local disk
- Future database boundary
- Project GUI to database boundary
- Catalog manifest to future tool registry boundary
- Future external command boundary
- Future AI provider boundary
- Future plugin boundary

## Current Foundation Threats

| Threat | Risk | Current Mitigation |
| --- | --- | --- |
| Safe Mode disabled by default | Unsafe actions could become normalized | Safe Mode defaults ON in settings |
| Anti-Hallucination disabled | Unsupported claims could be generated | Anti-Hallucination Mode is forced ON |
| Safety banner hidden | User loses visible safety context | GUI banner overrides hide and false visibility calls |
| Audit log missing | Local actions are not traceable | Audit logger creates JSONL records |
| Settings tampering | Unsafe settings could be loaded | Settings validation forces safety banner and anti-hallucination ON |
| Placeholder capability mistaken as working | User may rely on unbuilt modules | Later modules are clearly labeled planned |
| Tool catalog mistaken as support | User may think tools are bundled or runnable | Catalog entries are marked planned/not supported, not bundled, disabled by default |
| Database corruption | Project data could be lost | Phase 2 uses SQLite with tests; backup workflow is still planned |
| Unsafe tool category normalized | Offensive-capable tools may be treated as safe | Restricted categories are labeled and must remain disabled by default |

## Future Threats To Address

- External command injection
- Running tools against out-of-scope targets
- Missing rate limits
- Unsafe plugin permissions
- Secrets stored in plaintext
- AI-generated unsupported findings
- False positives marked confirmed
- Evidence tampering after report freeze
- Unauthorized screenshots or data collection
- Tool wrappers bypassing the safe command runner
- Catalog entries being promoted without safe profiles and tests

## Required Controls For Future Active Modules

Future modules must enforce:

1. Project selection.
2. Scope validation.
3. Authorized test type validation.
4. Rate limit validation.
5. Command preview.
6. User confirmation.
7. Audit logging.
8. Evidence capture with timestamps and source.
9. Conservative finding status.
10. Safe Mode behavior.
