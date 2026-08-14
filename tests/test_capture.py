from pathlib import Path

import pytest

from market_analysis.capture import capture_snapshot, normalize_source_text


def test_metadata_only_capture_does_not_write_full_text(tmp_path: Path) -> None:
    text = "Build  Python\n pipelines. Benefits follow."
    normalized = normalize_source_text(text)
    snapshot = capture_snapshot(
        text,
        excerpt_start=0,
        excerpt_end=len("Build Python pipelines."),
        retention_mode="excerpt_hash_metadata_only",
        restricted_dir=tmp_path,
        snapshot_id="job-1",
    )
    assert normalized == "Build Python pipelines. Benefits follow."
    assert snapshot.excerpt == "Build Python pipelines."
    assert snapshot.full_text_path is None
    assert list(tmp_path.iterdir()) == []


def test_restricted_capture_writes_only_to_requested_directory(tmp_path: Path) -> None:
    snapshot = capture_snapshot(
        "Use Nextflow.",
        excerpt_start=0,
        excerpt_end=13,
        retention_mode="restricted_full_snapshot",
        restricted_dir=tmp_path / "data/raw/2026-08",
        snapshot_id="job-2",
    )
    assert snapshot.full_text_path is not None
    assert Path(snapshot.full_text_path).read_text() == "Use Nextflow.\n"


def test_capture_rejects_oversized_or_invalid_excerpts(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="limit"):
        capture_snapshot(
            "x" * 600,
            excerpt_start=0,
            excerpt_end=501,
            retention_mode="excerpt_hash_metadata_only",
            restricted_dir=tmp_path,
            snapshot_id="job-3",
        )
    with pytest.raises(ValueError, match="span"):
        capture_snapshot(
            "short",
            excerpt_start=2,
            excerpt_end=99,
            retention_mode="excerpt_hash_metadata_only",
            restricted_dir=tmp_path,
            snapshot_id="job-4",
        )
