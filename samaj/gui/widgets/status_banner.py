"""Permanent status banner for safety context."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from samaj.config.defaults import SAFETY_BANNER_TEXT, UNSAFE_MODE_BANNER_TEXT


class PermanentSafetyBanner(QFrame):
    """Banner that stays visible in normal widget operations."""

    def __init__(self, safe_mode: bool = True, parent=None) -> None:
        super().__init__(parent)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.addWidget(self.label)
        self.setObjectName("safetyBanner")
        self.update_for_safe_mode(safe_mode)

    def update_for_safe_mode(self, safe_mode: bool) -> None:
        if safe_mode:
            self.label.setText(SAFETY_BANNER_TEXT)
            self.setStyleSheet(
                """
                QFrame#safetyBanner {
                    background: #0f5132;
                    border: 1px solid #198754;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                    font-weight: 700;
                    letter-spacing: 0px;
                }
                """
            )
        else:
            self.label.setText(UNSAFE_MODE_BANNER_TEXT)
            self.setStyleSheet(
                """
                QFrame#safetyBanner {
                    background: #842029;
                    border: 1px solid #dc3545;
                    color: #ffffff;
                }
                QLabel {
                    color: #ffffff;
                    font-weight: 800;
                    letter-spacing: 0px;
                }
                """
            )
        super().setVisible(True)

    def hide(self) -> None:  # noqa: D102
        super().setVisible(True)

    def setHidden(self, hidden: bool) -> None:  # noqa: N802, D102
        super().setVisible(True)

    def setVisible(self, visible: bool) -> None:  # noqa: N802, D102
        super().setVisible(True)

