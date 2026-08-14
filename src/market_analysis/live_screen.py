"""Conservative live-pool screening, snapshot metadata, and deduplication."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from market_analysis.adapters import Posting, parse_ashby, parse_greenhouse, parse_lever
from market_analysis.capture import capture_snapshot, normalize_source_text
from market_analysis.deduplicate import (
    DedupRecord,
    canonical_job_id,
    exact_duplicate_groups,
    near_duplicate_candidates,
    normalize_label,
    template_fingerprint,
)
from market_analysis.schema import validate_record
from market_analysis.screen import ScreeningFacts, screen

PARSERS = {
    "ashby": parse_ashby,
    "greenhouse": parse_greenhouse,
    "lever": parse_lever,
}

ACADEMIC_RE = re.compile(
    r"\b(post[ -]?doc(?:toral)?|faculty|professor|fellowship)\b", re.I
)
INTERN_RE = re.compile(r"\b(intern(?:ship)?|co-op|student|graduate program)\b", re.I)
OUT_OF_SCOPE_RE = re.compile(
    r"\b(sales|account executive|marketing|legal|counsel|finance|accounting|"
    r"human resources|people operations|talent|recruiter|business development|"
    r"medical science liaison|executive assistant|facilities|maintenance|"
    r"manufacturing associate|quality assurance|quality control|clinical trial manager|"
    r"project manager|program manager|product manager|technical writer)\b",
    re.I,
)
TARGET_TITLE_RE = re.compile(
    r"\b(bioinformatics|computational|software|data (?:engineer|scientist|architect)|"
    r"machine learning|ml engineer|ai[/ -]?(?:ml|engineer|scientist)|informatics|"
    r"biostatistic|research engineer|platform engineer|cloud engineer|"
    r"infrastructure engineer|devops|workflow engineer|pipeline engineer|"
    r"scientific systems|systems engineer)\b",
    re.I,
)
LIFE_TITLE_RE = re.compile(
    r"\b(bioinformatics|computational biology|genomic|clinical data|biostatistic|"
    r"protein|biological|scientific|informatics)\b",
    re.I,
)
ENGINEERING_RE = re.compile(
    r"\b(Python|R programming|R language|SQL|Java|C\+\+|JavaScript|TypeScript|"
    r"software|source code|coding|programming|Git(?:Hub|Lab)?|API|pipeline|workflow|"
    r"data engineering|machine learning|deep learning|MLOps|PyTorch|TensorFlow|JAX|"
    r"AWS|GCP|Azure|cloud computing|Docker|Kubernetes|Nextflow|Snakemake|WDL|"
    r"Cromwell|Airflow|HPC|Slurm|distributed computing|database|ETL|CI/CD)\b",
    re.I,
)
LIFE_RE = re.compile(
    r"\b(biology|biological|biomedical|bioinformatics|genom(?:e|ic|ics)|"
    r"sequencing|omics|transcriptomics|proteomics|single-cell|clinical|patient|"
    r"therapeutic|drug discovery|protein|molecular|diagnostic|assay|cellular|"
    r"pharmaceutical|life science)\b",
    re.I,
)
US_STATE_RE = re.compile(
    r"\b(Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|"
    r"Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|"
    r"Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|"
    r"Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|"
    r"North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|"
    r"South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|"
    r"Wisconsin|Wyoming|District of Columbia)\b",
    re.I,
)
US_ABBR_RE = re.compile(
    r"(?:^|[,;/\s])(AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|"
    r"MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|"
    r"TX|UT|VT|VA|WA|WV|WI|WY|DC)(?:$|[,;/\s])"
)
US_CITY_RE = re.compile(
    r"\b(Boston|Cambridge|Somerville|Watertown|San Francisco|South San Francisco|"
    r"Palo Alto|Menlo Park|Fremont|Emeryville|Redwood City|Seattle|New York|"
    r"Durham|San Diego|Rockville|Bethesda|Washington,? D\.?C\.?)\b",
    re.I,
)
EXPLICIT_US_RE = re.compile(
    r"\b(United States|U\.S\.|USA|US-based|Remote[-, ]+(?:in )?(?:the )?US)\b",
    re.I,
)


def _response_path(
    response_dirs: tuple[Path, ...], system: str, identifier: str
) -> Path:
    filename = f"{system}-{identifier.replace(' ', '_')}.json"
    matches = [directory / filename for directory in response_dirs]
    for path in matches:
        if path.exists():
            return path
    raise ValueError(f"missing retrieved response: {filename}")


def _us_eligibility(posting: Posting) -> tuple[bool, bool]:
    location = "; ".join(posting.locations)
    explicit = bool(
        EXPLICIT_US_RE.search(location)
        or US_STATE_RE.search(location)
        or US_ABBR_RE.search(location)
        or US_CITY_RE.search(location)
    )
    if explicit:
        return True, False
    if "remote" in location.lower() and EXPLICIT_US_RE.search(posting.description_text):
        return True, False
    ambiguous = "remote" in location.lower() or not location.strip()
    return False, ambiguous


def _employment_type(posting: Posting) -> tuple[str, bool]:
    text = f"{posting.title} {posting.description_text[:1000]}".lower()
    if "part-time" in text or "part time" in text:
        return "part_time", True
    if "contract" in text:
        return "contract", True
    if "fixed-term" in text or "fixed term" in text or "temporary" in text:
        return "fixed_term", True
    return "full_time", True


def _role_family(title: str) -> str:
    value = title.lower()
    if re.search(
        r"\b(manager|director|head|lead|principal|staff|architect|vp)\b", value
    ):
        return "technical_leadership_management"
    if "bioinformatics" in value or "genomics engineer" in value:
        return "bioinformatics_engineering"
    if "computational" in value or "biostatistic" in value:
        return "computational_biology_science"
    if re.search(r"\b(machine learning|ml |ai[/ -])", value):
        return "ai_ml_for_biology"
    if re.search(r"\b(data|workflow|pipeline|cloud|infrastructure|devops)\b", value):
        return "data_workflow_infrastructure"
    return "scientific_software_platform"


def _seniority(title: str) -> str:
    value = title.lower()
    if re.search(
        r"\b(senior|sr\.?|staff|principal|lead|manager|director|head|vp)\b", value
    ):
        return "senior_plus"
    if re.search(r"\b(junior|jr\.?|associate|entry|level i\b|engineer i\b)\b", value):
        return "entry_associate"
    if re.search(r"\b(engineer ii|scientist ii|[2-9]\+? years?)\b", value):
        return "mid_level"
    return "unspecified"


def _location_mode(posting: Posting) -> str:
    value = " ".join(posting.locations).lower()
    if "remote" in value:
        return "remote"
    if "hybrid" in value:
        return "hybrid"
    return "onsite" if value.strip() else "unspecified"


def _facts(posting: Posting) -> ScreeningFacts:
    title = posting.title
    description = normalize_source_text(posting.description_text)
    us_eligible, ambiguous_geography = _us_eligibility(posting)
    target_title = bool(TARGET_TITLE_RE.search(title))
    life_title = bool(LIFE_TITLE_RE.search(title))
    engineering_matches = ENGINEERING_RE.findall(description)
    life_matches = LIFE_RE.findall(description)
    out_of_scope = bool(OUT_OF_SCOPE_RE.search(title)) and not target_title
    engineering_material = (
        target_title and bool(engineering_matches) and not out_of_scope
    )
    life_science_material = (life_title or len(life_matches) >= 2) and not out_of_scope
    _, paid_allowed = _employment_type(posting)
    return ScreeningFacts(
        industry=True,
        active=True,
        complete_text=len(description) >= 200,
        life_science_material=life_science_material,
        engineering_material=engineering_material,
        us_eligible=us_eligible,
        paid_allowed_employment=paid_allowed,
        identity_complete=bool(
            posting.canonical_url and posting.posting_id and posting.locations
        ),
        excluded_academic=bool(ACADEMIC_RE.search(title)),
        excluded_internship=bool(INTERN_RE.search(title)),
        confidence=0.95 if not ambiguous_geography else 0.75,
        ambiguous_geography=ambiguous_geography,
        ambiguous_biological_materiality=target_title and not life_science_material,
    )


def _audit_span(text: str) -> tuple[int, int]:
    normalized = normalize_source_text(text)
    match = ENGINEERING_RE.search(normalized) or LIFE_RE.search(normalized)
    center = match.start() if match else 0
    start = max(0, center - 80)
    end = min(len(normalized), start + 320)
    if end - start < 1:
        raise ValueError("eligible posting has no auditable text")
    return start, end


def _job_record(
    row: dict[str, str], posting: Posting, retrieved_at: str
) -> tuple[dict[str, Any], dict[str, Any], DedupRecord]:
    normalized = normalize_source_text(posting.description_text)
    provisional = DedupRecord(
        job_id=f"source_{posting.source}_{posting.posting_id}",
        company_domain=row["company_domain"],
        company_name=row["company_name_normalized"],
        title=posting.title,
        location_group="; ".join(posting.locations) or "Unspecified",
        canonical_url=posting.canonical_url,
        requisition_id=posting.posting_id,
        normalized_text_sha256=hashlib.sha256(normalized.encode()).hexdigest(),
        comparison_text=normalized,
    )
    stable_id = canonical_job_id(provisional)
    record = DedupRecord(**{**asdict(provisional), "job_id": stable_id})
    start, end = _audit_span(normalized)
    snapshot = capture_snapshot(
        normalized,
        excerpt_start=start,
        excerpt_end=end,
        retention_mode="excerpt_hash_metadata_only",
        restricted_dir=Path("data/raw/2026-08"),
        snapshot_id=stable_id,
    )
    employment_type, _ = _employment_type(posting)
    location_raw = "; ".join(posting.locations) or "Unspecified (source omitted)"
    job: dict[str, Any] = {
        "run_id": "2026-08_bioinfo_jobs_us_v01",
        "job_id": stable_id,
        "canonical_job_id": stable_id,
        "company_name_raw": row["company_name_normalized"],
        "company_name_normalized": row["company_name_normalized"],
        "company_domain": row["company_domain"],
        "title_raw": posting.title,
        "title_normalized": normalize_label(posting.title),
        "role_family": _role_family(posting.title),
        "seniority": _seniority(posting.title),
        "sector": row["sector"],
        "employment_type": employment_type,
        "location_raw": location_raw,
        "country": "US",
        "state": None,
        "city": None,
        "location_mode": _location_mode(posting),
        "us_eligible": True,
        "salary_min": None,
        "salary_max": None,
        "salary_currency": None,
        "salary_period": None,
        "posting_date": None,
        "first_seen_at": retrieved_at,
        "last_verified_at": retrieved_at,
        "active_at_freeze": None,
        "canonical_url": posting.canonical_url,
        "discovery_url": row["public_board_url"],
        "source_type": "employer_operated_ats",
        "requisition_id": posting.posting_id,
        "description_sha256": snapshot.normalized_text_sha256,
        "template_fingerprint": template_fingerprint(normalized),
        "full_text_path": None,
        "selection_status": "eligible",
        "inclusion_decision": "include",
        "decision_reason_code": "include_meets_all",
        "decision_rationale": "All deterministic inclusion conditions passed; human review remains required before freeze.",
        "inclusion_confidence": 0.95,
        "duplicate_cluster_id": None,
        "replacement_for_job_id": None,
        "human_review_status": "not_reviewed",
    }
    evidence = {
        "evidence_id": f"evidence_{stable_id[4:]}_screen",
        "job_id": stable_id,
        "source_url": posting.canonical_url,
        "retrieved_at": retrieved_at,
        "source_section": "screening_context",
        "paragraph_or_bullet_index": None,
        "char_start": start,
        "char_end": end,
        "verbatim_excerpt": snapshot.excerpt,
        "excerpt_sha256": snapshot.excerpt_sha256,
        "snapshot_sha256": snapshot.normalized_text_sha256,
        "capture_method": "public_ats_adapter_1.0.0",
        "terms_retention_mode": "excerpt_hash_metadata_only",
    }
    return job, evidence, record


def screen_live_pool(
    registry_path: Path,
    response_dirs: tuple[Path, ...],
    jobs_path: Path,
    evidence_path: Path,
    decisions_path: Path,
    near_duplicates_path: Path,
    report_path: Path,
    *,
    retrieved_at: str,
    jobs_schema: dict[str, Any],
    evidence_schema: dict[str, Any],
) -> dict[str, Any]:
    """Screen every active-board posting and write reproducible validated artifacts."""
    with registry_path.open(newline="") as handle:
        rows = [row for row in csv.DictReader(handle) if row["active"] == "true"]
    jobs: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    records: list[DedupRecord] = []
    decisions: list[dict[str, Any]] = []
    for row in rows:
        path = _response_path(response_dirs, row["ats_system"], row["board_identifier"])
        postings = PARSERS[row["ats_system"]](path.read_bytes())
        for posting in postings:
            facts = _facts(posting)
            decision = screen(facts)
            decision_row = {
                "run_id": "2026-08_bioinfo_jobs_us_v01",
                "employer_id": row["employer_id"],
                "posting_id": posting.posting_id,
                "canonical_url": posting.canonical_url,
                "title_raw": posting.title,
                "location_raw": "; ".join(posting.locations) or None,
                "description_sha256": hashlib.sha256(
                    normalize_source_text(posting.description_text).encode()
                ).hexdigest(),
                **asdict(decision),
                "inclusion_confidence": facts.confidence,
            }
            decisions.append(decision_row)
            if decision.inclusion_decision != "include":
                continue
            job, item_evidence, dedup_record = _job_record(row, posting, retrieved_at)
            jobs.append(job)
            evidence.append(item_evidence)
            records.append(dedup_record)

    by_job = {str(item["job_id"]): item for item in jobs}
    duplicate_ids: set[str] = set()
    exact_groups = exact_duplicate_groups(records)
    for index, group in enumerate(exact_groups, start=1):
        keep = min(group)
        cluster = f"exact_{index:04d}"
        for job_id in group:
            by_job[job_id]["duplicate_cluster_id"] = cluster
            if job_id != keep:
                duplicate_ids.add(job_id)
    for job_id in duplicate_ids:
        item = by_job[job_id]
        item["selection_status"] = "excluded"
        item["inclusion_decision"] = "exclude"
        item["decision_reason_code"] = "exclude_duplicate"
        item["decision_rationale"] = (
            "Exact URL, requisition, or normalized-text duplicate."
        )

    near_pairs = [asdict(pair) for pair in near_duplicate_candidates(records)]
    for item in jobs:
        validate_record(item, jobs_schema)
    for item in evidence:
        validate_record(item, evidence_schema)

    jobs_path.parent.mkdir(parents=True, exist_ok=True)
    for path, items in (
        (jobs_path, jobs),
        (evidence_path, evidence),
        (decisions_path, decisions),
        (near_duplicates_path, near_pairs),
    ):
        path.write_text(
            "".join(json.dumps(item, sort_keys=True) + "\n" for item in items)
        )
    reason_counts = Counter(str(item["decision_reason_code"]) for item in decisions)
    report: dict[str, Any] = {
        "run_id": "2026-08_bioinfo_jobs_us_v01",
        "retrieved_at": retrieved_at,
        "screened_n": len(decisions),
        "deterministic_include_before_dedup_n": len(jobs),
        "exact_duplicate_exclusions_n": len(duplicate_ids),
        "eligible_unique_n": len(jobs) - len(duplicate_ids),
        "near_duplicate_pairs_n": len(near_pairs),
        "decision_reason_counts": dict(sorted(reason_counts.items())),
        "raw_descriptions_committed": False,
        "snapshot_retention_mode": "excerpt_hash_metadata_only",
        "human_review_complete": False,
    }
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    return report
