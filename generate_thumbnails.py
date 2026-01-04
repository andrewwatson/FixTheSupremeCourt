#!/usr/bin/env python3
"""
Generate Instagram thumbnail images from blog post titles.

This script reads blog posts from content/posts/, extracts titles,
and generates 1080x1080px Instagram-ready images with the titles.

Requirements:
    pip install Pillow tomli

Usage:
    python generate_thumbnails.py [--all] [--post POST_NAME]

    --all: Generate thumbnails for all posts
    --post: Generate thumbnail for specific post (e.g., --post pattern-of-corruption)

Output:
    Creates images in static/thumbnails/ directory
"""

import tomli
import argparse
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap
import re

# Configuration
OUTPUT_DIR = Path("static/thumbnails")
POSTS_DIR = Path("content/posts")
IMAGE_SIZE = (1080, 1080)

# Color schemes
COLOR_SCHEMES = {
    "corruption": {
        "bg": (0, 0, 0),          # Black
        "text": (255, 215, 0),     # Gold
        "accent": (220, 20, 60)    # Crimson
    },
    "democracy": {
        "bg": (13, 27, 62),        # Navy blue
        "text": (255, 255, 255),   # White
        "accent": (220, 53, 69)    # Red
    },
    "urgent": {
        "bg": (139, 0, 0),         # Dark red
        "text": (255, 255, 255),   # White
        "accent": (255, 215, 0)    # Gold
    },
    "clean": {
        "bg": (255, 255, 255),     # White
        "text": (33, 37, 41),      # Dark gray
        "accent": (0, 123, 255)    # Blue
    }
}

def parse_front_matter(post_path):
    """Extract title from TOML front matter."""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract front matter between +++
    match = re.match(r'\+\+\+(.*?)\+\+\+', content, re.DOTALL)
    if not match:
        return None

    front_matter = match.group(1)
    try:
        data = tomli.loads(front_matter)
        return data.get('title')
    except Exception as e:
        print(f"Error parsing {post_path}: {e}")
        return None

def get_color_scheme(title):
    """Determine color scheme based on title content."""
    title_lower = title.lower()

    if any(word in title_lower for word in ['corruption', 'gifts', 'thomas', 'alito', 'ethics']):
        return COLOR_SCHEMES['corruption']
    elif any(word in title_lower for word in ['broke', 'destroyed', 'dismantled', 'failed']):
        return COLOR_SCHEMES['urgent']
    elif any(word in title_lower for word in ['reform', 'solution', 'fix', 'need']):
        return COLOR_SCHEMES['democracy']
    else:
        return COLOR_SCHEMES['clean']

def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width > max_width:
            if len(current_line) == 1:
                # Single word is too long, just use it
                lines.append(current_line[0])
                current_line = []
            else:
                # Remove last word and start new line
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def create_thumbnail(title, output_path, scheme_name=None):
    """Generate a thumbnail image for the given title."""
    # Choose color scheme
    if scheme_name and scheme_name in COLOR_SCHEMES:
        colors = COLOR_SCHEMES[scheme_name]
    else:
        colors = get_color_scheme(title)

    # Create image
    img = Image.new('RGB', IMAGE_SIZE, colors['bg'])
    draw = ImageDraw.Draw(img)

    # Try to load custom font, fall back to default
    try:
        # Try different font sizes to find best fit
        font_size = 80
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 80)
        except:
            font = ImageFont.load_default()

    # Wrap title text
    max_width = IMAGE_SIZE[0] - 100  # 50px padding on each side
    lines = wrap_text(title, font, max_width)

    # Calculate total text height
    line_height = font.getbbox("Ay")[3] + 20  # Add line spacing
    total_height = len(lines) * line_height

    # Calculate starting Y position to center text
    y = (IMAGE_SIZE[1] - total_height) // 2

    # Draw each line
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (IMAGE_SIZE[0] - text_width) // 2

        # Add shadow for better readability
        shadow_offset = 3
        draw.text((x + shadow_offset, y + shadow_offset), line,
                 fill=(0, 0, 0, 128), font=font)
        draw.text((x, y), line, fill=colors['text'], font=font)
        y += line_height

    # Add website URL at bottom
    try:
        url_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 30)
    except:
        url_font = font

    url = "FixTheSupremeCourt.com"
    url_bbox = url_font.getbbox(url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (IMAGE_SIZE[0] - url_width) // 2
    url_y = IMAGE_SIZE[1] - 80

    draw.text((url_x, url_y), url, fill=colors['accent'], font=url_font)

    # Save image
    img.save(output_path, quality=95)
    print(f"✓ Created: {output_path}")

def generate_for_post(post_name):
    """Generate thumbnail for a specific post."""
    post_path = POSTS_DIR / f"{post_name}.md"
    if not post_path.exists():
        print(f"Error: Post not found: {post_path}")
        return

    title = parse_front_matter(post_path)
    if not title:
        print(f"Error: Could not extract title from {post_path}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{post_name}.png"
    create_thumbnail(title, output_path)

def generate_all():
    """Generate thumbnails for all posts."""
    if not POSTS_DIR.exists():
        print(f"Error: Posts directory not found: {POSTS_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    post_files = list(POSTS_DIR.glob("*.md"))
    print(f"Found {len(post_files)} posts")

    for post_file in post_files:
        title = parse_front_matter(post_file)
        if not title:
            print(f"⚠ Skipping {post_file.name} (no title found)")
            continue

        output_path = OUTPUT_DIR / f"{post_file.stem}.png"
        create_thumbnail(title, output_path)

    print(f"\n✓ Generated {len(list(OUTPUT_DIR.glob('*.png')))} thumbnails in {OUTPUT_DIR}")

def list_posts():
    """List all available posts."""
    if not POSTS_DIR.exists():
        print(f"Error: Posts directory not found: {POSTS_DIR}")
        return

    post_files = sorted(POSTS_DIR.glob("*.md"))
    print(f"\nAvailable posts ({len(post_files)}):\n")

    for post_file in post_files:
        title = parse_front_matter(post_file)
        if title:
            print(f"  • {post_file.stem}")
            print(f"    \"{title}\"")
            print()

def main():
    parser = argparse.ArgumentParser(
        description='Generate Instagram thumbnails from blog post titles'
    )
    parser.add_argument('--all', action='store_true',
                       help='Generate thumbnails for all posts')
    parser.add_argument('--post', type=str,
                       help='Generate thumbnail for specific post (without .md)')
    parser.add_argument('--list', action='store_true',
                       help='List all available posts')
    parser.add_argument('--scheme', type=str, choices=COLOR_SCHEMES.keys(),
                       help='Force specific color scheme')

    args = parser.parse_args()

    if args.list:
        list_posts()
    elif args.all:
        generate_all()
    elif args.post:
        generate_for_post(args.post)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python generate_thumbnails.py --all")
        print("  python generate_thumbnails.py --post pattern-of-corruption")
        print("  python generate_thumbnails.py --post thomas-corruption --scheme corruption")
        print("  python generate_thumbnails.py --list")

if __name__ == "__main__":
    main()
