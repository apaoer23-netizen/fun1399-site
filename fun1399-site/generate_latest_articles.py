#!/usr/bin/env python3
"""
自動生成首頁最新文章列表
從 articles 目錄讀取文章，依修改時間排序，生成 HTML 區塊
"""

import os
import re
from pathlib import Path
from datetime import datetime

def extract_article_info(filepath):
    """從文章檔案提取標題、描述、日期"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取標題 (優先從 <title>，其次 <h1>)
        title_match = re.search(r'<title>(.*?)(?:\s*-\s*娛樂城玩家俱樂部)?</title>', content)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
            title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else filepath.stem
        
        # 提取 description
        desc_match = re.search(r'<meta[^>]*name="description"[^>]*content="([^"]*)"', content)
        description = desc_match.group(1) if desc_match else title[:50] + "..."
        
        # 限制描述長度
        if len(description) > 80:
            description = description[:77] + "..."
        
        # 獲取檔案修改時間
        mtime = os.path.getmtime(filepath)
        
        return {
            'filename': filepath.name,
            'title': title,
            'description': description,
            'mtime': mtime,
            'date': datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
        }
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def generate_latest_articles_html(articles_dir, count=6):
    """生成最新文章 HTML"""
    articles_path = Path(articles_dir)
    
    # 收集所有文章資訊
    articles = []
    for html_file in articles_path.glob('*.html'):
        info = extract_article_info(html_file)
        if info:
            articles.append(info)
    
    # 依修改時間排序（新→舊）
    articles.sort(key=lambda x: x['mtime'], reverse=True)
    
    # 取前 N 篇
    latest = articles[:count]
    
    # 生成 HTML
    html_cards = []
    for article in latest:
        card = f'''                <article class="article-card">
                    <h3><a href="/articles/{article['filename']}">{article['title']}</a></h3>
                    <p>{article['description']}</p>
                    <a href="/articles/{article['filename']}" class="read-more">閱讀全文 →</a>
                </article>'''
        html_cards.append(card)
    
    return '\n'.join(html_cards), latest

def update_index_html(index_path, articles_dir, count=6):
    """更新首頁 HTML"""
    index_file = Path(index_path)
    
    # 讀取現有 index.html
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成最新文章 HTML
    new_articles_html, articles_list = generate_latest_articles_html(articles_dir, count)
    
    # 替換 <!-- Latest Articles --> 區塊
    pattern = r'(<!-- Latest Articles -->\s*<section class="latest-articles">\s*<div class="container">\s*<h2>📚 最新攻略文章</h2>\s*<div class="article-grid">)(.*?)(</div>\s*</div>\s*</section>)'
    
    replacement = r'\1\n' + new_articles_html + r'\n            \3'
    
    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # 如果沒有匹配到，嘗試另一種模式
    if new_content == content:
        pattern2 = r'(<section class="latest-articles">.*?<h2>📚 最新攻略文章</h2>.*?<div class="article-grid">)(.*?)(</div>\s*</div>\s*</section>)'
        replacement2 = r'\1\n' + new_articles_html + r'\n            \3'
        new_content = re.sub(pattern2, replacement2, content, flags=re.DOTALL)
    
    # 寫回檔案
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return articles_list

if __name__ == '__main__':
    # 設定路徑
    base_dir = Path('/root/.openclaw/workspace/fun1399-site/fun1399-fixed')
    index_path = base_dir / 'index.html'
    articles_dir = base_dir / 'articles'
    
    print("🔧 自動生成首頁最新文章列表...")
    print("=" * 60)
    
    # 更新首頁
    articles = update_index_html(index_path, articles_dir, count=6)
    
    print(f"✅ 已更新 {index_path}")
    print(f"✅ 顯示最新 {len(articles)} 篇文章")
    print()
    print("📊 文章列表（依修改時間排序）：")
    print("-" * 60)
    for i, article in enumerate(articles, 1):
        print(f"{i}. {article['date']} - {article['title'][:40]}...")
    print("=" * 60)
