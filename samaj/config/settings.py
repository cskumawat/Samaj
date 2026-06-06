"""Settings model and JSON persistence."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from samaj.config.defaults import (
    DEFAULT_LOG_LEVEL,
    default_audit_log_path,
    default_data_dir,
    default_settings_path,
)


class AppSettings(BaseModel):
    """Local application settings.

    Anti-Hallucination Mode and the safety banner are intentionally forced ON.
    Safe Mode defaults ON. Future phases may show stronger warnings if a user
    explicitly disables Safe Mode, but Phase 1 does not provide active testing.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    data_dir: Path = Field(default_factory=default_data_dir)
    audit_log_path: Path | None = None
    log_level: str = DEFAULT_LOG_LEVEL
    theme: Literal["system", "light", "dark"] = "system"
    analyst_name: str = ""
    safe_mode: bool = True
    anti_hallucination_mode: Literal[True] = True
    show_safety_banner: Literal[True] = True

    @field_validator("anti_hallucination_mode", mode="before")
    @classmethod
    def force_anti_hallucination_on(cls, value: object) -> bool:
        return True

    @field_validator("show_safety_banner", mode="before")
    @classmethod
    def force_safety_banner_visible(cls, value: object) -> bool:
        return True

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        normalized = value.upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed:
            return DEFAULT_LOG_LEVEL
        return normalized

    @model_validator(mode="after")
    def fill_derived_paths(self) -> AppSettings:
        object.__setattr__(self, "data_dir", Path(self.data_dir).expanduser())
        if self.audit_log_path is None:
            object.__setattr__(self, "audit_log_path", default_audit_log_path(self.data_dir))
        else:
            object.__setattr__(self, "audit_log_path", Path(self.audit_log_path).expanduser())
        return self


def settings_path(path: Path | None = None) -> Path:
    return Path(path).expanduser() if path else default_settings_path()


def ensure_runtime_dirs(settings: AppSettings) -> None:
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    if settings.audit_log_path is not None:
        settings.audit_log_path.parent.mkdir(parents=True, exist_ok=True)


def load_settings(path: Path | None = None) -> AppSettings:
    resolved_path = settings_path(path)
    raw: dict[str, object] = {}

    if resolved_path.exists():
        with resolved_path.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)

    if os.getenv("SAMAJ_LOG_LEVEL"):
        raw["log_level"] = os.getenv("SAMAJ_LOG_LEVEL")
    if os.getenv("SAMAJ_DATA_DIR"):
        raw["data_dir"] = os.getenv("SAMAJ_DATA_DIR")

    settings = AppSettings(**cast(dict[str, Any], raw))
    ensure_runtime_dirs(settings)
    if not resolved_path.exists():
        save_settings(settings, resolved_path)
    return settings


def save_settings(settings: AppSettings, path: Path | None = None) -> Path:
    resolved_path = settings_path(path)
    ensure_runtime_dirs(settings)
    resolved_path.parent.mkdir(parents=True, exist_ok=True)
    data = settings.model_dump(mode="json")
    data["anti_hallucination_mode"] = True
    data["show_safety_banner"] = True
    with resolved_path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")
    return resolved_path
