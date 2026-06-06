"""Safety policy evaluation primitives."""

from __future__ import annotations

from dataclasses import dataclass, field

from samaj.config.safety_policy import (
    BLOCKED_ACTION_KEYWORDS,
    DEFAULT_PREFLIGHT_QUESTIONS,
    ActionPolicy,
    RiskLevel,
    get_action_policy,
)


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    reasons: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()
    risk_level: RiskLevel = RiskLevel.HIGH


@dataclass(frozen=True)
class PreflightAnswers:
    target_authorized: bool = False
    target_in_scope: bool = False
    test_allowed: bool = False
    rate_limit_configured: bool = False
    action_logged: bool = True
    evidence_capture: bool = True
    safe_mode_enabled: bool = True

    def as_dict(self) -> dict[str, bool]:
        return {
            "target_authorized": self.target_authorized,
            "target_in_scope": self.target_in_scope,
            "test_allowed": self.test_allowed,
            "rate_limit_configured": self.rate_limit_configured,
            "action_logged": self.action_logged,
            "evidence_capture": self.evidence_capture,
            "safe_mode_enabled": self.safe_mode_enabled,
        }


@dataclass
class SafetyPolicy:
    """Conservative safety evaluator for future active modules."""

    default_block_reason: str = "Action blocked by conservative foundation safety policy."
    preflight_question_keys: tuple[str, ...] = field(
        default_factory=lambda: tuple(question.key for question in DEFAULT_PREFLIGHT_QUESTIONS)
    )

    def evaluate_action(
        self,
        action: str,
        answers: PreflightAnswers | None = None,
        policy: ActionPolicy | None = None,
        target: str | None = None,
    ) -> SafetyDecision:
        answers = answers or PreflightAnswers()
        policy = policy or get_action_policy(action)
        reasons: list[str] = []
        warnings: list[str] = []

        unsafe_keyword = next(
            (keyword for keyword in BLOCKED_ACTION_KEYWORDS if keyword in action.lower()),
            None,
        )
        if unsafe_keyword:
            reasons.append(f"Action contains blocked unsafe keyword: {unsafe_keyword}.")

        if not policy.implemented:
            reasons.append(
                f"Action '{action}' is planned but not implemented in the current foundation."
            )

        if policy.requires_scope and not target:
            reasons.append("Target is required for scoped actions.")

        answer_map = answers.as_dict()
        for question in DEFAULT_PREFLIGHT_QUESTIONS:
            if question.required_answer and not answer_map[question.key]:
                reasons.append(f"Preflight failed: {question.question}")

        if not answers.safe_mode_enabled:
            warnings.append(
                "Safe Mode is disabled. Future active actions must show a strong warning."
            )

        return SafetyDecision(
            allowed=not reasons,
            reasons=tuple(reasons),
            warnings=tuple(warnings),
            risk_level=policy.risk_level,
        )


def required_preflight_questions() -> tuple[str, ...]:
    return tuple(question.question for question in DEFAULT_PREFLIGHT_QUESTIONS)


def is_safe_mode_policy_passed(answers: PreflightAnswers) -> bool:
    return answers.safe_mode_enabled and SafetyPolicy().evaluate_action(
        action="active_test",
        answers=answers,
        target="placeholder",
    ).allowed
