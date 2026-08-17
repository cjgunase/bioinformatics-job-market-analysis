"""Private candidate-to-opening ranking, separate from the market study."""

from __future__ import annotations

import argparse
import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

from market_analysis.adapters import Posting, parse_ashby, parse_greenhouse, parse_lever

PARSERS = {
    "ashby": parse_ashby,
    "greenhouse": parse_greenhouse,
    "lever": parse_lever,
}


@dataclass(frozen=True)
class RankedOpening:
    rank: int
    score: int
    employer: str
    title: str
    locations: tuple[str, ...]
    url: str
    salary_status: str
    salary_max_usd: int | None
    matched_lanes: tuple[str, ...]
    matched_terms: tuple[str, ...]


def _annual_salary_max(value: str | None) -> int | None:
    if not value:
        return None
    lowered = value.lower()
    try:
        structured = json.loads(value)
    except json.JSONDecodeError:
        structured = None
    structured_maxima: list[float] = []

    def collect_salary_maxima(item: Any) -> None:
        if isinstance(item, dict):
            compensation_type = str(item.get("compensationType", "")).lower()
            currency = str(item.get("currencyCode", item.get("currency", ""))).upper()
            interval = str(item.get("interval", "")).lower()
            maximum = item.get("maxValue", item.get("max"))
            if (
                isinstance(maximum, int | float)
                and compensation_type in {"", "salary"}
                and currency in {"", "USD"}
            ):
                annual = float(maximum)
                if "hour" in interval:
                    annual *= 2_080
                structured_maxima.append(annual)
            for child in item.values():
                collect_salary_maxima(child)
        elif isinstance(item, list):
            for child in item:
                collect_salary_maxima(child)

    collect_salary_maxima(structured)
    if structured_maxima:
        return round(max(structured_maxima))
    numbers: list[float] = []
    pattern = (
        r"\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)\s*([km]?)|\b([0-9]+(?:\.[0-9]+)?)\s*([km])\b"
    )
    for dollar_raw, dollar_suffix, short_raw, short_suffix in re.findall(
        pattern, lowered
    ):
        raw = dollar_raw or short_raw
        suffix = dollar_suffix or short_suffix
        number = float(raw.replace(",", ""))
        if suffix == "k":
            number *= 1_000
        elif suffix == "m":
            number *= 1_000_000
        if number >= 10:
            numbers.append(number)
    if not numbers:
        return None
    maximum = max(numbers)
    if re.search(r"(?:per\s+hour|hourly|/\s*(?:hr|hour))", lowered):
        maximum *= 2_080
    return round(maximum)


def _location_allowed(posting: Posting, search: dict[str, Any]) -> bool:
    location = " ".join(posting.locations).lower()
    if bool(search["remote_us"]) and "remote" in location:
        return True
    return any(str(place).lower() in location for place in search["local_locations"])


def rank_postings(
    postings: list[tuple[str, Posting]], profile: dict[str, Any]
) -> list[RankedOpening]:
    """Apply hard constraints and rank remaining openings by evidenced term overlap."""
    search = profile["search"]
    minimum = int(search["minimum_salary_usd"])
    include_unknown = bool(search["include_when_salary_unstated"])
    excluded = tuple(str(term).lower() for term in profile.get("exclude_terms", []))
    rows: list[tuple[int, str, Posting, int | None, list[str], list[str]]] = []
    for employer, posting in postings:
        text = f"{posting.title} {posting.description_text}".lower()
        if not _location_allowed(posting, search) or any(
            term in text for term in excluded
        ):
            continue
        salary_max = _annual_salary_max(posting.compensation)
        if salary_max is None and not include_unknown:
            continue
        if salary_max is not None and salary_max < minimum:
            continue
        score = 0
        lanes: list[str] = []
        terms: list[str] = []
        for lane, definition in profile["target_lanes"].items():
            hits = [
                str(term) for term in definition["terms"] if str(term).lower() in text
            ]
            if hits:
                lanes.append(str(lane))
                terms.extend(hits)
                score += int(definition["weight"]) + min(len(hits) - 1, 3)
        if lanes:
            rows.append((score, employer, posting, salary_max, lanes, terms))
    rows.sort(key=lambda row: (-row[0], row[1].lower(), row[2].title.lower()))
    return [
        RankedOpening(
            rank=index,
            score=score,
            employer=employer,
            title=posting.title,
            locations=posting.locations,
            url=posting.canonical_url,
            salary_status="meets_floor" if salary is not None else "not_stated",
            salary_max_usd=salary,
            matched_lanes=tuple(lanes),
            matched_terms=tuple(dict.fromkeys(terms)),
        )
        for index, (score, employer, posting, salary, lanes, terms) in enumerate(
            rows, start=1
        )
    ]


def load_registry_postings(
    registry_path: Path,
    response_dir: Path,
    eligible_urls: set[str] | None = None,
) -> list[tuple[str, Posting]]:
    """Load already collected public ATS responses without making network requests."""
    output: list[tuple[str, Posting]] = []
    with registry_path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            if row["active"] != "true":
                continue
            identifier = row["board_identifier"].replace(" ", "_")
            path = response_dir / f"{row['ats_system']}-{identifier}.json"
            if not path.exists():
                continue
            for posting in PARSERS[row["ats_system"]](path.read_bytes()):
                if (
                    eligible_urls is not None
                    and posting.canonical_url not in eligible_urls
                ):
                    continue
                output.append((row["company_name_normalized"], posting))
    return output


def load_eligible_urls(path: Path) -> set[str]:
    """Read deterministic inclusions without asserting human approval."""
    urls: set[str] = set()
    for line in path.read_text().splitlines():
        record = json.loads(line)
        if (
            record.get("inclusion_decision") == "include"
            and record.get("selection_status") == "eligible"
        ):
            urls.add(str(record["canonical_url"]))
    return urls


def _markdown(rows: list[RankedOpening]) -> str:
    lines = [
        "# Personal job shortlist",
        "",
        "> Private decision aid. Openings must be rechecked before applying.",
        "",
        f"Qualified matches: {len(rows)}",
        "",
        "| Rank | Score | Employer | Role | Location | Salary | Match |",
        "|---:|---:|---|---|---|---|---|",
    ]
    for row in rows:
        salary = (
            f"up to ${row.salary_max_usd:,}"
            if row.salary_max_usd is not None
            else "not stated"
        )
        lines.append(
            "| {rank} | {score} | {employer} | [{title}]({url}) | {location} | "
            "{salary} | {match} |".format(
                rank=row.rank,
                score=row.score,
                employer=row.employer.replace("|", "\\|"),
                title=row.title.replace("|", "\\|"),
                url=row.url,
                location=", ".join(row.locations).replace("|", "\\|"),
                salary=salary,
                match=", ".join(row.matched_lanes).replace("_", " "),
            )
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--registry", type=Path, required=True)
    parser.add_argument("--responses", type=Path, required=True)
    parser.add_argument("--eligible-jobs", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-markdown", type=Path, required=True)
    args = parser.parse_args()
    profile = yaml.safe_load(args.profile.read_text())
    rows = rank_postings(
        load_registry_postings(
            args.registry,
            args.responses,
            load_eligible_urls(args.eligible_jobs),
        ),
        profile,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_markdown.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps([asdict(row) for row in rows], indent=2) + "\n"
    )
    args.output_markdown.write_text(_markdown(rows))


if __name__ == "__main__":
    main()
