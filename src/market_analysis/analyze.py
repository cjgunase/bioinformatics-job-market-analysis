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


@dataclass(frozen=True)
class Comparison:
    comparison_id: str
    group_a_numerator: int
    group_a_denominator: int
    group_b_numerator: int
    group_b_denominator: int
    percentage_point_difference: float
    prevalence_ratio: float | None
    test: str
    p_value: float
    q_value: float | None = None


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


def _hypergeometric_probability(a: int, b: int, c: int, d: int) -> float:
    return math.comb(a + b, a) * math.comb(c + d, c) / math.comb(a + b + c + d, a + c)


def _fisher_two_sided(a: int, b: int, c: int, d: int) -> float:
    observed = _hypergeometric_probability(a, b, c, d)
    row_a, row_b, col_a = a + b, c + d, a + c
    lower = max(0, col_a - row_b)
    upper = min(row_a, col_a)
    probabilities = [
        _hypergeometric_probability(x, row_a - x, col_a - x, row_b - col_a + x)
        for x in range(lower, upper + 1)
    ]
    return min(1.0, sum(value for value in probabilities if value <= observed + 1e-12))


def compare_groups(
    comparison_id: str,
    group_a_success: int,
    group_a_total: int,
    group_b_success: int,
    group_b_total: int,
    *,
    subgroup_min_n: int = 15,
) -> Comparison | None:
    if min(group_a_total, group_b_total) < subgroup_min_n:
        return None
    a, b = group_a_success, group_a_total - group_a_success
    c, d = group_b_success, group_b_total - group_b_success
    if min(a, b, c, d) < 0:
        raise ValueError("invalid 2x2 counts")
    expected = [
        (a + b) * (a + c) / (a + b + c + d),
        (a + b) * (b + d) / (a + b + c + d),
        (c + d) * (a + c) / (a + b + c + d),
        (c + d) * (b + d) / (a + b + c + d),
    ]
    if min(expected) < 5:
        test = "fisher_exact_two_sided"
        p_value = _fisher_two_sided(a, b, c, d)
    else:
        test = "chi_square_1df"
        total = a + b + c + d
        numerator = total * (a * d - b * c) ** 2
        denominator = (a + b) * (c + d) * (a + c) * (b + d)
        chi_square = numerator / denominator if denominator else 0.0
        p_value = math.erfc(math.sqrt(chi_square / 2))
    rate_a = group_a_success / group_a_total
    rate_b = group_b_success / group_b_total
    return Comparison(
        comparison_id,
        group_a_success,
        group_a_total,
        group_b_success,
        group_b_total,
        round(100 * (rate_a - rate_b), 6),
        round(rate_a / rate_b, 6) if rate_b else None,
        test,
        p_value,
    )


def benjamini_hochberg(comparisons: list[Comparison]) -> list[Comparison]:
    ordered = sorted(enumerate(comparisons), key=lambda pair: pair[1].p_value)
    adjusted = [1.0] * len(comparisons)
    running = 1.0
    for rank_index in range(len(ordered) - 1, -1, -1):
        original_index, comparison = ordered[rank_index]
        rank = rank_index + 1
        running = min(running, comparison.p_value * len(comparisons) / rank)
        adjusted[original_index] = min(1.0, running)
    return [
        Comparison(**{**row.__dict__, "q_value": adjusted[index]})
        for index, row in enumerate(comparisons)
    ]
