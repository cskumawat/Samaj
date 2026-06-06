# Tool Catalog Disclaimer Workflow

Samaj requires explicit user acceptance before catalog import or tool detail
viewing.

The required disclaimer is stored in:

- `TOOL_CATALOG_DISCLAIMER.md`
- `samaj/tools/disclaimer.py`
- GUI first-run Tool Catalog disclaimer dialog
- Tool Catalog view acceptance panel

## Required Text

Samaj is for lawful, educational, defensive, authorized bug bounty, internal
red-team, blue-team, research, and lab use only.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

A tool appearing in Samaj's catalog does not mean Samaj endorses it, supports
it, verifies it, recommends it, installs it, executes it, or grants permission
to use it.

Proxy features must not be used for illegal activity, abuse, bypassing bans,
bypassing rate limits, unauthorized scraping, credential attacks, or hiding
unauthorized activity.

Safe Analysis Lab does not execute malware on the host and must not be treated
as a complete malware sandbox until dynamic VM isolation is separately
implemented and tested.

## Database Fields

- `user_accepted_tool_disclaimer_at`
- `user_accepted_tool_disclaimer_version`
- `actor`
- `acceptance_text`

## Enforcement

The repository service raises `ToolCatalogDisclaimerRequiredError` when catalog
import, listing, or detail viewing is attempted before acceptance.
