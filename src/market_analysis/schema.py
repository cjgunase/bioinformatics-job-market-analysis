"""Validate records against the project's JSON Schema contracts."""

from collections.abc import Mapping
from typing import cast

from jsonschema import Draft202012Validator, FormatChecker


def validator_for(schema: Mapping[str, object]) -> Draft202012Validator:
    """Build a Draft 2020-12 validator after checking the schema itself."""
    schema_document = cast("dict[str, object]", dict(schema))
    Draft202012Validator.check_schema(schema_document)
    return Draft202012Validator(schema_document, format_checker=FormatChecker())


def validate_record(record: Mapping[str, object], schema: Mapping[str, object]) -> None:
    """Fail closed when a record does not satisfy its supplied schema."""
    validator_for(schema).validate(dict(record))
