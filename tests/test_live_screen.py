import json
from pathlib import Path

from market_analysis.adapters import Posting
from market_analysis.live_screen import _facts, _role_family, _seniority
from market_analysis.screen import screen


def _posting(title: str, description: str, location: str) -> Posting:
    return Posting(
        source="greenhouse",
        posting_id="123",
        title=title,
        description_text=description,
        locations=(location,),
        canonical_url="https://job-boards.greenhouse.io/example/jobs/123",
        compensation=None,
    )


def test_live_rule_includes_explicit_us_bioinformatics_engineering() -> None:
    posting = _posting(
        "Bioinformatics Engineer",
        "Build Python and Nextflow pipelines for genomic sequencing analysis. " * 8,
        "Boston, MA",
    )
    decision = screen(_facts(posting))
    assert decision.inclusion_decision == "include"
    assert _role_family(posting.title) == "bioinformatics_engineering"


def test_live_rule_excludes_wet_lab_and_internship() -> None:
    wet_lab = _posting(
        "Scientist, Cell Biology",
        "Run cellular assays for therapeutic discovery and molecular biology. " * 8,
        "Cambridge, MA",
    )
    internship = _posting(
        "Bioinformatics Intern",
        "Build Python pipelines for genomic sequencing and biological data. " * 8,
        "Fremont, CA",
    )
    assert screen(_facts(wet_lab)).decision_reason_code == "exclude_not_engineering"
    assert screen(_facts(internship)).decision_reason_code == "exclude_internship"


def test_live_rule_fails_closed_on_global_remote_geography() -> None:
    posting = _posting(
        "Computational Biologist",
        "Develop Python software for biological and genomic analysis. " * 8,
        "Remote",
    )
    decision = screen(_facts(posting))
    assert decision.inclusion_decision == "exclude"
    assert decision.decision_reason_code == "exclude_geography"


def test_committed_live_artifacts_are_internally_consistent() -> None:
    root = Path(__file__).parents[1]
    report_path = root / "reports/2026-08/live_pool_screening.json"
    if not report_path.exists():
        return
    report = json.loads(report_path.read_text())
    decisions = (
        (root / "data/validated/2026-08/screening_decisions.jsonl")
        .read_text()
        .splitlines()
    )
    jobs = (
        (root / "data/validated/2026-08/screened_jobs.jsonl").read_text().splitlines()
    )
    assert report["screened_n"] == len(decisions)
    assert report["deterministic_include_before_dedup_n"] == len(jobs)
    assert report["raw_descriptions_committed"] is False
    assert report["human_review_complete"] is False


def test_seniority_rules_are_explicit() -> None:
    assert _seniority("Senior Bioinformatics Engineer") == "senior_plus"
    assert _seniority("Associate Computational Scientist") == "entry_associate"
    assert _seniority("Bioinformatics Engineer") == "unspecified"
