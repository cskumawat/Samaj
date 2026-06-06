"""Tool Catalog / Knowledge Registry view."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from samaj.core.audit import AuditLogger
from samaj.db.crud import SamajRepository, ToolCatalogDisclaimerRequiredError
from samaj.db.database import DatabaseManager
from samaj.db.models import ToolCatalogEntryRecord
from samaj.tools.catalog import list_catalog_entries
from samaj.tools.disclaimer import TOOL_CATALOG_ACCEPTANCE_LABEL, TOOL_CATALOG_DISCLAIMER_TEXT


class ToolCatalogDisclaimerDialog(QDialog):
    def __init__(
        self,
        database_manager: DatabaseManager,
        audit_logger: AuditLogger,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.database_manager = database_manager
        self.audit_logger = audit_logger
        self.setWindowTitle("Tool Catalog Disclaimer")
        self.setMinimumSize(680, 520)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Tool Catalog / Knowledge Registry Disclaimer")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        text = QTextEdit()
        text.setReadOnly(True)
        text.setPlainText(TOOL_CATALOG_DISCLAIMER_TEXT)
        layout.addWidget(text, 1)

        self.acceptance_checkbox = QCheckBox(TOOL_CATALOG_ACCEPTANCE_LABEL)
        self.acceptance_checkbox.stateChanged.connect(self._sync_buttons)
        layout.addWidget(self.acceptance_checkbox)

        self.buttons = QDialogButtonBox()
        self.accept_button = self.buttons.addButton(
            "Accept",
            QDialogButtonBox.ButtonRole.AcceptRole,
        )
        self.cancel_button = self.buttons.addButton(
            "Not Now",
            QDialogButtonBox.ButtonRole.RejectRole,
        )
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.accept_disclaimer)
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.buttons)

    def _sync_buttons(self) -> None:
        self.accept_button.setEnabled(self.acceptance_checkbox.isChecked())

    def accept_disclaimer(self) -> None:
        if not self.acceptance_checkbox.isChecked():
            return
        with self.database_manager.session() as session:
            repository = SamajRepository(session)
            acceptance = repository.accept_tool_catalog_disclaimer(
                accepted=True,
                actor="gui_user",
                acceptance_text=TOOL_CATALOG_ACCEPTANCE_LABEL,
            )
        self.audit_logger.log(
            event_type="tool_catalog_disclaimer_accepted_gui",
            message="Tool Catalog disclaimer accepted in GUI.",
            metadata={
                "user_accepted_tool_disclaimer_at": (
                    acceptance.user_accepted_tool_disclaimer_at.isoformat()
                    if acceptance.user_accepted_tool_disclaimer_at
                    else ""
                )
            },
        )
        self.accept()


class ToolCatalogView(QWidget):
    def __init__(
        self,
        database_manager: DatabaseManager,
        audit_logger: AuditLogger,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.database_manager = database_manager
        self.audit_logger = audit_logger
        self.entries: list[ToolCatalogEntryRecord] = []
        self.visible_entries: list[ToolCatalogEntryRecord] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Tool Catalog / Knowledge Registry")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        self.disclaimer_status = QLabel("")
        self.disclaimer_status.setWordWrap(True)
        self.disclaimer_status.setObjectName("mutedText")
        layout.addWidget(self.disclaimer_status)

        self.disclaimer_text = QTextEdit()
        self.disclaimer_text.setReadOnly(True)
        self.disclaimer_text.setPlainText(TOOL_CATALOG_DISCLAIMER_TEXT)
        self.disclaimer_text.setFixedHeight(180)
        layout.addWidget(self.disclaimer_text)

        self.acceptance_checkbox = QCheckBox(TOOL_CATALOG_ACCEPTANCE_LABEL)
        self.acceptance_checkbox.stateChanged.connect(self._sync_accept_button)
        layout.addWidget(self.acceptance_checkbox)

        button_row = QHBoxLayout()
        self.accept_button = QPushButton("Accept Disclaimer")
        self.accept_button.setEnabled(False)
        self.accept_button.clicked.connect(self.accept_disclaimer)
        self.import_button = QPushButton("Import Catalog Intake")
        self.import_button.clicked.connect(self.import_catalog)
        self.reload_button = QPushButton("Reload Catalog")
        self.reload_button.clicked.connect(self.reload_catalog)
        self.view_details_button = QPushButton("View Selected Details")
        self.view_details_button.clicked.connect(self.view_selected_details)
        button_row.addWidget(self.accept_button)
        button_row.addWidget(self.import_button)
        button_row.addWidget(self.reload_button)
        button_row.addWidget(self.view_details_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        filter_row = QHBoxLayout()
        filter_label = QLabel("Filter")
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            [
                "All entries",
                "Knowledge-entry-only",
                "Windows support unknown",
                "Kali support unknown",
                "Linux support unknown",
                "Adapter available",
                "Developer verified",
                "Requires API key",
                "Requires admin/root",
            ]
        )
        self.filter_combo.currentTextChanged.connect(self._render_table)
        filter_row.addWidget(filter_label)
        filter_row.addWidget(self.filter_combo)
        filter_row.addStretch(1)
        layout.addLayout(filter_row)

        self.table = QTableWidget(0, 12)
        self.table.setHorizontalHeaderLabels(
            [
                "#",
                "Tool name",
                "Category",
                "Subcategory",
                "Catalog status",
                "Support status",
                "Windows",
                "Kali",
                "Linux",
                "AI-suggested",
                "Developer verified",
                "Adapter",
            ]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)

        self.detail_text = QTextEdit()
        self.detail_text.setReadOnly(True)
        self.detail_text.setFixedHeight(150)
        layout.addWidget(self.detail_text)

        self.refresh_gate_state()

    def _sync_accept_button(self) -> None:
        self.accept_button.setEnabled(self.acceptance_checkbox.isChecked())

    def has_acceptance(self) -> bool:
        with self.database_manager.session() as session:
            return SamajRepository(session).has_accepted_tool_catalog_disclaimer()

    def refresh_gate_state(self) -> None:
        accepted = self.has_acceptance()
        self.disclaimer_text.setVisible(not accepted)
        self.acceptance_checkbox.setVisible(not accepted)
        self.accept_button.setVisible(not accepted)
        self.import_button.setEnabled(accepted)
        self.reload_button.setEnabled(accepted)
        self.view_details_button.setEnabled(accepted)
        self.filter_combo.setEnabled(accepted)
        self.table.setVisible(accepted)
        self.detail_text.setVisible(accepted)
        self.disclaimer_status.setText(
            "Disclaimer accepted. Catalog entries are still neutral intake only."
            if accepted
            else (
                "Explicit checkbox acceptance is required before catalog import "
                "or tool detail viewing."
            )
        )
        if accepted:
            self.reload_catalog()

    def accept_disclaimer(self) -> None:
        if not self.acceptance_checkbox.isChecked():
            self.disclaimer_status.setText("Check the acceptance box before continuing.")
            return
        with self.database_manager.session() as session:
            SamajRepository(session).accept_tool_catalog_disclaimer(
                accepted=True,
                actor="gui_user",
                acceptance_text=TOOL_CATALOG_ACCEPTANCE_LABEL,
            )
        self.audit_logger.log(
            event_type="tool_catalog_disclaimer_accepted_gui",
            message="Tool Catalog disclaimer accepted from catalog view.",
        )
        self.refresh_gate_state()

    def import_catalog(self) -> None:
        try:
            entries = list_catalog_entries()
            with self.database_manager.session() as session:
                imported = SamajRepository(session).import_tool_catalog_entries(entries)
        except ToolCatalogDisclaimerRequiredError as exc:
            self.disclaimer_status.setText(str(exc))
            return
        self.audit_logger.log(
            event_type="tool_catalog_import_gui",
            message="Tool Catalog manifest imported from GUI.",
            metadata={"manifest_entries": len(entries), "new_records": imported},
        )
        self.disclaimer_status.setText(
            f"Imported {len(entries)} catalog entries; {imported} new records."
        )
        self.reload_catalog()

    def reload_catalog(self) -> None:
        try:
            with self.database_manager.session() as session:
                self.entries = SamajRepository(session).list_tool_catalog_entries()
        except ToolCatalogDisclaimerRequiredError as exc:
            self.disclaimer_status.setText(str(exc))
            return
        self.table.setRowCount(len(self.entries))
        self._render_table()

    def _render_table(self, selected_filter: str | None = None) -> None:
        selected_filter = selected_filter or self.filter_combo.currentText()
        self.visible_entries = [
            entry for entry in self.entries if self._entry_matches_filter(entry, selected_filter)
        ]
        self.table.setRowCount(len(self.visible_entries))
        for row, entry in enumerate(self.visible_entries):
            values = (
                str(entry.sequence),
                entry.tool_name,
                entry.category,
                entry.subcategory,
                entry.catalog_status,
                entry.support_status,
                entry.windows_supported,
                entry.kali_supported,
                entry.linux_supported,
                entry.ai_suggested,
                entry.verified_by_developer,
                entry.adapter_available,
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.ItemDataRole.UserRole, entry.id)
                self.table.setItem(row, column, item)
        self.table.resizeColumnsToContents()

    def _entry_matches_filter(self, entry: ToolCatalogEntryRecord, selected_filter: str) -> bool:
        if selected_filter == "Knowledge-entry-only":
            return entry.catalog_status == "knowledge-entry-only"
        if selected_filter == "Windows support unknown":
            return entry.windows_supported == "unknown"
        if selected_filter == "Kali support unknown":
            return entry.kali_supported == "unknown"
        if selected_filter == "Linux support unknown":
            return entry.linux_supported == "unknown"
        if selected_filter == "Adapter available":
            return entry.adapter_available == "yes"
        if selected_filter == "Developer verified":
            return entry.verified_by_developer == "yes"
        if selected_filter == "Requires API key":
            return entry.requires_api_key == "yes"
        if selected_filter == "Requires admin/root":
            return entry.requires_admin_or_root == "yes"
        return True

    def view_selected_details(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            self.detail_text.setPlainText("Select a catalog entry first.")
            return
        entry_id = selected[0].data(Qt.ItemDataRole.UserRole)
        try:
            with self.database_manager.session() as session:
                entry = SamajRepository(session).get_tool_catalog_entry(str(entry_id))
        except ToolCatalogDisclaimerRequiredError as exc:
            self.detail_text.setPlainText(str(exc))
            return
        self.detail_text.setPlainText(
            "\n".join(
                (
                    f"Tool name: {entry.tool_name}",
                    f"Category: {entry.category}",
                    f"Subcategory: {entry.subcategory}",
                    f"Description: {entry.description}",
                    f"Catalog status: {entry.catalog_status}",
                    f"Planned phase: {entry.planned_phase}",
                    f"Install status: {entry.install_status}",
                    f"Support status: {entry.support_status}",
                    f"Safety note: {entry.safety_note}",
                    f"License note: {entry.license_note}",
                    f"Official URL: {entry.official_url}",
                    f"Install notes: {entry.install_notes}",
                    f"User notes: {entry.user_notes}",
                    f"AI-suggested: {entry.ai_suggested}",
                    f"Verified by developer: {entry.verified_by_developer}",
                    f"Windows support: {entry.windows_supported}",
                    f"Kali support: {entry.kali_supported}",
                    f"Linux support: {entry.linux_supported}",
                    f"Adapter available: {entry.adapter_available}",
                    f"Disclaimer status: {entry.disclaimer_status}",
                    f"Source note: {entry.source_note}",
                    (
                        "Tool Catalog entry does not mean tool support, endorsement, "
                        "verification, safety, installation, execution, recommendation, "
                        "or permission to use."
                    ),
                )
            )
        )
