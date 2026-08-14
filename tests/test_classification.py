from pathlib import Path

from market_analysis.classify import load_taxonomy, map_evidence
from market_analysis.extract import DeterministicBulletExtractor, ExtractionContext

ROOT = Path(__file__).parents[1]


def test_exact_taxonomy_mapping_and_within_job_collapse() -> None:
    text = "Requirements:\n- Python and Docker.\n- Python for testing.\n"
    context = ExtractionContext(
        "run", "job", "https://example.test/job", "2026-08-14T04:20:00Z", "a" * 64
    )
    evidence = DeterministicBulletExtractor().extract(text, context)
    mappings = map_evidence(evidence, load_taxonomy(ROOT / "taxonomy/taxonomy.yaml"))
    python = [row for row in mappings if row.taxonomy_skill_id == "python"]
    assert len(python) == 1
    assert len(python[0].evidence_ids) == 2
    assert python[0].quantitative_eligible


def test_ai_mapping_always_routes_to_human_review() -> None:
    text = "Requirements:\n- Experience with machine learning engineering.\n"
    context = ExtractionContext(
        "run", "job", "https://example.test/job", "2026-08-14T04:20:00Z", "a" * 64
    )
    evidence = DeterministicBulletExtractor().extract(text, context)
    mappings = map_evidence(evidence, load_taxonomy(ROOT / "taxonomy/taxonomy.yaml"))
    ai_rows = [row for row in mappings if row.ai_relation != "none"]
    assert ai_rows
    assert all(row.human_review_status == "pending" for row in ai_rows)
