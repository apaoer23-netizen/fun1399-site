#!/usr/bin/env python3
"""
移除所有文章底部的固定平台推薦區塊
平台比較應該是文章內容的一部分，而非固定模板
"""

import re
from pathlib import Path

def remove_platform_cta(filepath):
    """移除文章中的平台推薦區塊"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 移除 platform-grid 區塊 (各種可能的格式)
    patterns = [
        # 標準格式
        r'<div class="cta-box featured"\s*\u003e\s*<h3>🔥[^\u003c]*</h3>\s*<div class="platform-grid"\u003e.*?\u003c/div>\s*</div\u003e',
        # 可能有換行的格式
        r'<div class="cta-box featured"\u003e[^\u003c]*<h3>[^\u003c]*推薦[^\u003c]*</h3>[^\u003c]*<div class="platform-grid"\u003e.*?\u003c/div>[^\u003c]*</div\u003e',
    ]
    
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    
    # 清理多餘的換行
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔧 開始移除所有平台推薦模板區塊...\n")
    
    removed_count = 0
    for filepath in articles_dir.glob('*.html'):
        try:
            if remove_platform_cta(filepath):
                print(f"  ✓ {filepath.name}: 移除平台推薦區塊")
                removed_count += 1
        except Exception as e:
            print(f"  ❌ {filepath.name}: {e}")
    
    print(f"\n✅ 共移除 {removed_count} 篇文章的平台推薦區塊")
    print("\n📋 說明:")
    print("  • 所有文章底部的固定5家平台推薦區塊已移除")
    print("  • 平台比較應該在文章內文自然呈現")
    print("  • 與主題相關的平台比較由作者自行撰寫")

if __name__ == '__main__':
    main()
