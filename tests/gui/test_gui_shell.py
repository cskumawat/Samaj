from __future__ import annotations

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")

from PySide6.QtWidgets import QApplication

from samaj.config.settings import AppSettings
from samaj.core.audit import AuditLogger
from samaj.db.database import DatabaseManager, default_database_config
from samaj.gui.main_window import MainWindow
from samaj.gui.tool_catalog_view import ToolCatalogView


@pytest.fixture
def qapp():
    app = QApplication.instance() or QApplication([])
    return app


def test_main_window_banner_cannot_be_hidden(qapp, tmp_path):  # noqa: ARG001
    settings = AppSettings(data_dir=tmp_path)
    audit = AuditLogger(tmp_path / "audit.jsonl")
    window = MainWindow(
        settings=settings,
        audit_logger=audit,
        settings_path=tmp_path / "settings.json",
    )
    window.show()
    qapp.processEvents()

    window.safety_banner.setVisible(False)
    window.safety_banner.hide()

    assert window.safety_banner.isVisible() is True
    assert "ANTI-HALLUCINATION: ON" in window.safety_banner.label.text()
    assert "SCOPE REQUIRED" in window.safety_banner.label.text()
    window.close()


def test_main_window_navigation_works(qapp, tmp_path):  # noqa: ARG001
    settings = AppSettings(data_dir=tmp_path)
    audit = AuditLogger(tmp_path / "audit.jsonl")
    window = MainWindow(
        settings=settings,
        audit_logger=audit,
        settings_path=tmp_path / "settings.json",
    )

    window.navigate_to("Settings")

    assert window.stack.currentWidget() is window.pages["Settings"]
    assert window.sidebar.currentItem().text() == "Settings"
    window.close()


def test_tool_catalog_view_requires_checkbox_acceptance(qapp, tmp_path):  # noqa: ARG001
    manager = DatabaseManager(default_database_config(tmp_path))
    manager.init()
    audit = AuditLogger(tmp_path / "audit.jsonl")
    view = ToolCatalogView(database_manager=manager, audit_logger=audit)

    assert view.import_button.isEnabled() is False

    view.acceptance_checkbox.setChecked(True)
    view.accept_disclaimer()
    view.import_catalog()

    assert view.import_button.isEnabled() is True
    assert view.table.rowCount() == 1620
