#!/usr/bin/env python3
"""
Final pass: Ensure all cards have proper img tags and no gradient backgrounds
"""
import re
import json

with open('/tmp/cover_mapping.json', 'r') as f:
    mapping = json.load(f)

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    html = f.read()

# Step 1: For all cards with img but still have background gradient, remove the background
# Match card-image divs that contain <img> but have style="background: ..."
pattern1 = r'(<div class="card-image") style="background: linear-gradient\([^"]+\)"([^>]*>\s*<img[^>]+>\s*</div>)'
replacement1 = r'\1\2'
html = re.sub(pattern1, replacement1, html, flags=re.DOTALL)

# Step 2: For all cards without img, add one
card_pattern = r'(<a href="/articles/([^"]+)" class="article-card[^"]*">)(.*?)(</a>)'

def add_img_if_missing(match):
    prefix = match.group(1)
    slug = match.group(2)
    inner = match.group(3)
    suffix = match.group(4)
    
    if slug == 'index':
        return match.group(0)
    
    # Check if already has img
    if re.search(r'<div class="card-image"[^>]*>\s*<img', inner):
        return match.group(0)
    
    # Get cover
    cover = mapping.get(slug)
    if not cover:
        return match.group(0)
    
    title_match = re.search(r'<h3 class="card-title">([^<]+)</h3>', inner)
    title = title_match.group(1).strip() if title_match else slug
    
    # Replace card-image div with img version
    new_inner = re.sub(
        r'<div class="card-image"[^>]*>.*?</div>',
        f'<div class="card-image"><img src="{cover}" alt="{title}" loading="lazy"></div>',
        inner,
        count=1,
        flags=re.DOTALL
    )
    return prefix + new_inner + suffix

html = re.sub(card_pattern, add_img_if_missing, html, flags=re.DOTALL)

# Verify
gradient_count = html.count('background: linear-gradient')
img_cards = len(re.findall(r'<div class="card-image"[^>]*>\s*<img', html))
total_cards = len(re.findall(r'<a href="/articles/[^"]+" class="article-card', html))

print(f'Remaining gradient backgrounds: {gradient_count}')
print(f'Cards with img tags: {img_cards}')
print(f'Total cards: {total_cards}')

# Find remaining gradient slugs
remaining = []
for match in re.finditer(r'<a href="/articles/([^"]+)" class="article-card[^"]*">', html):
    slug = match.group(1)
    start = match.start()
    end = html.find('</a>', start)
    card_html = html[start:end+4]
    if 'background: linear-gradient' in card_html:
        remaining.append(slug)

if remaining:
    print(f'\nRemaining gradient slugs: {sorted(set(remaining))}')

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(html)

print(f'\nSaved. Size: {len(html)} bytes')
