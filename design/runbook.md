# Knowledge Hub Runbook

## Read locally

```bash
uv sync --locked
uv run python scripts/validate.py
uv run pytest
uv run zensical build
uv run zensical serve --dev-addr 127.0.0.1:8000
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. No account or hosting is required. Keep
the unauthenticated development server on loopback. For this session's Termux/Linux
tooling paths, see [M1 verification](m1-verification.md#environment-and-limitations).

## Inspect and plan

```bash
uv run python scripts/hub.py status
uv run python scripts/hub.py inventory
uv run python scripts/hub.py relationships
uv run python scripts/hub.py plan --limit 3
uv run python scripts/hub.py freshness
uv run python scripts/hub.py freshness --as-of 2027-10-19
```

These commands are read-only and print JSON. Planning respects prerequisite order,
priority, and a maximum of five new topics. Draft/review/stale prerequisites block a
new batch; selected planned prerequisites precede their dependents. The output is a
proposal, not authorization to write, publish, or deploy. Freshness uses 180 days for
version-scoped pages and 365 for general pages, or `--days`; it does not fetch upstream
changes or rewrite verification dates. `generate_inventory.py` remains an alias for
the canonical inventory, including article-only fields from frontmatter.

## Add or revise a bounded batch

1. Read AGENTS.md, the registry, taxonomy, and related articles. Select at most 3–5 new
   topics. Prefer updating an existing topic over creating a near-duplicate.
2. Use an existing planned ID, or add a row with status planned, path null, and priority.
   Copy the matching article template to drafts/<domain>/<slug>.md and change both
   article and registry status/path to draft. Keep shared metadata aligned.
3. Research primary sources. Reuse or add records in registry/sources.yaml; record an
   identifiable URL, version/document edition, and actual verification date. Article
   sources lists their IDs; the corresponding URLs must appear in References.
4. Write substance under every template heading. Explain assumptions, examples,
   alternatives, and failure modes. Use applies_to for version scope; it is mandatory
   for technology and comparison pages. Keep code examples small and label simulations.
5. Move to review. Use [the review template](../agents/review-report-template.md),
   recording accepted/revise/rejected and evidence. Source-backed technical review
   can reject a draft even if the structural validator passes.
6. After scope and content approval, move accepted pages into docs/, update the
   registry path/status, repair all relative links, and add navigation in zensical.toml.
   Preserve IDs. Articles are the canonical written metadata; registry mirrors are
   validated. Relationships remain in frontmatter/registry, with a derived JSON export,
   rather than a second hand-maintained relationships.yaml.
7. Run the local checks and relevant examples. Review the diff and report changed
   files/topics, sources, uncertainty, validation results, and remaining work. Obtain
   separate authorization before a PR, push, merge, access change, or deployment.

## Browser verification

The optional browser dependency group is separate from normal validation:

```bash
uv sync --locked --group browser
uv run --group browser python -m playwright install --with-deps firefox
uv run zensical build
uv run --group browser python scripts/check_browser.py
```

The check starts and stops a loopback server, verifies all article URLs and headings,
search interaction, and mobile menu/navigation, and saves ignored screenshots under
browser-results/. It fails nonzero on a failed interaction. The search panel uses a small presentation script to set an opacity token inside
Zensical's open search shadow root. This keeps results readable when background blur
is unavailable; browser checks catch upstream markup changes. Fonts use system fallbacks. System libraries for
Firefox must be available; installing them may need administrator permission.

## Private hosting and updates

Use [the optional hosting guide](hosting.md). Hosting is not needed to read or maintain
the hub. The prepared workflow is manual and disabled until you configure the environment
flag, protected hostname, Access policies, secrets, and approval process. No public
preview or automatic content publishing is part of the workflow.


In this PRoot environment, Chromium could not create a page. Firefox passed with
`MOZ_DISABLE_CONTENT_SANDBOX=1` and `PLAYWRIGHT_BROWSERS_PATH=/tmp/de-hub-browsers`.
Those are local smoke-test compatibility settings, not website or production settings.
Normal CI uses Playwright's standard headless Firefox configuration.
