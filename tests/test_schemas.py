"""Tests for the versioned JSON Schema record contracts."""

from copy import deepcopy
from pathlib import Path
from typing import cast

import pytest
from jsonschema.exceptions import ValidationError

from market_analysis.config import load_json_mapping, load_yaml_mapping
from market_analysis.schema import validate_record, validator_for

ROOT = Path(__file__).parents[1]
SCHEMA_DIR = ROOT / "schemas"
SCHEMA_NAMES = ("runs", "jobs", "requirements", "evidence")

type StringMapping = dict[str, object]


def _mapping(value: object) -> StringMapping:
    assert isinstance(value, dict)
    assert all(isinstance(key, str) for key in value)
    return cast("StringMapping", value)


def _string_list(value: object) -> list[str]:
    assert isinstance(value, list)
    assert all(isinstance(item, str) for item in value)
    return cast("list[str]", value)


def _schema(name: str) -> StringMapping:
    return load_json_mapping(SCHEMA_DIR / f"{name}.schema.json")


def _valid_job() -> StringMapping:
    return {
        "run_id": "2026-08_bioinfo_jobs_us_v01",
        "job_id": "job-001",
        "canonical_job_id": "example.com:req-001",
        "company_name_raw": "Example Bio, Inc.",
        "company_name_normalized": "example_bio",
        "company_domain": "example.com",
        "title_raw": "Bioinformatics Software Engineer",
        "title_normalized": "bioinformatics software engineer",
        "role_family": "bioinformatics_engineering",
        "seniority": "mid_level",
        "sector": "biotechnology_tools",
        "employment_type": "full_time",
        "location_raw": "Boston, MA",
        "country": "US",
        "state": "MA",
        "city": "Boston",
        "location_mode": "hybrid",
        "us_eligible": True,
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "posting_date": "2026-08-01",
        "first_seen_at": "2026-08-02T12:00:00Z",
        "last_verified_at": "2026-08-03T12:00:00Z",
        "active_at_freeze": True,
        "canonical_url": "https://example.com/jobs/req-001",
        "discovery_url": "https://example.com/careers",
        "source_type": "employer_operated_ats",
        "requisition_id": "req-001",
        "description_sha256": "a" * 64,
        "template_fingerprint": "b" * 64,
        "full_text_path": "data/raw/2026-08/job-001.json",
        "selection_status": "included",
        "inclusion_decision": "include",
        "decision_reason_code": "include_meets_all",
        "decision_rationale": "All inclusion criteria are explicitly supported.",
        "inclusion_confidence": 0.98,
        "duplicate_cluster_id": None,
        "replacement_for_job_id": None,
        "human_review_status": "not_reviewed",
    }


def _valid_requirement() -> StringMapping:
    return {
        "run_id": "2026-08_bioinfo_jobs_us_v01",
        "requirement_id": "requirement-001",
        "job_id": "job-001",
        "evidence_id": "evidence-001",
        "requirement_text_normalized": "build reproducible Python pipelines",
        "requirement_status": "responsibility",
        "taxonomy_category_id": None,
        "taxonomy_skill_id": None,
        "tool_or_technology_raw": "Python",
        "years_experience_min": None,
        "years_experience_max": None,
        "education_level": None,
        "proficiency_term": None,
        "ai_relation": "none",
        "extraction_method": "deterministic_fixture",
        "extractor_model": None,
        "prompt_version": None,
        "confidence": 0.99,
        "human_verified": False,
        "adjudication_note": None,
    }


def _valid_evidence() -> StringMapping:
    return {
        "evidence_id": "evidence-001",
        "job_id": "job-001",
        "source_url": "https://example.com/jobs/req-001",
        "retrieved_at": "2026-08-03T12:00:00Z",
        "source_section": "Responsibilities",
        "paragraph_or_bullet_index": 2,
        "char_start": 120,
        "char_end": 156,
        "verbatim_excerpt": "Build reproducible Python pipelines.",
        "excerpt_sha256": "c" * 64,
        "snapshot_sha256": "a" * 64,
        "capture_method": "public_ats_api",
        "terms_retention_mode": "excerpt_hash_metadata_only",
    }


def test_all_schemas_are_valid_draft_2020_12_documents() -> None:
    """Every checked-in contract is itself a valid, uniquely identified schema."""
    identifiers: set[object] = set()

    for name in SCHEMA_NAMES:
        schema = _schema(name)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] not in identifiers
        identifiers.add(schema["$id"])
        validator_for(schema)


def test_valid_records_pass_their_contracts() -> None:
    """Representative run, job, requirement, and evidence records validate."""
    records = {
        "runs": load_json_mapping(ROOT / "config" / "run_metadata.example.json"),
        "jobs": _valid_job(),
        "requirements": _valid_requirement(),
        "evidence": _valid_evidence(),
    }

    for name, record in records.items():
        validate_record(record, _schema(name))


@pytest.mark.parametrize(
    ("schema_name", "field", "invalid_value"),
    [
        ("runs", "target_n", 149),
        ("runs", "run_id", "2026-8-bad"),
        ("jobs", "canonical_url", "http://example.com/jobs/req-001"),
        ("jobs", "description_sha256", "not-a-sha256"),
        ("requirements", "confidence", 1.01),
        ("requirements", "ai_relation", "generic_automation"),
        ("evidence", "retrieved_at", "2026-08-03 12:00:00"),
        ("evidence", "excerpt_sha256", "C" * 64),
    ],
)
def test_invalid_field_values_fail_closed(
    schema_name: str, field: str, invalid_value: object
) -> None:
    """Invalid identifiers, formats, hashes, and ranges are rejected."""
    records = {
        "runs": load_json_mapping(ROOT / "config" / "run_metadata.example.json"),
        "jobs": _valid_job(),
        "requirements": _valid_requirement(),
        "evidence": _valid_evidence(),
    }
    record = deepcopy(records[schema_name])
    record[field] = invalid_value

    with pytest.raises(ValidationError):
        validate_record(record, _schema(schema_name))


@pytest.mark.parametrize("schema_name", SCHEMA_NAMES)
def test_missing_or_undeclared_fields_fail_closed(schema_name: str) -> None:
    """Contracts require all declared fields and reject accidental additions."""
    records = {
        "runs": load_json_mapping(ROOT / "config" / "run_metadata.example.json"),
        "jobs": _valid_job(),
        "requirements": _valid_requirement(),
        "evidence": _valid_evidence(),
    }
    schema = _schema(schema_name)
    required = _string_list(schema["required"])

    missing = deepcopy(records[schema_name])
    del missing[required[0]]
    with pytest.raises(ValidationError):
        validate_record(missing, schema)

    undeclared = deepcopy(records[schema_name])
    undeclared["silent_extra_field"] = "not permitted"
    with pytest.raises(ValidationError):
        validate_record(undeclared, schema)


@pytest.mark.parametrize(
    ("schema_name", "property_name", "codebook_name"),
    [
        ("runs", "status", "run.status"),
        ("jobs", "role_family", "job.role_family"),
        ("jobs", "seniority", "job.seniority"),
        ("jobs", "sector", "job.sector"),
        ("jobs", "employment_type", "job.employment_type"),
        ("jobs", "location_mode", "job.location_mode"),
        ("jobs", "source_type", "job.source_type"),
        ("jobs", "selection_status", "job.selection_status"),
        ("jobs", "inclusion_decision", "job.inclusion_decision"),
        ("jobs", "decision_reason_code", "job.decision_reason_code"),
        ("jobs", "human_review_status", "job.human_review_status"),
        ("requirements", "requirement_status", "requirement.requirement_status"),
        ("requirements", "ai_relation", "requirement.ai_relation"),
        ("evidence", "terms_retention_mode", "evidence.terms_retention_mode"),
    ],
)
def test_schema_enums_match_the_codebook(
    schema_name: str, property_name: str, codebook_name: str
) -> None:
    """Machine validation and documented controlled values cannot drift."""
    codebook = load_yaml_mapping(SCHEMA_DIR / "codebook.yaml")
    controlled_values = _mapping(codebook["controlled_values"])
    properties = _mapping(_schema(schema_name)["properties"])
    property_schema = _mapping(properties[property_name])

    assert _string_list(property_schema["enum"]) == _string_list(
        controlled_values[codebook_name]
    )
