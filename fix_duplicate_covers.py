#!/usr/bin/env python3
"""Remove duplicate old covers, keep new article-hero-image"""
import re, os

# Fix 3 articles with duplicate covers
SLUGS = ['casino-investment-scam', 'casino-scam-emergency-response', 'casino-romance-scam']

for slug in SLUGS:
    path = f'articles/{slug}.html'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find and remove the old article-cover div (the one with old path, not article-hero-image)
    # Pattern: <div class="article-cover" ...>...</div>  (not article-hero-image)
    # We need to be careful to only remove the one that's NOT inside article-hero-image
    
    # Find all article-cover divs
    pattern = r'\s*<div class="article-cover"[^>]*>.*?<\/div>\s*'
    matches = list(re.finditer(pattern, content, re.DOTALL))
    
    removed = 0
    for m in reversed(matches):
        div_content = m.group(0)
        # Check if this div contains an img pointing to the OLD path
        if 'static/images/articles/articles/' in div_content:
            # This is the NEW one (in articles/articles/), keep it
            continue
        else:
            # This is the OLD one, remove it
            content = content[:m.start()] + content[m.end():]
            removed += 1
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f'  ✅ {slug}: removed {removed} old cover(s)')

print('Done!')
