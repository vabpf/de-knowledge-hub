# Review Workflow

Use agents/review-report-template.md. Decide accept, revise, or reject based on source
support, example correctness, version scope, consistency, and useful explanations.
Check existing topics for overlap, prerequisites, and implementation direction.
A passing structural check does not require an accept decision. Unsupported or
contradictory claims are blocking findings, not a reason to fabricate certainty.

Run `uv run python scripts/validate.py`, `uv run pytest`, and `uv run zensical build`.
Run browser checks for presentation/search changes and relevant examples for content
changes. Inspect the diff for generated files and private material. Report files/topics,
sources, uncertainties, commands/results, and remaining work. Stop before a PR, push,
merge, access change, or deployment unless separately authorized.
