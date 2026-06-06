"""Safe Analysis Lab static-only GUI view."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from samaj.config.settings import AppSettings
from samaj.core.audit import AuditLogger
from samaj.core.platform_paths import default_platform_paths
from samaj.lab.lab_policy import SAFE_LAB_MANDATORY_STATEMENT
from samaj.lab.safe_analysis_lab import analyze_file_static_only


class SafeLabView(QWidget):
    def __init__(
        self,
        settings: AppSettings,
        audit_logger: AuditLogger,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.settings = settings
        self.audit_logger = audit_logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Safe Analysis Lab")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        notice = QLabel(SAFE_LAB_MANDATORY_STATEMENT)
        notice.setObjectName("mutedText")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        path_row = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select a local file for static-only analysis")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        analyze_button = QPushButton("Static Analyze")
        analyze_button.clicked.connect(self.analyze_selected_file)
        path_row.addWidget(self.path_input, 1)
        path_row.addWidget(browse_button)
        path_row.addWidget(analyze_button)
        layout.addLayout(path_row)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlainText(
            "No file analyzed. This page copies selected files to project-local "
            "quarantine and performs hashes, file type checks, string extraction, "
            "and static indicator notes only."
        )
        layout.addWidget(self.output, 1)

    def browse_file(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select file for static analysis")
        if path:
            self.path_input.setText(path)

    def analyze_selected_file(self) -> None:
        source = Path(self.path_input.text().strip())
        if not source.exists() or not source.is_file():
            self.output.setPlainText("Select an existing local file first.")
            return

        report = analyze_file_static_only(source, default_platform_paths(self.settings.data_dir))
        result = report.result
        self.audit_logger.log(
            event_type="safe_lab_static_analysis",
            message="Safe Analysis Lab static-only analysis completed.",
            metadata={
                "source_name": source.name,
                "sha256": result.signature.sha256,
                "execution_performed": False,
                "network_performed": False,
                "report_path": str(report.report_path),
            },
        )
        indicators = "\n".join(f"- {item}" for item in result.indicators) or "- None observed"
        self.output.setPlainText(
            "\n".join(
                (
                    "Static analysis complete.",
                    "",
                    "Execution performed: no",
                    "Network access performed: no",
                    f"Quarantine copy: {result.quarantined_path}",
                    f"Report: {report.report_path}",
                    f"File type: {result.signature.file_type}",
                    f"MD5: {result.signature.md5}",
                    f"SHA1: {result.signature.sha1}",
                    f"SHA256: {result.signature.sha256}",
                    "",
                    "Static indicators:",
                    indicators,
                )
            )
        )
