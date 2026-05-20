#!/usr/bin/env python3
"""
全站CTA連結修復腳本
根據頁面中的平台名稱，將CTA按鈕連結替換為對應平台的正確連結
"""

import json
import re
import os
from pathlib import Path

# 讀取平台連結配置
with open('/root/.openclaw/workspace/fun1399-site/platform_links.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

platforms = config['platforms']

# 建立平台名稱到URL的映射
platform_map = {}
for key, data in platforms.items():
    platform_map[data['name']] = data['url']
    for alias in data['aliases']:
        platform_map[alias] = data['url']

# 定義CTA按鈕文字模式
cta_patterns = [
    r'立即註冊',
    r'立即遊玩',
    r'立即領取',
    r'前往平台',
    r'查看優惠',
    r'立即體驗',
    r'開始遊戲',
    r'前往註冊',
]

# 統計資訊
stats = {
    'fixed_pages': 0,
    'fixed_ctas': 0,
    'details': []
}

def detect_platforms_in_content(content):
    """檢測內容中包含哪些平台"""
    detected = {}
    for key, data in platforms.items():
        # 檢查主要名稱
        if data['name'] in content:
            detected[data['name']] = data['url']
        # 檢查別名（確保是完整匹配）
        for alias in data['aliases']:
            # 使用正則確保是完整單詞匹配
            pattern = r'\b' + re.escape(alias) + r'\b'
            if re.search(pattern, content):
                detected[data['name']] = data['url']
                break
    return detected

def fix_cta_links_in_file(filepath, content, detected_platforms):
    """修復檔案中的CTA連結"""
    original_content = content
    fixed_count = 0
    
    # 對於每個檢測到的平台，修復其附近的CTA
    for platform_name, url in detected_platforms.items():
        # 找到平台名稱的位置
        platform_pattern = re.escape(platform_name)
        
        # 方法1: 在平台名稱附近查找CTA按鈕
        # 尋找平台名稱後面的CTA按鈕
        pattern = rf'({re.escape(platform_name)}.*?)(href="https://[^"]*")([^>]*>)({"|".join(cta_patterns)})'
        
        matches = list(re.finditer(pattern, content, re.DOTALL | re.IGNORECASE))
        for match in matches:
            old_href = match.group(2)
            if old_href != f'href="{url}"':
                # 替換連結
                new_text = match.group(1) + f'href="{url}"' + match.group(3) + match.group(4)
                content = content[:match.start()] + new_text + content[match.end():]
                fixed_count += 1
    
    # 方法2: 處理 recommend/2026.html 這種列表頁面
    # 尋找 casino-item 區塊，根據平台名稱設置正確連結
    if 'casino-item' in content:
        for key, data in platforms.items():
            platform_name = data['name']
            url = data['url']
            
            # 在 casino-item 區塊中尋找該平台
            # 匹配模式：<h3>平台名稱</h3>...<a href="...">立即註冊</a>
            pattern = rf'(<h3>{re.escape(platform_name)}</h3>.*?)(href="https://[^"]*")([^>]*class="btn[^"]*"[^>]*>)({"|".join(cta_patterns)})'
            
            matches = list(re.finditer(pattern, content, re.DOTALL | re.IGNORECASE))
            for match in matches:
                old_href = match.group(2)
                if url not in old_href:
                    new_text = match.group(1) + f'href="{url}" target="_blank" rel="noopener"' + match.group(3) + match.group(4)
                    content = content[:match.start()] + new_text + content[match.end():]
                    fixed_count += 1
    
    # 方法3: 處理 promotions 頁面
    # 根據優惠卡片的平台名稱設置連結
    if 'promo-card' in content or 'promotion-item' in content:
        for key, data in platforms.items():
            platform_name = data['name']
            url = data['url']
            
            # 尋找包含平台名稱的優惠卡片
            pattern = rf'({re.escape(platform_name)}.*?)(href="https://[^"]*")([^>]*>)({"|".join(cta_patterns)})'
            
            matches = list(re.finditer(pattern, content, re.DOTALL | re.IGNORECASE))
            for match in matches:
                old_href = match.group(2)
                if url not in old_href:
                    new_text = match.group(1) + f'href="{url}" target="_blank" rel="noopener"' + match.group(3) + match.group(4)
                    content = content[:match.start()] + new_text + content[match.end():]
                    fixed_count += 1
    
    # 方法4: 處理 reviews 頁面
    # 單一平台評測頁，整頁的CTA都應該指向該平台
    if '/reviews/' in str(filepath):
        for key, data in platforms.items():
            if key in str(filepath).lower() or data['name'].lower().replace('娛樂城', '') in str(filepath).lower():
                # 這是該平台的評測頁，替換所有CTA
                url = data['url']
                
                # 替換所有CTA按鈕（不在header和footer中的）
                for cta in cta_patterns:
                    pattern = rf'(href="https://[^"]*")([^>]*>)({cta})'
                    
                    def replace_if_not_correct(match):
                        nonlocal fixed_count
                        old_href = match.group(1)
                        if url not in old_href:
                            fixed_count += 1
                            return f'href="{url}" target="_blank" rel="noopener"' + match.group(2) + match.group(3)
                        return match.group(0)
                    
                    content = re.sub(pattern, replace_if_not_correct, content)
                break
    
    return content, fixed_count

def main():
    build_dir = Path('/root/.openclaw/workspace/fun1399-site/build')
    html_files = list(build_dir.rglob('*.html'))
    
    print(f"🔍 掃描 {len(html_files)} 個HTML檔案...")
    print()
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 檢測頁面中的平台
            detected_platforms = detect_platforms_in_content(content)
            
            if not detected_platforms:
                continue
            
            # 修復CTA連結
            new_content, fixed_count = fix_cta_links_in_file(filepath, content, detected_platforms)
            
            if fixed_count > 0:
                # 寫回檔案
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                stats['fixed_pages'] += 1
                stats['fixed_ctas'] += fixed_count
                stats['details'].append({
                    'file': str(filepath.relative_to(build_dir)),
                    'platforms': list(detected_platforms.keys()),
                    'fixed_ctas': fixed_count
                })
                
                print(f"✅ {filepath.name}: 修復 {fixed_count} 個CTA ({', '.join(detected_platforms.keys())})")
        
        except Exception as e:
            print(f"❌ {filepath.name}: 處理失敗 - {e}")
    
    # 輸出統計
    print()
    print("=" * 50)
    print("📊 修復報告")
    print("=" * 50)
    print(f"修復頁面數: {stats['fixed_pages']}")
    print(f"修復CTA數: {stats['fixed_ctas']}")
    print()
    print("詳細修復列表:")
    for detail in stats['details']:
        print(f"  - {detail['file']}: {detail['fixed_ctas']} 個CTA")
    
    # 保存統計到JSON
    with open('/root/.openclaw/workspace/fun1399-site/fix_stats.json', 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
