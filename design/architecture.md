# ADR-001: Knowledge Hub Architecture

Status: Accepted. Version 1.0. October 19, 2026.

Markdown and YAML are the source of truth. A private GitHub repository stores history,
registry, templates, and versioned Codex instructions. Zensical renders a static wiki.
Codex plans, researches, writes, and validates bounded changes. GitHub Actions validates
and builds pull requests. Cloudflare static hosting with Access is the intended private
delivery layer; deployment is deferred and requires explicit approval.

## Decisions and consequences

Keep content portable: ordinary relative Markdown links and YAML metadata. No database,
custom backend, vector index, interactive graph, or autonomous scheduled generation.
Drafts live outside docs because navigation exclusion alone is not a privacy boundary.
The Python validator owns application-level metadata and relationships; Zensical
frontmatter support does not enforce our schema. Prerequisite edges form a DAG;
related edges may be reciprocal. IDs survive path moves.

The validation workflow has read-only permissions and never deploys or uploads built
content. A separate optional workflow can upload only after manual dispatch, explicit
confirmation, environment configuration/approval, and a passing Access probe. Actual GitHub
visibility, branch protection, credentials, and Cloudflare access policies require
external configuration and verification. None is established by this milestone.

## Deployment gate (future)

Require explicit authorization for merging and production deployment. Evaluate every
reachable custom domain, production pages.dev domain, and preview hostname independently.
Check unauthenticated HTML, assets, and search indexes as well as authenticated access;
remove or protect every bypass. Preview protection does not imply production protection.
Do not publish before these checks pass.

## Primary implementation references

- [Zensical configuration basics](https://zensical.org/docs/setup/basics/)
- [Zensical navigation](https://zensical.org/docs/setup/navigation/)
- [Cloudflare Pages preview access policies](https://developers.cloudflare.com/pages/configuration/preview-deployments/)

The Zensical references were consulted for M1 configuration. The Cloudflare reference
is a deployment-stage verification starting point; no hosting changes were performed.


## Completion addendum: October 19, 2026

The local platform now includes eight articles, a source catalog, priority-aware batch
planning, freshness reports, and browser verification. Written article metadata is
canonical; validated registry mirrors retain topic paths/priorities and planned work.
Relationships are exported from those same records, without an independent graph file.
Research, writing, review, and maintenance remain workflows for one coding agent.

Optional hosting uses Workers Static Assets without custom backend code. Its generated
configuration disables workers.dev and version/preview URLs and requires a custom
hostname under Access. This narrows the hostname inventory compared with Pages; it
does not prove account policies or every alternative route are safe. The hosting guide
requires a placeholder-only bootstrap and authenticated/unauthenticated checks before
private content is uploaded. Hosting is prepared but not activated.
