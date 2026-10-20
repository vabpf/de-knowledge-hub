from datetime import date
import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from scripts.hub import freshness, inventory, plan_batch, relationships
from scripts.validate import ROOT, article, load_yaml, validate
from test_validation import repo, save_article


def topic(ident, pre=(), status='planned', priority='high'):
    return {'id': ident, 'prerequisites': list(pre), 'priority': priority, 'status': status}


def test_planner_orders_dependencies_before_priority():
    topics = [topic('foundation', status='published'), topic('child', ['parent']),
              topic('parent', ['foundation'], priority='low')]
    assert [t['id'] for t in plan_batch(topics, 2)['selected']] == ['parent', 'child']


def test_planner_blocks_drafts_and_stale_prerequisites():
    topics = [topic('draft', status='draft'), topic('stale', status='stale'),
              topic('next', ['draft', 'stale'])]
    result = plan_batch(topics)
    assert not result['selected']
    assert result['blocked'] == [{'id': 'next', 'unmet_prerequisites': ['draft', 'stale']}]


def test_planner_bounded_and_deterministic():
    topics = [topic(str(n)) for n in range(10)]
    assert len(plan_batch(topics, 3)['selected']) == 3
    assert plan_batch(topics) == plan_batch(list(reversed(topics)))
    with pytest.raises(ValueError):
        plan_batch(topics, 6)


def test_freshness_thresholds_and_manual_stale():
    topics = [dict(id='a', status='published', path='a.md', verified_at='2026-01-01', sources=[], applies_to='v1'),
              dict(id='b', status='published', path='b.md', verified_at='2026-01-01', sources=[]),
              dict(id='c', status='stale', path='c.md', verified_at='2026-07-01', sources=[])]
    result = freshness(topics, date(2026, 7, 1))
    assert [row['id'] for row in result] == ['a', 'c']
    assert result[1]['reason'] == 'marked stale'
    assert len(freshness(topics, date(2026, 7, 1), days=90)) == 3


def test_inventory_prefers_frontmatter(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['description'] = 'Updated canonical description.'
    save_article(path, meta, body)
    entry = next(t for t in inventory(repo) if t['id'] == meta['id'])
    assert entry['description'] == meta['description']
    assert entry['priority'] == 'high'


def test_relationship_export_includes_implementation():
    edges = relationships(inventory(ROOT))
    assert {'source': 'distributed-systems/partitioning', 'type': 'implementations', 'target': 'processing/apache-spark'} in edges


@pytest.mark.parametrize('command', ['status', 'inventory', 'relationships', 'plan', 'freshness'])
def test_cli_json(command):
    result = subprocess.run([sys.executable, str(ROOT/'scripts/hub.py'), command], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert isinstance(json.loads(result.stdout), (list, dict))


def test_missing_source_fails(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['sources'] = ['does-not-exist']
    save_article(path, meta, body)
    assert any('unknown source ID' in error for error in validate(repo))


def test_source_must_be_in_references(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['sources'] = ['postgres-insert']
    save_article(path, meta, body)
    assert any('source URL missing from References' in error for error in validate(repo))


def test_duplicate_title_fails(repo):
    path = repo / 'registry/topics.yaml'
    registry = load_yaml(path.read_text())
    registry['topics'].append(dict(registry['topics'][0], id='foundations/duplicate', status='planned', path=None))
    path.write_text(yaml.safe_dump(registry))
    assert any('duplicate canonical title' in error for error in validate(repo))


def test_duplicate_source_fails(repo):
    path = repo / 'registry/sources.yaml'
    catalog = load_yaml(path.read_text())
    catalog['sources'].append(dict(catalog['sources'][0]))
    path.write_text(yaml.safe_dump(catalog))
    assert any('duplicate source' in error for error in validate(repo))


def test_published_article_requires_sources(repo):
    path = repo / 'docs/distributed-systems/partitioning.md'
    meta, body = article(path)
    meta['sources'] = []
    save_article(path, meta, body)
    assert validate(repo)


def test_technology_requires_version_scope(repo):
    path = repo / 'docs/processing/apache-spark.md'
    meta, body = article(path)
    del meta['applies_to']
    save_article(path, meta, body)
    assert any('applies_to' in error for error in validate(repo))


def test_build_excludes_registered_drafts_and_search_content(repo):
    from scripts.validate import SECTIONS
    path = repo / 'drafts/foundations/private-sentinel.md'
    path.parent.mkdir(parents=True, exist_ok=True)
    meta, _ = article(repo / 'docs/distributed-systems/partitioning.md')
    meta.update(id='foundations/private-sentinel', title='Private Sentinel', status='draft',
                prerequisites=[], related=[], implementations=[])
    marker = 'PRIVATE_DRAFT_SENTINEL_7af3e921'
    body = '# Private Sentinel\n\n' + '\n\n'.join('## ' + section + '\n\n' + marker for section in SECTIONS)
    body += '\n\n[Source](https://spark.apache.org/docs/3.5.7/rdd-programming-guide.html)\n'
    save_article(path, meta, body)
    registry_path = repo / 'registry/topics.yaml'
    registry = load_yaml(registry_path.read_text())
    registry['topics'].append({k: v for k, v in meta.items() if k not in ('description', 'verified_at', 'sources', 'applies_to')} | {'path': path.relative_to(repo).as_posix(), 'priority': 'low'})
    registry_path.write_text(yaml.safe_dump(registry))
    assert validate(repo) == []
    command = [str(Path(sys.executable).with_name('zensical')), 'build']
    result = subprocess.run(command, cwd=repo, capture_output=True, text=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert (repo / 'site/search.json').is_file()
    assert not (repo / 'site/drafts').exists()
    for generated in (repo / 'site').rglob('*'):
        if generated.is_file() and generated.suffix in ('.html', '.json', '.js', '.css'):
            assert marker.encode() not in generated.read_bytes(), generated
