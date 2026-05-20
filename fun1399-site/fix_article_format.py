#!/usr/bin/env python3
"""
批量修復文章格式問題
- 添加標準導航列
- 添加CSS連結
- 添加麵包屑導航
- 添加Sidebar
- 添加底部CTA
"""

import os
import re
from pathlib import Path

# 標準Header導航列
STANDARD_HEADER = '''    <header class="header">
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
    </header>'''

# 標準Sidebar
STANDARD_SIDEBAR = '''            <aside class="sidebar">
                <div class="sidebar-widget">
                    <h4>🔥 推薦娛樂城</h4>
                    <ul class="sidebar-list">
                        <li>
                            <a href="/reviews/jucity.html" class="sidebar-link">
                                <span class="sidebar-rank">#1</span>
                                <span>鉅城娛樂城</span>
                                <span class="sidebar-rating">★4.9</span>
                            </a>
                        </li>
                        <li>
                            <a href="/reviews/mbm.html" class="sidebar-link">
                                <span class="sidebar-rank">#2</span>
                                <span>MBM娛樂城</span>
                                <span class="sidebar-rating">★4.7</span>
                            </a>
                        </li>
                        <li>
                            <a href="/reviews/utown.html" class="sidebar-link">
                                <span class="sidebar-rank">#3</span>
                                <span>優塔娛樂城</span>
                                <span class="sidebar-rating">★4.6</span>
                            </a>
                        </li>
                    </ul>
                </div>

                <div class="sidebar-widget">
                    <h4>📚 熱門攻略</h4>
                    <ul class="sidebar-list">
                        <li><a href="/articles/baccarat-guide.html">百家樂技巧攻略</a></li>
                        <li><a href="/articles/slots-guide.html">老虎機RTP攻略</a></li>
                        <li><a href="/articles/sports-betting-guide.html">體育投注教學</a></li>
                    </ul>
                </div>

                <div class="sidebar-widget sidebar-cta">
                    <h4>💬 加入 LINE@</h4>
                    <p>獲取最新優惠情報與專業攻略</p>
                    <a href="https://lin.ee/Mc1pb7z" class="btn btn-line" target="_blank">加入好友</a>
                </div>
            </aside>'''

# 底部CTA
BOTTOM_CTA = '''        <div class="cta-box bottom-cta">
            <h3>🚀 準備開始你的娛樂城之旅？</h3>
            <p>立即加入我們推薦的平台，領取專屬優惠！</p>
            <div class="cta-buttons">
                <a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="btn btn-primary btn-large">🎮 立即遊玩</a>
                <a href="https://lin.ee/Mc1pb7z" target="_blank" class="btn btn-line btn-large">💬 加入LINE@獲取優惠</a>
            </div>
        </div>'''

# 相關文章
RELATED_ARTICLES = '''        <div class="related-articles">
            <h3>📚 相關文章推薦</h3>
            <ul class="related-list">
                <li>👉 <a href="/articles/baccarat-guide.html">百家樂技巧完整攻略</a></li>
                <li>👉 <a href="/articles/slots-guide.html">老虎機RTP攻略</a></li>
                <li>👉 <a href="/articles/safety-guide.html">娛樂城安全指南</a></li>
                <li>👉 <a href="/recommend/2026.html">2026最新娛樂城推薦</a></li>
            </ul>
        </div>'''

# Footer
FOOTER = '''    <footer class="footer">
        <div class="container">
            <p>© 2026 娛樂城玩家俱樂部</p>
        </div>
    </footer>'''

def fix_article_format(filepath):
    """修復文章格式"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    filename = filepath.name
    fixed_items = []
    
    # 檢查是否有標準header
    if 'class="header"' not in content:
        # 檢查是否有任何header標籤
        if '<header>' in content and '<header class="header">' not in content:
            # 替換簡單header為標準header
            content = re.sub(r'<header>.*?</header>', STANDARD_HEADER, content, flags=re.DOTALL)
            fixed_items.append('修復Header')
        else:
            # 在<body>後添加標準header
            content = re.sub(r'(<body[^>]*>)', r'\1\n' + STANDARD_HEADER, content)
            fixed_items.append('添加Header')
    
    # 檢查CSS連結
    if 'style.css' not in content:
        # 在</head>前添加CSS
        content = re.sub(r'(</head>)', r'    <link rel="stylesheet" href="/static/css/style.css">\n\1', content)
        fixed_items.append('添加CSS')
    
    # 檢查麵包屑
    if 'class="breadcrumb"' not in content:
        # 在<h1>前添加麵包屑
        breadcrumb = '''                <nav class="breadcrumb"><a href="/">首頁</a> > <a href="/articles/">攻略文章</a> > <span>文章</span></nav>
'''
        content = re.sub(r'(<h1[^>]*>)', breadcrumb + r'\1', content)
        fixed_items.append('添加麵包屑')
    
    # 檢查Sidebar
    if 'class="sidebar"' not in content:
        # 在</article>前添加Sidebar
        content = re.sub(r'(</article>)', STANDARD_SIDEBAR + '\n        </div>\n' + BOTTOM_CTA + '\n' + RELATED_ARTICLES + '\n' + r'\1', content)
        fixed_items.append('添加Sidebar和CTA')
    
    # 檢查Footer
    if 'class="footer"' not in content:
        content = re.sub(r'(</body>)', FOOTER + '\n' + r'\1', content)
        fixed_items.append('添加Footer')
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixed_items
    return False, []

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始修復文章格式...\n")
    
    fixed_count = 0
    for filepath in articles_dir.glob('*.html'):
        # 跳過index.html
        if filepath.name == 'index.html':
            continue
        
        try:
            was_fixed, items = fix_article_format(filepath)
            if was_fixed:
                print(f"  ✓ {filepath.name}: {', '.join(items)}")
                fixed_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print(f"\n✅ 共修復 {fixed_count} 篇文章")

if __name__ == '__main__':
    main()
