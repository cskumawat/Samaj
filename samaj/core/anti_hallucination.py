"""Anti-hallucination primitives for evidence-based generated text."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from samaj.config.defaults import HALLUCINATION_WARNING_TEXT

HALLUCINATION_WARNING_BANNER = HALLUCINATION_WARNING_TEXT


class VerificationStatus(StrEnum):
    OBSERVED = "observed"
    INFERRED = "inferred"
    UNVERIFIED = "unverified"
    FALSE_POSITIVE = "false_positive"
    NEEDS_MANUAL_REVIEW = "needs_manual_review"


class StatementKind(StrEnum):
    OBSERVED_FACT = "observed_fact"
    INFERENCE = "inference"
    HYPOTHESIS = "hypothesis"
    RECOMMENDATION = "recommendation"
    NEEDS_MANUAL_VERIFICATION = "needs_manual_verification"


@dataclass(frozen=True)
class EvidenceRecord:
    source: str
    timestamp: datetime
    tool: str
    command: str
    raw_evidence: str
    analyst_note: str = ""
    confidence_score: float = 0.0
    evidence_id: str = field(default_factory=lambda: str(uuid4()))

    def is_complete(self) -> bool:
        return not EvidenceChecker.missing_required_fields(self)


@dataclass(frozen=True)
class TaggedStatement:
    text: str
    kind: StatementKind
    verification_status: VerificationStatus
    confidence_label: str
    evidence_ids: tuple[str, ...] = ()
    source_ids: tuple[str, ...] = ()
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class ClaimValidationResult:
    allowed: bool
    verification_status: VerificationStatus
    confidence_label: str
    missing_evidence: tuple[str, ...] = ()
    warnings: tuple[str, ...] = ()


class EvidenceChecker:
    REQUIRED_FIELDS = (
        "source",
        "timestamp",
        "tool",
        "command",
        "raw_evidence",
        "analyst_note",
        "confidence_score",
    )

    @classmethod
    def missing_required_fields(
        cls,
        evidence: EvidenceRecord | Mapping[str, Any],
    ) -> tuple[str, ...]:
        missing: list[str] = []
        for field_name in cls.REQUIRED_FIELDS:
            value = getattr(evidence, field_name, None)
            if isinstance(evidence, Mapping):
                value = evidence.get(field_name)
            if value is None or value == "":
                missing.append(field_name)
        return tuple(missing)

    @classmethod
    def has_minimum_evidence(cls, evidence: EvidenceRecord | Mapping[str, Any] | None) -> bool:
        if evidence is None:
            return False
        return not cls.missing_required_fields(evidence)


class ConfidenceLabeler:
    @staticmethod
    def label(score: float | None) -> str:
        if score is None:
            return "unknown"
        if score >= 0.85:
            return "high"
        if score >= 0.55:
            return "medium"
        if score > 0:
            return "low"
        return "unknown"


class SourceTracker:
    def __init__(self) -> None:
        self._sources: dict[str, str] = {}

    def add_source(self, source: str) -> str:
        source_id = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
        self._sources[source_id] = source
        return source_id

    def get_source(self, source_id: str) -> str | None:
        return self._sources.get(source_id)

    def all_sources(self) -> dict[str, str]:
        return dict(self._sources)


class MissingEvidenceDetector:
    @staticmethod
    def for_finding(finding: Mapping[str, Any]) -> tuple[str, ...]:
        required = (
            "source",
            "timestamp",
            "tool",
            "command",
            "raw_evidence",
            "analyst_note",
            "confidence_score",
            "verification_status",
        )
        return tuple(key for key in required if not finding.get(key))


class ClaimValidator:
    @staticmethod
    def validate(
        statement_text: str,
        kind: StatementKind,
        evidence: EvidenceRecord | Mapping[str, Any] | None = None,
        severity_reasoning: str | None = None,
    ) -> ClaimValidationResult:
        missing = (
            EvidenceChecker.missing_required_fields(evidence)
            if evidence
            else EvidenceChecker.REQUIRED_FIELDS
        )
        warnings: list[str] = []

        if kind == StatementKind.OBSERVED_FACT and missing:
            warnings.append("Observed claims require complete evidence.")
            return ClaimValidationResult(
                allowed=False,
                verification_status=VerificationStatus.UNVERIFIED,
                confidence_label="unknown",
                missing_evidence=tuple(missing),
                warnings=tuple(warnings),
            )

        if "severity" in statement_text.lower() and not severity_reasoning:
            warnings.append("Severity claims require reasoning.")

        if missing:
            status = VerificationStatus.NEEDS_MANUAL_REVIEW
            confidence_label = "unknown"
        elif kind == StatementKind.INFERENCE:
            status = VerificationStatus.INFERRED
            confidence_label = ConfidenceLabeler.label(_confidence_from_evidence(evidence))
        else:
            status = VerificationStatus.OBSERVED
            confidence_label = ConfidenceLabeler.label(_confidence_from_evidence(evidence))

        return ClaimValidationResult(
            allowed=not warnings or kind != StatementKind.OBSERVED_FACT,
            verification_status=status,
            confidence_label=confidence_label,
            missing_evidence=tuple(missing),
            warnings=tuple(warnings),
        )


class AIOutputSafetyWrapper:
    @staticmethod
    def wrap(
        statement_text: str,
        kind: StatementKind,
        evidence: EvidenceRecord | Mapping[str, Any] | None = None,
        source_tracker: SourceTracker | None = None,
    ) -> TaggedStatement:
        validation = ClaimValidator.validate(statement_text, kind, evidence)
        evidence_ids: tuple[str, ...] = ()
        source_ids: tuple[str, ...] = ()

        if isinstance(evidence, EvidenceRecord):
            evidence_ids = (evidence.evidence_id,)
            if source_tracker is not None:
                source_ids = (source_tracker.add_source(evidence.source),)
        elif isinstance(evidence, Mapping) and evidence.get("evidence_id"):
            evidence_ids = (str(evidence["evidence_id"]),)
            if source_tracker is not None and evidence.get("source"):
                source_ids = (source_tracker.add_source(str(evidence["source"])),)

        return TaggedStatement(
            text=statement_text,
            kind=kind,
            verification_status=validation.verification_status,
            confidence_label=validation.confidence_label,
            evidence_ids=evidence_ids,
            source_ids=source_ids,
        )


def determine_verification_status(
    evidence: EvidenceRecord | Mapping[str, Any] | None,
    *,
    inferred: bool = False,
    false_positive: bool = False,
) -> VerificationStatus:
    if false_positive:
        return VerificationStatus.FALSE_POSITIVE
    if not EvidenceChecker.has_minimum_evidence(evidence):
        return VerificationStatus.NEEDS_MANUAL_REVIEW
    if inferred:
        return VerificationStatus.INFERRED
    return VerificationStatus.OBSERVED


def enforce_do_not_guess(
    request_text: str,
    evidence: EvidenceRecord | Mapping[str, Any] | None = None,
) -> ClaimValidationResult:
    asks_for_confirmation = any(
        phrase in request_text.lower()
        for phrase in (
            "confirm this vulnerability",
            "mark as confirmed",
            "prove impact",
            "assign severity",
        )
    )

    if asks_for_confirmation and not EvidenceChecker.has_minimum_evidence(evidence):
        return ClaimValidationResult(
            allowed=False,
            verification_status=VerificationStatus.UNVERIFIED,
            confidence_label="unknown",
            missing_evidence=EvidenceChecker.REQUIRED_FIELDS,
            warnings=("Missing evidence. Ask for evidence instead of guessing.",),
        )

    return ClaimValidationResult(
        allowed=True,
        verification_status=determine_verification_status(evidence),
        confidence_label=ConfidenceLabeler.label(_confidence_from_evidence(evidence)),
    )


def _confidence_from_evidence(evidence: EvidenceRecord | Mapping[str, Any] | None) -> float | None:
    if evidence is None:
        return None
    if isinstance(evidence, EvidenceRecord):
        return evidence.confidence_score
    value = evidence.get("confidence_score")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
