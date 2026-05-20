#!/usr/bin/env python3
"""
Add related article links to fun1399 article pages.
Creates a cross-link network to help Google crawl isolated pages.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path('/root/.openclaw/workspace/fun1399-clean')
ARTICLES_DIR = BASE_DIR / 'articles'

# Article categories with related links mapping
RELATED_LINKS = {
    'scam': [
        ('/articles/casino-scam-methods', '娛樂城詐騙手法大全：2026最新騙術拆解'),
        ('/articles/casino-no-withdrawal-scam', '娛樂城不出金詐騙：如何識別與自保'),
        ('/articles/casino-fake-customer-service', '假客服詐騙：LINE官方帳號辨識攻略'),
        ('/articles/casino-investment-scam', '娛樂城投資詐騙手法：代操保證獲利是真的嗎？'),
        ('/articles/casino-scam-emergency-response', '被娛樂城詐騙了怎麼辦？緊急應變5步驟'),
        ('/articles/how-to-check-casino-scam-record', '如何查詢娛樂城詐騙紀錄與黑網名單'),
        ('/articles/casino-account-freeze-scam', '娛樂城帳號凍結詐騙：要求儲值解凍都是騙局'),
        ('/articles/casino-romance-scam', '娛樂城愛情詐騙揭秘：交友軟體假帳號識別'),
        ('/articles/fake-line-official-account', '娛樂城假客服詐騙升級版：LINE官方帳號辨識'),
    ],
    'guide': [
        ('/articles/casino-registration-guide', '娛樂城註冊教學：新手開戶完整流程'),
        ('/articles/casino-withdrawal-tutorial', '娛樂城提款完整教學：出金流程與注意事項'),
        ('/articles/deposit-guide', '娛樂城儲值教學：安全入金方式比較'),
        ('/articles/fast-withdrawal', '快速出金娛樂城推薦：15分鐘內到帳實測'),
        ('/articles/casino-deposit-methods', '娛樂城入金方式比較：哪種最方便安全？'),
        ('/articles/casino-withdrawal-fast', '娛樂城快速出金實測：各平台速度比較'),
        ('/articles/withdrawal-risks', '娛樂城出金風險：哪些情況會被拖延或拒絕'),
        ('/articles/cashback-guide', '返水教學：如何計算與最大化你的返水收益'),
        ('/articles/wagering-guide', '流水教學：娛樂城投注要求計算方式'),
        ('/articles/safety-guide', '娛樂城安全指南'),
    ],
    'game': [
        ('/articles/baccarat-guide', '百家樂完整攻略：規則、牌路與下注策略'),
        ('/articles/baccarat-rules', '百家樂規則詳解：從基礎到進階'),
        ('/articles/baccarat-strategy', '百家樂策略：看路法與注碼管理'),
        ('/articles/slots-guide', '老虎機攻略：RTP、波動度與選台技巧'),
        ('/articles/slots-beginner', '老虎機新手教學：第一次玩就上手'),
        ('/articles/slots-myths', '老虎機迷思破解：冷熱台、必中法都是假的'),
        ('/articles/high-rtp-slots', '高RTP老虎機推薦：回報率最高的遊戲'),
        ('/articles/rtp-compare', '娛樂城RTP比較：哪家遊戲回報率最高'),
        ('/articles/sports-betting-guide', '體育投注完整教學：賠率計算與投注策略'),
        ('/articles/sports-betting-tips', '體育投注技巧：提高勝率的5個策略'),
        ('/articles/soccer-betting', '足球投注教學：亞洲盤、大小球玩法'),
        ('/articles/nba-betting', 'NBA投注教學：讓分盤、大小球與單節玩法'),
        ('/articles/mlb-betting', 'MLB投注教學：讓分盤、大小球與獨贏玩法'),
        ('/articles/live-casino-guide', '真人娛樂城教學：百家樂、龍虎、骰寶'),
        ('/articles/fish-game-guide', '捕魚機教學：技巧與選台攻略'),
        ('/articles/poker-casino-guide', '撲克遊戲教學：德州撲克與奧馬哈'),
        ('/articles/lottery-casino-guide', '彩票遊戲教學：六合彩、539玩法'),
    ],
    'bonus': [
        ('/articles/free-credit-guide', '娛樂城體驗金完整指南'),
        ('/articles/casino-bonus-guide', '娛樂城優惠攻略：返水、體驗金與首儲怎麼領'),
        ('/articles/casino-free-trial-bonus', '體驗金詐騙：領取優惠前必看的陷阱'),
        ('/articles/vip-guide', '娛樂城VIP制度解析'),
        ('/articles/high-cashback-casino', '高返水娛樂城推薦：哪家返水最優惠'),
    ],
    'review': [
        ('/reviews/jucity', '鉅城娛樂城評測'),
        ('/reviews/mbm', 'MBM娛樂城評測'),
        ('/reviews/utown', '優塔娛樂城評測'),
        ('/reviews/hg', 'HG娛樂城評測'),
        ('/reviews/3a', '3A娛樂城評測'),
        ('/reviews/gm1688', 'GM1688娛樂城評測'),
        ('/articles/2026-casino-recommendation', '2026娛樂城推薦完整指南'),
        ('/articles/casino-ranking-2026', '2026年娛樂城排名'),
        ('/articles/withdrawal-ranking', '娛樂城出金速度排行'),
        ('/articles/newbie-friendly', '新手友善娛樂城推薦'),
        ('/articles/mobile-casino-guide', '手機娛樂城推薦'),
        ('/articles/casino-review-real', '真實娛樂城評價：如何辨識假評價'),
        ('/articles/casino-safe', '安全娛樂城推薦：5大必備條件'),
    ],
    'worldcup': [
        ('/articles/world-cup-2026-guide', '2026世界盃投注攻略'),
        ('/articles/world-cup-betting-guide', '世界盃投注教學'),
        ('/articles/world-cup-betting-tips', '世界盃投注技巧'),
        ('/articles/world-cup-favorites', '世界盃奪冠熱門分析'),
        ('/articles/world-cup-live-betting', '世界盃滾球投注教學'),
        ('/articles/world-cup-schedule', '2026世界盃賽程表'),
    ],
    'pillar': [
        ('/pillars/newbie-guide', '娛樂城新手完全指南'),
        ('/pillars/baccarat-master', '百家樂大師攻略'),
        ('/pillars/sports-betting-master', '體育投注大師攻略'),
        ('/pillars/casino-scam-complete-guide', '娛樂城詐騙完整指南'),
    ],
}

# Map article filenames to categories
ARTICLE_CATEGORIES = {
    # Scam articles
    'casino-scam-methods': 'scam',
    'casino-no-withdrawal-scam': 'scam',
    'casino-fake-customer-service': 'scam',
    'casino-investment-scam': 'scam',
    'casino-scam-emergency-response': 'scam',
    'how-to-check-casino-scam-record': 'scam',
    'casino-account-freeze-scam': 'scam',
    'casino-romance-scam': 'scam',
    'fake-line-official-account': 'scam',
    'casino-scam-alert': 'scam',
    '3a-casino-scam-review': 'scam',
    'gm1688-casino-scam-review': 'scam',
    'biwin-casino-no-withdrawal': 'scam',
    'utown-casino-scam-review': 'scam',
    'wealth-god-casino-scam-review': 'scam',
    
    # Guide articles
    'casino-registration-guide': 'guide',
    'casino-withdrawal-tutorial': 'guide',
    'deposit-guide': 'guide',
    'fast-withdrawal': 'guide',
    'casino-deposit-methods': 'guide',
    'casino-withdrawal-fast': 'guide',
    'withdrawal-risks': 'guide',
    'cashback-guide': 'guide',
    'wagering-guide': 'guide',
    'safety-guide': 'guide',
    
    # Game articles
    'baccarat-guide': 'game',
    'baccarat-rules': 'game',
    'baccarat-strategy': 'game',
    'slots-guide': 'game',
    'slots-beginner': 'game',
    'slots-myths': 'game',
    'high-rtp-slots': 'game',
    'rtp-compare': 'game',
    'sports-betting-guide': 'game',
    'sports-betting-tips': 'game',
    'soccer-betting': 'game',
    'nba-betting': 'game',
    'mlb-betting': 'game',
    'live-casino-guide': 'game',
    'fish-game-guide': 'game',
    'poker-casino-guide': 'game',
    'lottery-casino-guide': 'game',
    
    # Bonus articles
    'free-credit-guide': 'bonus',
    'casino-bonus-guide': 'bonus',
    'casino-free-trial-bonus': 'bonus',
    'vip-guide': 'bonus',
    'high-cashback-casino': 'bonus',
    
    # Review articles
    '2026-casino-recommendation': 'review',
    'casino-ranking-2026': 'review',
    'withdrawal-ranking': 'review',
    'newbie-friendly': 'review',
    'mobile-casino-guide': 'review',
    'casino-review-real': 'review',
    'casino-safe': 'review',
    'jucity-casino-review-may-2026': 'review',
    'hg-casino-review': 'review',
    'mbm-casino-review': 'review',
    
    # World Cup
    'world-cup-2026-guide': 'worldcup',
    'world-cup-betting-guide': 'worldcup',
    'world-cup-betting-tips': 'worldcup',
    'world-cup-favorites': 'worldcup',
    'world-cup-live-betting': 'worldcup',
    'world-cup-schedule': 'worldcup',
    
    # Pillar-like articles
    'casino-agent-guide': 'pillar',
    'casino-customer-service': 'pillar',
    'casino-app-download': 'pillar',
    'usdt-casino': 'pillar',
    'casino-ptt-discussion': 'pillar',
    'casino-dcard-2026': 'pillar',
}

def get_related_html(article_name, current_path):
    """Generate related articles HTML for a given article."""
    category = ARTICLE_CATEGORIES.get(article_name, 'scam')
    
    # Get links from same category + a few from other categories
    links = list(RELATED_LINKS.get(category, RELATED_LINKS['scam']))
    
    # Add cross-category links for variety
    cross_cats = ['guide', 'game', 'review', 'bonus']
    for cat in cross_cats:
        if cat != category and links:
            # Add 1-2 links from other categories
            for url, title in RELATED_LINKS.get(cat, []):
                if (url, title) not in links:
                    links.append((url, title))
                    break
    
    # Remove self-reference
    current_url = f'/articles/{article_name}'
    links = [(url, title) for url, title in links if url != current_url]
    
    # Pick up to 8 links
    selected = links[:8]
    
    if not selected:
        return ''
    
    html_parts = [
        '\n\n<!-- Related Articles -->',
        '<div class="related-articles" style="margin-top: 60px; padding: 30px; background: #f8f9fa; border-radius: 12px; border-left: 4px solid #00d4aa;">',
        '  <h3 style="font-size: 22px; margin-bottom: 20px; color: #1a1a2e;">📚 你可能還想看</h3>',
        '  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">',
    ]
    
    for url, title in selected:
        html_parts.append(
            f'    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">'
            f'<a href="{url}" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ {title}</a></div>'
        )
    
    html_parts.extend([
        '  </div>',
        '</div>',
        '<!-- End Related Articles -->\n',
    ])
    
    return '\n'.join(html_parts)


def add_related_to_article(filepath):
    """Add related articles block before </body> or footer."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    article_name = filepath.stem
    
    # Skip if already has related articles
    if 'related-articles' in content or '你可能還想看' in content:
        return False
    
    related_html = get_related_html(article_name, str(filepath))
    
    if not related_html:
        return False
    
    # Insert before </body> or before footer
    if '</body>' in content:
        content = content.replace('</body>', related_html + '\n</body>')
    elif '<footer' in content:
        content = content.replace('<footer', related_html + '\n<footer')
    else:
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def main():
    modified = 0
    skipped = 0
    
    for html_file in sorted(ARTICLES_DIR.glob('*.html')):
        # Skip index.html
        if html_file.name == 'index.html':
            continue
        
        result = add_related_to_article(html_file)
        if result:
            modified += 1
        else:
            skipped += 1
    
    print(f'Modified: {modified} articles')
    print(f'Skipped: {skipped} articles (already had related links or no match)')


if __name__ == '__main__':
    main()
