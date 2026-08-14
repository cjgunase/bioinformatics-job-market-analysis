"""Versioned, strict adapters for preferred public ATS job feeds."""

from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from typing import Any

PARSER_VERSION = "1.0.0"


class ContractError(ValueError):
    """A public source no longer satisfies its declared response contract."""


@dataclass(frozen=True)
class Posting:
    source: str
    posting_id: str
    title: str
    description_text: str
    locations: tuple[str, ...]
    canonical_url: str
    compensation: str | None
    parser_version: str = PARSER_VERSION


def _object(payload: bytes) -> dict[str, Any]:
    try:
        parsed = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError("malformed JSON response") from error
    if not isinstance(parsed, dict):
        raise ContractError("expected a JSON object")
    return parsed


def html_to_text(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", value)
    return " ".join(html.unescape(without_tags).split())


def _text(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"missing required string: {key}")
    return value.strip()


def parse_greenhouse(payload: bytes) -> list[Posting]:
    document = _object(payload)
    records = document.get("jobs")
    if not isinstance(records, list):
        raise ContractError("Greenhouse response missing jobs array")
    postings: list[Posting] = []
    for raw in records:
        if not isinstance(raw, dict):
            raise ContractError("Greenhouse job is not an object")
        posting_id = raw.get("id")
        if not isinstance(posting_id, int | str):
            raise ContractError("Greenhouse job missing id")
        location = raw.get("location")
        if not isinstance(location, dict):
            raise ContractError("Greenhouse job missing location")
        location_name = _text(location, "name")
        metadata = raw.get("metadata")
        compensation = None
        if isinstance(metadata, list):
            for item in metadata:
                if isinstance(item, dict) and item.get("name") == "Compensation":
                    value = item.get("value")
                    compensation = str(value) if value is not None else None
        postings.append(
            Posting(
                source="greenhouse",
                posting_id=str(posting_id),
                title=_text(raw, "title"),
                description_text=html_to_text(_text(raw, "content")),
                locations=(location_name,),
                canonical_url=_text(raw, "absolute_url"),
                compensation=compensation,
            )
        )
    return postings
