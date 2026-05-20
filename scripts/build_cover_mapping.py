#!/usr/bin/env python3
"""
Build cover image mapping for all articles in articles/index.html
"""
import os
import re
import json

ARTICLES_DIR = '/root/.openclaw/workspace/fun1399-clean/articles'

# Extract all slugs from articles/index.html
with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    index_html = f.read()

slugs = set()
for match in re.finditer(r'href="/articles/([^"]+)"', index_html):
    slug = match.group(1)
    if slug != 'index':
        slugs.add(slug)

mapping = {}
no_cover = []

for slug in sorted(slugs):
    filepath = os.path.join(ARTICLES_DIR, f'{slug}.html')
    if not os.path.exists(filepath):
        no_cover.append(slug)
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    cover = None
    
    # 1. Try hero image in article-hero-image
    hero_match = re.search(r'<div class="article-hero-image">\s*<img src="([^"]+)"', content)
    if hero_match:
        cover = hero_match.group(1)
    
    # 2. Try og:image
    if not cover:
        og_match = re.search(r'<meta property="og:image" content="([^"]+)"', content)
        if og_match:
            cover = og_match.group(1)
    
    # 3. Try any img with articles path
    if not cover:
        img_match = re.search(r'src="(/static/images/articles/[^"]+)"', content)
        if img_match:
            cover = img_match.group(1)
    
    # 4. Try twitter:image
    if not cover:
        tw_match = re.search(r'<meta name="twitter:image" content="([^"]+)"', content)
        if tw_match:
            cover = tw_match.group(1)
    
    if cover:
        # Normalize to relative path
        if cover.startswith('https://fun1399.com'):
            cover = cover.replace('https://fun1399.com', '')
        mapping[slug] = cover
    else:
        no_cover.append(slug)

print(f'Total articles in index: {len(slugs)}')
print(f'With cover: {len(mapping)}')
print(f'No cover: {len(no_cover)}')
print()
print('=== COVER MAPPING ===')
for slug in sorted(mapping.keys()):
    print(f'{slug}|{mapping[slug]}')
print()
if no_cover:
    print('=== NO COVER ===')
    for slug in no_cover:
        print(slug)

# Save to JSON
with open('/tmp/cover_mapping.json', 'w') as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

print(f'\nMapping saved to /tmp/cover_mapping.json')
