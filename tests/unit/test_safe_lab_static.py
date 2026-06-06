from __future__ import annotations

from samaj.core.platform_paths import default_platform_paths
from samaj.lab.safe_analysis_lab import analyze_file_static_only


def test_safe_lab_static_analysis_does_not_execute_or_network(tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("powershell http://example.invalid password", encoding="utf-8")
    paths = default_platform_paths(tmp_path / ".samaj")

    report = analyze_file_static_only(sample, paths)

    assert report.result.quarantined_path.exists()
    assert report.report_path.exists()
    assert report.result.policy.execution_enabled is False
    assert report.result.policy.network_enabled is False
    assert any("powershell" in indicator for indicator in report.result.indicators)
    assert "Execution performed: no" in report.report_path.read_text(encoding="utf-8")
