#!/bin/bash
# Quick thumbnail generator script
# Makes it easier to generate thumbnails without remembering Python commands

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Supreme Court Blog Thumbnail Generator ===${NC}\n"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found. Run: python3 -m venv venv"
    exit 1
fi

# Activate venv
source venv/bin/activate

# Parse arguments
case "$1" in
    "all")
        echo -e "${GREEN}Generating thumbnails for all posts...${NC}\n"
        python generate_thumbnails.py --all
        ;;
    "list")
        echo -e "${GREEN}Available posts:${NC}\n"
        python generate_thumbnails.py --list
        ;;
    "recent")
        echo -e "${GREEN}Generating thumbnails for 5 most recent posts...${NC}\n"
        ls -t content/posts/*.md | head -5 | while read file; do
            post_name=$(basename "$file" .md)
            python generate_thumbnails.py --post "$post_name"
        done
        ;;
    "")
        echo "Usage: ./make_thumbnails.sh [COMMAND]"
        echo ""
        echo "Commands:"
        echo "  all           Generate thumbnails for all posts"
        echo "  list          List all available posts"
        echo "  recent        Generate for 5 most recent posts"
        echo "  [post-name]   Generate thumbnail for specific post"
        echo ""
        echo "Examples:"
        echo "  ./make_thumbnails.sh all"
        echo "  ./make_thumbnails.sh pattern-of-corruption"
        echo "  ./make_thumbnails.sh recent"
        ;;
    *)
        echo -e "${GREEN}Generating thumbnail for: $1${NC}\n"
        python generate_thumbnails.py --post "$1"
        ;;
esac

echo ""
echo -e "${BLUE}Thumbnails saved to: static/thumbnails/${NC}"
echo -e "${BLUE}Ready to upload to Instagram!${NC}"
