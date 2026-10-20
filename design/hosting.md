# Optional Private Hosting and Update Guide

Local use requires no Cloudflare account. This guide prepares an optional static
Cloudflare deployment; nothing has been uploaded or configured remotely. Follow it
only when you explicitly choose to publish privately. Do not put credentials in Git,
Markdown, chat, or workflow inputs.

## Chosen deployment shape

Use Cloudflare Workers Static Assets for the generated `site/` directory, with a
custom hostname protected by Cloudflare Access. There is no custom Worker script,
database, or backend. `scripts/prepare_cloudflare.py` creates an ignored config with
`workers_dev: false` and `preview_urls: false`. A custom hostname is required.

This choice avoids creating a Pages project and its pages.dev hostname. Disabling
workers.dev alone is insufficient: version and preview URLs are separate settings.
Account features can introduce other deployment URLs; inspect all routes and URLs
in the dashboard before allowing private content. Never assume a flag alone proves
privacy. If using Pages instead, separately protect or disable production pages.dev,
custom domains, immutable deployments, and branch previews.

## Before you begin

You need a Cloudflare account, a domain managed in that account, an Access identity
provider or email one-time PIN configuration, and an explicit allowlist of users.
Choose a hostname such as `wiki.your-domain.com` and identify the Access team domain
such as `your-team.cloudflareaccess.com`. Use your own values, not the examples.
Review current account limits and pricing in the provider dashboard; no paid plan is
assumed here. Local build dependencies remain managed by uv; optional uploading uses
Node.js 22 and Wrangler 4.136.3, pinned by the deployment workflow.

Keep the GitHub repository private. Set branch protection to require validation and
review before merging. These settings are not configured by files in this repository.

## Bootstrap without private content

1. In Cloudflare Zero Trust, create a self-hosted Access application for the entire
   chosen hostname, with no path restriction. Configure the intended identity provider
   and an explicit allow policy for your users. Avoid Bypass or Allow Everyone rules.
   Review other applications and policies that overlap the hostname.
2. Prepare local configuration:

   ```bash
   uv run python scripts/prepare_cloudflare.py --hostname wiki.your-domain.com
   ```

   Read `wrangler.local.json`. It contains only static-assets settings and the custom
   hostname; no credentials. Keep provider and preview URLs disabled.
3. For the first deployment, create a separate directory containing only a generic
   placeholder page. Temporarily change `assets.directory` in the ignored config to
   that directory. Do not point it at docs/, the repository root, or the real site yet.
4. Authenticate Wrangler locally using your Cloudflare account, or use an appropriately
   scoped API token from a secure environment. After explicitly approving this external
   change, deploy only the placeholder:

   ```bash
   npx wrangler@4.136.3 deploy --config wrangler.local.json
   ```

5. Inspect Workers & Pages → your Worker → Domains & Routes. Confirm the custom domain,
   disabled workers.dev, and disabled version/preview URLs. Enumerate any deployment
   URLs, aliases, old Workers, old Pages projects, or alternate domains; disable them
   or put them under an equivalent Access policy. Remove obsolete routes. Wait for
   DNS and TLS provisioning to complete.
6. Build locally and probe the protected hostname without a session:

   ```bash
   uv run zensical build
   uv run python scripts/check_private.py \
     --base-url https://wiki.your-domain.com \
     --team-domain your-team.cloudflareaccess.com
   ```

   The probe checks the site’s HTML, JSON search index, JavaScript, CSS, and WASM URLs.
   It does not send credentials or follow redirects. Each must redirect to your expected
   Access login. A public 200, ordinary redirect, 404, or network error fails. During
   bootstrap, Access should challenge even paths not present in the placeholder site.
7. In a fresh browser profile, verify a permitted identity can read the placeholder,
   and a disallowed identity cannot. Check alternative URLs individually without a
   session. Do not proceed until every reachable route is accounted for.
8. Restore real assets by regenerating `wrangler.local.json` with the same hostname.
   Run validation, tests, and build. Choose either manual local upload or the optional
   GitHub workflow below. This is the first upload containing private knowledge and
   requires explicit deployment approval.

## Optional GitHub deployment

The `Optional private deployment` workflow runs only from an explicit manual dispatch
on main; content pushes and pull requests never deploy automatically. It requires a
`private-wiki` environment, the exact confirmation `DEPLOY PRIVATE HUB`, an enabled
flag, and a passing unauthenticated probe before any upload.

Create GitHub environment **private-wiki** with required reviewers where your GitHub
plan supports them, and restrict it to main. If environment approvals are unavailable,
keep deployment manual with a separate human approval process; do not treat the
confirmation string as an enforceable reviewer boundary.

Set these environment variables:

| Variable | Value |
| --- | --- |
| PRIVATE_HOSTING_ENABLED | `true`, only after the bootstrap privacy review |
| CLOUDFLARE_HOSTNAME | Your custom hostname, without scheme or slash |
| CLOUDFLARE_ACCESS_TEAM_DOMAIN | Your Access team hostname, without scheme |

Set environment secrets `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`. Restrict the
token to the intended account/zone and the permissions needed for Worker/static-asset
uploads and its custom domain; do not use a global API key. Follow Cloudflare's current
permission documentation when creating the token. Verify the upload identity cannot
change Access policies. Keep policy administration separate from content deployment.

After an approved merge, select **Actions → Optional private deployment → Run workflow**
on main and enter the confirmation. Approve the environment when prompted. The workflow
validates and builds locally on the runner, probes Access, uploads static assets, and
probes again. It does not upload build artifacts to GitHub or change Access policies.
No private preview deployment is created from a PR.

A post-deployment probe failure stops the job but cannot undo exposure already caused
by a policy change. Disable the enabled flag, block access at the edge, and resolve the
policy or route issue immediately. Do not rerun uploads until it is understood.

## Updating content

1. Select a small batch with `uv run python scripts/hub.py plan --limit 3`, or request
   an update to an existing canonical ID. Read the [runbook](runbook.md).
2. Research primary sources, write/review the change, and run metadata/link validation,
   tests, relevant examples, and `uv run zensical build`.
3. Preview locally. For layout/search changes, run the browser checks in the runbook.
4. Review the diff, commit and push only when authorized, then merge through your
   protected branch process. A merge does not trigger deployment.
5. Explicitly approve and run the manual deployment workflow. Alternatively, run the
   preflight probe, then `npx wrangler@4.136.3 deploy --config wrangler.local.json`
   locally with the same prepared config and securely supplied credentials.
6. Re-run the unauthenticated probe, test permitted and denied users in fresh sessions,
   verify search and cross-links, and record the commit and deployment version.

For maintenance, use `uv run python scripts/hub.py freshness`; it reports review
candidates without silently changing dates, statuses, or articles.

## Rollback and removal

For a content regression, restore the last reviewed source revision, run checks and
build, and explicitly approve a new deployment of that revision. Cloudflare also has
Worker deployment rollback controls; inspect the target version and its assets before
using them. Keep Access and alternate-hostname checks in place throughout.

For an access incident, disable content delivery or enforce a deny policy before
investigating. Removing a DNS record alone is not proof that old provider URLs are
unreachable. When retiring hosting, disable the workflow flag, revoke upload credentials,
remove routes/deployments as appropriate, and verify every old hostname again. Your
Markdown repository remains usable locally.

## Official references

Consulted October 19, 2026; recheck when enabling hosting:

- [Static assets](https://developers.cloudflare.com/workers/static-assets/get-started/)
- [Wrangler configuration](https://developers.cloudflare.com/workers/wrangler/configuration/)
- [workers.dev controls](https://developers.cloudflare.com/workers/configuration/routing/workers-dev/)
- [Version URL controls](https://developers.cloudflare.com/workers/versions-and-deployments/version-urls/)
- [Access self-hosted applications](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/self-hosted-public-app/)
- [Wrangler GitHub Action](https://github.com/cloudflare/wrangler-action)
- [Pages preview limitations](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
