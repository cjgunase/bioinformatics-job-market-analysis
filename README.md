# Bioinformatics Job Market Analysis

An evidence-backed, reproducible system for studying software-engineering and
AI competencies in U.S. bioinformatics and computational-biology job postings.

The project follows specification `BSE-JMA-001` version `1.1.1`. Development is
deliberately incremental: an unattended midnight run completes at most one
milestone per day and records its evidence in the repository.

## Status

The project is in staged implementation. See [the roadmap](docs/ROADMAP.md) and
[progress log](docs/PROGRESS.md).

Canonical market findings will not be published until all mandatory quality
gates—including human review—pass. Unreviewed outputs will be labeled drafts.

## Source specification

The approved baseline is preserved as [BSE-JMA-001 version
1.1.1](docs/specification/BSE-JMA-001-v1.1.1.md). Its provenance and pinned
SHA-256 digest are documented in the [specification
README](docs/specification/README.md).

## Development setup

The development environment is pinned to Python 3.13.11 and uv 0.9.27. Install
[uv](https://docs.astral.sh/uv/), then create the locked environment:

```bash
uv python install "$(cat .python-version)"
uv sync --locked --all-groups
```

Run the same baseline checks as CI:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest
uv build --no-build-isolation
```

The `uv.lock` file pins transitive dependencies. Update it only as a reviewed
toolchain or dependency change.

## Data handling

Never commit secrets, cookies, applicant data, or restricted full job text.
Raw and interim job-source material belongs under the gitignored `data/raw/`
and `data/interim/` paths when lawful retention is permitted. Public artifacts
must contain only permitted excerpts, provenance metadata, derived values, and
aggregates.

## License

Code is released under the MIT License. Job-posting evidence remains subject to
its original sources' terms; restricted raw text must never be committed.
