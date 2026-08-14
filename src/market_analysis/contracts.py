"""Source-contract checks that emit reviewable, fail-closed issue artifacts."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from market_analysis.adapters import ContractError, Posting


class SourceContractFailure(RuntimeError):
    """Parsing stopped and an issue artifact was created."""


def validate_contract(
    source: str,
    payload: bytes,
    parser: Callable[[bytes], list[Posting]],
    artifact_dir: Path,
    *,
    checked_at: str,
    request_url: str,
    http_status: int,
) -> list[Posting]:
    try:
        return parser(payload)
    except ContractError as error:
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact = {
            "issue_type": "source_contract_failure",
            "source": source,
            "checked_at": checked_at,
            "request_url": request_url,
            "http_status": http_status,
            "failure": str(error),
            "production_records_emitted": 0,
            "required_action": (
                "Review current official documentation and terms; update fixtures and "
                "adapter only through a reviewed change."
            ),
        }
        path = artifact_dir / f"{source}-contract-failure.json"
        path.write_text(json.dumps(artifact, indent=2, sort_keys=True) + "\n")
        raise SourceContractFailure(str(path)) from error
