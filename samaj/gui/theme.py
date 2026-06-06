"""Samaj GUI theme foundation."""

from __future__ import annotations

from pathlib import Path

ASSET_DIR = Path(__file__).with_name("assets")
LOGO_PATH = ASSET_DIR / "logo.png"


def samaj_stylesheet() -> str:
    """Return the application stylesheet used by the Qt GUI."""

    return """
    QMainWindow, QWidget {
        background: #f5f7fb;
        color: #182230;
        font-family: Segoe UI, Arial, sans-serif;
        font-size: 13px;
    }
    QLabel#viewTitle {
        font-size: 24px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: 0px;
    }
    QLabel#sectionTitle {
        font-size: 16px;
        font-weight: 700;
        color: #0f172a;
        letter-spacing: 0px;
    }
    QLabel#mutedText {
        color: #526173;
        line-height: 150%;
    }
    QLabel#brandName {
        color: #ffffff;
        font-size: 20px;
        font-weight: 800;
        letter-spacing: 0px;
    }
    QLabel#brandTagline {
        color: #a7f3d0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0px;
    }
    QFrame#navigationSidebar {
        background: #08111f;
        border: none;
    }
    QListWidget#sidebarList {
        background: transparent;
        color: #d8e2f0;
        border: none;
        padding: 8px;
        outline: none;
    }
    QListWidget#sidebarList::item {
        padding: 9px 10px;
        min-height: 22px;
        border-radius: 5px;
    }
    QListWidget#sidebarList::item:selected {
        background: #1282d8;
        color: #ffffff;
    }
    QListWidget#sidebarList::item:hover {
        background: #12304f;
    }
    QFrame#divider {
        color: #d7dee8;
        background: #d7dee8;
        max-width: 1px;
    }
    QFrame#statusCard, QFrame#modernCard {
        background: #ffffff;
        border: 1px solid #d9e1ec;
        border-radius: 7px;
    }
    QLabel#cardTitle {
        color: #475569;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0px;
    }
    QLabel#cardValue {
        color: #0f172a;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 0px;
    }
    QPushButton {
        background: #1282d8;
        color: #ffffff;
        border: 1px solid #0f6db4;
        border-radius: 5px;
        padding: 7px 12px;
        font-weight: 700;
    }
    QPushButton:hover {
        background: #0f6db4;
    }
    QPushButton:disabled {
        background: #d5dde8;
        border: 1px solid #c8d2df;
        color: #667085;
    }
    QLineEdit, QComboBox, QTextEdit, QTableWidget {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 5px;
        padding: 6px;
        selection-background-color: #1282d8;
    }
    QHeaderView::section {
        background: #e8edf5;
        color: #253244;
        border: none;
        border-right: 1px solid #cbd5e1;
        padding: 6px;
        font-weight: 700;
    }
    QCheckBox:disabled {
        color: #374151;
    }
    """
