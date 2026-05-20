#!/bin/bash
# =============================================================================
# Netlify 部署 + 記錄 Deploy ID
# 用途：包裝 netlify-cli deploy，成功後記錄 deploy_id 供驗證腳本使用
# =============================================================================

set -euo pipefail

DEPLOY_ID_FILE="/tmp/fun1399-last-deploy-id.txt"
WORKSPACE="/root/.openclaw/workspace"
FUN1399_DIR="${WORKSPACE}/fun1399-clean"

cd "$FUN1399_DIR"

# 執行 Netlify 部署並擷取 deploy_id
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "🚀 開始 Netlify 部署..."

# 使用 netlify-cli 部署並取得 JSON 輸出
DEPLOY_OUTPUT=$(NETLIFY_AUTH_TOKEN="${NETLIFY_AUTH_TOKEN}" \
    npx netlify-cli deploy \
    --site=7232c8ac-d01c-454d-867b-f0eb8f4c7f94 \
    --prod \
    --dir=. \
    --json 2>&1) || {
    log "❌ Netlify 部署失敗"
    exit 1
}

# 從輸出中擷取 deploy_id
deploy_id=$(echo "$DEPLOY_OUTPUT" | grep -o '"deploy_id": "[^"]*"' | head -1 | cut -d'"' -f4)

if [[ -n "$deploy_id" && "$deploy_id" =~ ^[a-f0-9]{24}$ ]]; then
    echo "$deploy_id" > "$DEPLOY_ID_FILE"
    log "✅ 部署成功，Deploy ID 已記錄: ${deploy_id}"
else
    log "⚠️ 無法擷取 Deploy ID，部署可能異常"
    exit 1
fi
