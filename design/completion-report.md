# Knowledge Hub Completion Report

Verified October 19, 2026. The initial local platform and eight-article corpus are
complete. Optional Cloudflare hosting is prepared, not activated, as requested.
Finalized for the owner-authorized local commit on October 20, 2026. The local preview
is stopped. No push, pull request, merge, remote deployment, or access change was performed.
GitHub privacy/settings remain unverified.

## Delivered

- Eight connected articles across all six content types, with guided reading paths,
  problem-oriented entry points, domain navigation, local search, and cross-links.
- Twelve reusable primary source records with URLs, versions/editions, and review dates.
  Sources and applicable versions are validated against article metadata.
- Four prioritized planned topics, a deterministic canonical inventory, derived
  relationship export, bounded dependency-aware planning, and read-only freshness reports.
- One-agent planning/research/writing/review/maintenance instructions. Review reports
  can accept, revise, or reject; rejected content remains outside the publication tree.
- Structural, duplicate-title, source, graph, link, navigation, publication-boundary,
  executable-example, and real-browser regression checks, with read-only validation CI.
- Optional manual static-asset deployment, an ignored-config generator, an unauthenticated
  Access probe, and an explicit bootstrap/update/rollback guide. No custom backend.

## Topics

Existing IDs retained and their article/registry source relationships updated:
`distributed-systems/partitioning`, `distributed-systems/data-shuffling`.

New articles, delivered in two batches of three:
`foundations/distributed-computing`, `processing/apache-spark`,
`processing/spark-execution-model`, `distributed-systems/data-skew`,
`processing/incremental-data-loading`, `orchestration/airflow-vs-dagster`.

Planned only: Spark Shuffle, Adaptive Query Execution, Change Data Capture, and
Dimensional Modeling. No hundreds-page corpus or autonomous scheduled generation added.

## Verification evidence

| Command/check | Result |
| --- | --- |
| uv sync --locked | Passed in a fresh source-only copy with a new virtual environment |
| uv run python scripts/validate.py | Passed, zero errors |
| uv run pytest | 88 passed |
| uv run zensical build | Passed; Zensical reported no issues |
| Draft publication integration test | A valid registered draft was absent from built HTML and search output |
| Self-contained article examples | Four examples executed successfully in tests |
| Spark example | Syntax checked; not executed against Spark/Java |
| uv run --group browser python scripts/check_browser.py | Passed in Firefox at 1440×1000 and 390×844 |
| Browser interactions | All eight article URLs/headings, no page-width overflow, real search results/navigation, mobile domain menu, and article cross-links passed |
| Browser appearance | Desktop/mobile screenshots inspected; transparent search panel corrected and an opacity assertion added |
| Optional hosting tests | Manual gates, static-only config, disabled provider/preview URLs, expected-login redirects, and rejection of public responses passed locally |
| Git/source hygiene | Whitespace/syntax checks passed; output, environments, screenshots, local hosting config, .env, and .dev.vars are ignored |

The required setup/validation/test/build sequence passed in a fresh source-only
directory without a commit or remote access. Browser verification used the generated
local site. Screenshots remain in ignored browser-results/. Validation and deployment
workflows are configured but have not executed on GitHub.

## Reading and operations guides

- [README](../README.md): start reading and repository map.
- [Runbook](runbook.md): local operation, bounded content batches, source/review standards,
  inventory, planning, freshness, and browser commands.
- [Optional hosting](hosting.md): Cloudflare Access setup, placeholder-only bootstrap,
  manual GitHub deployment, updates, account checks, and rollback.
- [Initial corpus review](review-initial-corpus.md): source-to-topic evidence and limitations.

## Sources and technical review limits

Technical sources include the original MapReduce paper, Spark 3.5.7 documentation,
PostgreSQL 16 documentation, Airflow 3.1.0 documentation, and Dagster documentation
labeled 1.13.26 when consulted. Exact URLs and dates are in registry/sources.yaml and
each article's References. Engine versions are explicit, not claims of current latest
releases. The agent performed a sequential author/review workflow; no independent
human signoff or live distributed-system exercise is implied.

Presentation and hosting references consulted:

- [Zensical search](https://zensical.org/docs/setup/search/)
- [Zensical customization](https://zensical.org/docs/customization/)
- [Zensical fonts](https://zensical.org/docs/setup/fonts/)
- [Cloudflare static assets](https://developers.cloudflare.com/workers/static-assets/get-started/)
- [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [Cloudflare Access](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)
- [Version URL controls](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/)
- [Wrangler GitHub Action](https://github.com/cloudflare/wrangler-action)

The small search presentation script adjusts an opacity token inside Zensical's open
search shadow root; it leaves Markdown portable. Browser regression checks will catch
an upstream widget change that invalidates this override. System fonts avoid font-service
requests. Browser testing is not a comprehensive accessibility or physical-device audit.

## Environment

Normal setup uses Python 3.12 and locked dependencies. In this Termux/PRoot session,
verification used Linux uv 0.11.6 and managed Python 3.12.13 under /tmp, as described
in the historical M1 verification record. The optional group locks Playwright 1.64.0.
Chromium could not create pages in this environment; Firefox 157.0 passed with
MOZ_DISABLE_CONTENT_SANDBOX=1. Browser binaries live under /tmp/de-hub-browsers, and
Playwright's required system libraries were installed for local verification. These
compatibility settings are not website or production settings. CI uses standard
headless Firefox on Ubuntu.

## Remaining owner choices

No local implementation blockers remain. Hosting activation is optional and requires
a real hostname/account, policies/allowlist, credentials, protected GitHub environment,
and explicit deployment authorization. Unauthenticated URL probes do not discover every
alias or prove allowed/denied identity behavior; the hosting guide requires those live
checks separately. PySpark and orchestration trial behavior needs environment-specific
execution before relying on it operationally. Future content grows in reviewed batches.

## Source files

The repository began without commits; all files below belong to the initial implementation.
Existing M1 files were extended in place; no canonical articles or topic IDs were deleted.
The temporary ineffective CSS override was removed before completion. This inventory
excludes generated site files, caches, environments, screenshots, and local secrets.

- `.gitattributes`
- `.github/workflows/deploy.yml`
- `.github/workflows/validate.yml`
- `.gitignore`
- `.python-version`
- `AGENTS.md`
- `README.md`
- `agents/maintenance.md`
- `agents/planning.md`
- `agents/research.md`
- `agents/review-report-template.md`
- `agents/review.md`
- `agents/writing.md`
- `design/architecture.md`
- `design/completion-report.md`
- `design/content-model.md`
- `design/hosting.md`
- `design/m1-verification.md`
- `design/review-initial-corpus.md`
- `design/roadmap.md`
- `design/runbook.md`
- `docs/architecture/.gitkeep`
- `docs/cloud/.gitkeep`
- `docs/data-modeling/.gitkeep`
- `docs/databases/.gitkeep`
- `docs/distributed-systems/.gitkeep`
- `docs/distributed-systems/data-shuffling.md`
- `docs/distributed-systems/data-skew.md`
- `docs/distributed-systems/partitioning.md`
- `docs/foundations/.gitkeep`
- `docs/foundations/distributed-computing.md`
- `docs/index.md`
- `docs/javascripts/search-readability.js`
- `docs/orchestration/.gitkeep`
- `docs/orchestration/airflow-vs-dagster.md`
- `docs/processing/.gitkeep`
- `docs/processing/apache-spark.md`
- `docs/processing/incremental-data-loading.md`
- `docs/processing/spark-execution-model.md`
- `docs/troubleshooting/.gitkeep`
- `drafts/.gitkeep`
- `pyproject.toml`
- `registry/sources.yaml`
- `registry/taxonomy.yaml`
- `registry/topics.yaml`
- `schemas/article.schema.json`
- `schemas/source.schema.json`
- `schemas/topic.schema.json`
- `scripts/__init__.py`
- `scripts/check_browser.py`
- `scripts/check_private.py`
- `scripts/generate_inventory.py`
- `scripts/hub.py`
- `scripts/prepare_cloudflare.py`
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
- `tests/test_examples.py`
- `tests/test_hosting.py`
- `tests/test_hub.py`
- `tests/test_validation.py`
- `uv.lock`
- `zensical.toml`
