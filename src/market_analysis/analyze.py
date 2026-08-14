"""Deterministic statistical analysis for validated job-skill assertions."""

from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Assertion:
    job_id: str
    skill_id: str
    requirement_status: str


@dataclass(frozen=True)
class Prevalence:
    skill_id: str
    status: str
    numerator: int
    denominator: int
    percentage: float
    wilson_low: float
    wilson_high: float


def wilson_interval(
    successes: int, total: int, z: float = 1.959963984540054
) -> tuple[float, float]:
    if total <= 0 or not 0 <= successes <= total:
        raise ValueError(
            "Wilson inputs must satisfy 0 <= successes <= total and total > 0"
        )
    proportion = successes / total
    denominator = 1 + z * z / total
    center = (proportion + z * z / (2 * total)) / denominator
    margin = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return center - margin, center + margin


def prevalence(
    assertions: list[Assertion], usable_job_ids: set[str]
) -> list[Prevalence]:
    allowed = {"required", "preferred", "responsibility"}
    skills = sorted({row.skill_id for row in assertions})
    results: list[Prevalence] = []
    for skill_id in skills:
        rows = [
            row
            for row in assertions
            if row.skill_id == skill_id and row.job_id in usable_job_ids
        ]
        for status in ("required", "preferred", "responsibility", "combined"):
            jobs = {
                row.job_id
                for row in rows
                if row.requirement_status == status
                or (status == "combined" and row.requirement_status in allowed)
            }
            low, high = wilson_interval(len(jobs), len(usable_job_ids))
            results.append(
                Prevalence(
                    skill_id,
                    status,
                    len(jobs),
                    len(usable_job_ids),
                    round(100 * len(jobs) / len(usable_job_ids), 6),
                    round(100 * low, 6),
                    round(100 * high, 6),
                )
            )
    return results


def binary_job_skill_matrix(
    assertions: list[Assertion], job_ids: set[str]
) -> dict[str, set[str]]:
    matrix: dict[str, set[str]] = defaultdict(set)
    for row in assertions:
        if row.job_id in job_ids:
            matrix[row.job_id].add(row.skill_id)
    for job_id in job_ids:
        matrix.setdefault(job_id, set())
    return dict(sorted(matrix.items()))
