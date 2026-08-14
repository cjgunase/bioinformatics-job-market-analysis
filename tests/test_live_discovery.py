import csv
import json
from pathlib import Path

import pytest

from market_analysis.live import build_discovery_increment


def test_live_discovery_exports_metadata_only_hash_chained_events(
    tmp_path: Path,
) -> None:
    registry = tmp_path / "employers.csv"
    fields = [
        "employer_id",
        "company_name_normalized",
        "ats_system",
        "board_identifier",
        "public_board_url",
        "active",
    ]
    with registry.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(
            {
                "employer_id": "emp_test",
                "company_name_normalized": "Test Bio",
                "ats_system": "greenhouse",
                "board_identifier": "test",
                "public_board_url": "https://example.test/jobs",
                "active": "true",
            }
        )
    response = {
        "jobs": [
            {
                "id": 1,
                "title": "Bioinformatics Engineer",
                "content": "<p>Restricted full description</p>",
                "location": {"name": "US"},
                "absolute_url": "https://example.test/jobs/1",
            }
        ]
    }
    (tmp_path / "greenhouse-test.json").write_text(json.dumps(response))
    output = tmp_path / "screening_log.jsonl"
    count = build_discovery_increment(
        registry,
        tmp_path,
        output,
        run_id="run",
        retrieved_at="2026-08-14T04:53:03Z",
    )
    assert count == 1
    event = json.loads(output.read_text())
    assert event["title_raw"] == "Bioinformatics Engineer"
    assert "description" not in event
    assert "Restricted full description" not in output.read_text()
    with pytest.raises(ValueError, match="append-only"):
        build_discovery_increment(
            registry,
            tmp_path,
            output,
            run_id="run",
            retrieved_at="2026-08-14T04:53:03Z",
        )
