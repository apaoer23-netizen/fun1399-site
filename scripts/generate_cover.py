#!/usr/bin/env python3
"""
Fun1399 封面圖自動生成腳本 (MVP)
用途：呼叫 OpenAI gpt-image-1 API 生成文章封面圖
輸出：build/static/images/articles/<slug>.png (1536x1024)

用法：
    export OPENAI_API_KEY="sk-..."
    python3 scripts/generate_cover.py "3a-casino-investigation-may-2026" "3A娛樂城詐騙爭議整理：玩家評價、出金問題與風險觀察"
"""

import os
import sys
import requests
import json
import base64
from pathlib import Path
from datetime import datetime
from PIL import Image

# === 設定 ===
OUTPUT_DIR = Path("/root/.openclaw/workspace/build/static/images/articles")
DALLE_SIZE = "1536x1024"          # gpt-image-1 支援的橫式尺寸 (3:2)
DALLE_MODEL = "gpt-image-1"       # OpenAI 最新圖片生成模型
OPENAI_API_URL = "https://api.openai.com/v1/images/generations"
WEBP_QUALITY = 80                 # WebP 壓縮品質 (1-100)

# 安全檢查：關鍵字過濾（避免生成違規內容）
BLOCKED_KEYWORDS = ["nude", "sex", "porn", "violence", "gore", "blood"]


def load_api_key() -> str:
    """讀取 OPENAI_API_KEY 環境變數，或從 ~/.openclaw/.openai_api_key 檔案讀取"""
    key = os.environ.get("OPENAI_API_KEY", "").strip()
    if key:
        return key
    
    # 嘗試從檔案讀取
    key_file = Path("/root/.openclaw/.openai_api_key")
    if key_file.exists():
        key = key_file.read_text().strip()
        if key:
            return key
    
    print("[ERROR] OPENAI_API_KEY not set. Please export it or create ~/.openclaw/.openai_api_key", file=sys.stderr)
    sys.exit(1)


def build_prompt(title: str, slug: str) -> str:
    """
    根據文章標題/類型構建 Prompt。
    策略：將中文標題轉換為英文、中性、示意圖風格的描述，
    避免出現品牌 Logo、具體人物、誘導性內容。
    """
    # 簡單關鍵字對應表（可擴充）
    keyword_map = {
        "詐騙": "fraud warning, scam alert, digital security concept",
        "娛樂城": "online casino platform, gaming interface, abstract",
        "出金": "money withdrawal, financial transaction, digital banking",
        "百家樂": "baccarat table, casino game, elegant cards",
        "老虎機": "slot machine, casino game, colorful reels",
        "體育投注": "sports betting, football match, stadium",
        "攻略": "strategy guide, infographic style, clean layout",
        "評價": "review comparison, rating stars, analytical",
        "爭議": "controversy discussion, warning signs, risk concept",
        "黑網": "dark web warning, cybersecurity, shield icon",
        "牌照": "license verification, official certificate, stamp",
        "教學": "tutorial guide, step by step, educational",
        "2026": "modern futuristic, 2026 year, tech style",
    }

    # 嘗試從標題提取關鍵字並映射
    english_concepts = []
    for zh, en in keyword_map.items():
        if zh in title:
            english_concepts.append(en)

    # 預設 fallback
    if not english_concepts:
        english_concepts = ["online entertainment platform, modern digital concept, clean professional design"]

    concepts_str = ", ".join(english_concepts[:3])  # 最多取 3 個概念

    prompt = (
        f"A professional, clean, modern banner illustration for an article about "
        f"'{title}'. "
        f"Style: flat design, minimal, corporate tech blog aesthetic. "
        f"Key visual elements: {concepts_str}. "
        f"No text, no logos, no brand names, no real people faces. "
        f"Color palette: deep blue, orange accent, white background. "
        f"Aspect ratio: 16:9 horizontal banner. "
        f"High quality, web-ready, editorial illustration style."
    )

    return prompt


def generate_image(api_key: str, prompt: str):
    """
    呼叫 OpenAI Image API 生成圖片。
    支援 gpt-image-1 的 b64_json 格式，也向下相容 url 格式。
    回傳: ("url", url) 或 ("base64", b64_string)
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DALLE_MODEL,
        "prompt": prompt,
        "size": DALLE_SIZE,
        "n": 1
    }

    print(f"[INFO] Calling {DALLE_MODEL} API...")
    print(f"[INFO] Prompt: {prompt[:120]}...")

    try:
        resp = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()

        if "data" not in data or len(data["data"]) == 0:
            print(f"[ERROR] API returned empty data: {json.dumps(data)}", file=sys.stderr)
            sys.exit(1)

        image_data = data["data"][0]
        
        # gpt-image-1 回傳 b64_json，dall-e-3 回傳 url
        if "b64_json" in image_data:
            print(f"[INFO] Image generated (base64 format).")
            return ("base64", image_data["b64_json"])
        elif "url" in image_data:
            revised_prompt = image_data.get("revised_prompt", "")
            print(f"[INFO] Image generated (URL format). Revised prompt: {revised_prompt[:100]}...")
            return ("url", image_data["url"])
        else:
            print(f"[ERROR] Unexpected API response format: {list(image_data.keys())}", file=sys.stderr)
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except (KeyError, IndexError) as e:
        print(f"[ERROR] Unexpected API response: {e}", file=sys.stderr)
        sys.exit(1)


def save_image(image_source, output_path: Path) -> None:
    """儲存圖片到指定路徑（支援 URL 或 base64）"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if image_source[0] == "url":
        print(f"[INFO] Downloading image from URL to {output_path}...")
        try:
            resp = requests.get(image_source[1], timeout=60)
            resp.raise_for_status()
            output_path.write_bytes(resp.content)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Download failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:  # base64
        print(f"[INFO] Saving base64 image to {output_path}...")
        image_bytes = base64.b64decode(image_source[1])
        output_path.write_bytes(image_bytes)
    
    size_kb = output_path.stat().st_size / 1024
    print(f"[INFO] Saved {size_kb:.1f} KB → {output_path}")


def compress_to_webp(input_path: Path, output_path: Path, quality: int = 80) -> None:
    """
    將 PNG 圖片壓縮轉換為 WebP 格式。
    大幅減少檔案大小（通常 2MB PNG → 200-400KB WebP）。
    """
    print(f"[INFO] Converting to WebP (quality={quality})...")
    try:
        img = Image.open(input_path)
        # 確保 RGB/RGBA 模式（WebP 不支援某些模式）
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGB")
        
        # 儲存為 WebP
        img.save(output_path, "WEBP", quality=quality, method=6)
        
        original_kb = input_path.stat().st_size / 1024
        webp_kb = output_path.stat().st_size / 1024
        ratio = webp_kb / original_kb * 100
        print(f"[INFO] WebP saved: {webp_kb:.1f} KB (compressed from {original_kb:.1f} KB, {ratio:.1f}%)")
    except Exception as e:
        print(f"[ERROR] WebP conversion failed: {e}", file=sys.stderr)
        # 如果轉換失敗，保留原始 PNG
        import shutil
        shutil.copy2(input_path, output_path.with_suffix(".png"))
        print(f"[WARN] Kept original PNG as fallback.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generate_cover.py <slug> [article_title]", file=sys.stderr)
        print("Example: python3 generate_cover.py '3a-casino-investigation-may-2026' '3A娛樂城詐騙爭議整理'", file=sys.stderr)
        sys.exit(1)

    slug = sys.argv[1].strip()
    title = sys.argv[2].strip() if len(sys.argv) > 2 else slug.replace("-", " ").title()

    # 安全檢查
    if any(kw in title.lower() for kw in BLOCKED_KEYWORDS):
        print(f"[ERROR] Title contains blocked keywords. Abort.", file=sys.stderr)
        sys.exit(1)

    api_key = load_api_key()
    prompt = build_prompt(title, slug)
    image_source = generate_image(api_key, prompt)

    # 輸出格式統一為 .png（暫存），再轉換為 .webp
    temp_png_path = OUTPUT_DIR / f"{slug}.png"
    save_image(image_source, temp_png_path)

    # WebP 壓縮轉換
    webp_path = OUTPUT_DIR / f"{slug}-cover.webp"
    compress_to_webp(temp_png_path, webp_path, quality=WEBP_QUALITY)
    
    # 刪除原始 PNG，釋放空間
    temp_png_path.unlink()
    print(f"[INFO] Removed original PNG: {temp_png_path}")

    # 輸出結果（供上層腳本解析）
    result = {
        "slug": slug,
        "title": title,
        "image_path": str(webp_path),
        "temp_png_removed": str(temp_png_path),
        "size": DALLE_SIZE,
        "timestamp": datetime.now().isoformat()
    }
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
