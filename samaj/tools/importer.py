"""Tool catalog import helpers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from samaj.db.crud import SamajRepository
from samaj.tools.catalog import list_catalog_entries


def import_default_catalog(session: Session) -> int:
    return SamajRepository(session).import_tool_catalog_entries(list_catalog_entries())

