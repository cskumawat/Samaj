"""Default values for Samaj."""

from __future__ import annotations

import os
from pathlib import Path

from samaj import APP_NAME, APP_VERSION

SETTINGS_FILENAME = "settings.json"
AUDIT_LOG_FILENAME = "audit.jsonl"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_THEME = "dark"

SAFETY_BANNER_TEXT = (
    "SAFE MODE: ON | ANTI-HALLUCINATION: ON | SCOPE REQUIRED | AUTHORIZED USE ONLY"
)
UNSAFE_MODE_BANNER_TEXT = (
    "WARNING: SAFE MODE DISABLED | ANTI-HALLUCINATION: ON | SCOPE REQUIRED | "
    "AUTHORIZED USE ONLY"
)
HALLUCINATION_WARNING_TEXT = "ANTI-HALLUCINATION MODE: ON | EVIDENCE REQUIRED | DO NOT GUESS"

IMPLEMENTED_PHASES = ("Phase 0", "Phase 1", "Phase 2 foundation")
PLANNED_PHASE_NOTICE = "Planned for a later phase. This feature is not implemented yet."


def default_data_dir() -> Path:
    configured = os.getenv("SAMAJ_DATA_DIR")
    if configured:
        return Path(configured).expanduser()
    return Path.cwd() / ".samaj"


def default_settings_path() -> Path:
    configured = os.getenv("SAMAJ_SETTINGS_PATH")
    if configured:
        return Path(configured).expanduser()
    return default_data_dir() / SETTINGS_FILENAME


def default_audit_log_path(data_dir: Path | None = None) -> Path:
    base_dir = data_dir or default_data_dir()
    return base_dir / AUDIT_LOG_FILENAME


__all__ = [
    "APP_NAME",
    "APP_VERSION",
    "AUDIT_LOG_FILENAME",
    "DEFAULT_LOG_LEVEL",
    "DEFAULT_THEME",
    "HALLUCINATION_WARNING_TEXT",
    "IMPLEMENTED_PHASES",
    "PLANNED_PHASE_NOTICE",
    "SAFETY_BANNER_TEXT",
    "SETTINGS_FILENAME",
    "UNSAFE_MODE_BANNER_TEXT",
    "default_audit_log_path",
    "default_data_dir",
    "default_settings_path",
]
