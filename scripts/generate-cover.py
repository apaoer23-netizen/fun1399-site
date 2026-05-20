#!/usr/bin/env python3
"""Generate a cover image for the casino fake LINE service article."""
from PIL import Image, ImageDraw, ImageFont
import os

# Canvas: 1280x800
width, height = 1280, 800
img = Image.new('RGB', (width, height), color='#0a0a1a')
draw = ImageDraw.Draw(img)

# Background gradient effect (dark red/black)
for y in range(height):
    ratio = y / height
    r = int(10 + ratio * 30)
    g = int(10 + ratio * 5)
    b = int(26 + ratio * 10)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Draw a warning stripe at top
stripe_height = 8
for i in range(0, width, 40):
    draw.rectangle([i, 0, i+20, stripe_height], fill='#ff4757')

# Draw a big warning icon (triangle with exclamation)
cx, cy = width // 2, 220
triangle_size = 120
points = [
    (cx, cy - triangle_size),
    (cx - triangle_size, cy + triangle_size // 2),
    (cx + triangle_size, cy + triangle_size // 2)
]
draw.polygon(points, fill='#ff4757', outline='#ff6b6b')
# Exclamation mark inside
ex_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
draw.text((cx, cy + 10), "!", fill="#ffffff", font=ex_font, anchor="mm")

# Title text
try:
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 52)
    subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 32)
    tag_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    tag_font = ImageFont.load_default()

# Tag at top
tag_text = "⚠️ 2026最新警示"
draw.rounded_rectangle([width//2 - 160, 80, width//2 + 160, 120], radius=20, fill='#ff4757')
draw.text((width//2, 100), tag_text, fill="#ffffff", font=tag_font, anchor="mm")

# Main title
title_lines = [
    "娛樂城假客服詐騙升級版",
    "LINE官方帳號辨識全攻略"
]
y_offset = 420
for line in title_lines:
    draw.text((width//2, y_offset), line, fill="#ffffff", font=title_font, anchor="mm")
    y_offset += 70

# Subtitle
subtitle = "2026年5月最新詐騙手法解析 · 真假客服一眼看穿"
draw.text((width//2, 560), subtitle, fill="#b0b0b0", font=subtitle_font, anchor="mm")

# Bottom bar with brand
brand_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
draw.rectangle([0, height-50, width, height], fill='#1a1a2e')
draw.text((width//2, height-25), "娛樂城玩家俱樂部 · fun1399.com", fill="#00d4aa", font=brand_font, anchor="mm")

# Save
output_path = "/root/.openclaw/workspace/fun1399-clean/static/images/articles/scam/fake-line-official-account-cover.webp"
img.save(output_path, "WEBP", quality=85)
print(f"Cover image saved to: {output_path}")
