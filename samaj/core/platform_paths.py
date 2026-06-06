"""Project-local path management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlatformPaths:
    workspace: Path

    @property
    def logs_dir(self) -> Path:
        return self.workspace / "logs"

    @property
    def lab_quarantine_dir(self) -> Path:
        return self.workspace / "lab" / "quarantine"

    @property
    def lab_reports_dir(self) -> Path:
        return self.workspace / "lab" / "reports"

    @property
    def lab_yara_dir(self) -> Path:
        return self.workspace / "lab" / "yara"

    @property
    def lab_diagrams_dir(self) -> Path:
        return self.workspace / "lab" / "diagrams"

    @property
    def kb_dir(self) -> Path:
        return self.workspace / "kb"

    def ensure(self) -> None:
        for directory in (
            self.workspace,
            self.logs_dir,
            self.lab_quarantine_dir,
            self.lab_reports_dir,
            self.lab_yara_dir,
            self.lab_diagrams_dir,
            self.kb_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


def default_platform_paths(base_dir: Path | None = None) -> PlatformPaths:
    return PlatformPaths(workspace=(base_dir or Path.cwd() / ".samaj").resolve())

