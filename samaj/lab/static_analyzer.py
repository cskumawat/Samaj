"""Static-only file analyzer."""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from samaj.core.platform_paths import PlatformPaths
from samaj.lab.lab_policy import DEFAULT_LAB_POLICY, LabPolicy
from samaj.lab.signature_analyzer import FileSignature, analyze_signature


@dataclass(frozen=True)
class StaticAnalysisResult:
    original_path: Path
    quarantined_path: Path
    signature: FileSignature
    strings: tuple[str, ...]
    indicators: tuple[str, ...]
    policy: LabPolicy


def import_and_analyze_static(
    source_path: Path,
    paths: PlatformPaths,
    policy: LabPolicy = DEFAULT_LAB_POLICY,
) -> StaticAnalysisResult:
    if not policy.validate_static_only():
        raise ValueError("Safe Analysis Lab policy must remain static-only for this phase.")
    paths.ensure()
    source = Path(source_path).resolve()
    signature = analyze_signature(source)
    safe_name = f"sample-{signature.sha256[:16]}.bin"
    quarantined = paths.lab_quarantine_dir / safe_name
    shutil.copy2(source, quarantined)
    quarantined_signature = analyze_signature(quarantined)
    strings = extract_strings(quarantined)
    indicators = detect_static_indicators(strings, quarantined_signature)
    return StaticAnalysisResult(
        original_path=source,
        quarantined_path=quarantined,
        signature=quarantined_signature,
        strings=tuple(strings),
        indicators=tuple(indicators),
        policy=policy,
    )


def extract_strings(path: Path, min_length: int = 4, max_strings: int = 500) -> list[str]:
    data = Path(path).read_bytes()
    pattern = rb"[ -~]{" + str(min_length).encode("ascii") + rb",}"
    found = [
        match.group(0).decode("ascii", errors="ignore")
        for match in re.finditer(pattern, data)
    ]
    return found[:max_strings]


def detect_static_indicators(
    strings: tuple[str, ...] | list[str],
    signature: FileSignature,
) -> list[str]:
    indicators: list[str] = []
    lower_strings = [item.lower() for item in strings]
    suspicious_terms = ("powershell", "cmd.exe", "http://", "https://", "autorun", "password")
    for term in suspicious_terms:
        if any(term in item for item in lower_strings):
            indicators.append(f"Observed static string containing: {term}")
    if signature.file_type in {"Windows PE executable or DLL", "ELF binary"}:
        indicators.append(f"Observed executable-like file type: {signature.file_type}")
    return indicators
