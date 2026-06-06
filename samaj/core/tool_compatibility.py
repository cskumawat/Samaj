"""Tool compatibility mapping primitives."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SupportValue(StrEnum):
    YES = "yes"
    NO = "no"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ToolCompatibility:
    tool_name: str
    category: str
    windows_supported: SupportValue = SupportValue.UNKNOWN
    kali_supported: SupportValue = SupportValue.UNKNOWN
    linux_supported: SupportValue = SupportValue.UNKNOWN
    mac_supported: SupportValue = SupportValue.UNKNOWN
    adapter_available: SupportValue = SupportValue.NO
    tested_by_samaj: SupportValue = SupportValue.NO
    install_method_windows: str = "Unknown / Not verified"
    install_method_kali: str = "Unknown / Not verified"
    install_method_linux: str = "Unknown / Not verified"
    notes: str = "Knowledge entry only."

    @property
    def supported_on_both_windows_and_kali(self) -> bool:
        return (
            self.windows_supported == SupportValue.YES
            and self.kali_supported == SupportValue.YES
        )

