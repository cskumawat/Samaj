"""Top-level application helpers."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

from samaj import APP_NAME, APP_VERSION
from samaj.config.settings import ensure_runtime_dirs, load_settings
from samaj.core.audit import AuditLogger
from samaj.db.database import DatabaseManager


def is_pyside6_available() -> bool:
    return importlib.util.find_spec("PySide6") is not None


def run_doctor(settings_path: Path | None = None) -> int:
    settings = load_settings(settings_path)
    ensure_runtime_dirs(settings)
    assert settings.audit_log_path is not None
    audit = AuditLogger(settings.audit_log_path)
    database = DatabaseManager.from_settings(settings)
    database.init()
    audit.log(
        event_type="doctor_ran",
        message="Samaj doctor completed.",
        metadata={
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
            "safe_mode": settings.safe_mode,
            "anti_hallucination_mode": settings.anti_hallucination_mode,
            "pyside6_available": is_pyside6_available(),
            "database": str(database.config.sqlite_path),
        },
    )

    print(f"{APP_NAME} {APP_VERSION}")
    print(f"Safe Mode: {settings.safe_mode}")
    print(f"Anti-Hallucination Mode: {settings.anti_hallucination_mode}")
    print(f"Safety banner visible: {settings.show_safety_banner}")
    print(f"Data directory: {settings.data_dir}")
    print(f"Audit log: {settings.audit_log_path}")
    print(f"Database: {database.config.sqlite_path}")
    print(f"PySide6 available: {is_pyside6_available()}")
    return 0


def run_gui(settings_path: Path | None = None) -> int:
    if not is_pyside6_available():
        print(
            "PySide6 is not installed. Install Phase 1 dependencies with "
            "`python -m pip install -r requirements-dev.txt`.",
            file=sys.stderr,
        )
        return 2

    from PySide6.QtWidgets import QApplication

    from samaj.gui.main_window import MainWindow

    settings = load_settings(settings_path)
    ensure_runtime_dirs(settings)
    assert settings.audit_log_path is not None
    audit = AuditLogger(settings.audit_log_path)
    database = DatabaseManager.from_settings(settings)
    database.init()
    audit.log(
        event_type="app_start",
        message="Samaj GUI starting.",
        metadata={
            "safe_mode": settings.safe_mode,
            "anti_hallucination_mode": settings.anti_hallucination_mode,
            "database": str(database.config.sqlite_path),
        },
    )

    qt_app = QApplication.instance() or QApplication(sys.argv)
    qt_app.setApplicationName(APP_NAME)
    qt_app.setApplicationVersion(APP_VERSION)

    window = MainWindow(
        settings=settings,
        audit_logger=audit,
        database_manager=database,
        settings_path=settings_path,
    )
    window.show()
    return int(qt_app.exec())
