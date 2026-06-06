"""Evidence metadata helpers for future evidence storage."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from samaj.core.anti_hallucination import VerificationStatus


@dataclass(frozen=True)
class EvidenceMetadata:
    evidence_id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str | None = None
    asset_id: str | None = None
    finding_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    source: str = ""
    tool: str = ""
    command: str = ""
    analyst_note: str = ""
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    file_hash_sha256: str | None = None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()

