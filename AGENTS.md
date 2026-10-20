# Codex Operating Contract

## Discover

Read README.md, design/content-model.md, registry/topics.yaml, registry/taxonomy.yaml,
existing articles, and the relevant template before editing. Preserve canonical IDs
when moving pages. Inspect git status and preserve unrelated work.

## Plan

Describe a bounded set of topics and files for the requested change. Avoid bulk
knowledge generation. Default to 3–5 new articles per batch. The current completion
request authorizes the eight-topic initial scope and supporting local workflows.

## Research

Prefer official documentation, standards, papers, and other primary sources. Record
identifiable URLs, product versions, verification dates, and unresolved uncertainty.
Do not invent citations or treat structural validation as factual verification.

## Generate

Follow templates and schemas. Register topics before creating articles. Keep planned
topics pathless; put draft/review articles in drafts/. Only approved published/stale
articles enter docs/. The current request authorizes locally published initial-scope articles after source
and technical review; future batches need user-approved scope. Update relative links and navigation
when moving articles, retaining their IDs. An implementation edge points from a
general topic to a technology article. Read agents/ guides for each workflow phase. Use agents/maintenance.md for freshness
reviews and design/runbook.md for repeatable commands. Article frontmatter is canonical
for written content; registry mirrors are validated, not independently edited facts.
Store primary source IDs in sources, version scope in applies_to, and prioritize
backlog rows with priority. A rejected review stays outside docs/.

## Validate

Run `uv run python scripts/validate.py`, `uv run pytest`, and
`uv run zensical build` before completion. Report failures and limitations honestly.
Use `uv sync --locked` in a clean checkout. Do not hand-edit uv.lock.

## Permissions

Reading, analysis, approved file edits, and local validation are allowed. Opening a
pull request requires approval. Merging, pushing, deploying, changing repository
visibility or access, and any other external repository mutation require explicit
authorization. Never publish generated site output or upload it as a CI artifact.
These instructions complement actual credentials, branch protection, and access controls.
Do not use sub-agents unless explicitly requested by the user.

## Completion report

Report files added/modified/deleted; topics created/updated; sources consulted and
unresolved uncertainties; validation commands and results; remaining work/blockers.
Do not claim hosting privacy or browser usability has been verified without evidence.
