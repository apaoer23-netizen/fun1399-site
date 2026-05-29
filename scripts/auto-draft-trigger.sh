#!/bin/bash
# ============================================================
# Fun1399 半自動發文流程觸發腳本 (v3 - sessions_send + Retry)
# 用途：週一/三/五自動觸發文章草稿生成
# 流程：
#   1. 檢查今天是星期幾（1=一, 3=三, 5=五）
#   2. 透過 openclaw agent 觸發 AI 生成文章草稿
#   3. 草稿存到 build/articles/
#   4. 重試機制：最多 3 次，每次檢查檔案數量
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
MAX_RETRIES=3
RETRY_DELAY=60

# 星期幾（1=一, 3=三, 5=五）
DOW=$(date +%u)

# 只在一三五執行
if [[ "$DOW" != "1" && "$DOW" != "3" && "$DOW" != "5" ]]; then
    echo "$(date): Today is not Mon/Wed/Fri (DOW=$DOW). Skip." >> "$LOG_FILE"
    exit 0
fi

# 讀取 content plan 確認存在
CONTENT_PLAN="$WORKSPACE/2MONTH-CONTENT-PLAN-May-Jun-2026-v7.md"
if [[ ! -f "$CONTENT_PLAN" ]]; then
    echo "$(date): Content plan not found!" >> "$LOG_FILE"
    exit 1
fi

echo "$(date): ==================================================" >> "$LOG_FILE"
echo "$(date): Triggering draft generation for fun1399..." >> "$LOG_FILE"
echo "$(date): ==================================================" >> "$LOG_FILE"

# 記錄初始檔案數量
BEFORE_COUNT=$(ls -1 "$DRAFT_DIR"/*.html 2>/dev/null | wc -l)
echo "$(date): HTML files before generation: $BEFORE_COUNT" >> "$LOG_FILE"

# 重試迴圈
ATTEMPT=1
SUCCESS=false

while [[ $ATTEMPT -le $MAX_RETRIES ]]; do
    echo "$(date): --- Attempt $ATTEMPT / $MAX_RETRIES ---" >> "$LOG_FILE"

    # 觸發 openclaw agent 生成文章草稿
    # 使用 --agent main 指定主 agent，避免 "choose a session" 錯誤
    # --deliver 會將結果發送到 Telegram
    set +e
    openclaw agent \
        --agent main \
        --message "[fun1399-auto-draft] Today is $(date +%Y-%m-%d). Please generate a new article draft for fun1399 according to the content plan (2MONTH-CONTENT-PLAN-May-Jun-2026-v7.md). Save the draft HTML to build/articles/ (NOT root articles/). DO NOT deploy. DO NOT push to production.\n\nIMPORTANT: The cover image will be auto-generated as <slug>-cover.webp (NOT .png). Please reference it in the HTML as: /static/images/articles/<slug>-cover.webp\n\nAFTER generating the article, please also run the cover image generation script:\n  python3 scripts/generate_cover.py <article-slug> '<article-title>'\n\nAfter generating, output: 1) Article title, 2) Permalink, 3) Cover image path (.webp), 4) Internal link plan, 5) CTA strategy. Send a summary to Hans for confirmation." \
        --channel telegram \
        --to 671592741 \
        --deliver \
        --thinking high \
        --timeout 1200 \
        >> "$LOG_FILE" 2>&1
    AGENT_EXIT_CODE=$?
    set -e

    echo "$(date): Agent exit code: $AGENT_EXIT_CODE" >> "$LOG_FILE"

    # 檢查檔案數量是否增加
    AFTER_COUNT=$(ls -1 "$DRAFT_DIR"/*.html 2>/dev/null | wc -l)
    echo "$(date): HTML files after attempt $ATTEMPT: $AFTER_COUNT" >> "$LOG_FILE"

    if [[ "$AFTER_COUNT" -gt "$BEFORE_COUNT" ]]; then
        echo "$(date): ✅ SUCCESS: New article detected ($BEFORE_COUNT → $AFTER_COUNT)" >> "$LOG_FILE"
        SUCCESS=true
        break
    fi

    # 也檢查是否有檔案在最近 10 分鐘內被修改（防止覆寫而非新增）
    RECENT_MODIFIED=$(find "$DRAFT_DIR" -name "*.html" -mmin -10 2>/dev/null | wc -l)
    if [[ "$RECENT_MODIFIED" -gt 0 ]]; then
        echo "$(date): ✅ SUCCESS: Recent file modification detected ($RECENT_MODIFIED files modified in last 10 min)" >> "$LOG_FILE"
        SUCCESS=true
        break
    fi

    if [[ $ATTEMPT -lt $MAX_RETRIES ]]; then
        echo "$(date): ⚠️ No new article. Waiting ${RETRY_DELAY}s before retry..." >> "$LOG_FILE"
        sleep $RETRY_DELAY
    fi

    ATTEMPT=$((ATTEMPT + 1))
done

if [[ "$SUCCESS" == "true" ]]; then
    echo "$(date): ✅ Draft generation confirmed after $((ATTEMPT)) attempt(s)." >> "$LOG_FILE"
    exit 0
else
    echo "$(date): ❌ FAILED: All $MAX_RETRIES attempts exhausted. No new article generated." >> "$LOG_FILE"
    # 發送 Telegram 錯誤通知
    set +e
    openclaw message send \
        --channel telegram \
        --to 671592741 \
        --message "❌ $(date +%Y-%m-%d) 文章生成失敗：${MAX_RETRIES} 次重試皆未產出新檔案\n請檢查 openclaw agent 狀態或手動補發。\nLog: $LOG_FILE" \
        >> "$LOG_FILE" 2>&1 || true
    set -e
    exit 1
fi
