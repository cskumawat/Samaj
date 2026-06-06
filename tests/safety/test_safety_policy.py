from __future__ import annotations

from samaj.config.safety_policy import ActionPolicy, RiskLevel
from samaj.core.safety import PreflightAnswers, SafetyPolicy, required_preflight_questions


def test_required_preflight_questions_are_present():
    questions = required_preflight_questions()

    assert "Is this target authorized?" in questions
    assert "Is this target inside scope?" in questions
    assert "Is Safe Mode enabled?" in questions


def test_active_action_blocks_without_scope_and_authorization():
    decision = SafetyPolicy().evaluate_action("active_test")

    assert decision.allowed is False
    assert decision.risk_level == RiskLevel.HIGH
    assert any("target authorized" in reason.lower() for reason in decision.reasons)
    assert any("not implemented" in reason.lower() for reason in decision.reasons)


def test_implemented_low_risk_action_can_pass_with_complete_answers():
    answers = PreflightAnswers(
        target_authorized=True,
        target_in_scope=True,
        test_allowed=True,
        rate_limit_configured=True,
        action_logged=True,
        evidence_capture=True,
        safe_mode_enabled=True,
    )
    policy = ActionPolicy(action="passive_review", risk_level=RiskLevel.LOW, implemented=True)

    decision = SafetyPolicy().evaluate_action(
        "passive_review",
        answers=answers,
        policy=policy,
        target="example.com",
    )

    assert decision.allowed is True

