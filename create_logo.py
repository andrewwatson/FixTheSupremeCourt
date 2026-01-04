#!/usr/bin/env python3
"""
Create a simple logo for FixTheSupremeCourt.com

Generates a clean, professional logo that can be used on thumbnails,
social media profiles, and the website.

Usage:
    python create_logo.py --style scales
    python create_logo.py --style gavel
    python create_logo.py --style building
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import argparse

OUTPUT_DIR = Path("static")

def get_font(size):
    """Get the best available font."""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]

    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    return ImageFont.load_default()

def create_scales_logo(size=(400, 400)):
    """Create logo with scales of justice icon."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    gold = (218, 165, 32)
    navy = (13, 27, 62)

    center_x = size[0] // 2
    center_y = size[1] // 2

    # Draw simple scales
    # Central pole
    pole_top = center_y - 80
    pole_bottom = center_y + 60
    draw.rectangle([center_x - 8, pole_top, center_x + 8, pole_bottom], fill=navy)

    # Base
    base_width = 100
    draw.rectangle([center_x - base_width//2, pole_bottom - 5,
                   center_x + base_width//2, pole_bottom + 15], fill=navy)

    # Crossbar
    bar_y = pole_top + 20
    bar_width = 140
    draw.rectangle([center_x - bar_width, bar_y - 4,
                   center_x + bar_width, bar_y + 4], fill=gold)

    # Left scale pan
    left_x = center_x - bar_width + 20
    draw.ellipse([left_x - 40, bar_y + 20, left_x + 40, bar_y + 35], fill=gold)
    draw.line([(left_x - 30, bar_y + 4), (left_x - 30, bar_y + 20)], fill=gold, width=3)
    draw.line([(left_x + 30, bar_y + 4), (left_x + 30, bar_y + 20)], fill=gold, width=3)

    # Right scale pan
    right_x = center_x + bar_width - 20
    draw.ellipse([right_x - 40, bar_y + 20, right_x + 40, bar_y + 35], fill=gold)
    draw.line([(right_x - 30, bar_y + 4), (right_x - 30, bar_y + 20)], fill=gold, width=3)
    draw.line([(right_x + 30, bar_y + 4), (right_x + 30, bar_y + 20)], fill=gold, width=3)

    # X mark on scales (broken justice)
    x_size = 25
    x_y = bar_y + 27
    draw.line([(center_x - x_size, x_y - x_size), (center_x + x_size, x_y + x_size)],
             fill=(220, 20, 60), width=8)
    draw.line([(center_x - x_size, x_y + x_size), (center_x + x_size, x_y - x_size)],
             fill=(220, 20, 60), width=8)

    return img

def create_text_logo(text="FIX\nSCOTUS", size=(400, 400), bg_color=(13, 27, 62)):
    """Create text-based logo."""
    img = Image.new('RGBA', size, bg_color + (255,))
    draw = ImageDraw.Draw(img)

    # Colors
    gold = (218, 165, 32)
    white = (255, 255, 255)

    # Large text
    font = get_font(80)

    lines = text.split('\n')
    line_height = 90
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2

    for line in lines:
        bbox = font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (size[0] - text_width) // 2

        # Shadow
        draw.text((x + 3, y + 3), line, fill=(0, 0, 0, 100), font=font)
        # Main text
        draw.text((x, y), line, fill=gold, font=font)
        y += line_height

    # Border
    draw.rectangle([10, 10, size[0] - 10, size[1] - 10], outline=gold, width=5)

    return img

def create_gavel_logo(size=(400, 400)):
    """Create logo with gavel icon."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    gold = (218, 165, 32)
    navy = (13, 27, 62)
    red = (220, 20, 60)

    center_x = size[0] // 2
    center_y = size[1] // 2

    # Gavel head (rotated)
    gavel_angle = -30
    import math
    angle_rad = math.radians(gavel_angle)

    # Draw simplified gavel
    # Head
    head_length = 80
    head_width = 40
    head_x = center_x - 40
    head_y = center_y - 40
    draw.rectangle([head_x, head_y, head_x + head_length, head_y + head_width], fill=navy)

    # Handle
    handle_length = 100
    handle_width = 15
    handle_x = head_x + head_length - 10
    handle_y = head_y + head_width
    draw.rectangle([handle_x, handle_y, handle_x + handle_width, handle_y + handle_length], fill=navy)

    # Crack through gavel (broken justice)
    crack_x = head_x + head_length // 2
    draw.line([(crack_x, head_y - 10), (crack_x + 30, head_y + head_width + 120)],
             fill=red, width=6)

    # Sound block
    block_size = 60
    block_x = center_x + 60
    block_y = center_y + 60
    draw.rectangle([block_x, block_y, block_x + block_size, block_y + 20], fill=gold)

    return img

def create_circle_logo(text="FIX", size=(400, 400)):
    """Create circular badge logo."""
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Colors
    navy = (13, 27, 62)
    gold = (218, 165, 32)
    white = (255, 255, 255)

    center_x = size[0] // 2
    center_y = size[1] // 2
    radius = 180

    # Outer circle
    draw.ellipse([center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius], fill=navy)

    # Inner circle (border)
    inner_radius = radius - 20
    draw.ellipse([center_x - inner_radius, center_y - inner_radius,
                 center_x + inner_radius, center_y + inner_radius],
                fill=navy, outline=gold, width=8)

    # Text - three lines for "FIX THE SUPREME COURT"
    font_large = get_font(56)  # Smaller to fit three lines
    font_medium = get_font(44)
    font_small = get_font(56)

    # Line 1: "FIX"
    line1 = "FIX"
    bbox1 = font_large.getbbox(line1)
    text1_width = bbox1[2] - bbox1[0]
    x1 = center_x - text1_width // 2
    y1 = center_y - 75
    draw.text((x1, y1), line1, fill=gold, font=font_large)

    # Line 2: "THE SUPREME"
    line2 = "THE SUPREME"
    bbox2 = font_medium.getbbox(line2)
    text2_width = bbox2[2] - bbox2[0]
    x2 = center_x - text2_width // 2
    y2 = center_y - 20
    draw.text((x2, y2), line2, fill=white, font=font_medium)

    # Line 3: "COURT"
    line3 = "COURT"
    bbox3 = font_small.getbbox(line3)
    text3_width = bbox3[2] - bbox3[0]
    x3 = center_x - text3_width // 2
    y3 = center_y + 40
    draw.text((x3, y3), line3, fill=gold, font=font_small)

    return img

def create_simple_icon(size=(400, 400)):
    """Create very simple, minimal icon."""
    img = Image.new('RGBA', size, (13, 27, 62, 255))  # Navy background
    draw = ImageDraw.Draw(img)

    gold = (218, 165, 32)
    red = (220, 20, 60)

    center_x = size[0] // 2
    center_y = size[1] // 2

    # Large "F" shape
    font = get_font(280)
    text = "F"
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    x = center_x - text_width // 2
    y = center_y - 180

    draw.text((x, y), text, fill=gold, font=font)

    # Crack/strike through
    draw.line([(80, 80), (320, 320)], fill=red, width=15)

    return img

def main():
    parser = argparse.ArgumentParser(description='Create logo for FixTheSupremeCourt.com')
    parser.add_argument('--style',
                       choices=['scales', 'gavel', 'text', 'circle', 'simple'],
                       default='scales',
                       help='Logo style')
    parser.add_argument('--size', type=int, default=400,
                       help='Logo size (square)')

    args = parser.parse_args()

    OUTPUT_DIR.mkdir(exist_ok=True)

    size = (args.size, args.size)

    if args.style == 'scales':
        img = create_scales_logo(size)
        filename = 'logo_scales.png'
    elif args.style == 'gavel':
        img = create_gavel_logo(size)
        filename = 'logo_gavel.png'
    elif args.style == 'text':
        img = create_text_logo("FIX\nSCOTUS", size)
        filename = 'logo_text.png'
    elif args.style == 'circle':
        img = create_circle_logo("FIX", size)
        filename = 'logo_circle.png'
    elif args.style == 'simple':
        img = create_simple_icon(size)
        filename = 'logo_simple.png'

    output_path = OUTPUT_DIR / filename
    img.save(output_path, quality=95)

    print(f"✓ Created logo: {output_path}")
    print(f"  Style: {args.style}")
    print(f"  Size: {size[0]}x{size[1]}px")
    print(f"\nUse this for:")
    print(f"  - Instagram profile picture (crop to circle)")
    print(f"  - Twitter/X profile")
    print(f"  - Website favicon")
    print(f"  - Thumbnail watermark")

if __name__ == "__main__":
    main()
