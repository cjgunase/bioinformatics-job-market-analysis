"""Generate a traceable, explicitly noncanonical article draft."""

from __future__ import annotations

from dataclasses import dataclass

WATERMARK = "NOT HUMAN VERIFIED — DO NOT CITE"


@dataclass(frozen=True)
class DraftContext:
    run_id: str
    collection_window: str
    included_n: int
    reserve_n: int
    screened_n: int
    spec_version: str
    taxonomy_version: str
    generated_at: str
    mandatory_gates_passed: bool
    human_approved: bool


def render_draft(context: DraftContext, table_html: str = "") -> str:
    if context.human_approved:
        raise ValueError(
            "canonical publication requires the separate human sign-off flow"
        )
    status = "passed" if context.mandatory_gates_passed else "not passed"
    return f"""---
title: "Bioinformatics job market analysis — review draft"
publication_status: draft_not_human_verified
run_id: {context.run_id}
---

# {WATERMARK}

Data collection window: {context.collection_window}

## What we studied

This noncanonical review artifact contains {context.included_n} included,
{context.reserve_n} reserve, and {context.screened_n} screened records in the
U.S. frame. The structured quota sample is not a probability sample. Mandatory
publication gates are **{status}**.

## Track A — observed job-posting evidence

{table_html or "No verified result table is available."}

Required/preferred, AI-related, co-occurrence, subgroup, trend/baseline, methods,
limitations, source mix, and downloadable-data sections are generated only from
validated tables. No missing result is silently replaced with prose.

## Track B — AI capability horizon

Capability measurements, adoption evidence, forecasts, scenarios, and author
inference must remain separately labeled. Scenario probability ranges are
withheld until a human forecasting editor approves them.

## Skills for an agentic future

The review template reports code production separately from codebase
comprehension, verification, reproducibility, scientific/analytical validity,
security, provenance, maintenance/stewardship, and accountable governance.

Spec {context.spec_version}; taxonomy {context.taxonomy_version}; generated
{context.generated_at}. Corrections must use the versioned pipeline and change
log. Human manifest/article/publication approval is still required.
"""
