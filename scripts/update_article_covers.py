#!/usr/bin/env python3
"""
Update articles/index.html cards with real cover images
"""
import re
import json

with open('/tmp/cover_mapping.json', 'r') as f:
    mapping = json.load(f)

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    html = f.read()

# Pattern to match article cards with placeholder card-image
# Match: <div class="card-image" style="background: ...">...</div>
# Within <a href="/articles/{slug}" class="article-card"> ... </a>

# Strategy: Find each article-card anchor, extract slug, replace the card-image div inside it

def replace_card_image(match):
    """Replace card-image placeholder with real img tag"""
    full_card = match.group(0)
    slug_match = re.search(r'href="/articles/([^"]+)"', full_card)
    if not slug_match:
        return full_card
    
    slug = slug_match.group(1)
    if slug == 'index':
        return full_card
    
    # Get title for alt text
    title_match = re.search(r'<h3 class="card-title">([^<]+)</h3>', full_card)
    title = title_match.group(1).strip() if title_match else slug
    
    # Find cover image
    cover = mapping.get(slug)
    if not cover:
        # Keep original placeholder if no cover found
        return full_card
    
    # Replace the old card-image div with new img-based one
    old_pattern = r'<div class="card-image"[^>]*>.*?</div>'
    new_image = f'<div class="card-image"><img src="{cover}" alt="{title}" loading="lazy"></div>'
    
    new_card = re.sub(old_pattern, new_image, full_card, count=1, flags=re.DOTALL)
    return new_card

# Match each article-card anchor block
pattern = r'<a href="/articles/[^"]+" class="article-card">.*?</a>'
new_html = re.sub(pattern, replace_card_image, html, flags=re.DOTALL)

# Count replacements
original_placeholders = html.count('background: linear-gradient')
new_placeholders = new_html.count('background: linear-gradient')
print(f'Original gradient placeholders: {original_placeholders}')
print(f'Remaining gradient placeholders: {new_placeholders}')
print(f'Replaced: {original_placeholders - new_placeholders}')

# Count img tags in cards
img_count = new_html.count('<div class="card-image"><img')
print(f'Cards with img tags: {img_count}')

# Save
with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(new_html)

print(f'\nFile saved. Size: {len(new_html)} bytes')
