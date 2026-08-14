"""Deterministic canonicalization and duplicate candidate generation."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_KEYS = {"fbclid", "gclid", "ref", "source", "trk"}


@dataclass(frozen=True)
class DedupRecord:
    job_id: str
    company_domain: str
    company_name: str
    title: str
    location_group: str
    canonical_url: str
    requisition_id: str | None
    normalized_text_sha256: str
    comparison_text: str


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url)
    query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_KEYS and not key.lower().startswith("utm_")
    ]
    return urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            urlencode(query),
            "",
        )
    )


def normalize_label(value: str) -> str:
    return " ".join(re.sub(r"[^a-z0-9+]+", " ", value.lower()).split())


def canonical_job_id(record: DedupRecord) -> str:
    if record.requisition_id:
        basis = (
            f"{record.company_domain.lower()}|{record.requisition_id.strip().lower()}"
        )
    else:
        basis = "|".join(
            [
                record.company_domain.lower(),
                normalize_label(record.title),
                normalize_label(record.location_group),
                record.normalized_text_sha256,
            ]
        )
    return "job_" + hashlib.sha256(basis.encode()).hexdigest()[:20]


def exact_duplicate_groups(records: list[DedupRecord]) -> list[tuple[str, ...]]:
    keys: dict[tuple[str, str], list[str]] = {}
    for record in records:
        candidates = {
            ("url", canonicalize_url(record.canonical_url)),
            ("text", record.normalized_text_sha256),
        }
        if record.requisition_id:
            candidates.add(
                (
                    "requisition",
                    f"{record.company_domain.lower()}|{record.requisition_id.lower()}",
                )
            )
        for key in candidates:
            keys.setdefault(key, []).append(record.job_id)
    groups = {tuple(sorted(ids)) for ids in keys.values() if len(set(ids)) > 1}
    return sorted(groups)
