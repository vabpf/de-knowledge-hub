# Maintenance Workflow

Run `uv run python scripts/hub.py freshness` before a maintenance batch. This is a
review queue, not proof of upstream change. Version-scoped content is due after 180
days; general concepts after 365, or use --days. Explicit stale status always appears.

Choose at most 3–5 pages. Reopen their registered primary references; check versions,
example assumptions, deprecated APIs, and contradictory claims. Reuse existing source
records for unchanged documents. Update sources only after actually consulting them.
Never advance verified_at just because a build passed. Keep research notes under design/.

If evidence is inconclusive, mark the article and mirrored registry row stale and
record the uncertainty. If a claim is wrong, correct it with a source-backed explanation.
If a proposed update fails technical review, keep it in drafts/ or retain the prior
approved version. Do not silently replace verified content with an unreviewed rewrite.

Run validation, tests, build, and relevant examples. Report the old/new scope, evidence,
uncertainties, and validation results. Remote PRs, pushes, merges, and deployments
remain separately authorized. Never schedule autonomous generation by default.
