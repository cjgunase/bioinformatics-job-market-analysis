"""Create metadata-only screening events from explicitly retrieved board responses."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from market_analysis.adapters import parse_ashby, parse_greenhouse, parse_lever
from market_analysis.discover import Discovery, append_discovery, validate_discovery_log


def _response_path(response_dir: Path, system: str, identifier: str) -> Path:
    safe_identifier = identifier.replace(" ", "_")
    return response_dir / f"{system}-{safe_identifier}.json"


def build_discovery_increment(
    registry_path: Path,
    response_dir: Path,
    output_path: Path,
    *,
    run_id: str,
    retrieved_at: str,
    append: bool = False,
    employer_ids: set[str] | None = None,
) -> int:
    if output_path.exists() and not append:
        raise ValueError(
            "screening discovery log is append-only; output already exists"
        )
    parsers = {
        "greenhouse": parse_greenhouse,
        "lever": parse_lever,
        "ashby": parse_ashby,
    }
    seen_urls: set[str] = set()
    if output_path.exists():
        seen_urls = {
            str(json.loads(line)["canonical_candidate_url"])
            for line in output_path.read_text().splitlines()
            if line
        }
    appended = 0
    with registry_path.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        if row["active"] != "true" or (
            employer_ids is not None and row["employer_id"] not in employer_ids
        ):
            continue
        system = row["ats_system"]
        path = _response_path(response_dir, system, row["board_identifier"])
        if not path.exists():
            raise ValueError(f"missing retrieved response for {row['employer_id']}")
        payload = path.read_bytes()
        response_hash = hashlib.sha256(payload).hexdigest()
        postings = parsers[system](payload)
        for posting in postings:
            if posting.canonical_url in seen_urls:
                continue
            seen_urls.add(posting.canonical_url)
            append_discovery(
                output_path,
                Discovery(
                    run_id=run_id,
                    query_id="registry_refresh",
                    exact_query="active employer board refresh",
                    source=system,
                    run_at_utc=retrieved_at,
                    returned_url=row["public_board_url"],
                    canonical_candidate_url=posting.canonical_url,
                    employer_id=row["employer_id"],
                    company_name_normalized=row["company_name_normalized"],
                    title_raw=posting.title,
                    source_response_sha256=response_hash,
                ),
            )
            appended += 1
    validate_discovery_log(output_path)
    return appended
