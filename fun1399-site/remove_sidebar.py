#!/usr/bin/env python3
"""
移除文章頁面的Sidebar，改為全寬內容布局
只保留 Header、文章內容、Footer
"""

import re
from pathlib import Path

def remove_sidebar(filepath):
    """移除文章的Sidebar"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixed_items = []
    
    # 1. 移除 content-with-sidebar 類別，改為單純 container
    content = re.sub(
        r'class="container content-with-sidebar"',
        'class="container"',
        content
    )
    if 'content-with-sidebar' in original:
        fixed_items.append('移除content-with-sidebar類別')
    
    # 2. 移除整個 aside.sidebar 區塊
    if '<aside class="sidebar"' in content:
        content = re.sub(
            r'<aside class="sidebar"[^\u003e]*>.*?\u003c/aside>',
            '',
            content,
            flags=re.DOTALL
        )
        fixed_items.append('移除Sidebar')
    
    # 3. 調整 content-main 容器（如果存在）
    content = re.sub(
        r'<div class="content-main"\u003e',
        '',
        content
    )
    content = re.sub(
        r'\u003c/div\u003e\s*\u003c!--\s*content-main\s*--\u003e',
        '',
        content,
        flags=re.DOTALL
    )
    
    # 4. 清理多餘的空行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixed_items
    return False, []

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始移除文章Sidebar...")
    print("📋 新布局：全寬內容（無側欄）\n")
    
    fixed_count = 0
    for filepath in articles_dir.glob('*.html'):
        if filepath.name == 'index.html':
            continue
        
        try:
            was_fixed, items = remove_sidebar(filepath)
            if was_fixed:
                print(f"  ✓ {filepath.name}: {', '.join(items) if items else '已清理布局'}")
                fixed_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print(f"\n✅ 共修復 {fixed_count} 篇文章")
    print("\n📋 新模板結構：")
    print("  1. Header導航列")
    print("  2. 麵包屑導航")
    print("  3. H1標題 + 作者資訊")
    print("  4. 文章內容（全寬）")
    print("  5. Footer")
    print("\n❌ 已移除：")
    print("  - Sidebar（推薦娛樂城）")
    print("  - Sidebar（熱門攻略）")
    print("  - Sidebar（最新優惠）")
    print("  - Sidebar（LINE CTA）")

if __name__ == '__main__':
    main()
