#!/usr/bin/env python3
"""
全站模板一致性檢查與強制統一
所有文章必須完全符合 world-cup-2026-guide.html 模板
"""

import re
from pathlib import Path

def get_standard_template():
    """讀取標準模板 world-cup-2026-guide.html"""
    template_path = Path('/root/.openclaw/workspace/fun1399-site/build/articles/world-cup-2026-guide.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_structure_template():
    """提取標準模板的結構框架"""
    standard = get_standard_template()
    
    # 提取從 <!DOCTYPE 到 </body> 的頭部
    head_match = re.search(r'(<!DOCTYPE.*?)<article', standard, re.DOTALL)
    head_template = head_match.group(1) if head_match else ''
    
    # 提取 article 開始標籤
    article_start = '<article class="content">'
    
    # 提取容器開始
    container_start = '        <div class="container">'
    
    return {
        'head_template': head_template,
        'article_start': article_start,
        'container_start': container_start,
    }

def check_article_issues(filepath):
    """檢查文章存在的問題"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    # 檢查1：DOCTYPE
    if '<!DOCTYPE html>' not in content[:50]:
        issues.append('缺少DOCTYPE')
    
    # 檢查2：lang 屬性
    if 'lang="zh-TW"' not in content[:200]:
        issues.append('缺少lang屬性')
    
    # 檢查3：CSS連結
    if '/static/css/style.css' not in content:
        issues.append('CSS路徑不正確')
    
    # 檢查4：GA4追蹤碼
    if 'G-1V53J5D71S' not in content:
        issues.append('缺少GA4追蹤碼')
    
    # 檢查5：header class
    if 'class="header"' not in content:
        issues.append('缺少標準header')
    
    # 檢查6：article class
    if 'class="content"' not in content or '<article class="content"' not in content:
        issues.append('article class不正確')
    
    # 檢查7：container class（不應有content-with-sidebar）
    if 'content-with-sidebar' in content:
        issues.append('仍有content-with-sidebar')
    
    # 檢查8：breadcrumb
    if 'class="breadcrumb"' not in content:
        issues.append('缺少麵包屑')
    
    # 檢查9：article-meta
    if 'class="article-meta"' not in content:
        issues.append('缺少article-meta')
    
    # 檢查10：sidebar
    if '<aside class="sidebar"' in content or '<aside' in content:
        issues.append('仍有sidebar')
    
    # 檢查11：bottom-cta
    if 'bottom-cta' in content:
        issues.append('仍有bottom-cta')
    
    # 檢查12：footer
    if 'class="footer"' not in content:
        issues.append('缺少footer')
    
    # 檢查13：相關文章區塊
    if 'related-articles' in content:
        issues.append('仍有related-articles')
    
    return issues

def fix_article_structure(filepath):
    """修復文章結構以符合標準模板"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # 1. 確保DOCTYPE正確
    if not content.strip().startswith('<!DOCTYPE html>'):
        content = re.sub(r'^.*?(<html|<HTML)', '<!DOCTYPE html>\n\1', content, flags=re.DOTALL)
        fixes.append('修正DOCTYPE')
    
    # 2. 確保html lang="zh-TW"
    content = re.sub(r'<html[^\u003e]*>', '<html lang="zh-TW">', content)
    
    # 3. 確保正確的meta viewport
    if 'width=device-width' not in content[:1000]:
        content = re.sub(
            r'(<meta charset="UTF-8">)',
            r'\1\n    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
            content
        )
        fixes.append('添加viewport')
    
    # 4. 確保CSS連結正確
    if '/static/css/style.css' not in content:
        content = re.sub(
            r'(<title>.*?\u003c/title>)',
            r'\1\n    <link rel="stylesheet" href="/static/css/style.css">',
            content
        )
        fixes.append('添加CSS')
    
    # 5. 移除content-with-sidebar
    if 'content-with-sidebar' in content:
        content = content.replace('content-with-sidebar', '')
        fixes.append('移除content-with-sidebar')
    
    # 6. 確保article class正確
    if '<article class="content"' not in content:
        content = re.sub(r'<article[^\u003e]*>', '<article class="content">', content)
        fixes.append('修正article class')
    
    # 7. 移除sidebar
    if '<aside' in content:
        content = re.sub(r'<aside[^\u003e]*>.*?\u003c/aside>', '', content, flags=re.DOTALL)
        fixes.append('移除sidebar')
    
    # 8. 移除bottom-cta
    if 'bottom-cta' in content:
        content = re.sub(r'<div class="cta-box bottom-cta"[^\u003e]*>.*?\u003c/div>\s*</div>', '', content, flags=re.DOTALL)
        fixes.append('移除bottom-cta')
    
    # 9. 移除related-articles
    if 'related-articles' in content:
        content = re.sub(r'<div class="related-articles"[^\u003e]*>.*?\u003c/div>', '', content, flags=re.DOTALL)
        fixes.append('移除related-articles')
    
    # 10. 清理多餘空白行
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, fixes
    return False, []

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    
    print("🔍 全站模板一致性檢查")
    print("=" * 60)
    print("📋 標準模板：world-cup-2026-guide.html")
    print("=" * 60)
    print()
    
    total = 0
    fixed = 0
    issues_found = 0
    
    for filepath in sorted(articles_dir.glob('*.html')):
        if filepath.name == 'index.html':
            continue
        
        total += 1
        filename = filepath.name
        
        # 檢查問題
        issues = check_article_issues(filepath)
        
        if issues:
            issues_found += 1
            print(f"\n⚠️  {filename}")
            for issue in issues:
                print(f"   - {issue}")
            
            # 嘗試修復
            was_fixed, fixes = fix_article_structure(filepath)
            if was_fixed:
                fixed += 1
                print(f"   ✅ 已修復: {', '.join(fixes)}")
    
    print()
    print("=" * 60)
    print("📊 掃描結果")
    print("=" * 60)
    print(f"總文章數量：{total}")
    print(f"有問題文章：{issues_found}")
    print(f"已修復文章：{fixed}")
    
    # 再次檢查
    if fixed > 0:
        print()
        print("🔍 進行二次檢查...")
        remaining = 0
        for filepath in articles_dir.glob('*.html'):
            if filepath.name == 'index.html':
                continue
            issues = check_article_issues(filepath)
            if issues:
                remaining += 1
                print(f"   ⚠️  {filepath.name}: {len(issues)} 個問題")
        
        if remaining == 0:
            print("   ✅ 所有文章已統一模板！")
        else:
            print(f"   仍有 {remaining} 篇文章需要手動檢查")
    
    print("=" * 60)

if __name__ == '__main__':
    main()
