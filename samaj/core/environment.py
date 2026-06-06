"""Runtime environment summary."""

from __future__ import annotations

import sys
from dataclasses import dataclass

from samaj.core.os_detect import OperatingSystem, detect_os


@dataclass(frozen=True)
class EnvironmentSummary:
    operating_system: OperatingSystem
    python_executable: str
    python_version: str
    venv_active: bool


def current_environment() -> EnvironmentSummary:
    return EnvironmentSummary(
        operating_system=detect_os(),
        python_executable=sys.executable,
        python_version=sys.version.split()[0],
        venv_active=sys.prefix != sys.base_prefix,
    )

