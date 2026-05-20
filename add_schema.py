#!/usr/bin/env python3
"""Add schema.org JSON-LD to articles that don't have it."""
import re, os

SLUGS_NO_SCHEMA = [
    'sports-betting-tips', 'mlb-betting', 'soccer-betting', 'nba-betting',
    'world-cup-betting-guide', 'world-cup-live-betting', 'world-cup-betting-tips',
    'free-credit-guide', 'rtp-compare', 'casino-deposit-methods',
    'lottery-casino-guide', 'fish-game-guide', 'live-casino-guide'
]

for slug in SLUGS_NO_SCHEMA:
    path = f'articles/{slug}.html'
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Get title and description
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else slug
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)"', content)
    desc = desc_match.group(1) if desc_match else ''
    
    # Determine image path
    img_ext = None
    for ext in ['.jpg', '.png', '.webp']:
        if os.path.exists(f'static/images/articles/articles/{slug}-cover{ext}'):
            img_ext = ext
            break
    
    if not img_ext:
        print(f'  ❌ {slug}: No cover image')
        continue
    
    img_url = f'https://fun1399.com/static/images/articles/articles/{slug}-cover{img_ext}'
    
    # Build schema JSON
    schema = f'''    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "description": "{desc}",
      "author": {{
        "@type": "Person",
        "name": "Kevin Lin",
        "url": "https://fun1399.com/author.html#kevin"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "娛樂城玩家俱樂部"
      }},
      "datePublished": "2026-03-14",
      "dateModified": "2026-05-17T01:00:00+08:00",
      "image": "{img_url}"
    }}
    </script>
'''
    
    # Insert before </head>
    if '<script type="application/ld+json">' not in content:
        content = content.replace('</head>', schema + '</head>')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'  ✅ {slug}: Added schema with image')
    else:
        print(f'  ℹ️ {slug}: Schema already exists')

print('Done!')
