# Content Model and Validation Contract

All article files use UTF-8, LF, kebab-case filenames, English prose, and a human-readable
Title Case title. Registry topic IDs are stable `<domain>/<slug>` identifiers; they need
not match a moved file's path. `docs/index.md` is the sole article-schema exemption
and cannot be registered as an article. Symlinks are forbidden throughout docs/,
including unlinked static assets, to keep files outside docs/ out of the generated site.
Internal design documents and templates are outside the publication tree.

## Fields

Article metadata is defined by schemas/article.schema.json. All fields are required,
including empty relationship arrays. Unknown fields fail. `verified_at` is a real ISO
date (quoted or unquoted YAML), never a future date; it records review, not automatic
proof of truth. Tags and ID domains must exist in registry/taxonomy.yaml. Types are
concept, technology, mechanism, pattern, problem, comparison. Difficulty is beginner,
intermediate, or advanced. Registry rows use schemas/topic.schema.json and mirror
article identity, title, type, status, difficulty, tags, and relationships, plus a path.
Description, verification date, source IDs, and applicable version scope belong to
the article only. `sources` is required and published/stale pages need at least one
registered source. Every cited source ID must have its URL (optionally with a section
fragment) in References. Technology and comparison pages require `applies_to`. The
source catalog has its own JSON schema, rejects duplicate IDs/URLs, and records document
versions and dates. Topic `priority` is high/medium/low; omitted priorities default to
medium. Normalized identical titles across different IDs fail duplicate detection;
semantic overlaps still require review.

## Lifecycle

- planned: registry only, path null, no article.
- draft: file under drafts/, excluded from site and search.
- review: technically reviewable file under drafts/.
- published: approved file under docs/.
- stale: previously published file under docs/ needing verification.

The initial eight-topic completion request authorizes local publication after review.
Subsequent batches require approved scope and content review. A missing registry file, duplicate ID/path, unregistered
article, mismatched metadata, invalid field/date, or incorrect publication path fails.
Changing status does not itself prove review occurred.

## Relationships

`prerequisites` lists topics required before this topic; all targets must exist and the
graph must be acyclic. `related` lists meaningful connections; reciprocal edges are
allowed. `implementations` points from a general topic to technology-specific articles
(type technology). Every relationship rejects self-reference, duplicates, and missing
targets. Planned target IDs are valid conceptual references, but Markdown links may
only target actual files. A published page cannot link outside docs/, including drafts. Drafts may link to docs/ or other drafts.
Relationships in metadata do not automatically become web links.

## Article body and links

One H1 matches title. H2 sections appear exactly in template order: TL;DR, Why It
Exists, How It Works, Practical Example, Trade-offs, Common Misconceptions, Related
Concepts, References. Additional subsections use H3. References require an HTTP(S)
source link. Reviewers ensure section substance, source relevance, and example accuracy.
The validator parses inline, reference-style, image, and HTML href/src links, checks
local files and Markdown heading anchors, and rejects links escaping the publication
boundary. It does not fetch external sources or verify claims. Navigation must list
each published/stale article and the landing page once. It does not measure browser
usability, production security, factual correctness, or reference freshness.

## Moving an article

Preserve its ID. Change the registry path, repair inbound/outbound relative links and
navigation, then validate and build. Never rewrite IDs merely to mirror a new folder.
