# Employer registry methodology

Registry version `1.0.0` uses one row per employer/board combination and the
strict contract in `schemas/employers.schema.json`. The empty header-only seed
is deliberate: M07 defines the method; it does not pretend that unverified
employers or board identifiers are evidence.

## Seeding and validation

Build toward 300–500 boards across all nine codebook sectors. Candidate company
names are discovery targets only. A row becomes active only after its board
identifier is obtained from a public employer career link, visible ATS URL, or
official documentation; one conservative request confirms the organization;
current terms and robots metadata are recorded; and the response passes the
versioned adapter contract. Never enumerate guessed identifiers at volume.

Distinct brands, regions, boards, and ATS migrations remain separate rows under
one normalized employer identity. Monthly review covers mergers, rebrands,
migrations, dead boards, and organization mismatch. A 401/403, contract change,
new restriction, organization mismatch, or incomplete source fails closed and
leaves the row inactive. Application, candidate, administrative, and recruiting
management endpoints are prohibited.

## Sector diversity

Seed in rounds so every sector receives coverage before any sector receives a
second round. Registry counts are not sample quotas. The sample allocator still
enforces company/template caps, at least six sectors, at least four role
families, seniority and location-mode representation, and first-party evidence.
