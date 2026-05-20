#!/usr/bin/env python3
"""
Batch update 21 articles with new cover images.
"""
import os, re, glob

# Map: slug -> image path and extension
SLUGS = [
    'deposit-guide', 'sports-betting-guide', 'casino-registration-guide',
    'sports-betting-tips', 'mlb-betting', 'soccer-betting', 'nba-betting',
    'world-cup-betting-guide', 'world-cup-live-betting', 'world-cup-betting-tips',
    'free-credit-guide', 'cashback-guide', 'casino-free-trial-bonus',
    'wagering-guide', 'rtp-compare', 'casino-customer-service',
    'casino-deposit-methods', 'lottery-casino-guide', 'fish-game-guide', 
    'live-casino-guide', 'baccarat-strategy'
]

success = []
failed = []

for slug in SLUGS:
    path = f'articles/{slug}.html'
    if not os.path.exists(path):
        failed.append((slug, 'HTML not found'))
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Determine image extension
    img_ext = None
    for ext in ['.jpg', '.png', '.webp']:
        if os.path.exists(f'static/images/articles/articles/{slug}-cover{ext}'):
            img_ext = ext
            break
    
    if not img_ext:
        failed.append((slug, 'No cover image found'))
        continue
    
    img_path = f'/static/images/articles/articles/{slug}-cover{img_ext}'
    abs_url = f'https://fun1399.com{img_path}'
    
    # Get alt text from h1
    h1_match = re.search(r'<h1[^>]*>([^<]+)</h1>', content)
    alt = h1_match.group(1).strip() if h1_match else f'{slug} 封面圖'
    
    # 1. Remove old article-cover div if exists
    content = re.sub(r'\s*<div class="article-cover"[^>]*>.*?</div>\s*', '', content, flags=re.DOTALL)
    
    # 2. Add new article-hero-image div
    hero_div = f'<div class="article-hero-image"><img src="{img_path}" alt="{alt}" loading="eager" style="width:100%;height:auto;display:block;"></div>\n'
    
    # Insert after <article> tag or before <div class="article-content">
    if '<div class="article-hero-image">' not in content:
        # Try to insert after <article> tag
        content = re.sub(
            r'(<article[^>]*>)\s*',
            r'\1\n' + hero_div,
            content,
            count=1
        )
    
    # 3. Update og:image
    if '<meta property="og:image"' in content:
        content = re.sub(
            r'<meta property="og:image" content="[^"]+"',
            f'<meta property="og:image" content="{abs_url}"',
            content
        )
    else:
        # Insert after title or after og:title
        content = re.sub(
            r'(<meta property="og:title"[^>]+>)\s*',
            r'\1\n    <meta property="og:image" content="' + abs_url + '">',
            content
        )
    
    # 4. Update twitter:image
    if '<meta name="twitter:image"' in content:
        content = re.sub(
            r'<meta name="twitter:image" content="[^"]+"',
            f'<meta name="twitter:image" content="{abs_url}"',
            content
        )
    else:
        content = re.sub(
            r'(<meta name="twitter:title"[^>]+>)\s*',
            r'\1\n    <meta name="twitter:image" content="' + abs_url + '">',
            content
        )
    
    # 5. Update schema image
    if '"image":' in content:
        # Check if it's ImageObject format or simple string
        if re.search(r'"image":\s*\{[^}]*"url"', content):
            # ImageObject format - update url
            content = re.sub(
                r'"image":\s*\{[^}]*"url":\s*"[^"]+"',
                f'"image": {{"@type": "ImageObject", "url": "{abs_url}"}}',
                content,
                flags=re.DOTALL
            )
        else:
            # Simple string format
            content = re.sub(
                r'"image":\s*"[^"]+"',
                f'"image": "{abs_url}"',
                content
            )
    else:
        # Insert into schema if image field doesn't exist
        content = re.sub(
            r'("dateModified":\s*"[^"]+")',
            r'\1,\n        "image": "' + abs_url + '"',
            content
        )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    success.append(slug)
    print(f'  ✅ {slug}: updated with {img_path}')

print(f'\n成功: {len(success)} 篇 | 失敗: {len(failed)} 篇')
if failed:
    for slug, reason in failed:
        print(f'  ❌ {slug}: {reason}')
