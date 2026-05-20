#!/usr/bin/env python3
"""
Fix all article cards in articles/index.html:
1. Remove background gradient from cards that already have <img>
2. Add <img> to cards that don't have it yet
"""
import re
import json

with open('/tmp/cover_mapping.json', 'r') as f:
    mapping = json.load(f)

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    html = f.read()

# Strategy: Process each article-card anchor individually
card_pattern = r'(<a href="/articles/([^"]+)" class="article-card[^"]*">)(.*?)(</a>)'

def process_card(match):
    prefix = match.group(1)  # <a href="..." class="...">
    slug = match.group(2)
    inner = match.group(3)
    suffix = match.group(4)
    
    if slug == 'index':
        return match.group(0)
    
    # Check if this card already has an <img> inside card-image
    has_img = bool(re.search(r'<div class="card-image"[^>]*>\s*<img', inner))
    
    # Find cover image for this slug
    cover = mapping.get(slug)
    
    if has_img:
        # Case 1: Already has img, just remove the background style from card-image
        new_inner = re.sub(
            r'(<div class="card-image") style="background: linear-gradient\([^"]+\)"([^>]*>)',
            r'\1\2',
            inner
        )
        # Also remove any emoji div inside card-image if img exists
        new_inner = re.sub(
            r'(<img[^/]+/>)\s*<div style="position: absolute; inset: 0;[^"]*"[^/]*>.*?</div>',
            r'\1',
            new_inner,
            flags=re.DOTALL
        )
        return prefix + new_inner + suffix
    
    elif cover:
        # Case 2: No img, has cover - replace card-image content with img
        title_match = re.search(r'<h3 class="card-title">([^<]+)</h3>', inner)
        title = title_match.group(1).strip() if title_match else slug
        
        new_image_html = f'<div class="card-image"><img src="{cover}" alt="{title}" loading="lazy"></div>'
        
        # Replace the entire card-image div
        new_inner = re.sub(
            r'<div class="card-image"[^>]*>.*?</div>',
            new_image_html,
            inner,
            count=1,
            flags=re.DOTALL
        )
        return prefix + new_inner + suffix
    
    else:
        # No cover found, keep as-is
        return match.group(0)

new_html = re.sub(card_pattern, process_card, html, flags=re.DOTALL)

# Count results
original_gradient = html.count('background: linear-gradient')
new_gradient = new_html.count('background: linear-gradient')
img_tags = new_html.count('<div class="card-image"><img')

print(f'Original gradient backgrounds: {original_gradient}')
print(f'Remaining gradient backgrounds: {new_gradient}')
print(f'Cards with img tags: {img_tags}')
print(f'Total cards: {len(re.findall(card_pattern, new_html, re.DOTALL))}')

# Find remaining slugs with gradient
remaining = re.findall(r'<a href="/articles/([^"]+)" class="article-card[^"]*">[^/]*?background: linear-gradient', new_html)
if remaining:
    print(f'\nRemaining with gradient: {sorted(set(remaining))}')

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(new_html)

print(f'\nSaved. Size: {len(new_html)} bytes')
