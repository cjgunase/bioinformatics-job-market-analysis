# Progress log

## 2026-08-08 — Project initialized

- Created the local and GitHub project structure.
- Converted specification 1.1.1 into a 42-milestone, one-part-per-day roadmap.
- Preserved the mandatory human-review boundary for canonical publication.
- Scheduled unattended work for midnight America/New_York.

Next: M01 — import and checksum the approved specification.

## 2026-08-09 — M01 completed

- Imported approved specification `BSE-JMA-001` version `1.1.1` byte-for-byte.
- Pinned SHA-256 digest
  `7721e84c22c3ef07dbcb9a926bef6074f74847f9c257f184fe8f87cda78a9ed0`.
- Documented provenance, verification, and change-governance requirements.
- Verified the repository copy with `sha256sum --check`, byte comparison with
  the approved source, JSON parsing, and whitespace validation.

Blockers: none.

Next: M02 — scaffold the Python package, pinned tooling, and baseline CI.

## 2026-08-10 — M02 completed

- Added the installable `market_analysis` source package and package smoke test.
- Pinned Python 3.13.11, uv 0.9.27, direct development tools, transitive
  dependencies, and GitHub Actions by immutable commit.
- Added baseline CI for linting, formatting, strict type checking, tests, and
  source/wheel builds.
- Documented reproducible setup, validation commands, and restricted-data
  handling.
- Validated locally with locked-environment sync, Ruff, mypy, pytest (1 passed),
  package builds, JSON parsing, and whitespace checks.

Blockers: none. No collection was performed; funnel and human-review counts
remain zero because M02 is infrastructure-only.

Next: M03 — define study configuration, controlled values, and run metadata.

## 2026-08-11 — M03 completed

- Added versioned study configuration 1.0.0 with specification 1.1.1 scope,
  sampling, review, analysis, quality, horizon-scan, and publication defaults.
- Documented exact controlled values in codebook 1.0.0, while leaving the skill
  taxonomy version unset for M05.
- Added an explicitly pre-collection run-metadata example with null timestamps,
  zero funnel counts, and no human-review claim.
- Added typed YAML/JSON configuration loaders and tests for normative defaults,
  controlled-value uniqueness, required metadata fields, and human-gate safety.

Blockers: none. No collection was performed; candidate, included, reserve,
evidence-validated, and human-reviewed counts remain zero.

Next: M04 — implement JSON Schemas and schema-validation tests.

## 2026-08-12 — M04 completed

- Added strict Draft 2020-12 schemas for run, job, atomic-requirement, and
  evidence records.
- Added fail-closed validation with date, time, URI, hostname, hash, identifier,
  controlled-value, nullability, and numeric-range checks.
- Added representative valid records, invalid-record rejection tests, schema
  self-validation, required/additional-field checks, and codebook-enum drift
  checks.
- Validated with locked dependency sync, Ruff lint and format checks, strict
  mypy, pytest (32 passed), distribution builds, JSON parsing, and whitespace
  checks.

Blockers: none. No collection was performed; candidate, included, reserve,
evidence-validated, and human-reviewed counts remain zero. Taxonomy identifiers
remain unset pending M05.

Next: M05 — establish taxonomy 1.0.0 and its governance changelog.

## 2026-08-14 — M05 completed

- Established taxonomy 1.0.0 with 187 hierarchical skill nodes across all 13
  specification-defined software-engineering, bioinformatics-context, AI, and
  durable AI-era categories.
- Added stable identifiers, definitions, inclusion and exclusion rules,
  aliases, parent links, tool and AI flags, lifecycle metadata, and an
  append-only governance changelog with migration and backcast requirements.
- Pinned study configuration and run metadata to taxonomy 1.0.0 and made
  taxonomy identifiers mandatory in atomic requirement records.
- Preserved the human gate: the implementation baseline is pending initial
  human review and remains ineligible for canonical market findings.
- Validated with locked dependency sync, Ruff lint and format checks, strict
  mypy, pytest (39 passed), distribution builds, JSON parsing, and whitespace
  checks.

Blockers: none. No collection was performed; candidate, included, reserve,
evidence-validated, and human-reviewed counts remain zero.

Next: M06 — add the versioned discovery-query catalogue.

## 2026-08-14 — Authorized completion run started

- Confirmed M05 was already merged in GitHub PR #5 with passing CI; it will not
  be duplicated.
- Started a one-shot, owner-authorized sequential run from M06. Decision D009
  records that only the daily pacing rule is overridden.
- Wrote the run plan before implementation or collection. No collection or
  publication approval is claimed by this checkpoint.

Next: M06 — add the versioned discovery-query catalogue.

## 2026-08-14 — M06–M37 one-shot completion run

- Completed M06–M30 sequentially in reviewable commits: versioned discovery,
  employer registry, fail-closed acquisition adapters and contract monitoring,
  append-only screening, lawful capture, exact/near deduplication, deterministic
  sampling, extraction/classification interfaces, Track A statistics, Track B
  evidence/scenario machinery, accessible draft generation, safety gates, a
  single-command pipeline, and synthetic end-to-end verification.
- Completed M31–M35 with current official contract checks and low-rate public
  reads only. Greenhouse, Lever, and Ashby example feeds passed their documented
  read contracts; one stale Neptune board and one stale Insitro board returned
  404 and remain inactive. The registry reached 38 rows, 36 active boards, eight
  sectors, and 918 hash-chained metadata-only discovery records. No application,
  candidate, administrative, or authenticated endpoint was called.
- Completed M36 by screening all 918 current postings, retaining only hashes and
  excerpts of at most 320 characters. Results: 105 deterministic pre-review
  inclusions, zero exact duplicates, and eight near-duplicate pairs queued for
  human adjudication. Automated privacy, copyright, link, schema, and provenance
  checks passed; raw descriptions were not committed.
- Completed M37 through its documented insufficiency branch. The company cap
  reduces the maximum selectable pool to 80, 70 below the final sample and 90
  below sample plus reserve. No manifest was frozen and no canonical estimate,
  publication candidate, or time-series update was produced.
- Validated the completed tree locally with Ruff lint and format checks, strict
  mypy, and 133 passing pytest tests. GitHub CI status is recorded separately
  after the review branch is pushed.
- Closed the dated pacing override and restored `daily_milestone_limit` to 1.

Blocking evidence: `reports/2026-08/insufficiency_report.md`.

Next: expand the publicly observed registry and run another one-shot collection
within the seven-day window. M38 is not dependency-ready until a compliant
150-record sample and 20-record reserve can be frozen.

## 2026-08-16 — M37 insufficiency continuation

- Added the minimum retained set of 38 publicly observed employer ATS boards:
  19 Greenhouse, 17 Ashby, and two Lever boards.
- Validated all 38 boards with one low-rate public read each. Every response was
  HTTP 200 and parsed under the existing 1.0.0 contracts; no new source type,
  authentication, application endpoint, administrative endpoint, guessed
  identifier, or access-control bypass was introduced.
- Rebuilt the current metadata-only collection and deterministic screening
  artifacts: 2,336 screened, 208 included before exact deduplication, one exact
  duplicate excluded, 207 unique pre-review records, and nine near-duplicate
  pairs queued for human adjudication.
- The unchanged company cap leaves exactly 170 usable records across 68
  contributing companies: 150 target records plus 20 reserves. Three records
  are deterministically classified as mid-level.
- Preserved the human gate. Template caps, diversity checks, evidence review,
  near-duplicate adjudication, and manifest approval remain incomplete; no
  manifest or canonical estimate was produced.

Next: human review and M37 manifest controls. M38 remains dependency-blocked
until an approved 150-record sample and 20-record reserve are frozen.
