"""Lawful source snapshot and minimum-excerpt capture."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path

RETENTION_MODES = {
    "restricted_full_snapshot",
    "permitted_full_snapshot",
    "excerpt_hash_metadata_only",
}


@dataclass(frozen=True)
class Snapshot:
    normalized_text_sha256: str
    excerpt: str
    excerpt_sha256: str
    full_text_path: str | None
    retention_mode: str


def normalize_source_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def capture_snapshot(
    text: str,
    *,
    excerpt_start: int,
    excerpt_end: int,
    retention_mode: str,
    restricted_dir: Path,
    snapshot_id: str,
) -> Snapshot:
    if retention_mode not in RETENTION_MODES:
        raise ValueError("unknown retention mode")
    normalized = normalize_source_text(text)
    if not 0 <= excerpt_start < excerpt_end <= len(normalized):
        raise ValueError("invalid excerpt span")
    excerpt = normalized[excerpt_start:excerpt_end]
    if len(excerpt) > 500:
        raise ValueError("excerpt exceeds the audit-minimum limit")
    full_path: str | None = None
    if retention_mode in {"restricted_full_snapshot", "permitted_full_snapshot"}:
        restricted_dir.mkdir(parents=True, exist_ok=True)
        path = restricted_dir / f"{snapshot_id}.txt"
        path.write_text(normalized + "\n")
        full_path = str(path)
    return Snapshot(
        normalized_text_sha256=sha256_text(normalized),
        excerpt=excerpt,
        excerpt_sha256=sha256_text(excerpt),
        full_text_path=full_path,
        retention_mode=retention_mode,
    )
