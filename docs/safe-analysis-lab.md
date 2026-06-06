# Safe Analysis Lab

Safe Analysis Lab does not execute malware on the host and must not be treated
as a complete malware sandbox until dynamic VM isolation is separately
implemented and tested.

## Current Foundation

The current implementation is static-only:

- Copy selected local file to `.samaj/lab/quarantine`.
- Calculate MD5, SHA1, and SHA256.
- Detect simple file signatures.
- Extract printable strings.
- Record simple static indicators.
- Generate a Markdown report under `.samaj/lab/reports`.
- Generate a Mermaid learning diagram.

## Explicit Non-Goals

- No sample execution.
- No dynamic detonation.
- No network access.
- No host behavior tracing.
- No VM orchestration.
- No claim of complete malware sandboxing.

## User Responsibility

Users are responsible for lawful authorization, safe handling, storage,
licensing, and consequences. Static analysis can miss important behavior and
must be manually reviewed.
