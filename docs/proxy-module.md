# Proxy Database Foundation

Proxy features must not be used for illegal activity, abuse, bypassing bans,
bypassing rate limits, unauthorized scraping, credential attacks, or hiding
unauthorized activity.

## Current Foundation

The current proxy module can:

- Parse pasted `host:port` and `type://host:port` entries.
- Deduplicate records by host, port, and type.
- Store records in the local SQLite database.
- Track source, country, ASN, status, latency fields, success rate fields,
  notes, and legal status notes.
- Preview proxy-chain configuration as metadata only.

## Not Implemented

- Live proxy testing.
- Proxy chain execution.
- Automatic scraping of proxy lists.
- Abuse prevention bypasses.
- Credential attacks.
- Any behavior intended to hide unauthorized activity.

## Database Table

Proxy records are stored in `proxy_records`. The presence of a proxy record is
inventory only and does not mean it is legal, safe, reliable, tested, or
approved for use.
