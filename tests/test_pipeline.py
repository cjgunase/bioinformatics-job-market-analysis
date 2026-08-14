import json
from pathlib import Path

import pytest

from market_analysis.pipeline import run_pipeline


def make_inputs(path: Path) -> None:
    path.mkdir()
    run = {
        "run_id": "synthetic_v01",
        "collection_window": "synthetic fixture",
        "included_n": 2,
        "reserve_n": 0,
        "screened_n": 2,
        "spec_version": "1.1.1",
        "taxonomy_version": "1.0.0",
        "generated_at": "2026-08-14T04:20:00Z",
        "mandatory_gates_passed": False,
    }
    (path / "run.json").write_text(json.dumps(run))
    (path / "jobs.json").write_text(
        json.dumps(
            [
                {"job_id": "j1", "usable_requirement_text": True},
                {"job_id": "j2", "usable_requirement_text": True},
            ]
        )
    )
    (path / "assertions.json").write_text(
        json.dumps(
            [
                {
                    "job_id": "j1",
                    "skill_id": "python",
                    "requirement_status": "required",
                },
                {
                    "job_id": "j2",
                    "skill_id": "python",
                    "requirement_status": "preferred",
                },
            ]
        )
    )


def test_clean_runs_are_byte_reproducible(tmp_path: Path) -> None:
    inputs = tmp_path / "inputs"
    make_inputs(inputs)
    first, second = tmp_path / "first", tmp_path / "second"
    run_pipeline(inputs, first)
    run_pipeline(inputs, second)
    assert (first / "checksums.sha256").read_text() == (
        second / "checksums.sha256"
    ).read_text()
    for relative in [
        "prevalence_overall.csv",
        "article_draft.md",
        "prevalence_chart.svg",
    ]:
        assert (first / relative).read_bytes() == (second / relative).read_bytes()


def test_pipeline_refuses_dirty_output_directory(tmp_path: Path) -> None:
    inputs, output = tmp_path / "inputs", tmp_path / "output"
    make_inputs(inputs)
    output.mkdir()
    (output / "manual.csv").write_text("do not overwrite")
    with pytest.raises(ValueError, match="clean run"):
        run_pipeline(inputs, output)
