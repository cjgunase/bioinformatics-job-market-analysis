import json

import pytest

from market_analysis.adapters import ContractError, parse_lever


def payload(**overrides: object) -> bytes:
    posting: dict[str, object] = {
        "id": "abc-123",
        "text": "Computational Biologist",
        "description": "<div>Develop <b>Python</b> workflows.</div>",
        "categories": {
            "location": "New York, NY",
            "allLocations": ["New York, NY", "Remote - US"],
        },
        "hostedUrl": "https://jobs.lever.co/example/abc-123",
        "salaryRange": {"min": 100000, "max": 130000, "currency": "USD"},
    }
    posting.update(overrides)
    return json.dumps([posting]).encode()


def test_lever_parses_multiple_locations_html_and_compensation() -> None:
    posting = parse_lever(payload())[0]
    assert posting.posting_id == "abc-123"
    assert posting.description_text == "Develop Python workflows."
    assert posting.locations == ("New York, NY", "Remote - US")
    assert '"currency": "USD"' in (posting.compensation or "")


def test_lever_supports_plain_description_and_single_location() -> None:
    body = payload(
        description=None,
        descriptionPlain="Write tested software.",
        categories={"location": "San Diego, CA"},
    )
    assert parse_lever(body)[0].locations == ("San Diego, CA",)


@pytest.mark.parametrize("broken", [b"not-json", b"{}", b"[null]"])
def test_lever_rejects_malformed_contracts(broken: bytes) -> None:
    with pytest.raises(ContractError):
        parse_lever(broken)


def test_lever_empty_array_represents_no_published_jobs() -> None:
    assert parse_lever(b"[]") == []
