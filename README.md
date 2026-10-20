# Data Engineering Knowledge Hub

A Markdown-first wiki for learning, diagnosing, and designing data systems. Zensical
provides browsing and local search; the knowledge and agent workflows remain ordinary
versioned files. The initial corpus contains eight connected articles across all six
article types, with primary sources and a prioritized backlog.

## Start reading

Use a supported Linux, macOS, or Windows environment with uv installed. The project
pins Python 3.12 and all dependencies in uv.lock.

```bash
uv sync --locked
uv run python scripts/validate.py
uv run pytest
uv run zensical build
uv run zensical serve --dev-addr 127.0.0.1:8000
```

Open **http://127.0.0.1:8000**. Start with Distributed Computing, then Partitioning,
Shuffling, and Spark. Use domain navigation or search to find a problem or concept.
The local server has no authentication; keep it on loopback. Stop with Ctrl+C.

Termux's Android Python is not a tested Zensical target. This session uses a compatible
Linux uv/Python installation; see the [environment commands](design/m1-verification.md#environment-and-limitations).
For normal installation, use [uv's official guide](https://docs.astral.sh/uv/getting-started/installation/).

## Maintain and expand

```bash
uv run python scripts/hub.py status
uv run python scripts/hub.py plan --limit 3
uv run python scripts/hub.py inventory
uv run python scripts/hub.py freshness
```

The tools are read-only. The planner chooses a bounded prerequisite-aware batch;
freshness reports review candidates without changing content. Read the
[runbook](design/runbook.md) for source research, article creation, review, browser
checks, and update procedures. [AGENTS.md](AGENTS.md) is the agent operating contract.
The maintainer is one coding agent following distinct workflows, not an autonomous
multi-agent service. No API key, model server, database, or scheduled generation is needed.

## Repository map

| Area | Responsibility |
| --- | --- |
| docs/ | Publishable articles and the reader landing page |
| drafts/ | Draft and review material, excluded from build/search |
| registry/ | Topics, priorities, taxonomy, and reusable source records |
| schemas/ | Article, topic, and source contracts |
| templates/ | Six article types |
| agents/ | Planning, research, writing, review, and maintenance instructions |
| scripts/ | Validation, inventory, planning, freshness, browser, and hosting tools |
| tests/ | Positive/negative contract and workflow regression tests |
| design/ | Internal architecture, runbooks, review evidence, and roadmap |
| .github/workflows/ | Read-only validation and separately gated optional deployment |

Article frontmatter is canonical for written metadata; the registry mirrors shared
fields and validation rejects disagreements. Planned topics have null paths. Metadata
relationships are exported from the same records instead of hand-maintaining another
graph file. The validator checks schema, IDs, duplicate canonical titles, sources,
versions, prerequisite cycles, publication boundaries, links/anchors, and navigation.
Technical accuracy and source relevance require review; passing validation is not
proof of factual correctness.

## Optional private hosting

The hub is ready to use locally. Cloudflare hosting is **prepared, not activated**.
Follow the [private hosting and update guide](design/hosting.md) when you choose to
host it. It covers Access setup, hostname checks, a placeholder-only bootstrap,
manual GitHub deployment, content updates, and rollback. Authentication must cover
the whole site, including assets and search data, and every alternative hostname.

Repository privacy has not been verified remotely. The initial implementation is committed locally. No push, PR, merge, deployment,
or access change has been performed. Those actions require explicit authorization.
Generated output, caches, environments, local hosting configuration, and secrets are ignored.

See [completion evidence](design/completion-report.md) for validation and limitations.
