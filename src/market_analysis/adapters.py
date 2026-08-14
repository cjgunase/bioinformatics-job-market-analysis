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


def parse_lever(payload: bytes) -> list[Posting]:
    try:
        records = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ContractError("malformed JSON response") from error
    if not isinstance(records, list):
        raise ContractError("Lever response must be an array")
    postings: list[Posting] = []
    for raw in records:
        if not isinstance(raw, dict):
            raise ContractError("Lever posting is not an object")
        categories = raw.get("categories")
        if not isinstance(categories, dict):
            raise ContractError("Lever posting missing categories")
        raw_locations = categories.get("allLocations")
        if isinstance(raw_locations, list) and raw_locations:
            locations = tuple(str(item).strip() for item in raw_locations if str(item))
        elif not categories.get("location"):
            locations = ()
        else:
            locations = (_text(categories, "location"),)
        description = raw.get("descriptionPlain") or raw.get("description")
        if description is None:
            description = ""
        if not isinstance(description, str):
            raise ContractError("Lever description has invalid type")
        salary = raw.get("salaryRange")
        compensation = (
            json.dumps(salary, sort_keys=True) if salary is not None else None
        )
        postings.append(
            Posting(
                source="lever",
                posting_id=_text(raw, "id"),
                title=_text(raw, "text"),
                description_text=html_to_text(description),
                locations=locations,
                canonical_url=_text(raw, "hostedUrl"),
                compensation=compensation,
            )
        )
    return postings


def parse_ashby(payload: bytes) -> list[Posting]:
    document = _object(payload)
    records = document.get("jobs")
    if not isinstance(records, list):
        raise ContractError("Ashby response missing jobs array")
    postings: list[Posting] = []
    for raw in records:
        if not isinstance(raw, dict):
            raise ContractError("Ashby job is not an object")
        description = raw.get("descriptionPlain") or raw.get("descriptionHtml")
        if not isinstance(description, str) or not description.strip():
            raise ContractError("missing required string: description")
        locations: list[str] = [_text(raw, "location")]
        secondary = raw.get("secondaryLocations")
        if isinstance(secondary, list):
            for item in secondary:
                if isinstance(item, dict):
                    locations.append(_text(item, "location"))
        if raw.get("isRemote") is True and "Remote" not in locations:
            locations.append("Remote")
        compensation = raw.get("compensation")
        postings.append(
            Posting(
                source="ashby",
                posting_id=_text(raw, "id"),
                title=_text(raw, "title"),
                description_text=html_to_text(description),
                locations=tuple(dict.fromkeys(locations)),
                canonical_url=_text(raw, "jobUrl"),
                compensation=(
                    json.dumps(compensation, sort_keys=True)
                    if compensation is not None
                    else None
                ),
            )
        )
    return postings
