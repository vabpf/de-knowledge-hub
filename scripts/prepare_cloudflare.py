"""Generate an ignored static-assets configuration; never upload or change access."""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def configuration(hostname):
    labels = hostname.split('.')
    if len(labels) < 2 or len(hostname) > 253 or any(not re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in labels):
        raise ValueError('provide a lowercase DNS hostname without scheme, path, wildcard, or port')
    if hostname.endswith(('.workers.dev', '.pages.dev')):
        raise ValueError('use an Access-protected custom hostname, not a provider hostname')
    return {'name': 'de-knowledge-hub', 'compatibility_date': '2026-10-19',
            'workers_dev': False, 'preview_urls': False,
            'routes': [{'pattern': hostname, 'custom_domain': True}],
            'assets': {'directory': './site', 'not_found_handling': '404-page'}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--hostname', required=True)
    args = parser.parse_args()
    try:
        config = configuration(args.hostname)
    except ValueError as exc:
        parser.error(str(exc))
    output = ROOT / 'wrangler.local.json'
    output.write_text(json.dumps(config, indent=2) + '\n')
    print(f'Prepared {output.name}; no deployment performed.')


if __name__ == '__main__':
    main()
