import json
from pathlib import Path

import pytest

from market_analysis.adapters import parse_greenhouse
from market_analysis.contracts import SourceContractFailure, validate_contract


def test_contract_failure_emits_issue_artifact_and_no_records(tmp_path: Path) -> None:
    with pytest.raises(SourceContractFailure) as caught:
        validate_contract(
            "greenhouse",
            b'{"changed": true}',
            parse_greenhouse,
            tmp_path,
            checked_at="2026-08-14T04:20:00Z",
            request_url="https://example.test/jobs",
            http_status=200,
        )
    artifact_path = Path(str(caught.value))
    artifact = json.loads(artifact_path.read_text())
    assert artifact["issue_type"] == "source_contract_failure"
    assert artifact["production_records_emitted"] == 0
    assert "official documentation" in artifact["required_action"]


def test_valid_contract_returns_records_without_issue(tmp_path: Path) -> None:
    postings = validate_contract(
        "greenhouse",
        b'{"jobs": []}',
        parse_greenhouse,
        tmp_path,
        checked_at="2026-08-14T04:20:00Z",
        request_url="https://example.test/jobs",
        http_status=200,
    )
    assert postings == []
    assert list(tmp_path.iterdir()) == []
