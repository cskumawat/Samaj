"""Main window for the Samaj GUI shell."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QListWidgetItem,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from samaj.config.settings import AppSettings
from samaj.core.audit import AuditLogger
from samaj.db.crud import SamajRepository
from samaj.db.database import DatabaseManager
from samaj.gui.about_view import AboutView
from samaj.gui.dashboard import DashboardView
from samaj.gui.logs_view import LogsView
from samaj.gui.placeholder import PlaceholderView
from samaj.gui.project_manager import ProjectManagerView
from samaj.gui.proxy_manager_view import ProxyManagerView
from samaj.gui.safe_lab_view import SafeLabView
from samaj.gui.settings_view import SettingsView
from samaj.gui.theme import samaj_stylesheet
from samaj.gui.tool_catalog_view import ToolCatalogDisclaimerDialog, ToolCatalogView
from samaj.gui.widgets.navigation_sidebar import NavigationSidebar
from samaj.gui.widgets.status_banner import PermanentSafetyBanner

NAVIGATION: tuple[tuple[str, str], ...] = (
    ("Dashboard", "Phase 1"),
    ("Projects", "Phase 2"),
    ("Scope Manager", "Phase 2"),
    ("Asset Inventory", "Phase 2"),
    ("Recon", "Phase 4"),
    ("OSINT", "Phase 5"),
    ("DNS", "Phase 4"),
    ("HTTP Probe", "Phase 4"),
    ("Screenshots", "Phase 7"),
    ("Technology Fingerprinting", "Phase 7"),
    ("Port Scan Orchestrator", "Phase 9"),
    ("Web Testing Checklist", "Phase 8"),
    ("API Testing Checklist", "Phase 8"),
    ("Cloud Review Checklist", "Phase 8"),
    ("Mobile Review Checklist", "Phase 8"),
    ("Code Review Checklist", "Phase 8"),
    ("Evidence Manager", "Phase 2"),
    ("Findings", "Phase 2"),
    ("Reports", "Phase 10"),
    ("Tool Catalog", "Phase 2 foundation"),
    ("Safe Analysis Lab", "Phase 2 foundation"),
    ("Proxy Database", "Phase 2 foundation"),
    ("Tool Registry", "Phase 9"),
    ("Plugin Manager", "Phase 12"),
    ("Logs and Audit Trail", "Phase 1"),
    ("Settings", "Phase 1"),
    ("Freeze / Release Manager", "Phase 13"),
    ("About Samaj", "Phase 2 foundation"),
)


class MainWindow(QMainWindow):
    def __init__(
        self,
        settings: AppSettings,
        audit_logger: AuditLogger,
        database_manager: DatabaseManager | None = None,
        settings_path: Path | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.settings = settings
        self.audit_logger = audit_logger
        self.database_manager = database_manager or DatabaseManager.from_settings(settings)
        self.database_manager.init()
        self.settings_path = settings_path
        self.pages: dict[str, QWidget] = {}
        self.tool_catalog_disclaimer_dialog: ToolCatalogDisclaimerDialog | None = None

        self.setWindowTitle("Samaj")
        self.resize(1180, 760)
        self.setMinimumSize(920, 620)

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.safety_banner = PermanentSafetyBanner(safe_mode=settings.safe_mode)
        root_layout.addWidget(self.safety_banner)

        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)

        self.sidebar = NavigationSidebar()
        self.sidebar.itemClicked.connect(self._on_sidebar_item_clicked)
        body_layout.addWidget(self.sidebar)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFrameShape(QFrame.Shape.VLine)
        body_layout.addWidget(divider)

        self.stack = QStackedWidget()
        body_layout.addWidget(self.stack, 1)

        root_layout.addWidget(body, 1)
        self.setCentralWidget(root)

        self._build_pages()
        self._apply_styles()
        self.navigate_to("Dashboard")

        self.audit_logger.log(
            event_type="gui_window_created",
            message="Main window created.",
            metadata={"navigation_count": len(NAVIGATION)},
        )
        QTimer.singleShot(0, self._show_first_run_tool_catalog_disclaimer)

    def _build_pages(self) -> None:
        for name, phase in NAVIGATION:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, name)
            self.sidebar.addItem(item)

            page: QWidget
            if name == "Dashboard":
                page = DashboardView(self.settings)
            elif name == "Projects":
                page = ProjectManagerView(
                    database_manager=self.database_manager,
                    audit_logger=self.audit_logger,
                )
            elif name == "Settings":
                page = SettingsView(
                    self.settings,
                    audit_logger=self.audit_logger,
                    settings_path=self.settings_path,
                )
                page.settings_saved.connect(self._on_settings_saved)
            elif name == "Logs and Audit Trail":
                page = LogsView(self.audit_logger)
            elif name == "Tool Catalog":
                page = ToolCatalogView(
                    database_manager=self.database_manager,
                    audit_logger=self.audit_logger,
                )
            elif name == "Safe Analysis Lab":
                page = SafeLabView(
                    settings=self.settings,
                    audit_logger=self.audit_logger,
                )
            elif name == "Proxy Database":
                page = ProxyManagerView(
                    database_manager=self.database_manager,
                    audit_logger=self.audit_logger,
                )
            elif name == "About Samaj":
                page = AboutView()
            else:
                page = PlaceholderView(name, phase)

            self.pages[name] = page
            self.stack.addWidget(page)

    def navigate_to(self, name: str) -> None:
        page = self.pages[name]
        self.stack.setCurrentWidget(page)

        matches = self.sidebar.findItems(name, Qt.MatchFlag.MatchExactly)
        if matches:
            self.sidebar.setCurrentItem(matches[0])

        if name == "Logs and Audit Trail" and hasattr(page, "reload"):
            page.reload()

        self.audit_logger.log(
            event_type="navigation",
            message=f"Navigated to {name}.",
            metadata={"view": name},
        )

    def _on_sidebar_item_clicked(self, item: QListWidgetItem) -> None:
        name = item.data(Qt.ItemDataRole.UserRole)
        self.navigate_to(str(name))

    def _on_settings_saved(self, settings: AppSettings) -> None:
        self.settings = settings
        self.safety_banner.update_for_safe_mode(settings.safe_mode)

    def _show_first_run_tool_catalog_disclaimer(self) -> None:
        with self.database_manager.session() as session:
            accepted = SamajRepository(session).has_accepted_tool_catalog_disclaimer()
        if accepted:
            return
        self.tool_catalog_disclaimer_dialog = ToolCatalogDisclaimerDialog(
            database_manager=self.database_manager,
            audit_logger=self.audit_logger,
            parent=self,
        )
        self.tool_catalog_disclaimer_dialog.open()

    def closeEvent(self, event) -> None:  # noqa: N802, ANN001
        self.audit_logger.log(event_type="app_close", message="Samaj GUI closing.")
        super().closeEvent(event)

    def _apply_styles(self) -> None:
        self.setStyleSheet(samaj_stylesheet())
