# M1 Verification Record

Historical M1 snapshot. See [current completion evidence](completion-report.md) for the expanded hub.

Verified October 19, 2026. Foundation implemented locally; no commit, push, PR,
merge, hosting, publication, or access change performed.

## Evidence

- `uv sync --locked`: passed using Python 3.12.13 and uv 0.11.6.
- `uv run python scripts/validate.py`: passed, zero errors.
- `uv run pytest`: 47 passed, including deliberately invalid metadata, IDs, dates,
  relationship targets, prerequisite cycles, links, anchors, publication paths,
  navigation, missing articles, and required fields.
- `uv run zensical build`: passed with Zensical 0.0.71; no issues reported.
- Repeated all four commands in a fresh source-only directory with a new virtual
  environment under `/tmp`; all passed. This simulates clean-checkout setup without
  creating a commit or contacting the repository remote.
- Loopback `zensical serve` smoke check: home and both article URLs returned HTTP 200;
  server stopped after verification.
- Inventory determinism tested; generated inventory contains two topics.
- Generated search index includes both sample titles and excludes template placeholders.
- Generated article HTML contains reciprocal article links.
- Ignore rules exclude site output, virtual environment, pytest cache, and .env.

## Final acceptance audit

All local M1 Definition of Done criteria pass:

| Criterion | Evidence |
| --- | --- |
| Clean setup using documented commands | Fresh source copy with a new virtual environment; locked sync passed |
| Both sample articles conform | Schema, registry, and graph validation passed |
| Navigable local site | Build passed; preview served all three pages; rendered cross-links resolve |
| Invalid metadata and links fail | 47 regression tests passed, including negative cases and CLI exit status |
| Instructions support adding articles | Six template-to-draft workflows tested, plus lifecycle and stable-ID moves |
| No unauthorized external changes | All implementation remains local and uncommitted; no deployment configured |

The final audit fixed landing-page registration bypass, malformed-link diagnostics,
and an inventory assertion that assumed there would always be exactly two topics.
It also rejects symlink assets throughout docs/, including unlinked files, so static
asset copying cannot pull draft files into the publication tree. Added positive tests
for technology implementation edges and all six templates, and negative tests for
unknown domains, unregistered articles, CRLF, missing frontmatter, and symlink exposure.
The sample Python code was executed successfully; generated search membership and
rendered article links were rechecked. The full locked-install/validation/test/build
sequence passed again in a new source-only directory after these fixes.

Files updated during this audit: scripts/validate.py, tests/test_validation.py,
design/content-model.md, and this verification record. No topics were added, changed,
or deleted. No additional external research was required; the sources below remain
the implementation references. No local M1 blockers remain. This does not mark the
full MVP or M2 as complete.

## Environment and limitations

The bundled Python is a Termux/Android build and could not install uv from PyPI.
Verification used a standalone Linux uv binary in `/tmp/uv-aarch64-unknown-linux-musl`
and uv-managed Linux Python under `/tmp/de-hub-python`, with cache under
`/tmp/de-hub-cache`. These tools are temporary and not repository dependencies.
For this session, prefix commands with:

```bash
export PATH="/tmp/uv-aarch64-unknown-linux-musl:$PATH"
export UV_PYTHON_INSTALL_DIR=/tmp/de-hub-python
export UV_CACHE_DIR=/tmp/de-hub-cache
```

A supported desktop/Linux setup with uv installed uses the README commands directly.
No browser automation was run: interactive search, responsive layout, and keyboard
usability still require M2 review. Repository privacy and Cloudflare authentication
remain unverified and deployment is deferred. CI is configured but has not run on GitHub.
Validation is structural and does not establish factual accuracy or external link availability.

## Topics and sources

Created `distributed-systems/partitioning` and `distributed-systems/data-shuffling`.
No existing topics were modified or deleted. The M1 request authorizes these samples.

Consulted primary sources:

- [Zensical basics](https://zensical.org/docs/setup/basics/)
- [Zensical navigation](https://zensical.org/docs/setup/navigation/)
- [Apache Spark 3.5.7 RDD guide](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html)
- [Cloudflare preview deployment access policies](https://developers.cloudflare.com/pages/configuration/preview-deployments/)

Engine examples are explicitly versioned or illustrative. Future engine versions and
hosting policies require rechecking at adoption/deployment time.

## Files

All files below are newly added local files. No tracked files were modified or deleted.
Generated files and environments are ignored, not included here.

- `.gitattributes`
- `.github/workflows/validate.yml`
- `.gitignore`
- `.python-version`
- `AGENTS.md`
- `README.md`
- `agents/planning.md`
- `agents/research.md`
- `agents/review.md`
- `agents/writing.md`
- `design/architecture.md`
- `design/content-model.md`
- `design/m1-verification.md`
- `design/roadmap.md`
- `docs/architecture/.gitkeep`
- `docs/cloud/.gitkeep`
- `docs/data-modeling/.gitkeep`
- `docs/databases/.gitkeep`
- `docs/distributed-systems/.gitkeep`
- `docs/distributed-systems/data-shuffling.md`
- `docs/distributed-systems/partitioning.md`
- `docs/foundations/.gitkeep`
- `docs/index.md`
- `docs/orchestration/.gitkeep`
- `docs/processing/.gitkeep`
- `docs/troubleshooting/.gitkeep`
- `drafts/.gitkeep`
- `pyproject.toml`
- `registry/taxonomy.yaml`
- `registry/topics.yaml`
- `schemas/article.schema.json`
- `schemas/topic.schema.json`
- `scripts/__init__.py`
- `scripts/generate_inventory.py`
- `scripts/validate.py`
- `templates/comparison.md`
- `templates/concept.md`
- `templates/mechanism.md`
- `templates/pattern.md`
- `templates/problem.md`
- `templates/technology.md`
- `tests/fixtures/bad-date.json`
- `tests/fixtures/bad-nav.json`
- `tests/fixtures/broken-html.json`
- `tests/fixtures/broken-image.json`
- `tests/fixtures/broken-link.json`
- `tests/fixtures/broken-reference-link.json`
- `tests/fixtures/cycle.json`
- `tests/fixtures/draft-in-docs.json`
- `tests/fixtures/draft-leak.json`
- `tests/fixtures/duplicate-id.json`
- `tests/fixtures/future-date.json`
- `tests/fixtures/invalid-id.json`
- `tests/fixtures/mismatch.json`
- `tests/fixtures/missing-anchor.json`
- `tests/fixtures/missing-article.json`
- `tests/fixtures/missing-field.json`
- `tests/fixtures/missing-section.json`
- `tests/fixtures/missing-target.json`
- `tests/fixtures/no-source.json`
- `tests/fixtures/planned-with-path.json`
- `tests/fixtures/self-reference.json`
- `tests/fixtures/unknown-field.json`
- `tests/fixtures/unknown-tag.json`
- `tests/fixtures/valid.json`
- `tests/fixtures/wrong-implementation.json`
- `tests/test_validation.py`
- `uv.lock`
- `zensical.toml`
