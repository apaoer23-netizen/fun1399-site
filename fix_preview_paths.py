#!/usr/bin/env python3
"""Fix preview image paths in index.html and articles/index.html"""
import re

# Map of old paths to new paths
old_to_new = {
    '/static/images/articles/tech/2026-casino-recommendation-cover.webp': '/static/images/articles/articles/2026-casino-recommendation-cover.jpg',
    '/static/images/articles/tech/baccarat-guide-cover.webp': '/static/images/articles/articles/baccarat-guide-cover.jpg',
    '/static/images/articles/tech/casino-app-download-cover.webp': '/static/images/articles/articles/casino-app-download-cover.jpg',
    '/static/images/articles/tech/casino-bonus-guide-cover.webp': '/static/images/articles/articles/casino-bonus-guide-cover.jpg',
    '/static/images/articles/tech/casino-safety-check-cover.webp': '/static/images/articles/articles/casino-safety-check-cover.jpg',
    '/static/images/articles/tech/high-cashback-casino-cover.webp': '/static/images/articles/articles/high-cashback-casino-cover.jpg',
    '/static/images/articles/tech/safety-guide-cover.webp': '/static/images/articles/articles/safety-guide-cover.jpg',
    '/static/images/articles/tech/withdrawal-ranking-cover.webp': '/static/images/articles/articles/withdrawal-ranking-cover.jpg',
    '/static/images/articles/tech/withdrawal-risks-cover.webp': '/static/images/articles/articles/withdrawal-risks-cover.jpg',
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

print('\nDone!')
