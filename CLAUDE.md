# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Hugo static site project called "FixTheSupremeCourt". Hugo is a fast static site generator written in Go that builds websites from markdown content and templates.

## Development Commands

### Core Hugo Commands
- `hugo server` - Start the development server with live reload (typically serves on http://localhost:1313)
- `hugo server -D` - Start development server including draft content
- `hugo` or `hugo build` - Build the site for production (outputs to `public/` directory)
- `hugo new posts/post-name.md` - Create a new post with front matter
- `hugo new site-section/page-name.md` - Create a new page in a specific section

### Content Management
- `hugo list drafts` - List all draft content
- `hugo list future` - List content with future publish dates
- `hugo list expired` - List expired content

## Project Structure

This is a Hugo site with the following key directories:

- `content/posts/` - Blog posts (42+ posts about Supreme Court reform)
- `layouts/` - Custom layout overrides (uses PaperMod theme)
- `static/` - Static assets:
  - `static/headers/` - Blog header images (1200x630)
  - `static/thumbnails/` - Instagram images (1080x1080)
  - `static/logo_circle.png` - Site logo
- `themes/PaperMod/` - Hugo theme (PaperMod)
- `venv/` - Python virtual environment for image generation
- `public/` - Generated site output (gitignored)

## Configuration

- `hugo.toml` - Main configuration file
  - Site URL: https://fixthesupremecourt.org
  - Theme: PaperMod
  - Taxonomies enabled for tags and categories

## Development Workflow

1. Use `hugo server -D` during development to see drafts and live reload changes
2. Create new content with `hugo new` commands
3. Build for production with `hugo` when ready to deploy
4. The generated site in `public/` directory can be deployed to any static hosting service

## Image Generation

The site uses professional thumbnail and header image generation:

- `generate_thumbnails_pro.py` - Generates both Instagram (1080x1080) and blog header (1200x630) images
- All images use consistent branding with the site logo
- Images stored in `static/thumbnails/` and `static/headers/`

### Generate images for a post:
```bash
source venv/bin/activate
python generate_thumbnails_pro.py --post POST-SLUG
```

## Instagram Posting

Semi-automated Instagram posting workflow:

```bash
./instagram_post.sh --post POST-SLUG [--open]
```

This will:
- Generate Instagram image (1080x1080)
- Create formatted caption with relevant hashtags
- Copy caption to clipboard
- Show you which image to upload
- Optionally open Instagram in browser

See `INSTAGRAM_POSTING.md` for full documentation.

## Site Information

- **Live site**: https://fixthesupremecourt.org
- **Theme**: PaperMod
- **Content**: 42+ blog posts about Supreme Court reform
- **Hugo version**: v0.148.2+extended
- **Taxonomies**: Tags and categories enabled

## Content Guidelines

- Don't use twitter handles in front matter
- Default author for every post: "Editor"
- Tags should come BEFORE `[cover]` section in TOML front matter
- All posts should have header images at `/headers/POST-SLUG_modern.png`