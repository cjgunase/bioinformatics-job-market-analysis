# Append-only decision log

## D001 — 2026-08-08 — Daily scope

The automation may complete at most one roadmap milestone per local calendar
day. Failed or blocked milestones remain current; the system does not catch up
by combining work.

## D002 — 2026-08-08 — Publication boundary

The agent may publish code, methods, progress, and explicitly watermarked draft
outputs. It may not claim human verification or publish canonical monthly market
findings until the specification's named human-review gates are complete.

## D003 — 2026-08-08 — Repository and portfolio

The implementation lives in `cjgunase/bioinformatics-job-market-analysis`.
Chathura's portfolio contains one living project entry linking to the repository
and its progress log. Every nightly run appends a dated public report to that
same project page, including outcome, validation, blockers, source links, and the
next milestone. Progress stays consolidated as one project instead of creating
separate posts.

## D004 — 2026-08-09 — Normative baseline provenance

Specification `BSE-JMA-001` version `1.1.1` is preserved byte-for-byte at
`docs/specification/BSE-JMA-001-v1.1.1.md` with SHA-256 digest
`7721e84c22c3ef07dbcb9a926bef6074f74847f9c257f184fe8f87cda78a9ed0`.
Normative changes require the specification's reviewed versioning process;
the pinned file and checksum must not be silently rewritten.

## D005 — 2026-08-10 — Baseline Python toolchain

The package baseline uses Python 3.13.11 and uv 0.9.27. Direct development
tools are exactly constrained in `pyproject.toml`, transitive dependencies are
locked in `uv.lock`, and CI actions are pinned to immutable commit SHAs. The
baseline CI gate runs linting, formatting, strict type checking, unit tests,
and distribution builds without accessing job-source data.

## D006 — 2026-08-11 — Versioned configuration boundary

Study defaults are represented in `config/study.yaml` at configuration version
`1.0.0`, and exact non-taxonomy controlled identifiers are documented in
`schemas/codebook.yaml` at codebook version `1.0.0`. The configuration preserves
specification 1.1.1 thresholds and keeps the taxonomy version null until M05.
Run metadata begins in an explicit pre-collection state with null timestamps,
zero funnel counts, and no reviewer; those fields may change only from observed
run events and human decisions. Semantic controlled-value changes require review
and an appended decision rather than silent replacement.

## D007 — 2026-08-12 — Record-schema boundary

Run, job, atomic-requirement, and evidence records use JSON Schema Draft
2020-12 contracts that require specification fields, reject undeclared fields,
preserve explicit nulls, check formats and ranges, and mirror codebook enums.
Tests make codebook/schema drift a failure. Cross-record foreign keys and
ordered comparisons remain pipeline checks because they are not reliably
expressible in portable JSON Schema. Taxonomy identifiers remain nullable until
M05 establishes taxonomy 1.0.0; M04 does not assign or change taxonomy meaning.
