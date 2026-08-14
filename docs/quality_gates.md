# Quality-gate execution

Automated gates fail closed for secret-like content, oversized excerpts or
published full-text paths, missing SVG/table semantics, malformed public URLs,
and incomplete provenance. CI runs these checks against synthetic fixtures and
the draft build. Production additionally requires schema validity, exact sample
size, eligibility, diversity, first-party share, evidence linkage, duplicate
resolution, independent recomputation, clean-run checksums, and source/horizon
provenance.

Automation cannot pass human gates. Inclusion/manifest review, ambiguity and AI
review, low-confidence adjudication, the stratified 20% audit, numerical and
quotation verification, forecast probability approval, deviations, and final
publication sign-off remain explicitly pending until a named human records a
decision and UTC timestamp.
