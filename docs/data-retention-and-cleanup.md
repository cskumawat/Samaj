# Data Retention and Cleanup

Data retention policy is documented but not fully automated in this phase.

## Current Runtime Locations

- `.samaj/samaj.sqlite3`
- `.samaj/audit.jsonl`
- `.samaj/logs`
- `.samaj/lab/quarantine`
- `.samaj/lab/reports`
- `.samaj/kb`

## Current Boundary

Automated retention enforcement, secure deletion, report freeze cleanup, and
evidence lifecycle workflows are not implemented yet. Users remain responsible
for lawful storage, retention, cleanup, and disclosure obligations.
