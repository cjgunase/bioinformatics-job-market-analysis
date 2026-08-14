import pytest

from market_analysis.analyze import (
    Assertion,
    benjamini_hochberg,
    clustering_distance_inputs,
    compare_groups,
    cooccurrence_pairs,
    prevalence,
    wilson_interval,
)


def test_wilson_known_value_and_bounds() -> None:
    low, high = wilson_interval(15, 150)
    assert 0 <= low < 0.10 < high <= 1
    assert low == pytest.approx(0.061541, abs=1e-6)
    assert high == pytest.approx(0.158435, abs=1e-6)


def test_prevalence_counts_each_skill_once_per_job_and_status() -> None:
    assertions = [
        Assertion("j1", "python", "required"),
        Assertion("j1", "python", "required"),
        Assertion("j1", "python", "preferred"),
        Assertion("j2", "python", "responsibility"),
        Assertion("j3", "python", "benefit_context"),
    ]
    rows = prevalence(assertions, {"j1", "j2", "j3"})
    combined = next(row for row in rows if row.status == "combined")
    required = next(row for row in rows if row.status == "required")
    assert combined.numerator == 2
    assert required.numerator == 1
    assert combined.denominator == 3


@pytest.mark.parametrize("successes,total", [(-1, 1), (2, 1), (0, 0)])
def test_wilson_rejects_invalid_inputs(successes: int, total: int) -> None:
    with pytest.raises(ValueError):
        wilson_interval(successes, total)


def test_stratified_comparison_suppresses_small_groups_and_reports_effects() -> None:
    assert compare_groups("small", 2, 14, 5, 20) is None
    result = compare_groups("role_a_vs_b", 12, 30, 6, 30)
    assert result is not None
    assert result.percentage_point_difference == 20.0
    assert result.prevalence_ratio == 2.0
    assert result.test in {"fisher_exact_two_sided", "chi_square_1df"}


def test_benjamini_hochberg_is_monotone_in_p_order() -> None:
    comparisons = [
        compare_groups("a", 18, 30, 3, 30),
        compare_groups("b", 15, 30, 5, 30),
        compare_groups("c", 12, 30, 6, 30),
    ]
    adjusted = benjamini_hochberg([row for row in comparisons if row is not None])
    ordered = sorted(adjusted, key=lambda row: row.p_value)
    assert all(row.q_value is not None for row in ordered)
    q_values = [row.q_value or 0.0 for row in ordered]
    assert q_values == sorted(q_values)


def test_cooccurrence_metrics_support_gate_and_clustering_inputs() -> None:
    matrix = {
        f"j{index}": (
            {"python", "docker", "nextflow"} if index < 5 else {"python", "sql"}
        )
        for index in range(10)
    }
    pairs = cooccurrence_pairs(matrix)
    assert [(row.skill_a, row.skill_b) for row in pairs] == [
        ("docker", "nextflow"),
        ("docker", "python"),
        ("nextflow", "python"),
        ("python", "sql"),
    ]
    docker_nextflow = pairs[0]
    assert docker_nextflow.support == 5
    assert docker_nextflow.jaccard == 1.0
    distances = clustering_distance_inputs(pairs, ["docker", "nextflow", "sql"])
    assert distances[0][0] == 0
    assert distances[0][1] == 0
    assert distances[0][2] == 1
