#!/usr/bin/env python3
"""
Prepare Instagram post for manual upload.

This script:
1. Generates the Instagram image (1080x1080)
2. Creates a formatted caption with hashtags
3. Copies caption to clipboard
4. Shows you which image to upload
5. Optionally opens Instagram in browser

Usage:
    python prepare_instagram_post.py --post ieepa-tariff-delay
    python prepare_instagram_post.py --post judicial-conflicts-comparison --open
"""

import argparse
import subprocess
import sys
from pathlib import Path
import re
import tomli

# Hashtag sets by topic
HASHTAG_SETS = {
    "corruption": [
        "#SupremeCourt", "#SCOTUS", "#JudicialEthics", "#Corruption",
        "#AccountabilityMatters", "#EthicsReform", "#Democracy"
    ],
    "ethics": [
        "#SupremeCourt", "#SCOTUS", "#JudicialEthics", "#Ethics",
        "#Transparency", "#AccountabilityMatters", "#LegalReform"
    ],
    "executive power": [
        "#SupremeCourt", "#SCOTUS", "#ExecutivePower", "#Constitution",
        "#ChecksAndBalances", "#Democracy", "#RuleOfLaw"
    ],
    "shadow docket": [
        "#SupremeCourt", "#SCOTUS", "#ShadowDocket", "#Transparency",
        "#JudicialReform", "#Democracy", "#EmergencyDocket"
    ],
    "partisanship": [
        "#SupremeCourt", "#SCOTUS", "#PartisanCourt", "#JudicialReform",
        "#Democracy", "#Accountability", "#CourtReform"
    ],
    "reform": [
        "#SupremeCourt", "#SCOTUS", "#CourtReform", "#JudicialReform",
        "#TermLimits", "#Democracy", "#ExpandTheCourt"
    ],
}

def parse_front_matter(post_path):
    """Extract title and tags from TOML front matter."""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'\+\+\+(.*?)\+\+\+', content, re.DOTALL)
    if not match:
        return None, []

    front_matter = match.group(1)

    try:
        data = tomli.loads(front_matter)
        title = data.get('title', '')
        tags = data.get('tags', [])
        return title, tags
    except Exception as e:
        print(f"Error parsing front matter: {e}")
        return None, []

def get_hashtags(tags):
    """Get relevant hashtags based on post tags."""
    hashtags = set()

    # Add hashtags based on tags
    for tag in tags:
        tag_lower = tag.lower()
        if tag_lower in HASHTAG_SETS:
            hashtags.update(HASHTAG_SETS[tag_lower])

    # If no matches, use default
    if not hashtags:
        hashtags.update(HASHTAG_SETS["reform"])

    return sorted(hashtags)[:10]  # Instagram recommends max 10-15 hashtags

def create_caption(title, post_slug, hashtags):
    """Create Instagram caption."""
    # Shorten title if needed (Instagram caption limit is 2200 chars)
    if len(title) > 100:
        title_short = title[:97] + "..."
    else:
        title_short = title

    url = f"https://fixthesupremecourt.org/posts/{post_slug}/"

    caption = f"""{title_short}

Read the full article: {url}

Why Supreme Court reform matters 👇

{' '.join(hashtags)}

#LinkInBio #FixTheCourt"""

    return caption

def copy_to_clipboard(text):
    """Copy text to clipboard."""
    try:
        subprocess.run(['pbcopy'], input=text.encode('utf-8'), check=True)
        return True
    except Exception as e:
        print(f"Couldn't copy to clipboard: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Prepare Instagram post")
    parser.add_argument('--post', required=True, help='Post slug (e.g., ieepa-tariff-delay)')
    parser.add_argument('--open', action='store_true', help='Open Instagram in browser')
    args = parser.parse_args()

    post_slug = args.post
    post_path = Path(f"content/posts/{post_slug}.md")

    if not post_path.exists():
        print(f"❌ Post not found: {post_path}")
        sys.exit(1)

    # Parse post
    title, tags = parse_front_matter(post_path)
    if not title:
        print(f"❌ Couldn't parse post front matter")
        sys.exit(1)

    print(f"📝 Post: {title}")
    print(f"🏷️  Tags: {', '.join(tags)}")

    # Check if Instagram image exists
    instagram_image = Path(f"static/thumbnails/{post_slug}_modern.png")
    if not instagram_image.exists():
        # Try without _modern suffix
        instagram_image = Path(f"static/thumbnails/{post_slug}.png")
        if not instagram_image.exists():
            print(f"\n⚠️  Instagram image not found, generating...")
            # Generate it
            result = subprocess.run([
                'python3', 'generate_thumbnails_pro.py',
                '--post', post_slug
            ], capture_output=True, text=True)

            if result.returncode != 0:
                print(f"❌ Failed to generate image: {result.stderr}")
                sys.exit(1)

            # Check again
            instagram_image = Path(f"static/thumbnails/{post_slug}_modern.png")
            if not instagram_image.exists():
                instagram_image = Path(f"static/thumbnails/{post_slug}.png")

    if not instagram_image.exists():
        print(f"❌ Instagram image still not found")
        sys.exit(1)

    print(f"🖼️  Image: {instagram_image}")

    # Get hashtags
    hashtags = get_hashtags(tags)

    # Create caption
    caption = create_caption(title, post_slug, hashtags)

    # Copy to clipboard
    if copy_to_clipboard(caption):
        print(f"\n✅ Caption copied to clipboard!")
    else:
        print(f"\n📋 Caption:")
        print(caption)

    # Show instructions
    print(f"\n" + "="*60)
    print("📱 INSTAGRAM POSTING INSTRUCTIONS")
    print("="*60)
    print(f"\n1. Upload this image:")
    print(f"   {instagram_image.absolute()}")
    print(f"\n2. Paste the caption (already in your clipboard)")
    print(f"\n3. Post!")

    # Open Instagram
    if args.open:
        print(f"\n🌐 Opening Instagram...")
        subprocess.run(['open', 'https://www.instagram.com/'])
    else:
        print(f"\n💡 Tip: Use --open flag to auto-open Instagram")

    print("\n" + "="*60)

if __name__ == '__main__':
    main()
