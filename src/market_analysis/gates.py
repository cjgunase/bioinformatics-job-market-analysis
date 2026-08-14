"""Automated privacy, copyright, accessibility, link, and provenance gates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

SECRET_PATTERNS = (
    re.compile(
        r"(?i)(api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*['\"]?[A-Za-z0-9_-]{8,}"
    ),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
)


@dataclass(frozen=True)
class GateResult:
    gate: str
    passed: bool
    detail: str


def privacy_gate(paths: list[Path]) -> GateResult:
    violations = []
    for path in paths:
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            violations.append(str(path))
    return GateResult(
        "privacy", not violations, ", ".join(violations) or "no secret patterns"
    )


def copyright_gate(
    excerpts: list[str], published_full_text_paths: list[Path]
) -> GateResult:
    failures = [
        f"excerpt {index} exceeds 500 chars"
        for index, text in enumerate(excerpts)
        if len(text) > 500
    ]
    failures.extend(str(path) for path in published_full_text_paths if path.exists())
    return GateResult(
        "copyright", not failures, "; ".join(failures) or "minimal excerpts only"
    )


def accessibility_gate(documents: list[str]) -> GateResult:
    failures = []
    for index, document in enumerate(documents):
        if "<svg" in document and not all(
            token in document for token in ('role="img"', "<title>", "<desc>")
        ):
            failures.append(f"SVG {index} lacks title/description")
        if "<table" in document and not all(
            token in document for token in ("<caption>", 'scope="col"')
        ):
            failures.append(f"table {index} lacks caption/header scope")
    return GateResult(
        "accessibility", not failures, "; ".join(failures) or "static semantics present"
    )


def link_gate(urls: list[str]) -> GateResult:
    invalid = []
    for url in urls:
        parts = urlsplit(url)
        if parts.scheme not in {"http", "https"} or not parts.netloc:
            invalid.append(url)
    return GateResult("links", not invalid, ", ".join(invalid) or "URL syntax valid")


def provenance_gate(records: list[dict[str, object]]) -> GateResult:
    required = {
        "canonical_url",
        "retrieved_at",
        "active_verified_at",
        "description_sha256",
        "source_type",
    }
    invalid = [
        str(index)
        for index, record in enumerate(records)
        if not required <= record.keys()
        or any(record.get(key) in {None, ""} for key in required)
    ]
    return GateResult(
        "provenance",
        not invalid,
        f"invalid records: {','.join(invalid)}"
        if invalid
        else "all required provenance present",
    )
