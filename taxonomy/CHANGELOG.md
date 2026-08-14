# Taxonomy changelog

All notable taxonomy changes are recorded here without rewriting prior entries.
Taxonomy versions follow semantic versioning under specification `BSE-JMA-001`
section 18.7: patch releases correct nonsemantic metadata, minor releases add
compatible nodes or aliases, and major releases change meaning or hierarchy in
a way that can break time-series comparability.

Every proposed change must use a reviewable pull request that documents the
definition, motivation, examples, exclusions, mapping or backcast plan, and
time-series impact. A human must review taxonomy additions before a monthly
sample is frozen. Deprecated nodes remain addressable, and published records
retain the exact taxonomy version used for coding.

## 1.0.0 — 2026-08-14

- Established the initial hierarchical, multi-label taxonomy directly from
  approved specification 1.1.1 sections 8.1–8.13.
- Added stable category and skill identifiers, explicit inclusion and exclusion
  rules, aliases, parent links, tool flags, AI-related flags, and lifecycle
  metadata.
- Kept bioinformatics context nodes separate from software-engineering
  prevalence and separated explicit AI evidence from generic automation,
  algorithms, statistical modeling, and conventional bioinformatics.
- Marked the implementation baseline as pending initial human review. It may be
  used for development and watermarked drafts, but it does not make canonical
  market findings eligible for publication.

Time-series impact: initial baseline; no prior taxonomy-coded series exists.

Backcast plan: not applicable for version 1.0.0. Future compatible additions
must document whether earlier preserved evidence can be backcast; incompatible
changes require a series break or reviewed migration.
