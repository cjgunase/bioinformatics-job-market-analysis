"""Accessible static tables and charts generated from result rows."""

from __future__ import annotations

import html
from dataclasses import dataclass


@dataclass(frozen=True)
class ChartRow:
    label: str
    numerator: int
    denominator: int
    percentage: float


def accessible_table(rows: list[ChartRow], caption: str) -> str:
    body = "".join(
        "<tr>"
        f'<th scope="row">{html.escape(row.label)}</th>'
        f"<td>{row.numerator}</td><td>{row.denominator}</td>"
        f"<td>{row.percentage:.1f}%</td></tr>"
        for row in rows
    )
    return (
        f"<table><caption>{html.escape(caption)}</caption>"
        '<thead><tr><th scope="col">Skill</th><th scope="col">Jobs</th>'
        '<th scope="col">Denominator</th><th scope="col">Percent</th>'
        f"</tr></thead><tbody>{body}</tbody></table>"
    )


def accessible_bar_svg(rows: list[ChartRow], title: str, description: str) -> str:
    width = 800
    row_height = 48
    height = 80 + row_height * len(rows)
    bars = []
    for index, row in enumerate(rows):
        y = 60 + index * row_height
        bar_width = max(0.0, min(600.0, 6 * row.percentage))
        bars.append(
            f'<text x="10" y="{y + 17}" fill="#111">{html.escape(row.label)}</text>'
            f'<rect x="180" y="{y}" width="{bar_width:.1f}" height="24" fill="#0072B2"/>'
            f'<text x="{190 + bar_width:.1f}" y="{y + 17}" fill="#111">'
            f"{row.numerator}/{row.denominator} ({row.percentage:.1f}%)</text>"
        )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" width="{width}" '
        f'height="{height}" viewBox="0 0 {width} {height}">'
        f"<title>{html.escape(title)}</title><desc>{html.escape(description)}</desc>"
        '<rect width="100%" height="100%" fill="#fff"/>' + "".join(bars) + "</svg>"
    )
