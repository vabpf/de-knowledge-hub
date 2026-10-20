# Writing Workflow

Copy the matching templates/<type>.md into drafts/<domain>/<slug>.md. Replace all
placeholders, assign the stable topic ID, and register draft status and its path.
Article frontmatter owns written metadata; keep shared registry mirrors aligned.
Source IDs come from registry/sources.yaml, and every source URL appears in References.
Technology/comparison articles require applies_to with specific versions or dated docs.

Explain why/how, a useful example with assumptions and expected results, trade-offs,
misconceptions, and relative links. Label simulations and unexecuted engine examples.
Use implementations for general-topic -> technology edges. Request technical review
using agents/review-report-template.md. Rejected/revise drafts stay outside docs/.

Within approved scope and after acceptance, move the article to docs/, update its
status/path and navigation, and repair links without changing its ID. Stale articles
remain publishable but must retain their uncertainty and review queue entry.
