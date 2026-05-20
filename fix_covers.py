import os, re, glob, json
from datetime import datetime

# 18 篇需要修復的文章與對應圖片路徑
articles_to_fix = {
    'casino-withdrawal-tutorial': {
        'img': '/static/images/articles/articles/casino-withdrawal-tutorial-cover.jpg',
        'alt_suffix': '娛樂城提款教學封面',
    },
    'mobile-casino-guide': {
        'img': '/static/images/articles/articles/mobile-casino-guide-cover.jpg',
        'alt_suffix': '手機娛樂城攻略封面',
    },
    'casino-ptt-discussion': {
        'img': '/static/images/articles/articles/casino-ptt-discussion-cover.jpg',
        'alt_suffix': '娛樂城PTT討論整理封面',
    },
    'casino-scam-methods': {
        'img': '/static/images/articles/articles/casino-scam-methods-cover.jpg',
        'alt_suffix': '娛樂城詐騙手法封面',
    },
    'casino-withdrawal-fast': {
        'img': '/static/images/articles/articles/casino-withdrawal-fast-cover.jpg',
        'alt_suffix': '娛樂城出金速度攻略封面',
    },
    'hg-casino-promotions-may-2026': {
        'img': '/static/images/articles/articles/hg-casino-promotions-may-2026-cover.jpg',
        'alt_suffix': 'HG娛樂城優惠封面',
    },
    'poker-casino-guide': {
        'img': '/static/images/articles/articles/poker-casino-guide-cover.jpg',
        'alt_suffix': '棋牌遊戲攻略封面',
    },
    'safety-guide': {
        'img': '/static/images/articles/articles/safety-guide-cover.jpg',
        'alt_suffix': '娛樂城安全指南封面',
    },
    'withdrawal-risks': {
        'img': '/static/images/articles/articles/withdrawal-risks-cover.jpg',
        'alt_suffix': '娛樂城提款風險封面',
    },
    'casino-app-download': {
        'img': '/static/images/articles/articles/casino-app-download-cover.jpg',
        'alt_suffix': '娛樂城APP下載教學封面',
    },
    'casino-bonus-guide': {
        'img': '/static/images/articles/articles/casino-bonus-guide-cover.jpg',
        'alt_suffix': '娛樂城優惠攻略封面',
    },
    'casino-safe': {
        'img': '/static/images/articles/articles/casino-safe-cover.jpg',
        'alt_suffix': '娛樂城安全指南封面',
    },
    'casino-safety-check': {
        'img': '/static/images/articles/articles/casino-safety-check-cover.jpg',
        'alt_suffix': '娛樂城安全檢查封面',
    },
    'high-cashback-casino': {
        'img': '/static/images/articles/articles/high-cashback-casino-cover.jpg',
        'alt_suffix': '高返水娛樂城推薦封面',
    },
    'baccarat-guide': {
        'img': '/static/images/articles/articles/baccarat-guide-cover.jpg',
        'alt_suffix': '百家樂技巧攻略封面',
    },
    'how-to-check-casino-scam-record': {
        'img': '/static/images/articles/articles/how-to-check-casino-scam-record-cover.jpg',
        'alt_suffix': '查詢娛樂城詐騙紀錄封面',
    },
    '2026-casino-recommendation': {
        'img': '/static/images/articles/articles/2026-casino-recommendation-cover.jpg',
        'alt_suffix': '2026娛樂城推薦封面',
    },
    'withdrawal-ranking': {
        'img': '/static/images/articles/articles/withdrawal-ranking-cover.jpg',
        'alt_suffix': '娛樂城出金速度排行封面',
    },
}

today = datetime.now().strftime('%Y-%m-%d')
today_iso = datetime.now().strftime('%Y-%m-%dT00:00:00+08:00')

success = []
failure = []

for slug, info in articles_to_fix.items():
    path = f'articles/{slug}.html'
    if not os.path.exists(path):
        failure.append((slug, 'HTML not found'))
        continue
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Extract title from HTML
    title_match = re.search(r'<title>([^\u003c]+)</title>', content)
    title = title_match.group(1).strip() if title_match else slug
    
    img_url = info['img']
    img_full_url = f'https://fun1399.com{img_url}'
    alt = f'{title} - {info["alt_suffix"]}'
    
    modified = False
    
    # 1. Fix og:image
    og_pattern = r'(<meta property="og:image" content=")([^"]+)("\u003e)'
    if re.search(og_pattern, content):
        content = re.sub(og_pattern, f'\g<1>{img_url}\g<3>', content)
    else:
        # Insert after og:description or og:title
        if '<meta property="og:description"' in content:
            content = re.sub(r'(<meta property="og:description" content="[^"]+"\u003e)', 
                           f'\g<1>\n    \u003cmeta property="og:image" content="{img_url}"\u003e', content)
        elif '<meta property="og:title"' in content:
            content = re.sub(r'(<meta property="og:title" content="[^"]+"\u003e)', 
                           f'\g<1>\n    \u003cmeta property="og:image" content="{img_url}"\u003e', content)
        else:
            content = re.sub(r'(<meta name="author" content="[^"]+"\u003e)', 
                           f'\g<1>\n    \u003cmeta property="og:image" content="{img_url}"\u003e', content)
    modified = True
    
    # 2. Fix twitter:image
    tw_pattern = r'(<meta name="twitter:image" content=")([^"]+)("\u003e)'
    if re.search(tw_pattern, content):
        content = re.sub(tw_pattern, f'\g<1>{img_url}\g<3>', content)
    else:
        if '<meta name="twitter:card"' in content:
            content = re.sub(r'(<meta name="twitter:card" content="[^"]+"\u003e)', 
                           f'\g<1>\n    \u003cmeta name="twitter:image" content="{img_url}"\u003e', content)
        else:
            content = re.sub(r'(<meta property="og:image" content="[^"]+"\u003e)', 
                           f'\g<1>\n    \u003cmeta name="twitter:card" content="summary_large_image"\u003e\n    \u003cmeta name="twitter:image" content="{img_url}"\u003e', content)
    modified = True
    
    # 3. Fix schema image
    # Try to find and replace existing image in JSON-LD
    schema_img_pattern = r'"image":\s*"([^"]+)"'
    schema_matches = list(re.finditer(schema_img_pattern, content))
    if schema_matches:
        # Replace all occurrences in schema
        for m in reversed(schema_matches):
            # Check if this is inside a script type="application/ld+json"
            start = max(0, m.start() - 500)
            snippet = content[start:m.start()]
            if 'ld+json' in snippet or '@context' in snippet:
                content = content[:m.start()] + f'"image": "{img_full_url}"' + content[m.end():]
    else:
        # Try to add image to existing schema
        schema_end = content.find('"author":')
        if schema_end > 0:
            content = content[:schema_end] + f'"image": "{img_full_url}",\n        ' + content[schema_end:]
    modified = True
    
    # 4. Inject article-cover div if missing
    has_cover = 'class="article-cover"' in content or 'article-hero-image' in content
    
    if not has_cover:
        # Find the header or article-content start to insert
        # Look for <header> or article start
        header_match = re.search(r'(<header[^\u003e]*\u003e)', content, re.IGNORECASE)
        if header_match:
            pos = header_match.end()
            cover_html = f'''
            \u003c!-- 封面圖 --\u003e
            \u003cdiv class="article-cover" style="margin-bottom: 30px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"\u003e
                \u003cimg src="{img_url}" alt="{alt}" style="width: 100%; height: auto; display: block;"\u003e
            \u003c/div\u003e
'''
            content = content[:pos] + cover_html + content[pos:]
            modified = True
        else:
            # Try to find article content start
            article_match = re.search(r'(<article class="article-content[^\u003e]*\u003e)', content, re.IGNORECASE)
            if article_match:
                pos = article_match.end()
                cover_html = f'''
        \u003cheader style="margin-bottom: 40px;"\u003e
            \u003c!-- 封面圖 --\u003e
            \u003cdiv class="article-cover" style="margin-bottom: 30px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);"\u003e
                \u003cimg src="{img_url}" alt="{alt}" style="width: 100%; height: auto; display: block;"\u003e
            \u003c/div\u003e
        \u003c/header\u003e
'''
                content = content[:pos] + cover_html + content[pos:]
                modified = True
    else:
        # Update existing cover image src
        cover_match = re.search(r'(<div class="article-cover"[^\u003e]*\u003e.*?\u003cimg[^\u003e]+src=")([^"]+)("[^\u003e]*\u003e)', content, re.DOTALL)
        if cover_match:
            content = content[:cover_match.start(2)] + img_url + content[cover_match.end(2):]
            modified = True
        
        # Also update article-hero-image if exists
        hero_match = re.search(r'(<div class="article-hero-image"\u003e.*?\u003cimg[^\u003e]+src=")([^"]+)("[^\u003e]*\u003e)', content, re.DOTALL)
        if hero_match:
            content = content[:hero_match.start(2)] + img_url + content[hero_match.end(2):]
            modified = True
    
    # 5. Update modified date in schema
    date_mod_pattern = r'"dateModified":\s*"[^"]+"'
    if re.search(date_mod_pattern, content):
        content = re.sub(date_mod_pattern, f'"dateModified": "{today_iso}"', content)
    
    # Update article:modified_time
    art_mod_pattern = r'<meta property="article:modified_time" content="[^"]+"\u003e'
    if re.search(art_mod_pattern, content):
        content = re.sub(art_mod_pattern, f'\u003cmeta property="article:modified_time" content="{today_iso}"\u003e', content)
    
    # 6. Update meta update tag
    update_pattern = r'<meta name="update" content="[^"]+"\u003e'
    if re.search(update_pattern, content):
        content = re.sub(update_pattern, f'\u003cmeta name="update" content="{today}"\u003e', content)
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        success.append(slug)
    else:
        failure.append((slug, 'No modifications made'))

print(f'成功修復: {len(success)} 篇')
print(f'失敗: {len(failure)} 篇')
if failure:
    for s, reason in failure:
        print(f'  ❌ {s}: {reason}')
if success:
    for s in success:
        print(f'  ✅ {s}')
