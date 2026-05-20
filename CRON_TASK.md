# Cron 自動發文任務指令

## 執行流程

1. **讀取** `/root/.openclaw/workspace/2MONTH-CONTENT-PLAN-May-Jun-2026-v2.md`
2. **讀取** `/root/.openclaw/workspace/memory/YYYY-MM-DD.md`（今天日期）
3. **確認** 今天應該寫的文章（依照規劃順序，尋找第一個未完成的）
4. **撰寫文章**，嚴格遵守以下規格：
   - Title 必須同時包含當日主關鍵字 2-3 個
   - 開頭 100 字內命中主關鍵字
   - H2 x 6-8 個
   - 內鏈 3-5 個（導向既有評價文章）
   - CTA 有情緒張力
   - 結論金句
   - Meta description 40-50 字
   - 字色 #111、line-height 1.7
   - 封面圖 1280x800 PNG
5. **更新首頁** `fun1399-clean/index.html`（插第1位，保留6篇）
6. **更新分類頁** `fun1399-clean/articles/index.html`
7. **部署到正式站**（使用 netlify-deploy.sh）
8. **執行驗證**（見下方「發文完成驗證」）
9. **回報用戶**（發送 Telegram 訊息）

---

## ✅ 發文完成驗證機制

**每次 cron 執行後必須執行驗證，不可靜默失敗。**

### 驗證腳本
- 路徑：`/root/.openclaw/workspace/scripts/verify-publish.sh`
- 用途：檢查發文是否「真正完成」

### 驗證項目（5項全部必須通過）

| # | 檢查項目 | 通過標準 |
|---|---------|---------|
| 1 | 文章 HTML 存在 | `articles/今日文章.html` 檔案存在 |
| 2 | 首頁已更新 | `index.html` 包含今日文章連結 |
| 3 | 分類頁已更新 | `articles/index.html` 包含今日文章 |
| 4 | Netlify 部署成功 | `/tmp/fun1399-last-deploy-id.txt` 有有效 Deploy ID |
| 5 | 正式站 200 OK | `curl https://fun1399.com/articles/今日文章.html` → HTTP 200 |

### 失敗補救流程

```
驗證失敗
    ↓
自動 Retry 一次（重新執行完整發文 + 部署）
    ↓
再次驗證
    ├── 通過 → ✅ 發文完成
    └── 失敗 → 🚨 標記「待補發」+ Telegram 通知
```

### 不可靜默失敗規則

- ❌ 不可只因「cron 有觸發」就視為成功
- ❌ 不可只因「文章已產出」就視為成功
- ❌ 不可只因「部署指令已執行」就視為成功
- ✅ 必須 5 項驗證全部通過，才算「發文完成」
- ✅ 若驗證失敗，必須留下錯誤記錄於 `logs/failed-publish.log`
- ✅ 若 Retry 仍失敗，必須留下 `logs/pending-publish.txt` 待補發記錄

### 部署腳本

- 路徑：`/root/.openclaw/workspace/scripts/netlify-deploy.sh`
- 用途：包裝 `netlify-cli deploy`，成功後自動記錄 Deploy ID 到 `/tmp/fun1399-last-deploy-id.txt`

## 禁止事項
- 不可自行新增主題（必須從 6MONTH-CONTENT-PLAN.md 選擇）
- 不可修改舊文章内容
- 不可直接部署正式站
- 不可使用 mtime 排序

## 關鍵路徑
- Source: `/root/.openclaw/workspace/fun1399-clean/`
- Site ID: `7232c8ac-d01c-454d-867b-f0eb8f4c7f94`
- Auth Token: `nfp_Bx3XZMAJS2sv86ujMqaAbcB9jGzya7tu589b`
