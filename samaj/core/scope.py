"""Conservative scope helpers.

Full project-backed scope management is planned for Phase 3. These helpers are
small primitives used by tests and future modules; they do not replace project
scope CRUD.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class ScopeDecision:
    target: str
    in_scope: bool
    reason: str


def normalize_host(target: str) -> str:
    parsed = urlparse(target if "://" in target else f"//{target}")
    host = parsed.hostname or target
    return host.strip().lower().rstrip(".")


def is_target_in_scope(
    target: str,
    allowed_hosts: list[str] | tuple[str, ...] | None = None,
) -> bool:
    if not target or not allowed_hosts:
        return False
    host = normalize_host(target)
    allowed = tuple(normalize_host(item) for item in allowed_hosts)
    return any(host == item or host.endswith(f".{item}") for item in allowed)


def evaluate_target_scope(
    target: str,
    allowed_hosts: list[str] | tuple[str, ...] | None = None,
) -> ScopeDecision:
    in_scope = is_target_in_scope(target, allowed_hosts)
    reason = (
        "Target matched configured scope."
        if in_scope
        else "Target is not in configured scope."
    )
    return ScopeDecision(target=target, in_scope=in_scope, reason=reason)
