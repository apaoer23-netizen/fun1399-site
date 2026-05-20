#!/usr/bin/env python3
"""
科技風格封面圖生成器 (Tech/Cyber Style)
未來感、新潮、專業
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

def create_tech_cover(title, subtitle, output_path, accent_color=(0, 255, 255)):
    """
    創建科技風格封面圖
    accent_color: 強調色 (預設青色 cyan)
    """
    # 創建深色科技背景
    width, height = 1200, 630
    img = Image.new('RGB', (width, height), (10, 10, 20))
    draw = ImageDraw.Draw(img)
    
    # 繪製科技線條網格
    # 水平線
    for i in range(0, height, 40):
        alpha = int(30 * (1 - i/height))
        draw.line([(0, i), (width, i)], fill=(0, 255, 255, alpha), width=1)
    
    # 垂直線（透視效果）
    for i in range(0, width, 60):
        draw.line([(i, 0), (i + (i - width//2)//5, height)], fill=(0, 100, 150, 40), width=1)
    
    # 繪製發光邊框
    border_width = 3
    # 外發光
    for i in range(5):
        alpha = 100 - i * 20
        glow_color = (*accent_color, alpha)
        draw.rectangle([i, i, width-1-i, height-1-i], outline=glow_color, width=1)
    
    # 主要邊框
    draw.rectangle([10, 10, width-11, height-11], outline=accent_color, width=2)
    
    # 角落裝飾（科技方塊）
    corner_size = 40
    corners = [
        (15, 15), (width-15-corner_size, 15),
        (15, height-15-corner_size), (width-15-corner_size, height-15-corner_size)
    ]
    for x, y in corners:
        draw.rectangle([x, y, x+corner_size, y+corner_size], fill=accent_color)
        draw.rectangle([x+5, y+5, x+corner_size-5, y+corner_size-5], fill=(10, 10, 20))
    
    # 載入字體
    font_path = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
    font_title = ImageFont.truetype(font_path, 56)
    font_subtitle = ImageFont.truetype(font_path, 32)
    
    # 計算標題位置
    max_width = width - 120
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
    
    # 繪製標題（發光效果）
    line_height = 70
    total_height = len(lines) * line_height + 50
    start_y = (height - total_height) // 2
    
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font_title)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        y = start_y + i * line_height
        
        # 發光效果（多層陰影）
        for offset in range(8, 0, -2):
            glow_alpha = 50 - offset * 5
            glow_color = (*accent_color,)
            draw.text((x+offset, y), line, font=font_title, fill=glow_color)
            draw.text((x-offset, y), line, font=font_title, fill=glow_color)
            draw.text((x, y+offset), line, font=font_title, fill=glow_color)
            draw.text((x, y-offset), line, font=font_title, fill=glow_color)
        
        # 主文字（白色）
        draw.text((x, y), line, font=font_title, fill=(255, 255, 255))
    
    # 繪製副標題
    if subtitle:
        y_sub = start_y + len(lines) * line_height + 20
        bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        
        # 副標題發光
        for offset in range(4, 0, -1):
            draw.text((x+offset, y_sub), subtitle, font=font_subtitle, fill=accent_color)
        draw.text((x, y_sub), subtitle, font=font_subtitle, fill=(255, 255, 255))
    
    # 底部裝飾線
    line_y = height - 80
    draw.line([(width//2 - 100, line_y), (width//2 + 100, line_y)], fill=accent_color, width=2)
    
    # 保存
    img.save(output_path, 'WEBP', quality=90)
    return output_path

if __name__ == "__main__":
    output_dir = "/root/.openclaw/workspace/fun1399-site/build/static/images/articles/tech"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成科技風格封面
    covers = [
        ("MBM娛樂城評價", "詐騙傳聞真相揭密", "mbm-tech.webp", (0, 255, 255)),  # 青色
        ("百家樂攻略", "從入門到精通", "baccarat-tech.webp", (255, 0, 128)),  # 粉紅
        ("詐騙防範指南", "保護你的資金", "scam-tech.webp", (255, 165, 0)),  # 橙色
        ("MLB投注", "棒球賽事分析", "mlb-tech.webp", (0, 255, 128)),  # 綠色
        ("NBA投注", "籃球賽事預測", "nba-tech.webp", (128, 0, 255)),  # 紫色
    ]
    
    for title, subtitle, filename, color in covers:
        output = f"{output_dir}/{filename}"
        create_tech_cover(title, subtitle, output, color)
        print(f"Created tech cover: {output}")
