"""Single-command deterministic pipeline for validated inputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from market_analysis.analyze import Assertion, prevalence
from market_analysis.publish import DraftContext, render_draft
from market_analysis.visualize import ChartRow, accessible_bar_svg, accessible_table


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text())


def _write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError(f"refusing headerless empty CSV: {path.name}")
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def _checksums(output_dir: Path) -> str:
    lines = []
    for path in sorted(
        item
        for item in output_dir.rglob("*")
        if item.is_file() and item.name != "checksums.sha256"
    ):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.relative_to(output_dir)}")
    return "\n".join(lines) + "\n"


def run_pipeline(input_dir: Path, output_dir: Path) -> None:
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("output directory must be absent or empty for a clean run")
    output_dir.mkdir(parents=True, exist_ok=True)
    run = _load_json(input_dir / "run.json")
    jobs = _load_json(input_dir / "jobs.json")
    assertion_rows = _load_json(input_dir / "assertions.json")
    if (
        not isinstance(run, dict)
        or not isinstance(jobs, list)
        or not isinstance(assertion_rows, list)
    ):
        raise ValueError("pipeline inputs have invalid top-level types")
    usable = {
        str(job["job_id"]) for job in jobs if job.get("usable_requirement_text") is True
    }
    assertions = [Assertion(**row) for row in assertion_rows]
    prevalence_rows = [asdict(row) for row in prevalence(assertions, usable)]
    _write_csv(output_dir / "prevalence_overall.csv", prevalence_rows)
    combined = [row for row in prevalence_rows if row["status"] == "combined"]
    chart_rows = [
        ChartRow(
            str(row["skill_id"]),
            int(row["numerator"]),
            int(row["denominator"]),
            float(row["percentage"]),
        )
        for row in combined
    ]
    table = accessible_table(chart_rows, "Combined skill prevalence")
    (output_dir / "prevalence_table.html").write_text(table + "\n")
    (output_dir / "prevalence_chart.svg").write_text(
        accessible_bar_svg(chart_rows, "Skill prevalence", "Counts and percentages")
        + "\n"
    )
    context = DraftContext(
        run_id=str(run["run_id"]),
        collection_window=str(run["collection_window"]),
        included_n=int(run["included_n"]),
        reserve_n=int(run["reserve_n"]),
        screened_n=int(run["screened_n"]),
        spec_version=str(run["spec_version"]),
        taxonomy_version=str(run["taxonomy_version"]),
        generated_at=str(run["generated_at"]),
        mandatory_gates_passed=bool(run["mandatory_gates_passed"]),
        human_approved=False,
    )
    (output_dir / "article_draft.md").write_text(render_draft(context, table))
    (output_dir / "run_metadata.json").write_text(
        json.dumps(run, indent=2, sort_keys=True) + "\n"
    )
    (output_dir / "checksums.sha256").write_text(_checksums(output_dir))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    arguments = parser.parse_args()
    run_pipeline(arguments.input_dir, arguments.output_dir)


if __name__ == "__main__":
    main()
