#!/bin/bash
# Quick wrapper to prepare Instagram posts

# Activate venv if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

python3 prepare_instagram_post.py "$@"
