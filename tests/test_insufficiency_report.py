from pathlib import Path


def test_insufficiency_report_blocks_freeze_without_diluting_criteria() -> None:
    report = (
        Path(__file__).parents[1] / "reports/2026-08/insufficiency_report.md"
    ).read_text()
    assert "not frozen" in report
    assert "Criteria were not weakened" in report
    assert "maximum selectable pool to 80" in report
    assert "no canonical estimate" in report
    assert "human-approved reduced-sample" in report
