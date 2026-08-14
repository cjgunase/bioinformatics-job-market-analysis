from market_analysis.deduplicate import (
    DedupRecord,
    canonical_job_id,
    canonicalize_url,
    exact_duplicate_groups,
    near_duplicate_candidates,
    normalize_label,
    template_fingerprint,
)


def record(job_id: str, **changes: object) -> DedupRecord:
    values: dict[str, object] = {
        "job_id": job_id,
        "company_domain": "example.org",
        "company_name": "Example, Inc.",
        "title": "Senior Bioinformatics Engineer",
        "location_group": "Boston MA",
        "canonical_url": f"https://EXAMPLE.org/jobs/{job_id}?utm_source=x",
        "requisition_id": job_id,
        "normalized_text_sha256": "a" * 64,
        "comparison_text": "build python workflows",
    }
    values.update(changes)
    return DedupRecord(**values)  # type: ignore[arg-type]


def test_url_and_label_normalization_preserve_level_terms() -> None:
    assert canonicalize_url("https://EXAMPLE.org/jobs/1/?utm_source=x&a=1#z") == (
        "https://example.org/jobs/1?a=1"
    )
    assert normalize_label("Sr. Bioinformatics Engineer") == (
        "sr bioinformatics engineer"
    )


def test_canonical_id_prefers_domain_and_requisition() -> None:
    assert canonical_job_id(record("REQ-1")) == canonical_job_id(
        record("other", requisition_id="REQ-1", title="Different")
    )


def test_exact_duplicates_detect_url_requisition_and_text() -> None:
    records = [
        record("a"),
        record("b", requisition_id="a"),
        record("c", normalized_text_sha256="c" * 64),
        record("d", canonical_url="https://example.org/jobs/c"),
    ]
    groups = exact_duplicate_groups(records)
    assert ("a", "b") in groups
    assert ("c", "d") in groups


def test_near_duplicates_route_uncertain_band_to_human() -> None:
    common = "python workflow cloud testing reproducibility genomics pipelines docker"
    records = [
        record("a", comparison_text=common),
        record("b", comparison_text=common + " aws"),
        record("c", comparison_text=common + " aws sql"),
    ]
    pairs = near_duplicate_candidates(records)
    assert pairs[0].disposition == "pending_human"
    assert any(pair.disposition == "duplicate_candidate" for pair in pairs)


def test_near_duplicate_comparison_is_scoped_to_same_employer() -> None:
    rows = [
        record("a", comparison_text="one two three"),
        record(
            "b",
            company_domain="different.org",
            comparison_text="one two three",
        ),
    ]
    assert near_duplicate_candidates(rows) == []
    assert template_fingerprint("Same  Template!") == template_fingerprint(
        "same template"
    )
