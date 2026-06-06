from __future__ import annotations

from datetime import UTC, datetime

from samaj.core.anti_hallucination import (
    AIOutputSafetyWrapper,
    ClaimValidator,
    ConfidenceLabeler,
    EvidenceRecord,
    StatementKind,
    VerificationStatus,
    enforce_do_not_guess,
)


def test_observed_claim_without_evidence_is_rejected():
    result = ClaimValidator.validate(
        "Observed missing security header.",
        StatementKind.OBSERVED_FACT,
        evidence=None,
    )

    assert result.allowed is False
    assert result.verification_status == VerificationStatus.UNVERIFIED
    assert "raw_evidence" in result.missing_evidence


def test_observed_claim_with_evidence_is_tagged():
    evidence = EvidenceRecord(
        source="manual",
        timestamp=datetime.now(UTC),
        tool="analyst",
        command="manual review",
        raw_evidence="Header X-Example was observed in a saved response.",
        analyst_note="Non-sensitive manual test fixture.",
        confidence_score=0.9,
    )

    tagged = AIOutputSafetyWrapper.wrap(
        "Observed header X-Example in the supplied evidence.",
        StatementKind.OBSERVED_FACT,
        evidence=evidence,
    )

    assert tagged.verification_status == VerificationStatus.OBSERVED
    assert tagged.confidence_label == "high"
    assert tagged.evidence_ids == (evidence.evidence_id,)


def test_do_not_guess_blocks_confirmation_without_evidence():
    result = enforce_do_not_guess("Mark as confirmed and assign severity.")

    assert result.allowed is False
    assert result.verification_status == VerificationStatus.UNVERIFIED
    assert result.warnings


def test_confidence_labels_are_conservative():
    assert ConfidenceLabeler.label(None) == "unknown"
    assert ConfidenceLabeler.label(0.2) == "low"
    assert ConfidenceLabeler.label(0.7) == "medium"
    assert ConfidenceLabeler.label(0.95) == "high"

