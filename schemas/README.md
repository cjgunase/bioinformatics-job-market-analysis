# Record schemas

The JSON files in this directory are the machine-readable record contracts for
specification `BSE-JMA-001` version `1.1.1`. They use JSON Schema Draft 2020-12
and validate one record at a time:

- `runs.schema.json` validates run metadata and the pre-collection example.
- `jobs.schema.json` validates screened job records.
- `requirements.schema.json` validates atomic job-skill assertions.
- `evidence.schema.json` validates the verbatim evidence linked to assertions.

All schemas reject undeclared properties and require every specification field.
Nullable fields remain explicit JSON `null`; empty strings are not substitutes
for missing values. Controlled enums mirror `codebook.yaml`, and tests fail if
the two sources drift.

The schemas enforce structural constraints, formats, identifier patterns,
controlled values, and numeric ranges. Cross-record and ordered comparisons—
for example, whether `char_end` is at least `char_start`, whether a foreign key
exists, or whether collection closed after it started—belong to later pipeline
validation because JSON Schema cannot express them reliably without custom
extensions.

Use `market_analysis.schema.validate_record` to validate with Draft 2020-12 and
format checking enabled. Validation errors fail closed; callers must quarantine
invalid records rather than partially accepting them.
