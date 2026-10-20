"""Exercise the validator against valid repositories and deliberate corruptions."""
import json
import re
from pathlib import Path
import shutil
import subprocess
import sys

import pytest
import yaml

from scripts.validate import ROOT, article, load_yaml, validate


@pytest.fixture
def repo(tmp_path):
    for name in ('docs', 'drafts', 'registry', 'schemas'):
        shutil.copytree(ROOT / name, tmp_path / name)
    shutil.copy(ROOT / 'zensical.toml', tmp_path)
    return tmp_path


def save_article(path, meta, body):
    path.write_text('---\n' + yaml.safe_dump(meta, sort_keys=False) + '---\n' + body)


@pytest.mark.parametrize('fixture', sorted((ROOT / 'tests/fixtures').glob('*.json')), ids=lambda p: p.stem)
def test_contract(repo, fixture):
    case = json.loads(fixture.read_text())
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    registry_path = repo / 'registry/topics.yaml'
    registry = load_yaml(registry_path.read_text())
    kind = case['kind']
    if kind == 'metadata':
        if case.get('delete'):
            del meta[case['field']]
        else:
            meta[case['field']] = case['value']
    elif kind == 'append':
        body += '\n\n' + case['value']
    elif kind == 'relation':
        registry['topics'][0][case['relation']] = [case['target']]
        meta[case['relation']] = [case['target']]
    elif kind == 'duplicate':
        registry['topics'].append(dict(registry['topics'][0]))
    elif kind == 'status':
        registry['topics'][0]['status'] = meta['status'] = case['value']
    elif kind == 'nav':
        config = repo / 'zensical.toml'
        config.write_text(config.read_text().replace('"index.md"', '"missing.md"'))
    elif kind == 'tag':
        registry['topics'][0]['tags'] = meta['tags'] = ['unknown']
    elif kind == 'section':
        body = body.replace('## Trade-offs', '## Costs')
    elif kind == 'source':
        body = body.split('## References')[0] + '## References\nNo source.\n'
    save_article(path, meta, body)
    if kind == 'missing':
        path.unlink()
    registry_path.write_text(yaml.safe_dump(registry, sort_keys=False))
    errors = validate(repo)
    if kind == 'valid':
        assert errors == []
    else:
        assert any(case['expected'] in message for message in errors), errors


def test_draft_and_planned_lifecycle(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['status'] = 'review'
    registry_path = repo / 'registry/topics.yaml'
    registry = load_yaml(registry_path.read_text())
    registry['topics'][0].update(status='review', path='drafts/distributed-systems/partitioning.md')
    # The published page must stop linking to the review file.
    other = repo / 'docs/distributed-systems/data-shuffling.md'
    other.write_text(other.read_text().replace('[Data Partitioning](partitioning.md)', 'Data Partitioning'))
    # Drafts may refer to published material without exposing the draft.
    body = body.replace('(data-shuffling.md)', '(../../docs/distributed-systems/data-shuffling.md)')
    body = body.replace('(../foundations/', '(../../docs/foundations/').replace('(../processing/', '(../../docs/processing/')
    target = repo / 'drafts/distributed-systems/partitioning.md'
    target.parent.mkdir(parents=True)
    save_article(target, meta, body)
    path.unlink()
    index = repo / 'docs/index.md'
    index.write_text(index.read_text().replace('[Data Partitioning](distributed-systems/partitioning.md)', 'Data Partitioning'))
    nav = repo / 'zensical.toml'
    nav.write_text(nav.read_text().replace('    { "Data Partitioning" = "distributed-systems/partitioning.md" },\n', ''))
    planned = dict(registry['topics'][0], id='foundations/planned-topic', title='Planned Topic', status='planned', path=None, prerequisites=[], related=[], implementations=[])
    registry['topics'].append(planned)
    registry_path.write_text(yaml.safe_dump(registry))
    for published in (repo / 'docs').rglob('*.md'):
        published.write_text(re.sub(r'\[([^\]]+)\]\([^)]*partitioning\.md(?:#[^)]*)?\)', r'\1', published.read_text()))
    assert validate(repo) == []


def test_move_preserves_id(repo):
    old = repo / 'docs/distributed-systems/partitioning.md'
    new = old.with_name('data-partitioning.md')
    old.rename(new)
    for path in [repo / 'registry/topics.yaml', repo / 'zensical.toml', *(repo / 'docs').rglob('*.md')]:
        path.write_text(path.read_text().replace('partitioning.md', 'data-partitioning.md'))
    assert validate(repo) == []


def test_duplicate_yaml_keys(repo):
    path = repo / 'registry/topics.yaml'
    path.write_text(path.read_text() + '\nversion: 1\n')
    assert any('duplicate YAML key' in e for e in validate(repo))


def test_valid_anchors_and_code_not_links(repo):
    path = repo / 'docs/index.md'
    path.write_text(path.read_text() + '\n[Section](distributed-systems/partitioning.md#trade-offs)\n\n```markdown\n[not a link](missing.md)\n```\n')
    assert validate(repo) == []


def test_cli_failure_exit(repo):
    (repo / 'registry/topics.yaml').write_text('invalid: true\n')
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/validate.py'), '--root', str(repo)], capture_output=True, text=True)
    assert result.returncode == 1
    assert 'FAILED' in result.stdout


def test_inventory_is_deterministic():
    command = [sys.executable, str(ROOT / 'scripts/generate_inventory.py')]
    first = subprocess.check_output(command, text=True)
    assert first == subprocess.check_output(command, text=True)
    from scripts.hub import inventory
    assert json.loads(first) == inventory(ROOT)


def test_inline_code_is_not_html_link(repo):
    path = repo / 'docs/index.md'
    path.write_text(path.read_text() + '\n`<a href="missing.md">example</a>`\n')
    assert validate(repo) == []


@pytest.mark.parametrize('template', sorted((ROOT / 'templates').glob('*.md')), ids=lambda p: p.stem)
def test_add_article_from_each_template(repo, template):
    meta, body = article(template)
    meta.update(id=f"foundations/{template.stem}-example", title=f"{template.stem.title()} Example")
    body = body.replace('# Replace Me', f"# {meta['title']}")
    meta['sources'] = ['spark-rdd']
    body += '\n[Primary source](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html)\n'
    path = repo / f"drafts/foundations/{template.stem}-example.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    save_article(path, meta, body)
    registry_path = repo / 'registry/topics.yaml'
    registry = load_yaml(registry_path.read_text())
    registry['topics'].append({**{k: v for k, v in meta.items() if k not in ('description', 'verified_at', 'sources', 'applies_to')}, 'path': path.relative_to(repo).as_posix()})
    registry_path.write_text(yaml.safe_dump(registry))
    assert validate(repo) == []


def test_landing_page_cannot_bypass_article_contract(repo):
    path = repo / 'registry/topics.yaml'
    registry = load_yaml(path.read_text())
    registry['topics'].append(dict(registry['topics'][0], id='foundations/home', path='docs/index.md'))
    path.write_text(yaml.safe_dump(registry))
    assert any('landing page cannot be registered' in error for error in validate(repo))


def test_malformed_html_url_reports_validation_error(repo):
    path = repo / 'docs/index.md'
    path.write_text(path.read_text() + '\n<a href="https://[invalid">Invalid URL</a>\n')
    assert any('invalid link' in error for error in validate(repo))


def test_valid_technology_implementation(repo):
    path = repo / 'registry/topics.yaml'
    registry = load_yaml(path.read_text())
    registry['topics'].append(dict(registry['topics'][0], id='processing/example-engine', title='Example Engine', type='technology', status='planned', path=None, prerequisites=[], related=[], implementations=[]))
    registry['topics'][0]['implementations'] = ['processing/example-engine']
    article_path = repo / registry['topics'][0]['path']
    meta, body = article(article_path)
    meta['implementations'] = ['processing/example-engine']
    save_article(article_path, meta, body)
    path.write_text(yaml.safe_dump(registry))
    assert validate(repo) == []


def test_unknown_domain_fails(repo):
    path = repo / 'registry/topics.yaml'
    registry = load_yaml(path.read_text())
    registry['topics'].append(dict(registry['topics'][0], id='unknown/example', title='Unknown Example', status='planned', path=None, prerequisites=[], related=[], implementations=[]))
    path.write_text(yaml.safe_dump(registry))
    assert any('unknown ID domain' in error for error in validate(repo))


def test_unregistered_article_fails(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['id'] = 'distributed-systems/unregistered'
    save_article(path.with_name('unregistered.md'), meta, body)
    assert any('article is not registered' in error for error in validate(repo))


def test_crlf_fails(repo):
    path = repo / 'docs/index.md'
    path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
    assert any('LF line endings' in error for error in validate(repo))


def test_missing_frontmatter_fails(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    path.write_text('# No Metadata\n')
    assert any('missing YAML frontmatter' in error for error in validate(repo))


def test_symlink_cannot_expose_draft(repo):
    secret = repo / 'drafts/private.txt'
    secret.write_text('private draft material')
    (repo / 'docs/private.txt').symlink_to(secret)
    path = repo / 'docs/index.md'
    path.write_text(path.read_text() + '\n[Private](private.txt)\n')
    assert any('unpublished link' in error for error in validate(repo))


def test_unlinked_symlink_asset_cannot_expose_draft(repo):
    secret = repo / 'drafts/private.txt'
    secret.write_text('private draft material')
    (repo / 'docs/private.txt').symlink_to(secret)
    assert any('symlinks are not allowed' in error for error in validate(repo))
