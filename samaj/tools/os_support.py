"""OS support mapping helpers for catalog entries."""

from __future__ import annotations

from samaj.core.tool_compatibility import SupportValue, ToolCompatibility
from samaj.tools.catalog import ToolCatalogEntry


def compatibility_from_catalog_entry(entry: ToolCatalogEntry) -> ToolCompatibility:
    return ToolCompatibility(
        tool_name=entry.tool_name,
        category=entry.category,
        windows_supported=_support_value(entry.windows_supported),
        kali_supported=_support_value(entry.kali_supported),
        linux_supported=_support_value(entry.linux_supported),
        mac_supported=_support_value(entry.mac_supported),
        adapter_available=_support_value(entry.adapter_available),
        tested_by_samaj=_support_value(entry.verified_by_developer),
        install_method_windows=entry.install_method_windows,
        install_method_kali=entry.install_method_kali,
        install_method_linux=entry.install_method_linux,
        notes=entry.usage_notes,
    )


def _support_value(value: str) -> SupportValue:
    normalized = value.strip().lower()
    if normalized == "yes":
        return SupportValue.YES
    if normalized == "no":
        return SupportValue.NO
    return SupportValue.UNKNOWN

