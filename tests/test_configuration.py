"""Tests for the versioned study configuration and controlled values."""

from pathlib import Path
from typing import cast

from market_analysis.config import load_json_mapping, load_yaml_mapping

ROOT = Path(__file__).parents[1]


def _mapping(value: object) -> dict[str, object]:
    assert isinstance(value, dict)
    assert all(isinstance(key, str) for key in value)
    return cast("dict[str, object]", value)


def _values(codebook: dict[str, object], field: str) -> list[str]:
    values = _mapping(codebook["controlled_values"])[field]
    assert isinstance(values, list)
    assert all(isinstance(value, str) for value in values)
    return cast("list[str]", values)


def test_study_configuration_matches_approved_defaults() -> None:
    """The versioned configuration preserves specification 1.1.1 defaults."""
    config = load_yaml_mapping(ROOT / "config" / "study.yaml")

    assert config["config_version"] == "1.0.0"
    assert config["study_id"] == "BSE-JMA-001"
    assert config["spec_version"] == "1.1.1"
    assert config["taxonomy_version"] == "1.0.0"
    assert config["timezone"] == "America/New_York"

    scope = _mapping(config["scope"])
    sampling = _mapping(config["sampling"])
    review = _mapping(config["review"])
    publication = _mapping(config["publication"])

    assert scope == {"geography": "US", "collection_window_days_max": 7}
    assert sampling["target_n"] == 150
    assert sampling["minimum_candidate_pool"] == 220
    assert sampling["minimum_reserve_pool"] == 20
    assert sampling["company_cap"] == 5
    assert sampling["template_cap"] == 3
    assert sampling["minimum_first_party_fraction"] == 0.70
    assert review["human_approval_required"] is True
    assert publication["canonical_publication_approved"] is False


def test_controlled_values_are_unique_and_cover_normative_values() -> None:
    """Controlled identifiers are unambiguous and include spec-defined values."""
    codebook = load_yaml_mapping(ROOT / "schemas" / "codebook.yaml")
    controlled = _mapping(codebook["controlled_values"])

    for field in controlled:
        values = _values(codebook, field)
        assert values
        assert len(values) == len(set(values))
        assert all(value == value.lower() and " " not in value for value in values)

    assert _values(codebook, "requirement.requirement_status") == [
        "required",
        "preferred",
        "responsibility",
        "benefit_context",
        "unclear",
    ]
    assert _values(codebook, "requirement.ai_relation") == [
        "none",
        "ai_assisted_development",
        "ai_ml_engineering",
        "generative_ai_llm",
        "ai_agents_or_orchestration",
        "ai_evaluation_safety",
        "ai_scientific_application",
        "ambiguous_ai",
    ]
    assert len(_values(codebook, "job.role_family")) == 6
    assert len(_values(codebook, "job.sector")) == 9


def test_run_metadata_template_is_explicitly_pre_collection() -> None:
    """The example records required run fields without claiming collection."""
    metadata = load_json_mapping(ROOT / "config" / "run_metadata.example.json")
    required_fields = {
        "run_id",
        "spec_version",
        "taxonomy_version",
        "pipeline_version",
        "collection_started_at",
        "collection_closed_at",
        "publication_month",
        "target_n",
        "included_n",
        "candidate_n",
        "reserve_n",
        "previous_run_id",
        "git_commit",
        "status",
        "human_reviewer",
        "freeze_timestamp",
        "notes",
    }

    assert required_fields <= metadata.keys()
    assert metadata["run_id"] == "2026-08_bioinfo_jobs_us_v01"
    assert metadata["status"] == "initialized"
    assert metadata["collection_started_at"] is None
    assert metadata["collection_closed_at"] is None
    assert metadata["included_n"] == 0
    assert metadata["candidate_n"] == 0
    assert metadata["reserve_n"] == 0
    assert metadata["taxonomy_version"] == "1.0.0"
    assert metadata["human_reviewer"] is None
