# Contributing

Samaj accepts contributions that improve lawful, authorized, defensive security workflows.

## Contribution Rules

- Do not add offensive automation that bypasses scope checks.
- Do not add destructive payloads.
- Do not add credential theft, phishing, malware, persistence, evasion, or exfiltration features.
- Do not hardcode secrets.
- Do not claim a finding is confirmed without evidence.
- Do not mark severity without reasoning.
- Do not hide Safe Mode or Anti-Hallucination Mode.

## Development Flow

1. Define the requirement.
2. Define safety impact.
3. Add or update tests.
4. Implement the smallest scoped change.
5. Update documentation.
6. Run tests and linting.
7. Record limitations.

## Tests

```bash
pytest
ruff check .
mypy samaj
```

If a dependency is unavailable, document the skipped verification honestly.

