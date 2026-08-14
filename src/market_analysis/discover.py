"""Candidate discovery records with an append-only hash chain."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Discovery:
    run_id: str
    query_id: str
    exact_query: str
    source: str
    run_at_utc: str
    returned_url: str
    canonical_candidate_url: str


def _digest(record: dict[str, Any]) -> str:
    encoded = json.dumps(record, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def append_discovery(path: Path, discovery: Discovery) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_hash: str | None = None
    sequence = 1
    if path.exists():
        lines = [line for line in path.read_text().splitlines() if line]
        if lines:
            previous = json.loads(lines[-1])
            previous_hash = previous["record_hash"]
            sequence = int(previous["sequence"]) + 1
    record: dict[str, Any] = {
        **asdict(discovery),
        "sequence": sequence,
        "previous_record_hash": previous_hash,
    }
    record["record_hash"] = _digest(record)
    with path.open("a") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def validate_discovery_log(path: Path) -> int:
    expected_previous: str | None = None
    expected_sequence = 1
    for line in path.read_text().splitlines():
        record = json.loads(line)
        recorded_hash = record.pop("record_hash")
        if record["sequence"] != expected_sequence:
            raise ValueError("noncontiguous discovery sequence")
        if record["previous_record_hash"] != expected_previous:
            raise ValueError("broken discovery hash chain")
        if _digest(record) != recorded_hash:
            raise ValueError("discovery record was modified")
        expected_previous = recorded_hash
        expected_sequence += 1
    return expected_sequence - 1
