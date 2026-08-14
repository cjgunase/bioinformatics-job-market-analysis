"""Deterministic capped allocation, diversity validation, and reserves."""

from __future__ import annotations

import hashlib
import math
from collections import Counter
from dataclasses import dataclass


@dataclass(frozen=True)
class SamplingCandidate:
    canonical_job_id: str
    company_id: str
    template_fingerprint: str
    sector: str
    role_family: str
    seniority: str
    location_mode: str
    first_party: bool


@dataclass(frozen=True)
class Allocation:
    included: tuple[SamplingCandidate, ...]
    reserve: tuple[SamplingCandidate, ...]


def _rank(run_id: str, candidate: SamplingCandidate) -> str:
    return hashlib.sha256(f"{run_id}{candidate.canonical_job_id}".encode()).hexdigest()


def allocate(
    candidates: list[SamplingCandidate],
    *,
    run_id: str,
    target_n: int = 150,
    reserve_n: int = 20,
    company_cap: int = 5,
    template_cap: int = 3,
) -> Allocation:
    ordered = sorted(candidates, key=lambda item: _rank(run_id, item))
    selected: list[SamplingCandidate] = []
    companies: Counter[str] = Counter()
    templates: Counter[str] = Counter()
    sectors: Counter[str] = Counter()
    roles: Counter[str] = Counter()

    def allowed(candidate: SamplingCandidate) -> bool:
        return (
            companies[candidate.company_id] < company_cap
            and templates[candidate.template_fingerprint] < template_cap
            and sectors[candidate.sector] < math.floor(target_n * 0.30)
            and roles[candidate.role_family] < math.floor(target_n * 0.40)
        )

    def add(candidate: SamplingCandidate) -> None:
        selected.append(candidate)
        companies[candidate.company_id] += 1
        templates[candidate.template_fingerprint] += 1
        sectors[candidate.sector] += 1
        roles[candidate.role_family] += 1

    dimensions = [
        ("sector", 6),
        ("role_family", 4),
        ("seniority", 3),
        ("location_mode", 2),
    ]
    for field, minimum in dimensions:
        values = {getattr(item, field) for item in selected}
        desired = [
            value
            for value in dict.fromkeys(getattr(item, field) for item in ordered)
            if value not in values
        ]
        for value in desired:
            if len(values) >= minimum:
                break
            match = next(
                (
                    item
                    for item in ordered
                    if item not in selected
                    and getattr(item, field) == value
                    and allowed(item)
                ),
                None,
            )
            if match is not None:
                add(match)
                values.add(value)

    for item in ordered:
        if len(selected) == target_n:
            break
        if item not in selected and allowed(item):
            add(item)
    if len(selected) != target_n:
        raise ValueError(
            f"eligible pool cannot fill target: {len(selected)}/{target_n}"
        )

    remaining = [item for item in ordered if item not in selected]
    if len(remaining) < reserve_n:
        raise ValueError(f"reserve pool insufficient: {len(remaining)}/{reserve_n}")
    allocation = Allocation(tuple(selected), tuple(remaining[:reserve_n]))
    validate_diversity(allocation.included, company_cap, template_cap)
    return allocation


def validate_diversity(
    included: tuple[SamplingCandidate, ...], company_cap: int, template_cap: int
) -> None:
    count = len(included)
    if not count:
        raise ValueError("empty sample")
    companies = Counter(item.company_id for item in included)
    templates = Counter(item.template_fingerprint for item in included)
    sectors = Counter(item.sector for item in included)
    roles = Counter(item.role_family for item in included)
    seniority = {item.seniority for item in included}
    modes = {item.location_mode for item in included}
    failures = []
    if max(companies.values()) > company_cap:
        failures.append("company cap")
    if max(templates.values()) > template_cap:
        failures.append("template cap")
    if len(sectors) < 6 or max(sectors.values()) / count > 0.30:
        failures.append("sector diversity")
    if len(roles) < 4 or max(roles.values()) / count > 0.40:
        failures.append("role diversity")
    if not {"entry_associate", "mid_level", "senior_plus"} <= seniority:
        failures.append("seniority representation")
    if "remote" not in modes or not modes & {"onsite", "hybrid"}:
        failures.append("location-mode representation")
    if sum(item.first_party for item in included) / count < 0.70:
        failures.append("first-party fraction")
    if failures:
        raise ValueError("diversity gate failed: " + ", ".join(failures))
