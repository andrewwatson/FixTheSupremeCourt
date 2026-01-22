# Instagram Thumbnail Generator

This tool automatically creates Instagram-ready thumbnail images from your blog post titles.

## Features

- ✅ Automatically extracts titles from Hugo blog posts
- ✅ Generates 1080x1080px Instagram square images
- ✅ Smart color scheme selection based on content
- ✅ Automatic text wrapping and sizing
- ✅ Adds website URL at bottom
- ✅ High-quality PNG output

## Installation

### 1. Install Python Dependencies

```bash
pip install Pillow tomli
```

Or if you have a requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. Make Script Executable (Optional)

```bash
chmod +x generate_thumbnails.py
```

## Usage

### Generate Thumbnails for All Posts

```bash
python generate_thumbnails.py --all
```

This creates thumbnails for every blog post in `content/posts/` and saves them to `static/thumbnails/`.

### Generate Thumbnail for Specific Post

```bash
python generate_thumbnails.py --post pattern-of-corruption
```

### List All Available Posts

```bash
python generate_thumbnails.py --list
```

### Force Specific Color Scheme

```bash
python generate_thumbnails.py --post thomas-corruption --scheme corruption
```

## Color Schemes

The generator automatically selects color schemes based on post title keywords:

### `corruption` (Black bg, Gold text)
**Triggers:** corruption, gifts, thomas, alito, ethics

- Background: Black (#000000)
- Text: Gold (#FFD700)
- Accent: Crimson (#DC143C)

**Best for:** Ethics scandals, corruption posts

### `urgent` (Dark Red bg, White text)
**Triggers:** broke, destroyed, dismantled, failed

- Background: Dark Red (#8B0000)
- Text: White (#FFFFFF)
- Accent: Gold (#FFD700)

**Best for:** Alarming decisions, democratic failures

### `democracy` (Navy bg, White text)
**Triggers:** reform, solution, fix, need

- Background: Navy Blue (#0D1B3E)
- Text: White (#FFFFFF)
- Accent: Red (#DC3545)

**Best for:** Reform proposals, solutions

### `clean` (White bg, Dark text)
**Default fallback**

- Background: White (#FFFFFF)
- Text: Dark Gray (#212529)
- Accent: Blue (#007BFF)

**Best for:** Informational, explanatory posts

## Output

Thumbnails are saved to: `static/thumbnails/[post-name].png`

For example:
- `pattern-of-corruption.md` → `static/thumbnails/pattern-of-corruption.png`
- `thomas-corruption.md` → `static/thumbnails/thomas-corruption.png`

## Examples

### Example Commands

```bash
# Generate all thumbnails
python generate_thumbnails.py --all

# Generate one specific thumbnail
python generate_thumbnails.py --post federalist-society-court

# List all posts to see what's available
python generate_thumbnails.py --list

# Force the "urgent" red color scheme
python generate_thumbnails.py --post voting-rights-destruction --scheme urgent
```

### Sample Output

```
Found 37 posts
✓ Created: static/thumbnails/pattern-of-corruption.png
✓ Created: static/thumbnails/thomas-corruption.png
✓ Created: static/thumbnails/alito-scandal.png
...

✓ Generated 37 thumbnails in static/thumbnails
```

## Using the Thumbnails

### For Instagram Posts

1. Generate thumbnail: `python generate_thumbnails.py --post pattern-of-corruption`
2. Find image: `static/thumbnails/pattern-of-corruption.png`
3. Upload to Instagram
4. Add caption with link to blog post
5. Add hashtags (see SOCIAL_MEDIA_STRATEGY.md)

### For Instagram Stories

The 1080x1080px images work for Stories but will have white bars top/bottom. For Stories-specific content, you might want to create 1080x1920px versions (TODO: add this feature).

### For Twitter/X

These thumbnails work great for Twitter as well. Twitter will crop them to 2:1 ratio in timeline but full image shows when clicked.

## Customization

### Change Image Size

Edit the `IMAGE_SIZE` constant in `generate_thumbnails.py`:

```python
IMAGE_SIZE = (1080, 1350)  # For Instagram portrait
# or
IMAGE_SIZE = (1080, 1920)  # For Instagram Stories
```

### Modify Color Schemes

Edit the `COLOR_SCHEMES` dictionary:

```python
COLOR_SCHEMES = {
    "yourtheme": {
        "bg": (R, G, B),      # Background color
        "text": (R, G, B),     # Main text color
        "accent": (R, G, B)    # Accent/URL color
    }
}
```

### Change Font

The script tries to use Helvetica (macOS) or Arial (Windows). To use a different font:

```python
font = ImageFont.truetype("/path/to/your/font.ttf", font_size)
```

### Adjust Text Wrapping

Modify the padding in the `create_thumbnail` function:

```python
max_width = IMAGE_SIZE[0] - 200  # Increase padding (100px each side)
```

## Troubleshooting

### "Module not found: tomli"

Install the dependency:
```bash
pip install tomli
```

### "Module not found: PIL"

Install Pillow:
```bash
pip install Pillow
```

### "Font not found"

The script will fall back to default font. To use custom fonts, download a .ttf file and specify the path in the code.

### "Post not found"

Make sure you're using the post filename without the `.md` extension:
- ✅ `--post pattern-of-corruption`
- ❌ `--post pattern-of-corruption.md`

### Text Too Small/Large

The script auto-sizes text, but you can manually adjust the `font_size` variable in `create_thumbnail()`.

## Advanced Usage

### Batch Generate for Recent Posts

```bash
# Get last 5 modified posts
ls -t content/posts/*.md | head -5 | xargs -I {} basename {} .md | xargs -I {} python generate_thumbnails.py --post {}
```

### Automated Workflow

Create a git hook or CI/CD step to automatically generate thumbnails when new posts are added:

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Find posts modified in this commit
git diff --cached --name-only | grep 'content/posts/.*\.md$' | while read file; do
    post_name=$(basename "$file" .md)
    python generate_thumbnails.py --post "$post_name"
    git add "static/thumbnails/$post_name.png"
done
```

## Future Enhancements

Potential features to add:

- [ ] Instagram Stories format (1080x1920)
- [ ] Multiple color scheme variants per post
- [ ] Add post excerpt/summary below title
- [ ] Add author byline
- [ ] Add post date
- [ ] Generate carousel slides (multiple images per post)
- [ ] Video thumbnail generation
- [ ] Batch export to Google Drive/Dropbox
- [ ] Integration with Canva API
- [ ] A/B testing variants

## Integration with Hugo

### Add Thumbnails to Posts

You can reference generated thumbnails in your Hugo front matter:

```toml
+++
title = "Pattern of Corruption"
thumbnail = "/thumbnails/pattern-of-corruption.png"
+++
```

Then use in templates:

```html
{{ if .Params.thumbnail }}
<meta property="og:image" content="{{ .Params.thumbnail | absURL }}" />
<meta name="twitter:image" content="{{ .Params.thumbnail | absURL }}" />
{{ end }}
```

This will make your blog posts show the thumbnail when shared on social media.

## Questions?

See the main [SOCIAL_MEDIA_STRATEGY.md](SOCIAL_MEDIA_STRATEGY.md) for the complete Instagram marketing strategy.
