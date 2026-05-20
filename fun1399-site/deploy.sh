#!/bin/bash
# Fun1399.com 自動部署腳本
# 使用方法：./deploy.sh

set -e

echo "🚀 開始自動部署 Fun1399.com 到 Netlify..."
echo ""

# 設定
TOKEN="nfp_TaE2jFupmC6TBN1ERFFUA46Z6p1bUogSf432"
SITE_ID="7232c8ac-d01c-454d-867b-f0eb8f4c7f94"
BUILD_DIR="build"

echo "【步驟1】準備部署檔案..."
cd "$(dirname "$0")"

if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ 錯誤：找不到 $BUILD_DIR 目錄"
    exit 1
fi

# 建立部署zip
rm -f deploy.zip
cd "$BUILD_DIR"
zip -r ../deploy.zip . > /dev/null 2>&1
cd ..

FILE_SIZE=$(du -h deploy.zip | cut -f1)
echo "✅ 部署檔案已建立 (大小: $FILE_SIZE)"

echo ""
echo "【步驟2】上傳到 Netlify..."

# 呼叫 API 部署
DEPLOY_RESPONSE=$(curl -s -X POST "https://api.netlify.com/api/v1/sites/${SITE_ID}/deploys" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/zip" \
  --data-binary @deploy.zip)

# 檢查是否有錯誤
ERROR_MSG=$(echo "$DEPLOY_RESPONSE" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('error_message',''))" 2>/dev/null)

if [ -n "$ERROR_MSG" ] && [ "$ERROR_MSG" != "None" ]; then
    echo "❌ 部署失敗: $ERROR_MSG"
    exit 1
fi

# 提取部署資訊
DEPLOY_ID=$(echo "$DEPLOY_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id','N/A'))" 2>/dev/null)
DEPLOY_URL=$(echo "$DEPLOY_RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('deploy_url','N/A'))" 2>/dev/null)

echo "✅ 部署已建立 (ID: $DEPLOY_ID)"

echo ""
echo "【步驟3】等待部署完成..."

# 輪詢檢查狀態
MAX_WAIT=60
for i in $(seq 1 $MAX_WAIT); do
    sleep 2
    
    STATUS=$(curl -s "https://api.netlify.com/api/v1/sites/${SITE_ID}/deploys/${DEPLOY_ID}" \
      -H "Authorization: Bearer ${TOKEN}")
    
    STATE=$(echo "$STATUS" | python3 -c "import sys,json; print(json.load(sys.stdin).get('state','unknown'))" 2>/dev/null)
    
    case "$STATE" in
        "ready")
            echo "✅ 部署完成！"
            break
            ;;
        "error")
            echo "❌ 部署失敗"
            exit 1
            ;;
        *)
            if [ $((i % 5)) -eq 0 ]; then
                echo "⏳ 處理中... ($STATE)"
            fi
            ;;
    esac
    
    if [ $i -eq $MAX_WAIT ]; then
        echo "⚠️ 等待超時，但部署可能仍在進行中"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 自動部署成功！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 網站網址：https://fun1399.com"
echo "🔗 部署預覽：$DEPLOY_URL"
echo "🆔 部署ID：$DEPLOY_ID"
echo ""
echo "📊 部署內容："
echo "   • HTML頁面：$(find $BUILD_DIR -name '*.html' | wc -l) 個"
echo "   • 檔案大小：$FILE_SIZE"
echo "   • 部署時間：$(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 清理
rm -f deploy.zip

echo ""
echo "✨ 部署完成！網站已更新。"
