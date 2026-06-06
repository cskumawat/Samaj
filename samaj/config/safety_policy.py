"""Static safety policy data for Samaj foundation phases."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class RiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class SafetyQuestion:
    key: str
    question: str
    required_answer: bool = True


@dataclass(frozen=True)
class ActionPolicy:
    action: str
    risk_level: RiskLevel
    requires_scope: bool = True
    requires_confirmation: bool = True
    requires_rate_limit: bool = True
    requires_audit_log: bool = True
    safe_mode_compatible: bool = True
    implemented: bool = False


DEFAULT_PREFLIGHT_QUESTIONS: tuple[SafetyQuestion, ...] = (
    SafetyQuestion("target_authorized", "Is this target authorized?"),
    SafetyQuestion("target_in_scope", "Is this target inside scope?"),
    SafetyQuestion("test_allowed", "Is this test allowed by program policy?"),
    SafetyQuestion("rate_limit_configured", "Is rate limiting configured?"),
    SafetyQuestion("action_logged", "Should this action be logged?"),
    SafetyQuestion("evidence_capture", "Should screenshots/evidence be captured?"),
    SafetyQuestion("safe_mode_enabled", "Is Safe Mode enabled?"),
)

DEFAULT_ACTION_POLICIES: dict[str, ActionPolicy] = {
    "passive_review": ActionPolicy(
        action="passive_review",
        risk_level=RiskLevel.LOW,
        requires_rate_limit=False,
        implemented=False,
    ),
    "active_test": ActionPolicy(
        action="active_test",
        risk_level=RiskLevel.HIGH,
        implemented=False,
    ),
    "external_command": ActionPolicy(
        action="external_command",
        risk_level=RiskLevel.HIGH,
        implemented=False,
    ),
}

BLOCKED_ACTION_KEYWORDS = (
    "credential theft",
    "phishing",
    "malware",
    "botnet",
    "persistence",
    "ddos",
    "exfiltration",
    "steal",
    "bypass authentication",
)


def get_action_policy(action: str) -> ActionPolicy:
    return DEFAULT_ACTION_POLICIES.get(
        action,
        ActionPolicy(action=action, risk_level=RiskLevel.HIGH, implemented=False),
    )
