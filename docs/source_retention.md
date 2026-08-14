# Source retention policy

Full job text is never committed by default. For
`excerpt_hash_metadata_only`, the pipeline stores only provenance, the complete
normalized-text hash, and a short evidence excerpt (maximum 500 characters).
Where current source terms clearly permit local research retention,
`restricted_full_snapshot` writes to gitignored `data/raw/`; permitted
redistributable text may use `permitted_full_snapshot`, but publication remains
subject to the copyright gate. Cookies, credentials, tokens, applicant data,
login-only content, and private pages are prohibited in every mode.

Every snapshot records retrieval/verification metadata through the job and
evidence schemas. A missing terms determination defaults to excerpt/hash only.
Removal from a public site does not retroactively authorize republication.
