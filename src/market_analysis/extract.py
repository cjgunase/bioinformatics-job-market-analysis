"""Pass-A atomic evidence extraction interfaces and deterministic fixtures."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ExtractionContext:
    run_id: str
    job_id: str
    source_url: str
    retrieved_at: str
    snapshot_sha256: str


@dataclass(frozen=True)
class AtomicEvidence:
    evidence_id: str
    job_id: str
    source_url: str
    retrieved_at: str
    source_section: str
    paragraph_or_bullet_index: int
    char_start: int
    char_end: int
    verbatim_excerpt: str
    excerpt_sha256: str
    snapshot_sha256: str
    requirement_text_normalized: str
    requirement_status: str
    extraction_method: str
    extractor_model: str | None
    prompt_version: str
    confidence: float


class EvidenceExtractor(Protocol):
    def extract(
        self, text: str, context: ExtractionContext
    ) -> list[AtomicEvidence]: ...


class DeterministicBulletExtractor:
    """Fixture/reference extractor; production semantic extraction may be AI-assisted."""

    def __init__(self, prompt_version: str = "extraction_v01") -> None:
        self.prompt_version = prompt_version

    def extract(self, text: str, context: ExtractionContext) -> list[AtomicEvidence]:
        evidence: list[AtomicEvidence] = []
        cursor = 0
        bullet_index = 0
        section = "unclear"
        for line in text.splitlines(keepends=True):
            stripped = line.strip()
            lowered = stripped.lower().rstrip(":")
            if lowered in {"requirements", "preferred", "responsibilities"}:
                section = lowered
            elif stripped.startswith(("- ", "* ")):
                excerpt = stripped[2:].strip()
                start = text.find(excerpt, cursor)
                end = start + len(excerpt)
                status = {
                    "requirements": "required",
                    "preferred": "preferred",
                    "responsibilities": "responsibility",
                }.get(section, "unclear")
                digest = hashlib.sha256(excerpt.encode()).hexdigest()
                evidence.append(
                    AtomicEvidence(
                        evidence_id=f"ev_{context.job_id}_{bullet_index:03d}",
                        job_id=context.job_id,
                        source_url=context.source_url,
                        retrieved_at=context.retrieved_at,
                        source_section=section,
                        paragraph_or_bullet_index=bullet_index,
                        char_start=start,
                        char_end=end,
                        verbatim_excerpt=excerpt,
                        excerpt_sha256=digest,
                        snapshot_sha256=context.snapshot_sha256,
                        requirement_text_normalized=" ".join(excerpt.split()),
                        requirement_status=status,
                        extraction_method="deterministic_fixture",
                        extractor_model=None,
                        prompt_version=self.prompt_version,
                        confidence=1.0 if status != "unclear" else 0.75,
                    )
                )
                bullet_index += 1
            cursor += len(line)
        validate_evidence(text, evidence)
        return evidence


def validate_evidence(text: str, records: list[AtomicEvidence]) -> None:
    for record in records:
        if text[record.char_start : record.char_end] != record.verbatim_excerpt:
            raise ValueError(f"evidence span mismatch: {record.evidence_id}")
        digest = hashlib.sha256(record.verbatim_excerpt.encode()).hexdigest()
        if digest != record.excerpt_sha256:
            raise ValueError(f"evidence hash mismatch: {record.evidence_id}")
        if not 0 <= record.confidence <= 1:
            raise ValueError(f"invalid confidence: {record.evidence_id}")
