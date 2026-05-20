# FUN1399 SEO 工作流程

**版本**: 1.0  
**日期**: 2026-05-20  
**適用**: fun1399.com Cloudflare Pages  
**原則**: 穩定 > 擴張，Technical SEO > Content Volume  

---

## 已啟用技能

| 技能 | 用途 | 觸發時機 |
|------|------|---------|
| **seo-audit** | Technical SEO 全面檢查 | 每次 deploy 後 |
| **internal-linker** | 內部連結結構分析 | 每次 deploy + 每週 |
| **google-search-console** | GSC 數據與索引監控 | 每週 |
| **ai-seo** | AI 搜尋可見度分析 | 每週 |

---

## Workflow 總覽

```
每次 Deploy 後（自動）
├── 1. deploy-seo-checklist.md — 5 大檢查
├── 2. internal-linker — orphan + 連結結構
├── 3. production-vs-preview diff — 回歸測試
└── 4. redirect-verification-checklist.md — 舊網址保護

每週固定（排程）
├── 1. weekly-seo-checklist.md — GSC + AI + 內鏈
└── 2. 記憶檔更新 — MEMORY.md + 本逊報告

每月（排程）
├── 1. 完整站點爬蟲（custom crawler）
├── 2. orphan pages 深度分析
└── 3. content freshness 檢查

遷移期間（額外）
└── cloudflare-migration-seo-checklist.md
```

---

## 文件位置

| 文件 | 路徑 |
|------|------|
| 本 workflow | `checklists/FUN1399-SEO-WORKFLOW.md` |
| Deploy 檢查清單 | `checklists/deploy-seo-checklist.md` |
| 每週檢查清單 | `checklists/weekly-seo-checklist.md` |
| Redirect 驗證 | `checklists/redirect-verification-checklist.md` |
| Cloudflare 遷移 | `checklists/cloudflare-migration-seo-checklist.md` |
| SEO Diff 腳本 | `/tmp/seo_diff.sh`（已定義） |
| Production Audit | `/tmp/cloudflare_production_audit.sh`（已定義） |

---

## 執行方式

### 每次 Deploy 後（手動/自動）

```bash
# 1. 執行 seo-audit 技能
@seo-audit analyze https://fun1399.com

# 2. 執行 internal-linker
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --orphan-pages --broken-links

# 3. 執行 diff
bash /tmp/seo_diff.sh

# 4. 檢查清單
read /root/.openclaw/workspace/checklists/deploy-seo-checklist.md
```

### 每週固定（排程建議）

```bash
# 1. GSC 檢查
@google-search-console status fun1399.com

# 2. AI SEO 檢查
@ai-seo check "娛樂城推薦"

# 3. 內部連結
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --link-depth --distribution
```

---

## 評估結論：補強項目優先順序

### 🔴 優先 #1：Googlebot Crawl Simulation（custom crawler）

| 項目 | 評估 |
|------|------|
| **實際幫助** | ⭐⭐⭐⭐⭐ 最高 — 能發現 deploy 後的隱藏 404、broken links、redirect loops |
| **對 indexing 影響** | 直接 — 確保所有重要頁面可被爬取 |
| **實施難度** | 低 — Python + requests + BeautifulSoup，約 2 小時 |
| **ROI** | 最高 — 一次建立，每次 deploy 自動執行 |

**建議**: 立即實作。模擬 Googlebot 爬取全站 98 頁，檢查 status code、redirect chain、canonical consistency。

---

### 🟡 優先 #2：Internal Link Graph（可視化）

| 項目 | 評估 |
|------|------|
| **實際幫助** | ⭐⭐⭐⭐ 高 — 發現 orphan pages、權重分配不均、cluster 薄弱點 |
| **對 indexing 影響** | 間接 — 改善 crawl budget 分配 |
| **實施難度** | 中 — Python + networkx 產生圖表 |
| **ROI** | 高 — 每月執行一次即可 |

**建議**: 第二階段實作。產生內部連結圖，標註 orphan、hub pages、cluster 邊界。

---

### 🟢 優先 #3：Lighthouse CI

| 項目 | 評估 |
|------|------|
| **實際幫助** | ⭐⭐⭐ 中 — Core Web Vitals 自動化測量 |
| **對 indexing 影響** | 中 — CWV 是排名因素但非決定性 |
| **實施難度** | 低 — GitHub Action 整合 |
| **ROI** | 中 — Cloudflare 已自動優化大部分 |

**建議**: 第三階段實作。Cloudflare 的 CDN + Polish 已處理 80%，lighthouse-ci 主要用於監控異常。

---

## 結論

| 優先順序 | 補強項目 | 預估時間 | 執行時機 |
|----------|---------|---------|---------|
| **#1** | Googlebot Crawl Simulation | 2 小時 | 立即 |
| **#2** | Internal Link Graph | 3 小時 | 1 週後 |
| **#3** | Lighthouse CI | 1 小時 | 2 週後 |

**最快提升 indexing 穩定性**: #1 Custom Crawler — 確保每次 deploy 後全站可爬取，無隱藏 404。

---

## 禁止清單（堅守）

- ❌ 不安裝新 content SEO skills
- ❌ 不追求文章數暴增
- ❌ 不做 keyword stuffing
- ❌ 不修改正式 DNS（除非明確授權）
- ❌ 不刪除 Netlify site（rollback 保險）

---

*最後更新: 2026-05-20*
