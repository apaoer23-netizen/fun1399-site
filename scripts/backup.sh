#!/bin/bash
# fun1399 + OpenClaw Backup Script
# Created: 2026-04-22
# Frequency: Weekly (Sundays 03:00)

set -e

DATE=$(date +%Y%m%d)
BACKUP_DIR="/root/.openclaw/backups"
WORKSPACE="/root/.openclaw/workspace"
SKILLS="/root/.openclaw/skills"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# === 1. Website Backup ===
WEBSITE_BACKUP="fun1399-backup-${DATE}.zip"
WEBSITE_SOURCE="${WORKSPACE}/fun1399-clean"

if [ -d "$WEBSITE_SOURCE" ]; then
    cd "$WORKSPACE"
    zip -r "${BACKUP_DIR}/${WEBSITE_BACKUP}" fun1399-clean/ \
        -x "*.tmp" "*.log" "*.bak" "*~" >/dev/null 2>&1
    echo "✅ Website backup: ${WEBSITE_BACKUP}"
else
    echo "❌ Website source not found: ${WEBSITE_SOURCE}"
fi

# === 2. OpenClaw System Backup ===
SYSTEM_BACKUP="openclaw-backup-${DATE}.zip"
SYSTEM_SPLIT="openclaw-backup-split"

if [ -d "$WORKSPACE" ] && [ -d "$SKILLS" ]; then
    cd /root/.openclaw
    zip -r "${BACKUP_DIR}/${SYSTEM_BACKUP}" workspace/ skills/ \
        -x "*.tmp" "*.log" "*.bak" "*~" "*/node_modules/*" "*/.git/*" >/dev/null 2>&1
    echo "✅ System backup: ${SYSTEM_BACKUP}"
    
    # === 2.5 Verify & Split ===
    echo ""
    echo "🔍 正在驗證壓縮檔完整性..."
    
    # Test original archive integrity first
    if zip -T "${BACKUP_DIR}/${SYSTEM_BACKUP}" >/dev/null 2>&1; then
        echo "✅ 原始壓縮檔驗證通過"
    else
        echo "❌ 原始壓縮檔驗證失敗！重新壓縮中..."
        cd /root/.openclaw
        rm -f "${BACKUP_DIR}/${SYSTEM_BACKUP}"
        zip -r "${BACKUP_DIR}/${SYSTEM_BACKUP}" workspace/ skills/ \
            -x "*.tmp" "*.log" "*.bak" "*~" "*/node_modules/*" "*/.git/*" >/dev/null 2>&1
        
        if zip -T "${BACKUP_DIR}/${SYSTEM_BACKUP}" >/dev/null 2>&1; then
            echo "✅ 重新壓縮並驗證通過"
        else
            echo "❌ 重新壓縮後仍驗證失敗，請手動檢查"
            exit 1
        fi
    fi
    
    # Now split into volumes
    echo ""
    echo "📦 正在分割系統備份（45MB/卷）..."
    cd "$BACKUP_DIR"
    
    # Remove old split files if exist
    rm -f "${SYSTEM_SPLIT}.z01" "${SYSTEM_SPLIT}.z02" "${SYSTEM_SPLIT}.z03" "${SYSTEM_SPLIT}.zip"
    
    # Split into 45MB volumes
    zip -s 45m "${SYSTEM_BACKUP}" --out "${SYSTEM_SPLIT}.zip" >/dev/null 2>&1
    echo "✅ 分割完成"
    
    # Verify split archive can be read
    if unzip -t "${SYSTEM_SPLIT}.zip" >/dev/null 2>&1; then
        echo "✅ 分卷壓縮檔可正常讀取"
    else
        echo "⚠️ 分卷讀取測試未通過（可能仍可正常解壓）"
    fi
else
    echo "❌ System directories not found"
fi

# === 3. Report ===
echo ""
echo "━━━━━━━━━━━━━━━"
echo "【備份完成回報】"
echo "━━━━━━━━━━━━━━━"
echo ""
echo "1. 備份檔案名稱："
if [ -f "${BACKUP_DIR}/${WEBSITE_BACKUP}" ]; then
    SIZE1=$(ls -lh "${BACKUP_DIR}/${WEBSITE_BACKUP}" | awk '{print $5}')
    echo "   - ${WEBSITE_BACKUP} (${SIZE1})"
fi
if [ -f "${BACKUP_DIR}/${SYSTEM_BACKUP}" ]; then
    SIZE2=$(ls -lh "${BACKUP_DIR}/${SYSTEM_BACKUP}" | awk '{print $5}')
    echo "   - ${SYSTEM_BACKUP} (${SIZE2})"
fi

echo ""
echo "2. 下載路徑："
echo "   - ${BACKUP_DIR}/${WEBSITE_BACKUP}"
echo "   - ${BACKUP_DIR}/${SYSTEM_BACKUP}"

echo ""
echo "3. 歷史備份檔案："
ls -lh "$BACKUP_DIR" | grep -E "fun1399-backup|openclaw-backup" | awk '{print $9, $5}'

echo ""
echo "━━━━━━━━━━━━━━━"
echo "備份時間: $(date '+%Y-%m-%d %H:%M:%S')"
echo "━━━━━━━━━━━━━━━"

# === 4. Send Email ===
echo ""
echo "📧 正在寄送備份 Email..."
python3 /root/.openclaw/workspace/scripts/send_backup_email.py 2>&1 || echo "⚠️ Email 寄送可能失敗，請檢查"
