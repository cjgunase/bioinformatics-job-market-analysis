"""Conservative cached HTTP transport for public read-only job feeds."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

REDACTED_QUERY_KEYS = {"access_token", "api_key", "key", "secret", "token"}
RETRY_STATUSES = {429, 500, 502, 503, 504}
STOP_STATUSES = {401, 403}


@dataclass(frozen=True)
class HttpResponse:
    status: int
    content_type: str
    body: bytes


@dataclass(frozen=True)
class Provenance:
    retrieved_at: str
    request_url: str
    http_status: int
    content_type: str
    response_sha256: str
    attempt_count: int
    cache_hit: bool


class Transport(Protocol):
    def __call__(self, url: str, timeout_seconds: float) -> HttpResponse: ...


class SourceAccessError(RuntimeError):
    """Raised when a source must fail closed."""


def redact_url(url: str) -> str:
    parts = urlsplit(url)
    query = [
        (key, "REDACTED" if key.lower() in REDACTED_QUERY_KEYS else value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
    ]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), ""))


class CachedHttpClient:
    def __init__(
        self,
        cache_dir: Path,
        transport: Transport,
        *,
        max_attempts: int = 3,
        timeout_seconds: float = 30,
        cache_ttl_seconds: int = 86400,
        sleeper: Callable[[float], None] = time.sleep,
        now: Callable[[], float] = time.time,
    ) -> None:
        self.cache_dir = cache_dir
        self.transport = transport
        self.max_attempts = max_attempts
        self.timeout_seconds = timeout_seconds
        self.cache_ttl_seconds = cache_ttl_seconds
        self.sleeper = sleeper
        self.now = now

    def get(self, url: str, retrieved_at: str) -> tuple[HttpResponse, Provenance]:
        safe_url = redact_url(url)
        key = hashlib.sha256(safe_url.encode()).hexdigest()
        body_path = self.cache_dir / f"{key}.body"
        meta_path = self.cache_dir / f"{key}.json"
        if body_path.exists() and meta_path.exists():
            metadata = json.loads(meta_path.read_text())
            if (
                self.now() - float(metadata["cached_at_epoch"])
                <= self.cache_ttl_seconds
            ):
                body = body_path.read_bytes()
                response = HttpResponse(
                    int(metadata["http_status"]), metadata["content_type"], body
                )
                return response, Provenance(
                    retrieved_at,
                    safe_url,
                    response.status,
                    response.content_type,
                    hashlib.sha256(body).hexdigest(),
                    0,
                    True,
                )

        last_response: HttpResponse | None = None
        for attempt in range(1, self.max_attempts + 1):
            response = self.transport(url, self.timeout_seconds)
            last_response = response
            if response.status in STOP_STATUSES:
                raise SourceAccessError(f"access stopped at HTTP {response.status}")
            if response.status not in RETRY_STATUSES:
                if not 200 <= response.status < 300:
                    raise SourceAccessError(f"unexpected HTTP {response.status}")
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                body_path.write_bytes(response.body)
                metadata = {
                    "cached_at_epoch": self.now(),
                    "http_status": response.status,
                    "content_type": response.content_type,
                }
                meta_path.write_text(json.dumps(metadata, sort_keys=True) + "\n")
                provenance = Provenance(
                    retrieved_at,
                    safe_url,
                    response.status,
                    response.content_type,
                    hashlib.sha256(response.body).hexdigest(),
                    attempt,
                    False,
                )
                return response, provenance
            if attempt < self.max_attempts:
                self.sleeper(float(2 ** (attempt - 1)))
        status = last_response.status if last_response else "transport failure"
        raise SourceAccessError(f"retry budget exhausted: {status}")


def provenance_json(provenance: Provenance) -> str:
    return json.dumps(asdict(provenance), sort_keys=True)
