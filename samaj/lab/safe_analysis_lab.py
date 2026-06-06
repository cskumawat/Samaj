"""Safe Analysis Lab static-only orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from samaj.core.platform_paths import PlatformPaths
from samaj.lab.behavior_diagram import static_infection_flow_diagram
from samaj.lab.containment import CONTAINMENT_CHECKLIST
from samaj.lab.lab_policy import SAFE_LAB_MANDATORY_STATEMENT
from samaj.lab.static_analyzer import StaticAnalysisResult, import_and_analyze_static
from samaj.lab.yara_scanner import scan_with_yara_placeholder


@dataclass(frozen=True)
class SafeLabReport:
    result: StaticAnalysisResult
    mermaid_diagram: str
    containment_steps: tuple[str, ...]
    report_path: Path


def analyze_file_static_only(source_path: Path, paths: PlatformPaths) -> SafeLabReport:
    result = import_and_analyze_static(source_path, paths)
    yara = scan_with_yara_placeholder(result.quarantined_path, paths.lab_yara_dir)
    diagram = static_infection_flow_diagram(len(result.indicators))
    report = render_static_report(result, diagram, yara.status)
    report_path = paths.lab_reports_dir / f"static-report-{result.signature.sha256[:16]}.md"
    report_path.write_text(report, encoding="utf-8")
    return SafeLabReport(
        result=result,
        mermaid_diagram=diagram,
        containment_steps=CONTAINMENT_CHECKLIST,
        report_path=report_path,
    )


def render_static_report(result: StaticAnalysisResult, diagram: str, yara_status: str) -> str:
    indicators = "\n".join(f"- Observed: {item}" for item in result.indicators) or "- Unknown: none"
    return "\n".join(
        (
            "# Safe Analysis Lab Static Report",
            "",
            SAFE_LAB_MANDATORY_STATEMENT,
            "",
            "Verification status: Needs manual verification",
            "Execution performed: no",
            "Network access performed: no",
            "",
            f"Quarantined path: {result.quarantined_path}",
            f"File type: {result.signature.file_type}",
            f"MD5: {result.signature.md5}",
            f"SHA1: {result.signature.sha1}",
            f"SHA256: {result.signature.sha256}",
            f"YARA status: {yara_status}",
            "",
            "## Static Indicators",
            indicators,
            "",
            "## Learning Diagram",
            "```mermaid",
            diagram,
            "```",
            "",
            "## Defensive Containment Checklist",
            *(f"- {item}" for item in CONTAINMENT_CHECKLIST),
        )
    )
