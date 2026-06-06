# Tool Catalog / Knowledge Registry

The Samaj Tool Catalog / Knowledge Registry is a neutral knowledge intake list.
It stores the complete pasted inventory as catalog records so future phases can
plan adapter work without claiming current support.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

A tool appearing in Samaj's catalog does not mean Samaj endorses it, supports
it, verifies it, recommends it, installs it, executes it, or grants permission
to use it.

## Current Manifest

- File: `samaj/tools/catalog_manifest.json`
- Count: 1,620 entries
- Categories: 45
- Status: knowledge-entry-only
- Support status: not implemented unless adapter exists

## Entry Fields

Each entry may contain:

- Tool name
- Category
- Subcategory
- Description
- Catalog status
- Support status
- Safety note
- License note
- Official URL
- Install notes
- User notes
- AI-suggested
- Verified by developer
- Source note
- Install status
- Documentation URL
- Disclaimer status
- OS support fields for Windows, Kali Linux, Linux, and macOS
- Install method fields for Windows, Kali Linux, and Linux
- Adapter availability
- Safe Mode and scope requirements
- Admin/root, network, and API-key requirements
- Usage notes
- Legal notes

Unknown fields are intentionally recorded as unknown or not verified. Samaj must
not guess missing facts.

## Import Gate

Catalog import and detail viewing require explicit checkbox acceptance of the
Tool Catalog disclaimer. The database stores
`user_accepted_tool_disclaimer_at` and
`user_accepted_tool_disclaimer_version` in
`tool_catalog_disclaimer_acceptance`.

## Execution Boundary

This phase does not make catalog tools executable. Future adapter work must be
implemented phase-wise and must pass Safe Mode, Anti-Hallucination Mode, scope
enforcement, command preview, explicit confirmation, rate limiting, audit
logging, and evidence controls.
