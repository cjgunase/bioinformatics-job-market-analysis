import json

import pytest

from market_analysis.adapters import ContractError, parse_greenhouse


def payload(**overrides: object) -> bytes:
    job: dict[str, object] = {
        "id": 42,
        "title": "Bioinformatics Engineer",
        "content": "<p>Build &amp; test <strong>Python</strong> pipelines.</p>",
        "location": {"name": "Boston, MA"},
        "absolute_url": "https://boards.greenhouse.io/example/jobs/42",
        "metadata": [{"name": "Compensation", "value": "$100k-$120k"}],
    }
    job.update(overrides)
    return json.dumps({"jobs": [job]}).encode()


def test_greenhouse_parses_html_location_and_compensation() -> None:
    posting = parse_greenhouse(payload())[0]
    assert posting.posting_id == "42"
    assert posting.description_text == "Build & test Python pipelines."
    assert posting.locations == ("Boston, MA",)
    assert posting.compensation == "$100k-$120k"


@pytest.mark.parametrize("broken", [b"not-json", b"[]", b"{}"])
def test_greenhouse_rejects_malformed_contracts(broken: bytes) -> None:
    with pytest.raises(ContractError):
        parse_greenhouse(broken)


def test_greenhouse_rejects_missing_fields() -> None:
    with pytest.raises(ContractError, match="content"):
        parse_greenhouse(payload(content=None))


def test_greenhouse_allows_empty_board_for_removed_jobs() -> None:
    assert parse_greenhouse(b'{"jobs": []}') == []
