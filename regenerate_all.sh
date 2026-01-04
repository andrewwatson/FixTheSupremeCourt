#!/bin/bash
# Regenerate all thumbnails with new logo

cd /Users/andy/development/projects/FixTheSupremeCourt

for post in content/posts/*.md; do
    post_name=$(basename "$post" .md)
    echo "Processing: $post_name"
    venv/bin/python3 generate_thumbnails_pro.py --post "$post_name"
done

# Also regenerate thesis
echo "Processing: thesis (featured)"
venv/bin/python3 -c "
import sys
sys.path.insert(0, '.')
exec(open('generate_thumbnails_pro.py').read(), globals())
title = 'A Stolen Court: How the Supreme Court Lost Its Legitimacy and Why Reform Is Overdue'
instagram_path = Path('static/thumbnails/thesis_modern.png')
header_path = Path('static/headers/thesis_modern.png')
create_thumbnail(title, instagram_path, 'modern', None, size=INSTAGRAM_SIZE)
create_thumbnail(title, header_path, 'modern', None, size=BLOG_HEADER_SIZE)
print('✓ Created Instagram (modern): static/thumbnails/thesis_modern.png')
print('✓ Created Blog (modern): static/headers/thesis_modern.png')
"

echo ""
echo "Done! All thumbnails regenerated with new logo."
