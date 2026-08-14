from dataclasses import replace
from pathlib import Path

import pytest

from market_analysis.horizon import (
    QUALITY_DIMENSIONS,
    CapabilityEvidence,
    ScenarioForecast,
    append_scenario,
    brier_score,
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


def test_scenarios_are_append_only_and_unapproved_ranges_may_stay_null(
    tmp_path: Path,
) -> None:
    forecast = ScenarioForecast(
        "2026-08_incremental_12",
        "incremental_assistance",
        12,
        "2026-08-14",
        "Evidence synthesis pending",
        "reliable long-horizon task success",
        "persistent regression and high review burden",
        None,
        None,
        "Draft implications pending human forecasting review",
        False,
    )
    path = tmp_path / "forecasts.jsonl"
    append_scenario(path, forecast)
    with pytest.raises(ValueError, match="append-only"):
        append_scenario(path, forecast)
    assert len(path.read_text().splitlines()) == 1


def test_brier_score_known_value_and_validation() -> None:
    assert brier_score([0.8, 0.3], [1, 0]) == pytest.approx(0.065)
    with pytest.raises(ValueError):
        brier_score([1.2], [1])
