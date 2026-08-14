import csv
import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).parents[1]


def test_registry_header_matches_strict_schema() -> None:
    schema = json.loads((ROOT / "schemas/employers.schema.json").read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    with (ROOT / "config/employers.csv").open(newline="") as handle:
        header = next(csv.reader(handle))
    assert header == schema["required"]


def test_registry_schema_accepts_a_valid_board_and_rejects_extras() -> None:
    schema = json.loads((ROOT / "schemas/employers.schema.json").read_text())
    row = {
        "employer_id": "emp_example_bio",
        "company_name_normalized": "Example Bio",
        "company_domain": "example.org",
        "sector": "biotechnology_tools",
        "company_size_proxy": None,
        "ats_system": "greenhouse",
        "board_identifier": "examplebio",
        "public_board_url": "https://boards.greenhouse.io/examplebio",
        "api_base_url": "https://boards-api.greenhouse.io/v1/boards",
        "api_documentation_url": "https://developer.greenhouse.io/job-board.html",
        "authentication_expected": False,
        "terms_checked_at": None,
        "robots_checked_at": None,
        "last_success_at": None,
        "last_http_status": None,
        "parser_version": "1.0.0",
        "active": False,
        "discovery_source": "public employer career link",
        "notes": None,
    }
    jsonschema.Draft202012Validator(schema).validate(row)
    row["unexpected"] = True
    assert list(jsonschema.Draft202012Validator(schema).iter_errors(row))
