import hashlib
import json
from pathlib import Path

from market_analysis.adapters import parse_greenhouse
from market_analysis.analyze import Assertion, prevalence
from market_analysis.capture import capture_snapshot
from market_analysis.classify import load_taxonomy, map_evidence
from market_analysis.deduplicate import DedupRecord, exact_duplicate_groups
from market_analysis.extract import DeterministicBulletExtractor, ExtractionContext
from market_analysis.gates import copyright_gate, privacy_gate, provenance_gate
from market_analysis.sample import SamplingCandidate, allocate
from market_analysis.screen import ScreeningFacts, screen

ROOT = Path(__file__).parents[1]


def synthetic_greenhouse_payload(count: int = 240) -> bytes:
    jobs = [
        {
            "id": index,
            "title": f"Bioinformatics Engineer {index}",
            "content": (
                "<p>Requirements:</p><p>- Python engineering for genomic workflows "
                f"with deterministic fixture identifier {index}.</p>"
            ),
            "location": {"name": "Remote - US" if index % 3 == 0 else "Boston, MA"},
            "absolute_url": f"https://example.test/jobs/{index}",
            "metadata": [],
        }
        for index in range(count)
    ]
    return json.dumps({"jobs": jobs}).encode()


def test_complete_synthetic_path_reaches_draft_but_not_human_approval(
    tmp_path: Path,
) -> None:
    postings = parse_greenhouse(synthetic_greenhouse_payload())
    assert len(postings) == 240
    passing = ScreeningFacts(True, True, True, True, True, True, True, True)
    assert all(screen(passing).inclusion_decision == "include" for _ in postings)

    snapshots = [
        capture_snapshot(
            posting.description_text,
            excerpt_start=0,
            excerpt_end=len(posting.description_text),
            retention_mode="excerpt_hash_metadata_only",
            restricted_dir=tmp_path / "raw",
            snapshot_id=posting.posting_id,
        )
        for posting in postings
    ]
    assert all(snapshot.full_text_path is None for snapshot in snapshots)
    dedup = [
        DedupRecord(
            posting.posting_id,
            f"company-{index // 3}.test",
            f"Synthetic Company {index // 3}",
            posting.title,
            "US",
            posting.canonical_url,
            posting.posting_id,
            snapshots[index].normalized_text_sha256,
            posting.description_text,
        )
        for index, posting in enumerate(postings)
    ]
    assert exact_duplicate_groups(dedup) == []

    sectors = [f"sector_{index}" for index in range(7)]
    roles = [f"role_{index}" for index in range(5)]
    seniority = ["entry_associate", "mid_level", "senior_plus"]
    modes = ["onsite", "hybrid", "remote"]
    candidates = [
        SamplingCandidate(
            f"job_{index}",
            f"company_{index // 3}",
            f"template_{index // 2}",
            sectors[index % 7],
            roles[index % 5],
            seniority[index % 3],
            modes[index % 3],
            index % 5 != 0,
        )
        for index in range(240)
    ]
    allocation = allocate(candidates, run_id="synthetic_v01")
    assert len(allocation.included) == 150
    assert len(allocation.reserve) == 20

    source = "Requirements:\n- Python engineering for genomic workflows.\n"
    context = ExtractionContext(
        "synthetic_v01",
        "job_1",
        "https://example.test/jobs/1",
        "2026-08-14T04:20:00Z",
        hashlib.sha256(source.encode()).hexdigest(),
    )
    evidence = DeterministicBulletExtractor().extract(source, context)
    mappings = map_evidence(evidence, load_taxonomy(ROOT / "taxonomy/taxonomy.yaml"))
    assert any(mapping.taxonomy_skill_id == "python" for mapping in mappings)

    assertions = [
        Assertion(item.canonical_job_id, "python", "required")
        for item in allocation.included
    ]
    result = prevalence(
        assertions, {item.canonical_job_id for item in allocation.included}
    )
    combined = next(row for row in result if row.status == "combined")
    assert (combined.numerator, combined.denominator, combined.percentage) == (
        150,
        150,
        100.0,
    )

    provenance: list[dict[str, object]] = [
        {
            "canonical_url": postings[0].canonical_url,
            "retrieved_at": "2026-08-14T04:20:00Z",
            "active_verified_at": "2026-08-14T04:20:00Z",
            "description_sha256": snapshots[0].normalized_text_sha256,
            "source_type": "synthetic_fixture",
        }
    ]
    assert provenance_gate(provenance).passed
    assert copyright_gate([snapshots[0].excerpt], []).passed
    assert privacy_gate([ROOT / "tests/fixtures/extraction/job_description.txt"]).passed
