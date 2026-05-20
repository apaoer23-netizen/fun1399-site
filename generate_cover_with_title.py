#!/usr/bin/env python3
"""
生成帶標題文字的AI封面圖
工作流程：
1. 使用Gemini生成背景圖
2. 使用PIL添加標題文字
3. 輸出WebP格式
"""

import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generate_background(prompt, output_path, api_key):
    """使用Gemini生成背景圖"""
    script_path = os.path.expanduser("~/.openclaw/workspace/skills/nano-banana-pro/scripts/generate_image.py")
    
    cmd = [
        "uv", "run", script_path,
        "--prompt", prompt,
        "--filename", output_path,
        "--resolution", "1K"
    ]
    
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = api_key
    
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    
    if result.returncode != 0:
        print(f"Error generating image: {result.stderr}")
        return False
    
    return True

def add_title_to_image(image_path, title, output_path):
    """在圖片上添加標題文字"""
    # 開啟圖片
    img = Image.open(image_path)
    width, height = img.size
    
    # 轉換為RGBA模式（支援透明）
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    
    # 創建繪圖層
    draw = ImageDraw.Draw(img)
    
    # 添加半透明黑色遮罩（底部）
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle([0, height * 0.6, width, height], fill=(0, 0, 0, 180))
    
    # 合併遮罩
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)
    
    # 嘗試載入中文字體
    font_paths = [
        "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/noto-cjk/NotoSansCJK-Bold.ttc",
        "/System/Library/Fonts/PingFang.ttc",  # macOS
        "C:/Windows/Fonts/msjhbd.ttc",  # Windows
    ]
    
    font = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, 48)
                break
            except:
                continue
    
    if font is None:
        # 使用預設字體
        font = ImageFont.load_default()
        print("Warning: Using default font, Chinese characters may not display correctly")
    
    # 文字換行處理
    max_width = width - 80
    lines = []
    words = title
    current_line = ""
    
    for char in words:
        test_line = current_line + char
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char
    
    if current_line:
        lines.append(current_line)
    
    # 計算文字位置（置中）
    line_height = 60
    total_text_height = len(lines) * line_height
    start_y = height - 150 - (total_text_height / 2)
    
    # 繪製文字（白色，帶陰影）
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (width - text_width) / 2
        y = start_y + i * line_height
        
        # 陰影
        draw.text((x+2, y+2), line, font=font, fill=(0, 0, 0, 255))
        # 主文字
        draw.text((x, y), line, font=font, fill=(255, 255, 255, 255))
    
    # 轉換為RGB並保存
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # 保存為WebP
    webp_path = output_path.replace('.png', '.webp')
    img.save(webp_path, 'WEBP', quality=85)
    
    # 刪除原始PNG
    if os.path.exists(image_path):
        os.remove(image_path)
    
    return webp_path

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        sys.exit(1)
    
    # 測試生成MBM文章封面
    title = "MBM娛樂城評價"
    subtitle = "詐騙傳聞真相揭密"
    
    # 生成背景圖
    temp_path = "/tmp/mbm-bg.png"
    prompt = "A professional luxury casino scene with golden chips and playing cards on a dark elegant background, premium gambling atmosphere, Taiwan style, high-end casino review concept"
    
    print("Generating background image...")
    if not generate_background(prompt, temp_path, api_key):
        print("Failed to generate background")
        sys.exit(1)
    
    # 添加文字
    output_path = "/root/.openclaw/workspace/fun1399-site/build/static/images/articles/mbm-cover.webp"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print("Adding title text...")
    final_path = add_title_to_image(temp_path, title + "\n" + subtitle, output_path)
    
    print(f"Cover image saved: {final_path}")

if __name__ == "__main__":
    main()
