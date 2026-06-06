"""About and phase-boundary view."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from samaj import APP_VERSION
from samaj.config.defaults import SAFETY_BANNER_TEXT
from samaj.gui.theme import LOGO_PATH
from samaj.lab.lab_policy import SAFE_LAB_MANDATORY_STATEMENT
from samaj.tools.disclaimer import TOOL_CATALOG_DISCLAIMER_TEXT


class AboutView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        logo = QLabel()
        logo.setAlignment(Qt.AlignmentFlag.AlignLeft)
        logo.setFixedHeight(128)
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH))
            logo.setPixmap(
                pixmap.scaledToHeight(
                    120,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        layout.addWidget(logo)

        title = QLabel(f"Samaj {APP_VERSION}")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        banner = QLabel(SAFETY_BANNER_TEXT)
        banner.setObjectName("sectionTitle")
        banner.setWordWrap(True)
        layout.addWidget(banner)

        text = QLabel(
            "Samaj is for lawful, educational, defensive, authorized bug bounty, "
            "internal red-team, blue-team, research, and lab use only.\n\n"
            "This phase builds the knowledge base, OS support mapping, disclaimer "
            "acceptance, safe static lab foundation, proxy database foundation, and "
            "modern theme foundation only. Catalog tools are not executable.\n\n"
            f"{SAFE_LAB_MANDATORY_STATEMENT}\n\n"
            + TOOL_CATALOG_DISCLAIMER_TEXT
        )
        text.setObjectName("mutedText")
        text.setWordWrap(True)
        layout.addWidget(text)
        layout.addStretch(1)
