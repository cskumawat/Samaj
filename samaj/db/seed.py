"""Seed helpers for local Phase 2 demos."""

from __future__ import annotations

from sqlalchemy.orm import Session

from samaj.db.crud import SamajRepository


def seed_demo_project(session: Session) -> str:
    repository = SamajRepository(session)
    project = repository.create_project(
        "Demo Authorized Assessment",
        client_organization="Example Organization",
        authorization_notes="Example only. Replace with real written authorization.",
        scope_summary="example.com",
        allowed_test_types="passive_recon, manual_review",
        rate_limits="30 requests per minute",
    )
    repository.create_scope_item(
        project.id,
        "domain",
        "example.com",
        authorized_test_types=("passive_recon", "manual_review"),
        notes="Demo scope item. This does not grant authorization.",
    )
    return project.id
