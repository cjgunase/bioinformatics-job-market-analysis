"""Tests for taxonomy 1.0.0 structure, governance, and version alignment."""

import re
from pathlib import Path
from typing import cast

from market_analysis.config import load_json_mapping, load_yaml_mapping

ROOT = Path(__file__).parents[1]
TAXONOMY_PATH = ROOT / "taxonomy" / "taxonomy.yaml"
IDENTIFIER = re.compile(r"^[a-z0-9][a-z0-9_]*$")

type StringMapping = dict[str, object]


def _mapping(value: object) -> StringMapping:
    assert isinstance(value, dict)
    assert all(isinstance(key, str) for key in value)
    return cast("StringMapping", value)


def _mapping_list(value: object) -> list[StringMapping]:
    assert isinstance(value, list)
    return [_mapping(item) for item in value]


def _string(value: object) -> str:
    assert isinstance(value, str)
    return value


def _taxonomy() -> StringMapping:
    return load_yaml_mapping(TAXONOMY_PATH)


def test_taxonomy_has_required_baseline_metadata_and_human_boundary() -> None:
    """The implementation baseline is versioned without claiming approval."""
    taxonomy = _taxonomy()

    assert taxonomy["taxonomy_version"] == "1.0.0"
    assert taxonomy["spec_version"] == "1.1.1"
    assert taxonomy["status"] == "implementation_baseline"
    assert taxonomy["human_review_status"] == "pending_initial_review"
    assert taxonomy["canonical_findings_eligible"] is False
    assert "most specific" in _string(taxonomy["coding_rule"])
    assert "reported separately" in _string(taxonomy["context_rule"])
    assert "not AI evidence" in _string(taxonomy["ai_rule"])


def test_categories_and_skill_rows_are_complete_and_stable() -> None:
    """Every row carries the specification 7.5 fields and stable identifiers."""
    taxonomy = _taxonomy()
    categories = _mapping_list(taxonomy["categories"])
    skills = _mapping_list(taxonomy["skills"])
    category_ids = [_string(category["category_id"]) for category in categories]
    skill_ids = [_string(skill["skill_id"]) for skill in skills]
    required_fields = {
        "taxonomy_version",
        "category_id",
        "skill_id",
        "preferred_label",
        "definition",
        "include_when",
        "exclude_when",
        "aliases",
        "parent_skill_id",
        "is_tool",
        "is_ai_related",
        "introduced_in_version",
        "deprecated_in_version",
    }

    assert len(categories) == 13
    assert len(skills) == 187
    assert len(category_ids) == len(set(category_ids))
    assert len(skill_ids) == len(set(skill_ids))
    assert all(IDENTIFIER.fullmatch(identifier) for identifier in category_ids)
    assert all(IDENTIFIER.fullmatch(identifier) for identifier in skill_ids)

    for category in categories:
        assert set(category) == {"category_id", "preferred_label", "definition"}
        assert _string(category["preferred_label"])
        assert _string(category["definition"])

    for skill in skills:
        assert set(skill) == required_fields
        assert skill["taxonomy_version"] == "1.0.0"
        assert skill["category_id"] in category_ids
        assert _string(skill["preferred_label"])
        assert _string(skill["definition"])
        assert _string(skill["include_when"])
        assert _string(skill["exclude_when"])
        assert isinstance(skill["is_tool"], bool)
        assert isinstance(skill["is_ai_related"], bool)
        assert skill["introduced_in_version"] == "1.0.0"
        assert skill["deprecated_in_version"] is None
        aliases = skill["aliases"]
        assert isinstance(aliases, list)
        assert all(isinstance(alias, str) and alias for alias in aliases)
        assert len(aliases) == len(set(cast("list[str]", aliases)))


def test_parent_links_resolve_without_cycles_or_cross_category_rollups() -> None:
    """Hierarchy rollups resolve deterministically within top-level categories."""
    skills = _mapping_list(_taxonomy()["skills"])
    by_id = {_string(skill["skill_id"]): skill for skill in skills}

    for skill_id, skill in by_id.items():
        parent = skill["parent_skill_id"]
        if parent is None:
            continue
        assert isinstance(parent, str)
        assert parent in by_id
        assert by_id[parent]["category_id"] == skill["category_id"]

        seen = {skill_id}
        current: object = parent
        while current is not None:
            assert isinstance(current, str)
            assert current not in seen
            seen.add(current)
            current = by_id[current]["parent_skill_id"]


def test_normative_taxonomy_sections_and_guardrails_are_represented() -> None:
    """The approved baseline's named sections and high-risk distinctions exist."""
    taxonomy = _taxonomy()
    skills = _mapping_list(taxonomy["skills"])
    by_id = {_string(skill["skill_id"]): skill for skill in skills}
    expected_nodes = {
        "python",
        "git",
        "unit_testing",
        "scientific_validation",
        "ci_cd",
        "docker",
        "kubernetes",
        "nextflow",
        "snakemake",
        "workflow_provenance",
        "data_quality",
        "system_design",
        "secure_coding",
        "technical_documentation",
        "ngs_genomics_pipelines",
        "ai_assisted_software_development",
        "ml_engineering",
        "generative_ai_llms",
        "ai_agents_orchestration",
        "ai_evaluation_safety",
        "ambiguous_ai",
        "specification_intent_engineering",
        "codebase_system_comprehension",
        "context_engineering",
        "verification_validation",
        "reproducibility_provenance",
        "scientific_uncertainty_correctness",
        "ai_generated_code_governance",
        "security_containment",
        "maintenance_stewardship",
        "human_factors_organizational_design",
    }

    assert expected_nodes <= by_id.keys()
    assert all(
        skill["is_ai_related"] is True
        for skill in skills
        if skill["category_id"] == "ai_engineering"
    )
    assert all(
        skill["category_id"] == "bioinformatics_engineering_context"
        for skill_id, skill in by_id.items()
        if skill_id
        in {
            "single_cell",
            "proteomics",
            "variant_calling",
            "clinical_bioinformatics",
        }
    )
    assert by_id["docker"]["is_tool"] is True
    assert by_id["kubernetes"]["is_tool"] is True
    assert "Do not infer Kubernetes" in _string(by_id["kubernetes"]["exclude_when"])
    assert "conventional bioinformatics" in _string(
        by_id["ambiguous_ai"]["exclude_when"]
    )


def test_config_records_and_schemas_pin_taxonomy_1_0_0() -> None:
    """Configuration and record contracts cannot silently use another taxonomy."""
    config = load_yaml_mapping(ROOT / "config" / "study.yaml")
    metadata = load_json_mapping(ROOT / "config" / "run_metadata.example.json")
    run_schema = load_json_mapping(ROOT / "schemas" / "runs.schema.json")
    requirement_schema = load_json_mapping(
        ROOT / "schemas" / "requirements.schema.json"
    )

    assert config["taxonomy_version"] == "1.0.0"
    assert metadata["taxonomy_version"] == "1.0.0"
    run_properties = _mapping(run_schema["properties"])
    assert _mapping(run_properties["taxonomy_version"])["const"] == "1.0.0"
    requirement_properties = _mapping(requirement_schema["properties"])
    assert _mapping(requirement_properties["taxonomy_category_id"])["$ref"] == (
        "#/$defs/identifier"
    )
    assert _mapping(requirement_properties["taxonomy_skill_id"])["$ref"] == (
        "#/$defs/identifier"
    )


def test_governance_changelog_preserves_review_and_migration_requirements() -> None:
    """Taxonomy governance documents review, versioning, and time-series impact."""
    changelog = (ROOT / "taxonomy" / "CHANGELOG.md").read_text(encoding="utf-8")

    assert "## 1.0.0 — 2026-08-14" in changelog
    assert "patch releases" in changelog
    assert "minor releases" in changelog
    assert "major releases" in changelog
    assert "A human must review taxonomy additions" in changelog
    assert "Time-series impact" in changelog
    assert "Backcast plan" in changelog
    assert "pending initial human review" in changelog
