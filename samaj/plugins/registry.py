"""Plugin registry placeholder."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginRegistryEntry:
    name: str
    version: str
    enabled: bool = False
    reason: str = "Plugin registry is planned for Phase 12."

