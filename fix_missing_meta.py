#!/usr/bin/env python3
"""
Fix 21 articles - add missing og:image, twitter:image, and fix hero image paths.
"""
import os, re

SLUGS = [
    'deposit-guide', 'sports-betting-guide', 'casino-registration-guide',
    'sports-betting-tips', 'mlb-betting', 'soccer-betting', 'nba-betting',
    'world-cup-betting-guide', 'world-cup-live-betting', 'world-cup-betting-tips',
    'free-credit-guide', 'cashback-guide', 'casino-free-trial-bonus',
    'wagering-guide', 'rtp-compare', 'casino-customer-service',
    'casino-deposit-methods', 'lottery-casino-guide', 'fish-game-guide', 
    'live-casino-guide', 'baccarat-strategy'
]

for slug in SLUGS:
    path = f'articles/{slug}.html'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Determine image path
    img_ext = None
    for ext in ['.jpg', '.png', '.webp']:
        if os.path.exists(f'static/images/articles/articles/{slug}-cover{ext}'):
            img_ext = ext
            break
    
    if not img_ext:
        print(f'  ❌ {slug}: No cover image')
        continue
    
    img_path = f'/static/images/articles/articles/{slug}-cover{img_ext}'
    abs_url = f'https://fun1399.com{img_path}'
    
    # Get title and description
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else slug
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    desc = desc_match.group(1) if desc_match else ''
    
    # 1. Fix hero image path if it's still pointing to old path
    content = re.sub(
        r'<img src="/static/images/articles/tech/' + re.escape(slug) + r'-cover\.webp"',
        f'<img src="{img_path}"',
        content
    )
    
    # 2. Check if og tags exist
    has_og = '<meta property="og:' in content
    has_twitter = '<meta name="twitter:' in content
    
    if not has_og:
        # Insert OG tags after canonical link
        og_tags = f'''    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://fun1399.com/articles/{slug}">
    <meta property="og:image" content="{abs_url}">
    <meta property="og:site_name" content="娛樂城玩家俱樂部">
'''
        content = re.sub(
            r'(</head>)',
            og_tags + r'\1',
            content
        )
        print(f'  ✅ {slug}: Added OG tags')
    else:
        # Update existing og:image
        content = re.sub(
            r'<meta property="og:image" content="[^"]+">',
            f'<meta property="og:image" content="{abs_url}">',
            content
        )
    
    if not has_twitter:
        # Insert Twitter tags after OG tags or before </head>
        twitter_tags = f'''    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{abs_url}">
'''
        content = re.sub(
            r'(</head>)',
            twitter_tags + r'\1',
            content
        )
        print(f'  ✅ {slug}: Added Twitter tags')
    else:
        # Update existing twitter:image
        content = re.sub(
            r'<meta name="twitter:image" content="[^"]+">',
            f'<meta name="twitter:image" content="{abs_url}">',
            content
        )
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print('Done!')
