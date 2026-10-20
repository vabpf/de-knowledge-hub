"""Verify the built wiki in a real browser at desktop and phone viewport widths."""
import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading

from playwright.sync_api import expect, sync_playwright

from hub import inventory
from validate import ROOT, validate


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--browser', choices=('firefox', 'chromium'), default='firefox')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'browser-results')
    args = parser.parse_args()
    errors = validate(ROOT)
    if errors:
        parser.exit(1, '\n'.join(errors) + '\n')
    if not (ROOT / 'site/index.html').is_file():
        parser.error('run zensical build first')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    handler = functools.partial(QuietHandler, directory=str(ROOT / 'site'))
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    origin = f'http://127.0.0.1:{server.server_port}'
    articles = [t for t in inventory(ROOT) if t['status'] in ('published', 'stale')]
    try:
        with sync_playwright() as playwright:
            browser = getattr(playwright, args.browser).launch(headless=True)
            try:
                for label, width, height in [('desktop', 1440, 1000), ('mobile', 390, 844)]:
                    context = browser.new_context(viewport={'width': width, 'height': height})
                    page = context.new_page()
                    page.set_default_timeout(15000)
                    page_errors = []
                    page.on('pageerror', lambda exc: page_errors.append(str(exc)))
                    for topic in articles:
                        suffix = topic['path'].removeprefix('docs/').removesuffix('.md') + '/'
                        response = page.goto(origin + '/' + suffix, wait_until='networkidle')
                        assert response.status == 200, topic['id']
                        expect(page.locator('h1').first).to_contain_text(topic['title'])
                        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth + 1'), f'page overflow: {label} {topic["id"]}'
                    page.goto(origin, wait_until='networkidle')
                    page.screenshot(path=str(args.output_dir / f'{label}-home.png'), full_page=True, animations='disabled')
                    if label == 'mobile':
                        page.locator('label.md-header__button[for="__drawer"]').click()
                        page.locator('.md-sidebar--primary label.md-nav__link').filter(has_text='Distributed Systems').click()
                        nav_link = page.locator('.md-sidebar--primary').get_by_role('link', name='Data Skew', exact=True)
                        expect(nav_link).to_be_visible()
                        nav_link.click()
                        expect(page.locator('h1').first).to_contain_text('Data Skew')
                        page.screenshot(path=str(args.output_dir / 'mobile-article.png'), full_page=True, animations='disabled')
                        page.locator('label.md-header__button[for="__search"]').click()
                    else:
                        page.locator('.md-search__button').click()
                    search = page.get_by_placeholder('Search', exact=True)
                    expect(search).to_be_visible()
                    search.fill('shuffling')
                    result = page.locator('dialog[open] a[href*="data-shuffling/"]').first
                    expect(result).to_be_visible()
                    panel = page.locator('dialog[open] > div:has(input[aria-label="Search"])')
                    assert panel.evaluate("e => getComputedStyle(e).backgroundColor.startsWith('rgb(')"), 'search results need an opaque background'
                    page.screenshot(path=str(args.output_dir / f'{label}-search.png'), animations='disabled')
                    result.click()
                    expect(page.locator('h1').first).to_contain_text('Data Shuffling')
                    # Follow an article-body cross-link, not a duplicate sidebar entry.
                    page.locator('.md-content').get_by_role('link', name='Data Partitioning', exact=True).click()
                    expect(page.locator('h1').first).to_contain_text('Data Partitioning')
                    assert not page_errors, page_errors
                    context.close()
                    print(f'{label}: {len(articles)} article URLs, responsive width, search, and cross-links passed')
            finally:
                browser.close()
    finally:
        server.shutdown()
        thread.join()
        server.server_close()
    print(f'Browser checks passed ({args.browser}); screenshots: {args.output_dir}')


if __name__ == '__main__':
    main()
