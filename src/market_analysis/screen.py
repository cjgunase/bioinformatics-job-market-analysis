"""Deterministic eligibility screening with conservative review routing."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScreeningFacts:
    industry: bool
    active: bool
    complete_text: bool
    life_science_material: bool
    engineering_material: bool
    us_eligible: bool
    paid_allowed_employment: bool
    identity_complete: bool
    excluded_academic: bool = False
    excluded_internship: bool = False
    confidence: float = 1.0
    ambiguous_industry: bool = False
    ambiguous_geography: bool = False
    ambiguous_biological_materiality: bool = False


@dataclass(frozen=True)
class ScreeningDecision:
    inclusion_decision: str
    decision_reason_code: str
    rationale: str
    human_review_status: str


def screen(facts: ScreeningFacts) -> ScreeningDecision:
    exclusions = [
        (facts.excluded_academic, "exclude_academic", "Academic role"),
        (facts.excluded_internship, "exclude_internship", "Internship role"),
        (not facts.industry, "exclude_not_life_science", "Not an industry role"),
        (not facts.active, "exclude_inactive", "Not verified active"),
        (not facts.complete_text, "exclude_incomplete_text", "Text incomplete"),
        (
            not facts.life_science_material,
            "exclude_not_life_science",
            "Life-science context not material",
        ),
        (
            not facts.engineering_material,
            "exclude_not_engineering",
            "Engineering content not material",
        ),
        (
            not facts.us_eligible,
            "exclude_geography",
            "U.S. eligibility not established",
        ),
        (
            not facts.paid_allowed_employment,
            "exclude_not_engineering",
            "Employment type is outside scope",
        ),
        (
            not facts.identity_complete,
            "exclude_source_unverifiable",
            "Identity metadata is insufficient",
        ),
    ]
    for failed, code, rationale in exclusions:
        if failed:
            return ScreeningDecision("exclude", code, rationale, "not_reviewed")

    borderline = (
        facts.confidence < 0.80
        or facts.ambiguous_industry
        or facts.ambiguous_geography
        or facts.ambiguous_biological_materiality
    )
    if borderline:
        return ScreeningDecision(
            "pending_human",
            "pending_human",
            "All deterministic criteria pass, but a specified ambiguity requires a human.",
            "pending",
        )
    return ScreeningDecision(
        "include",
        "include_meets_all",
        "All specification 1.1.1 inclusion conditions pass.",
        "not_reviewed",
    )
