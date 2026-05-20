#!/usr/bin/env python3
"""Fix casino-no-withdrawal-scam preview image paths in index.html and articles/index.html"""
import re

# Map of old paths to new paths for casino-no-withdrawal-scam
old_to_new = {
    '/static/images/articles/tech/casino-no-withdrawal-scam-cover.webp': '/static/images/articles/articles/casino-no-withdrawal-scam-cover.jpg',
    '/static/images/articles/scam/casino-no-withdrawal-scam-cover.webp': '/static/images/articles/articles/casino-no-withdrawal-scam-cover.jpg',
}

for filepath in ['index.html', 'articles/index.html']:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modified = False
    for old, new in old_to_new.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f'  ✅ {filepath}: {old} -> {new}')
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done!')
