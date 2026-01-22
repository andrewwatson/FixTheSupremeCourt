# Using Blog Header Images

The thumbnail generator now creates **two versions** of each image:

## Formats Generated

### 1. Instagram Square (1080x1080px)
- **Location**: `static/thumbnails/`
- **Use for**: Instagram posts
- **Format**: Square, optimized for social media feeds

### 2. Blog Header (1200x630px)
- **Location**: `static/headers/`
- **Use for**:
  - Blog post featured images
  - Open Graph images (social sharing previews)
  - Twitter cards
  - LinkedIn previews
- **Format**: 1.9:1 ratio (Open Graph standard)

## Adding to Hugo Blog Posts

Add the blog header image to your post's front matter:

```toml
+++
date = '2025-12-28T00:05:42-05:00'
draft = false
title = 'A Pattern of Corruption: Why Self-Policing Has Failed at the Supreme Court'
author = 'Editor'

[cover]
image = '/headers/pattern-of-corruption_modern.png'
alt = 'A Pattern of Corruption: Why Self-Policing Has Failed at the Supreme Court'
+++
```

## How It Works

When you run:
```bash
python generate_thumbnails_pro.py --post pattern-of-corruption
```

The script automatically generates **both**:
1. `static/thumbnails/pattern-of-corruption_modern.png` (1080x1080)
2. `static/headers/pattern-of-corruption_modern.png` (1200x630)

## Social Sharing Benefits

The 1200x630px header format ensures your posts look great when shared on:
- **Facebook**: Uses Open Graph image
- **Twitter/X**: Uses Twitter Card image
- **LinkedIn**: Uses og:image
- **Slack/Discord**: Displays rich preview
- **Google Search**: May show as result thumbnail

All these platforms will automatically pull the image from your `cover.image` field.

## Template Consistency

Both formats use the same:
- ✅ Color scheme
- ✅ Typography
- ✅ Logo placement
- ✅ Brand style

The only difference is the aspect ratio, with the blog headers optimized for horizontal display.

## File Organization

```
static/
├── headers/           # Blog headers (1200x630)
│   ├── abortion_modern.png
│   ├── pattern-of-corruption_modern.png
│   └── ... (37 total)
├── thumbnails/        # Instagram squares (1080x1080)
│   ├── abortion_modern.png
│   ├── pattern-of-corruption_modern.png
│   └── ... (37 total)
└── logo_circle.png
```

## Bulk Adding to Posts

To add header images to all posts, you can edit the front matter:

```bash
for post in content/posts/*.md; do
    post_name=$(basename "$post" .md)
    # Add cover image if not already present
    if ! grep -q "^\[cover\]" "$post"; then
        # Insert after front matter opening
        sed -i '' "/^+++$/a\\
\\
[cover]\\
image = '/headers/${post_name}_modern.png'
" "$post"
    fi
done
```

## Regenerating Images

Both formats are regenerated together:

```bash
# Regenerate all posts (both formats)
source venv/bin/activate
for post in content/posts/*.md; do
    post_name=$(basename "$post" .md)
    python generate_thumbnails_pro.py --post "$post_name"
done
```

This creates 74 total images (37 Instagram + 37 blog headers).
