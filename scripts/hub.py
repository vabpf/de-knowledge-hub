"""Read-only knowledge inventory, bounded batch planning, and freshness review."""
import argparse
from collections import Counter
from datetime import date
import json
from pathlib import Path

if __package__:
    from .validate import ROOT, article, load_yaml, validate, RELATIONS
else:
    from validate import ROOT, article, load_yaml, validate, RELATIONS

PRIORITY = {'high': 0, 'medium': 1, 'low': 2}


def inventory(root=ROOT):
    topics = load_yaml((root / 'registry/topics.yaml').read_text())['topics']
    result = []
    for topic in topics:
        entry = dict(topic)
        entry.setdefault('priority', 'medium')
        if topic['path']:
            # Article frontmatter owns written content; registry owns priority/path.
            entry.update(article(root / topic['path'])[0])
        result.append(entry)
    return sorted(result, key=lambda topic: topic['id'])


def plan_batch(topics, limit=3):
    if not 1 <= limit <= 5:
        raise ValueError('batch size must be between 1 and 5')
    available = {t['id'] for t in topics if t['status'] == 'published'}
    candidates = sorted((t for t in topics if t['status'] == 'planned'),
                        key=lambda t: (PRIORITY[t.get('priority', 'medium')], t['id']))
    selected = []
    while len(selected) < limit:
        ready = next((t for t in candidates if set(t['prerequisites']) <= available), None)
        if ready is None:
            break
        selected.append(ready)
        available.add(ready['id'])
        candidates.remove(ready)
    blocked = [{'id': t['id'], 'unmet_prerequisites': sorted(set(t['prerequisites']) - available)}
               for t in candidates if set(t['prerequisites']) - available]
    return {'limit': limit, 'selected': selected, 'blocked': blocked,
            'remaining_ready': [t['id'] for t in candidates if set(t['prerequisites']) <= available]}


def freshness(topics, as_of, days=None):
    result = []
    for topic in topics:
        if topic['status'] not in ('published', 'stale'):
            continue
        age = (as_of - date.fromisoformat(topic['verified_at'])).days
        threshold = days if days is not None else (180 if topic.get('applies_to') else 365)
        if topic['status'] == 'stale' or age >= threshold:
            result.append({'id': topic['id'], 'path': topic['path'], 'age_days': age,
                           'review_after_days': threshold,
                           'reason': 'marked stale' if topic['status'] == 'stale' else 'verification age',
                           'applies_to': topic.get('applies_to'), 'sources': topic['sources']})
    return sorted(result, key=lambda row: (-row['age_days'], row['id']))


def relationships(topics):
    return sorted([{'source': topic['id'], 'type': kind, 'target': target}
                   for topic in topics for kind in RELATIONS for target in topic[kind]],
                  key=lambda edge: (edge['source'], edge['type'], edge['target']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('status')
    commands.add_parser('inventory')
    commands.add_parser('relationships')
    plan = commands.add_parser('plan')
    plan.add_argument('--limit', type=int, choices=range(1, 6), default=3)
    fresh = commands.add_parser('freshness')
    fresh.add_argument('--as-of', type=date.fromisoformat, default=date.today())
    fresh.add_argument('--days', type=int)
    args = parser.parse_args()
    if args.command == 'freshness' and args.days is not None and args.days < 1:
        parser.error('--days must be positive')
    errors = validate(args.root)
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    topics = inventory(args.root)
    if args.command == 'status':
        result = {'total': len(topics), 'statuses': dict(sorted(Counter(t['status'] for t in topics).items())),
                  'types': dict(sorted(Counter(t['type'] for t in topics).items()))}
    elif args.command == 'inventory':
        result = topics
    elif args.command == 'relationships':
        result = relationships(topics)
    elif args.command == 'plan':
        result = plan_batch(topics, args.limit)
    else:
        result = freshness(topics, args.as_of, args.days)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
