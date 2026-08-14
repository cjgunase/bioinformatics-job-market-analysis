import random

import pytest

from market_analysis.sample import SamplingCandidate, allocate


def pool() -> list[SamplingCandidate]:
    sectors = [f"sector_{index}" for index in range(7)]
    roles = [f"role_{index}" for index in range(5)]
    seniority = ["entry_associate", "mid_level", "senior_plus"]
    modes = ["onsite", "hybrid", "remote"]
    return [
        SamplingCandidate(
            canonical_job_id=f"job_{index:03d}",
            company_id=f"company_{index // 3:03d}",
            template_fingerprint=f"template_{index // 2:03d}",
            sector=sectors[index % len(sectors)],
            role_family=roles[index % len(roles)],
            seniority=seniority[index % len(seniority)],
            location_mode=modes[index % len(modes)],
            first_party=index % 5 != 0,
        )
        for index in range(240)
    ]


def test_allocation_is_deterministic_capped_and_has_reserves() -> None:
    candidates = pool()
    first = allocate(candidates, run_id="run", target_n=150)
    random.Random(42).shuffle(candidates)
    second = allocate(candidates, run_id="run", target_n=150)
    assert [item.canonical_job_id for item in first.included] == [
        item.canonical_job_id for item in second.included
    ]
    assert len(first.included) == 150
    assert len(first.reserve) == 20


def test_allocation_fails_closed_when_target_or_reserve_is_impossible() -> None:
    with pytest.raises(ValueError, match=r"target|reserve"):
        allocate(pool()[:25], run_id="run", target_n=20, reserve_n=20)
