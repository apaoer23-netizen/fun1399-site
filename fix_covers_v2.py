#!/usr/bin/env python3
"""
Batch fix 18 articles that have cover images but missing HTML references.
"""
import os, re
from datetime import datetime

ARTICLES_TO_FIX = {
    'casino-withdrawal-tutorial': {
        'img': '/static/images/articles/articles/casino-withdrawal-tutorial-cover.jpg',
        'alt': '娛樂城提款教學｜出金流程與注意事項完整攻略',
    },
    'mobile-casino-guide': {
        'img': '/static/images/articles/articles/mobile-casino-guide-cover.jpg',
        'alt': '手機娛樂城攻略：隨時隨地暢玩最佳平台推薦',
    },
    'casino-ptt-discussion': {
        'img': '/static/images/articles/articles/casino-ptt-discussion-cover.jpg',
        'alt': '娛樂城PTT討論整理：網友真實經驗與熱門話題',
    },
    'casino-scam-methods': {
        'img': '/static/images/articles/articles/casino-scam-methods-cover.jpg',
        'alt': '娛樂城詐騙手法全解析：如何識別與防範',
    },
    'casino-withdrawal-fast': {
        'img': '/static/images/articles/articles/casino-withdrawal-fast-cover.jpg',
        'alt': '娛樂城快速出金攻略：縮短等待時間的秘訣',
    },
    'hg-casino-promotions-may-2026': {
        'img': '/static/images/articles/articles/hg-casino-promotions-may-2026-cover.jpg',
        'alt': 'HG娛樂城2026年5月優惠活動總整理',
    },
    'poker-casino-guide': {
        'img': '/static/images/articles/articles/poker-casino-guide-cover.jpg',
        'alt': '棋牌遊戲攻略：撲克、德州撲克技巧教學',
    },
    'safety-guide': {
        'img': '/static/images/articles/articles/safety-guide-cover.jpg',
        'alt': '娛樂城安全指南：選擇合法平台的完整攻略',
    },
    'withdrawal-risks': {
        'img': '/static/images/articles/articles/withdrawal-risks-cover.jpg',
        'alt': '娛樂城提款風險：常見問題與應對策略',
    },
    'casino-app-download': {
        'img': '/static/images/articles/articles/casino-app-download-cover.jpg',
        'alt': '娛樂城APP下載教學：iOS與Android安裝指南',
    },
    'casino-bonus-guide': {
        'img': '/static/images/articles/articles/casino-bonus-guide-cover.jpg',
        'alt': '娛樂城優惠攻略：如何最大化領取獎金',
    },
    'casino-safe': {
        'img': '/static/images/articles/articles/casino-safe-cover.jpg',
        'alt': '娛樂城安全玩法：保護資金的必備知識',
    },
    'casino-safety-check': {
        'img': '/static/images/articles/articles/casino-safety-check-cover.jpg',
        'alt': '娛樂城安全檢查清單：註冊前必看',
    },
    'high-cashback-casino': {
        'img': '/static/images/articles/articles/high-cashback-casino-cover.jpg',
        'alt': '高返水娛樂城推薦：最大化你的返利收益',
    },
    'baccarat-guide': {
        'img': '/static/images/articles/articles/baccarat-guide-cover.jpg',
        'alt': '百家樂技巧攻略：從入門到高手完整教學',
    },
    'how-to-check-casino-scam-record': {
        'img': '/static/images/articles/articles/how-to-check-casino-scam-record-cover.jpg',
        'alt': '如何查詢娛樂城詐騙紀錄：黑網辨識教學',
    },
    '2026-casino-recommendation': {
        'img': '/static/images/articles/articles/2026-casino-recommendation-cover.jpg',
        'alt': '2026娛樂城推薦：台灣最佳線上娛樂城評測',
    },
    'withdrawal-ranking': {
        'img': '/static/images/articles/articles/withdrawal-ranking-cover.jpg',
        'alt': '娛樂城出金速度排行：快速提款平台推薦',
    },
}

def fix_article(slug, info):
    path = f'articles/{slug}.html'
    if not os.path.exists(path):
        return False, 'HTML file not found'
    
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    img_url = info['img']
    img_full = f'https://fun1399.com{img_url}'
    alt_text = info['alt']
    
    title_match = re.search(r'<title>([^<]+)</title>', content)
    title = title_match.group(1).strip() if title_match else alt_text
    
    canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', content)
    canonical = canonical_match.group(1) if canonical_match else f'https://fun1399.com/articles/{slug}'
    
    desc_match = re.search(r'<meta name="description" content="([^"]+)">', content)
    description = desc_match.group(1) if desc_match else title
    
    modified = False
    
    # 1. Add og:image and twitter:image if missing
    if not re.search(r'<meta property="og:image"', content, re.IGNORECASE):
        og_block = f'''    <meta property="og:type" content="article">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{img_url}">
    <meta property="og:locale" content="zh_TW">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{img_url}">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
'''
        content = content.replace('</head>', og_block + '</head>')
        modified = True
    else:
        # Update existing
        content = re.sub(
            r'<meta property="og:image" content="[^"]+">',
            f'<meta property="og:image" content="{img_url}">',
            content
        )
        if re.search(r'<meta name="twitter:image"', content, re.IGNORECASE):
            content = re.sub(
                r'<meta name="twitter:image" content="[^"]+">',
                f'<meta name="twitter:image" content="{img_url}">',
                content
            )
        modified = True
    
    # 2. Add/update JSON-LD schema
    today = datetime.now().strftime('%Y-%m-%d')
    today_iso = f'{today}T00:00:00+08:00'
    
    if '<script type="application/ld+json">' in content:
        if re.search(r'"image":\s*"', content):
            content = re.sub(
                r'"image":\s*"[^"]+",?',
                f'"image": "{img_full}",',
                content
            )
        else:
            content = re.sub(
                r'("headline":\s*"[^"]+",)',
                r'\1\n        "image": "' + img_full + '",',
                content
            )
        modified = True
    else:
        schema = f'''<script type="application/ld+json">
{{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{title}",
    "description": "{description}",
    "image": "{img_full}",
    "author": {{
        "@type": "Person",
        "name": "Kevin Lin",
        "url": "https://fun1399.com/author.html"
    }},
    "publisher": {{
        "@type": "Organization",
        "name": "娛樂城玩家俱樂部",
        "logo": {{
            "@type": "ImageObject",
            "url": "https://fun1399.com/favicon.svg"
        }}
    }},
    "datePublished": "{today_iso}",
    "dateModified": "{today_iso}",
    "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{canonical}"
    }}
}}
</script>
'''
        content = content.replace('</head>', schema + '</head>')
        modified = True
    
    # 3. Add article-cover div if missing
    if 'class="article-cover"' not in content:
        cover_div = f'''<div class="article-cover" style="margin: 20px 0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <img src="{img_url}" alt="{alt_text}" style="width: 100%; height: auto; display: block;">
            </div>
'''
        
        if '<div class="article-hero-image">' in content:
            content = re.sub(
                r'(<div class="article-hero-image">.*?</div>\s*)',
                r'\1\n            ' + cover_div,
                content,
                flags=re.DOTALL,
                count=1
            )
        else:
            h1_match = re.search(r'(<h1[^>]*>.*?</h1>\s*)', content, re.DOTALL)
            if h1_match:
                pos = h1_match.end()
                content = content[:pos] + '\n            ' + cover_div + content[pos:]
            else:
                bc_match = re.search(r'(</nav>\s*<h1>)', content, re.DOTALL)
                if bc_match:
                    pos = bc_match.start() + len('</nav>')
                    content = content[:pos] + '\n            ' + cover_div + content[pos:]
        modified = True
    else:
        content = re.sub(
            r'(<div class="article-cover"[^>]*>.*?<img[^>]+src=")([^"]+)("[^>]*>)',
            r'\g<1>' + img_url + r'\g<3>',
            content,
            flags=re.DOTALL,
            count=1
        )
        modified = True
    
    # 4. Update modified time
    if re.search(r'<meta property="article:modified_time"', content):
        content = re.sub(
            r'<meta property="article:modified_time" content="[^"]+">',
            f'<meta property="article:modified_time" content="{today_iso}">',
            content
        )
    
    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return True, 'Fixed'

if __name__ == '__main__':
    success = []
    failure = []
    
    for slug, info in ARTICLES_TO_FIX.items():
        ok, msg = fix_article(slug, info)
        if ok:
            success.append(slug)
        else:
            failure.append((slug, msg))
    
    print(f'成功修復: {len(success)} 篇')
    print(f'失敗: {len(failure)} 篇')
    for s in success:
        print(f'  ✅ {s}')
    for s, m in failure:
        print(f'  ❌ {s}: {m}')
