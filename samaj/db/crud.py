"""CRUD service helpers for Phase 2 database entities."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from samaj.core.anti_hallucination import VerificationStatus
from samaj.db.models import (
    Asset,
    AuditRecord,
    Evidence,
    EvidenceType,
    Finding,
    Project,
    ProjectState,
    ProxyRecord,
    ScopeItem,
    Severity,
    ToolCatalogDisclaimerAcceptance,
    ToolCatalogEntryRecord,
    utc_now,
)
from samaj.tools.catalog import ToolCatalogEntry

TOOL_CATALOG_DISCLAIMER_VERSION = "2026-06-06"


class ToolCatalogDisclaimerRequiredError(PermissionError):
    pass


class RecordNotFoundError(LookupError):
    pass


PROJECT_FIELDS = {
    "name",
    "client_organization",
    "program_url",
    "authorization_notes",
    "start_date",
    "end_date",
    "scope_summary",
    "out_of_scope",
    "rate_limits",
    "allowed_test_types",
    "disallowed_test_types",
    "contacts",
    "data_retention_notes",
    "legal_notes",
    "report_status",
    "freeze_status",
    "version",
    "state",
}


class SamajRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_project(self, name: str, **fields: Any) -> Project:
        project = Project(name=name.strip(), **_filter_fields(fields, PROJECT_FIELDS))
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        self.create_audit_record(
            event_type="project_created",
            message=f"Project created: {project.name}",
            project_id=project.id,
        )
        return project

    def get_project(self, project_id: str) -> Project:
        project = self.session.get(Project, project_id)
        if project is None:
            raise RecordNotFoundError(f"Project not found: {project_id}")
        return project

    def list_projects(self, include_archived: bool = False) -> list[Project]:
        statement = select(Project).order_by(Project.updated_at.desc())
        if not include_archived:
            statement = statement.where(Project.state != ProjectState.ARCHIVED.value)
        return list(self.session.scalars(statement).all())

    def update_project(self, project_id: str, **fields: Any) -> Project:
        project = self.get_project(project_id)
        for key, value in _filter_fields(fields, PROJECT_FIELDS).items():
            setattr(project, key, value)
        project.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(project)
        self.create_audit_record(
            event_type="project_updated",
            message=f"Project updated: {project.name}",
            project_id=project.id,
        )
        return project

    def archive_project(self, project_id: str) -> Project:
        return self.update_project(project_id, state=ProjectState.ARCHIVED.value)

    def delete_project(self, project_id: str) -> None:
        project = self.get_project(project_id)
        self.session.delete(project)
        self.session.commit()
        self.create_audit_record(
            event_type="project_deleted",
            message=f"Project deleted: {project.name}",
        )

    def create_scope_item(
        self,
        project_id: str,
        target_type: str,
        target_value: str,
        *,
        in_scope: bool = True,
        authorized_test_types: Iterable[str] | None = None,
        rate_limit_rule: str = "",
        testing_window: str = "",
        notes: str = "",
    ) -> ScopeItem:
        scope_item = ScopeItem(
            project_id=project_id,
            target_type=target_type,
            target_value=target_value,
            in_scope=in_scope,
            authorized_test_types=list(authorized_test_types or []),
            rate_limit_rule=rate_limit_rule,
            testing_window=testing_window,
            notes=notes,
        )
        self.session.add(scope_item)
        self.session.commit()
        self.session.refresh(scope_item)
        self.create_audit_record(
            event_type="scope_item_created",
            message=f"Scope item created: {target_value}",
            project_id=project_id,
        )
        return scope_item

    def list_scope_items(self, project_id: str) -> list[ScopeItem]:
        statement = (
            select(ScopeItem)
            .where(ScopeItem.project_id == project_id)
            .order_by(ScopeItem.created_at.asc())
        )
        return list(self.session.scalars(statement).all())

    def create_asset(
        self,
        project_id: str,
        asset_type: str,
        value: str,
        **fields: Any,
    ) -> Asset:
        existing = self.session.scalar(
            select(Asset).where(
                Asset.project_id == project_id,
                Asset.asset_type == asset_type,
                Asset.value == value,
            )
        )
        if existing is not None:
            existing.last_seen = utc_now()
            for key, item in _filter_fields(fields, ASSET_FIELDS).items():
                setattr(existing, key, item)
            self.session.commit()
            self.session.refresh(existing)
            return existing

        asset = Asset(
            project_id=project_id,
            asset_type=asset_type,
            value=value,
            **_filter_fields(fields, ASSET_FIELDS),
        )
        self.session.add(asset)
        self.session.commit()
        self.session.refresh(asset)
        self.create_audit_record(
            event_type="asset_created",
            message=f"Asset created: {value}",
            project_id=project_id,
        )
        return asset

    def list_assets(self, project_id: str) -> list[Asset]:
        statement = (
            select(Asset)
            .where(Asset.project_id == project_id)
            .order_by(Asset.last_seen.desc())
        )
        return list(self.session.scalars(statement).all())

    def create_finding(
        self,
        project_id: str,
        title: str,
        *,
        asset_id: str | None = None,
        severity: Severity = Severity.NEEDS_REVIEW,
        verification_status: VerificationStatus = VerificationStatus.UNVERIFIED,
        **fields: Any,
    ) -> Finding:
        finding = Finding(
            project_id=project_id,
            asset_id=asset_id,
            title=title,
            severity=severity.value,
            verification_status=verification_status.value,
            **_filter_fields(fields, FINDING_FIELDS),
        )
        self.session.add(finding)
        self.session.commit()
        self.session.refresh(finding)
        self.create_audit_record(
            event_type="finding_created",
            message=f"Finding created: {title}",
            project_id=project_id,
        )
        return finding

    def list_findings(self, project_id: str) -> list[Finding]:
        statement = (
            select(Finding)
            .where(Finding.project_id == project_id)
            .order_by(Finding.updated_at.desc())
        )
        return list(self.session.scalars(statement).all())

    def create_evidence(
        self,
        project_id: str,
        evidence_type: EvidenceType = EvidenceType.MANUAL_NOTE,
        *,
        asset_id: str | None = None,
        finding_id: str | None = None,
        **fields: Any,
    ) -> Evidence:
        evidence = Evidence(
            project_id=project_id,
            asset_id=asset_id,
            finding_id=finding_id,
            evidence_type=evidence_type.value,
            **_filter_fields(fields, EVIDENCE_FIELDS),
        )
        self.session.add(evidence)
        self.session.commit()
        self.session.refresh(evidence)
        self.create_audit_record(
            event_type="evidence_created",
            message=f"Evidence created: {evidence.evidence_type}",
            project_id=project_id,
        )
        return evidence

    def list_evidence(self, project_id: str) -> list[Evidence]:
        statement = (
            select(Evidence)
            .where(Evidence.project_id == project_id)
            .order_by(Evidence.timestamp.desc())
        )
        return list(self.session.scalars(statement).all())

    def create_audit_record(
        self,
        event_type: str,
        message: str,
        *,
        project_id: str | None = None,
        actor: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> AuditRecord:
        record = AuditRecord(
            project_id=project_id,
            event_type=event_type,
            message=message,
            actor=actor,
            metadata_json=metadata or {},
        )
        self.session.add(record)
        self.session.commit()
        self.session.refresh(record)
        return record

    def list_audit_records(self, project_id: str | None = None) -> list[AuditRecord]:
        statement = select(AuditRecord).order_by(AuditRecord.timestamp.desc())
        if project_id is not None:
            statement = statement.where(AuditRecord.project_id == project_id)
        return list(self.session.scalars(statement).all())

    def get_tool_catalog_acceptance(self) -> ToolCatalogDisclaimerAcceptance | None:
        return self.session.get(ToolCatalogDisclaimerAcceptance, "global")

    def has_accepted_tool_catalog_disclaimer(self) -> bool:
        acceptance = self.get_tool_catalog_acceptance()
        return bool(acceptance and acceptance.user_accepted_tool_disclaimer_at)

    def accept_tool_catalog_disclaimer(
        self,
        *,
        accepted: bool,
        actor: str = "",
        acceptance_text: str = "",
    ) -> ToolCatalogDisclaimerAcceptance:
        if not accepted:
            raise ToolCatalogDisclaimerRequiredError(
                "Explicit checkbox acceptance is required for the Tool Catalog disclaimer."
            )
        acceptance = self.get_tool_catalog_acceptance()
        if acceptance is None:
            acceptance = ToolCatalogDisclaimerAcceptance(id="global")
            self.session.add(acceptance)
        acceptance.user_accepted_tool_disclaimer_at = utc_now()
        acceptance.user_accepted_tool_disclaimer_version = TOOL_CATALOG_DISCLAIMER_VERSION
        acceptance.actor = actor
        acceptance.acceptance_text = acceptance_text
        acceptance.updated_at = utc_now()
        self.session.commit()
        self.session.refresh(acceptance)
        self.create_audit_record(
            event_type="tool_catalog_disclaimer_accepted",
            message="Tool Catalog disclaimer accepted.",
            actor=actor,
            metadata={"disclaimer_version": TOOL_CATALOG_DISCLAIMER_VERSION},
        )
        return acceptance

    def require_tool_catalog_disclaimer_accepted(self) -> None:
        if not self.has_accepted_tool_catalog_disclaimer():
            raise ToolCatalogDisclaimerRequiredError(
                "Tool Catalog disclaimer acceptance is required before import or detail viewing."
            )

    def import_tool_catalog_entries(self, entries: list[ToolCatalogEntry]) -> int:
        self.require_tool_catalog_disclaimer_accepted()
        imported = 0
        for entry in entries:
            record = self.session.scalar(
                select(ToolCatalogEntryRecord).where(
                    ToolCatalogEntryRecord.sequence == entry.sequence
                )
            )
            if record is None:
                record = ToolCatalogEntryRecord(sequence=entry.sequence)
                self.session.add(record)
                imported += 1
            record.tool_name = entry.tool_name
            record.name = entry.name
            record.category = entry.category
            record.subcategory = entry.subcategory
            record.planned_phase = entry.planned_phase
            record.description = entry.description
            record.catalog_status = entry.catalog_status
            record.source_note = entry.source_note
            record.install_status = entry.install_status
            record.support_status = entry.support_status
            record.safety_note = entry.safety_note
            record.license_note = entry.license_note
            record.official_url = entry.official_url
            record.install_notes = entry.install_notes
            record.user_notes = entry.user_notes
            record.ai_suggested = entry.ai_suggested
            record.verified_by_developer = entry.verified_by_developer
            record.documentation_url = entry.documentation_url
            record.disclaimer_status = entry.disclaimer_status
            record.imported_from = entry.imported_from
            record.active_execution_supported = entry.active_execution_supported
            record.bundled_by_samaj = entry.bundled_by_samaj
            record.tested_by_samaj = entry.tested_by_samaj
            record.recommended_by_samaj = entry.recommended_by_samaj
            record.windows_supported = entry.windows_supported
            record.kali_supported = entry.kali_supported
            record.linux_supported = entry.linux_supported
            record.mac_supported = entry.mac_supported
            record.install_method_windows = entry.install_method_windows
            record.install_method_kali = entry.install_method_kali
            record.install_method_linux = entry.install_method_linux
            record.license = entry.license
            record.adapter_available = entry.adapter_available
            record.safe_mode_required = entry.safe_mode_required
            record.scope_required = entry.scope_required
            record.requires_admin_or_root = entry.requires_admin_or_root
            record.requires_network = entry.requires_network
            record.requires_api_key = entry.requires_api_key
            record.usage_notes = entry.usage_notes
            record.legal_notes = entry.legal_notes
            record.updated_at = utc_now()

        self.session.commit()
        self.create_audit_record(
            event_type="tool_catalog_imported",
            message="Tool Catalog entries imported as neutral knowledge registry records.",
            metadata={"entry_count": len(entries), "new_records": imported},
        )
        return imported

    def list_tool_catalog_entries(self) -> list[ToolCatalogEntryRecord]:
        self.require_tool_catalog_disclaimer_accepted()
        statement = select(ToolCatalogEntryRecord).order_by(ToolCatalogEntryRecord.sequence.asc())
        return list(self.session.scalars(statement).all())

    def get_tool_catalog_entry(self, entry_id: str) -> ToolCatalogEntryRecord:
        self.require_tool_catalog_disclaimer_accepted()
        entry = self.session.get(ToolCatalogEntryRecord, entry_id)
        if entry is None:
            raise RecordNotFoundError(f"Tool catalog entry not found: {entry_id}")
        return entry

    def upsert_proxy(
        self,
        *,
        ip: str,
        port: int,
        proxy_type: str = "unknown",
        source: str = "manual",
        country: str = "",
        asn: str = "",
        notes: str = "",
        legal_status_note: str = "",
        user_added: bool = True,
    ) -> ProxyRecord:
        record = self.session.scalar(
            select(ProxyRecord).where(
                ProxyRecord.ip == ip,
                ProxyRecord.port == port,
                ProxyRecord.type == proxy_type,
            )
        )
        if record is None:
            record = ProxyRecord(ip=ip, port=port, type=proxy_type)
            self.session.add(record)
        record.source = source
        record.country = country
        record.asn = asn
        record.notes = notes
        if legal_status_note:
            record.legal_status_note = legal_status_note
        record.user_added = user_added
        self.session.commit()
        self.session.refresh(record)
        self.create_audit_record(
            event_type="proxy_record_upserted",
            message=f"Proxy record stored: {ip}:{port}",
            metadata={"proxy_type": proxy_type, "source": source},
        )
        return record

    def list_proxies(self) -> list[ProxyRecord]:
        statement = select(ProxyRecord).order_by(ProxyRecord.first_seen.desc())
        return list(self.session.scalars(statement).all())


ASSET_FIELDS = {
    "asn",
    "port",
    "service",
    "technology",
    "status_code",
    "title",
    "screenshot_path",
    "tls_info",
    "waf_cdn_info",
    "source",
    "confidence",
    "scope_status",
    "status",
    "notes",
}

FINDING_FIELDS = {
    "cvss_score",
    "cwe",
    "owasp_category",
    "url",
    "parameter",
    "description",
    "impact",
    "reproduction_steps",
    "remediation",
    "references",
    "confidence",
    "false_positive_notes",
    "assigned_analyst",
    "report_inclusion_status",
}

EVIDENCE_FIELDS = {
    "timestamp",
    "source",
    "tool",
    "command",
    "raw_output",
    "analyst_note",
    "file_path",
    "file_hash_sha256",
    "immutable_after_freeze",
}


def _filter_fields(fields: dict[str, Any], allowed: set[str]) -> dict[str, Any]:
    return {key: value for key, value in fields.items() if key in allowed}
