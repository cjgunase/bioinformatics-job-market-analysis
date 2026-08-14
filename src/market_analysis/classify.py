"""Pass-B taxonomy mapping, confidence gates, and within-job collapse."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from market_analysis.extract import AtomicEvidence


@dataclass(frozen=True)
class SkillMapping:
    job_id: str
    taxonomy_category_id: str
    taxonomy_skill_id: str
    evidence_ids: tuple[str, ...]
    requirement_statuses: tuple[str, ...]
    confidence: float
    ai_relation: str
    quantitative_eligible: bool
    human_review_status: str


def load_taxonomy(path: Path) -> list[dict[str, Any]]:
    document = yaml.safe_load(path.read_text())
    if document.get("taxonomy_version") != "1.0.0":
        raise ValueError("unsupported taxonomy version")
    return list(document["skills"])


def _explicit_alias_match(text: str, values: list[str]) -> bool:
    for value in sorted(values, key=len, reverse=True):
        pattern = rf"(?<![A-Za-z0-9]){re.escape(value)}(?![A-Za-z0-9])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    return False


def _ai_relation(skill: dict[str, Any]) -> str:
    if not skill.get("is_ai_related"):
        return "none"
    skill_id = str(skill["skill_id"])
    if "agent" in skill_id or "orchestration" in skill_id:
        return "ai_agents_or_orchestration"
    if any(term in skill_id for term in ("evaluation", "safety", "governance")):
        return "ai_evaluation_safety"
    if any(term in skill_id for term in ("llm", "generative", "foundation")):
        return "generative_ai_llm"
    if "assisted" in skill_id or "coding" in skill_id:
        return "ai_assisted_development"
    return "ai_ml_engineering"


def map_evidence(
    evidence: list[AtomicEvidence], taxonomy: list[dict[str, Any]]
) -> list[SkillMapping]:
    raw: list[SkillMapping] = []
    for item in evidence:
        for skill in taxonomy:
            aliases = [
                str(skill["preferred_label"]),
                str(skill["skill_id"]).replace("_", " "),
                *[str(alias) for alias in skill.get("aliases", [])],
            ]
            if not _explicit_alias_match(item.verbatim_excerpt, aliases):
                continue
            confidence = item.confidence
            ai_relation = _ai_relation(skill)
            review = (
                "pending"
                if confidence < 0.80 or ai_relation != "none"
                else "not_reviewed"
            )
            raw.append(
                SkillMapping(
                    job_id=item.job_id,
                    taxonomy_category_id=str(skill["category_id"]),
                    taxonomy_skill_id=str(skill["skill_id"]),
                    evidence_ids=(item.evidence_id,),
                    requirement_statuses=(item.requirement_status,),
                    confidence=confidence,
                    ai_relation=ai_relation,
                    quantitative_eligible=confidence >= 0.60,
                    human_review_status=review,
                )
            )
    return collapse_within_job(raw)


def collapse_within_job(mappings: list[SkillMapping]) -> list[SkillMapping]:
    grouped: dict[tuple[str, str], list[SkillMapping]] = {}
    for mapping in mappings:
        grouped.setdefault((mapping.job_id, mapping.taxonomy_skill_id), []).append(
            mapping
        )
    collapsed = []
    for key in sorted(grouped):
        rows = grouped[key]
        collapsed.append(
            SkillMapping(
                job_id=rows[0].job_id,
                taxonomy_category_id=rows[0].taxonomy_category_id,
                taxonomy_skill_id=rows[0].taxonomy_skill_id,
                evidence_ids=tuple(
                    dict.fromkeys(
                        evidence for row in rows for evidence in row.evidence_ids
                    )
                ),
                requirement_statuses=tuple(
                    dict.fromkeys(
                        status for row in rows for status in row.requirement_statuses
                    )
                ),
                confidence=max(row.confidence for row in rows),
                ai_relation=rows[0].ai_relation,
                quantitative_eligible=any(row.quantitative_eligible for row in rows),
                human_review_status=(
                    "pending"
                    if any(row.human_review_status == "pending" for row in rows)
                    else "not_reviewed"
                ),
            )
        )
    return collapsed
