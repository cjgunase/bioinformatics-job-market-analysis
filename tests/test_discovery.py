import json
from pathlib import Path

import pytest

from market_analysis.discover import Discovery, append_discovery, validate_discovery_log


def discovery(index: int) -> Discovery:
    return Discovery(
        run_id="2026-08_bioinfo_jobs_us_v01",
        query_id=f"q{index:03d}",
        exact_query="bioinformatics engineer",
        source="employer_board",
        run_at_utc="2026-08-14T04:20:00Z",
        returned_url=f"https://example.org/jobs/{index}",
        canonical_candidate_url=f"https://example.org/jobs/{index}",
    )


def test_discovery_log_is_append_only_and_hash_chained(tmp_path: Path) -> None:
    path = tmp_path / "screening_log.jsonl"
    first = append_discovery(path, discovery(1))
    second = append_discovery(path, discovery(2))
    assert second["previous_record_hash"] == first["record_hash"]
    assert validate_discovery_log(path) == 2


def test_discovery_log_detects_modification(tmp_path: Path) -> None:
    path = tmp_path / "screening_log.jsonl"
    append_discovery(path, discovery(1))
    record = json.loads(path.read_text())
    record["exact_query"] = "changed"
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(ValueError, match="modified"):
        validate_discovery_log(path)
