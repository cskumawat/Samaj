"""YARA scanner placeholder.

YARA integration is intentionally optional and not required for static analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class YaraScanResult:
    rules_loaded: int
    matches: tuple[str, ...]
    status: str


def scan_with_yara_placeholder(sample_path: Path, rules_dir: Path) -> YaraScanResult:
    del sample_path
    if not rules_dir.exists():
        return YaraScanResult(rules_loaded=0, matches=(), status="no_rules_available")
    rule_count = len(list(rules_dir.glob("*.yar"))) + len(list(rules_dir.glob("*.yara")))
    return YaraScanResult(rules_loaded=rule_count, matches=(), status="placeholder_no_execution")

