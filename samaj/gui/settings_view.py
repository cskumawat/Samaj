"""Settings view for Phase 1."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from samaj.config.settings import AppSettings, save_settings
from samaj.core.audit import AuditLogger


class SettingsView(QWidget):
    settings_saved = Signal(object)

    def __init__(
        self,
        settings: AppSettings,
        audit_logger: AuditLogger,
        settings_path: Path | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self.settings = settings
        self.audit_logger = audit_logger
        self.settings_path = settings_path

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        title = QLabel("Settings")
        title.setObjectName("viewTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(12)
        layout.addLayout(form)

        self.analyst_name_input = QLineEdit(settings.analyst_name)
        self.analyst_name_input.setPlaceholderText("Optional analyst display name")
        form.addRow("Analyst", self.analyst_name_input)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["system", "light", "dark"])
        self.theme_combo.setCurrentText(settings.theme)
        form.addRow("Theme", self.theme_combo)

        self.safe_mode_check = QCheckBox("Safe Mode ON")
        self.safe_mode_check.setChecked(settings.safe_mode)
        self.safe_mode_check.setEnabled(False)
        form.addRow("Safe Mode", self.safe_mode_check)

        self.anti_hallucination_check = QCheckBox("Anti-Hallucination Mode ON")
        self.anti_hallucination_check.setChecked(True)
        self.anti_hallucination_check.setEnabled(False)
        form.addRow("Anti-Hallucination", self.anti_hallucination_check)

        self.banner_check = QCheckBox("Permanent safety banner visible")
        self.banner_check.setChecked(True)
        self.banner_check.setEnabled(False)
        form.addRow("Safety Banner", self.banner_check)

        self.status_label = QLabel("")
        self.status_label.setObjectName("mutedText")

        button_row = QHBoxLayout()
        button_row.addStretch(1)
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save)
        button_row.addWidget(self.save_button)

        layout.addLayout(button_row)
        layout.addWidget(self.status_label)
        layout.addStretch(1)

    def save(self) -> None:
        self.settings = self.settings.model_copy(
            update={
                "analyst_name": self.analyst_name_input.text().strip(),
                "theme": self.theme_combo.currentText(),
                "safe_mode": self.settings.safe_mode,
                "anti_hallucination_mode": True,
                "show_safety_banner": True,
            }
        )
        path = save_settings(self.settings, self.settings_path)
        self.audit_logger.log(
            event_type="settings_saved",
            message="Settings saved from GUI.",
            metadata={
                "settings_path": str(path),
                "theme": self.settings.theme,
                "safe_mode": self.settings.safe_mode,
                "anti_hallucination_mode": self.settings.anti_hallucination_mode,
            },
        )
        self.status_label.setText(f"Saved to {path}")
        self.settings_saved.emit(self.settings)

