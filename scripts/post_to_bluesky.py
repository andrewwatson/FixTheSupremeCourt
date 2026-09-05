#!/usr/bin/env python3
"""
Post one new page to Bluesky per run, oldest-unposted-first.

Scans content/posts/*.md (this covers every content type in this repo,
including the guide and justice-profile types, which live in that same
directory despite overriding their front-matter `url`). Posts are tracked
in data/bluesky-posted.json so each page goes out exactly once, in order
of front-matter `date`, regardless of publish bursts or run cadence.
"""

import json
import os
import sys
import tomllib
from datetime import datetime, timezone
from pathlib import Path

import requests

BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')
SITE_URL = os.getenv('SITE_URL', 'https://fixthesupremecourt.org').rstrip('/')

POSTS_DIR = Path('content/posts')
STATE_FILE = Path('data/bluesky-posted.json')

BLUESKY_MAX_CHARS = 300


class BlueskyPoster:
    def __init__(self, handle, password):
        self.handle = handle
        self.password = password
        self.session = None
        self.api_base = "https://bsky.social/xrpc"

    def login(self):
        response = requests.post(
            f"{self.api_base}/com.atproto.server.createSession",
            json={"identifier": self.handle, "password": self.password},
        )
        response.raise_for_status()
        self.session = response.json()
        return self.session

    def create_post(self, text, url):
        if not self.session:
            raise Exception("Not logged in. Call login() first.")

        record = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        }

        url_start = text.find(url)
        if url_start != -1:
            # Bluesky facets are byte-indexed, not character-indexed.
            byte_start = len(text[:url_start].encode('utf-8'))
            byte_end = byte_start + len(url.encode('utf-8'))
            record["facets"] = [{
                "index": {"byteStart": byte_start, "byteEnd": byte_end},
                "features": [{
                    "$type": "app.bsky.richtext.facet#link",
                    "uri": url,
                }],
            }]

        response = requests.post(
            f"{self.api_base}/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {self.session['accessJwt']}"},
            json={
                "repo": self.session["did"],
                "collection": "app.bsky.feed.post",
                "record": record,
            },
        )
        response.raise_for_status()
        return response.json()


def parse_front_matter(content):
    """Parse Hugo TOML front matter (+++ ... +++) with tomllib."""
    if not content.startswith('+++'):
        return {}
    end = content.find('\n+++', 3)
    if end == -1:
        return {}
    toml_block = content[3:end].strip('\n')
    try:
        return tomllib.loads(toml_block)
    except tomllib.TOMLDecodeError as e:
        print(f"  ! TOML parse error: {e}")
        return {}


def load_posted_state():
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())


def save_posted_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')


def get_page_url(front_matter, slug, site_url):
    """Respect a front-matter `url` override; fall back to /posts/<slug>/."""
    override = front_matter.get('url')
    if override:
        path = override if override.startswith('/') else f'/{override}'
        if not path.endswith('/'):
            path += '/'
        return f"{site_url}{path}"
    return f"{site_url}/posts/{slug}/"


def collect_candidates():
    """All non-draft pages with a parseable date, sorted oldest-first."""
    if not POSTS_DIR.exists():
        print(f"Posts directory not found: {POSTS_DIR}")
        return []

    now = datetime.now(timezone.utc)
    candidates = []

    for post_file in sorted(POSTS_DIR.glob('*.md')):
        content = post_file.read_text()
        front_matter = parse_front_matter(content)

        if not front_matter:
            continue
        if front_matter.get('draft') is True:
            continue

        date_val = front_matter.get('date')
        if date_val is None:
            continue

        # Hugo front matter quotes dates (e.g. '2026-09-04T09:00:00-04:00'),
        # which TOML parses as a plain string rather than a datetime. Bare,
        # unquoted RFC3339 dates parse as real datetime/date objects instead.
        if isinstance(date_val, str):
            try:
                post_date = datetime.fromisoformat(date_val)
            except ValueError:
                print(f"  ! Unparseable date in {post_file.name}: {date_val!r}")
                continue
        elif isinstance(date_val, datetime):
            post_date = date_val
        elif hasattr(date_val, 'year'):  # date, not datetime
            post_date = datetime(date_val.year, date_val.month, date_val.day)
        else:
            continue

        if post_date.tzinfo is None:
            post_date = post_date.replace(tzinfo=timezone.utc)

        if post_date > now:
            continue  # future-dated / scheduled content

        slug = post_file.stem
        candidates.append({
            'slug': slug,
            'file': post_file.name,
            'title': front_matter.get('title', slug),
            'description': front_matter.get('description', ''),
            'date': post_date,
            'url': get_page_url(front_matter, slug, SITE_URL),
        })

    return sorted(candidates, key=lambda p: p['date'])


def create_post_text(page):
    """Title + description + link, truncated to fit Bluesky's limit.

    Truncates the description (rather than dropping it outright) when the
    full text overflows, since most front-matter descriptions are written
    long for SEO and even a partial one beats none. Falls back to
    truncating the title only if there's no room for a description at all.
    """
    url = page['url']
    title = page['title']
    description = page['description']

    if not description:
        text = f"{title}\n\n{url}"
        if len(text) <= BLUESKY_MAX_CHARS:
            return text, url
        return _truncate_title_only(title, url), url

    text = f"{title}\n\n{description}\n\n{url}"
    if len(text) <= BLUESKY_MAX_CHARS:
        return text, url

    # Over budget: shrink the description to fit, keeping title intact.
    fixed_len = len(title) + len("\n\n") + len("\n\n") + len(url) + len("...")
    max_desc_len = BLUESKY_MAX_CHARS - fixed_len
    if max_desc_len >= 20:  # only bother if a meaningful snippet still fits
        description = description[:max_desc_len].rsplit(' ', 1)[0] + "..."
        text = f"{title}\n\n{description}\n\n{url}"
        return text, url

    # No room for any description alongside this title; drop it.
    text = f"{title}\n\n{url}"
    if len(text) <= BLUESKY_MAX_CHARS:
        return text, url
    return _truncate_title_only(title, url), url


def _truncate_title_only(title, url):
    fixed_len = len("\n\n") + len(url) + len("...")
    max_title_len = BLUESKY_MAX_CHARS - fixed_len
    return f"{title[:max_title_len]}...\n\n{url}"


def main():
    if not BLUESKY_HANDLE or not BLUESKY_PASSWORD:
        print("Error: BLUESKY_HANDLE and BLUESKY_PASSWORD environment variables must be set")
        sys.exit(1)

    state = load_posted_state()
    candidates = collect_candidates()
    unposted = [p for p in candidates if p['slug'] not in state]

    print(f"{len(candidates)} total page(s), {len(unposted)} not yet posted.")

    if not unposted:
        print("Nothing new to post.")
        return

    page = unposted[0]
    text, url = create_post_text(page)

    print(f"Posting: {page['title']}")
    print(f"URL: {url}")
    print(f"Text:\n{text}")

    poster = BlueskyPoster(BLUESKY_HANDLE, BLUESKY_PASSWORD)
    try:
        poster.login()
    except Exception as e:
        print(f"Login failed: {e}")
        sys.exit(1)

    try:
        result = poster.create_post(text, url)
    except Exception as e:
        print(f"Failed to post '{page['title']}': {e}")
        sys.exit(1)

    print(f"Posted successfully: {result.get('uri', 'unknown URI')}")

    state[page['slug']] = {
        'title': page['title'],
        'url': url,
        'posted_at': datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'uri': result.get('uri'),
    }
    save_posted_state(state)


if __name__ == '__main__':
    main()
