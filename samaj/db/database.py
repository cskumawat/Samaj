"""Database configuration and initialization for Phase 2."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, create_engine, event, inspect, text
from sqlalchemy.engine import Engine as EngineType
from sqlalchemy.orm import Session, sessionmaker

from samaj.config.settings import AppSettings
from samaj.db.models import Base


@dataclass(frozen=True)
class DatabaseConfig:
    sqlite_path: Path

    @property
    def url(self) -> str:
        return f"sqlite:///{self.sqlite_path.as_posix()}"


def default_database_config(data_dir: Path) -> DatabaseConfig:
    return DatabaseConfig(sqlite_path=Path(data_dir) / "samaj.sqlite3")


def database_config_from_settings(settings: AppSettings) -> DatabaseConfig:
    return default_database_config(settings.data_dir)


@event.listens_for(EngineType, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection: Any, connection_record: Any) -> None:
    del connection_record
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_engine_for_config(config: DatabaseConfig) -> Engine:
    config.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(config.url, future=True)


def create_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)


def init_database(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine)
    ensure_sqlite_schema(engine)


def ensure_sqlite_schema(engine: Engine) -> None:
    if engine.dialect.name != "sqlite":
        return

    table_columns: dict[str, dict[str, str]] = {
        "tool_catalog_entries": {
            "tool_name": "TEXT DEFAULT ''",
            "name": "TEXT DEFAULT ''",
            "category": "TEXT DEFAULT ''",
            "subcategory": "TEXT DEFAULT ''",
            "planned_phase": "VARCHAR(255) DEFAULT ''",
            "description": "TEXT DEFAULT ''",
            "catalog_status": "VARCHAR(255) DEFAULT 'knowledge-entry-only'",
            "source_note": "TEXT DEFAULT ''",
            "install_status": "VARCHAR(100) DEFAULT 'not_checked'",
            "support_status": "VARCHAR(255) DEFAULT 'not implemented unless adapter exists'",
            "safety_note": "TEXT DEFAULT 'Unknown / Not verified'",
            "license_note": "TEXT DEFAULT 'Unknown / Not verified'",
            "official_url": "VARCHAR(1000) DEFAULT ''",
            "install_notes": "TEXT DEFAULT 'Unknown / Not verified'",
            "user_notes": "TEXT DEFAULT ''",
            "ai_suggested": "VARCHAR(20) DEFAULT 'yes'",
            "verified_by_developer": "VARCHAR(20) DEFAULT 'no'",
            "documentation_url": "VARCHAR(1000) DEFAULT ''",
            "disclaimer_status": "VARCHAR(255) DEFAULT 'requires_user_acceptance'",
            "imported_from": "VARCHAR(255) DEFAULT 'user_pasted_tool_inventory'",
            "active_execution_supported": "BOOLEAN DEFAULT 0",
            "bundled_by_samaj": "BOOLEAN DEFAULT 0",
            "tested_by_samaj": "BOOLEAN DEFAULT 0",
            "recommended_by_samaj": "BOOLEAN DEFAULT 0",
            "windows_supported": "VARCHAR(20) DEFAULT 'unknown'",
            "kali_supported": "VARCHAR(20) DEFAULT 'unknown'",
            "linux_supported": "VARCHAR(20) DEFAULT 'unknown'",
            "mac_supported": "VARCHAR(20) DEFAULT 'unknown'",
            "install_method_windows": "TEXT DEFAULT 'Unknown / Not verified'",
            "install_method_kali": "TEXT DEFAULT 'Unknown / Not verified'",
            "install_method_linux": "TEXT DEFAULT 'Unknown / Not verified'",
            "license": "TEXT DEFAULT 'Unknown / Not verified'",
            "adapter_available": "VARCHAR(20) DEFAULT 'no'",
            "safe_mode_required": "VARCHAR(20) DEFAULT 'yes'",
            "scope_required": "VARCHAR(20) DEFAULT 'yes'",
            "requires_admin_or_root": "VARCHAR(20) DEFAULT 'unknown'",
            "requires_network": "VARCHAR(20) DEFAULT 'unknown'",
            "requires_api_key": "VARCHAR(20) DEFAULT 'unknown'",
            "usage_notes": "TEXT DEFAULT 'Knowledge entry only.'",
            "legal_notes": "TEXT DEFAULT 'Use only with lawful authorization.'",
        },
        "tool_catalog_disclaimer_acceptance": {
            "user_accepted_tool_disclaimer_version": "VARCHAR(100) DEFAULT '2026-06-06'",
        },
    }

    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    with engine.begin() as connection:
        for table_name, columns in table_columns.items():
            if table_name not in existing_tables:
                continue
            existing_columns = {
                column["name"] for column in inspector.get_columns(table_name)
            }
            for column_name, ddl in columns.items():
                if column_name not in existing_columns:
                    statement = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {ddl}"
                    connection.execute(text(statement))


class DatabaseManager:
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config
        self.engine = create_engine_for_config(config)
        self.session_factory = create_session_factory(self.engine)

    @classmethod
    def from_settings(cls, settings: AppSettings) -> DatabaseManager:
        return cls(database_config_from_settings(settings))

    def init(self) -> None:
        init_database(self.engine)

    def session(self) -> Session:
        return self.session_factory()
