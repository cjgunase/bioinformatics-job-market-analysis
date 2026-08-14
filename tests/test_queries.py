from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
REQUIRED = {
    "bioinformatics engineer",
    "bioinformatics software engineer",
    "computational biologist",
    "computational scientist genomics",
    "scientific software engineer biology",
    "genomics engineer",
    "workflow engineer genomics",
    "pipeline engineer bioinformatics",
    "platform engineer life sciences",
    "machine learning engineer biology",
    "AI engineer drug discovery",
    "research engineer biological foundation model",
    "Nextflow engineer",
    "Snakemake engineer",
    "single-cell computational",
    "clinical bioinformatics software",
}


def test_query_catalogue_is_versioned_complete_and_unique() -> None:
    document = yaml.safe_load((ROOT / "config/queries.yaml").read_text())
    rows = document["queries"]
    queries = {row["query"] for row in rows}
    ids = [row["query_id"] for row in rows]
    assert document["catalog_version"] == "1.0.0"
    assert document["spec_version"] == "1.1.1"
    assert queries >= REQUIRED
    assert {row["family"] for row in rows} == {
        "title_forward",
        "capability_forward",
    }
    assert len(ids) == len(set(ids)) == len(rows)
    assert document["governance"]["discovery_only_is_not_inclusion_evidence"]
