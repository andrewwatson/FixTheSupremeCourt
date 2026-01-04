#!/usr/bin/env python3
"""
Professional Instagram thumbnail generator with advanced graphics.

Enhanced version with:
- Multiple template designs
- Logo support
- Background patterns
- Better typography
- Gradient backgrounds
- Icon support

Requirements:
    pip install Pillow tomli

Usage:
    python generate_thumbnails_pro.py --post POST_NAME --template modern
"""

import tomli
import argparse
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import textwrap
import re
import math

# Configuration
OUTPUT_DIR = Path("static/thumbnails")
BLOG_HEADERS_DIR = Path("static/headers")
POSTS_DIR = Path("content/posts")
# Logo paths - will use first one found
LOGO_PATHS = [
    Path("static/logo_circle.png"),
    Path("static/logo_simple.png"),
    Path("static/logo.png"),
]
# Image sizes - will generate both formats
INSTAGRAM_SIZE = (1080, 1080)  # Square for Instagram
BLOG_HEADER_SIZE = (1200, 630)  # Open Graph standard for blog/social
USE_LOGO = True  # Set to False to disable logo

# Enhanced color schemes with gradients
COLOR_SCHEMES = {
    "corruption": {
        "bg_top": (20, 20, 20),      # Near black
        "bg_bottom": (40, 0, 0),     # Dark red
        "text": (255, 215, 0),        # Gold
        "accent": (220, 20, 60),      # Crimson
        "overlay": (0, 0, 0, 180)     # Semi-transparent overlay
    },
    "democracy": {
        "bg_top": (13, 27, 62),       # Navy blue
        "bg_bottom": (25, 50, 100),   # Lighter navy
        "text": (255, 255, 255),      # White
        "accent": (220, 53, 69),      # Red
        "overlay": (13, 27, 62, 180)  # Navy overlay
    },
    "urgent": {
        "bg_top": (139, 0, 0),        # Dark red
        "bg_bottom": (200, 0, 0),     # Brighter red
        "text": (255, 255, 255),      # White
        "accent": (255, 215, 0),      # Gold
        "overlay": (139, 0, 0, 180)   # Red overlay
    },
    "clean": {
        "bg_top": (240, 240, 245),    # Light gray
        "bg_bottom": (255, 255, 255), # White
        "text": (33, 37, 41),         # Dark gray
        "accent": (0, 123, 255),      # Blue
        "overlay": (255, 255, 255, 200)
    },
    "justice": {
        "bg_top": (25, 25, 112),      # Midnight blue
        "bg_bottom": (72, 61, 139),   # Dark slate blue
        "text": (255, 255, 255),      # White
        "accent": (218, 165, 32),     # Goldenrod
        "overlay": (25, 25, 112, 180)
    }
}

# Template designs
TEMPLATES = {
    "bold": "Large centered text, minimal design",
    "modern": "Geometric shapes, contemporary feel",
    "classic": "Traditional layout with ornamental elements",
    "minimal": "Maximum whitespace, subtle accents",
    "impact": "High contrast, attention-grabbing",
}

def parse_front_matter(post_path):
    """Extract title from TOML front matter."""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

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

    if any(word in title_lower for word in ['corruption', 'gifts', 'thomas', 'alito', 'ethics', 'scandal']):
        return COLOR_SCHEMES['corruption']
    elif any(word in title_lower for word in ['broke', 'destroyed', 'dismantled', 'failed', 'crisis']):
        return COLOR_SCHEMES['urgent']
    elif any(word in title_lower for word in ['reform', 'solution', 'fix', 'need', 'democracy', 'voting']):
        return COLOR_SCHEMES['democracy']
    elif any(word in title_lower for word in ['justice', 'court', 'federalist', 'supreme']):
        return COLOR_SCHEMES['justice']
    else:
        return COLOR_SCHEMES['clean']

def create_gradient_background(size, color_top, color_bottom, direction='vertical'):
    """Create a gradient background."""
    width, height = size
    gradient = Image.new('RGB', size)
    draw = ImageDraw.Draw(gradient)

    if direction == 'vertical':
        for y in range(height):
            ratio = y / height
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:  # horizontal
        for x in range(width):
            ratio = x / width
            r = int(color_top[0] * (1 - ratio) + color_bottom[0] * ratio)
            g = int(color_top[1] * (1 - ratio) + color_bottom[1] * ratio)
            b = int(color_top[2] * (1 - ratio) + color_bottom[2] * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return gradient

def add_geometric_pattern(img, colors):
    """Add subtle geometric pattern overlay."""
    draw = ImageDraw.Draw(img, 'RGBA')
    width, height = img.size

    # Add subtle diagonal lines
    overlay_color = (*colors['accent'][:3], 20)  # Very transparent
    line_spacing = 60

    for i in range(-height, width, line_spacing):
        draw.line([(i, 0), (i + height, height)], fill=overlay_color, width=2)

    return img

def add_corner_accents(draw, size, color, accent_size=40):
    """Add decorative corner accents."""
    width, height = size

    # Top left corner
    draw.rectangle([0, 0, accent_size, 5], fill=color)
    draw.rectangle([0, 0, 5, accent_size], fill=color)

    # Top right corner
    draw.rectangle([width - accent_size, 0, width, 5], fill=color)
    draw.rectangle([width - 5, 0, width, accent_size], fill=color)

    # Bottom left corner
    draw.rectangle([0, height - 5, accent_size, height], fill=color)
    draw.rectangle([0, height - accent_size, 5, height], fill=color)

    # Bottom right corner
    draw.rectangle([width - accent_size, height - 5, width, height], fill=color)
    draw.rectangle([width - 5, height - accent_size, width, height], fill=color)

def get_font(size, bold=False):
    """Get the best available font."""
    font_paths = [
        # macOS
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNS.ttf",
        # Common fonts
        "arial.ttf",
        "Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue

    return ImageFont.load_default()

def wrap_text_smart(text, font, max_width):
    """Intelligently wrap text, trying to break at logical points."""
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        test_line = current_line + [word]
        test_text = ' '.join(test_line)
        bbox = font.getbbox(test_text)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                # Word itself is too long, just add it
                lines.append(word)
                current_line = []

    if current_line:
        lines.append(' '.join(current_line))

    return lines

def add_logo_and_save(img, output_path, bg_color, position='top-right', size=70, opacity=180):
    """
    Add logo to image and save.

    Args:
        img: PIL Image to add logo to
        output_path: Where to save
        bg_color: Background color for RGB conversion
        position: 'bottom-right', 'bottom-left', 'top-right', 'top-left'
        size: Logo size in pixels
        opacity: 0-255, lower = more transparent
    """
    # Add logo if enabled
    if USE_LOGO:
        # Find first available logo
        logo_path = None
        for path in LOGO_PATHS:
            if path.exists():
                logo_path = path
                break

        if logo_path:
            try:
                logo = Image.open(logo_path).convert('RGBA')
                logo = logo.resize((size, size), Image.Resampling.LANCZOS)

                # Adjust opacity
                if opacity < 255:
                    alpha = logo.split()[3]
                    alpha = alpha.point(lambda p: int(p * opacity / 255))
                    logo.putalpha(alpha)

                # Calculate position
                padding = 20
                if position == 'bottom-right':
                    x = img.width - size - padding
                    y = img.height - size - padding
                elif position == 'bottom-left':
                    x = padding
                    y = img.height - size - padding
                elif position == 'top-right':
                    x = img.width - size - padding
                    y = padding
                elif position == 'top-left':
                    x = padding
                    y = padding
                else:
                    x = img.width - size - padding
                    y = img.height - size - padding

                # Convert img to RGBA if not already
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                # Paste logo
                img.paste(logo, (x, y), logo)

            except:
                pass  # If logo loading fails, continue without it

    # Convert back to RGB for saving
    if img.mode == 'RGBA':
        rgb_img = Image.new('RGB', img.size, bg_color)
        rgb_img.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        rgb_img.save(output_path, quality=95)
    else:
        img.save(output_path, quality=95)

def create_thumbnail_bold(title, output_path, colors, size=INSTAGRAM_SIZE):
    """Bold template: Large centered text, minimal design."""
    # Create gradient background
    img = create_gradient_background(size, colors['bg_top'], colors['bg_bottom'])

    # Add subtle pattern
    img = add_geometric_pattern(img, colors)

    draw = ImageDraw.Draw(img, 'RGBA')

    # Title - scale font size based on image size
    base_font_size = int(75 * (size[0] / INSTAGRAM_SIZE[0]))
    font = get_font(base_font_size, bold=True)
    max_width = size[0] - int(120 * (size[0] / INSTAGRAM_SIZE[0]))
    lines = wrap_text_smart(title, font, max_width)

    # Calculate text positioning
    line_height = font.getbbox("Ay")[3] + int(25 * (size[1] / INSTAGRAM_SIZE[1]))
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2

    # Draw text with shadow
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2

        # Shadow
        draw.text((x + 4, y + 4), line, fill=(0, 0, 0, 100), font=font)
        # Main text
        draw.text((x, y), line, fill=colors['text'], font=font)
        y += line_height

    # Add accent line above and below
    margin = int(100 * (size[0] / INSTAGRAM_SIZE[0]))
    accent_y_top = (size[1] - total_height) // 2 - int(30 * (size[1] / INSTAGRAM_SIZE[1]))
    accent_y_bottom = accent_y_top + total_height + int(60 * (size[1] / INSTAGRAM_SIZE[1]))
    draw.rectangle([margin, accent_y_top, size[0] - margin, accent_y_top + 4],
                  fill=colors['accent'])
    draw.rectangle([margin, accent_y_bottom, size[0] - margin, accent_y_bottom + 4],
                  fill=colors['accent'])

    # Add URL
    url_font_size = int(28 * (size[0] / INSTAGRAM_SIZE[0]))
    url_font = get_font(url_font_size)
    url = "FixTheSupremeCourt.com"
    url_bbox = url_font.getbbox(url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (size[0] - url_width) // 2
    url_y = size[1] - int(70 * (size[1] / INSTAGRAM_SIZE[1]))
    draw.text((url_x, url_y), url, fill=colors['accent'], font=url_font)

    # Add logo and save
    logo_size = int(70 * (size[0] / INSTAGRAM_SIZE[0]))
    add_logo_and_save(img, output_path, colors['bg_top'], size=logo_size)

def create_thumbnail_modern(title, output_path, colors, size=INSTAGRAM_SIZE):
    """Modern template: Geometric shapes, contemporary feel."""
    # Create gradient background
    img = create_gradient_background(size, colors['bg_top'], colors['bg_bottom'])

    draw = ImageDraw.Draw(img, 'RGBA')

    # Add large geometric shape (circle) in background - scale to image size
    scale = size[0] / INSTAGRAM_SIZE[0]
    circle_color = (*colors['accent'][:3], 40)
    draw.ellipse([int(700*scale), int(-200*scale), int(1300*scale), int(400*scale)], fill=circle_color)
    draw.ellipse([int(-100*scale), int(700*scale), int(500*scale), int(1300*scale)], fill=circle_color)

    # Add colored bar on left side
    bar_color = (*colors['accent'][:3], 120)
    draw.rectangle([0, 0, int(15*scale), size[1]], fill=bar_color)

    # Title
    font_size = int(70 * scale)
    font = get_font(font_size, bold=True)
    max_width = size[0] - int(160 * scale)
    lines = wrap_text_smart(title, font, max_width)

    # Calculate positioning (left-aligned with padding)
    line_height = font.getbbox("Ay")[3] + int(22 * scale)
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2
    x_start = int(80 * scale)

    # Draw text
    for line in lines:
        # Shadow
        draw.text((x_start + 3, y + 3), line, fill=(0, 0, 0, 80), font=font)
        # Main text
        draw.text((x_start, y), line, fill=colors['text'], font=font)
        y += line_height

    # Add URL in bottom right
    url_font = get_font(int(26 * scale))
    url = "FixTheSupremeCourt.com"
    url_bbox = url_font.getbbox(url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = size[0] - url_width - int(40 * scale)
    url_y = size[1] - int(60 * scale)

    # URL background
    draw.rectangle([url_x - 15, url_y - 10, url_x + url_width + 15, url_y + 40],
                  fill=(*colors['accent'][:3], 200))
    draw.text((url_x, url_y), url, fill=colors['text'], font=url_font)

    # Add logo and save (larger, more visible) - scale logo size
    logo_size = int(102 * scale)
    add_logo_and_save(img, output_path, colors['bg_top'], size=logo_size, opacity=230)

def create_thumbnail_classic(title, output_path, colors, size=INSTAGRAM_SIZE):
    """Classic template: Traditional layout with ornamental elements."""
    # Create gradient background
    img = create_gradient_background(size, colors['bg_top'], colors['bg_bottom'])
    scale = size[0] / INSTAGRAM_SIZE[0]

    draw = ImageDraw.Draw(img, 'RGBA')

    # Add corner accents
    add_corner_accents(draw, size, colors['accent'], accent_size=int(50*scale))

    # Add border frame
    frame_color = (*colors['accent'][:3], 150)
    draw.rectangle([int(30*scale), int(30*scale), size[0] - int(30*scale), size[1] - int(30*scale)],
                  outline=frame_color, width=3)
    draw.rectangle([int(35*scale), int(35*scale), size[0] - int(35*scale), size[1] - int(35*scale)],
                  outline=frame_color, width=1)

    # Title
    font = get_font(int(65*scale), bold=True)
    max_width = size[0] - int(180*scale)
    lines = wrap_text_smart(title, font, max_width)

    # Calculate positioning (centered)
    line_height = font.getbbox("Ay")[3] + int(20*scale)
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2

    # Draw text
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2

        # Shadow
        draw.text((x + 3, y + 3), line, fill=(0, 0, 0, 100), font=font)
        # Main text
        draw.text((x, y), line, fill=colors['text'], font=font)
        y += line_height

    # Add decorative line separator
    sep_y = size[1] - int(140*scale)
    draw.rectangle([int(200*scale), sep_y, size[0] - int(200*scale), sep_y + 2], fill=colors['accent'])

    # Add URL centered at bottom
    url_font = get_font(int(30*scale))
    url = "FixTheSupremeCourt.com"
    url_bbox = url_font.getbbox(url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (size[0] - url_width) // 2
    url_y = size[1] - int(90*scale)
    draw.text((url_x, url_y), url, fill=colors['accent'], font=url_font)

    # Add logo and save
    add_logo_and_save(img, output_path, colors['bg_top'])

def create_thumbnail_minimal(title, output_path, colors, size=INSTAGRAM_SIZE):
    """Minimal template: Maximum whitespace, subtle accents."""
    # Create solid or subtle gradient
    img = create_gradient_background(size, colors['bg_top'], colors['bg_bottom'])

    scale = size[0] / INSTAGRAM_SIZE[0]

    draw = ImageDraw.Draw(img, 'RGBA')

    # Single accent element (thin line on left)
    draw.rectangle([int(60*scale), int(200*scale), int(65*scale), size[1] - int(200*scale)], fill=colors['accent'])

    # Title - smaller, more space
    font = get_font(int(62*scale))
    max_width = size[0] - int(250*scale)
    lines = wrap_text_smart(title, font, max_width)

    # Left-aligned with lots of padding
    line_height = font.getbbox("Ay")[3] + int(28*scale)
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2
    x_start = int(120*scale)

    # Draw text (no shadow - clean look)
    for line in lines:
        draw.text((x_start, y), line, fill=colors['text'], font=font)
        y += line_height

    # URL - small and subtle
    url_font = get_font(int(24*scale))
    url = "FixTheSupremeCourt.com"
    draw.text((int(120*scale), size[1] - int(80*scale)), url, fill=colors['accent'], font=url_font)

    # Add logo and save
    add_logo_and_save(img, output_path, colors['bg_top'], position='top-right', size=int(60*scale), opacity=150)

def create_thumbnail_impact(title, output_path, colors, size=INSTAGRAM_SIZE):
    """Impact template: High contrast, attention-grabbing."""
    # Dark background
    img = create_gradient_background(size, colors['bg_top'], colors['bg_bottom'])

    scale = size[0] / INSTAGRAM_SIZE[0]

    draw = ImageDraw.Draw(img, 'RGBA')

    # Large diagonal stripe
    stripe_color = (*colors['accent'][:3], 100)
    points = [(0, size[1] // 2), (size[0], size[1] // 2 - 300),
              (size[0], size[1] // 2 - 150), (0, size[1] // 2 + 150)]
    draw.polygon(points, fill=stripe_color)

    # Title - very large
    font = get_font(int(80*scale), bold=True)
    max_width = size[0] - int(140*scale)
    lines = wrap_text_smart(title, font, max_width)

    # Calculate positioning
    line_height = font.getbbox("Ay")[3] + int(20*scale)
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2 - 30

    # Draw text with strong shadow
    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2

        # Strong shadow
        draw.text((x + 5, y + 5), line, fill=(0, 0, 0, 200), font=font)
        # Outline effect
        for offset in [(1,0), (-1,0), (0,1), (0,-1)]:
            draw.text((x + offset[0], y + offset[1]), line, fill=(0, 0, 0, 100), font=font)
        # Main text
        draw.text((x, y), line, fill=colors['text'], font=font)
        y += line_height

    # URL with background
    url_font = get_font(int(32*scale), bold=True)
    url = "FixTheSupremeCourt.com"
    url_bbox = url_font.getbbox(url)
    url_width = url_bbox[2] - url_bbox[0]
    url_x = (size[0] - url_width) // 2
    url_y = size[1] - int(80*scale)

    # Background rectangle for URL
    padding = int(20*scale)
    draw.rectangle([url_x - padding, url_y - 10, url_x + url_width + padding, url_y + 45],
                  fill=colors['accent'])
    draw.text((url_x, url_y), url, fill=colors['bg_top'], font=url_font)

    # Add logo and save (smaller, more subtle for this template)
    add_logo_and_save(img, output_path, colors['bg_top'], position='top-left', size=int(65*scale), opacity=160)

def create_thumbnail(title, output_path, template='modern', scheme_name=None, size=INSTAGRAM_SIZE):
    """Generate thumbnail with specified template and size."""
    # Choose color scheme
    if scheme_name and scheme_name in COLOR_SCHEMES:
        colors = COLOR_SCHEMES[scheme_name]
    else:
        colors = get_color_scheme(title)

    # Select template function
    template_funcs = {
        'bold': create_thumbnail_bold,
        'modern': create_thumbnail_modern,
        'classic': create_thumbnail_classic,
        'minimal': create_thumbnail_minimal,
        'impact': create_thumbnail_impact,
    }

    template_func = template_funcs.get(template, create_thumbnail_modern)
    template_func(title, output_path, colors, size)
    size_label = "Instagram" if size == INSTAGRAM_SIZE else "Blog"
    print(f"✓ Created {size_label} ({template}): {output_path}")

def generate_for_post(post_name, template='modern', scheme=None):
    """Generate thumbnails for a specific post in both Instagram and blog formats."""
    post_path = POSTS_DIR / f"{post_name}.md"
    if not post_path.exists():
        print(f"Error: Post not found: {post_path}")
        return

    title = parse_front_matter(post_path)
    if not title:
        print(f"Error: Could not extract title from {post_path}")
        return

    # Create both output directories
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    BLOG_HEADERS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate Instagram square version
    instagram_path = OUTPUT_DIR / f"{post_name}_{template}.png"
    create_thumbnail(title, instagram_path, template, scheme, size=INSTAGRAM_SIZE)

    # Generate blog header version
    header_path = BLOG_HEADERS_DIR / f"{post_name}_{template}.png"
    create_thumbnail(title, header_path, template, scheme, size=BLOG_HEADER_SIZE)

def generate_all_variants(post_name):
    """Generate all template variants for a post."""
    post_path = POSTS_DIR / f"{post_name}.md"
    if not post_path.exists():
        print(f"Error: Post not found: {post_path}")
        return

    title = parse_front_matter(post_path)
    if not title:
        print(f"Error: Could not extract title from {post_path}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for template in TEMPLATES.keys():
        output_path = OUTPUT_DIR / f"{post_name}_{template}.png"
        create_thumbnail(title, output_path, template)

    print(f"\n✓ Created {len(TEMPLATES)} variants for {post_name}")

def main():
    parser = argparse.ArgumentParser(
        description='Generate professional Instagram thumbnails with templates'
    )
    parser.add_argument('--post', type=str,
                       help='Post name (without .md)')
    parser.add_argument('--template', type=str,
                       choices=list(TEMPLATES.keys()),
                       default='modern',
                       help='Template style to use (default: modern)')
    parser.add_argument('--scheme', type=str,
                       choices=list(COLOR_SCHEMES.keys()),
                       help='Force specific color scheme')
    parser.add_argument('--all-templates', action='store_true',
                       help='Generate all template variants for a post')
    parser.add_argument('--list-templates', action='store_true',
                       help='List available templates')

    args = parser.parse_args()

    if args.list_templates:
        print("\nAvailable Templates:\n")
        for name, desc in TEMPLATES.items():
            print(f"  {name:12} - {desc}")
        print()
    elif args.all_templates and args.post:
        generate_all_variants(args.post)
    elif args.post:
        generate_for_post(args.post, args.template, args.scheme)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python generate_thumbnails_pro.py --post pattern-of-corruption --template modern")
        print("  python generate_thumbnails_pro.py --post thomas-corruption --all-templates")
        print("  python generate_thumbnails_pro.py --list-templates")

if __name__ == "__main__":
    main()
