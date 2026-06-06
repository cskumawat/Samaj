"""Permission labels for future plugins and tool execution."""

from __future__ import annotations

from enum import StrEnum


class Permission(StrEnum):
    READ_PROJECT = "read_project"
    WRITE_PROJECT = "write_project"
    READ_EVIDENCE = "read_evidence"
    WRITE_EVIDENCE = "write_evidence"
    NETWORK_PASSIVE = "network_passive"
    NETWORK_ACTIVE = "network_active"
    RUN_EXTERNAL_COMMAND = "run_external_command"


SAFE_DEFAULT_PERMISSIONS = (
    Permission.READ_PROJECT,
    Permission.READ_EVIDENCE,
)
