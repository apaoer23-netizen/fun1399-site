#!/usr/bin/env python3
"""
快速為文章生成帶標題的封面圖
使用現有圖片作為背景
"""

from PIL import Image, ImageDraw, ImageFont
import os
import random

# 現有背景圖選擇
BACKGROUNDS = {
    "casino": "/root/.openclaw/workspace/fun1399-site/build/static/images/baccarat-chips.webp",
    "security": "/root/.openclaw/workspace/fun1399-site/build/static/images/casino-security.webp",
    "sports": "/root/.openclaw/workspace/fun1399-site/build/static/images/sports-betting.webp",
    "warning": "/root/.openclaw/workspace/fun1399-site/build/static/images/warning-shield.webp",
    "basketball": "/root/.openclaw/workspace/fun1399-site/build/static/images/basketball-court.webp",
}

def create_cover(title, subtitle, output_path, bg_type="casino"):
    """創建封面圖"""
    
    # 開啟背景圖
    bg_path = BACKGROUNDS.get(bg_type, BACKGROUNDS["casino"])
    img = Image.open(bg_path).convert('RGBA')
    width, height = img.size
    
    # 創建繪圖層
    draw = ImageDraw.Draw(img)
    
    # 添加半透明黑色遮罩（底部區域）
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, height * 0.5, width, height], fill=(0, 0, 0, 160))
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # 載入中文字體
    font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
    font_title = ImageFont.truetype(font_path, 42)
    font_subtitle = ImageFont.truetype(font_path, 28)
    
    # 標題文字換行
    max_width = width - 60
    lines = []
    current_line = ""
    
    for char in title:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    if current_line:
        lines.append(current_line)
    
    # 計算位置
    line_height = 55
    total_height = len(lines) * line_height + 40  # +40 for subtitle
    start_y = height - 120 - total_height
    
    # 繪製標題
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        y = start_y + i * line_height
        
        # 陰影
        draw.text((x+2, y+2), line, font=font_title, fill=(0, 0, 0, 255))
        # 主文字（金色）
        draw.text((x, y), line, font=font_title, fill=(255, 215, 0, 255))
    
    # 繪製副標題
    if subtitle:
        y_sub = start_y + len(lines) * line_height + 15
        bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        draw.text((x+1, y_sub+1), subtitle, font=font_subtitle, fill=(0, 0, 0, 255))
        draw.text((x, y_sub), subtitle, font=font_subtitle, fill=(255, 255, 255, 255))
    
    # 轉換並保存
    img = img.convert('RGB')
    img.save(output_path, 'WEBP', quality=85)
    
    return output_path

if __name__ == "__main__":
    # 為MBM文章生成封面
    output = "/root/.openclaw/workspace/fun1399-site/build/static/images/articles/mbm-cover.webp"
    create_cover(
        title="MBM娛樂城評價",
        subtitle="詐騙傳聞真相揭密",
        output_path=output,
        bg_type="casino"
    )
    print(f"Created: {output}")
    
    # 為其他文章生成不同封面
    covers = [
        ("百家樂攻略", "從入門到精通", "baccarat-cover.webp", "casino"),
        ("詐騙防範指南", "保護你的資金", "scam-prevention.webp", "warning"),
        ("MLB投注", "棒球賽事分析", "mlb-cover.webp", "sports"),
        ("NBA投注", "籃球賽事預測", "nba-cover.webp", "basketball"),
        ("安全指南", "娛樂城安全", "safety-cover.webp", "security"),
    ]
    
    for title, subtitle, filename, bg in covers:
        output = f"/root/.openclaw/workspace/fun1399-site/build/static/images/articles/{filename}"
        create_cover(title, subtitle, output, bg)
        print(f"Created: {output}")
