"""Tool knowledge-base dataclasses."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolKnowledgeRecord:
    tool_name: str
    category: str
    subcategory: str = ""
    description: str = "Unknown / Not verified"
    catalog_status: str = "knowledge-entry-only"
    support_status: str = "not implemented unless adapter exists"
    ai_suggested: str = "yes"
    verified_by_developer: str = "no"

