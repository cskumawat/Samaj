"""Audit log viewer for Phase 1."""

from __future__ import annotations

import json

from PySide6.QtWidgets import QLabel, QPushButton, QTextEdit, QVBoxLayout, QWidget

from samaj.core.audit import AuditLogger


class LogsView(QWidget):
    def __init__(self, audit_logger: AuditLogger, parent=None) -> None:
        super().__init__(parent)
        self.audit_logger = audit_logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Logs and Audit Trail")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        layout.addWidget(self.log_text, 1)

        self.reload_button = QPushButton("Reload Logs")
        self.reload_button.clicked.connect(self.reload)
        layout.addWidget(self.reload_button)

        self.reload()

    def reload(self) -> None:
        events = self.audit_logger.read_events(limit=500)
        rendered = "\n".join(
            json.dumps(
                {
                    "timestamp": event.timestamp,
                    "event_type": event.event_type,
                    "message": event.message,
                    "metadata": event.metadata,
                },
                sort_keys=True,
            )
            for event in events
        )
        self.log_text.setPlainText(rendered)

