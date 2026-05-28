#!/bin/bash
# ============================================================
# Fun1399 封面圖自動生成後續腳本
# 用途：檢查最新文章並自動生成封面圖
# 觸發：由 cron 在 auto-draft-trigger.sh 之後 10 分鐘執行
# 或手動執行：bash scripts/auto-cover-trigger.sh
# ============================================================

set -euo pipefail

WORKSPACE="/root/.openclaw/workspace"
DRAFT_DIR="$WORKSPACE/build/articles"
LOG_FILE="$WORKSPACE/build/cover-generation.log"
SCRIPT="$WORKSPACE/scripts/generate_cover.py"

# 檢查是否有新文章
if [[ ! -d "$DRAFT_DIR" ]]; then
    echo "$(date): Draft directory not found. Skip." >> "$LOG_FILE"
    exit 0
fi

# 找到最新的 HTML 檔案
LATEST_HTML=$(ls -t "$DRAFT_DIR"/*.html 2>/dev/null | head -1)
if [[ -z "$LATEST_HTML" ]]; then
    echo "$(date): No HTML drafts found. Skip." >> "$LOG_FILE"
    exit 0
fi

SLUG=$(basename "$LATEST_HTML" .html)
COVER_PATH="$WORKSPACE/build/static/images/articles/${SLUG}.png"

# 如果封面圖已存在，跳過
if [[ -f "$COVER_PATH" ]]; then
    echo "$(date): Cover already exists for $SLUG. Skip." >> "$LOG_FILE"
    exit 0
fi

# 從 HTML 中提取 title
TITLE=$(grep -oP '(?<=<title>).*?(?=</title>)' "$LATEST_HTML" 2>/dev/null || echo "$SLUG")
# 清理 title（移除後綴如 " | Fun1399"）
TITLE=$(echo "$TITLE" | sed 's/ | Fun1399$//;s/ | fun1399$//')

echo "$(date): Generating cover for $SLUG: $TITLE" >> "$LOG_FILE"

# 執行封面圖生成
if python3 "$SCRIPT" "$SLUG" "$TITLE" >> "$LOG_FILE" 2>&1; then
    echo "$(date): Cover generated successfully for $SLUG" >> "$LOG_FILE"
    
    # 通知 Hans（透過 Telegram）
    openclaw message send \
        --channel telegram \
        --to 671592741 \
        --message "🎨 封面圖已自動生成：${SLUG}.png (${TITLE})
儲存：build/static/images/articles/${SLUG}.png
請確認圖片品質後再 deploy。" \
        >> "$LOG_FILE" 2>&1 || true
else
    echo "$(date): Cover generation FAILED for $SLUG" >> "$LOG_FILE"
fi
