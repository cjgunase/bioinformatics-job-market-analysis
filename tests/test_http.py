import json
from pathlib import Path

import pytest

from market_analysis.http import (
    CachedHttpClient,
    HttpResponse,
    SourceAccessError,
    redact_url,
)


def test_http_retries_caches_and_records_redacted_provenance(tmp_path: Path) -> None:
    calls: list[str] = []
    responses = iter(
        [
            HttpResponse(429, "application/json", b"{}"),
            HttpResponse(200, "application/json", b'{"jobs": []}'),
        ]
    )

    def transport(url: str, timeout_seconds: float) -> HttpResponse:
        calls.append(url)
        assert timeout_seconds == 30
        return next(responses)

    sleeps: list[float] = []
    client = CachedHttpClient(
        tmp_path,
        transport,
        sleeper=sleeps.append,
        now=lambda: 100.0,
    )
    url = "https://example.org/jobs?token=private&content=true#fragment"
    response, provenance = client.get(url, "2026-08-14T04:20:00Z")
    assert response.status == 200
    assert provenance.attempt_count == 2
    assert provenance.request_url.endswith("token=REDACTED&content=true")
    assert sleeps == [1.0]
    cached, cached_provenance = client.get(url, "2026-08-14T04:21:00Z")
    assert cached.body == response.body
    assert cached_provenance.cache_hit
    assert len(calls) == 2
    assert len(list(tmp_path.glob("*.body"))) == 1
    assert json.loads(next(tmp_path.glob("*.json")).read_text())["http_status"] == 200


@pytest.mark.parametrize("status", [401, 403])
def test_http_fails_closed_on_access_control(status: int, tmp_path: Path) -> None:
    client = CachedHttpClient(
        tmp_path,
        lambda _url, _timeout: HttpResponse(status, "text/plain", b"blocked"),
    )
    with pytest.raises(SourceAccessError, match=f"HTTP {status}"):
        client.get("https://example.org/jobs", "2026-08-14T04:20:00Z")


def test_url_redaction_removes_fragments_and_secrets() -> None:
    assert redact_url("https://e.test/x?api_key=a&q=b#x") == (
        "https://e.test/x?api_key=REDACTED&q=b"
    )
