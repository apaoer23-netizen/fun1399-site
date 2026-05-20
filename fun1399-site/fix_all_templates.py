#!/usr/bin/env python3
"""
批量修正文章模板
- 推薦/比較類文章：添加平台推薦區塊
- 一般攻略文章：移除平台推薦區塊，保留基本CTA
"""

import os
import re
from pathlib import Path

# 平台推薦區塊HTML
PLATFORM_CTA = '''<div class="cta-box featured">
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

# 底部CTA區塊
BOTTOM_CTA = '''<div class="cta-box bottom-cta">
    <h3>🚀 準備開始你的娛樂城之旅？</h3>
    <p>立即加入我們推薦的平台，領取專屬優惠！</p>
    <div class="cta-buttons">
        <a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="btn btn-primary btn-large">🎮 立即遊玩</a>
        <a href="https://lin.ee/Mc1pb7z" target="_blank" class="btn btn-line btn-large">💬 加入LINE@獲取優惠</a>
    </div>
</div>'''

# 推薦/比較類文章關鍵詞
RECO_KEYWORDS = [
    '推薦', '排行', '比較', '排名', '最佳', '出金排行', 
    '娛樂城比較', '2026推薦', 'recommend', 'ranking',
    '出金速度', 'withdrawal', 'rtp比較'
]

def is_recommendation_article(filename, content):
    """判斷是否為推薦/比較類文章"""
    text = (filename + ' ' + content[:500]).lower()
    for keyword in RECO_KEYWORDS:
        if keyword.lower() in text:
            return True
    return False

def fix_article_template(filepath):
    """修正文章模板"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    filename = filepath.name
    is_reco = is_recommendation_article(filename, content)
    
    has_platform = 'platform-grid' in content
    has_bottom_cta = 'bottom-cta' in content
    
    if is_reco:
        # 推薦類文章：確保有平台區塊
        if not has_platform:
            # 在相關文章前或footer前添加平台區塊
            if 'related-articles' in content:
                content = content.replace(
                    '<div class="related-articles"',
                    PLATFORM_CTA + '\n\n    <div class="related-articles"'
                )
            else:
                content = content.replace(
                    '</footer',
                    PLATFORM_CTA + '\n\n</footer'
                )
            print(f"  ✓ {filename}: 添加平台推薦區塊")
        
        # 確保有底部CTA
        if not has_bottom_cta:
            if 'related-articles' in content:
                content = content.replace(
                    '<div class="related-articles"',
                    BOTTOM_CTA + '\n\n    <div class="related-articles"'
                )
            else:
                content = content.replace(
                    '</footer',
                    BOTTOM_CTA + '\n\n</footer'
                )
    else:
        # 一般攻略文章：移除平台區塊（如果有）
        if has_platform:
            # 移除platform-grid區塊
            content = re.sub(
                r'<div class="cta-box featured">\s*<h3>🔥[^\u003c]*</h3>\s*<div class="platform-grid">.*?\u003c/div>\s*\u003c/div>',
                '',
                content,
                flags=re.DOTALL
            )
            print(f"  ✓ {filename}: 移除平台推薦區塊")
        
        # 確保有底部CTA（但不含平台推薦）
        if not has_bottom_cta:
            if 'related-articles' in content:
                content = content.replace(
                    '<div class="related-articles"',
                    BOTTOM_CTA + '\n\n    <div class="related-articles"'
                )
            else:
                content = content.replace(
                    '</footer',
                    BOTTOM_CTA + '\n\n</footer'
                )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始修正文章模板...\n")
    
    fixed_count = 0
    for filepath in articles_dir.glob('*.html'):
        try:
            if fix_article_template(filepath):
                fixed_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print(f"\n✅ 共修正 {fixed_count} 篇文章")

if __name__ == '__main__':
    main()
