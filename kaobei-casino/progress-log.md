# 靠北娛樂城 MVP 建置進度紀錄

## 建置時間
2025-05-30 (Asia/Taipei)

## 專案路徑
`/root/.openclaw/workspace/kaobei-casino/`

## 已完成的項目

### 1. 目錄結構 ✅
```
kaobei-casino/
├── config/
│   └── site-config.js          # 站點全域配置（含 fun1399 URL、LINE、Email placeholder）
├── data/
│   ├── raw-reports/              # 內部資料夾（空，不納入 build）
│   ├── cases/
│   │   ├── demo-case-001.md     # 出金延遲示範案件
│   │   ├── demo-case-002.md     # 客服糾紛示範案件
│   │   └── demo-case-003.md     # 優惠條款示範案件
│   └── casinos/
│       ├── demo-casino-a.md     # Demo Casino A 示範平台
│       └── demo-casino-b.md     # Demo Casino B 示範平台
├── public/
│   └── images/
│       └── cases/                # 公開圖片（空，待未來使用）
├── static/
│   └── styles.css               # 共用樣式表（暗色主題、行動優先）
├── index.html                   # 首頁（hero、最新案件、常見問題、平台紀錄、回報入口、fun1399 CTA）
├── cases/
│   └── index.html               # 爭議案件列表頁
├── withdrawal-issues/
│   └── index.html               # 出金問題資料庫頁
├── casinos/
│   └── index.html               # 平台風險紀錄總覽
├── casino/
│   ├── demo-casino-a/
│   │   └── index.html           # 單一平台風險檔案（demo）
│   └── demo-casino-b/
│       └── index.html           # 單一平台風險檔案（demo）
├── case/
│   ├── demo-case-001/
│   │   └── index.html           # 單一案件頁（出金延遲 demo）
│   ├── demo-case-002/
│   │   └── index.html           # 單一案件頁（客服糾紛 demo）
│   └── demo-case-003/
│       └── index.html           # 單一案件頁（優惠條款 demo）
├── report/
│   └── index.html               # 玩家回報表單頁（示範模式）
├── about/
│   └── index.html               # 關於本站
├── disclaimer/
│   └── index.html               # 免責聲明
├── contact/
│   └── index.html               # 聯絡與申訴
├── robots.txt                   # robots.txt（禁止 demo / data / config / static）
├── sitemap.xml                  # Sitemap（僅含非 demo 頁面）
└── progress-log.md              # 本檔案
```

### 2. 視覺設計 ✅
- 暗色主題（深藍/炭黑背景 `#0f1117` / `#161920`）
- 警示色使用暗紅/橙紅（`#dc2626` / `#ea580c`）
- 金色僅用於小 CTA 按鈕（`#d4a017`）
- 行動優先響應式設計
- 專業調查資料庫風格（無賭場閃亮感、無攻擊性語言）

### 3. SEO 設定 ✅
- 所有頁面 `<meta name="robots" content="noindex, nofollow">`（預覽模式）
- OG tags（title, description, type, url, site_name）
- Canonical URLs（placeholder base URL）
- Schema.org JSON-LD：
  - 首頁：WebSite + Organization
  - 案件頁：Article
- Sitemap 排除所有 demo/draft 頁面
- robots.txt 禁止 `/case/`、`/casino/`、`/data/`、`/config/`、`/static/`

### 4. 法律文字 ✅
- 所有案件/平台頁面包含「詐騙/黑網/不出金僅為搜尋常用詞彙」聲明
- 無直接指控語言（使用「玩家反映」「觀察紀錄」等中性詞）
- Demo 頁面顯示醒目示範資料橫幅

### 5. 示範資料 ✅
- 2 個虛構平台：Demo Casino A、Demo Casino B
- 3 個虛構案件（均設 `is_demo: true`）
- 所有 demo 頁面顯示「測試資料／示範頁面，非真實平台爭議紀錄」
- Demo 內容未納入 sitemap

### 6. 共用元件 ✅
- 統一 Header（logo + nav + 行動選單按鈕）
- 統一 Footer（品牌 + 導覽連結 + 法律聲明）
- fun1399 CTA 區塊（首頁與部分頁面）
- 搜尋用詞聲明區塊（案件/平台頁）

### 7. 本地預覽 ✅
- Python http.server on port 3456
- Cloudflared tunnel active

## 待 Hans 提供
1. **fun1399 正式網址**：目前使用 `https://fun1399.com/`，請 Hans 確認
2. **LINE ID**：配置於 `site-config.js` 與聯絡頁面，目前標示 `[待 Hans 提供]`
3. **Email 地址**：配置於 `site-config.js` 與聯絡/回報頁面，目前標示 `[待 Hans 提供]`
4. **正式域名**：目前所有 canonical URL 使用 `https://kaobei-casino.example.com/`，上線前需替換
5. **Logo / 品牌素材**：目前使用文字 logo「KB」+ CSS 漸層方塊
6. **公開圖片**：`public/images/cases/` 目前為空，待未來審核通過後放入

## 已知限制
- 目前為純靜態 HTML，無後端表單處理（回報表單為示範模式）
- 無搜尋/篩選功能（靜態站點限制）
- 行動選單按鈕目前僅切換 class，需補上 CSS `.mobile-open` 樣式或 JS 行為
- 無自動化資料同步機制（未來可擴展 Node.js/Python 腳本從 `data/` 生成 HTML）

## 預覽資訊
- **本地伺服器**：`http://localhost:3456`
- **Cloudflared Tunnel**：`https://lookup-learning-latina-heavily.trycloudflare.com`
- **狀態**：預覽中，全站 `noindex, nofollow`

## 後續建議
1. 確認 Hans 提供的 LINE / Email 後，批量替換所有頁面中的 placeholder
2. 設計正式 Logo 與品牌素材
3. 確認上線後移除所有 `noindex` meta tag，並更新 sitemap.xml 中的 base URL
4. 評估是否需要自動化 build 流程（將 Markdown data 轉為靜態 HTML）
5. 新增 `.gitignore`（排除 `data/raw-reports/` 與 build artifacts）
