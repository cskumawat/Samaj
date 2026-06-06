"""Tool Catalog disclaimer text."""

TOOL_CATALOG_DISCLAIMER_TEXT = """
The Samaj Tool Catalog / Knowledge Registry is a neutral knowledge intake list.

Samaj is for lawful, educational, defensive, authorized bug bounty, internal
red-team, blue-team, research, and lab use only.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

A tool appearing in Samaj's catalog does not mean Samaj endorses it, supports
it, verifies it, recommends it, installs it, executes it, or grants permission
to use it.

The catalog is AI-suggested/publicly-known, not handmade, and not verified by
Samaj unless an entry explicitly says "Verified by developer: yes". It may
contain dual-use, offensive-capable, lab-only, unknown, outdated, commercial,
unmaintained, unsafe, jurisdiction-restricted, or AI-suggested tools.

The catalog is provided only for educational, research, defensive, authorized
bug bounty, internal red-team, blue-team, and lab purposes. Samaj does not
endorse illegal use. The user alone is responsible for authorization, legality,
licensing, installation, configuration, safe operation, scope compliance, rate
limits, local policy compliance, third-party terms, and consequences.

Presence in the catalog does not grant permission to run a tool against any
system. Written authorization and scope are still required.

Proxy features must not be used for illegal activity, abuse, bypassing bans,
bypassing rate limits, unauthorized scraping, credential attacks, or hiding
unauthorized activity.

Safe Analysis Lab does not execute malware on the host and must not be treated
as a complete malware sandbox until dynamic VM isolation is separately
implemented and tested.

This phase does not make catalog tools executable. Future execution support, if
implemented, must still pass Safe Mode, Anti-Hallucination Mode, scope
enforcement, command preview, explicit confirmation, rate limiting, audit
logging, and evidence controls.
""".strip()

TOOL_CATALOG_ACCEPTANCE_LABEL = (
    "I understand and accept that Tool Catalog entries are neutral knowledge "
    "intake only, not support, endorsement, verification, safety, installation, "
    "execution, recommendation, permission, or Samaj-built functionality."
)
