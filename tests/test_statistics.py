import pytest

from market_analysis.analyze import Assertion, prevalence, wilson_interval


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
