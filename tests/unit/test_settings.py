from __future__ import annotations

import json

from samaj.config.settings import AppSettings, load_settings, save_settings


def test_settings_default_safe_modes_are_on(tmp_path):
    settings = AppSettings(data_dir=tmp_path)

    assert settings.safe_mode is True
    assert settings.anti_hallucination_mode is True
    assert settings.show_safety_banner is True
    assert settings.audit_log_path == tmp_path / "audit.jsonl"


def test_settings_persist_and_force_anti_hallucination(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings = AppSettings(data_dir=tmp_path, analyst_name="Analyst", theme="dark")

    save_settings(settings, settings_path)
    loaded = load_settings(settings_path)

    assert loaded.analyst_name == "Analyst"
    assert loaded.theme == "dark"
    assert loaded.safe_mode is True
    assert loaded.anti_hallucination_mode is True
    assert loaded.show_safety_banner is True


def test_tampered_settings_cannot_disable_anti_hallucination_or_banner(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text(
        json.dumps(
            {
                "data_dir": str(tmp_path),
                "safe_mode": False,
                "anti_hallucination_mode": False,
                "show_safety_banner": False,
            }
        ),
        encoding="utf-8",
    )

    loaded = load_settings(settings_path)

    assert loaded.safe_mode is False
    assert loaded.anti_hallucination_mode is True
    assert loaded.show_safety_banner is True

