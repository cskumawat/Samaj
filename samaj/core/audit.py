"""Append-only JSONL audit logging for local Samaj events."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

SECRET_KEY_RE = re.compile(r"(api[_-]?key|token|password|secret|credential)", re.IGNORECASE)


@dataclass(frozen=True)
class AuditEvent:
    event_type: str
    message: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    metadata: dict[str, Any] = field(default_factory=dict)


def redact_secrets(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: dict[str, Any] = {}
        for key, item in value.items():
            redacted[key] = "[REDACTED]" if SECRET_KEY_RE.search(str(key)) else redact_secrets(item)
        return redacted
    if isinstance(value, list):
        return [redact_secrets(item) for item in value]
    return value


class AuditLogger:
    """Small JSONL audit logger.

    This local file logger is intentionally available from the start. Database
    audit records are stored separately by the repository service.
    """

    def __init__(self, log_path: Path) -> None:
        self.log_path = Path(log_path).expanduser()
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(
        self,
        event_type: str,
        message: str,
        metadata: dict[str, Any] | None = None,
    ) -> AuditEvent:
        event = AuditEvent(
            event_type=event_type,
            message=message,
            metadata=redact_secrets(metadata or {}),
        )
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), sort_keys=True))
            handle.write("\n")
        return event

    def read_events(self, limit: int | None = None) -> list[AuditEvent]:
        if not self.log_path.exists():
            return []

        rows = self.log_path.read_text(encoding="utf-8").splitlines()
        if limit is not None:
            rows = rows[-limit:]

        events: list[AuditEvent] = []
        for row in rows:
            if not row.strip():
                continue
            data = json.loads(row)
            events.append(
                AuditEvent(
                    event_type=data["event_type"],
                    message=data["message"],
                    event_id=data["event_id"],
                    timestamp=data["timestamp"],
                    metadata=data.get("metadata", {}),
                )
            )
        return events
