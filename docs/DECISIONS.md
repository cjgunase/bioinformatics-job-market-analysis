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

## D008 — 2026-08-14 — Initial taxonomy baseline

Taxonomy 1.0.0 encodes specification 1.1.1 sections 8.1–8.13 as 187 stable
skill nodes in 13 top-level categories. Each skill carries explicit inclusion
and exclusion guidance, aliases, within-category parent links, tool and
AI-related flags, and lifecycle metadata. Bioinformatics context stays separate
from software-engineering prevalence, and explicit AI evidence stays separate
from generic automation, algorithms, statistics, and conventional
bioinformatics. Run and requirement contracts now require taxonomy 1.0.0 and
non-null taxonomy identifiers. The implementation baseline remains pending
initial human review and does not authorize canonical market findings; future
taxonomy changes follow the append-only semantic-versioning, review, migration,
and backcast rules in `taxonomy/CHANGELOG.md`.

## D009 — 2026-08-14 — One-shot completion pacing override

Chathura explicitly authorized a same-day, sequential completion run through
all dependency-ready remaining milestones. For this run only, the
one-milestone-per-day rule and `daily_milestone_limit` are superseded. No other
rule changes: dependency order, scope and taxonomy governance, access controls,
privacy, copyright, provenance, mandatory quality thresholds, reproducibility,
and human-only decisions remain binding. The agent must complete only verified
automatable work, must not invent live evidence, and must stop with an accurate
`awaiting_human_review` status at the mandatory sign-off gate. The override is
closed at the end of this one-shot run and does not create or re-enable a cron.

## D010 — 2026-08-14 — Insufficiency branch and publication stop

The first live pool screened 918 postings from 36 active, publicly observed ATS
boards. Deterministic rules retained 105 before human review, but the mandatory
five-posting company cap leaves a maximum of 80. This cannot fill the 150-record
sample or 20-record reserve. M37 therefore takes its specification-defined
insufficiency branch: no manifest is frozen, M38–M42 remain dependency-blocked,
and no monthly estimate, publication candidate, or time-series update is
generated. Eligibility, geography, diversity, evidence, and human-review rules
remain unchanged. Safe continuation requires additional publicly observed
employers and a new one-shot collection, or explicit human approval for the
specification's noncanonical reduced-sample special edition. D009 is now closed
and the normal daily limit is restored.

## D011 — 2026-08-16 — Minimum retained registry expansion

The M37 insufficiency continuation retains 38 additional publicly observed
employer boards: the smallest validated set, ordered by observed capped yield,
that raises the refreshed cap-usable pool to 170. Collection reused only the
approved Greenhouse, Lever, and Ashby public read contracts. Every retained
board returned HTTP 200 and parsed under adapter contract 1.0.0; no identifier
was guessed and no authentication, application, administrative, or bypass path
was used. Eligibility, U.S. geography, the five-record company cap, evidence
retention, diversity controls, and human-review requirements are unchanged.

The expanded run has 207 unique deterministic pre-review records, nine
near-duplicate pairs, three deterministic mid-level records, and exactly 170
records after the company cap. This closes the numerical insufficiency only.
Human adjudication, template caps, diversity checks, and manifest approval still
gate M38; no sample is frozen and no canonical estimate is authorized.

## D012 — 2026-08-16 — Separate private job-search layer

The repository may reuse already collected public posting data as a private
candidate decision aid, but personal ranking remains outside the approved market
study. Candidate profiles and generated shortlists are gitignored applicant data.
Personal location, compensation, sponsorship, and academic-role preferences do
not alter study eligibility, sampling, taxonomy, evidence, human review, or
publication artifacts. Rankings are leads, not verified fit or application
decisions, and every posting must be rechecked before use.
