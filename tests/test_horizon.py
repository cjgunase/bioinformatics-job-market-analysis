from dataclasses import replace

import pytest

from market_analysis.horizon import (
    QUALITY_DIMENSIONS,
    CapabilityEvidence,
    central_projection_eligible,
    quality_score,
    validate_track_separation,
)


def evidence(score: int) -> CapabilityEvidence:
    return CapabilityEvidence(
        "ev1",
        "https://example.test/paper",
        "Example",
        "2026-08-01",
        "2026-08-14",
        "reproducible_benchmark",
        "system-1",
        "repository issue resolution",
        "container",
        "shell and tests",
        "2 hours",
        "multi-file repository",
        "resolved",
        "80%",
        "none",
        "reported",
        "declared",
        "artifacts_available",
        "fixture only",
        "none declared",
        "synthetic test record",
        {dimension: score for dimension in QUALITY_DIMENSIONS},
    )


@pytest.mark.parametrize(
    ("item", "expected"),
    [
        (evidence(2), (14, "strong")),
        (evidence(1), (7, "moderate")),
        (evidence(0), (0, "weak")),
    ],
)
def test_quality_score_boundaries(
    item: CapabilityEvidence, expected: tuple[int, str]
) -> None:
    assert quality_score(item) == expected
    assert central_projection_eligible(item) == (expected[1] != "weak")


def test_quality_score_requires_every_dimension() -> None:
    with pytest.raises(ValueError, match="incomplete"):
        quality_score(replace(evidence(1), quality_scores={}))


def test_track_b_cannot_use_job_denominator() -> None:
    with pytest.raises(ValueError, match="must not"):
        validate_track_separation("B", "included_jobs")
    validate_track_separation("B", None)
