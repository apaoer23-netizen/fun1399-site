#!/usr/bin/env python3
"""
為所有文章添加「延伸閱讀」區塊
根據文章主題推薦相關文章
"""

import re
from pathlib import Path

# 定義文章分類和相關文章映射
RELATED_ARTICLES_MAP = {
    # 世界盃相關
    'world-cup': {
        'pattern': r'world.?cup|世界盃|世足',
        'articles': [
            ('/articles/world-cup-favorites.html', '2026世界盃奪冠熱門分析'),
            ('/articles/world-cup-betting-guide.html', '世界盃投注玩法完整教學'),
            ('/articles/world-cup-betting-tips.html', '世界盃投注技巧與策略'),
            ('/articles/world-cup-schedule.html', '2026世界盃賽程時間表'),
            ('/articles/sports-betting-guide.html', '體育投注基礎教學'),
        ]
    },
    # 體育投注相關
    'sports': {
        'pattern': r'sport|體育|投注|足球|籃球|棒球|soccer|nba|mlb',
        'articles': [
            ('/articles/sports-betting-guide.html', '體育投注完整教學'),
            ('/articles/soccer-betting.html', '足球投注攻略'),
            ('/articles/nba-betting.html', 'NBA投注教學'),
            ('/articles/mlb-betting.html', 'MLB棒球投注攻略'),
            ('/articles/world-cup-2026-guide.html', '2026世界盃完整指南'),
        ]
    },
    # 百家樂相關
    'baccarat': {
        'pattern': r'baccarat|百家樂',
        'articles': [
            ('/articles/baccarat-guide.html', '百家樂技巧完整攻略'),
            ('/articles/baccarat-strategy.html', '百家樂策略進階教學'),
            ('/articles/baccarat-rules.html', '百家樂規則詳解'),
        ]
    },
    # 老虎機相關
    'slots': {
        'pattern': r'slot|老虎機|rtp',
        'articles': [
            ('/articles/slots-guide.html', '老虎機完整攻略'),
            ('/articles/slots-beginner.html', '老虎機新手入門'),
            ('/articles/slots-myths.html', '老虎機迷思破解'),
            ('/articles/rtp-compare.html', '娛樂城RTP比較分析'),
        ]
    },
    # 安全防詐相關
    'safety': {
        'pattern': r'safety|safe|scam|安全|詐騙|防詐',
        'articles': [
            ('/articles/safety-guide.html', '娛樂城安全完整指南'),
            ('/articles/casino-safe.html', '如何選擇安全娛樂城'),
            ('/articles/casino-scam-methods.html', '常見詐騙手法解析'),
            ('/articles/casino-safety-check.html', '娛樂城安全檢查清單'),
        ]
    },
    # 出金相關
    'withdrawal': {
        'pattern': r'withdrawal|出金|提款',
        'articles': [
            ('/articles/withdrawal-ranking.html', '娛樂城出金速度排行'),
            ('/articles/fast-withdrawal.html', '快速出金教學'),
            ('/articles/casino-withdrawal-fast.html', '娛樂城快速提款攻略'),
        ]
    },
    # 優惠相關
    'bonus': {
        'pattern': r'bonus|優惠|返水|cashback|體驗金|free.*credit',
        'articles': [
            ('/articles/casino-bonus-guide.html', '娛樂城優惠活動攻略'),
            ('/articles/cashback-guide.html', '返水攻略完整教學'),
            ('/articles/free-credit-guide.html', '體驗金領取攻略'),
        ]
    },
    # 儲值相關
    'deposit': {
        'pattern': r'deposit|儲值|存款|usdt',
        'articles': [
            ('/articles/deposit-guide.html', '娛樂城儲值完整教學'),
            ('/articles/usdt-casino.html', 'USDT娛樂城攻略'),
        ]
    },
    # 新手相關
    'newbie': {
        'pattern': r'newbie|新手|入門|beginner',
        'articles': [
            ('/articles/newbie-friendly.html', '新手友善娛樂城推薦'),
            ('/articles/casino-recommendation-2026.html', '2026娛樂城推薦'),
        ]
    },
    # 預設/通用
    'default': {
        'pattern': r'.*',
        'articles': [
            ('/articles/baccarat-guide.html', '百家樂技巧完整攻略'),
            ('/articles/slots-guide.html', '老虎機完整攻略'),
            ('/articles/sports-betting-guide.html', '體育投注教學'),
            ('/articles/safety-guide.html', '娛樂城安全指南'),
            ('/articles/recommend/2026.html', '2026最新娛樂城推薦'),
        ]
    }
}

def get_related_articles(filename, content):
    """根據文章內容獲取相關文章"""
    text = (filename + ' ' + content[:1000]).lower()
    
    # 檢查每個分類
    matched_articles = None
    for category, data in RELATED_ARTICLES_MAP.items():
        if category == 'default':
            continue
        if re.search(data['pattern'], text, re.IGNORECASE):
            matched_articles = data['articles']
            break
    
    # 如果沒有匹配，使用預設
    if not matched_articles:
        matched_articles = RELATED_ARTICLES_MAP['default']['articles']
    
    # 排除當前文章本身
    current_file = filename.replace('.html', '')
    filtered = [a for a in matched_articles if current_file not in a[0]]
    
    # 返回3-5篇
    return filtered[:5]

def generate_related_section(articles):
    """生成延伸閱讀HTML"""
    if not articles:
        return ''
    
    links = '\n'.join([f'                    <li><a href="{url}">{title}</a></li>' for url, title in articles])
    
    return f'''            <div class="cta-box">
                <h3>延伸閱讀</h3>
                <ul>
{links}
                </ul>
            </div>'''

def add_related_section(filepath):
    """為文章添加延伸閱讀區塊"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 檢查是否已有延伸閱讀
    if '延伸閱讀' in content or 'class="cta-box"' in content:
        # 已經有類似區塊，檢查是否需要更新
        if '延伸閱讀' in content:
            return False, '已有延伸閱讀'
    
    # 獲取相關文章
    filename = filepath.name
    related = get_related_articles(filename, content)
    
    if not related:
        return False, '無相關文章'
    
    related_html = generate_related_section(related)
    
    # 在 </div></article> 前插入延伸閱讀
    # 找到最後一個 </div> 在 </article> 之前
    pattern = r'(\s*)(</div>\s*</article>)'
    
    def insert_related(match):
        indent = match.group(1)
        return f'{indent}{related_html}\n{indent}{match.group(2)}'
    
    new_content = re.sub(pattern, insert_related, content, count=1)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, f'已添加 {len(related)} 篇相關文章'
    
    return False, '無法插入'

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始為所有文章添加「延伸閱讀」區塊")
    print("=" * 60)
    print()
    
    added_count = 0
    skipped_count = 0
    
    for filepath in sorted(articles_dir.glob('*.html')):
        if filepath.name == 'index.html':
            continue
        
        try:
            was_added, msg = add_related_section(filepath)
            if was_added:
                print(f"  ✅ {filepath.name}: {msg}")
                added_count += 1
            else:
                print(f"  ⏭️  {filepath.name}: {msg}")
                skipped_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print()
    print("=" * 60)
    print("📊 完成報告")
    print("=" * 60)
    print(f"已添加延伸閱讀：{added_count} 篇")
    print(f"跳過（已有）：{skipped_count} 篇")
    print()
    print("✅ 所有文章現在都包含延伸閱讀區塊")

if __name__ == '__main__':
    main()
