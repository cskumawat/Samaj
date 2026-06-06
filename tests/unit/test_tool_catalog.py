from __future__ import annotations

from samaj.tools.catalog import list_catalog_entries, load_catalog_manifest


def test_tool_catalog_manifest_contains_full_intake():
    manifest = load_catalog_manifest()
    entries = list_catalog_entries()
    names = {entry.name for entry in entries}

    assert manifest["total_categories"] == 45
    assert manifest["total_tool_entries"] == 1620
    assert len(entries) == 1620
    assert "Nmap" in names
    assert "Metasploit Framework — authorized lab/testing only" in names
    assert "Final release freeze checklist" in names


def test_tool_catalog_entries_are_neutral_intake_only():
    entries = list_catalog_entries()

    assert all(entry.install_status == "not_checked" for entry in entries)
    assert all(
        entry.support_status == "not implemented unless adapter exists"
        for entry in entries
    )
    assert all(entry.catalog_status == "knowledge-entry-only" for entry in entries)
    assert all(entry.disclaimer_status == "requires_user_acceptance" for entry in entries)
    assert all(entry.active_execution_supported is False for entry in entries)
    assert all(entry.bundled_by_samaj is False for entry in entries)
    assert all(entry.tested_by_samaj is False for entry in entries)
    assert all(entry.recommended_by_samaj is False for entry in entries)
    assert all(entry.ai_suggested in {"yes", "no"} for entry in entries)
    assert all(entry.verified_by_developer in {"yes", "no"} for entry in entries)
    assert all(entry.windows_supported == "unknown" for entry in entries)
    assert all(entry.kali_supported == "unknown" for entry in entries)
