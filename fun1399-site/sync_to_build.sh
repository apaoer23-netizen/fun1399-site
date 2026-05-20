#!/bin/bash
# 從 Source (fun1399-fixed) 同步到 Build 目錄
# 並確保所有修改都被正確應用

set -e

echo "🔄 開始從 Source 同步到 Build 目錄..."
echo ""

SOURCE_DIR="/root/.openclaw/workspace/fun1399-site/fun1399-fixed"
BUILD_DIR="/root/.openclaw/workspace/fun1399-site/build"

# Step 1: 同步根目錄檔案
echo "📁 Step 1: 同步根目錄..."
cp -r "$SOURCE_DIR"/*.html "$BUILD_DIR/" 2>/dev/null || true
cp -r "$SOURCE_DIR"/static "$BUILD_DIR/" 2>/dev/null || true

# Step 2: 同步 articles
echo "📝 Step 2: 同步 articles..."
if [ -d "$SOURCE_DIR/articles" ]; then
    mkdir -p "$BUILD_DIR/articles"
    cp -r "$SOURCE_DIR/articles"/*.html "$BUILD_DIR/articles/"
fi

# Step 3: 同步 reviews
echo "⭐ Step 3: 同步 reviews..."
if [ -d "$SOURCE_DIR/reviews" ]; then
    mkdir -p "$BUILD_DIR/reviews"
    cp -r "$SOURCE_DIR/reviews"/*.html "$BUILD_DIR/reviews/"
fi

# Step 4: 同步其他目錄
echo "📂 Step 4: 同步其他目錄..."
for dir in pillars recommend promotions comparisons; do
    if [ -d "$SOURCE_DIR/$dir" ]; then
        mkdir -p "$BUILD_DIR/$dir"
        cp -r "$SOURCE_DIR/$dir"/*.html "$BUILD_DIR/$dir/" 2>/dev/null || true
    fi
done

echo ""
echo "✅ 同步完成！"
echo ""
echo "📊 同步統計："
echo "   • HTML檔案: $(find $BUILD_DIR -name '*.html' | wc -l) 個"
echo "   • Articles: $(find $BUILD_DIR/articles -name '*.html' 2>/dev/null | wc -l) 個"
echo "   • Reviews: $(find $BUILD_DIR/reviews -name '*.html' 2>/dev/null | wc -l) 個"
echo ""
echo "🔧 準備部署..."
