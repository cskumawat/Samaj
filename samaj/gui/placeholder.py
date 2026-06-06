"""Placeholder views for modules planned after Phase 1."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from samaj.config.defaults import PLANNED_PHASE_NOTICE


class PlaceholderView(QWidget):
    def __init__(self, title: str, phase: str, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        heading = QLabel(title)
        heading.setObjectName("viewTitle")
        layout.addWidget(heading)

        phase_label = QLabel(f"{phase}: {PLANNED_PHASE_NOTICE}")
        phase_label.setObjectName("mutedText")
        phase_label.setWordWrap(True)
        layout.addWidget(phase_label)
        layout.addStretch(1)

