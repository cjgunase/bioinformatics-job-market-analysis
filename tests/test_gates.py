from pathlib import Path

from market_analysis.gates import (
    accessibility_gate,
    copyright_gate,
    link_gate,
    privacy_gate,
    provenance_gate,
)
from market_analysis.visualize import ChartRow, accessible_bar_svg, accessible_table


def test_privacy_and_copyright_gates_fail_closed(tmp_path: Path) -> None:
    clean = tmp_path / "clean.txt"
    clean.write_text("derived aggregate")
    assert privacy_gate([clean]).passed
    secret = tmp_path / "bad.txt"
    secret.write_text("api_key=abcdefghijk")
    assert not privacy_gate([secret]).passed
    assert not copyright_gate(["x" * 501], []).passed
    full_text = tmp_path / "published-full.txt"
    full_text.write_text("full posting")
    assert not copyright_gate(["short"], [full_text]).passed


def test_accessibility_and_link_gates() -> None:
    rows = [ChartRow("Python", 1, 2, 50.0)]
    assert accessibility_gate(
        [
            accessible_bar_svg(rows, "Title", "Description"),
            accessible_table(rows, "Caption"),
        ]
    ).passed
    assert not accessibility_gate(["<svg></svg>"]).passed
    assert link_gate(["https://example.org/jobs/1"]).passed
    assert not link_gate(["javascript:alert(1)"]).passed


def test_provenance_requires_every_field_and_nonnull_value() -> None:
    valid: dict[str, object] = {
        "canonical_url": "https://example.org/jobs/1",
        "retrieved_at": "2026-08-14T04:20:00Z",
        "active_verified_at": "2026-08-14T04:20:00Z",
        "description_sha256": "a" * 64,
        "source_type": "employer_operated_ats",
    }
    assert provenance_gate([valid]).passed
    assert not provenance_gate([{**valid, "active_verified_at": None}]).passed
