"""Safe tool registry placeholders for Phase 9."""

from __future__ import annotations

from dataclasses import dataclass

from samaj.config.safety_policy import RiskLevel


@dataclass(frozen=True)
class ToolRegistryEntry:
    tool_name: str
    category: str
    description: str
    installed: bool = False
    version: str | None = None
    command_path: str | None = None
    safe_mode_compatible: bool = True
    requires_scope: bool = True
    requires_confirmation: bool = True
    supports_rate_limit: bool = False
    risk_level: RiskLevel = RiskLevel.HIGH
    documentation_url: str = ""
    license: str = ""
    notes: str = "Tool execution is planned for Phase 9."


class ToolRegistry:
    def __init__(self) -> None:
        self._entries: dict[str, ToolRegistryEntry] = {}

    def register(self, entry: ToolRegistryEntry) -> None:
        self._entries[entry.tool_name] = entry

    def list_entries(self) -> list[ToolRegistryEntry]:
        return list(self._entries.values())
