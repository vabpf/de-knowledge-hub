"""Require unauthenticated requests to redirect to the expected Cloudflare Access login.

This is a probe of supplied URLs, not discovery of all deployment aliases or policy proof.
"""
import argparse
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import build_opener, HTTPRedirectHandler, Request

ROOT = Path(__file__).resolve().parents[1]


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def is_access_redirect(status, location, team_domain):
    try:
        url = urlsplit(location or '')
        return (status in (302, 303, 307, 308) and url.scheme == 'https'
                and url.hostname == team_domain and url.port in (None, 443)
                and url.username is None and url.password is None
                and url.path.startswith('/cdn-cgi/access/login/'))
    except ValueError:
        return False


def probe(url, team_domain):
    opener = build_opener(NoRedirect())
    try:
        response = opener.open(Request(url, headers={'User-Agent': 'knowledge-hub-privacy-probe'}), timeout=15)
    except HTTPError as exc:
        response = exc
    with response:
        return is_access_redirect(response.status, response.headers.get('Location'), team_domain), response.status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--team-domain', required=True, help='team.cloudflareaccess.com, without scheme')
    parser.add_argument('--site-dir', type=Path, default=ROOT / 'site')
    args = parser.parse_args()
    base = urlsplit(args.base_url)
    team = args.team_domain
    if (base.scheme != 'https' or not base.hostname or base.path not in ('', '/') or base.query or base.fragment
            or base.username or base.password or base.port not in (None, 443)):
        parser.error('--base-url must be an HTTPS origin without credentials, path, or query')
    if not team.endswith('.cloudflareaccess.com') or '/' in team or ':' in team:
        parser.error('--team-domain must be the expected Cloudflare Access team hostname')
    if not (args.site_dir / 'index.html').is_file() or not (args.site_dir / 'search.json').is_file():
        parser.error('build the site first; index.html and search.json are required')
    paths = {'/', '/search.json'} | {'/' + p.relative_to(args.site_dir).as_posix()
             for p in args.site_dir.rglob('*') if p.is_file() and p.suffix in ('.html', '.json', '.js', '.wasm', '.css')}
    failures = 0
    for path in sorted(paths):
        url = args.base_url.rstrip('/') + path
        try:
            passed, status = probe(url, team)
            print(f"{'PASS' if passed else 'FAIL'} {status} {path}")
        except (OSError, URLError, ValueError) as exc:
            passed = False
            print(f'FAIL {path}: {exc}', file=sys.stderr)
        failures += not passed
    print(f'{len(paths)} unauthenticated URLs checked; {failures} failures. Audit alternate hostnames separately.')
    return int(bool(failures))


if __name__ == '__main__':
    raise SystemExit(main())
