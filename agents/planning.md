# Planning Workflow

Read AGENTS.md, registry/topics.yaml, taxonomy, existing articles, and git status.
Run `uv run python scripts/hub.py plan --limit 3` for a dependency-aware proposal.
State the approved outcome and bounded topic/file list. Default to 3–5 new pages,
including prerequisites added in that batch. Do not start bulk generation.

Prefer canonical IDs and update existing topics instead of generating overlap. Check
normalized titles and semantic similarity manually. Register planned topics with null
paths and high/medium/low priority. Draft/review/stale prerequisites need attention;
do not silently present them as ready. Preserve unrelated work.
