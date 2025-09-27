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

This is a standard Hugo site with the following key directories:

- `content/` - Markdown files for site content (currently empty)
- `layouts/` - HTML templates for rendering content (currently empty, likely using theme layouts)
- `static/` - Static assets (images, CSS, JS) served directly
- `themes/` - Hugo themes (currently empty)
- `data/` - YAML/JSON/TOML data files for site data
- `assets/` - Assets to be processed by Hugo Pipes
- `i18n/` - Translation files for internationalization
- `archetypes/` - Content templates for `hugo new` command
- `public/` - Generated site output (should be in .gitignore for most workflows)

## Configuration

- `hugo.toml` - Main configuration file
  - Currently configured with placeholder values (baseURL: 'https://example.org/', title: 'My New Hugo Site')
  - These should be updated for the actual site

## Development Workflow

1. Use `hugo server -D` during development to see drafts and live reload changes
2. Create new content with `hugo new` commands
3. Build for production with `hugo` when ready to deploy
4. The generated site in `public/` directory can be deployed to any static hosting service

## Notes

- The site is currently in initial state with empty content and layout directories
- No theme is currently installed - layouts will need to be created manually or a theme added
- Hugo version in use: v0.148.2+extended (supports Sass/SCSS processing and other extended features)