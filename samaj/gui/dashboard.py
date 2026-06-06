"""Dashboard view for the Samaj GUI shell."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QGridLayout, QLabel, QVBoxLayout, QWidget

from samaj.config.settings import AppSettings


class DashboardView(QWidget):
    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(18)

        title = QLabel("Dashboard")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        grid = QGridLayout()
        grid.setSpacing(12)
        layout.addLayout(grid)

        cards = (
            ("Safe Mode", "ON" if settings.safe_mode else "OFF"),
            ("Anti-Hallucination", "ON"),
            ("Audit Log", str(settings.audit_log_path)),
            ("Implemented", "Phase 0, Phase 1, and Phase 2 foundation"),
        )
        for index, (label, value) in enumerate(cards):
            grid.addWidget(_StatusCard(label, value), index // 2, index % 2)

        status = QLabel(
            "Current foundation includes project database records, neutral Tool Catalog intake, "
            "disclaimer acceptance, OS support mapping, static-only lab analysis, proxy database "
            "storage, audit logging, and theme assets. Catalog tool execution remains "
            "unimplemented."
        )
        status.setWordWrap(True)
        status.setObjectName("mutedText")
        layout.addWidget(status)
        layout.addStretch(1)


class _StatusCard(QFrame):
    def __init__(self, label: str, value: str, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("statusCard")
        self.setMinimumHeight(92)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(6)

        title = QLabel(label)
        title.setObjectName("cardTitle")
        value_label = QLabel(value)
        value_label.setObjectName("cardValue")
        value_label.setWordWrap(True)
        value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        layout.addWidget(title)
        layout.addWidget(value_label)
