#!/bin/bash
# ============================================================
# Fun1399 半自動發文流程觸發腳本
# 用途：週一/三/五自動觸發文章草稿生成
# 流程：
#   1. 檢查今天是星期幾（1=一, 3=三, 5=五）
#   2. 讀取 content plan 決定主題
#   3. 透過 openclaw agent 觸發 AI 生成文章草稿
#   4. 草稿存到 build/articles/
#   5. 發送 Telegram 通知給 Hans 等待確認
# 注意：
#   - 此腳本不自動 deploy
#   - 不自動 push production
#   - 只生成草稿到 build/ 目錄
# ============================================================

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
BUILD_DIR="$WORKSPACE/build"
DRAFT_DIR="$BUILD_DIR/articles"
LOG_FILE="$WORKSPACE/build/draft-generation.log"

# 星期幾（1=一, 3=三, 5=五）
DOW=$(date +%u)

# 只在一三五執行
if [[ "$DOW" != "1" && "$DOW" != "3" && "$DOW" != "5" ]]; then
    echo "$(date): Today is not Mon/Wed/Fri (DOW=$DOW). Skip." >> "$LOG_FILE"
    exit 0
fi

# 讀取 content plan 取得下一篇主題
CONTENT_PLAN="$WORKSPACE/2MONTH-CONTENT-PLAN-May-Jun-2026-v7.md"
if [[ ! -f "$CONTENT_PLAN" ]]; then
    echo "$(date): Content plan not found!" >> "$LOG_FILE"
    exit 1
fi

# 決定文章主題（簡單輪詢：取 content plan 中尚未生成的第一篇）
# 實際主題由 AI agent 根據 content plan 決定

echo "$(date): Triggering draft generation for fun1399..." >> "$LOG_FILE"

# 觸發 openclaw agent 生成文章草稿
# 防呆：記錄生成前 HTML 檔案數量
BEFORE_COUNT=$(ls -1 "$DRAFT_DIR"/*.html 2>/dev/null | wc -l)
echo "$(date): HTML files before generation: $BEFORE_COUNT" >> "$LOG_FILE"

# 同時要求 AI 在文章生成後，自動執行 generate_cover.py 生成封面圖
# --deliver 會將結果發送到 Telegram
openclaw agent \
    --message "[fun1399-auto-draft] Today is $(date +%Y-%m-%d). Please generate a new article draft for fun1399 according to the content plan (2MONTH-CONTENT-PLAN-May-Jun-2026-v7.md). Save the draft HTML to build/articles/ (NOT root articles/). DO NOT deploy. DO NOT push to production.\n\nIMPORTANT: The cover image will be auto-generated as <slug>-cover.webp (NOT .png). Please reference it in the HTML as: /static/images/articles/<slug>-cover.webp\n\nAFTER generating the article, please also run the cover image generation script:\n  python3 scripts/generate_cover.py <article-slug> '<article-title>'\n\nAfter generating, output: 1) Article title, 2) Permalink, 3) Cover image path (.webp), 4) Internal link plan, 5) CTA strategy. Send a summary to Hans for confirmation." \
    --channel telegram \
    --to 671592741 \
    --deliver \
    --thinking high \
    --timeout 1200 \
    >> "$LOG_FILE" 2>&1

AGENT_EXIT_CODE=$?

# 防呆：檢查生成後 HTML 檔案數量是否增加
AFTER_COUNT=$(ls -1 "$DRAFT_DIR"/*.html 2>/dev/null | wc -l)
echo "$(date): HTML files after generation: $AFTER_COUNT" >> "$LOG_FILE"

if [[ "$AFTER_COUNT" -le "$BEFORE_COUNT" ]]; then
    echo "$(date): ❌ ERROR: No new article generated! (Before: $BEFORE_COUNT, After: $AFTER_COUNT)" >> "$LOG_FILE"
    # 發送 Telegram 錯誤通知
    openclaw message send \
        --channel telegram \
        --to 671592741 \
        --message "❌ $(date +%Y-%m-%d) 文章生成失敗：未產出新檔案\n請檢查 openclaw agent 狀態或手動補發。" \
        >> "$LOG_FILE" 2>&1 || true
    exit 1
fi

echo "$(date): ✅ Draft generation confirmed: new article created ($BEFORE_COUNT → $AFTER_COUNT)." >> "$LOG_FILE"
