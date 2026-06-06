"""Proxy database foundation view."""

from __future__ import annotations

from PySide6.QtWidgets import (
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
from samaj.db.crud import SamajRepository
from samaj.db.database import DatabaseManager
from samaj.proxy.proxy_db import import_proxy_lines
from samaj.proxy.proxy_policy import PROXY_MANDATORY_STATEMENT


class ProxyManagerView(QWidget):
    def __init__(
        self,
        database_manager: DatabaseManager,
        audit_logger: AuditLogger,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.database_manager = database_manager
        self.audit_logger = audit_logger

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        title = QLabel("Proxy Database")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        notice = QLabel(PROXY_MANDATORY_STATEMENT)
        notice.setObjectName("mutedText")
        notice.setWordWrap(True)
        layout.addWidget(notice)

        self.input = QTextEdit()
        self.input.setPlaceholderText(
            "Paste proxy endpoints, one per line: host:port or type://host:port"
        )
        self.input.setFixedHeight(110)
        layout.addWidget(self.input)

        button_row = QHBoxLayout()
        import_button = QPushButton("Import to Database")
        import_button.clicked.connect(self.import_proxies)
        reload_button = QPushButton("Reload")
        reload_button.clicked.connect(self.reload_proxies)
        button_row.addWidget(import_button)
        button_row.addWidget(reload_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self.status = QLabel(
            "Live proxy testing and chain execution are not implemented in this phase."
        )
        self.status.setObjectName("mutedText")
        self.status.setWordWrap(True)
        layout.addWidget(self.status)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(
            ["IP / Host", "Port", "Type", "Status", "Source", "Legal Note", "Live Test"]
        )
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        layout.addWidget(self.table, 1)
        self.reload_proxies()

    def import_proxies(self) -> None:
        lines = self.input.toPlainText().splitlines()
        with self.database_manager.session() as session:
            records = import_proxy_lines(session, lines, source="gui")
        self.audit_logger.log(
            event_type="proxy_records_imported_gui",
            message="Proxy records imported to local database without live testing.",
            metadata={"record_count": len(records), "live_testing": False},
        )
        self.status.setText(
            f"Imported or updated {len(records)} proxy records. Live testing: not run."
        )
        self.reload_proxies()

    def reload_proxies(self) -> None:
        with self.database_manager.session() as session:
            proxy_records = SamajRepository(session).list_proxies()

        self.table.setRowCount(len(proxy_records))
        for row, record in enumerate(proxy_records):
            values = (
                record.ip,
                str(record.port),
                record.type,
                record.status,
                record.source,
                record.legal_status_note,
                "Not implemented",
            )
            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))
        self.table.resizeColumnsToContents()
