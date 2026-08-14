"""Track-B capability/adoption evidence and scenario governance."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

QUALITY_DIMENSIONS = (
    "task_representativeness",
    "evaluation_independence",
    "contamination_controls",
    "high_reliability_reporting",
    "system_configuration_disclosure",
    "reproducible_artifacts",
    "scientific_software_relevance",
)


@dataclass(frozen=True)
class CapabilityEvidence:
    evidence_id: str
    source_url_or_doi: str
    publisher: str
    publication_date: str
    retrieval_date: str
    evidence_type: str
    system_version: str
    benchmark_task: str
    environment: str
    permitted_tools: str
    task_duration: str
    repository_context_scale: str
    success_metric: str
    reliability_threshold: str
    human_assistance: str
    compute_cost: str
    contamination_controls_note: str
    reproducibility_status: str
    limitations: str
    conflicts_funding: str
    assessment: str
    quality_scores: dict[str, int]


@dataclass(frozen=True)
class ScenarioForecast:
    forecast_id: str
    scenario: str
    horizon_months: int
    evidence_cutoff_date: str
    assumptions: str
    leading_indicators: str
    disconfirming_indicators: str
    probability_low: float | None
    probability_high: float | None
    implications: str
    human_approved: bool


def quality_score(evidence: CapabilityEvidence) -> tuple[int, str]:
    if set(evidence.quality_scores) != set(QUALITY_DIMENSIONS):
        raise ValueError("quality score dimensions are incomplete")
    if any(value not in {0, 1, 2} for value in evidence.quality_scores.values()):
        raise ValueError("quality dimensions must be scored 0, 1, or 2")
    score = sum(evidence.quality_scores.values())
    label = "strong" if score >= 11 else "moderate" if score >= 7 else "weak"
    return score, label


def central_projection_eligible(evidence: CapabilityEvidence) -> bool:
    _, label = quality_score(evidence)
    return label in {"strong", "moderate"}


def validate_track_separation(track: str, denominator: str | None) -> None:
    if track == "B" and denominator == "included_jobs":
        raise ValueError("Track B must not use the Track A job-sample denominator")
    if track not in {"A", "B"}:
        raise ValueError("unknown analytical track")


def append_scenario(path: Path, forecast: ScenarioForecast) -> None:
    scenarios = {
        "incremental_assistance",
        "agentic_delegation",
        "supervised_autonomy",
        "reliability_governance_bottleneck",
    }
    if forecast.scenario not in scenarios or forecast.horizon_months not in {
        12,
        24,
        36,
    }:
        raise ValueError("invalid scenario or horizon")
    bounds = (forecast.probability_low, forecast.probability_high)
    if any(value is not None and not 0 <= value <= 1 for value in bounds):
        raise ValueError("probability bounds must be in [0, 1]")
    low, high = bounds
    if low is not None and high is not None and low > high:
        raise ValueError("probability range is reversed")
    if forecast.human_approved and None in bounds:
        raise ValueError("approved forecast requires probability bounds")
    path.parent.mkdir(parents=True, exist_ok=True)
    existing_ids = set()
    if path.exists():
        existing_ids = {
            json.loads(line)["forecast_id"]
            for line in path.read_text().splitlines()
            if line
        }
    if forecast.forecast_id in existing_ids:
        raise ValueError("forecasts are append-only; forecast_id already exists")
    with path.open("a") as handle:
        handle.write(json.dumps(forecast.__dict__, sort_keys=True) + "\n")


def brier_score(probabilities: list[float], outcomes: list[int]) -> float:
    if len(probabilities) != len(outcomes) or not probabilities:
        raise ValueError("aligned nonempty forecast and outcome lists required")
    if any(not 0 <= probability <= 1 for probability in probabilities):
        raise ValueError("probabilities must be in [0, 1]")
    if any(outcome not in {0, 1} for outcome in outcomes):
        raise ValueError("outcomes must be binary")
    return sum(
        (probability - outcome) ** 2
        for probability, outcome in zip(probabilities, outcomes, strict=True)
    ) / len(outcomes)
