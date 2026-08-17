from market_analysis.adapters import Posting
from market_analysis.job_search import _annual_salary_max, rank_postings


def _profile() -> dict[str, object]:
    return {
        "search": {
            "remote_us": True,
            "local_locations": ["Houston, TX"],
            "minimum_salary_usd": 100000,
            "include_when_salary_unstated": True,
        },
        "target_lanes": {
            "genomics": {"weight": 5, "terms": ["genomics", "nextflow"]},
            "engineering": {"weight": 3, "terms": ["python"]},
        },
        "exclude_terms": [],
    }


def _posting(location: str, compensation: str | None = None) -> Posting:
    return Posting(
        source="greenhouse",
        posting_id="1",
        title="Senior Bioinformatics Engineer",
        description_text="Build genomics pipelines with Nextflow and Python.",
        locations=(location,),
        canonical_url="https://example.org/job/1",
        compensation=compensation,
    )


def test_salary_parser_handles_annual_and_hourly_ranges() -> None:
    assert _annual_salary_max("$100k-$145k per year") == 145000
    assert _annual_salary_max("$110,000-$130,000") == 130000
    assert _annual_salary_max("$50-$60 / hour") == 124800
    structured = (
        '{"summaryComponents":[{"compensationType":"Salary",'
        '"currencyCode":"USD","interval":"1 YEAR","maxValue":210000}]}'
    )
    assert _annual_salary_max(structured) == 210000


def test_ranking_keeps_remote_or_houston_and_rejects_low_salary() -> None:
    postings = [
        ("Remote Co", _posting("Remote - United States")),
        ("Houston Co", _posting("Houston, TX", "$110,000-$130,000")),
        ("Low Pay", _posting("Remote", "$70k-$90k")),
        ("Elsewhere", _posting("Boston, MA", "$150k-$180k")),
    ]
    rows = rank_postings(postings, _profile())
    assert [row.employer for row in rows] == ["Houston Co", "Remote Co"]
    assert rows[0].matched_lanes == ("genomics", "engineering")
