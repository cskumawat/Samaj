from __future__ import annotations

from samaj.db.crud import SamajRepository
from samaj.db.database import DatabaseManager, default_database_config
from samaj.proxy.proxy_db import import_proxy_lines
from samaj.proxy.proxy_policy import PROXY_MANDATORY_STATEMENT
from samaj.proxy.proxy_tester import preview_proxy_test


def test_proxy_import_stores_inventory_without_live_testing(tmp_path):
    manager = DatabaseManager(default_database_config(tmp_path))
    manager.init()

    with manager.session() as session:
        records = import_proxy_lines(
            session,
            ["http://127.0.0.1:8080", "127.0.0.1:8080", "bad-line"],
            source="test",
        )
        stored = SamajRepository(session).list_proxies()
        preview = preview_proxy_test(stored[0], approved=True, test_url="https://example.com")

    assert len(records) == 2
    assert len(stored) == 2
    assert preview.live_network_performed is False
    assert preview.allowed is False
    assert "not implemented" in preview.reason
    assert "Proxy features must not be used for illegal activity" in PROXY_MANDATORY_STATEMENT
