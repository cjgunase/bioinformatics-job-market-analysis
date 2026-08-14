from dataclasses import replace

from market_analysis.publish import WATERMARK, DraftContext, render_draft
from market_analysis.visualize import ChartRow, accessible_bar_svg, accessible_table

ROWS = [ChartRow("Python", 75, 150, 50.0), ChartRow("Docker", 30, 150, 20.0)]


def test_table_has_caption_scopes_and_exact_data() -> None:
    table = accessible_table(ROWS, "Synthetic fixture prevalence")
    assert "<caption>Synthetic fixture prevalence</caption>" in table
    assert 'scope="col"' in table
    assert "75</td><td>150</td><td>50.0%" in table


def test_svg_has_text_alternatives_direct_labels_and_safe_color() -> None:
    svg = accessible_bar_svg(ROWS, "Fixture skills", "Synthetic data only")
    assert 'role="img"' in svg
    assert "<title>Fixture skills</title>" in svg
    assert "<desc>Synthetic data only</desc>" in svg
    assert "75/150 (50.0%)" in svg
    assert "#0072B2" in svg


def test_draft_is_watermarked_and_refuses_self_approval() -> None:
    context = DraftContext(
        "2026-08_bioinfo_jobs_us_v01",
        "not opened",
        0,
        0,
        0,
        "1.1.1",
        "1.0.0",
        "2026-08-14T04:20:00Z",
        False,
        False,
    )
    draft = render_draft(context)
    assert WATERMARK in draft
    assert "No verified result table is available" in draft
    try:
        render_draft(replace(context, human_approved=True))
    except ValueError as error:
        assert "human sign-off" in str(error)
    else:
        raise AssertionError("self-approved draft was accepted")
