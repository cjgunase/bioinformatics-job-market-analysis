from dataclasses import replace
from pathlib import Path

import pytest

from market_analysis.extract import (
    DeterministicBulletExtractor,
    ExtractionContext,
    validate_evidence,
)

FIXTURE = Path(__file__).parent / "fixtures/extraction/job_description.txt"
CONTEXT = ExtractionContext(
    "2026-08_bioinfo_jobs_us_v01",
    "job_fixture_1",
    "https://example.test/jobs/1",
    "2026-08-14T04:20:00Z",
    "a" * 64,
)


def test_fixture_extraction_preserves_atomic_verbatim_evidence() -> None:
    text = FIXTURE.read_text()
    records = DeterministicBulletExtractor().extract(text, CONTEXT)
    assert len(records) == 3
    assert records[0].requirement_status == "responsibility"
    assert records[2].requirement_status == "preferred"
    assert text[records[0].char_start : records[0].char_end] == (
        "Build Python pipelines in AWS using Docker."
    )
    assert records[0].extractor_model is None


def test_validator_rejects_changed_span_or_hash() -> None:
    text = FIXTURE.read_text()
    record = DeterministicBulletExtractor().extract(text, CONTEXT)[0]
    with pytest.raises(ValueError, match="span mismatch"):
        validate_evidence(text, [replace(record, char_start=record.char_start + 1)])
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_evidence(text, [replace(record, excerpt_sha256="0" * 64)])
