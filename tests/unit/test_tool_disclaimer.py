from __future__ import annotations

from samaj.tools.disclaimer import TOOL_CATALOG_ACCEPTANCE_LABEL, TOOL_CATALOG_DISCLAIMER_TEXT


def test_tool_catalog_disclaimer_contains_required_boundaries():
    assert "lawful, educational, defensive" in TOOL_CATALOG_DISCLAIMER_TEXT
    assert "does not mean tool support" in TOOL_CATALOG_DISCLAIMER_TEXT
    assert "does not mean Samaj endorses it" in TOOL_CATALOG_DISCLAIMER_TEXT
    assert "Proxy features must not be used for illegal activity" in TOOL_CATALOG_DISCLAIMER_TEXT
    assert "Safe Analysis Lab does not execute malware on the host" in (
        TOOL_CATALOG_DISCLAIMER_TEXT
    )
    assert "not support, endorsement, verification" in TOOL_CATALOG_ACCEPTANCE_LABEL
