from __future__ import annotations

from samaj.core.anti_hallucination import VerificationStatus
from samaj.db.crud import SamajRepository, ToolCatalogDisclaimerRequiredError
from samaj.db.database import DatabaseManager, default_database_config
from samaj.db.models import AssetStatus, EvidenceType, ProjectState, Severity
from samaj.tools.catalog import list_catalog_entries


def test_phase_2_crud_flow(tmp_path):
    manager = DatabaseManager(default_database_config(tmp_path))
    manager.init()

    with manager.session() as session:
        repository = SamajRepository(session)

        project = repository.create_project(
            "Authorized Program",
            client_organization="Example Org",
            authorization_notes="Written authorization stored by analyst.",
            rate_limits="30 requests per minute",
        )
        assert project.state == ProjectState.DRAFT.value

        updated = repository.update_project(
            project.id,
            state=ProjectState.SCOPE_DEFINED.value,
            scope_summary="example.com",
        )
        assert updated.state == ProjectState.SCOPE_DEFINED.value

        scope_item = repository.create_scope_item(
            project.id,
            "domain",
            "example.com",
            authorized_test_types=("passive_recon", "manual_review"),
        )
        assert scope_item.in_scope is True

        first_asset = repository.create_asset(
            project.id,
            "domain",
            "example.com",
            status=AssetStatus.VALIDATED.value,
            confidence=0.9,
        )
        duplicate_asset = repository.create_asset(
            project.id,
            "domain",
            "example.com",
            notes="seen again",
        )
        assert duplicate_asset.id == first_asset.id
        assert duplicate_asset.notes == "seen again"

        finding = repository.create_finding(
            project.id,
            "Needs evidence before severity",
            asset_id=first_asset.id,
            severity=Severity.NEEDS_REVIEW,
            verification_status=VerificationStatus.UNVERIFIED,
        )
        assert finding.verification_status == VerificationStatus.UNVERIFIED.value

        evidence = repository.create_evidence(
            project.id,
            EvidenceType.MANUAL_NOTE,
            asset_id=first_asset.id,
            finding_id=finding.id,
            source="analyst",
            tool="manual",
            command="manual note",
            raw_output="No automated scan output.",
            analyst_note="Evidence placeholder for CRUD verification.",
        )
        assert evidence.finding_id == finding.id

        audits = repository.list_audit_records(project.id)
        assert {record.event_type for record in audits} >= {
            "project_created",
            "project_updated",
            "scope_item_created",
            "asset_created",
            "finding_created",
            "evidence_created",
        }

        archived = repository.archive_project(project.id)
        assert archived.state == ProjectState.ARCHIVED.value
        assert repository.list_projects() == []
        assert repository.list_projects(include_archived=True)[0].id == project.id


def test_database_file_is_created(tmp_path):
    config = default_database_config(tmp_path)
    manager = DatabaseManager(config)
    manager.init()

    assert config.sqlite_path.exists()


def test_tool_catalog_import_requires_explicit_disclaimer_acceptance(tmp_path):
    manager = DatabaseManager(default_database_config(tmp_path))
    manager.init()
    entries = list_catalog_entries()

    with manager.session() as session:
        repository = SamajRepository(session)

        try:
            repository.import_tool_catalog_entries(entries)
        except ToolCatalogDisclaimerRequiredError:
            pass
        else:  # pragma: no cover
            raise AssertionError("Catalog import must require disclaimer acceptance.")

        acceptance = repository.accept_tool_catalog_disclaimer(
            accepted=True,
            actor="test",
            acceptance_text="accepted in test",
        )
        assert acceptance.user_accepted_tool_disclaimer_at is not None
        assert acceptance.user_accepted_tool_disclaimer_version == "2026-06-06"

        imported = repository.import_tool_catalog_entries(entries)
        assert imported == 1620

        records = repository.list_tool_catalog_entries()
        assert len(records) == 1620
        assert records[0].name == "Nmap"
        assert records[0].install_status == "not_checked"
        assert records[0].support_status == "not implemented unless adapter exists"
        assert records[0].catalog_status == "knowledge-entry-only"
        assert records[0].windows_supported == "unknown"
        assert records[0].kali_supported == "unknown"
        assert records[0].ai_suggested == "yes"
        assert records[0].verified_by_developer == "no"
        assert records[0].active_execution_supported is False

        detail = repository.get_tool_catalog_entry(records[0].id)
        assert detail.name == "Nmap"


def test_tool_catalog_detail_requires_acceptance(tmp_path):
    manager = DatabaseManager(default_database_config(tmp_path))
    manager.init()

    with manager.session() as session:
        repository = SamajRepository(session)
        try:
            repository.list_tool_catalog_entries()
        except ToolCatalogDisclaimerRequiredError:
            pass
        else:  # pragma: no cover
            raise AssertionError("Catalog detail/list viewing must require acceptance.")
