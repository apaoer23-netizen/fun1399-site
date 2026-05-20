#!/bin/bash
# Bitly 短連結生成腳本
# 用法: ./bitly_shorten.sh "https://your-long-url.com"

LONG_URL="${1:-https://fun1399.ofa177.net/?refer=bonus2026}"
BITLY_TOKEN="${BITLY_ACCESS_TOKEN:-YOUR_BITLY_ACCESS_TOKEN_HERE}"

if [ "$BITLY_TOKEN" = "YOUR_BITLY_ACCESS_TOKEN_HERE" ]; then
    echo "❌ 錯誤：請設定 BITLY_ACCESS_TOKEN 環境變數"
    echo ""
    echo "取得方式："
    echo "1. 登入 https://app.bitly.com"
    echo "2. 進入 Settings > API > Access Token"
    echo "3. 複製 Generic Access Token"
    echo ""
    echo "使用方式："
    echo "   export BITLY_ACCESS_TOKEN='your_token_here'"
    echo "   ./bitly_shorten.sh 'https://your-url.com'"
    exit 1
fi

echo "🔗 正在生成短連結..."
echo "原始網址: $LONG_URL"
echo ""

RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $BITLY_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"long_url\": \"$LONG_URL\", \"domain\": \"bit.ly\"}" \
  https://api-ssl.bitly.com/v4/shorten)

# 檢查是否有錯誤
if echo "$RESPONSE" | grep -q '"message":'; then
    echo "❌ API 錯誤:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi

SHORT_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('link',''))" 2>/dev/null)

if [ -n "$SHORT_URL" ]; then
    echo "✅ 短連結生成成功！"
    echo ""
    echo "🎯 短連結: $SHORT_URL"
    echo "📋 已複製到剪貼簿 (若系統支援)"
    echo "$SHORT_URL" | xclip -selection clipboard 2>/dev/null || echo "$SHORT_URL" | pbcopy 2>/dev/null || true
    echo ""
    echo "回應詳情:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
else
    echo "❌ 無法解析回應:"
    echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
    exit 1
fi
