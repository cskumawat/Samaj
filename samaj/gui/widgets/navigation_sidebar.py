"""Logo-aware navigation sidebar."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from samaj.gui.theme import LOGO_PATH


class NavigationSidebar(QFrame):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("navigationSidebar")
        self.setFixedWidth(286)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 14, 12, 12)
        layout.setSpacing(10)

        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)

        logo = QLabel()
        logo.setFixedSize(48, 48)
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH))
            logo.setPixmap(
                pixmap.scaled(
                    48,
                    48,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        brand_row.addWidget(logo)

        brand_text = QVBoxLayout()
        brand_text.setSpacing(0)
        name = QLabel("Samaj")
        name.setObjectName("brandName")
        tagline = QLabel("Learn. Connect. Secure. Grow.")
        tagline.setObjectName("brandTagline")
        brand_text.addWidget(name)
        brand_text.addWidget(tagline)
        brand_row.addLayout(brand_text, 1)

        layout.addLayout(brand_row)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("sidebarList")
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout.addWidget(self.list_widget, 1)

        self.itemClicked = self.list_widget.itemClicked

    def addItem(self, item: QListWidgetItem) -> None:  # noqa: N802
        self.list_widget.addItem(item)

    def findItems(self, text: str, flags: Qt.MatchFlag) -> list[QListWidgetItem]:  # noqa: N802
        return self.list_widget.findItems(text, flags)

    def setCurrentItem(self, item: QListWidgetItem) -> None:  # noqa: N802
        self.list_widget.setCurrentItem(item)

    def currentItem(self) -> QListWidgetItem | None:  # noqa: N802
        return self.list_widget.currentItem()
