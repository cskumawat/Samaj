"""Safe Analysis Lab policy."""

from __future__ import annotations

from dataclasses import dataclass

SAFE_LAB_MANDATORY_STATEMENT = (
    "Safe Analysis Lab does not execute malware on the host and must not be "
    "treated as a complete malware sandbox until dynamic VM isolation is "
    "separately implemented and tested."
)


@dataclass(frozen=True)
class LabPolicy:
    network_enabled: bool = False
    execution_enabled: bool = False
    host_filesystem_write_enabled: bool = False
    dynamic_analysis_enabled: bool = False
    quarantine_required: bool = True
    static_analysis_first: bool = True

    def validate_static_only(self) -> bool:
        return (
            not self.network_enabled
            and not self.execution_enabled
            and not self.dynamic_analysis_enabled
            and self.quarantine_required
            and self.static_analysis_first
        )


DEFAULT_LAB_POLICY = LabPolicy()

