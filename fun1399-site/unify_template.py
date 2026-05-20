#!/usr/bin/env python3
"""
統一文章模板為 world-cup-2026-guide 風格
移除所有多餘的CTA和浮動按鈕
"""

import re
from pathlib import Path

def fix_article_template(filepath):
    """統一文章模板"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixed_items = []
    
    # 1. 移除 bottom-cta 區塊
    if 'bottom-cta' in content:
        content = re.sub(
            r'<div class="cta-box bottom-cta"[^\u003e]*>.*?\u003c/div>\s*</div>',
            '',
            content,
            flags=re.DOTALL
        )
        fixed_items.append('移除bottom-cta')
    
    # 2. 移除 float-play/float-line 浮動按鈕
    if 'float-play' in content or 'float-line' in content:
        content = re.sub(
            r'<a href="[^"]*" class="float-play"[^\u003e]*>[^\u003c]*\u003c/a>',
            '',
            content
        )
        content = re.sub(
            r'<a href="[^"]*" class="float-line"[^\u003e]*>[^\u003c]*\u003c/a>',
            '',
            content
        )
        fixed_items.append('移除浮動按鈕')
    
    # 3. 移除 platform-grid 平台推薦區塊
    if 'platform-grid' in content:
        content = re.sub(
            r'<div class="cta-box featured"[^\u003e]*>\s*<h3>[^\u003c]*推薦[^\u003c]*</h3>\s*<div class="platform-grid"\u003e.*?\u003c/div>\s*</div>',
            '',
            content,
            flags=re.DOTALL
        )
        fixed_items.append('移除平台推薦區塊')
    
    # 4. 移除多餘的空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixed_items
    return False, []

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始統一文章模板...")
    print("📋 標準模板：world-cup-2026-guide.html 風格")
    print("✂️  移除項目：bottom-cta、浮動按鈕、平台推薦區塊\n")
    
    fixed_count = 0
    for filepath in articles_dir.glob('*.html'):
        if filepath.name == 'index.html':
            continue
        
        try:
            was_fixed, items = fix_article_template(filepath)
            if was_fixed:
                print(f"  ✓ {filepath.name}: {', '.join(items)}")
                fixed_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print(f"\n✅ 共修復 {fixed_count} 篇文章")
    print("\n📋 統一後的模板結構：")
    print("  1. Header導航列")
    print("  2. 麵包屑導航")
    print("  3. H1標題")
    print("  4. 作者資訊")
    print("  5. 文章內容（含目錄、段落）")
    print("  6. 延伸閱讀/簡單CTA（如需要）")
    print("  7. Sidebar")
    print("  8. Footer")
    print("\n❌ 已移除：")
    print("  - bottom-cta 區塊")
    print("  - 浮動立即遊玩按鈕")
    print("  - 底部平台推薦區塊")

if __name__ == '__main__':
    main()
