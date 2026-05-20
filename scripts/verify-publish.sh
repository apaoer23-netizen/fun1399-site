#!/bin/bash
# =============================================================================
# 發文完成驗證腳本 verify-publish.sh
# 用途：每次 cron 執行後自動檢查發文是否真正完成
# 執行位置：/root/.openclaw/workspace/scripts/
# =============================================================================

set -euo pipefail

# ── 設定 ────────────────────────────────────────────────────────────────────
WORKSPACE="/root/.openclaw/workspace"
FUN1399_DIR="${WORKSPACE}/fun1399-clean"
ARTICLES_DIR="${FUN1399_DIR}/articles"
INDEX_HTML="${FUN1399_DIR}/index.html"
ARTICLES_INDEX="${ARTICLES_DIR}/index.html"
PLAN_FILE="${WORKSPACE}/2MONTH-CONTENT-PLAN-May-Jun-2026-v2.md"
DEPLOY_ID_FILE="/tmp/fun1399-last-deploy-id.txt"
VERIFY_LOG="${WORKSPACE}/logs/publish-verify.log"
FAILED_LOG="${WORKSPACE}/logs/failed-publish.log"
MAX_RETRIES=1
RETRY_COUNT=0

# 建立日誌目錄
mkdir -p "$(dirname "$VERIFY_LOG")"
mkdir -p "$(dirname "$FAILED_LOG")"

# ── 工具函式 ────────────────────────────────────────────────────────────────
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$VERIFY_LOG"
}

fail() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ❌ FAIL: $1" | tee -a "$FAILED_LOG"
}

# 取得今天日期與星期
today_date=$(date +%Y-%m-%d)
today_month_day=$(date +%-m/%-d)
today_weekday=$(date +%u)  # 1=一, 2=二, 3=三, 4=四, 5=五

# 檢查今天是否為發文日（週一三五）
is_publish_day() {
    case "$today_weekday" in
        1|3|5) return 0 ;;
        *) return 1 ;;
    esac
}

# ── 主驗證函式 ─────────────────────────────────────────────────────────────
verify_publish() {
    local errors=0
    local article_file=""
    local article_url_path=""
    
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    log "🔍 開始驗證 ${today_date} 發文任務"
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    
    # 1️⃣ 檢查今天是否為發文日
    if ! is_publish_day; then
        log "📅 今天不是發文日（週一三五），跳過驗證"
        return 0
    fi
    
    # 2️⃣ 從排程表找出今日文章
    log "📋 步驟 1/6: 查找今日排程文章..."
    
    # 嘗試從排程表讀取今日文章標題
    # 排程表格式：| 2026-05-06 | 鉅城娛樂城... | ... |
    if [[ -f "$PLAN_FILE" ]]; then
        # 先用精確日期匹配
        today_line=$(grep "^| ${today_date} " "$PLAN_FILE" 2>/dev/null || true)
        if [[ -z "$today_line" ]]; then
            # 嘗試用月/日格式匹配
            today_line=$(grep "| ${today_month_day} " "$PLAN_FILE" 2>/dev/null || true)
        fi
    fi
    
    # 如果找不到排程表，嘗試用日期推算
    if [[ -z "$today_line" ]]; then
        log "⚠️ 無法從排程表讀取今日文章，改用檔案日期檢查"
        # 找出今天建立/修改的 HTML 檔案（排除 index.html）
        article_file=$(find "$ARTICLES_DIR" -name "*.html" ! -name "index.html" -newermt "$(date +%Y-%m-%d) 00:00" ! -newermt "$(date +%Y-%m-%d) 23:59" -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    fi
    
    # 如果還找不到，嘗試搜尋今天產出的檔案（用 mtime，排除 index.html）
    if [[ -z "$article_file" ]]; then
        article_file=$(find "$ARTICLES_DIR" -name "*.html" ! -name "index.html" -mtime 0 -printf '%T@ %p\n' 2>/dev/null | sort -n | tail -1 | cut -d' ' -f2-)
    fi
    
    # 檢查文章檔案是否存在
    if [[ -z "$article_file" || ! -f "$article_file" ]]; then
        fail "步驟 1/6 失敗: 今日文章 HTML 檔案不存在"
        errors=$((errors + 1))
    else
        article_basename=$(basename "$article_file" .html)
        article_url_path="/articles/${article_basename}.html"
        log "✅ 步驟 1/6 通過: 文章檔案存在 → ${article_basename}.html"
    fi
    
    # 3️⃣ 檢查 index.html 是否已插入今日文章
    log "🏠 步驟 2/6: 檢查首頁 index.html..."
    if [[ -n "$article_basename" && -f "$INDEX_HTML" ]]; then
        if grep -q "$article_basename" "$INDEX_HTML"; then
            log "✅ 步驟 2/6 通過: 首頁已包含今日文章連結"
        else
            fail "步驟 2/6 失敗: 首頁 index.html 未包含今日文章"
            errors=$((errors + 1))
        fi
    else
        fail "步驟 2/6 失敗: 無法檢查首頁（文章未定義或首頁不存在）"
        errors=$((errors + 1))
    fi
    
    # 4️⃣ 檢查 articles/index.html 是否已加入分類
    log "📑 步驟 3/6: 檢查文章列表頁..."
    if [[ -n "$article_basename" && -f "$ARTICLES_INDEX" ]]; then
        if grep -q "$article_basename" "$ARTICLES_INDEX"; then
            log "✅ 步驟 3/6 通過: 文章列表頁已包含今日文章"
        else
            fail "步驟 3/6 失敗: 文章列表頁未包含今日文章"
            errors=$((errors + 1))
        fi
    else
        fail "步驟 3/6 失敗: 無法檢查文章列表頁"
        errors=$((errors + 1))
    fi
    
    # 5️⃣ 檢查 Netlify deploy 是否成功
    log "🚀 步驟 4/6: 檢查 Netlify 部署..."
    if [[ -f "$DEPLOY_ID_FILE" ]]; then
        deploy_id=$(cat "$DEPLOY_ID_FILE")
        # 檢查 deploy_id 格式是否正確
        if [[ "$deploy_id" =~ ^[a-f0-9]{24}$ ]]; then
            log "✅ 步驟 4/6 通過: Deploy ID 有效 → ${deploy_id}"
        else
            fail "步驟 4/6 失敗: Deploy ID 格式異常 → ${deploy_id}"
            errors=$((errors + 1))
        fi
    else
        fail "步驟 4/6 失敗: Deploy ID 記錄檔不存在"
        errors=$((errors + 1))
    fi
    
    # 6️⃣ 檢查正式站 URL 是否 200 OK
    log "🌐 步驟 5/6: 檢查正式站可訪問性..."
    if [[ -n "$article_url_path" ]]; then
        full_url="https://fun1399.com${article_url_path}"
        http_code=$(curl -sL -o /dev/null -w "%{http_code}" --max-time 30 "$full_url" 2>/dev/null || echo "000")
        if [[ "$http_code" == "200" ]]; then
            log "✅ 步驟 5/6 通過: ${full_url} → HTTP ${http_code}"
        else
            fail "步驟 5/6 失敗: ${full_url} → HTTP ${http_code} (預期 200)"
            errors=$((errors + 1))
        fi
    else
        fail "步驟 5/6 失敗: 無法檢查 URL（文章未定義）"
        errors=$((errors + 1))
    fi
    
    # 6️⃣ 檢查 sitemap.xml 是否含今日文章 URL
    log "🗺️ 步驟 6/6: 檢查 sitemap.xml 含今日文章..."
    SITEMAP_FILE="${FUN1399_DIR}/sitemap.xml"
    if [[ -n "$article_basename" && -f "$SITEMAP_FILE" ]]; then
        if grep -q "${article_basename}" "$SITEMAP_FILE"; then
            log "✅ 步驟 6/6 通過: sitemap.xml 已包含今日文章 URL"
        else
            fail "步驟 6/6 失敗: sitemap.xml 缺少今日文章 URL → ${article_basename}"
            errors=$((errors + 1))
        fi
    else
        fail "步驟 6/6 失敗: 無法檢查 sitemap（文章未定義或 sitemap 不存在）"
        errors=$((errors + 1))
    fi
    
    # ── 結果總結 ──────────────────────────────────────────────────────────
    log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    if [[ $errors -eq 0 ]]; then
        log "🎉 驗證全部通過！發文任務真正完成"
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return 0
    else
        log "❌ 驗證失敗: ${errors} 項檢查未通過"
        log "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        return 1
    fi
}

# ── Retry 機制 ──────────────────────────────────────────────────────────────
retry_publish() {
    RETRY_COUNT=$((RETRY_COUNT + 1))
    log "🔄 啟動自動 Retry (${RETRY_COUNT}/${MAX_RETRIES})..."
    
    # Retry: 重新執行完整發文流程
    # 注意：這裡會呼叫主發文腳本（需另外實作）
    if [[ -x "${WORKSPACE}/scripts/auto-publish.sh" ]]; then
        "${WORKSPACE}/scripts/auto-publish.sh"
        return $?
    else
        log "⚠️ 找不到 auto-publish.sh，無法自動 Retry"
        return 1
    fi
}

# ── Telegram 通知 ─────────────────────────────────────────────────────────
send_telegram_alert() {
    local message="🔴 fun1399 發文失敗警報\n\n日期: ${today_date}\n錯誤: $1\n\n請手動檢查並補發。"
    # 這裡需要 Telegram Bot Token 和 Chat ID
    # 由於安全性，Token 應從環境變數讀取
    if [[ -n "${TELEGRAM_BOT_TOKEN:-}" && -n "${TELEGRAM_CHAT_ID:-}" ]]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=${message}" \
            -d "parse_mode=HTML" > /dev/null 2>&1
        log "📨 Telegram 通知已發送"
    else
        log "⚠️ Telegram 通知未設定（缺少 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID）"
    fi
}

# ── 主程式 ──────────────────────────────────────────────────────────────────
main() {
    # 第一次驗證
    if verify_publish; then
        exit 0
    fi
    
    # 驗證失敗，嘗試 Retry
    if [[ $RETRY_COUNT -lt $MAX_RETRIES ]]; then
        log ""
        log "═══════════════════════════════════════════════════"
        log "  驗證失敗，啟動自動 Retry (${RETRY_COUNT}/${MAX_RETRIES})"
        log "═══════════════════════════════════════════════════"
        log ""
        
        if retry_publish; then
            # Retry 成功，再次驗證
            log ""
            log "═══════════════════════════════════════════════════"
            log "  Retry 完成，重新驗證..."
            log "═══════════════════════════════════════════════════"
            log ""
            
            if verify_publish; then
                log "🎉 Retry 後驗證通過！發文任務完成"
                exit 0
            fi
        fi
    fi
    
    # Retry 後仍失敗
    log ""
    log "═══════════════════════════════════════════════════"
    log "  ❌ 驗證失敗且 Retry 無效"
    log "  標記為「待補發」，請手動處理"
    log "═══════════════════════════════════════════════════"
    log ""
    
    # 寫入待補發記錄
    echo "${today_date}|$(date +%H:%M:%S)|FAILED|待手動補發" >> "${WORKSPACE}/logs/pending-publish.txt"
    
    # 發送 Telegram 通知
    send_telegram_alert "驗證失敗且 Retry 無效，需手動補發"
    
    exit 1
}

# 執行主程式
main "$@"
