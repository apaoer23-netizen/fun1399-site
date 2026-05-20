#!/usr/bin/env python3
"""
強制統一所有文章模板
完全重建不符合標準的文章
"""

import re
from pathlib import Path

def get_template_structure():
    """獲取標準模板的各個部分"""
    template_path = Path('/root/.openclaw/workspace/fun1399-site/build/articles/world-cup-2026-guide.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 提取標準頭部（從DOCTYPE到<body>）
    head_match = re.search(r'(<!DOCTYPE html>.*?)<article', template, re.DOTALL)
    head = head_match.group(1) if head_match else ''
    
    # 提取標準尾部（從</article>到</html>）
    foot_match = re.search(r'</article>(.*?)</html>', template, re.DOTALL)
    foot = foot_match.group(1) + '</html>' if foot_match else ''
    
    return head, foot

def rebuild_article(filepath, head_template, foot_template):
    """重建文章以符合標準模板"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取文章的關鍵內容
    # 1. 標題
    title_match = re.search(r'<title>(.*?)\s*-\s*娛樂城玩家俱樂部</title>', content)
    title = title_match.group(1) if title_match else filepath.stem
    
    # 2. description
    desc_match = re.search(r'name="description" content="([^"]*)"', content)
    description = desc_match.group(1) if desc_match else title
    
    # 3. H1標題
    h1_match = re.search(r'<h1[^\u003e]*>(.*?)</h1>', content, re.DOTALL)
    h1 = h1_match.group(1) if h1_match else title
    h1_clean = re.sub(r'<[^\u003e]+>', '', h1).strip()
    
    # 4. 作者資訊
    author_match = re.search(r'class="article-meta"[^\u003e]*>(.*?)</div>', content, re.DOTALL)
    author_section = author_match.group(1) if author_match else ''
    
    # 提取作者名
    author_name_match = re.search(r'作者：<a href="/author.html#([^"]+)">([^\u003c]+)</a>', author_section)
    author_id = author_name_match.group(1) if author_name_match else 'kevin'
    author_name = author_name_match.group(2) if author_name_match else 'Kevin Lin'
    
    # 5. 文章內容（從intro到最後一個section）
    content_match = re.search(r'(<div class="intro".*?)\s*(?:<div class="cta-box"|<div class="final-cta"|</div>\s*</article>)', content, re.DOTALL)
    body_content = content_match.group(1) if content_match else ''
    
    # 如果沒有intro，嘗試提取所有section內容
    if not body_content:
        sections = re.findall(r'(<section[^\u003e]*>.*?</section>|<h2[^\u003e]*>.*?(?=<h2|</article>|$))', content, re.DOTALL)
        if sections:
            body_content = '\n'.join(sections)
    
    # 清理內容
    body_content = re.sub(r'<aside[^\u003e]*>.*?</aside>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<div class="sidebar[^"]*"[^\u003e]*>.*?</div>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<div class="cta-box bottom-cta"[^\u003e]*>.*?</div>', '', body_content, flags=re.DOTALL)
    body_content = re.sub(r'<div class="related-articles"[^\u003e]*>.*?</div>', '', body_content, flags=re.DOTALL)
    
    # 生成新的標準文章
    new_article = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{h1_clean} - 娛樂城玩家俱樂部</title>
    <meta name="description" content="{description}">
    <link rel="stylesheet" href="/static/css/style.css">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-1V53J5D71S"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-1V53J5D71S');
    </script>

</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo"><a href="/">娛樂城玩家俱樂部</a></div>
            <nav class="nav">
                <a href="/">首頁</a>
                <a href="/articles/">攻略文章</a>
                <a href="/reviews/">平台評測</a>
                <a href="https://fun1399.ofa177.net/" class="play-btn" target="_blank" rel="noopener">立即遊玩</a>
                <a href="https://lin.ee/Mc1pb7z" class="line-btn" target="_blank">加入LINE</a>
            </nav>
        </div>
    </header>

    <article class="content">
        <div class="container">
            <nav class="breadcrumb">
                <a href="/">首頁</a> &gt; 
                <a href="/articles/">攻略文章</a> &gt; 
                <span>{h1_clean}</span>
            </nav>

            <h1>{h1_clean}</h1>

            <div class="article-meta">
                <div class="author-info">
                    <span>👤 作者：<a href="/author.html#{author_id}">{author_name}</a></span>
                    <span>📅 發布日期：2026年3月15日</span>
                    <span>🔄 最後更新：2026年3月15日</span>
                </div>
            </div>

{body_content}

        </div>
    </article>

    <footer class="footer">
        <div class="container">
            <p>© 2026 娛樂城玩家俱樂部</p>
        </div>
    </footer>
</body>
</html>'''
    
    return new_article

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    # 需要重建的文章列表
    problem_files = [
        'cashback-guide.html',
        'free-credit-guide.html',
        'high-cashback-casino.html',
        'casino-scam-methods.html',
        'withdrawal-risks.html',
        'casino-ptt-discussion.html',
        'casino-app-download.html',
        'casino-scam-alert.html',
        'live-casino-guide.html',
        'casino-safe.html',
        'soccer-betting.html',
        'casino-safety-check.html',
        'lottery-casino-guide.html',
        'casino-review-real.html',
        'casino-deposit-methods.html',
        'sports-betting-guide.html',
        'mobile-casino-guide.html',
        'sports-betting-tips.html',
        'casino-withdrawal-fast.html',
        'poker-casino-guide.html',
        'fish-game-guide.html',
        'casino-dcard-2026.html',
        'casino-free-credit.html',
        'casino-bonus-guide.html',
        'casino-withdrawal-tutorial.html',
        'mlb-betting.html',
        'nba-betting.html',
    ]
    
    print("🔧 強制重建不符合標準的文章")
    print("=" * 60)
    print()
    
    fixed = 0
    for filename in problem_files:
        filepath = articles_dir / filename
        if filepath.exists():
            try:
                new_content = rebuild_article(filepath, '', '')
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  ✅ {filename} - 已重建為標準模板")
                fixed += 1
            except Exception as e:
                print(f"  ❌ {filename} - 重建失敗: {e}")
    
    print()
    print("=" * 60)
    print(f"📊 已重建 {fixed} 篇文章")
    print("=" * 60)

if __name__ == '__main__':
    main()
