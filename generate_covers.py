#!/usr/bin/env python3
"""
批量生成科技風格封面圖
"""
import os
import re
import random
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import html

# 配色方案（循環使用）
ACCENT_COLORS = [
    (0, 255, 255),     # 青色 (Cyan)
    (255, 0, 128),     # 粉紅 (Pink)
    (255, 165, 0),     # 橙色 (Orange)
    (0, 255, 128),     # 綠色 (Mint)
    (128, 0, 255),     # 紫色 (Purple)
    (255, 255, 0),     # 黃色 (Yellow)
    (0, 191, 255),     # 深藍 (Deep Blue)
    (255, 69, 0),      # 紅橙 (Red-Orange)
    (50, 205, 50),     # 萊姆綠 (Lime)
    (238, 130, 238),   # 紫紅 (Violet)
]

def extract_article_info(file_path):
    """從HTML文件中提取標題和副標題"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取標題
    title = None
    subtitle = None
    
    # 嘗試從 h1 提取
    h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL | re.IGNORECASE)
    if h1_match:
        # 清理HTML標籤
        title_text = re.sub(r'<[^>]+>', '', h1_match.group(1))
        title = html.unescape(title_text.strip())
    
    # 如果沒有h1，嘗試從 title 標籤提取
    if not title:
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL | re.IGNORECASE)
        if title_match:
            title = html.unescape(title_match.group(1).strip())
            # 移除站點名稱
            title = re.sub(r'\s*[-|]\s*FUN.*$', '', title, flags=re.IGNORECASE)
    
    # 嘗試從 meta description 提取副標題
    desc_match = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', content, re.IGNORECASE)
    if desc_match:
        subtitle = html.unescape(desc_match.group(1).strip())
        # 限制長度
        if len(subtitle) > 60:
            subtitle = subtitle[:57] + '...'
    
    # 如果沒有副標題，嘗試從 h2 提取
    if not subtitle:
        h2_match = re.search(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL | re.IGNORECASE)
        if h2_match:
            subtitle_text = re.sub(r'<[^>]+>', '', h2_match.group(1))
            subtitle = html.unescape(subtitle_text.strip())
            if len(subtitle) > 60:
                subtitle = subtitle[:57] + '...'
    
    # 預設副標題
    if not subtitle:
        subtitle = "專業分析與實用指南"
    
    return title, subtitle

def create_tech_cover(title, subtitle, output_path, accent_color):
    """生成科技風格封面圖"""
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    
    # 網格線（隨機間距增加變化）
    grid_spacing = random.choice([30, 35, 40, 45, 50])
    for i in range(0, height, grid_spacing):
        alpha = min(40, int(30 * (1 - i/height)))
        line_color = (max(0, accent_color[0]//4), max(0, accent_color[1]//4), max(0, accent_color[2]//4))
        draw.line([(0, i), (width, i)], fill=line_color, width=1)
    
    for i in range(0, width, grid_spacing + 20):
        offset = (i - width//2) // random.randint(4, 8)
        line_color = (max(0, accent_color[0]//5), max(0, accent_color[1]//5), max(0, accent_color[2]//5))
        draw.line([(i, 0), (i + offset, height)], fill=line_color, width=1)
    
    # 發光邊框
    for i in range(4):
        glow_intensity = 80 - i * 20
        glow_color = tuple(min(255, c + glow_intensity) for c in accent_color)
        draw.rectangle([i, i, width-1-i, height-1-i], outline=glow_color, width=1)
    draw.rectangle([8, 8, width-9, height-9], outline=accent_color, width=2)
    
    # 角落裝飾
    corner_size = random.choice([30, 35, 40])
    corners = [(10, 10), (width-10-corner_size, 10), (10, height-10-corner_size), (width-10-corner_size, height-10-corner_size)]
    for x, y in corners:
        draw.rectangle([x, y, x+corner_size, y+corner_size], fill=accent_color)
        inner = corner_size // 3
        draw.rectangle([x+inner, y+inner, x+corner_size-inner, y+corner_size-inner], fill=(10, 10, 20))
    
    # 字體
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    ]
    
    font_path = None
    for fp in font_paths:
        if os.path.exists(fp):
            font_path = fp
            break
    
    if not font_path:
        raise RuntimeError("找不到中文字體")
    
    font_title = ImageFont.truetype(font_path, 52)
    font_subtitle = ImageFont.truetype(font_path, 30)
    
    # 標題換行
    max_width = width - 100
    lines = []
    current = ""
    for char in title:
        test = current + char
        bbox = draw.textbbox((0,0), test, font=font_title)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = char
    if current:
        lines.append(current)
    
    # 限制行數最多3行
    if len(lines) > 3:
        lines = lines[:2]
        lines[1] = lines[1][:15] + "..."
    
    # 繪製標題
    line_height = 65
    start_y = (height - len(lines) * line_height - 80) // 2
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=font_title)
        x = (width - (bbox[2]-bbox[0])) / 2
        y = start_y + i * line_height
        # 發光效果
        for offset in range(6, 0, -2):
            glow_col = tuple(max(0, min(255, c - offset * 20)) for c in accent_color)
            draw.text((x+offset, y+offset), line, font=font_title, fill=glow_col)
        draw.text((x, y), line, font=font_title, fill=(255, 255, 255))
    
    # 副標題
    if subtitle:
        y = start_y + len(lines) * line_height + 30
        bbox = draw.textbbox((0,0), subtitle, font=font_subtitle)
        x = (width - (bbox[2]-bbox[0])) / 2
        # 發光效果
        for offset in range(3, 0, -1):
            glow_col = tuple(max(0, min(255, c - offset * 30)) for c in accent_color)
            draw.text((x+offset, y+offset), subtitle, font=font_subtitle, fill=glow_col)
        draw.text((x, y), subtitle, font=font_subtitle, fill=(255, 255, 255))
    
    # 底部裝飾線
    line_y = height - 60
    draw.line([(width//2 - 80, line_y), (width//2 + 80, line_y)], fill=accent_color, width=2)
    
    # 保存
    img.save(output_path, 'WEBP', quality=90)
    return output_path

def update_article_image(html_path, image_path, title):
    """更新HTML文件中的圖片引用"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找並替換 hero image
    # 模式1: article-hero-image div
    pattern1 = r'(<div class="article-hero-image"[^>]*>.*?<img[^>]*src=")([^"]+)("[^>]*alt=")([^"]*)(")'
    replacement1 = r'\1' + image_path + r'\3' + title + r'\5'
    
    new_content = re.sub(pattern1, replacement1, content, flags=re.DOTALL)
    
    # 模式2: 直接替換圖片路徑
    if new_content == content:
        # 嘗試找到任何 img 標籤在 hero 區域
        pattern2 = r'(<div[^>]*class="[^"]*hero[^"]*"[^>]*>.*?<img[^>]*src=")([^"]+)(")'
        new_content = re.sub(pattern2, r'\1' + image_path + r'\3', content, flags=re.DOTALL)
    
    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    articles_dir = Path('/root/.openclaw/workspace/fun1399-site/build/articles')
    images_dir = Path('/root/.openclaw/workspace/fun1399-site/build/static/images/articles/tech')
    
    # 確保輸出目錄存在
    images_dir.mkdir(parents=True, exist_ok=True)
    
    # 獲取所有HTML文件
    html_files = sorted([f for f in articles_dir.glob('*.html') if f.name != 'index.html'])
    
    print(f"找到 {len(html_files)} 篇文章")
    print("=" * 60)
    
    results = []
    
    for idx, html_file in enumerate(html_files):
        filename = html_file.stem
        color_idx = idx % len(ACCENT_COLORS)
        accent_color = ACCENT_COLORS[color_idx]
        color_name = ['青色', '粉紅', '橙色', '綠色', '紫色', '黃色', '深藍', '紅橙', '萊姆綠', '紫紅'][color_idx]
        
        # 提取文章信息
        title, subtitle = extract_article_info(html_file)
        
        if not title:
            title = filename.replace('-', ' ').title()
        
        print(f"[{idx+1}/{len(html_files)}] {filename}")
        print(f"    標題: {title}")
        print(f"    副標: {subtitle}")
        print(f"    配色: {color_name} {accent_color}")
        
        # 生成封面圖
        output_path = images_dir / f"{filename}-cover.webp"
        try:
            create_tech_cover(title, subtitle, str(output_path), accent_color)
            print(f"    封面: ✓ {output_path}")
            
            # 更新HTML引用
            image_rel_path = f"/static/images/articles/tech/{filename}-cover.webp"
            updated = update_article_image(html_file, image_rel_path, title)
            print(f"    引用: {'✓ 已更新' if updated else '- 無需更新'}")
            
            results.append({
                'filename': filename,
                'title': title,
                'subtitle': subtitle,
                'color_name': color_name,
                'color': accent_color,
                'image_path': str(output_path),
                'updated': updated
            })
        except Exception as e:
            print(f"    錯誤: ✗ {e}")
            results.append({
                'filename': filename,
                'title': title,
                'error': str(e)
            })
        
        print()
    
    # 輸出摘要
    print("=" * 60)
    print("生成完成！")
    print(f"總共: {len(results)} 篇文章")
    print(f"成功: {len([r for r in results if 'error' not in r])}")
    print(f"失敗: {len([r for r in results if 'error' in r])}")
    
    return results

if __name__ == '__main__':
    main()
