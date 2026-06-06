from __future__ import annotations

from samaj.core.audit import AuditLogger


def test_audit_logger_creates_jsonl_events_and_redacts_secrets(tmp_path):
    logger = AuditLogger(tmp_path / "audit.jsonl")

    event = logger.log(
        event_type="test_event",
        message="Audit test.",
        metadata={"api_key": "secret-value", "safe": "value"},
    )
    events = logger.read_events()

    assert event.event_type == "test_event"
    assert len(events) == 1
    assert events[0].metadata["api_key"] == "[REDACTED]"
    assert events[0].metadata["safe"] == "value"

