"""Project manager view for Phase 2."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
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
from samaj.db.models import Project, ProjectState


class ProjectManagerView(QWidget):
    def __init__(
        self,
        database_manager: DatabaseManager,
        audit_logger: AuditLogger,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.database_manager = database_manager
        self.audit_logger = audit_logger
        self.selected_project_id: str | None = None
        self.projects: list[Project] = []

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Projects")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        layout.addLayout(form)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Required project name")
        form.addRow("Project Name", self.name_input)

        self.client_input = QLineEdit()
        self.client_input.setPlaceholderText("Client or organization")
        form.addRow("Client", self.client_input)

        self.program_url_input = QLineEdit()
        self.program_url_input.setPlaceholderText("Program URL")
        form.addRow("Program URL", self.program_url_input)

        self.authorization_notes_input = QTextEdit()
        self.authorization_notes_input.setPlaceholderText("Written authorization notes")
        self.authorization_notes_input.setFixedHeight(78)
        form.addRow("Authorization", self.authorization_notes_input)

        self.scope_summary_input = QTextEdit()
        self.scope_summary_input.setPlaceholderText("High-level scope summary")
        self.scope_summary_input.setFixedHeight(70)
        form.addRow("Scope Summary", self.scope_summary_input)

        self.rate_limits_input = QLineEdit()
        self.rate_limits_input.setPlaceholderText("Example: 30 requests per minute")
        form.addRow("Rate Limits", self.rate_limits_input)

        self.state_combo = QComboBox()
        self.state_combo.addItems([state.value for state in ProjectState])
        form.addRow("State", self.state_combo)

        button_row = QHBoxLayout()
        self.new_button = QPushButton("New")
        self.new_button.clicked.connect(self.clear_form)
        self.save_button = QPushButton("Save Project")
        self.save_button.clicked.connect(self.save_project)
        self.archive_button = QPushButton("Archive")
        self.archive_button.clicked.connect(self.archive_project)
        button_row.addWidget(self.new_button)
        button_row.addWidget(self.save_button)
        button_row.addWidget(self.archive_button)
        button_row.addStretch(1)
        layout.addLayout(button_row)

        self.status_label = QLabel("")
        self.status_label.setObjectName("mutedText")
        layout.addWidget(self.status_label)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Name", "Client", "State", "Version", "Updated"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self.load_selected_project)
        layout.addWidget(self.table, 1)

        self.reload_projects()

    def repository(self) -> SamajRepository:
        return SamajRepository(self.database_manager.session())

    def clear_form(self) -> None:
        self.selected_project_id = None
        self.name_input.clear()
        self.client_input.clear()
        self.program_url_input.clear()
        self.authorization_notes_input.clear()
        self.scope_summary_input.clear()
        self.rate_limits_input.clear()
        self.state_combo.setCurrentText(ProjectState.DRAFT.value)
        self.status_label.setText("Ready for a new project.")

    def save_project(self) -> None:
        name = self.name_input.text().strip()
        if not name:
            self.status_label.setText("Project name is required.")
            return

        with self.database_manager.session() as session:
            repository = SamajRepository(session)
            fields = {
                "client_organization": self.client_input.text().strip(),
                "program_url": self.program_url_input.text().strip(),
                "authorization_notes": self.authorization_notes_input.toPlainText().strip(),
                "scope_summary": self.scope_summary_input.toPlainText().strip(),
                "rate_limits": self.rate_limits_input.text().strip(),
                "state": self.state_combo.currentText(),
            }
            if self.selected_project_id:
                project = repository.update_project(self.selected_project_id, name=name, **fields)
                message = f"Updated project: {project.name}"
            else:
                project = repository.create_project(name, **fields)
                self.selected_project_id = project.id
                message = f"Created project: {project.name}"

        self.audit_logger.log(
            event_type="project_manager_save",
            message=message,
            metadata={"project_id": self.selected_project_id},
        )
        self.status_label.setText(message)
        self.reload_projects(select_project_id=self.selected_project_id)

    def archive_project(self) -> None:
        if not self.selected_project_id:
            self.status_label.setText("Select a project to archive.")
            return
        with self.database_manager.session() as session:
            repository = SamajRepository(session)
            project = repository.archive_project(self.selected_project_id)

        self.audit_logger.log(
            event_type="project_manager_archive",
            message=f"Archived project: {project.name}",
            metadata={"project_id": project.id},
        )
        self.status_label.setText(f"Archived project: {project.name}")
        self.selected_project_id = None
        self.clear_form()
        self.reload_projects()

    def reload_projects(self, select_project_id: str | None = None) -> None:
        with self.database_manager.session() as session:
            self.projects = SamajRepository(session).list_projects()

        self.table.setRowCount(len(self.projects))
        selected_row = -1
        for row, project in enumerate(self.projects):
            if project.id == select_project_id:
                selected_row = row
            values = (
                project.name,
                project.client_organization,
                project.state,
                project.version,
                project.updated_at.isoformat(timespec="seconds"),
            )
            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setData(Qt.ItemDataRole.UserRole, project.id)
                self.table.setItem(row, column, item)

        self.table.resizeColumnsToContents()
        if selected_row >= 0:
            self.table.selectRow(selected_row)

    def load_selected_project(self) -> None:
        selected = self.table.selectedItems()
        if not selected:
            return
        project_id = selected[0].data(Qt.ItemDataRole.UserRole)
        project = next((item for item in self.projects if item.id == project_id), None)
        if project is None:
            return

        self.selected_project_id = project.id
        self.name_input.setText(project.name)
        self.client_input.setText(project.client_organization)
        self.program_url_input.setText(project.program_url)
        self.authorization_notes_input.setPlainText(project.authorization_notes)
        self.scope_summary_input.setPlainText(project.scope_summary)
        self.rate_limits_input.setText(project.rate_limits)
        self.state_combo.setCurrentText(project.state)
        self.status_label.setText(f"Selected project: {project.name}")
