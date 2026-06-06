"""Policy-gated proxy test preview.

No live network test is performed in this foundation phase.
"""

from __future__ import annotations

from dataclasses import dataclass

from samaj.db.models import ProxyRecord
from samaj.proxy.proxy_policy import validate_proxy_test_request


@dataclass(frozen=True)
class ProxyTestPreview:
    allowed: bool
    reason: str
    test_url: str
    proxy: str
    live_network_performed: bool = False


def preview_proxy_test(proxy: ProxyRecord, *, approved: bool, test_url: str) -> ProxyTestPreview:
    allowed, reason = validate_proxy_test_request(approved, test_url)
    return ProxyTestPreview(
        allowed=allowed,
        reason=reason,
        test_url=test_url,
        proxy=f"{proxy.type}://{proxy.ip}:{proxy.port}",
        live_network_performed=False,
    )

