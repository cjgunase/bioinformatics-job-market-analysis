# August 2026 draft-sample insufficiency report

Status: **blocked before sample freeze; no canonical estimate may be produced**

Run: `2026-08_bioinfo_jobs_us_v01`  
Specification: `BSE-JMA-001` version `1.1.1`  
Collection window represented by this one-shot increment: 2026-08-14 UTC

## Verified result

The run screened all 918 postings retrieved from 36 active, publicly observed
employer ATS boards. Deterministic screening retained 105 postings before human
review. No exact duplicates were found. Eight near-duplicate pairs are preserved
for human adjudication.

The required five-posting company cap reduces the maximum selectable pool to 80.
That is 70 below the required sample of 150 and 90 below the sample-plus-reserve
minimum of 170. The current pool also has no confidently classified mid-level
record; that representation gate cannot be claimed. The sample manifest was
therefore **not frozen**. M38–M42 are not dependency-ready, and no Track A
estimate, Track B monthly draft, publication candidate, or canonical time-series
update was generated from this incomplete pool.

## Screening accounting

| Outcome | Count |
|---|---:|
| Screened | 918 |
| Deterministically eligible before human review | 105 |
| Exact duplicate exclusions | 0 |
| Near-duplicate pairs awaiting adjudication | 8 |
| Maximum after company cap | 80 |
| Required final sample | 150 |
| Required reserve | 20 |

Exclusion reason counts are: 542 without material engineering content, 243
without material life-science content, 17 without established U.S. eligibility,
7 academic/postdoctoral, and 4 internships. Criteria were not weakened to improve
the count.

## Reproducible review artifacts

- `data/validated/2026-08/screening_decisions.jsonl` — all 918 decisions,
  SHA-256 `7a3e8f88652385136ce07496174e2de5103acd6fa13dba26b587ed5a5a60fe97`.
- `data/validated/2026-08/screened_jobs.jsonl` — 105 pre-review eligible records,
  SHA-256 `c74acfa5c27d7800789d2d05f8e289f848892ca451b293de59c61070eb36db3f`.
- `data/validated/2026-08/screening_evidence.jsonl` — minimum audit excerpts and
  hashes, SHA-256 `4ac960b9c9086800c6ebf238a092c439b1a1664b741fd33f4ce640b2c91f7f25`.
- `data/validated/2026-08/near_duplicate_queue.jsonl` — eight pairs,
  SHA-256 `73090720830e3502b56193c73fd22b5c7691bbf7bd1e60ae643144911d60d986`.
- `reports/2026-08/live_pool_screening.json` — machine-readable phase report,
  SHA-256 `e54c2568883e70f9985be41effb740780b1954780a0843040caae19d3839f9d9`.

Raw descriptions remain uncommitted. Committed evidence uses metadata, hashes,
and excerpts no longer than 320 characters. Automated privacy, copyright, link,
schema, and provenance checks passed; human review is not complete.

## Smallest safe continuation

Do not change geography, eligibility, company caps, or diversity thresholds.
Expand the publicly observed employer registry—especially employers likely to
contribute eligible roles without increasing current company concentrations—then
run another low-rate, one-shot collection within the allowed seven-day window.
The next attempt needs at least 90 additional cap-usable eligible postings and a
mid-level stratum before freeze can succeed. A human-approved reduced-sample
special edition is the only specification-permitted alternative, and it must stay
outside the canonical time series.

No access control was bypassed, no live evidence was invented, and no recurring
schedule is requested by this report.

## 2026-08-17 compliant continuation

The smallest retained expansion adds 38 publicly observed employer boards using
only the already approved Greenhouse, Lever, and Ashby read-only contracts. All
38 returned HTTP 200 and parsed under adapter contract version 1.0.0. No
authentication, application endpoint, administrative endpoint, identifier
guessing, or access-control bypass was used.

The refreshed run screened 2,336 postings and retained 208 deterministic
inclusions before exact deduplication. One exact duplicate was excluded, leaving
207 unique pre-review eligible records. Applying the unchanged five-record
company cap across 68 contributing companies leaves exactly 170 cap-usable
records: 150 for the requested sample and 20 reserves. Three records are
deterministically classified as mid-level.

This resolves only the numerical insufficiency. Nine near-duplicate pairs,
human eligibility/evidence review, template-cap enforcement, diversity checks,
and final manifest approval remain mandatory. The manifest is not frozen and no
canonical estimate or publication is authorized. Machine-readable validation is
in `reports/2026-08/collection_expansion_validation.json`.
