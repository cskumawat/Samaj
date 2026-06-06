# SECURITY SCOPE

Samaj is for lawful, educational, defensive, authorized bug bounty, internal
red-team, blue-team, research, and lab use only.

Samaj must not be used for:

- Unauthorized access
- Credential theft
- Phishing
- Malware deployment
- Botnets
- Persistence on systems without authorization
- Privilege escalation on systems without permission
- Exploiting third-party systems outside written scope
- DDoS
- Data theft
- Bypassing authentication
- Stealing secrets
- Exfiltration
- Attacking public systems without written authorization

Every project must define:

- Program name
- Scope
- Out-of-scope assets
- Authorized test types
- Rate limits
- Legal notes
- Contact details
- Evidence policy
- Data retention policy

Safe Mode must be enabled by default.

## Required Preflight Questions

Before running any future active test, Samaj must ask:

1. Is this target authorized?
2. Is this target inside scope?
3. Is this test allowed by program policy?
4. Is rate limiting configured?
5. Should this action be logged?
6. Should screenshots/evidence be captured?
7. Is Safe Mode enabled?

Default answers must be conservative. If any answer is missing or unsafe, the
action must be blocked.

## Current Enforcement Status

Implemented:

- Safe Mode defaults ON in settings.
- Anti-Hallucination Mode is forced ON in settings.
- GUI safety banner is permanent.
- Safety policy data exists in code.
- Safety evaluator blocks actions when required safety conditions are missing.
- Audit logger creates append-only JSONL records for local application events.
- Tool Catalog import and detail viewing require explicit disclaimer acceptance.
- Tool Catalog entries are neutral knowledge records only.
- Safe Analysis Lab is static-only and does not execute samples.
- Proxy database stores inventory records only; live testing is not implemented.

Not implemented yet:

- Active testing modules.
- External command execution.
- Runtime confirmation dialogs for active tests.
- Full GUI CRUD for every database-backed record.
- Rate-limit enforcement for active modules.
- Dynamic malware sandboxing.
- Live proxy testing.
- Proxy-chain execution.

Any future active testing feature must integrate with the safety policy before
it can run.

## Tool Catalog / Knowledge Registry Scope

Samaj may store a neutral Tool Catalog / Knowledge Registry intake for tool
names provided by a user or publicly-known/AI-suggested sources.

Tool Catalog entry does not mean tool support, endorsement, verification,
safety, installation, execution, recommendation, operational support, or
permission to use.

A tool appearing in Samaj's catalog does not mean Samaj endorses it, supports
it, verifies it, recommends it, installs it, executes it, or grants permission
to use it.

The catalog may contain dual-use, offensive-capable, lab-only, unknown,
outdated, commercial, unmaintained, unsafe, jurisdiction-restricted, or
AI-suggested tools. Samaj does not endorse illegal use. The user alone is
responsible for authorization, legality, licensing, installation,
configuration, safe operation, scope compliance, rate limits, local policy
compliance, third-party terms, and consequences.

Catalog entry creation must not be blocked only because a tool is
offensive-capable, lab-only, unknown, or AI-suggested. Instead, Samaj must
require explicit Tool Catalog disclaimer acceptance before catalog import, tool
detail viewing, or catalog use.

The Phase 2 catalog foundation must not execute tools.

## Safe Analysis Lab Scope

Safe Analysis Lab does not execute malware on the host and must not be treated
as a complete malware sandbox until dynamic VM isolation is separately
implemented and tested.

The current lab foundation is static-only. It may quarantine a copy, hash it,
extract strings, record static indicators, and write a learning report. It must
not execute samples or perform network activity.

## Proxy Scope

Proxy features must not be used for illegal activity, abuse, bypassing bans,
bypassing rate limits, unauthorized scraping, credential attacks, or hiding
unauthorized activity.

The current proxy foundation stores local inventory records only. Live proxy
testing and chain execution are not implemented.
