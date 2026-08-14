import json

import pytest

from market_analysis.adapters import ContractError, parse_ashby


def payload(**overrides: object) -> bytes:
    job: dict[str, object] = {
        "id": "ashby-7",
        "title": "Scientific Software Engineer",
        "descriptionHtml": "<p>Build <em>reproducible</em> tools.</p>",
        "location": "Cambridge, MA",
        "secondaryLocations": [{"location": "Seattle, WA"}],
        "isRemote": True,
        "jobUrl": "https://jobs.ashbyhq.com/example/ashby-7",
        "compensation": {"summary": "$120k-$150k"},
    }
    job.update(overrides)
    return json.dumps({"jobs": [job]}).encode()


def test_ashby_parses_locations_remote_html_and_compensation() -> None:
    posting = parse_ashby(payload())[0]
    assert posting.posting_id == "ashby-7"
    assert posting.description_text == "Build reproducible tools."
    assert posting.locations == ("Cambridge, MA", "Seattle, WA", "Remote")
    assert "$120k-$150k" in (posting.compensation or "")


def test_ashby_prefers_plain_description() -> None:
    body = payload(descriptionPlain="Implement validated workflows.")
    assert parse_ashby(body)[0].description_text == "Implement validated workflows."


@pytest.mark.parametrize("broken", [b"no", b"[]", b"{}", b'{"jobs":[null]}'])
def test_ashby_rejects_malformed_contracts(broken: bytes) -> None:
    with pytest.raises(ContractError):
        parse_ashby(broken)


def test_ashby_empty_board_represents_no_published_jobs() -> None:
    assert parse_ashby(b'{"jobs": []}') == []
