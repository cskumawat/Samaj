"""Small rate-limit data structures for future modules."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RateLimitRule:
    requests_per_minute: int

    def is_configured(self) -> bool:
        return self.requests_per_minute > 0


def is_rate_limit_allowed(rule: RateLimitRule | None) -> bool:
    return bool(rule and rule.is_configured())

