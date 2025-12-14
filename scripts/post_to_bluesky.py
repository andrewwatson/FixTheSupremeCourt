#!/usr/bin/env python3
"""
Post new Hugo blog posts to Bluesky automatically.
Reads posts from content/posts/ and posts those published in the last 24 hours.
"""

import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import requests

# Bluesky API credentials from environment variables
BLUESKY_HANDLE = os.getenv('BLUESKY_HANDLE')
BLUESKY_PASSWORD = os.getenv('BLUESKY_PASSWORD')
SITE_URL = os.getenv('SITE_URL', 'https://fixthesupremecourt.com')

class BlueskyPoster:
    def __init__(self, handle, password):
        self.handle = handle
        self.password = password
        self.session = None
        self.api_base = "https://bsky.social/xrpc"

    def login(self):
        """Authenticate with Bluesky and get session token."""
        response = requests.post(
            f"{self.api_base}/com.atproto.server.createSession",
            json={
                "identifier": self.handle,
                "password": self.password
            }
        )
        response.raise_for_status()
        self.session = response.json()
        return self.session

    def create_post(self, text, url=None):
        """Create a post on Bluesky."""
        if not self.session:
            raise Exception("Not logged in. Call login() first.")

        # Build the post record
        record = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        }

        # Add URL as a facet if provided
        if url:
            # Find URL position in text
            url_start = text.find(url)
            if url_start != -1:
                record["facets"] = [{
                    "index": {
                        "byteStart": url_start,
                        "byteEnd": url_start + len(url)
                    },
                    "features": [{
                        "$type": "app.bsky.richtext.facet#link",
                        "uri": url
                    }]
                }]

        response = requests.post(
            f"{self.api_base}/com.atproto.repo.createRecord",
            headers={
                "Authorization": f"Bearer {self.session['accessJwt']}"
            },
            json={
                "repo": self.session["did"],
                "collection": "app.bsky.feed.post",
                "record": record
            }
        )
        response.raise_for_status()
        return response.json()

def parse_front_matter(content):
    """Parse Hugo front matter from markdown file."""
    # Match TOML front matter between +++
    match = re.match(r'\+\+\+\n(.*?)\n\+\+\+', content, re.DOTALL)
    if not match:
        return {}

    front_matter = {}
    for line in match.group(1).split('\n'):
        if '=' in line:
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip("'\"")
            front_matter[key] = value

    return front_matter

def get_recent_posts(hours=24):
    """Get posts published in the last N hours."""
    posts_dir = Path('content/posts')
    if not posts_dir.exists():
        print(f"Posts directory not found: {posts_dir}")
        return []

    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
    recent_posts = []

    for post_file in posts_dir.glob('*.md'):
        content = post_file.read_text()
        front_matter = parse_front_matter(content)

        # Skip drafts
        if front_matter.get('draft', 'false').lower() == 'true':
            continue

        # Parse date
        date_str = front_matter.get('date', '')
        if not date_str:
            continue

        try:
            # Parse ISO 8601 date
            post_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))

            # Check if post is recent
            if post_date >= cutoff_time and post_date <= datetime.now(timezone.utc):
                title = front_matter.get('title', post_file.stem)
                slug = post_file.stem

                recent_posts.append({
                    'title': title,
                    'slug': slug,
                    'date': post_date,
                    'file': post_file.name
                })
        except ValueError as e:
            print(f"Error parsing date in {post_file.name}: {e}")
            continue

    return sorted(recent_posts, key=lambda x: x['date'])

def create_post_text(post, site_url):
    """Create the text for a Bluesky post."""
    url = f"{site_url}/posts/{post['slug']}/"

    # Bluesky has a 300 character limit
    # Format: Title + newline + URL
    text = f"{post['title']}\n\n{url}"

    if len(text) > 300:
        # Truncate title if needed
        max_title_length = 300 - len(url) - 3  # 3 for "\n\n"
        title = post['title'][:max_title_length - 3] + "..."
        text = f"{title}\n\n{url}"

    return text, url

def main():
    if not BLUESKY_HANDLE or not BLUESKY_PASSWORD:
        print("Error: BLUESKY_HANDLE and BLUESKY_PASSWORD environment variables must be set")
        sys.exit(1)

    # Get recent posts
    print("Checking for recent posts...")
    recent_posts = get_recent_posts(hours=24)

    if not recent_posts:
        print("No recent posts found to share.")
        return

    print(f"Found {len(recent_posts)} recent post(s):")
    for post in recent_posts:
        print(f"  - {post['title']} ({post['file']})")

    # Login to Bluesky
    print("\nLogging in to Bluesky...")
    poster = BlueskyPoster(BLUESKY_HANDLE, BLUESKY_PASSWORD)
    try:
        poster.login()
        print("✓ Logged in successfully")
    except Exception as e:
        print(f"✗ Login failed: {e}")
        sys.exit(1)

    # Post each recent post
    for post in recent_posts:
        try:
            text, url = create_post_text(post, SITE_URL)
            print(f"\nPosting: {post['title']}")
            print(f"Text: {text}")

            result = poster.create_post(text, url)
            print(f"✓ Posted successfully: {result.get('uri', 'unknown URI')}")
        except Exception as e:
            print(f"✗ Failed to post '{post['title']}': {e}")
            continue

if __name__ == '__main__':
    main()
