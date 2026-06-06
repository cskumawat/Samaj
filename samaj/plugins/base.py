"""Plugin metadata base classes for Phase 12."""

from __future__ import annotations

from dataclasses import dataclass

from samaj.config.safety_policy import RiskLevel
from samaj.core.permissions import Permission


@dataclass(frozen=True)
class PluginMetadata:
    name: str
    version: str
    author: str
    description: str
    required_permissions: tuple[Permission, ...]
    supported_actions: tuple[str, ...]
    risk_level: RiskLevel
    safe_mode_behavior: str


class SamajPlugin:
    metadata: PluginMetadata

    def execute(self, *args, **kwargs):  # noqa: ANN002, ANN003
        raise NotImplementedError("Plugin execution is planned for Phase 12.")

