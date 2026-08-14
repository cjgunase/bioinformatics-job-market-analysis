import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_live_contract_report_is_metadata_only_and_fail_closed() -> None:
    report = json.loads(
        (ROOT / "reports/2026-08/source_contract_validation.json").read_text()
    )
    assert report["raw_response_committed"] is False
    assert report["application_or_admin_endpoints_called"] is False
    assert report["overall_status"] == "pass_for_documented_read_only_contracts"
    assert {source["source"] for source in report["sources"]} == {
        "greenhouse",
        "lever",
        "ashby",
    }
    assert all(source["http_status"] == 200 for source in report["sources"])
    assert all(len(source["response_sha256"]) == 64 for source in report["sources"])
    assert "warning" in report["sources"][2]["contract_status"]
