"""Validate the registry, publication boundary, metadata, graph, and local links."""
from __future__ import annotations

import argparse
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import tomllib
import unicodedata
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator, FormatChecker
from markdown_it import MarkdownIt
import yaml

ROOT = Path(__file__).resolve().parents[1]
RELATIONS = ("prerequisites", "related", "implementations")
SECTIONS = ("TL;DR", "Why It Exists", "How It Works", "Practical Example",
            "Trade-offs", "Common Misconceptions", "Related Concepts", "References")
MD = MarkdownIt("commonmark")


class Loader(yaml.SafeLoader):
    """Keep ISO dates as schema-checkable strings and reject duplicate keys."""


def mapping(loader, node):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node)
        if key in result:
            raise ValueError(f"duplicate YAML key: {key}")
        result[key] = loader.construct_object(value_node)
    return result


Loader.add_constructor("tag:yaml.org,2002:map", mapping)
Loader.add_constructor("tag:yaml.org,2002:timestamp", lambda loader, node: loader.construct_scalar(node))


def load_yaml(text):
    return yaml.load(text, Loader=Loader)


def article(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)(.*)", text, re.S)
    if not match:
        raise ValueError("missing YAML frontmatter")
    return load_yaml(match[1]), match[2]


class HtmlTargets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.links.extend(attrs[k] for k in ("href", "src") if attrs.get(k))
        if attrs.get("id"):
            self.anchors.add(attrs["id"])


def structure(body):
    tokens = MD.parse(body)
    headings, links, anchors, counts = [], [], set(), {}
    for i, token in enumerate(tokens):
        if token.type == "heading_open":
            inline = tokens[i + 1]
            title = "".join(c.content for c in inline.children or [] if c.type in ("text", "code_inline"))
            headings.append((token.tag, title))
            slug = re.sub(r"[^\w\- ]", "", unicodedata.normalize("NFKC", title).lower()).replace(" ", "-")
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            anchors.add(slug if count == 0 else f"{slug}_{count}")
        for child in token.children or []:
            if child.type in ("link_open", "image"):
                links.append(child.attrGet("href") or child.attrGet("src"))
            if child.type == "html_inline":
                html = HtmlTargets()
                html.feed(child.content)
                links.extend(html.links)
                anchors.update(html.anchors)
        if token.type == "html_block":
            html = HtmlTargets()
            html.feed(token.content)
            links.extend(html.links)
            anchors.update(html.anchors)
    return headings, links, anchors


def validate(root: Path = ROOT) -> list[str]:
    root = root.resolve()
    errors = []

    def error(path, message):
        errors.append(f"{path}: {message}")

    def read_yaml(path):
        try:
            return load_yaml((root / path).read_text(encoding="utf-8"))
        except (OSError, ValueError, yaml.YAMLError, TypeError) as exc:
            error(path, str(exc))
            return None

    validators = {}
    for kind in ("article", "topic", "source"):
        try:
            schema = json.loads((root / f"schemas/{kind}.schema.json").read_text())
            Draft202012Validator.check_schema(schema)
            validators[kind] = Draft202012Validator(schema, format_checker=FormatChecker())
        except Exception as exc:
            error("schemas", str(exc))
    if len(validators) != 3:
        return errors

    def conforms(kind, data, path):
        issues = sorted(validators[kind].iter_errors(data), key=lambda e: str(list(e.path)))
        for issue in issues:
            error(path, f"{'.'.join(map(str, issue.path)) or 'metadata'}: {issue.message}")
        return not issues

    catalog = read_yaml("registry/sources.yaml")
    if not conforms('source', catalog, 'registry/sources.yaml'):
        return errors
    sources, source_urls = {}, set()
    for source in catalog['sources']:
        if source['id'] in sources or source['url'] in source_urls:
            error('registry/sources.yaml', 'duplicate source ID or URL')
        sources[source['id']] = source
        source_urls.add(source['url'])
        if date.fromisoformat(source['verified_at']) > date.today():
            error(source['id'], 'source verification date cannot be in the future')

    taxonomy = read_yaml("registry/taxonomy.yaml")
    if (not isinstance(taxonomy, dict) or taxonomy.get("version") != 1 or
        any(not isinstance(taxonomy.get(k), list) or not taxonomy[k] or
            any(not isinstance(v, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", v) for v in taxonomy[k]) or
            len(set(taxonomy[k])) != len(taxonomy[k]) for k in ("domains", "tags"))):
        error("registry/taxonomy.yaml", "expected version 1 and unique domain/tag lists")
        return errors
    registry = read_yaml("registry/topics.yaml")
    if not isinstance(registry, dict) or registry.get("version") != 1 or not isinstance(registry.get("topics"), list):
        error("registry/topics.yaml", "expected version 1 and a topics list")
        return errors
    topics, paths, titles = {}, {}, {}
    for n, topic in enumerate(registry["topics"]):
        label = f"registry/topics.yaml[{n}]"
        if not conforms("topic", topic, label):
            continue
        ident, path = topic["id"], topic["path"]
        if ident in topics:
            error(label, f"duplicate ID {ident}")
        canonical_title = re.sub(r'[^a-z0-9]', '', topic['title'].casefold())
        if canonical_title in titles and titles[canonical_title] != ident:
            error(label, f"duplicate canonical title: {topic['title']}")
        titles[canonical_title] = ident
        topics[ident] = topic
        if ident.split('/')[0] not in taxonomy['domains']:
            error(label, "unknown ID domain")
        if set(topic['tags']) - set(taxonomy['tags']):
            error(label, "unknown taxonomy tag")
        if path:
            if path == 'docs/index.md':
                error(label, "landing page cannot be registered as an article")
            if path in paths:
                error(label, f"duplicate path {path}")
            paths[path] = topic
            expected = "docs/" if topic['status'] in ('published', 'stale') else "drafts/"
            if not path.startswith(expected):
                error(label, f"status requires {expected}")
            if not (root / path).is_file():
                error(label, f"missing article {path}")
    for ident, topic in topics.items():
        for relation in RELATIONS:
            for target in topic[relation]:
                if target == ident or target not in topics:
                    error(ident, f"{relation}: self-reference or missing target {target}")
                elif relation == "implementations" and topics[target]['type'] != 'technology':
                    error(ident, f"implementation target must be a technology: {target}")
    visited, active = set(), set()

    def visit(ident):
        if ident in active:
            error(ident, "prerequisite cycle")
            return
        if ident in visited:
            return
        active.add(ident)
        for target in topics[ident]['prerequisites']:
            if target in topics:
                visit(target)
        active.remove(ident)
        visited.add(ident)

    for ident in topics:
        visit(ident)

    # Zensical copies static assets too, even when no page links to them.
    for path in (root / 'docs').rglob('*'):
        if path.is_symlink():
            error(path.relative_to(root).as_posix(), 'symlinks are not allowed in the publishable tree')

    documents = {}
    article_ids = set()
    for folder in ('docs', 'drafts'):
        for path in sorted((root / folder).rglob('*.md')):
            rel = path.relative_to(root).as_posix()
            try:
                raw = path.read_bytes()
                if b'\r' in raw:
                    error(rel, "use LF line endings")
                text = raw.decode('utf-8')
                if path.is_symlink() or not path.resolve().is_relative_to(root / folder):
                    error(rel, "symlink or path outside content tree")
                    continue
                if rel == 'docs/index.md':
                    body = text
                else:
                    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*\.md', path.name):
                        error(rel, "filename must be kebab-case.md")
                    meta, body = article(path)
                    if not conforms('article', meta, rel):
                        continue
                    if meta['id'] in article_ids:
                        error(rel, f"duplicate article ID {meta['id']}")
                    article_ids.add(meta['id'])
                    topic = paths.get(rel)
                    if not topic:
                        error(rel, "article is not registered")
                    else:
                        for field in ('id', 'title', 'type', 'status', 'difficulty', 'tags', *RELATIONS):
                            if meta[field] != topic[field]:
                                error(rel, f"{field} differs from registry")
                    if folder == 'docs' and meta['status'] not in ('published', 'stale'):
                        error(rel, "only published/stale articles belong in docs")
                    if folder == 'drafts' and meta['status'] not in ('draft', 'review'):
                        error(rel, "only draft/review articles belong in drafts")
                    if date.fromisoformat(meta['verified_at']) > date.today():
                        error(rel, "verified_at cannot be in the future")
                    reference_links = structure(body.split('## References', 1)[-1])[1]
                    for source_id in meta['sources']:
                        if source_id not in sources:
                            error(rel, f'unknown source ID: {source_id}')
                        elif not any(link.split('#', 1)[0] == sources[source_id]['url'].split('#', 1)[0] for link in reference_links):
                            error(rel, f'source URL missing from References: {source_id}')
                    headings, links, _ = structure(body)
                    if [t for level, t in headings if level == 'h1'] != [meta['title']]:
                        error(rel, "expected one H1 matching title")
                    if [t for level, t in headings if level == 'h2'] != list(SECTIONS):
                        error(rel, "required article sections missing or out of order")
                    if not any(urlsplit(link).scheme in ('https', 'http') for link in structure(body.split('## References', 1)[-1])[1]):
                        error(rel, "References must include an identifiable HTTP(S) source")
                documents[path.resolve()] = structure(body)
            except (OSError, UnicodeError, ValueError, yaml.YAMLError, TypeError) as exc:
                error(rel, str(exc))
    if not (root / 'docs/index.md').is_file():
        error('docs/index.md', 'missing landing page')
    for path, (_, links, _) in documents.items():
        rel = path.relative_to(root).as_posix()
        for link in links:
            try:
                url = urlsplit(link)
            except ValueError as exc:
                error(rel, f"invalid link {link!r}: {exc}")
                continue
            if url.scheme in ('https', 'http', 'mailto'):
                continue
            if url.scheme or url.netloc or url.path.startswith('/'):
                error(rel, f"use relative internal links: {link}")
                continue
            try:
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
            except (OSError, ValueError) as exc:
                error(rel, f"invalid link {link!r}: {exc}")
                continue
            boundaries = [root / 'docs'] if rel.startswith('docs/') else [root / 'docs', root / 'drafts']
            if not any(target.is_relative_to(boundary) for boundary in boundaries) or not target.is_file():
                error(rel, f"broken or unpublished link: {link}")
                continue
            if target.suffix in ('.html', '.htm'):
                error(rel, f"use Markdown links: {link}")
            if url.fragment and target.suffix == '.md':
                if target not in documents or unquote(url.fragment) not in documents[target][2]:
                    error(rel, f"missing anchor: {link}")
    try:
        config = tomllib.loads((root / 'zensical.toml').read_text())['project']
        if config.get('docs_dir', 'docs') != 'docs':
            error('zensical.toml', 'docs_dir must be docs')
        def nav_paths(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, list):
                for item in value:
                    yield from nav_paths(item)
            elif isinstance(value, dict):
                for item in value.values():
                    yield from nav_paths(item)
        nav = list(nav_paths(config.get('nav', [])))
        expected = {'index.md'} | {p.removeprefix('docs/') for p in paths if p.startswith('docs/')}
        if set(nav) != expected or len(nav) != len(set(nav)):
            error('zensical.toml', 'navigation must contain each publishable page exactly once')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        error('zensical.toml', str(exc))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    for message in errors:
        print(message, file=sys.stderr)
    print(f"Validation {'FAILED' if errors else 'passed'} ({len(errors)} errors)")
    return int(bool(errors))


if __name__ == '__main__':
    raise SystemExit(main())
