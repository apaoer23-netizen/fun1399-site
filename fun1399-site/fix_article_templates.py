#!/usr/bin/env python3
"""
文章模板修復腳本
自動檢測並修復不符合規範的文章
"""

import os
import re
import random
from pathlib import Path
from datetime import datetime

# 設定
AUTHORS = {
    'kevin': {
        'name': 'Kevin Lin',
        'title': '資深娛樂城分析師 / 百家樂策略專家',
        'expertise': ['百家樂', '娛樂城評測', '資金管理']
    },
    'jason': {
        'name': 'Jason Chen',
        'title': '博弈產業研究員 / 數據分析師',
        'expertise': ['產業分析', '數據研究', '市場趨勢']
    },
    'vivian': {
        'name': 'Vivian Wu',
        'title': '資深玩家顧問 / 優惠活動專家',
        'expertise': ['優惠攻略', '新手教學', '平台比較']
    }
}

PLATFORM_LINKS = {
    '鉅城': 'https://fun1399.ofa177.net/',
    'MBM': 'https://fun1399.mbm88.net/',
    '優塔': 'https://u.town/3006',
    'HG': 'https://www.leyo.tw/r?p=685e99859c687',
    '大老爺': 'https://fun1399.gm1688.net/',
    '3A': 'https://fun1399.3a1788.bet/'
}

RELATED_ARTICLES = [
    ('baccarat-guide.html', '百家樂技巧：從入門到高手的完整攻略'),
    ('slots-guide.html', '老虎機攻略：RTP、波動度與中獎密技'),
    ('sports-betting-guide.html', '體育投注教學：從新手到專業玩家'),
    ('safety-guide.html', '娛樂城安全指南：如何選擇安全平台'),
    ('wagering-guide.html', '洗碼量流水計算完整教學'),
    ('withdrawal-ranking.html', '娛樂城出金速度排行榜'),
    ('casino-recommendation-2026.html', '2026年娛樂城推薦：6大平台比較'),
    ('rtp-compare.html', '娛樂城RTP比較：哪個平台最划算'),
]

# 統計資訊
stats = {
    'checked': 0,
    'fixed': 0,
    'added_author': 0,
    'added_cta': 0,
    'added_related': 0,
    'added_sidebar': 0,
    'added_internal_links': 0
}

def detect_article_topic(content, filename):
    """根據內容和檔名判斷文章主題"""
    topic_keywords = {
        'baccarat': '百家樂',
        'slots': '老虎機',
        'sports': '體育投注',
        'soccer': '足球投注',
        'nba': 'NBA投注',
        'mlb': 'MLB投注',
        'world-cup': '世界盃',
        'safety': '安全',
        'scam': '詐騙',
        'withdrawal': '出金',
        'deposit': '儲值',
        'bonus': '優惠',
        'cashback': '返水',
        'app': 'APP下載',
        'mobile': '手機版',
        'live': '真人娛樂',
        'fish': '捕魚機',
        'lottery': '彩票',
        'poker': '撲克',
        'vip': 'VIP',
        'newbie': '新手',
        'usdt': 'USDT',
        'rtp': 'RTP',
        'wagering': '洗碼量'
    }
    
    filename_lower = filename.lower()
    content_lower = content.lower()
    
    for key, topic in topic_keywords.items():
        if key in filename_lower or key in content_lower:
            return topic
    
    return '一般'

def select_author(topic):
    """根據主題選擇合適的作者"""
    topic_author_map = {
        '百家樂': 'kevin',
        '老虎機': 'vivian',
        '體育投注': 'jason',
        '足球投注': 'jason',
        'NBA投注': 'jason',
        '安全': 'jason',
        '詐騙': 'jason',
        '優惠': 'vivian',
        '返水': 'vivian',
        '新手': 'vivian',
        'VIP': 'vivian'
    }
    
    author_id = topic_author_map.get(topic)
    if author_id:
        return author_id, AUTHORS[author_id]
    
    # 隨機選擇
    author_id = random.choice(list(AUTHORS.keys()))
    return author_id, AUTHORS[author_id]

def generate_article_meta(author_id, author_info):
    """生成文章元資訊HTML"""
    today = datetime.now().strftime('%Y年%m月%d日')
    return f'''<div class="article-meta">
    <div class="author-info">
        <span class="author-name">👤 作者：<a href="/author.html#{author_id}">{author_info['name']}</a>（{author_info['title']}）</span>
        <span class="publish-date">📅 發布日期：{today}</span>
        <span class="update-date">🔄 最後更新：{today}</span>
    </div>
</div>'''

def generate_platform_cta():
    """生成平台推薦CTA"""
    return '''<div class="cta-box featured">
    <h3>🔥 2026年推薦娛樂城平台</h3>
    <div class="platform-grid">
        <div class="platform-card">
            <h4>鉅城娛樂城</h4>
            <p>★★★★★ 4.9/5</p>
            <p>首儲1000送1000</p>
            <a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="btn btn-primary">立即註冊</a>
        </div>
        <div class="platform-card">
            <h4>MBM娛樂城</h4>
            <p>★★★★☆ 4.7/5</p>
            <p>2分鐘極速出金</p>
            <a href="https://fun1399.mbm88.net/" target="_blank" rel="noopener" class="btn btn-primary">立即註冊</a>
        </div>
        <div class="platform-card">
            <h4>優塔娛樂城</h4>
            <p>★★★★☆ 4.6/5</p>
            <p>USDT專精 1%返水</p>
            <a href="https://u.town/3006" target="_blank" rel="noopener" class="btn btn-primary">立即註冊</a>
        </div>
        <div class="platform-card">
            <h4>HG娛樂城</h4>
            <p>★★★★☆ 4.5/5</p>
            <p>體驗金388免費試玩</p>
            <a href="https://www.leyo.tw/r?p=685e99859c687" target="_blank" rel="noopener" class="btn btn-primary">立即註冊</a>
        </div>
        <div class="platform-card">
            <h4>大老爺娛樂城</h4>
            <p>★★★★☆ 4.4/5</p>
            <p>遊戲種類最豐富</p>
            <a href="https://fun1399.gm1688.net/" target="_blank" rel="noopener" class="btn btn-primary">立即註冊</a>
        </div>
    </div>
</div>'''

def generate_bottom_cta():
    """生成底部CTA"""
    return '''<div class="cta-box bottom-cta">
    <h3>🚀 準備開始你的娛樂城之旅？</h3>
    <p>立即加入我們推薦的平台，領取專屬優惠！</p>
    <div class="cta-buttons">
        <a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="btn btn-primary btn-large">🎮 立即遊玩</a>
        <a href="https://lin.ee/Mc1pb7z" target="_blank" class="btn btn-line btn-large">💬 加入LINE@獲取優惠</a>
    </div>
</div>'''

def generate_related_articles(current_file):
    """生成相關文章推薦"""
    # 選擇3-5篇隨機相關文章（不包含當前文章）
    available = [a for a in RELATED_ARTICLES if a[0] != current_file]
    selected = random.sample(available, min(5, len(available)))
    
    links = '\n'.join([f'<li>👉 <a href="/articles/{file}">{title}</a></li>' for file, title in selected])
    
    return f'''<div class="related-articles">
    <h3>📚 相關文章推薦</h3>
    <ul class="related-list">
        {links}
        <li>👉 <a href="/recommend/2026.html">2026最新娛樂城推薦</a></li>
        <li>👉 <a href="/articles/safety-guide.html">娛樂城安全指南</a></li>
    </ul>
</div>'''

def generate_sidebar():
    """生成Sidebar"""
    return '''<aside class="sidebar">
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
            <li>
                <a href="/reviews/hg.html" class="sidebar-link">
                    <span class="sidebar-rank">#4</span>
                    <span>HG娛樂城</span>
                    <span class="sidebar-rating">★4.5</span>
                </a>
            </li>
            <li>
                <a href="/reviews/gm1688.html" class="sidebar-link">
                    <span class="sidebar-rank">#5</span>
                    <span>大老爺娛樂城</span>
                    <span class="sidebar-rating">★4.4</span>
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
            <li><a href="/articles/wagering-guide.html">洗碼量計算教學</a></li>
            <li><a href="/articles/withdrawal-ranking.html">出金速度排行</a></li>
        </ul>
    </div>

    <div class="sidebar-widget">
        <h4>🎁 最新優惠</h4>
        <ul class="sidebar-list">
            <li><a href="/promotions/2026-03.html">2026年3月優惠總整理</a></li>
            <li><a href="/articles/cashback-guide.html">返水攻略指南</a></li>
        </ul>
    </div>

    <div class="sidebar-widget sidebar-cta">
        <h4>💬 加入 LINE@</h4>
        <p>獲取最新優惠情報與專業攻略</p>
        <a href="https://lin.ee/Mc1pb7z" class="btn btn-line" target="_blank">加入好友</a>
    </div>
</aside>'''

def fix_article(filepath):
    """修復單篇文章"""
    filename = filepath.name
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixed = False
    fixes = []
    
    # 檢測文章主題
    topic = detect_article_topic(content, filename)
    author_id, author_info = select_author(topic)
    
    # 1. 檢查並添加作者資訊
    if 'author.html#' not in content and '作者：' not in content:
        # 找到 h1 標題後面插入作者資訊
        h1_match = re.search(r'(<h1[^>]*>.*?</h1>)', content, re.DOTALL)
        if h1_match:
            article_meta = generate_article_meta(author_id, author_info)
            insert_pos = h1_match.end()
            content = content[:insert_pos] + '\n' + article_meta + content[insert_pos:]
            fixes.append('添加作者資訊')
            stats['added_author'] += 1
            fixed = True
    
    # 2. 檢查並添加平台推薦CTA
    if 'platform-grid' not in content and 'platform-card' not in content:
        # 在文章結尾前添加
        if '</div>\n</footer' in content or '</footer' in content:
            platform_cta = generate_platform_cta()
            # 找到文章內容區域結尾
            content = re.sub(r'(</div>\s*</footer)', platform_cta + '\n\\1', content)
            fixes.append('添加平台推薦CTA')
            stats['added_cta'] += 1
            fixed = True
    
    # 3. 檢查並添加底部CTA
    if 'bottom-cta' not in content:
        bottom_cta = generate_bottom_cta()
        # 在相關文章或footer前添加
        if 'related-articles' in content:
            content = re.sub(r'(<div class="related-articles)', bottom_cta + '\n\\1', content)
        else:
            content = re.sub(r'(</div>\s*<footer)', bottom_cta + '\n\\1', content)
        fixes.append('添加底部CTA')
        stats['added_cta'] += 1
        fixed = True
    
    # 4. 檢查並添加相關文章
    if 'related-articles' not in content and '相關文章' not in content:
        related = generate_related_articles(filename)
        content = re.sub(r'(</div>\s*<footer)', related + '\n\\1', content)
        fixes.append('添加相關文章')
        stats['added_related'] += 1
        fixed = True
    
    # 5. 檢查並添加Sidebar
    if '<aside class="sidebar"' not in content and 'sidebar-widget' not in content:
        # 找到 content-main 結尾，添加 sidebar
        sidebar = generate_sidebar()
        # 嘗試在 content-main 結尾後添加
        content = re.sub(r'(</div>\s*</footer)', sidebar + '\n\\1', content)
        fixes.append('添加Sidebar')
        stats['added_sidebar'] += 1
        fixed = True
    
    # 6. 添加內部連結（在內容中）
    internal_links_added = 0
    # 如果沒有連結到推薦頁，添加一個
    if 'recommend/2026' not in content:
        # 在適當位置添加內部連結
        content = re.sub(
            r'(<p>.*?</p>)',
            r'\1\n<p>推薦閱讀：<a href="/recommend/2026.html">2026最新娛樂城推薦</a></p>',
            content,
            count=1
        )
        internal_links_added += 1
    
    if internal_links_added > 0:
        fixes.append(f'添加{internal_links_added}個內部連結')
        stats['added_internal_links'] += 1
        fixed = True
    
    # 寫回檔案
    if fixed and content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        stats['fixed'] += 1
        return True, fixes
    
    return False, []

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    if not articles_dir.exists():
        print(f"❌ 找不到目錄: {articles_dir}")
        return
    
    html_files = list(articles_dir.glob('*.html'))
    
    print(f"🔍 開始檢查 {len(html_files)} 篇文章...")
    print()
    
    for filepath in html_files:
        stats['checked'] += 1
        filename = filepath.name
        
        try:
            was_fixed, fixes = fix_article(filepath)
            
            if was_fixed:
                print(f"✅ {filename}: {' / '.join(fixes)}")
            elif stats['checked'] <= 5:  # 只顯示前5個已規範的
                print(f"  {filename}: 已符合規範")
                
        except Exception as e:
            print(f"❌ {filename}: 修復失敗 - {e}")
    
    # 輸出統計
    print()
    print("=" * 60)
    print("📊 修復報告")
    print("=" * 60)
    print(f"檢查文章數: {stats['checked']}")
    print(f"修復文章數: {stats['fixed']}")
    print(f"添加作者資訊: {stats['added_author']}")
    print(f"添加CTA區塊: {stats['added_cta']}")
    print(f"添加相關文章: {stats['added_related']}")
    print(f"添加Sidebar: {stats['added_sidebar']}")
    print(f"添加內部連結: {stats['added_internal_links']}")
    print("=" * 60)

if __name__ == '__main__':
    main()
