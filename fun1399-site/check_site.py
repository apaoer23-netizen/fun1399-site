#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
網站全面檢查腳本
檢查項目：連結、SEO、延伸閱讀、模板一致性
"""

import os
import re
from pathlib import Path
from datetime import datetime

BUILD_DIR = Path("/root/.openclaw/workspace/fun1399-site/build")
ARTICLES_DIR = BUILD_DIR / "articles"

def check_all_articles():
    """檢查所有文章"""
    results = {
        "total": 0,
        "with_related": 0,
        "without_related": [],
        "broken_links": [],
        "missing_meta": [],
        "template_issues": []
    }
    
    html_files = list(ARTICLES_DIR.glob("*.html"))
    results["total"] = len(html_files)
    
    print(f"檢查 {len(html_files)} 篇文章...")
    
    for html_file in html_files:
        content = html_file.read_text(encoding='utf-8')
        filename = html_file.name
        
        # 檢查延伸閱讀
        if '延伸閱讀' in content or 'related' in content.lower():
            results["with_related"] += 1
        else:
            results["without_related"].append(filename)
        
        # 檢查基本 SEO
        if '<title>' not in content or len(re.findall(r'<title>(.*?)</title>', content)) == 0:
            results["missing_meta"].append(f"{filename}: 缺少 title")
        
        if 'meta name="description"' not in content:
            results["missing_meta"].append(f"{filename}: 缺少 description")
        
        # 檢查 H1
        h1_count = len(re.findall(r'<h1[^>]*>', content))
        if h1_count != 1:
            results["template_issues"].append(f"{filename}: H1 數量為 {h1_count}")
    
    return results

def check_internal_links():
    """檢查內部連結"""
    all_links = set()
    broken_links = []
    
    for html_file in BUILD_DIR.rglob("*.html"):
        content = html_file.read_text(encoding='utf-8')
        # 提取所有 href
        links = re.findall(r'href="([^"]+)"', content)
        for link in links:
            if link.startswith('/') and not link.startswith('//') and not link.startswith('/static/'):
                # 內部連結
                target_path = BUILD_DIR / link.lstrip('/')
                if not target_path.exists() and not link.endswith(('.html', '/')):
                    # 嘗試添加 .html
                    target_path = BUILD_DIR / (link.lstrip('/') + '.html')
                
                if not target_path.exists():
                    broken_links.append(f"{html_file.name} -> {link}")
    
    return broken_links

if __name__ == "__main__":
    print("=" * 60)
    print("網站全面檢查報告")
    print("=" * 60)
    
    # 檢查文章
    results = check_all_articles()
    print(f"\n📄 文章檢查:")
    print(f"  總數: {results['total']}")
    print(f"  有延伸閱讀: {results['with_related']}")
    print(f"  缺少延伸閱讀: {len(results['without_related'])}")
    if results['without_related']:
        for f in results['without_related'][:5]:
            print(f"    - {f}")
    
    # 檢查連結
    print(f"\n🔗 連結檢查:")
    broken = check_internal_links()
    print(f"  可疑連結數: {len(broken)}")
    if broken:
        for b in broken[:10]:
            print(f"    - {b}")
    
    print("\n" + "=" * 60)
