#!/usr/bin/env python3
"""Remove responsible-gaming references from index.html and articles/index.html"""
import re

for filepath in ['index.html', 'articles/index.html']:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    
    # Remove links to responsible-gaming
    # Pattern 1: <a href="/responsible-gaming">理性博彩</a>
    content = re.sub(r'\s*<a href="/responsible-gaming"[^>]*>[^<]*</a>\s*', '', content)
    
    # Pattern 2: article cards with responsible-gaming link
    # <a href="/responsible-gaming" class="article-card ...">...</a>
    # Remove the entire card
    content = re.sub(
        r'<a href="/responsible-gaming" class="article-card[^"]*"[^>]*>.*?</a>\s*',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {filepath}: removed responsible-gaming references')
    else:
        print(f'  ℹ️ {filepath}: no changes needed')

print('Done!')
