# Roadmap and Delivery Status

## Delivered locally

1. **Repository foundation:** stable IDs, schemas, templates, taxonomy, Codex operating
   contract, validation CLI, fixtures, locked dependencies, and CI.
2. **Reading experience:** domain navigation, guided starting path, problem-oriented
   article discovery, local search, relative cross-links, and responsive Zensical layout.
3. **Representative knowledge:** eight connected articles spanning concept, technology,
   mechanism, problem, pattern, and comparison; version scopes and registered sources.
4. **Generation and maintenance workflow:** one coding agent with planning, research,
   writing, review, and maintenance instructions; bounded dependency-aware planning,
   canonical inventory, derived relationships, and read-only freshness reports.
5. **Quality automation:** schema, source, duplicate-title, graph, link, navigation,
   publication-boundary, executable-example, and optional browser checks. A real build
   regression test ensures registered drafts stay out of HTML and search output.
6. **Optional hosting preparation:** manual deployment workflow, static-assets config
   generator, unauthenticated Access probe, and bootstrap/update/rollback guide.

See [completion evidence](completion-report.md) for actual command results and limitations.
These are local implementation deliverables; configured workflows have not run on GitHub.

## Optional activation, left to the owner

No GitHub push, PR, merge, hosting upload, or access change has occurred. When choosing
Cloudflare hosting, follow [the guide](hosting.md): confirm private repository settings,
branch protection, the Access allowlist, and all reachable hostnames before uploading
private content. Live authenticated and unauthenticated checks require the real account.
Hosting activation is optional per the owner's request and is not claimed complete.

## Incremental content backlog

The registry includes planned Spark Shuffle, Adaptive Query Execution, Change Data
Capture, and Dimensional Modeling topics. Use `hub.py plan --limit 3` for a bounded
proposal. Review source and article quality before expanding to large batches.

## Deliberately deferred

Vector search, an interactive graph UI, autonomous scheduled generation, custom frontend,
multiple autonomous agents, and a custom backend remain outside the initial system.
