# 2026-08 completion-run plan

- Study/specification: `BSE-JMA-001` / `1.1.1`
- Taxonomy/configuration/pipeline: `1.0.0` / `1.0.0` / `0.1.0`
- Planned run ID: `2026-08_bioinfo_jobs_us_v01`
- Collection window: not opened; if lawful live collection begins, at most
  `2026-08-14T04:20:00Z` through `2026-08-21T04:20:00Z`
- Target: 150 included active unique U.S. postings, at least 220 screened and
  at least 20 reserves
- Prior run: none (first baseline); M05 implementation state is the dependency
  baseline and must not be rerun
- Extraction model/prompt: deterministic fixtures first; no production model is
  selected or authorized by this plan
- Owner-authorized pacing: sequential M06 onward during 2026-08-14 only

## Checkpoints

1. Implement and verify acquisition, screening, deduplication, extraction,
   analysis, horizon-scan, publication-draft, and reproducibility machinery
   with deterministic synthetic fixtures where permitted.
2. Validate public source contracts and build live registry/discovery artifacts
   only when current terms, robots directives, access behavior, and provenance
   requirements can be verified; fail closed otherwise.
3. Never manufacture the required 150 live postings or human decisions. If the
   live pool cannot lawfully meet the frozen-sample gates in this run, record
   exact counts and stop the production run before analysis claims.
4. Generate a watermarked review candidate only from traceable artifacts.
5. Stop at mandatory human review. Required checkpoints include inclusion and
   manifest review, all AI/low-confidence/borderline/duplicate judgments, the
   stratified 20% audit, numerical and quotation verification, scenario
   probability approval, and publication sign-off.
