# Living Specification: Monthly Bioinformatics Software-Engineering Job Market Analysis

**Specification ID:** BSE-JMA-001  
**Version:** 1.1.1  
**Status:** Approved baseline  
**Owner:** Repository maintainer  
**Update cadence:** Monthly  
**Target sample:** 150 active, unique industry job postings  
**Primary publication:** GitHub Pages blog post with observed-market and AI-capability-horizon sections  
**Normative language:** MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are requirements terms.

## 1. Agent mandate

The agent MUST maintain a reproducible, evidence-backed monthly analysis with two separate tracks: (A) current industry demand for software-engineering and AI-related competencies in bioinformatics, computational biology, and adjacent scientific-software roles; and (B) a forward-looking AI capability and engineering-practice horizon scan. Each monthly run MUST collect and validate a cross-sectional sample of 150 active job postings, extract atomic requirements with verbatim evidence, classify them under a versioned taxonomy, calculate prevalence and co-occurrence, compare the results with prior months, evaluate evidence about changing AI coding capabilities and human/agent work allocation, and publish an accessible GitHub Pages article plus reusable data artifacts.

The agent is an evidence processor, not an authority. It MAY use AI to discover, extract, normalize, code, summarize, draft, and test, but MUST preserve source evidence, declare uncertainty, and route specified judgments to a human reviewer. It MUST NOT fabricate text, infer unstated requirements, silently repair missing evidence, bypass access controls, or publish unsupported claims. Observed labor-market evidence, measured AI capability evidence, expert forecasts, and the study's own scenarios MUST remain visibly separate.

## 2. Research questions

### 2.1 Primary question

What software-engineering competencies are explicitly requested in current industry bioinformatics and computational-biology job postings, how prevalent are they, which skills co-occur, and how are AI-related expectations changing over time?

### 2.2 Secondary questions

1. How do requirements differ by role family, seniority, company sector, company size proxy, location mode, and education requirement?
2. Which named tools occur most often, and which broader competencies do they represent?
3. Which competency pairs and clusters co-occur more often than expected?
4. How often are AI-assisted development, AI/ML engineering, foundation models, agents, prompt/evaluation practices, or responsible-AI controls explicit requirements?
5. Which requirements are new, rising, falling, or persistent across comparable monthly samples?
6. What proportion of postings distinguish required from preferred qualifications?
7. Which software-development tasks are AI agents becoming able to perform reliably, at what task duration, level of repository context, and degree of autonomy?
8. As direct manual coding declines, which durable human competencies become more important: problem formulation, codebase comprehension, architecture, verification, scientific validation, reproducibility, security, provenance, governance, and accountability?
9. Which future scenarios are consistent with current evidence, and what leading indicators would support or falsify each scenario?

## 2.3 Dual-track interpretation rule

Track A answers “what employers explicitly request now.” Track B answers “how the work may change as AI capabilities advance.” Track B MUST NOT be presented as if it came from the 150 postings. The article MUST label every forward-looking statement as measured capability, adoption evidence, forecast, scenario, or author inference. The study MUST continue measuring conventional coding skills even if their explicit prevalence falls, because declining job-ad language may indicate automation, assumed baseline knowledge, or changing role boundaries rather than irrelevance.

## 2.4 AI-era engineering thesis to test, not assume

The standing hypothesis is that the scarce human contribution may shift from producing most code tokens to specifying intent, supplying context, understanding system behavior, designing constraints and interfaces, evaluating agent output, proving scientific and operational correctness, and accepting accountability. The analysis MUST test this hypothesis against evidence and MUST report contradictory evidence. It MUST NOT assume that “no manual coding” means “no need to understand code.”

## 3. Scope and unit of analysis

### 3.1 Population

The target population is active, externally advertised, paid industry employment in which biological, biomedical, genomic, clinical, pharmaceutical, or life-science work is a material part of the role and software construction, computational analysis, data engineering, workflow engineering, ML/AI engineering, or scientific platform work is material to the role.

Default geography is the United States, including remote roles that explicitly permit U.S.-based employment. A future geography expansion requires a minor specification version, a declared sampling frame, and separate reporting; it MUST NOT be silently mixed into the U.S. time series.

### 3.2 Unit of inclusion

The unit is one unique job requisition for one materially distinct position. Multiple locations under one requisition count once. A repost counts as the same job when company, normalized title, responsibilities, and requirements are substantially unchanged. Distinct requisition IDs count separately only if the postings differ materially in team, level, scope, or requirements.

### 3.3 Observation window

Each run has a UTC `collection_started_at` and `collection_closed_at`. Collection SHOULD finish within seven calendar days. A posting is “current” only when verified active during that window. The article MUST state the window, not merely the publication month.

### 3.4 Target roles

Include, when the job content satisfies the population definition:

- Bioinformatics Engineer; Bioinformatics Software Engineer; Genomics Engineer.
- Computational Biologist; Computational Scientist; Bioinformatics Scientist.
- Scientific Software Engineer; Research Software Engineer; Software Engineer, Biology/Genomics.
- Workflow, Pipeline, Platform, Data, Cloud, or Infrastructure Engineer for life-science computation.
- ML/AI Engineer, Applied Scientist, or Research Engineer working materially on biological data, drug discovery, diagnostics, genomics, or scientific agents.
- Technical lead, staff, principal, architect, or engineering-manager variants when hands-on technical requirements remain visible.

Titles are discovery aids, not sufficient evidence of inclusion.

## 4. Inclusion and exclusion criteria

### 4.1 Inclusion: all conditions MUST pass

1. The employer is an industry organization or industry-facing nonprofit; contract roles are allowed when the client/domain and requirements are disclosed.
2. The posting is active and accepts applications at verification time, or the employer page clearly labels it open.
3. The full or substantively complete job description is accessible and can be archived lawfully as structured evidence or permitted excerpts.
4. Biological or life-science context is material, not incidental.
5. At least one software-engineering, computational, data, workflow, cloud, infrastructure, or AI/ML competency is explicit.
6. The location is U.S.-based or remote with explicit U.S. eligibility under the default frame.
7. Employment is full-time or part-time paid work. Fixed-term and contract work MUST be flagged.
8. The posting has enough identity metadata for deduplication: employer, title, location or remote status, canonical URL, and either requisition ID or content fingerprint.

### 4.2 Exclusion: any condition is sufficient

- Academic faculty, postdoctoral, student, internship, fellowship, or unpaid roles.
- Pure wet-lab roles with no material computational/software component.
- Generic software/data/AI roles where life science is merely one possible customer sector.
- Clinical informatics roles centered on operations, billing, or EHR administration without material software/computational biology work.
- IT support, help desk, systems administration, sales, solutions consulting, product management, project management, or technical writing without hands-on engineering requirements.
- Staffing-board mirrors when the original employer posting is available; use the canonical employer source.
- Expired, closed, removed, inaccessible, login-only, or snippet-only postings without sufficient evidence.
- Duplicate or near-duplicate requisitions beyond the caps below.
- Roles lacking a reliable U.S. location/eligibility determination.

### 4.3 Borderline adjudication

The agent MUST record `inclusion_decision`, `decision_reason_code`, and a short rationale for every screened candidate. Borderline cases are those with confidence below 0.80, ambiguous industry/academic status, ambiguous geography, or unclear biological materiality. A human MUST decide borderline inclusions before sample freeze. If no human is available by the deadline, the agent MUST exclude the case conservatively, mark it `pending_human`, and replace it from the reserve pool.

## 5. Sampling strategy

### 5.1 Candidate pool and freeze

The agent SHOULD screen at least 220 candidates to obtain 150 eligible unique postings plus a reserve pool of at least 20. It MUST freeze a monthly manifest before analysis. Records added after freeze require a logged replacement event.

### 5.2 Source hierarchy

Use sources in this order:

1. Employer career page or employer-operated applicant-tracking system.
2. Employer-authenticated LinkedIn or equivalent posting that contains the full text.
3. Reputable job board carrying full employer-attributed text.
4. Search-engine cache or aggregator only for discovery, never as sole evidence unless the exception is human-approved and disclosed.

The agent MUST obey site terms, robots/access restrictions, and rate limits. It MUST NOT circumvent CAPTCHAs, authentication, paywalls, or technical controls.

### 5.2.1 Preferred free public job APIs

The default acquisition route is the employer's public applicant-tracking-system job feed. At specification version 1.1.1, Greenhouse, Lever, and Ashby provide public read endpoints for published job postings without an API key. These are company-specific feeds, not global search APIs. The agent MUST know or discover the employer's board identifier before querying them and MUST revalidate access behavior at the start of each monthly run.

| System | Public read endpoint | Authentication for published-job GET | Board identifier | Official documentation |
|---|---|---|---|---|
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{board_token}/jobs?content=true` | None normally required | `board_token` from the employer's Greenhouse board URL | `https://developer.greenhouse.io/job-board.html` |
| Lever | `https://api.lever.co/v0/postings/{site}?mode=json` | None normally required | employer `site` name from `jobs.lever.co/{site}` | `https://github.com/lever/postings-api` |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{job_board_name}?includeCompensation=true` | None normally required | employer job-board name from its Ashby board URL | `https://developers.ashbyhq.com/docs/public-job-posting-api` |

The agent MUST use only read operations. It MUST NOT call application-submission, candidate, administrative, or recruiting-management endpoints. Those operations are outside scope and may require credentials. Never collect applicant information.

“No authentication normally required” describes the documented public published-job feed at the time of this specification. It is not a permanent guarantee. On HTTP 401/403, a changed response contract, or a newly stated restriction, the agent MUST stop using that route, record the change, consult the current official documentation and site terms, and use an allowed fallback. It MUST NOT search for private keys, reuse browser credentials, or imitate an authenticated applicant session.

### 5.2.2 Employer and board registry

Maintain `config/employers.csv` or an equivalent validated table. One row represents one employer/board combination and MUST contain:

`employer_id`, `company_name_normalized`, `company_domain`, `sector`, `company_size_proxy`, `ats_system`, `board_identifier`, `public_board_url`, `api_base_url`, `api_documentation_url`, `authentication_expected`, `terms_checked_at`, `robots_checked_at`, `last_success_at`, `last_http_status`, `parser_version`, `active`, `discovery_source`, `notes`.

The starting registry SHOULD contain 300–500 relevant employers across all study sectors. Board identifiers MUST come from publicly visible employer career links, public ATS URLs, or official documentation. The agent MUST NOT guess identifiers at high request volume. Validate a candidate identifier with one low-rate request, confirm that the returned organization matches the employer, and cache the result.

An employer may operate multiple boards, brands, regions, or ATS systems. Preserve distinct board records and link them to one normalized employer. Review the registry monthly for mergers, acquisitions, rebrands, ATS migrations, dead boards, and newly relevant companies.

### 5.2.3 Secondary discovery sources

Use general job platforms and search engines only to discover candidate employer postings when possible. Candidate sources include LinkedIn Jobs, BioSpace, Indeed, Built In, Google or Bing job/search results, Wellfound, Nature Careers, Science Careers, and relevant biotechnology associations. The agent MUST follow a discovered vacancy to the employer's canonical career page or public ATS record and use that first-party record as evidence when available.

Do not assume a free public bulk API exists for LinkedIn, Indeed, Google Jobs, Workday, iCIMS, SuccessFactors, or every custom career site. Do not automate collection from a platform when its terms or technical controls prohibit it. Search snippets may support discovery but are not sufficient evidence for inclusion.

### 5.2.4 Workday and other nonstandard career systems

Workday and several enterprise ATS products do not provide one standardized, documented, cross-employer public job API comparable to the three preferred feeds. Treat their public career pages as company-specific sources. The agent MAY retrieve a posting only when it is publicly accessible, the method complies with current terms and access controls, and the full text can be captured reliably. Store the exact career-site tenant/instance metadata and parser version. If the page is client-rendered, unstable, login-only, blocked, or incomplete, mark it unavailable and use the reserve pool; do not reverse-engineer private services or bypass controls.

### 5.2.5 Source-specific extraction requirements

For every API response, retain the retrieval timestamp, request URL with secrets removed, HTTP status, response content type, posting ID, canonical application URL, and SHA-256 of normalized content. Validate required response fields before parsing. Preserve the raw response only when allowed by retention policy; otherwise preserve permitted excerpts, hashes, and metadata.

Implement one versioned adapter per source system rather than a single brittle scraper. Each adapter MUST have frozen fixtures and tests covering normal records, missing fields, HTML descriptions, pagination, compensation, multiple locations, removed jobs, rate limiting, malformed responses, and schema changes. A source-contract failure MUST fail closed and create an issue; it MUST NOT emit partially parsed production records silently.

### 5.2.6 Access cost and redistribution rule

The preferred Greenhouse, Lever, and Ashby published-job GET routes do not normally charge a per-request API fee. This means the study can collect its core sample without purchasing a commercial jobs API. “Free access” does not mean unlimited requests or unrestricted republication. Apply conservative caching, rate limits, exponential backoff, identifiable research contact information when appropriate, and domain-level concurrency limits.

Do not publish complete job descriptions unless redistribution permission is clear. Public releases SHOULD contain employer/title metadata, canonical links, derived taxonomy codes, hashes, and the minimum short excerpts required to audit claims. Full permitted snapshots belong in restricted or gitignored storage with the documented retention schedule.

### 5.2.7 Default monthly acquisition funnel

The agent SHOULD plan for attrition rather than stopping when it discovers 150 appealing jobs:

| Stage | Planning range |
|---|---:|
| Raw discoveries across registry, queries, and secondary sources | 350–500 |
| Full postings successfully retrieved | 275–350 |
| Pass initial title/content relevance screening | 210–260 |
| Eligible after industry, geography, activity, and evidence checks | 180–220 |
| Unique after deduplication and caps | 170–200 |
| Frozen final sample | Exactly 150 |
| Reserve pool | 20–30, minimum 20 |

These are planning ranges, not quotas to manipulate. The agent MUST continue discovery until the eligible unique pool can satisfy the final sample, reserve minimum, and diversity constraints. It MUST preserve every rejected and reserve candidate in the screening log.

### 5.2.8 Initial employer-universe sectors

Seed and maintain the registry across large biopharma; biotechnology and research tools; genomics and sequencing; diagnostics and precision medicine; AI-enabled drug discovery; bioinformatics/scientific platforms; synthetic biology; clinical and health technology; and contract research/services. Employer names are discovery targets, not guaranteed active-job sources. The agent MUST determine current eligibility and openings during each collection window rather than treating a static company list as evidence.

### 5.2.9 Required acquisition query families

The versioned query file MUST include, at minimum: `bioinformatics engineer`, `bioinformatics software engineer`, `computational biologist`, `computational scientist genomics`, `scientific software engineer biology`, `genomics engineer`, `workflow engineer genomics`, `pipeline engineer bioinformatics`, `platform engineer life sciences`, `machine learning engineer biology`, `AI engineer drug discovery`, `research engineer biological foundation model`, `Nextflow engineer`, `Snakemake engineer`, `single-cell computational`, and `clinical bioinformatics software`.

Queries MUST include title-forward and capability-forward variants. A generic title such as “Research Engineer,” “Applied Scientist,” or “ML Engineer” is eligible only when the full description establishes material biological and engineering content.

### 5.3 Discovery query families

Use a versioned query list covering target titles, role synonyms, and sector terms. Include both title-forward queries (`bioinformatics engineer`, `computational biologist`, `scientific software engineer`) and capability-forward queries (`Nextflow genomics engineer`, `AI drug discovery software`, `single-cell pipeline engineer`). Save the exact query, source, run time, and returned URL for every discovered candidate.

### 5.4 Diversity controls

The final sample MUST satisfy these controls unless the run report documents a scarcity exception approved by a human:

- No company contributes more than 5 postings or 3.3% of the sample, whichever is lower; default cap is 5.
- No normalized posting template contributes more than 3 records.
- At least 6 sector groups are represented, with no sector above 30%.
- At least 4 role families are represented, with no role family above 40%.
- Entry/associate, mid-level, and senior+ roles MUST all be present; “unspecified” is reported separately.
- On-site/hybrid and remote-eligible roles MUST both be represented when available.
- At least 70% of records SHOULD use first-party employer sources.

Sector groups: biopharma; biotechnology/tools; diagnostics/clinical labs; genomics/sequencing; health-tech; AI-enabled drug discovery; contract research/services; scientific software/platform; other life science.

Role families: bioinformatics engineering; computational biology/science; scientific software/platform; data/workflow/infrastructure; AI/ML for biology; technical leadership/management.

### 5.5 Selection procedure

1. Screen candidates against inclusion/exclusion rules.
2. Deduplicate and assign strata.
3. Sort eligible records within each stratum by deterministic hash of `run_id + canonical_job_id`; do not handpick based on interesting requirements.
4. Allocate 150 positions using proportional allocation with diversity floors and caps.
5. Fill short strata from the closest declared stratum using the reserve pool.
6. Save all eligible nonselected records with `selection_status=reserve` and the reason.

This is a structured quota sample, not a probability sample. The article MUST avoid claims that the estimates represent every employer or vacancy without qualification.

## 6. Evidence capture and provenance

### 6.1 Required source snapshot

For each included posting, preserve:

- canonical URL and discovery URL;
- retrieval and active-verification timestamps in UTC;
- source type and access status;
- requisition ID when present;
- normalized plain text or permitted local snapshot;
- SHA-256 of normalized source text;
- page title, employer, job title, location, and posting date when present;
- parser/extractor version;
- content language;
- licensing/terms note and snapshot retention mode.

If full-text retention is not permitted, store metadata, hash, retrieval time, and only the minimum short excerpts necessary to audit coded claims. Never commit personal applicant data, session tokens, cookies, credentials, or private page content.

### 6.2 Atomic evidence rule

Every coded requirement MUST point to one or more verbatim source excerpts. An excerpt SHOULD be one sentence or bullet and MUST be short enough to audit. Preserve the original wording and punctuation except whitespace normalization. Store a source locator such as section heading, bullet index, paragraph index, or character offsets. Do not use the job title alone as evidence of a skill.

Split compound bullets into atomic requirement records only when each coded item is textually supported. Example: “Build Python pipelines in AWS using Docker” may yield Python, workflow/pipeline engineering, AWS/cloud, and containers, each linked to the same excerpt. Never infer Kubernetes from containers, CI/CD from GitHub, or deep learning from “AI.”

### 6.3 Requirement status

Classify each atomic item as `required`, `preferred`, `responsibility`, `benefit_context`, or `unclear`. Prevalence defaults to `required + preferred + responsibility` and MUST also be reported separately for required versus preferred. Do not count benefits or descriptive company marketing.

### 6.4 Evidence confidence

Assign extraction confidence from 0 to 1. Confidence is about fidelity to explicit text, not belief that the employer truly uses the skill.

- 0.95–1.00: named skill/tool with unambiguous requirement status.
- 0.80–0.94: explicit broader competency or clear compound statement.
- 0.60–0.79: ambiguous status, alias mapping, or broad category needing review.
- Below 0.60: do not include in quantitative analysis without human approval.

## 7. Data model

All tabular outputs MUST be UTF-8, use stable snake_case field names, ISO 8601 dates/times, explicit nulls, and a published JSON Schema or equivalent validation model.

### 7.1 `runs`

Required fields: `run_id`, `spec_version`, `taxonomy_version`, `pipeline_version`, `collection_started_at`, `collection_closed_at`, `publication_month`, `target_n`, `included_n`, `candidate_n`, `reserve_n`, `previous_run_id`, `git_commit`, `status`, `human_reviewer`, `freeze_timestamp`, `notes`.

`run_id` format: `YYYY-MM_bioinfo_jobs_us_vNN`, where `NN` is a two-digit rerun number.

### 7.2 `jobs`

Required fields:

`run_id`, `job_id`, `canonical_job_id`, `company_name_raw`, `company_name_normalized`, `company_domain`, `title_raw`, `title_normalized`, `role_family`, `seniority`, `sector`, `employment_type`, `location_raw`, `country`, `state`, `city`, `location_mode`, `us_eligible`, `salary_min`, `salary_max`, `salary_currency`, `salary_period`, `posting_date`, `first_seen_at`, `last_verified_at`, `active_at_freeze`, `canonical_url`, `discovery_url`, `source_type`, `requisition_id`, `description_sha256`, `template_fingerprint`, `full_text_path`, `selection_status`, `inclusion_decision`, `decision_reason_code`, `decision_rationale`, `inclusion_confidence`, `duplicate_cluster_id`, `replacement_for_job_id`, `human_review_status`.

Controlled values MUST be documented in `schemas/codebook.yaml`. Salary values remain null when absent; never impute salary.

### 7.3 `requirements`

Required fields:

`run_id`, `requirement_id`, `job_id`, `evidence_id`, `requirement_text_normalized`, `requirement_status`, `taxonomy_category_id`, `taxonomy_skill_id`, `tool_or_technology_raw`, `years_experience_min`, `years_experience_max`, `education_level`, `proficiency_term`, `ai_relation`, `extraction_method`, `extractor_model`, `prompt_version`, `confidence`, `human_verified`, `adjudication_note`.

One row represents one job-skill assertion. Repeated mentions of the same skill in one posting MUST collapse to one row for prevalence, while all evidence links remain available through a junction table.

### 7.4 `evidence`

Required fields:

`evidence_id`, `job_id`, `source_url`, `retrieved_at`, `source_section`, `paragraph_or_bullet_index`, `char_start`, `char_end`, `verbatim_excerpt`, `excerpt_sha256`, `snapshot_sha256`, `capture_method`, `terms_retention_mode`.

### 7.5 `taxonomy`

Required fields:

`taxonomy_version`, `category_id`, `skill_id`, `preferred_label`, `definition`, `include_when`, `exclude_when`, `aliases`, `parent_skill_id`, `is_tool`, `is_ai_related`, `introduced_in_version`, `deprecated_in_version`.

### 7.6 `screening_log` and `change_log`

The screening log contains every candidate URL and outcome. The change log contains timestamp, agent/human actor, entity, field, old value, new value, reason, and related issue or commit. No silent corrections are permitted after freeze.

## 8. Software-engineering and AI taxonomy

The taxonomy is multi-label and hierarchical. Code the most specific supported skill and roll up to its parents during analysis. A named tool MAY map to both a tool node and a broader competency. Categories are not mutually exclusive.

### 8.1 Programming and software construction

Languages: Python, R, Bash/shell, SQL, Java, C/C++, JavaScript/TypeScript, Go, Rust, Scala, Julia, MATLAB, other named language. Practices: modular design, object-oriented or functional design, algorithms/data structures, APIs, CLI development, libraries/packages, code quality/refactoring, performance optimization, parallel/concurrent programming.

### 8.2 Version control and collaboration

Git; GitHub/GitLab/Bitbucket; branching and pull requests; code review; issue tracking; collaborative development; open-source contribution.

### 8.3 Testing, quality, and reliability

Unit, integration, end-to-end, regression, property-based, performance, and validation testing; test automation; scientific validation; reproducibility; observability; logging; monitoring; error handling; incident response; reliability/SRE; static analysis; linting; type checking.

### 8.4 Build, release, and DevOps

CI/CD; build systems; dependency and environment management; package publishing; infrastructure as code; deployment automation; release/versioning; artifact registries.

### 8.5 Containers, orchestration, and cloud

Docker/containers; Kubernetes; serverless; AWS, GCP, Azure; cloud architecture; batch/HPC cloud; cost optimization; identity/access management; cloud storage and compute.

### 8.6 Workflow and scientific computing

Nextflow, Snakemake, WDL/Cromwell, CWL, Airflow, Dagster, Prefect, other orchestrators; pipeline design; workflow portability; provenance; HPC; schedulers such as Slurm; distributed computing; GPUs; numerical/scientific computing.

### 8.7 Data engineering and platforms

Relational and NoSQL databases; data modeling; ETL/ELT; data lakes/warehouses; Spark; streaming; metadata/catalogs; data quality; scalable storage; vector databases; search/indexing; data governance.

### 8.8 Architecture and product engineering

System design; distributed systems; microservices; event-driven systems; web applications; frontend/UI; backend services; API design; platform engineering; multi-tenant systems; usability/user-centered development; requirements translation.

### 8.9 Security, privacy, and regulated engineering

Secure coding; threat/risk management; secrets; access control; privacy; HIPAA; GxP; FDA/clinical validation; audit trails; compliance; software lifecycle controls. Count a regulation only when tied to technical or process expectations relevant to the role.

### 8.10 Documentation and engineering process

Technical documentation; architecture/design documents; SOPs; Agile/Scrum/Kanban; estimation/planning; mentorship; stakeholder communication; cross-functional work; product ownership; technical leadership.

### 8.11 Bioinformatics engineering context

NGS/genomics pipelines; single-cell; spatial omics; proteomics; transcriptomics; variant calling; sequence analysis; imaging; clinical bioinformatics; laboratory information systems; FAIR data; bioinformatics formats and standards. These contextual codes are reported separately and MUST NOT inflate software-engineering prevalence unless paired with an explicit engineering competency.

### 8.12 AI-related taxonomy

Use `ai_relation` values: `none`, `ai_assisted_development`, `ai_ml_engineering`, `generative_ai_llm`, `ai_agents_or_orchestration`, `ai_evaluation_safety`, `ai_scientific_application`, `ambiguous_ai`.

Code the following distinct skills when explicit:

- AI-assisted software development: Copilot, Cursor, coding agents, AI code review, AI-supported testing/documentation, or explicit routine use of AI coding tools.
- ML engineering: training/inference pipelines, feature engineering, model serving, MLOps, experiment tracking, monitoring, and reproducibility.
- Deep learning frameworks: PyTorch, TensorFlow, JAX, named frameworks.
- Generative AI/LLMs: prompting, retrieval-augmented generation, fine-tuning, embeddings, foundation models, multimodal models.
- Agents/orchestration: tool-using agents, multi-step planning, agent frameworks, human-in-the-loop systems.
- Evaluation and safety: benchmarks, hallucination/error analysis, guardrails, red teaming, privacy, security, model governance, responsible AI.
- AI for scientific work: protein/sequence models, biological foundation models, drug-discovery models, lab/analysis agents.

Do not classify generic “automation,” algorithms, statistical modeling, or conventional bioinformatics as AI. “Experience with AI” without detail receives `ambiguous_ai` and a low-specificity taxonomy node.

### 8.13 Durable AI-era engineering competencies

Code and report these competencies independently of programming-language prevalence:

- Specification and intent engineering: translating scientific goals into testable requirements, constraints, interfaces, acceptance tests, and machine-executable plans.
- Codebase and system comprehension: repository navigation, dependency tracing, architecture reconstruction, reading generated code, impact analysis, and maintaining accurate mental/system models.
- Context engineering: selecting authoritative repository, data, protocol, issue, and domain context for agents; managing context freshness, permissions, and information boundaries.
- Agent orchestration: task decomposition, delegation, tool permissions, checkpoints, escalation policies, multi-agent coordination, and recovery from partial failure.
- Verification and validation: test design, independent oracles, invariant/property checks, differential testing, benchmark design, scientific validation, and adversarial review.
- Reproducibility and provenance: immutable inputs, environment capture, workflow provenance, prompt/model/tool lineage, deterministic reruns, data lineage, artifact signing, and traceable results.
- Correctness under scientific uncertainty: distinguishing software correctness from biological validity; checking assumptions, leakage, confounding, calibration, units, reference builds, statistical validity, and domain plausibility.
- AI-generated-code governance: authorship and ownership rules, approval boundaries, audit logs, risk tiering, model/vendor change control, licensing/IP review, incident reporting, and accountability.
- Security and containment: least-privilege tools, sandboxing, secrets protection, prompt-injection defenses, supply-chain controls, dependency review, data exfiltration prevention, and safe rollback.
- Maintenance and stewardship: diagnosing agent-written systems, controlling architectural drift, reducing generated-code sprawl, documentation currency, deprecation, migration, and long-term operability.
- Human factors and organizational design: reviewer workload, automation bias, skill atrophy, training, escalation competence, separation of duties, and responsibility assignment.

The primary AI-era outcome is not “manual coding required.” It is “capacity to understand, direct, verify, reproduce, govern, and safely maintain software-intensive scientific work,” regardless of who or what generated the code.

## 8.14 Work-allocation maturity model

Classify evidence and scenarios using a versioned five-level model:

1. Assisted: humans write and review most code; AI suggests local fragments.
2. Delegated tasks: agents implement bounded issues under close human review.
3. Delegated workflows: agents plan and execute multi-file changes, tests, documentation, and pull requests with checkpoints.
4. Supervised autonomy: agents maintain substantial subsystems and resolve routine incidents; humans specify goals, review evidence, and approve high-risk changes.
5. Governed autonomous engineering: agents perform most implementation and maintenance across long horizons; humans remain accountable for architecture, scientific validity, safety, policy, exceptions, and auditability.

This model describes work allocation, not guaranteed capability. A company, tool, benchmark, or scenario MAY occupy different levels for different task classes. Never assign a universal maturity level from marketing language alone.

## 8.15 Manual-code and system-understanding indicators

Track separate indicators for: explicit coding-language requirements; code-reading/debugging; architecture/system design; test and evaluation design; reproducibility/provenance; code review; AI-agent supervision; approval/accountability; security/governance; and scientific validation. Report whether manual coding signals decline while system-understanding and assurance signals rise, fall, or remain absent. Absence in a posting is not proof that a competency is unnecessary.

## 8.16 Scientific software assurance hierarchy

For AI-generated bioinformatics software, require evidence at multiple layers:

1. Build and syntax: code executes in the pinned environment.
2. Software behavior: unit, integration, property, regression, and failure-mode tests pass.
3. Data integrity: schemas, identifiers, reference assemblies, units, metadata, and lineage are correct.
4. Analytical validity: statistical assumptions, calibration, controls, leakage prevention, and benchmark design are sound.
5. Biological validity: outputs are plausible and supported by domain-relevant controls or expert review.
6. Reproducibility: an independent clean run regenerates results from declared inputs.
7. Operational assurance: security, privacy, observability, rollback, change control, and incident response are adequate.
8. Governance: accountable humans approve risk-appropriate evidence and retain an auditable decision record.

Passing a generated test suite is necessary but never sufficient evidence of scientific correctness.

## 9. Deduplication

### 9.1 Canonicalization

Normalize URLs by removing tracking parameters, fragments, and mirror-domain wrappers. Normalize company names and titles without deleting level terms. Construct `canonical_job_id` from employer domain plus requisition ID when reliable; otherwise use employer, normalized title, normalized location group, and description hash.

### 9.2 Duplicate detection

Apply, in order:

1. Exact canonical URL or requisition-ID match.
2. Exact normalized-text SHA-256 match.
3. Near-duplicate comparison after removing boilerplate, benefits, equal-opportunity text, and location lists.
4. Template similarity across one employer.

Flag candidate pairs when normalized title matches and text similarity is at least 0.90, or when MinHash/SimHash similarity exceeds the documented threshold. A human MUST adjudicate uncertain pairs in the 0.82–0.90 similarity band when both would enter the final sample.

### 9.3 Resolution rules

Keep the first-party, most complete, most recently verified record. Merge location variants under one requisition. Preserve aliases and duplicate links. If distinct levels share a template but materially different experience or scope, retain them but apply the per-template cap. Report duplicate counts and resolution reasons.

## 10. AI-assisted extraction and coding protocol

### 10.1 Permitted AI work

AI MAY propose inclusion decisions, atomic requirements, taxonomy mappings, aliases, seniority, strata, summaries, code, tests, visualizations, and article prose. Every AI call used in production MUST record provider/model identifier, model version where available, temperature or equivalent, prompt template version, input hash, output hash, timestamp, and retry count. Secrets and prohibited source content MUST NOT be sent to third-party models.

### 10.2 Deterministic-first principle

Use deterministic parsing for URLs, timestamps, hashes, schema validation, exact aliases, counts, and statistical calculations. Use AI for semantic interpretation only where rules and dictionaries are insufficient. Generated code MUST be reviewed, tested, pinned, and run in a controlled environment before its results are accepted.

### 10.3 Two-pass extraction

Pass A extracts candidate atomic requirements and evidence spans without taxonomy labels. Pass B maps each extracted item to the versioned taxonomy using only the excerpt and limited posting context. A validator rejects mappings with missing evidence, unsupported labels, invalid controlled values, or confidence below threshold.

### 10.4 Human verification requirements

Before publication, a human MUST:

1. Review all 150 inclusion decisions at least at title, employer, source, role-family, and rationale level.
2. Review every borderline inclusion, duplicate ambiguity, replacement, taxonomy addition, and post-freeze edit.
3. Review 100% of AI-related requirement rows and every AI trend claim.
4. Review all rows with confidence below 0.80 and all `unclear` requirement statuses included in analysis.
5. Audit a reproducible random sample of at least 20% of included jobs, stratified by role family, comparing every coded requirement with source text.
6. Verify every numerical headline, chart annotation, and quoted excerpt in the article.
7. Approve the frozen manifest and publication checklist.

Human verification MUST be represented by reviewer ID, timestamp, decision, and notes. A model reviewing another model does not satisfy “human.” If human review is unavailable, the run MAY produce a clearly watermarked draft but MUST NOT publish or update the canonical time series.

### 10.5 Agreement and correction

For the human-audited sample, calculate precision of extracted job-skill assertions and category-level agreement. Target precision is at least 0.95 overall and at least 0.90 for each top-level category with 10 or more audited assertions. Estimate recall on the audited jobs by having the human mark missed explicit requirements. Target recall is at least 0.90. Correct all discovered systematic errors across the full dataset, rerun analyses, and repeat the audit when a gate fails.

## 11. Analysis methods

### 11.0 Two analytical tracks

All labor-market results in Sections 11.1–11.6 belong to Track A. Track B uses the separate horizon-scan method in Sections 11.7–11.12. The article MUST not combine their observations into one denominator, trend line, or confidence interval.

### 11.1 Denominators and prevalence

The primary denominator is included unique jobs (`N=150`). For skill `s`:

`prevalence_s = number of unique jobs containing s / number of eligible included jobs with usable requirement text`.

Count each skill at most once per job. Report numerator, denominator, percentage, and Wilson 95% confidence interval. Report required, preferred, responsibility, and combined prevalence separately. Do not treat mentions as independent observations.

### 11.2 Stratified comparisons

Report a subgroup only when its denominator is at least 15; otherwise combine responsibly or suppress it. Show raw numerator and denominator. Use percentage-point differences and prevalence ratios with uncertainty. Label subgroup results descriptive; do not imply causal effects. For hypothesis tests, declare the family of comparisons, use Fisher’s exact or chi-square as appropriate, adjust for multiple testing using Benjamini–Hochberg, and report effect sizes rather than highlighting p-values alone.

### 11.3 Co-occurrence

Create a binary job-by-skill matrix. Restrict the main network to skills appearing in at least 5 jobs. For each pair report support count, joint prevalence, Jaccard similarity, lift, and phi coefficient. Require support of at least 5 to display a pair. Rank by a declared metric and never rank by lift alone when support is small.

`lift(A,B) = P(A and B) / (P(A) × P(B))`.

Use hierarchical clustering or community detection only as an exploratory view. Record algorithm, distance/edge definition, parameters, random seed, and package versions. Do not name clusters as market facts without human interpretation.

### 11.4 Trend analysis

Maintain both:

- Independent monthly cross-sections: each month’s 150-job prevalence.
- Matched/overlap sensitivity series: persistent postings or comparable strata, used to assess composition effects.

For month-over-month change, report percentage-point change and denominators. Do not call a skill “rising” or “falling” unless it meets the predeclared rule: same taxonomy definition, comparable samples, at least 5 occurrences in one of the two months, absolute change of at least 3 percentage points, and direction sustained for two consecutive updates or supported by a 3-month rolling estimate. Label the first observed change “watch,” not a trend.

Taxonomy changes MUST be backcast to prior raw evidence when feasible. If not feasible, break the series and annotate it. Never compare incompatible category definitions silently.

### 11.5 Sensitivity analyses

At minimum compare: first-party-only versus full sample; required-only versus combined; company-capped base versus one-posting-per-company; and sample with versus without AI/ML-for-biology role family. Material differences belong in limitations.

### 11.6 Missing data and weighting

Never impute an absent skill as present. If usable requirement text is incomplete, exclude the job from affected denominators and report it. Default results are unweighted. Experimental post-stratification weights MAY be shown separately only if a defensible external frame exists; document construction, trimming, and sensitivity.

### 11.7 AI capability horizon scan

Maintain a monthly evidence register of AI software-engineering capability and adoption signals. Prioritize primary, reproducible sources: benchmark maintainers and underlying datasets/code; peer-reviewed or fully documented research; standards bodies and regulators; model/system cards and technical reports; vendor release documentation with reproducible evaluations; and clearly described organizational field studies. Commentary, surveys without methods, social posts, demos, and marketing may identify leads but MUST NOT establish a capability claim alone.

For each item record: source URL/DOI, publisher, publication and retrieval dates, evidence type, model/agent/scaffold versions, benchmark/task definition, environment, permitted tools, task duration, repository/context scale, success metric, reliability threshold, human assistance, compute/cost, contamination controls, reproducibility status, limitations, conflicts/funding, and agent/human assessment.

### 11.8 Capability dimensions

Do not summarize progress with a single benchmark score. Track at least:

- Task success at both 50% and high-reliability thresholds such as 80% or 90%.
- Human-equivalent task duration and end-to-end elapsed time.
- Repository size, number of files/services, dependency complexity, and novelty.
- New implementation versus debugging, refactoring, migration, testing, operations, and maintenance.
- Degree of specification completeness and hidden-test independence.
- Autonomous tool use, planning horizon, retry budget, and human intervention.
- Correctness beyond tests: security, performance, maintainability, scientific validity, and reproducibility.
- Cost, latency, variance, failure modes, and regression across model/scaffold versions.

A benchmark result MUST be tied to the complete system—model, prompts, agent scaffold, tools, environment, and evaluation version—not attributed to the base model alone.

### 11.9 Capability evidence quality score

Score each source 0–2 on: task representativeness, evaluation independence, contamination controls, high-reliability reporting, system/configuration disclosure, reproducible artifacts, and relevance to scientific software. Sum to 0–14. Use 11–14 as strong, 7–10 as moderate, and 0–6 as weak evidence. Weak evidence may appear only in a labeled watch list and MUST NOT drive the central projection.

### 11.10 Adoption and organizational evidence

Capability is not adoption. Separately track: explicit AI-tool requirements in jobs; enterprise policy and governance; code-review and test burden; deployment frequency and stability; developer time allocation; defect/security outcomes; cost; human override rates; and incident reports. Distinguish controlled experiments, surveys, telemetry, case studies, and vendor claims. Report adoption evidence with its sampling limitations.

### 11.11 Scenario projections

Publish scenarios, never a single deterministic forecast. At minimum maintain:

- Incremental assistance: AI accelerates implementation, but humans remain primary authors and integrators.
- Agentic delegation: agents produce most routine code and changes; humans specify, contextualize, review, and validate.
- Supervised autonomy: agents own long-running subsystem work; human effort concentrates on architecture, scientific correctness, exceptions, and governance.
- Reliability or governance bottleneck: capability improves faster than trustworthy deployment, so verification, security, data rights, regulation, and organizational controls constrain adoption.

For each 12-, 24-, and 36-month horizon, state assumptions, leading indicators, disconfirming indicators, probability range rather than point probability, and implications for skills, hiring, education, and this book. A human forecasting editor MUST approve probabilities. The agent MUST preserve prior forecasts and score them later rather than overwriting them.

### 11.12 Projection discipline and backtesting

Every projection MUST identify its evidence cutoff date and use information available at that date. Avoid straight-line extrapolation from one benchmark. Use multiple evidence classes, include base rates and bottlenecks, and state uncertainty. Quarterly, compare prior predictions with realized indicators using Brier scores for probabilistic events and directional accuracy for ordinal claims. Report calibration failures. Scenario probabilities MUST NOT be presented as confidence intervals for job-market statistics.

## 12. Monthly update workflow

### Phase 0 — initialize

1. Create a dated branch and `run_id`.
2. Load the prior manifest, taxonomy, codebook, open issues, and known source failures.
3. Pin environments; record commit and dependency lock hashes.
4. Run schema, unit, and smoke tests before collection.

### Phase 1 — refresh and discover

1. Revisit prior included and reserve URLs; record active/closed/changed status.
2. Run the versioned discovery queries across the source mix.
3. Add new candidates to the append-only screening log.
4. Stop collection only after the candidate and reserve targets and diversity constraints are achievable.

### Phase 2 — screen, snapshot, and deduplicate

1. Apply eligibility rules and capture source evidence.
2. Compute canonical IDs, hashes, similarity candidates, and duplicate clusters.
3. Route borderline and duplicate ambiguities to human review.
4. Allocate the deterministic quota sample and reserve pool.

### Phase 3 — extract and code

1. Run two-pass atomic extraction and taxonomy mapping.
2. Validate evidence spans, schemas, controlled values, and within-job collapsing.
3. Review low-confidence and AI-related rows.
4. Freeze `sample_manifest.csv`; record its SHA-256.

### Phase 4 — analyze

1. Build job-skill matrices.
2. Run prevalence, stratified, co-occurrence, trend, and sensitivity analyses from scripts—not spreadsheet edits.
3. Generate data tables before charts; charts MUST derive from those tables.
4. Compare headline values with an independent recomputation test.
5. Refresh the AI capability evidence register and adoption indicators.
6. Update scenarios from predeclared indicators, preserve the previous forecast, and record forecast changes with reasons.

### Phase 5 — human QA and publication

1. Complete the audit sample and correct systematic errors.
2. Run privacy, copyright, accessibility, broken-link, schema, provenance, and reproducibility gates.
3. Draft the article from verified result artifacts.
4. Human approves the manifest, article, and publication checklist.
5. Merge and publish; verify the public page and downloadable artifacts.

### Phase 6 — archive and learn

1. Tag the release `market-analysis-YYYY-MM`.
2. Save run metadata, immutable derived data, checksums, logs, and a compact snapshot according to retention policy.
3. Open issues for source failures, taxonomy proposals, and methodological deviations.
4. Update the run ledger and next-month watch list.

## 13. Replacements and panel continuity

An included posting that closes before freeze is replaced from the same stratum where possible. Record `replacement_for_job_id` and reason. After freeze, do not replace records merely because they close; the sample represents the verified collection window. Correct only factual/data errors through the change log and rerun all affected outputs.

Each month is a refreshed cross-section: active prior postings may remain, but the deterministic allocation and caps apply anew. Report overlap count with the prior month so readers can interpret change.

## 14. Reproducibility and engineering requirements

- All production analysis MUST run from a single documented command or workflow in a clean environment.
- Pin direct and transitive dependencies with lockfiles; record language/runtime versions.
- Store configuration, queries, prompts, schemas, taxonomy, and analysis parameters under version control.
- Use deterministic seeds and stable sorting. Record any nondeterministic component.
- Separate raw snapshots, interim data, validated data, and published aggregates.
- Never hand-edit generated CSV, JSON, chart, or article statistic. Fix source/config/code and regenerate.
- Validate inputs and outputs against schemas. Fail closed on invalid records.
- Generate SHA-256 checksums for frozen manifest, validated datasets, result tables, and publication assets.
- CI MUST run unit tests, schema checks, extraction fixtures, deduplication fixtures, statistical spot checks, article build, link checks, and accessibility checks.
- Keep secrets outside the repository; use least privilege and redact logs.
- A README MUST document setup, permitted data retention, commands, expected runtime/cost, and troubleshooting.

## 15. Repository structure

```text
/
├── README.md
├── LICENSE
├── CITATION.cff
├── CHANGELOG.md
├── pyproject.toml                  # or equivalent pinned project manifest
├── lockfile
├── config/
│   ├── study.yaml
│   ├── sources.yaml
│   ├── queries.yaml
│   └── strata.yaml
├── schemas/
│   ├── jobs.schema.json
│   ├── requirements.schema.json
│   ├── evidence.schema.json
│   └── codebook.yaml
├── taxonomy/
│   ├── taxonomy.yaml
│   └── CHANGELOG.md
├── prompts/
│   ├── inclusion_vNN.md
│   ├── extraction_vNN.md
│   └── classification_vNN.md
├── src/market_analysis/
│   ├── discover.py
│   ├── capture.py
│   ├── screen.py
│   ├── deduplicate.py
│   ├── extract.py
│   ├── classify.py
│   ├── analyze.py
│   ├── visualize.py
│   └── publish.py
├── tests/
│   ├── fixtures/
│   ├── test_schemas.py
│   ├── test_deduplication.py
│   ├── test_extraction.py
│   └── test_statistics.py
├── data/
│   ├── raw/YYYY-MM/               # restricted or gitignored where required
│   ├── interim/YYYY-MM/
│   ├── validated/YYYY-MM/
│   └── published/YYYY-MM/
├── reports/YYYY-MM/
│   ├── run_report.md
│   ├── audit_report.md
│   ├── deviations.md
│   └── checksums.sha256
├── site/
│   ├── _posts/YYYY-MM-DD-bioinformatics-job-market.md
│   ├── assets/YYYY-MM/
│   └── downloads/YYYY-MM/
└── .github/workflows/
    ├── test.yml
    ├── monthly-draft.yml
    └── publish.yml
```

Raw source material MUST be gitignored when redistribution is restricted. Publish only lawful excerpts and aggregate/derived data.

## 16. Required outputs

### 16.1 Data and audit artifacts

Each run MUST produce:

- `screening_log.csv` for all candidates.
- `sample_manifest.csv` containing 150 included jobs.
- `jobs.csv`, `requirements.csv`, `evidence.csv`, and `taxonomy.csv` or Parquet equivalents plus CSV exports.
- `prevalence_overall.csv`, `prevalence_by_stratum.csv`, `cooccurrence_pairs.csv`, `monthly_trends.csv`, and `sensitivity_results.csv`.
- `run_metadata.json`, `data_dictionary.md`, `methods.md`, `limitations.md`, `audit_report.md`, `deviations.md`, and `checksums.sha256`.
- `ai_capability_evidence.csv`, `adoption_signals.csv`, `scenario_forecasts.csv`, `forecast_scorecard.csv`, and `horizon_scan_methods.md`.
- Machine-readable chart data and accessible chart images.

### 16.2 GitHub Pages article

The article MUST contain:

1. A plain-language headline and “data collected” date range.
2. A concise “what we studied” box with N, geography, source mix, and sampling caveat.
3. Top software-engineering competencies with counts, percentages, and uncertainty.
4. Required-versus-preferred comparison.
5. AI-related findings that distinguish AI-assisted development from AI/ML role content.
6. Co-occurrence findings with minimum-support disclosure.
7. Role-family or seniority contrasts that meet denominator rules.
8. Month-over-month and longer-term findings, or an explicit baseline statement for the first run.
9. Methods, limitations, conflicts/funding if applicable, last-updated date, spec/taxonomy versions, and correction link.
10. Links to downloadable aggregate data, code, prior editions, and reproducibility instructions.
11. A clearly separated “AI capability horizon” section showing measured capability, adoption evidence, scenarios, uncertainties, leading indicators, and implications for durable engineering competencies.
12. A “skills for an agentic future” section that distinguishes code production from codebase comprehension, verification, reproducibility, scientific correctness, security, stewardship, and governance.

Every factual claim MUST trace to a generated result table; every source quotation MUST trace to an evidence record. Avoid employer rankings, individual-company criticism, or claims about hiring intent beyond posting text.

### 16.3 Accessibility and presentation

Charts MUST have descriptive titles, units, direct labels where practical, color-blind-safe palettes, adequate contrast, and text alternatives or adjacent data tables. Do not encode meaning by color alone. The page MUST work on mobile, pass the project’s accessibility check, and avoid interactive-only access to essential results.

## 17. Quality gates

Publication is blocked unless every mandatory gate passes:

| Gate | Pass condition |
|---|---|
| Sample size | Exactly 150 included, active-at-freeze, unique jobs |
| Eligibility | 150/150 meet all inclusion criteria; human review complete |
| Diversity | Company/template caps and declared role/sector floors pass, or approved scarcity deviation exists |
| First-party evidence | At least 70% first-party sources, or approved documented exception |
| Provenance | 100% of included jobs have URL, retrieval time, active check, hash, and source type |
| Evidence linkage | 100% of analyzed job-skill assertions link to verbatim evidence |
| Schema validity | Zero validation errors in frozen inputs and published outputs |
| Duplicate control | Zero unresolved duplicate pairs in final sample |
| AI review | 100% of AI-related assertions and claims human-verified |
| Low-confidence review | 100% of included rows below 0.80 human-adjudicated |
| Audit precision | ≥0.95 overall and ≥0.90 by sufficiently represented top-level category |
| Audit recall | ≥0.90 on human-audited jobs |
| Numerical integrity | Independent recomputation matches all headline figures within rounding tolerance |
| Reproducibility | Clean run recreates published tables and checksums for deterministic artifacts |
| Tests/CI | All required tests, build, links, privacy, and accessibility checks pass |
| Human approval | Named reviewer signs manifest and publication checklist |
| Horizon provenance | 100% of capability and adoption claims link to registered evidence with evidence-type labels |
| Projection separation | No scenario or forecast is represented as a finding from the 150-job sample |
| Forecast governance | Probabilities and material scenario changes receive human approval; prior forecasts are preserved |
| Scientific assurance | Article distinguishes test passage, software correctness, analytical validity, and biological validity |

Warnings such as fewer than 20 reserves, subgroup scarcity, or source outages may permit a documented publication. Any failed mandatory gate produces a draft only.

## 18. Failure handling

### 18.1 Source unavailable or blocked

Retry with exponential backoff within rate limits, then try the canonical employer source or an allowed full-text source. Never bypass controls. Mark the candidate unavailable and replace it. Record domain, error class, attempt count, and final disposition.

### 18.2 Insufficient eligible jobs

Expand discovery queries and approved sources without changing geography or eligibility. Extend collection up to seven days. If fewer than 150 eligible unique jobs remain, do not dilute criteria silently. Publish no canonical monthly estimate; produce a failure report or a human-approved, prominently labeled reduced-sample special edition that is excluded from the main time series.

### 18.3 Model/API failure

Retry idempotently with capped attempts. Resume from checkpoints. A fallback model requires an explicit logged configuration change and validation against extraction fixtures. Do not mix model outputs without recording model per row.

### 18.4 Schema, test, or reproducibility failure

Stop the pipeline. Quarantine invalid artifacts, correct code/config/source, rebuild from the last trusted stage, and rerun downstream analyses. Never patch published numbers manually.

### 18.5 Human-review delay

Generate a noncanonical draft labeled “Not human verified—do not cite.” Do not deploy it to the production GitHub Pages path and do not append it to trends.

### 18.6 Post-publication correction

Open a correction issue, preserve the original release/tag, correct through the pipeline, increment the rerun suffix and patch version, add a dated correction note, regenerate checksums, and disclose whether conclusions changed. Never rewrite history without notice.

### 18.7 Taxonomy drift

Propose changes through a pull request containing definition, motivation, examples, exclusions, mapping/backcast plan, and time-series impact. Minor versions add compatible nodes or aliases; major versions change meaning or hierarchy; patch versions correct metadata/typos.

## 19. Acceptance criteria

The autonomous agent’s assignment is complete only when:

1. A frozen, checksum-identified manifest contains exactly 150 eligible, active-at-freeze, deduplicated postings.
2. Sampling caps, strata, source hierarchy, and all deviations are machine-checked and documented.
3. Every analyzed skill assertion is atomic, taxonomy-coded, status-coded, confidence-scored, and linked to preserved verbatim evidence.
4. AI-related assertions, borderline cases, duplicates, low-confidence rows, replacements, taxonomy changes, and a stratified 20% audit have human decisions on record.
5. Required analyses and sensitivity checks run from version-controlled code and emit validated tables.
6. All headline values independently recompute from the frozen data.
7. The GitHub Pages article meets the required content, traceability, limitation, accessibility, and correction requirements.
8. A clean pinned environment reproduces deterministic results and passes CI.
9. The repository contains run metadata, schemas, codebook, taxonomy version, prompt versions, model provenance, checksums, audit report, and publication approval.
10. The public page and downloads are verified after deployment, and the release is tagged.
11. The AI capability horizon scan is current to the declared cutoff, evidence-scored, separated from observed job data, and includes multiple scenarios with falsifiable indicators.
12. The article explains how engineering competence changes if agents generate most code, including the continuing need for codebase comprehension, verification, reproducibility, scientific correctness, maintenance, security, provenance, and accountable governance.

“Mostly complete,” “plausible,” or “AI-reviewed” does not satisfy acceptance when a mandatory human or quantitative gate is missing.

## 20. Agent operating instructions

At the start of every run, the agent MUST print or write a run plan naming the spec version, collection window, target N, prior run, model/config versions, and expected human checkpoints. It MUST maintain an append-only decision log and checkpoint after each phase. It MUST stop and request human direction when a proposed action would change scope, inclusion rules, taxonomy meaning, publication status, legal/terms assumptions, or a mandatory quality threshold.

The agent SHOULD communicate progress using counts: candidates discovered, screened, eligible, duplicate, included, reserve, evidence-validated, human-reviewed, and gates passed. It MUST distinguish a recoverable warning from a blocking failure. It MUST not claim completion until Section 19 is satisfied.

## 21. Configuration defaults

```yaml
study_id: BSE-JMA-001
spec_version: 1.1.1
geography: US
target_n: 150
minimum_candidate_pool: 220
minimum_reserve_pool: 20
collection_window_days_max: 7
company_cap: 5
template_cap: 3
minimum_first_party_fraction: 0.70
human_audit_job_fraction: 0.20
low_confidence_threshold: 0.80
exclude_confidence_below: 0.60
near_duplicate_review_band: [0.82, 0.90]
main_skill_min_support: 5
cooccurrence_min_support: 5
subgroup_min_n: 15
trend_min_absolute_percentage_points: 3
trend_confirmation_updates: 2
audit_precision_target: 0.95
audit_category_precision_target: 0.90
audit_recall_target: 0.90
random_seed: 202608
horizon_scan_cadence: monthly
horizon_scenarios: [incremental_assistance, agentic_delegation, supervised_autonomy, reliability_governance_bottleneck]
horizon_months: [12, 24, 36]
capability_evidence_strong_min: 11
capability_evidence_moderate_min: 7
forecast_backtest_cadence: quarterly
```

## 22. Human sign-off record

The monthly pull request MUST include this completed block:

```text
Run ID:
Manifest SHA-256:
Spec version:
Taxonomy version:
Collection window:
Included / reserve / screened:
Audit sample size:
Audit precision / recall:
Mandatory gates passed: yes / no
Approved deviations:
Reviewer name or ID:
Review timestamp (UTC):
Publication approved: yes / no
Reviewer notes:
```

## Appendix A. Decision reason codes

Recommended controlled codes include `include_meets_all`, `exclude_academic`, `exclude_internship`, `exclude_wet_lab`, `exclude_not_life_science`, `exclude_not_engineering`, `exclude_geography`, `exclude_inactive`, `exclude_incomplete_text`, `exclude_duplicate`, `exclude_company_cap`, `exclude_template_cap`, `exclude_source_unverifiable`, `pending_human`, and `reserve_quota`.

## Appendix B. Minimum monthly run report

The run report MUST record funnel counts, source mix, company/sector/role distributions, prior-month overlap, replacement events, extraction/model versions, human review coverage, audit metrics, failed/retried sources, taxonomy changes, deviations, gate results, runtime/cost summary, and known limitations.

## Appendix C. Living-specification governance

This document is the normative baseline. Modify it only through reviewed pull requests. Record rationale and migration impact in `CHANGELOG.md`.

- Patch: wording, clarification, or nonsemantic correction.
- Minor: backward-compatible field, taxonomy node, output, or workflow addition.
- Major: population, geography, sampling design, primary metric, taxonomy meaning, or quality-threshold change that can break comparability.

Each monthly article MUST cite the exact specification and taxonomy versions. The agent MAY propose improvements but MUST NOT self-approve a specification change.

## Appendix D. Baseline horizon-scan source families

The agent MUST refresh this list rather than treating it as permanent. Initial source families include reproducible real-repository software-engineering benchmarks such as SWE-bench and its human-validated variants; task-horizon evaluations that report reliability and human-equivalent task duration; secure software-development and AI risk-management guidance such as the NIST SSDF, AI RMF, and Generative AI Profile; peer-reviewed scientific-software validation literature; incident databases; and methodologically transparent studies of AI adoption and software-delivery outcomes.

Benchmark leaderboards are inputs, not forecasts. Standards are governance evidence, not capability measurements. Vendor system cards are first-party evidence and MUST be labeled accordingly. No single source family may determine the scenario narrative.
