#!/usr/bin/env python3
"""Update preview images in index.html and articles/index.html"""
import re, os

SLUGS = [
    'deposit-guide', 'sports-betting-guide', 'casino-registration-guide',
    'sports-betting-tips', 'mlb-betting', 'soccer-betting', 'nba-betting',
    'world-cup-betting-guide', 'world-cup-live-betting', 'world-cup-betting-tips',
    'free-credit-guide', 'cashback-guide', 'casino-free-trial-bonus',
    'wagering-guide', 'rtp-compare', 'casino-customer-service',
    'casino-deposit-methods', 'lottery-casino-guide', 'fish-game-guide', 
    'live-casino-guide', 'baccarat-strategy'
]

# Build mapping of possible old paths to new paths
for filepath in ['index.html', 'articles/index.html']:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    modified = False
    
    for slug in SLUGS:
        # Check if this slug exists in the file
        if f'href="/articles/{slug}"' not in content and f'href="/{slug}"' not in content:
            continue
        
        # Determine extension
        ext = None
        for e in ['.jpg', '.png', '.webp']:
            if os.path.exists(f'static/images/articles/articles/{slug}-cover{e}'):
                ext = e
                break
        
        if not ext:
            continue
        
        new_path = f'/static/images/articles/articles/{slug}-cover{ext}'
        
        # Find all img src references near this slug
        pattern = re.compile(
            r'(href="(?:/articles/)?' + re.escape(slug) + r'"[^>]*>.*?<img[^>]+src=")([^"]+)("[^>]*>)',
            re.DOTALL
        )
        
        def replace_img(match):
            return match.group(1) + new_path + match.group(3)
        
        new_content = pattern.sub(replace_img, content)
        
        if new_content != content:
            content = new_content
            modified = True
            print(f'  ✅ {filepath}: updated {slug} preview to {new_path}')
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

print('Done!')
