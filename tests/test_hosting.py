from pathlib import Path
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest
import yaml

from scripts.check_private import is_access_redirect, probe
from scripts.prepare_cloudflare import configuration
from scripts.validate import ROOT


def test_static_configuration_disables_provider_urls():
    config = configuration('wiki.example.com')
    assert config['workers_dev'] is False
    assert config['preview_urls'] is False
    assert config['routes'] == [{'pattern': 'wiki.example.com', 'custom_domain': True}]
    assert config['assets']['directory'] == './site'
    assert 'main' not in config  # No custom backend code.


@pytest.mark.parametrize('hostname', ['https://wiki.example.com', 'wiki.example.com/path', '*.example.com',
                                    'example.com:443', 'bad..example.com', '-bad.example.com', 'a.workers.dev'])
def test_bad_hostnames_rejected(hostname):
    with pytest.raises(ValueError):
        configuration(hostname)


@pytest.mark.parametrize('status,location,expected', [
    (302, 'https://team.cloudflareaccess.com/cdn-cgi/access/login/wiki.example.com', True),
    (200, 'https://team.cloudflareaccess.com/cdn-cgi/access/login/wiki.example.com', False),
    (404, None, False),
    (302, 'https://attacker.example/cdn-cgi/access/login/wiki.example.com', False),
    (302, 'https://team.cloudflareaccess.com/not-login', False),
    (302, 'http://team.cloudflareaccess.com/cdn-cgi/access/login/wiki.example.com', False),
    (302, 'https://team.cloudflareaccess.com:444/cdn-cgi/access/login/wiki.example.com', False),
    (302, 'https://[invalid', False),
])
def test_privacy_probe_requires_expected_access_login(status, location, expected):
    assert is_access_redirect(status, location, 'team.cloudflareaccess.com') is expected


def test_probe_does_not_follow_redirect_or_accept_public_content():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/protected':
                self.send_response(302)
                self.send_header('Location', 'https://team.cloudflareaccess.com/cdn-cgi/access/login/wiki.example.com')
            else:
                self.send_response(200)
            self.end_headers()
        def log_message(self, *args):
            pass
    server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        origin = f'http://127.0.0.1:{server.server_port}'
        assert probe(origin + '/protected', 'team.cloudflareaccess.com') == (True, 302)
        assert probe(origin + '/public', 'team.cloudflareaccess.com') == (False, 200)
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def test_deploy_is_manual_gated_and_read_only():
    workflow = yaml.load((ROOT / '.github/workflows/deploy.yml').read_text(), Loader=yaml.BaseLoader)
    assert set(workflow['on']) == {'workflow_dispatch'}
    assert workflow['permissions'] == {'contents': 'read'}
    job = workflow['jobs']['deploy']
    assert job['environment'] == 'private-wiki'
    assert "inputs.approval == 'DEPLOY PRIVATE HUB'" in job['if']
    steps = job['steps']
    assert any('PRIVATE_HOSTING_ENABLED' in str(step) for step in steps)
    assert sum('scripts/check_private.py' in step.get('run', '') for step in steps) == 2
