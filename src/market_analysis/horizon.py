"""Track-B capability/adoption evidence and scenario governance."""

from __future__ import annotations

from dataclasses import dataclass

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
