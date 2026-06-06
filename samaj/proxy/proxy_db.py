"""Proxy database service helpers."""

from __future__ import annotations

from sqlalchemy.orm import Session

from samaj.db.crud import SamajRepository
from samaj.db.models import ProxyRecord
from samaj.proxy.proxy_importer import parse_proxy_lines


def import_proxy_lines(
    session: Session,
    lines: list[str] | tuple[str, ...],
    *,
    source: str = "manual",
) -> list[ProxyRecord]:
    repository = SamajRepository(session)
    records: list[ProxyRecord] = []
    for entry in parse_proxy_lines(lines):
        records.append(
            repository.upsert_proxy(
                ip=entry.ip,
                port=entry.port,
                proxy_type=entry.proxy_type,
                source=source,
            )
        )
    return records

