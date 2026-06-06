"""Phase-wise external tool catalog intake loader."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CATALOG_MANIFEST_PATH = Path(__file__).with_name("catalog_manifest.json")


@dataclass(frozen=True)
class ToolCatalogEntry:
    sequence: int
    tool_name: str
    name: str
    category: str
    subcategory: str
    planned_phase: str
    description: str
    catalog_status: str
    support_status: str
    safety_note: str
    license_note: str
    official_url: str
    install_notes: str
    user_notes: str
    ai_suggested: str
    verified_by_developer: str
    source_note: str
    install_status: str
    documentation_url: str
    disclaimer_status: str
    imported_from: str
    active_execution_supported: bool
    bundled_by_samaj: bool
    tested_by_samaj: bool
    recommended_by_samaj: bool
    windows_supported: str
    kali_supported: str
    linux_supported: str
    mac_supported: str
    install_method_windows: str
    install_method_kali: str
    install_method_linux: str
    license: str
    adapter_available: str
    safe_mode_required: str
    scope_required: str
    requires_admin_or_root: str
    requires_network: str
    requires_api_key: str
    usage_notes: str
    legal_notes: str


def load_catalog_manifest(path: Path = CATALOG_MANIFEST_PATH) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def list_catalog_entries(path: Path = CATALOG_MANIFEST_PATH) -> list[ToolCatalogEntry]:
    manifest = load_catalog_manifest(path)
    entries: list[ToolCatalogEntry] = []
    for category in manifest["categories"]:
        for tool in category["entries"]:
            entries.append(
                ToolCatalogEntry(
                    sequence=int(tool["sequence"]),
                    tool_name=tool["tool_name"],
                    name=tool["name"],
                    category=tool.get("category", category["category"]),
                    subcategory=tool.get("subcategory", ""),
                    planned_phase=tool.get("planned_phase", category.get("planned_phase", "")),
                    description=tool["description"],
                    catalog_status=tool["catalog_status"],
                    support_status=tool["support_status"],
                    safety_note=tool["safety_note"],
                    license_note=tool["license_note"],
                    official_url=tool["official_url"],
                    install_notes=tool["install_notes"],
                    user_notes=tool["user_notes"],
                    ai_suggested=tool["ai_suggested"],
                    verified_by_developer=tool["verified_by_developer"],
                    source_note=tool["source_note"],
                    install_status=tool["install_status"],
                    documentation_url=tool["documentation_url"],
                    disclaimer_status=tool["disclaimer_status"],
                    imported_from=tool.get("imported_from", "user_pasted_tool_inventory"),
                    active_execution_supported=tool["active_execution_supported"],
                    bundled_by_samaj=tool["bundled_by_samaj"],
                    tested_by_samaj=tool["tested_by_samaj"],
                    recommended_by_samaj=tool["recommended_by_samaj"],
                    windows_supported=tool["windows_supported"],
                    kali_supported=tool["kali_supported"],
                    linux_supported=tool["linux_supported"],
                    mac_supported=tool["mac_supported"],
                    install_method_windows=tool["install_method_windows"],
                    install_method_kali=tool["install_method_kali"],
                    install_method_linux=tool["install_method_linux"],
                    license=tool["license"],
                    adapter_available=tool["adapter_available"],
                    safe_mode_required=tool["safe_mode_required"],
                    scope_required=tool["scope_required"],
                    requires_admin_or_root=tool["requires_admin_or_root"],
                    requires_network=tool["requires_network"],
                    requires_api_key=tool["requires_api_key"],
                    usage_notes=tool["usage_notes"],
                    legal_notes=tool["legal_notes"],
                )
            )
    return entries
