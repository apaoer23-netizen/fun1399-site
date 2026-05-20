# FUN1399 SEO 技能系統完整分析報告

**日期**: 2026-05-20  
**分析對象**: OpenClaw 技能系統中適合 fun1399.com 的 SEO 相關技能  
**分析者**: FUN1399 Bot  

---

## 一、目前已安裝 SEO 相關技能清單

### 📊 系統級技能（/usr/lib/node_modules/openclaw/skills/）

| # | 技能名稱 | 路徑 | 主要用途 | 適合 fun1399 |
|---|---------|------|---------|------------|
| 1 | **seo-audit** | workspace/skills/seo-audit | Technical SEO 全面檢查 | ✅ 最適合 |
| 2 | **seo** | workspace/skills/seo | 基礎 SEO 優化指南 | ✅ 適合 |
| 3 | **seo-geo** | workspace/skills/seo-geo | SEO + AI 搜尋優化 | ✅ 適合 |
| 4 | **ai-seo** | workspace/skills/ai-seo | AI 搜尋引擎優化 | ✅ 適合 |
| 5 | **google-search-console** | workspace/skills/google-search-console | GSC 數據分析 | ✅ 最適合 |
| 6 | **seo-content-brief** | workspace/skills/seo-content-brief | 內容策略規劃 | ✅ 適合 |
| 7 | **programmatic-seo** | workspace/skills/programmatic-seo | 大量頁面生成 | ⚠️ 部分適合 |
| 8 | **schema-markup** | （內嵌在 seo-audit 中）| 結構化資料 | ✅ 適合 |
| 9 | **seo-optimizer** | ~/.openclaw/skills/seo-optimizer | 自動 SEO 優化 | ⚠️ 功能重複 |
| 10 | **internal-linker** | ~/.openclaw/skills/internal-linker | 內部連結分析 | ✅ 適合 |
| 11 | **seo-site-master** | ~/.openclaw/skills/seo-site-master | 全站 SEO 建置 | ❌ 不適合 |
| 12 | **keyword-planner** | ~/.openclaw/skills/keyword-planner | 關鍵字規劃 | ✅ 適合 |
| 13 | **image-optimizer** | ~/.openclaw/skills/image-optimizer | 圖片優化 | ⚠️ 可有可無 |
| 14 | **static-site-generator** | ~/.openclaw/skills/static-site-generator | 靜態站生成 | ❌ 不適合 |
| 15 | **humanizer** | workspace/skills/humanizer | 去除 AI 寫作痕跡 | ⚠️ 可有可無 |

---

## 二、技能功能對應分析

### 🔍 Technical SEO 檢查能力

| 檢查項目 | 最適合技能 | 替代技能 | 手動方法 |
|----------|-----------|---------|---------|
| **SEO 全站健檢** | seo-audit | seo-geo | curl + grep |
| **robots.txt 檢查** | seo-audit, seo-geo | — | curl |
| **sitemap.xml 檢查** | seo-audit, seo-geo | — | curl + grep |
| **canonical 檢查** | seo-audit | seo | curl + grep |
| **schema 檢查** | seo-audit | ai-seo | browser render |
| **redirect chain** | seo-audit | — | curl -L -w |
| **status code 檢查** | seo-audit | — | curl -w %{http_code} |
| **trailing slash** | seo-audit | — | curl 多 URL 測試 |
| **.html → clean URL** | seo-audit | — | curl 測試 |
| **404 處理** | seo-audit | — | curl 不存在 URL |
| **Core Web Vitals** | seo-audit (提及) | — | PageSpeed Insights API |
| **mobile rendering** | seo-audit | — | curl + User-Agent |
| **indexability** | seo-audit, google-search-console | — | GSC API |
| **security headers** | seo-audit | — | curl -I |

### 📈 內容與策略分析

| 檢查項目 | 最適合技能 | 替代技能 |
|----------|-----------|---------|
| **internal link 分析** | internal-linker | seo-audit |
| **orphan pages** | internal-linker | seo-audit |
| **content quality** | ai-seo | seo-audit |
| **EEAT 分析** | ai-seo | seo-audit |
| **thin content** | seo-audit | ai-seo |
| **page quality** | seo-audit | ai-seo |
| **topical authority** | ai-seo | seo-content-brief |
| **content cluster** | seo-content-brief | ai-seo |
| **keyword research** | keyword-planner | seo-content-brief |
| **GSC 對應分析** | google-search-console | — |

### 🚀 AI / GEO 優化

| 檢查項目 | 最適合技能 | 說明 |
|----------|-----------|------|
| **AI 搜尋可見度** | ai-seo | ChatGPT/Perplexity 被引用 |
| **GEO 優化** | seo-geo | 結構化內容 + 統計 |
| **FAQ Schema** | seo-geo | +40% AI 可見度 |
| **AI Bot robots.txt** | ai-seo | GPTBot/PerplexityBot |

---

## 三、技能重複與重疊分析

### 🔴 高度重複（功能幾乎相同）

| 技能組合 | 重複功能 | 建議 |
|----------|---------|------|
| **seo-audit + seo** | Technical SEO 檢查 | 保留 seo-audit（更全面），seo 作為參考 |
| **seo-geo + ai-seo** | AI 搜尋優化 | 兩者互補，seo-geo 偏重技術，ai-seo 偏重內容 |
| **seo-optimizer + seo-audit** | 頁面優化建議 | 功能重複，seo-optimizer 較弱 |

### 🟡 部分重疊（可互補使用）

| 技能組合 | 互補方式 |
|----------|---------|
| **internal-linker + seo-audit** | internal-linker 專精連結結構，seo-audit 全面檢查 |
| **seo-content-brief + keyword-planner** | brief 偏重內容策略，planner 偏重關鍵字數據 |
| **google-search-console + seo-audit** | GSC 看數據，seo-audit 看技術 |

### ✅ 無重複（各自獨立）

| 技能 | 獨特功能 |
|------|---------|
| **google-search-console** | GSC API 數據拉取 |
| **programmatic-seo** | 大量頁面模板生成 |
| **humanizer** | AI 文本自然化 |
| **image-optimizer** | 圖片壓縮/格式轉換 |

---

## 四、技能強弱評估

### 💪 強力推薦（核心技能）

| 排名 | 技能 | 強度 | 原因 |
|------|------|------|------|
| 🥇 | **seo-audit** | ⭐⭐⭐⭐⭐ | 最全面 technical SEO 檢查，包含 crawlability、indexation、Core Web Vitals、content quality、structured data |
| 🥈 | **google-search-console** | ⭐⭐⭐⭐⭐ | GSC 數據分析，索引狀態、查詢分析、Core Web Vitals 報告 |
| 🥉 | **ai-seo** | ⭐⭐⭐⭐ | AI 搜尋優化（未來趨勢），包含 Princeton GEO 研究方法 |

### 👍 推薦使用（輔助技能）

| 技能 | 強度 | 適用場景 |
|------|------|---------|
| **internal-linker** | ⭐⭐⭐⭐ | 內部連結結構分析、orphan pages 檢測 |
| **seo-geo** | ⭐⭐⭐⭐ | 傳統 SEO + AI 搜尋雙優化 |
| **seo-content-brief** | ⭐⭐⭐ | 新文章規劃、SERP 分析 |
| **keyword-planner** | ⭐⭐⭐ | 關鍵字研究 |

### ⚠️ 可有可無（非核心）

| 技能 | 強度 | 原因 |
|------|------|------|
| **seo-optimizer** | ⭐⭐ | 功能被 seo-audit 覆蓋，且偏自動化不精細 |
| **image-optimizer** | ⭐⭐ | Cloudflare Polish 已可替代 |
| **humanizer** | ⭐⭐ | 內容行銷輔助，非 SEO 核心 |

### ❌ 不推薦（不適合 fun1399）

| 技能 | 原因 |
|------|------|
| **seo-site-master** | 專為新站建立設計，fun1399 已有完整架構 |
| **static-site-generator** | fun1399 已是靜態站，無需再生成 |
| **one-click-deploy** | Cloudflare Pages 已整合 GitHub auto-deploy |

---

## 五、fun1399 最適合的技能組合

### 🎯 TOP 3 核心技能

| 優先級 | 技能 | 用途 | 使用頻率 |
|--------|------|------|---------|
| **1** | **seo-audit** | Technical SEO 全面檢查、canonical、sitemap、redirect、schema、404 | 每次 deploy 後 |
| **2** | **google-search-console** | 索引監控、查詢分析、Core Web Vitals、爬蟲錯誤 | 每週 |
| **3** | **ai-seo** | AI 搜尋可見度、GEO 優化、內容結構化 | 每月 |

### 📋 輔助技能組合

| 場景 | 使用技能 |
|------|---------|
| **新文章規劃** | seo-content-brief + keyword-planner |
| **內部連結優化** | internal-linker |
| **大量頁面生成** | programmatic-seo |
| **AI 搜尋趨勢** | ai-seo + seo-geo |
| **內容品質提升** | humanizer + ai-seo |

---

## 六、目前技能系統缺失的能力

### 🔴 明顯缺失（高優先補強）

| # | 缺失能力 | 影響 | 建議解決方案 |
|---|---------|------|------------|
| 1 | **Core Web Vitals 自動測量** | 無法自動化 LCP/CLS/INP 檢查 | 使用 PageSpeed Insights API + lighthouse CLI |
| 2 | **GSC API 自動拉取** | 需手動查 GSC | 安裝 gsc skill 或使用 Search Console API |
| 3 | **爬蟲模擬（Crawl Simulation）** | 無法模擬 Googlebot 爬取全站 | 使用 wget --spider 或自訂爬蟲腳本 |
| 4 | **Backlink 分析** | 無法檢查外部連結 | 需第三方工具（Ahrefs API）|
| 5 | **Content Freshness 監控** | 無法追蹤文章更新頻率 | 自訂腳本檢查 lastmod |

### 🟡 部分缺失（中優先）

| # | 缺失能力 | 說明 |
|---|---------|------|
| 6 | **Topical Authority 分析** | 無法分析主題群組覆蓋率 |
| 7 | **Search Intent 自動分類** | 需手動判斷 |
| 8 | **SERP Feature 追蹤** | 無法追蹤 Featured Snippet/PAA |
| 9 | **Competitor Content Gap** | 無法自動比對競爭對手內容 |
| 10 | **Rank Tracking** | 無法追蹤關鍵字排名變化 |

### 🟢 低優先（現有工具可替代）

| # | 缺失能力 | 替代方案 |
|---|---------|---------|
| 11 | **Heatmap / User Behavior** | 使用 GA4 |
| 12 | **A/B Testing for SEO** | 手動測試 |
| 13 | **Log File Analysis** | Cloudflare Analytics |

---

## 七、fun1399 專屬建議

### 立即安裝/啟用

| 技能 | 優先級 | 原因 |
|------|--------|------|
| **seo-audit** | 🔴 高 | 每次 deploy 後自動檢查 |
| **google-search-console** | 🔴 高 | 追蹤索引與 Core Web Vitals |
| **internal-linker** | 🟡 中 | 分析 98 頁的內部連結結構 |
| **ai-seo** | 🟡 中 | 未來 AI 搜尋趨勢 |

### 可自建替代方案

| 需求 | 自建方案 | 工具 |
|------|---------|------|
| **Production vs Preview Diff** | curl + diff | 已實作 |
| **Sitemap 驗證** | curl + grep | 已實作 |
| **Redirect 檢查** | curl -L -w | 已實作 |
| **Orphan Pages** | 自訂腳本掃描 | 可實作 |
| **Core Web Vitals** | lighthouse-ci | 可整合 |

### 不建議安裝

| 技能 | 原因 |
|------|------|
| seo-site-master | 不適合已有架構的站 |
| static-site-generator | 已有靜態站 |
| one-click-deploy | Cloudflare 已 auto-deploy |

---

## 八、技能使用建議

### 每次 Deploy 後執行

```bash
# 1. seo-audit 全面檢查
@seo-audit analyze https://fun1399.com

# 2. 自訂 diff 檢查（已實作）
bash /tmp/seo_diff.sh

# 3. sitemap + robots 驗證
curl -s https://fun1399.com/sitemap.xml | grep -c '<loc>'
curl -s https://fun1399.com/robots.txt
```

### 每週執行

```bash
# 1. GSC 檢查
@google-search-console status fun1399.com

# 2. 404 監控
# 檢查 Cloudflare Analytics 或 GSC Coverage report
```

### 每月執行

```bash
# 1. AI 搜尋可見度
@ai-seo check "娛樂城推薦"

# 2. 內部連結分析
@internal-linker analyze /path/to/fun1399-clean

# 3. Content gap 分析
@seo-content-brief research "娛樂城 2026"
```

---

## 九、總結

### 最推薦的 SEO 技能組合（TOP 3）

1. **🥇 seo-audit** — Technical SEO 全面檢查，涵蓋所有 on-page、structured data、crawlability
2. **🥈 google-search-console** — 數據驅動的索引與效能監控
3. **🥉 ai-seo** — 未來趨勢，AI 搜尋優化

### 技能系統最大缺失

1. **Core Web Vitals 自動化測量** — 需整合 lighthouse-ci
2. **爬蟲模擬** — 需自訂爬蟲腳本
3. **GSC API 自動化** — 需啟用 Search Console API

### 最值得補強的能力

| 補強項目 | 方法 | 預估時間 |
|----------|------|---------|
| **Lighthouse CI 整合** | GitHub Action + Pagespeed Insights | 2 小時 |
| **自訂爬蟲腳本** | Python + BeautifulSoup | 4 小時 |
| **GSC API 存取** | OAuth + API 呼叫 | 2 小時 |

### 是否需要額外安裝技能

| 建議 | 說明 |
|------|------|
| **不需要大量安裝** | 現有技能已覆蓋 80% 需求 |
| **建議啟用 3 個核心** | seo-audit、google-search-console、ai-seo |
| **其餘用自建腳本替代** | curl + grep + diff 已足夠 |

---

**報告產生時間**: 2026-05-20 20:30 CST  
**分析依據**: SKILL.md 文件內容 + 實際使用經驗  
**下次檢討**: 2026-06-20（一個月後評估技能使用效果）
