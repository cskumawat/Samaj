"""SQLAlchemy models for the Phase 2 persistence layer."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
from enum import StrEnum
from typing import Any
from uuid import uuid4

from sqlalchemy import (
    JSON,
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from samaj.core.anti_hallucination import VerificationStatus
from samaj.core.audit import AuditEvent


def new_id() -> str:
    return str(uuid4())


def utc_now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


class ProjectState(StrEnum):
    DRAFT = "Draft"
    SCOPE_DEFINED = "Scope Defined"
    RECON_STARTED = "Recon Started"
    TESTING_STARTED = "Testing Started"
    FINDINGS_REVIEW = "Findings Review"
    REPORT_DRAFT = "Report Draft"
    FINAL_REPORT = "Final Report"
    FROZEN = "Frozen"
    ARCHIVED = "Archived"


class AssetStatus(StrEnum):
    NEW = "New"
    VALIDATED = "Validated"
    OUT_OF_SCOPE = "Out of Scope"
    DUPLICATE = "Duplicate"
    DEAD = "Dead"
    INTERESTING = "Interesting"
    NEEDS_REVIEW = "Needs Review"


class Severity(StrEnum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    INFORMATIONAL = "Informational"
    NEEDS_REVIEW = "Needs Review"


class ScopeTargetType(StrEnum):
    DOMAIN = "domain"
    SUBDOMAIN = "subdomain"
    IP_RANGE = "ip_range"
    URL = "url"
    API = "api"
    MOBILE_APP = "mobile_app"
    CLOUD_ACCOUNT = "cloud_account"
    GITHUB_REPOSITORY = "github_repository"
    EXCLUDED_ASSET = "excluded_asset"
    EXCLUDED_PATH = "excluded_path"
    EXCLUDED_PARAMETER = "excluded_parameter"


class EvidenceType(StrEnum):
    SCREENSHOT = "screenshot"
    HTTP_REQUEST = "http_request"
    HTTP_RESPONSE = "http_response"
    TOOL_OUTPUT = "tool_output"
    MANUAL_NOTE = "manual_note"
    CODE_SNIPPET = "code_snippet"
    LOG_FILE = "log_file"
    VIDEO_REFERENCE = "video_reference"
    REPRODUCTION_STEPS = "reproduction_steps"
    IMPACT_EXPLANATION = "impact_explanation"
    REMEDIATION_REFERENCE = "remediation_reference"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    client_organization: Mapped[str] = mapped_column(String(255), default="")
    program_url: Mapped[str] = mapped_column(String(1000), default="")
    authorization_notes: Mapped[str] = mapped_column(Text, default="")
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    scope_summary: Mapped[str] = mapped_column(Text, default="")
    out_of_scope: Mapped[str] = mapped_column(Text, default="")
    rate_limits: Mapped[str] = mapped_column(Text, default="")
    allowed_test_types: Mapped[str] = mapped_column(Text, default="")
    disallowed_test_types: Mapped[str] = mapped_column(Text, default="")
    contacts: Mapped[str] = mapped_column(Text, default="")
    data_retention_notes: Mapped[str] = mapped_column(Text, default="")
    legal_notes: Mapped[str] = mapped_column(Text, default="")
    report_status: Mapped[str] = mapped_column(String(100), default="Draft")
    freeze_status: Mapped[str] = mapped_column(String(100), default="Not Frozen")
    version: Mapped[str] = mapped_column(String(50), default="0.1.0")
    state: Mapped[str] = mapped_column(String(50), default=ProjectState.DRAFT.value, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    scope_items: Mapped[list[ScopeItem]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    assets: Mapped[list[Asset]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    findings: Mapped[list[Finding]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    evidence_items: Mapped[list[Evidence]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )
    audit_records: Mapped[list[AuditRecord]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ScopeItem(Base):
    __tablename__ = "scope_items"
    __table_args__ = (
        UniqueConstraint("project_id", "target_type", "target_value", name="uq_scope_target"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    target_type: Mapped[str] = mapped_column(String(100), default=ScopeTargetType.DOMAIN.value)
    target_value: Mapped[str] = mapped_column(String(1000), nullable=False)
    in_scope: Mapped[bool] = mapped_column(Boolean, default=True)
    authorized_test_types: Mapped[list[str]] = mapped_column(JSON, default=list)
    rate_limit_rule: Mapped[str] = mapped_column(Text, default="")
    testing_window: Mapped[str] = mapped_column(Text, default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    project: Mapped[Project] = relationship(back_populates="scope_items")


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (UniqueConstraint("project_id", "asset_type", "value", name="uq_asset_value"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    asset_type: Mapped[str] = mapped_column(String(100), nullable=False)
    value: Mapped[str] = mapped_column(String(1000), nullable=False)
    asn: Mapped[str] = mapped_column(String(100), default="")
    port: Mapped[int | None] = mapped_column(nullable=True)
    service: Mapped[str] = mapped_column(String(255), default="")
    technology: Mapped[str] = mapped_column(Text, default="")
    status_code: Mapped[int | None] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(String(1000), default="")
    screenshot_path: Mapped[str] = mapped_column(String(1000), default="")
    tls_info: Mapped[str] = mapped_column(Text, default="")
    waf_cdn_info: Mapped[str] = mapped_column(Text, default="")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    source: Mapped[str] = mapped_column(String(500), default="")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    scope_status: Mapped[str] = mapped_column(String(100), default="Needs Review")
    status: Mapped[str] = mapped_column(String(100), default=AssetStatus.NEW.value)
    notes: Mapped[str] = mapped_column(Text, default="")

    project: Mapped[Project] = relationship(back_populates="assets")
    findings: Mapped[list[Finding]] = relationship(back_populates="asset")
    evidence_items: Mapped[list[Evidence]] = relationship(back_populates="asset")


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), nullable=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(50), default=Severity.NEEDS_REVIEW.value)
    cvss_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    cwe: Mapped[str] = mapped_column(String(100), default="")
    owasp_category: Mapped[str] = mapped_column(String(255), default="")
    url: Mapped[str] = mapped_column(String(1000), default="")
    parameter: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    impact: Mapped[str] = mapped_column(Text, default="")
    reproduction_steps: Mapped[str] = mapped_column(Text, default="")
    remediation: Mapped[str] = mapped_column(Text, default="")
    references: Mapped[list[str]] = mapped_column(JSON, default=list)
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    verification_status: Mapped[str] = mapped_column(
        String(100),
        default=VerificationStatus.UNVERIFIED.value,
    )
    false_positive_notes: Mapped[str] = mapped_column(Text, default="")
    assigned_analyst: Mapped[str] = mapped_column(String(255), default="")
    report_inclusion_status: Mapped[str] = mapped_column(String(100), default="Needs Review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )

    project: Mapped[Project] = relationship(back_populates="findings")
    asset: Mapped[Asset | None] = relationship(back_populates="findings")
    evidence_items: Mapped[list[Evidence]] = relationship(back_populates="finding")


class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    asset_id: Mapped[str | None] = mapped_column(ForeignKey("assets.id"), nullable=True, index=True)
    finding_id: Mapped[str | None] = mapped_column(
        ForeignKey("findings.id"),
        nullable=True,
        index=True,
    )
    evidence_type: Mapped[str] = mapped_column(String(100), default=EvidenceType.MANUAL_NOTE.value)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    source: Mapped[str] = mapped_column(String(1000), default="")
    tool: Mapped[str] = mapped_column(String(255), default="")
    command: Mapped[str] = mapped_column(Text, default="")
    raw_output: Mapped[str] = mapped_column(Text, default="")
    analyst_note: Mapped[str] = mapped_column(Text, default="")
    file_path: Mapped[str] = mapped_column(String(1000), default="")
    file_hash_sha256: Mapped[str] = mapped_column(String(64), default="")
    immutable_after_freeze: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project] = relationship(back_populates="evidence_items")
    asset: Mapped[Asset | None] = relationship(back_populates="evidence_items")
    finding: Mapped[Finding | None] = relationship(back_populates="evidence_items")


class AuditRecord(Base):
    __tablename__ = "audit_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str | None] = mapped_column(
        ForeignKey("projects.id"),
        nullable=True,
        index=True,
    )
    event_type: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, default="")
    actor: Mapped[str] = mapped_column(String(255), default="")
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)

    project: Mapped[Project | None] = relationship(back_populates="audit_records")

    @classmethod
    def from_audit_event(cls, event: AuditEvent, project_id: str | None = None) -> AuditRecord:
        return cls(
            project_id=project_id,
            event_type=event.event_type,
            message=event.message,
            metadata_json=event.metadata,
            timestamp=datetime.fromisoformat(event.timestamp),
        )


class ToolCatalogEntryRecord(Base):
    __tablename__ = "tool_catalog_entries"
    __table_args__ = (UniqueConstraint("sequence", name="uq_tool_catalog_sequence"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    sequence: Mapped[int] = mapped_column(nullable=False, index=True)
    tool_name: Mapped[str] = mapped_column(Text, nullable=False, default="")
    name: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(Text, default="")
    subcategory: Mapped[str] = mapped_column(Text, default="")
    planned_phase: Mapped[str] = mapped_column(String(255), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    catalog_status: Mapped[str] = mapped_column(String(255), default="knowledge-entry-only")
    source_note: Mapped[str] = mapped_column(Text, default="")
    install_status: Mapped[str] = mapped_column(String(100), default="not_checked")
    support_status: Mapped[str] = mapped_column(
        String(255),
        default="not implemented unless adapter exists",
    )
    safety_note: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    license_note: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    official_url: Mapped[str] = mapped_column(String(1000), default="")
    install_notes: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    user_notes: Mapped[str] = mapped_column(Text, default="")
    ai_suggested: Mapped[str] = mapped_column(String(20), default="yes")
    verified_by_developer: Mapped[str] = mapped_column(String(20), default="no")
    documentation_url: Mapped[str] = mapped_column(String(1000), default="")
    disclaimer_status: Mapped[str] = mapped_column(
        String(255),
        default="requires_user_acceptance",
    )
    imported_from: Mapped[str] = mapped_column(String(255), default="user_pasted_tool_inventory")
    active_execution_supported: Mapped[bool] = mapped_column(Boolean, default=False)
    bundled_by_samaj: Mapped[bool] = mapped_column(Boolean, default=False)
    tested_by_samaj: Mapped[bool] = mapped_column(Boolean, default=False)
    recommended_by_samaj: Mapped[bool] = mapped_column(Boolean, default=False)
    windows_supported: Mapped[str] = mapped_column(String(20), default="unknown")
    kali_supported: Mapped[str] = mapped_column(String(20), default="unknown")
    linux_supported: Mapped[str] = mapped_column(String(20), default="unknown")
    mac_supported: Mapped[str] = mapped_column(String(20), default="unknown")
    install_method_windows: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    install_method_kali: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    install_method_linux: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    license: Mapped[str] = mapped_column(Text, default="Unknown / Not verified")
    adapter_available: Mapped[str] = mapped_column(String(20), default="no")
    safe_mode_required: Mapped[str] = mapped_column(String(20), default="yes")
    scope_required: Mapped[str] = mapped_column(String(20), default="yes")
    requires_admin_or_root: Mapped[str] = mapped_column(String(20), default="unknown")
    requires_network: Mapped[str] = mapped_column(String(20), default="unknown")
    requires_api_key: Mapped[str] = mapped_column(String(20), default="unknown")
    usage_notes: Mapped[str] = mapped_column(Text, default="Knowledge entry only.")
    legal_notes: Mapped[str] = mapped_column(Text, default="Use only with lawful authorization.")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )


class ToolCatalogDisclaimerAcceptance(Base):
    __tablename__ = "tool_catalog_disclaimer_acceptance"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default="global")
    user_accepted_tool_disclaimer_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    user_accepted_tool_disclaimer_version: Mapped[str] = mapped_column(
        String(100),
        default="2026-06-06",
    )
    actor: Mapped[str] = mapped_column(String(255), default="")
    acceptance_text: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        onupdate=utc_now,
    )


class ProxyRecord(Base):
    __tablename__ = "proxy_records"
    __table_args__ = (UniqueConstraint("ip", "port", "type", name="uq_proxy_endpoint"),)

    proxy_id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    ip: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    port: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(String(20), default="unknown")
    country: Mapped[str] = mapped_column(String(100), default="")
    asn: Mapped[str] = mapped_column(String(100), default="")
    source: Mapped[str] = mapped_column(String(1000), default="")
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now)
    last_checked: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="unknown")
    latency_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    download_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    upload_speed: Mapped[float | None] = mapped_column(Float, nullable=True)
    success_rate: Mapped[float] = mapped_column(Float, default=0.0)
    failure_count: Mapped[int] = mapped_column(default=0)
    last_error: Mapped[str] = mapped_column(Text, default="")
    requires_auth: Mapped[str] = mapped_column(String(20), default="unknown")
    username_reference: Mapped[str] = mapped_column(String(255), default="")
    password_reference: Mapped[str] = mapped_column(String(255), default="")
    notes: Mapped[str] = mapped_column(Text, default="")
    legal_status_note: Mapped[str] = mapped_column(
        Text,
        default="Proxy features must not be used for illegal activity.",
    )
    user_added: Mapped[bool] = mapped_column(Boolean, default=True)


@dataclass(frozen=True)
class FindingDraft:
    title: str
    severity: Severity = Severity.NEEDS_REVIEW
    verification_status: VerificationStatus = VerificationStatus.UNVERIFIED
    evidence_count: int = 0

    @property
    def is_reportable(self) -> bool:
        return self.evidence_count > 0 and self.verification_status != VerificationStatus.UNVERIFIED
