from dataclasses import replace

import pytest

from market_analysis.screen import ScreeningFacts, screen

PASSING = ScreeningFacts(True, True, True, True, True, True, True, True)


def test_passing_candidate_is_included_but_not_human_approved() -> None:
    decision = screen(PASSING)
    assert decision.inclusion_decision == "include"
    assert decision.decision_reason_code == "include_meets_all"
    assert decision.human_review_status == "not_reviewed"


@pytest.mark.parametrize(
    ("field", "reason"),
    [
        ("active", "exclude_inactive"),
        ("complete_text", "exclude_incomplete_text"),
        ("life_science_material", "exclude_not_life_science"),
        ("engineering_material", "exclude_not_engineering"),
        ("us_eligible", "exclude_geography"),
        ("identity_complete", "exclude_source_unverifiable"),
    ],
)
def test_failed_condition_excludes(field: str, reason: str) -> None:
    decision = screen(replace(PASSING, **{field: False}))
    assert decision.inclusion_decision == "exclude"
    assert decision.decision_reason_code == reason


@pytest.mark.parametrize(
    "facts",
    [
        replace(PASSING, confidence=0.79),
        replace(PASSING, ambiguous_industry=True),
        replace(PASSING, ambiguous_geography=True),
        replace(PASSING, ambiguous_biological_materiality=True),
    ],
)
def test_borderline_candidates_route_to_human(facts: ScreeningFacts) -> None:
    decision = screen(facts)
    assert decision.inclusion_decision == "pending_human"
    assert decision.human_review_status == "pending"
