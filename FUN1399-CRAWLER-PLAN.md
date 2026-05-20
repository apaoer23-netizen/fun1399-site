# FUN1399 Custom SEO Crawler 規劃報告

**日期**: 2026-05-20  
**目標**: 建立 deploy 後自動執行的 SEO Crawler  
**範圍**: fun1399.com（~98 頁靜態站）  
**原則**: 規劃先行，不改動網站  

---

## 一、現有技能能力邊界分析

### 1.1 seo-audit 技能

| 能力 | 支援度 | 限制 |
|------|--------|------|
| **robots.txt** | ✅ 完整 | 可檢查 Allow/Disallow |
| **sitemap.xml** | ✅ 基本 | 可檢查存在，但無 URL 列表 |
| **meta title/description** | ✅ 完整 | 可解析所有頁面 |
| **canonical** | ✅ 基本 | curl + grep 可行 |
| **OG tags** | ✅ 基本 | 文字匹配 |
| **H1 檢查** | ✅ 基本 | 可檢查存在與數量 |
| **noindex** | ✅ 基本 | grep 檢查 |
| **JSON-LD** | ⚠️ 部分 | 提醒 web_fetch 無法檢測 JS-injected schema |
| **redirect chain** | ✅ 可檢查 | curl -L -w |
| **internal links** | ❌ 無 | 無爬蟲能力 |
| **broken links** | ❌ 無 | 需逐頁爬取 |
| **orphan pages** | ❌ 無 | 需建立圖 |
| **images 404/alt** | ❌ 無 | 需解析 HTML + 請求圖片 |
| **performance 細節** | ❌ 無 | 無 Core Web Vitals 測量 |
| **redirect loop** | ⚠️ 手動 | curl -L 可發現，但無自動 |

**結論**: seo-audit 是**知識型技能**（告訴你怎麼檢查），不是**自動化工具**（幫你執行全站檢查）。

### 1.2 internal-linker 技能

| 能力 | 支援度 | 限制 |
|------|--------|------|
| **orphan pages** | ✅ 有 | `@internal-linker analyze --orphan-pages` |
| **broken links** | ✅ 有 | `@internal-linker analyze --broken-links` |
| **link depth** | ✅ 有 | `@internal-linker analyze --link-depth` |
| **link distribution** | ✅ 有 | `@internal-linker analyze --distribution` |
| **build links** | ✅ 有 | `@internal-linker build` |
| **crawl simulation** | ❌ 無 | 無 status code 檢查 |
| **canonical 檢查** | ❌ 無 | 非連結相關 |
| **schema 檢查** | ❌ 無 | 非連結相關 |
| **redirect chain** | ❌ 無 | 非連結相關 |
| **sitemap consistency** | ❌ 無 | 需比對 sitemap vs 實際 |

**結論**: internal-linker 專精**連結結構**，但無法檢查 status code、redirect、canonical、schema 等技術元素。

### 1.3 seo-geo 技能（scripts/seo_audit.py）

現有腳本 `scripts/seo_audit.py` 能力：

| 能力 | 支援度 | 備註 |
|------|--------|------|
| **單頁 fetch** | ✅ 有 | urllib.request，timeout 30s |
| **title/description** | ✅ 有 | regex 解析 |
| **OG 基本檢查** | ✅ 有 | 只檢查 og:title 存在 |
| **JSON-LD 計數** | ✅ 有 | 計算 `<script type="application/ld+json">` 數量 |
| **H1 提取** | ✅ 有 | regex + 去除內標籤 |
| **robots.txt** | ✅ 有 | 檢查存在 + AI bots |
| **sitemap.xml 存在** | ✅ 有 | 檢查 `<urlset` 或 `<sitemapindex` |
| **load time** | ✅ 有 | 測量 fetch 時間 |
| **User-Agent** | ⚠️ 固定 | `"SEO-Audit/1.0"`，非 Googlebot |
| **多頁爬取** | ❌ 無 | 只能單頁 |
| **redirect chain** | ❌ 無 | 無 redirect 分析 |
| **internal links** | ❌ 無 | 無連結提取 |
| **canonical** | ❌ 無 | 未實作 |
| **images** | ❌ 無 | 未實作 |
| **sitemap URL 列表** | ❌ 無 | 只檢查存在，不解析 |
| **輸出格式** | ❌ 純文字 | 無 JSON/Markdown/HTML |

**結論**: 現有 `seo_audit.py` 是**單頁基礎檢查**，需要大幅擴充才能滿足 FUN1399 需求。

---

## 二、三者能力差異總結

| 需求 | seo-audit | internal-linker | seo_audit.py | Custom Crawler |
|------|-----------|-----------------|--------------|----------------|
| robots.txt 分析 | ✅ 知識 | ❌ | ✅ 基本 | ✅ 完整 |
| sitemap 解析 | ⚠️ 知識 | ❌ | ⚠️ 存在檢查 | ✅ URL 列表 + 比對 |
| 全站 status code | ❌ | ❌ | ❌ | ✅ 98 頁自動 |
| redirect chain | ⚠️ 手動 | ❌ | ❌ | ✅ 自動追蹤 |
| redirect loop | ⚠️ 手動 | ❌ | ❌ | ✅ 自動偵測 |
| canonical 檢查 | ⚠️ 手動 | ❌ | ❌ | ✅ 全站自動 |
| noindex 檢查 | ⚠️ 手動 | ❌ | ❌ | ✅ 全站自動 |
| JSON-LD 驗證 | ⚠️ 手動 | ❌ | ⚠️ 計數 | ✅ 提取 + 結構驗證 |
| OG 完整檢查 | ⚠️ 手動 | ❌ | ⚠️ 部分 | ✅ 全欄位 |
| internal links | ❌ | ✅ 完整 | ❌ | ✅ 完整 |
| broken links | ❌ | ✅ 完整 | ❌ | ✅ 完整 |
| orphan pages | ❌ | ✅ 完整 | ❌ | ✅ 完整 |
| image 404/alt | ❌ | ❌ | ❌ | ✅ 完整 |
| HTML size | ❌ | ❌ | ❌ | ✅ 有 |
| diff（Preview vs Production）| ❌ | ❌ | ❌ | ✅ 自動 |
| Markdown 報告 | ❌ | ❌ | ❌ | ✅ 自動 |

**結論**: 現有技能**無法覆蓋**「全站自動化 SEO 技術檢查」。Custom Crawler 是**必要補強**。

---

## 三、Custom Crawler 架構設計

### 3.1 核心架構

```
FUN1399 SEO Crawler
├── Crawler Engine（爬蟲引擎）
│   ├── URL Discovery（URL 發現）
│   │   ├── Sitemap Parser（sitemap.xml → URL 列表）
│   │   ├── Recursive Crawler（遞迴爬取內部連結）
│   │   └── URL Filter（排除外部連結、錨點、query string）
│   ├── Request Manager（請求管理）
│   │   ├── Googlebot User-Agent
│   │   ├── Rate Limiter（防 Cloudflare block）
│   │   ├── Retry Logic（重試機制）
│   │   └── Timeout & Error Handler
│   └── Response Analyzer（回應分析器）
│       ├── Status Code Inspector
│       ├── Redirect Chain Tracer
│       └── Header Analyzer
│
├── SEO Inspector（SEO 檢查器）
│   ├── Meta Inspector
│   │   ├── title（長度、重複、缺失）
│   │   ├── description（長度、重複、缺失）
│   │   ├── viewport
│   │   └── robots meta
│   ├── Canonical Inspector
│   │   ├── 存在檢查
│   │   ├── self-referencing 驗證
│   │   └── 一致性檢查（全站 canonical 策略）
│   ├── OG Inspector
│   │   ├── og:title, og:description, og:image, og:url, og:type
│   │   └── og:image 可存取性檢查
│   ├── Twitter Card Inspector
│   │   ├── twitter:card, twitter:title, twitter:image
│   │   └── twitter:image 可存取性
│   ├── Heading Inspector
│   │   ├── H1 數量（必須 = 1）
│   │   ├── H1 內容提取
│   │   └── H2-H6 層級結構
│   ├── Schema Inspector
│   │   ├── JSON-LD 提取
│   │   ├── @type 識別（Article, Organization, FAQPage, etc.）
│   │   └── 結構驗證（Python json 解析）
│   └── Image Inspector
│       ├── src 提取
│       ├── alt 屬性檢查
│       ├── HTTP 請求驗證（200?）
│       └── Content-Length 檢查（oversized?）
│
├── Link Analyzer（連結分析器）
│   ├── Internal Link Extractor（提取所有 `<a href>`）
│   ├── Broken Link Detector（HTTP 請求驗證）
│   ├── Link Graph Builder（NetworkX 有向圖）
│   ├── Orphan Page Detector（in_degree = 0）
│   ├── /team Link Auditor（/team 內鏈數量統計）
│   └── Redirected Link Detector（連到 301/302 的內部連結）
│
├── Sitemap Auditor（Sitemap 審計器）
│   ├── Sitemap Parser（`<loc>` 提取）
│   ├── URL Count（總數驗證）
│   ├── Crawlable Check（sitemap 中的 URL 是否 200）
│   └── Orphan Detection（crawl 到但不在 sitemap）
│
├── Redirect Auditor（Redirect 審計器）
│   ├── Chain Tracer（追蹤 redirect 路徑）
│   ├── Loop Detector（A→B→A 偵測）
│   ├── 301 vs 302 檢查（SEO-relevant 必須 301）
│   ├── .html Redirect 檢查
│   └── Trailing Slash 一致性
│
├── Performance Basic（基本性能）
│   ├── HTML Size（bytes）
│   ├── Image Count & Size
│   ├── External Resource Count（CSS/JS CDN）
│   └── Response Time（TTFB approximation）
│
├── Diff Engine（差異引擎）
│   ├── Preview vs Production Diff
│   │   ├── URL 列表比對
│   │   ├── Status Code 比對
│   │   ├── Meta 比對
│   │   ├── Canonical 比對
│   │   ├── Schema 比對
│   │   └── OG 比對
│   └── Cloudflare Migration Diff（遷移前後比對）
│
└── Report Generator（報告產生器）
    ├── Markdown Report（人類可讀，預設）
    ├── JSON Report（機器可讀，CI 整合）
    ├── HTML Report（視覺化，可選）
    └── Exit Code（CI: 0 = pass, 1 = fail）
```

### 3.2 資料流

```
輸入 URL
    ↓
[URL Discovery]
    ├── Sitemap 解析 → URL 列表 A
    └── 遞迴爬取 → URL 列表 B
    ↓
[URL 合併 + 去重] → 總 URL 列表
    ↓
[Request Manager] 並行請求（Rate Limited）
    ↓
[Response Analyzer] → (status, headers, body, redirect_chain)
    ↓
[Parallel Inspectors]
    ├── Meta Inspector → meta_report
    ├── Canonical Inspector → canonical_report
    ├── OG Inspector → og_report
    ├── Schema Inspector → schema_report
    ├── Image Inspector → image_report
    ├── Link Analyzer → link_report
    └── Redirect Auditor → redirect_report
    ↓
[Report Aggregator]
    ↓
[Diff Engine]（如有兩組資料）
    ↓
[Report Generator] → Markdown / JSON / HTML
```

---

## 四、技術方案比較

### 4.1 Python vs Node.js vs Go

| 維度 | Python 3 | Node.js | Go |
|------|----------|---------|-----|
| **生態** | BeautifulSoup, requests, lxml, networkx | axios, cheerio, puppeteer | goquery, colly |
| **學習曲線** | 低（團隊熟悉）| 中 | 高 |
| **性能** | 中（98 頁足夠）| 中 | 高（過剩）|
| **並行** | asyncio + aiohttp | async/await | goroutine |
| **HTML 解析** | BeautifulSoup（強大）| cheerio（jQuery-like）| goquery（jQuery-like）|
| **JSON 處理** | 原生（強）| 原生（強）| 原生（強）|
| **Report 產生** | Markdown/json 簡單 | Markdown/json 簡單 | 稍繁瑣 |
| **相依數量** | 中（~5 個）| 中（~5 個）| 少 |
| **執行環境** | 已安裝（OpenClaw host）| 需安裝 | 需安裝 |
| **現有基礎** | 有 seo_audit.py | 無 | 無 |

**推薦**: **Python 3 + asyncio**

原因：
1. 團隊已熟悉（現有 seo_audit.py 是 Python）
2. 98 頁網站，Python asyncio 效能足夠
3. BeautifulSoup HTML 解析最強大
4. 相依少（requests, beautifulsoup4, networkx, lxml）
5. 可直接在 OpenClaw host 執行

### 4.2 相依套件

```
# requirements.txt
requests>=2.31.0
beautifulsoup4>=4.12.0
lxml>=4.9.0
aiohttp>=3.9.0
networkx>=3.2.0
```

**總計 5 個套件，均為主流套件，維護活躍。**

---

## 五、執行時間與負載評估

### 5.1 對 98 頁網站的預估時間

| 模式 | 頁數 | 並行度 | 預估時間 | 說明 |
|------|------|--------|----------|------|
| **基本模式** | 98 | 5 req/sec | ~20 秒 | 只檢查 status + meta |
| **標準模式** | 98 | 3 req/sec | ~35 秒 | + canonical + OG + schema |
| **深度模式** | 98 | 2 req/sec | ~50 秒 | + image 驗證 + 連結圖 |
| **全站 diff** | 196（Preview+Production）| 2 req/sec | ~100 秒 | 兩組全站比對 |

### 5.2 Cloudflare Rate Limit 風險

| 風險 | 評估 |
|------|------|
| **Rate Limit** | Cloudflare Free Plan 無明確 rate limit，但過快可能觸發 WAF |
| **安全並行度** | 2-3 req/sec（每頁 ~1-2KB HTML）|
| **總流量** | 98 頁 × 50KB = ~5MB（極低）|
| **IP 風險** | 單一 IP 短时间大量請求可能觸發 challenge |
| **建議** | 增加 delay（每請求 300-500ms），設定 `CF-Visitor` header |
| **User-Agent** | `Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` |

### 5.3 負載安全評估

| 檢查項 | 影響 | 評估 |
|--------|------|------|
| **CPU** | HTML 解析 + regex | 低（單頁 < 10ms）|
| **Memory** | 儲存 98 頁 HTML | ~10MB（極低）|
| **Network** | 98 次 HTTP 請求 | 安全（間隔 300ms）|
| **Disk** | 報告輸出 | ~50KB Markdown |
| **對網站影響** | 98 次額外請求 | 可忽略（Cloudflare cache 會命中）|

**結論**: 對 98 頁網站完全安全，無 rate limit 風險（前提是 2-3 req/sec）。

---

## 六、輸出格式設計

### 6.1 Markdown Report（預設，人類可讀）

```markdown
# FUN1399 SEO Crawl Report

**日期**: 2026-05-20 18:30 CST  
**目標**: https://fun1399.com  
**頁面數**: 98  
**執行時間**: 35.2s  

---

## 🚨 Critical Issues (3)

### C1: Orphan Page — /articles/new-post.html
- **影響**: Google 可能無法發現此頁面
- **建議**: 從首頁或相關文章增加內鏈

### C2: Broken Image — /static/images/missing.jpg
- **位置**: /articles/mbm-review.html
- **狀態**: 404
- **建議**: 更新圖片路徑或移除引用

### C3: Redirect Chain — /old-path
- **路徑**: /old-path → /intermediate → /new-path
- **深度**: 3（建議 ≤ 2）
- **建議**: 直接 /old-path → /new-path

---

## ⚠️ Warnings (5)

### W1: Missing OG Image
- **頁面**: /contact.html
- **缺失**: og:image

### W2: Multiple H1
- **頁面**: /articles/nba-betting.html
- **數量**: 2
- **H1s**: [...]

---

## ✅ Passes (90)

| 檢查項 | 通過 | 失敗 |
|--------|------|------|
| Status 200 | 95 | 0 |
| Canonical | 98 | 0 |
| OG Tags | 97 | 1 |
| Schema | 85 | 0 |
| No Orphan | 97 | 1 |

---

## 📊 Statistics

| 指標 | 數值 |
|------|------|
| 平均載入時間 | 0.45s |
| 最大 HTML | 45KB |
| 總圖片數 | 234 |
| 圖片 404 | 1 |
| 內部連結總數 | 1,247 |
| Broken 內鏈 | 0 |

---

## 🔗 Orphan Pages

| # | URL | 建議 |
|---|-----|------|
| 1 | /articles/new-post.html | 從首頁增加連結 |

---

## 🔀 Redirect Summary

| 類型 | 數量 |
|------|------|
| 301 | 12 |
| 308 | 8 |
| 302 | 0 ✅ |
| Chain > 2 | 1 ⚠️ |

---

*Generated by FUN1399 SEO Crawler v1.0*
```

### 6.2 JSON Report（機器可讀，CI 整合）

```json
{
  "meta": {
    "url": "https://fun1399.com",
    "date": "2026-05-20T18:30:00+08:00",
    "pages_crawled": 98,
    "duration_seconds": 35.2
  },
  "summary": {
    "critical": 3,
    "warnings": 5,
    "passes": 90
  },
  "issues": [
    {
      "severity": "critical",
      "type": "orphan_page",
      "url": "https://fun1399.com/articles/new-post.html",
      "message": "No internal links point to this page",
      "fix": "Add link from homepage or related articles"
    },
    {
      "severity": "critical",
      "type": "broken_image",
      "url": "https://fun1399.com/articles/mbm-review.html",
      "resource": "https://fun1399.com/static/images/missing.jpg",
      "status": 404,
      "fix": "Update image path or remove reference"
    }
  ],
  "pages": [
    {
      "url": "https://fun1399.com/",
      "status": 200,
      "canonical": "https://fun1399.com/",
      "title": "娛樂城玩家俱樂部 | 最專業的娛樂城評測與分析",
      "title_length": 32,
      "description": "...",
      "h1_count": 1,
      "h1_text": "娛樂城玩家俱樂部",
      "og_complete": true,
      "schema_types": ["Organization", "WebSite"],
      "internal_links": 12,
      "load_time": 0.42
    }
  ],
  "redirects": {
    "total": 20,
    "by_status": {"301": 12, "308": 8, "302": 0},
    "chains_over_2": 1
  },
  "images": {
    "total": 234,
    "with_alt": 228,
    "without_alt": 6,
    "broken": 1
  },
  "orphan_pages": [
    "https://fun1399.com/articles/new-post.html"
  ]
}
```

### 6.3 Diff Report（Preview vs Production）

```markdown
# FUN1399 Deploy Diff Report

**Preview**: https://abc123.pages.dev  
**Production**: https://fun1399.com  

## 🔴 Regression Issues

| 類型 | Preview | Production | 狀態 |
|------|---------|------------|------|
| /team canonical | https://abc123.pages.dev/team.html | https://fun1399.com/team.html | ❌ Mismatch |

## 🟢 Improvements

| 類型 | Preview | Production | 狀態 |
|------|---------|------------|------|
| sitemap URL count | 91 | 93 | ✅ +2 |

## ➡️ Unchanged

| 類型 | 狀態 |
|------|------|
| robots.txt | ✅ Identical |
| redirect rules | ✅ Identical |
```

---

## 七、實施計畫

### Phase 1: 核心爬蟲（2h）

| 任務 | 時間 | 產出 |
|------|------|------|
| URL Discovery（sitemap + recursive）| 0.5h | `crawler.py` |
| Request Manager（asyncio + rate limit）| 0.5h | `fetcher.py` |
| Response Analyzer（status + headers）| 0.5h | `analyzer.py` |
| Report Generator（Markdown）| 0.5h | `reporter.py` |

### Phase 2: SEO 檢查器（2h）

| 任務 | 時間 | 產出 |
|------|------|------|
| Meta Inspector | 0.5h | `inspectors/meta.py` |
| Canonical + OG Inspector | 0.5h | `inspectors/og_canonical.py` |
| Schema Inspector | 0.5h | `inspectors/schema.py` |
| Heading Inspector | 0.5h | `inspectors/heading.py` |

### Phase 3: 進階分析（2h）

| 任務 | 時間 | 產出 |
|------|------|------|
| Link Analyzer（internal + broken）| 0.75h | `analyzers/links.py` |
| Image Inspector | 0.5h | `inspectors/images.py` |
| Redirect Auditor | 0.5h | `analyzers/redirects.py` |
| Sitemap Auditor | 0.25h | `analyzers/sitemap.py` |

### Phase 4: Diff 引擎 + CLI（1h）

| 任務 | 時間 | 產出 |
|------|------|------|
| Diff Engine | 0.5h | `diff.py` |
| CLI Interface（argparse）| 0.5h | `fun1399_crawler.py` |

### Phase 5: 整合測試（1h）

| 任務 | 時間 |
|------|------|
| 全站測試（98 頁）| 0.5h |
| Bug fix + 優化 | 0.5h |

### 總計時間: **8 小時**

---

## 八、檔案結構

```
scripts/fun1399-crawler/
├── fun1399_crawler.py          # 主入口
├── requirements.txt            # 相依
├── config.py                   # 設定（URL, rate limit, timeouts）
├── core/
│   ├── __init__.py
│   ├── fetcher.py              # HTTP fetcher（asyncio + rate limit）
│   ├── parser.py               # HTML parser（BeautifulSoup）
│   └── sitemap.py              # Sitemap.xml parser
├── inspectors/
│   ├── __init__.py
│   ├── meta.py                 # Title, description, viewport
│   ├── canonical.py            # Canonical URL
│   ├── og.py                   # Open Graph
│   ├── twitter.py              # Twitter Card
│   ├── heading.py              # H1-H6
│   ├── schema.py               # JSON-LD
│   ├── images.py               # Image src + alt + status
│   └── robots.py               # robots.txt + X-Robots-Tag
├── analyzers/
│   ├── __init__.py
│   ├── links.py                # Internal link graph
│   ├── redirects.py            # Redirect chain + loop
│   ├── sitemap_auditor.py      # Sitemap vs crawl consistency
│   └── performance.py          # Basic performance metrics
├── diff/
│   ├── __init__.py
│   └── engine.py               # Preview vs Production diff
├── reporters/
│   ├── __init__.py
│   ├── markdown.py             # Markdown report generator
│   ├── json_reporter.py        # JSON report generator
│   └── html_reporter.py        # HTML report generator（可選）
└── reports/                     # 輸出目錄（.gitignore）
    └── .gitkeep
```

---

## 九、CLI 介面設計

```bash
# 基本用法：爬取全站
python3 fun1399_crawler.py https://fun1399.com

# 指定模式
python3 fun1399_crawler.py https://fun1399.com --mode=full      # 深度模式
python3 fun1399_crawler.py https://fun1399.com --mode=fast      # 基本模式（只 status + meta）
python3 fun1399_crawler.py https://fun1399.com --mode=links     # 只檢查連結

# 只檢查 sitemap 中的 URL
python3 fun1399_crawler.py https://fun1399.com --sitemap-only

# 只檢查單頁
python3 fun1399_crawler.py https://fun1399.com/team.html --single

# Diff 模式
python3 fun1399_crawler.py \
  --preview=https://abc123.pages.dev \
  --production=https://fun1399.com \
  --mode=diff

# 輸出格式
python3 fun1399_crawler.py https://fun1399.com --format=markdown   # 預設
python3 fun1399_crawler.py https://fun1399.com --format=json       # JSON
python3 fun1399_crawler.py https://fun1399.com --format=html      # HTML

# 輸出到檔案
python3 fun1399_crawler.py https://fun1399.com -o reports/2026-05-20-crawl.md

# CI 模式（exit code 1 if issues found）
python3 fun1399_crawler.py https://fun1399.com --ci

# 調整 rate limit（預設 3 req/sec）
python3 fun1399_crawler.py https://fun1399.com --rate-limit=5
```

---

## 十、是否值得建立？

### 10.1 成本

| 項目 | 成本 |
|------|------|
| 開發時間 | 8 小時 |
| 相依套件 | 5 個 Python 套件（均免費）|
| 執行時間 | ~35 秒/次 |
| 維護成本 | 低（靜態站結構穩定）|

### 10.2 收益

| 收益 | 價值 |
|------|------|
| **提前發現問題** | 每次 deploy 避免潛在 SEO 損失 |
| **節省人工** | 原本手動檢查 ~30 分鐘 → 自動 35 秒 |
| **全面覆蓋** | 98 頁全檢查，人工易遺漏 |
| **歷史追蹤** | 報告存檔，可追溯問題時間點 |
| **CI 整合** | GitHub Action 自動執行 |
| **遷移保護** | Cloudflare / 未來遷移的 safety net |

### 10.3 ROI 計算

| 情境 | 效益 |
|------|------|
| 發現 1 次 orphan page | 避免該頁面永遠不被索引 |
| 發現 1 次 broken link | 避免使用者流失 + 爬蟲浪費 budget |
| 發現 1 次 302 redirect | 避免 SEO 權重流失 |
| 節省人工時間 | 每次 deploy 節省 ~25 分鐘 |

**結論**: 8 小時開發，每次 deploy 節省 25 分鐘，發現 1 次重大問題即回本。

---

## 十一、與現有技能的整合

### 11.1 使用時機

| 時機 | 行動 |
|------|------|
| **每次 deploy 後** | 執行 crawler → 產生報告 → 有問題通知 Hans |
| **每週固定** | 執行 crawler → 追蹤趨勢變化 |
| **遷移前** | Preview crawl → 遷移後 Production crawl → diff |
| **收到 GSC 異常時** | 執行 crawler 定位問題 |

### 11.2 與現有技能協作

```
Deploy 後 Workflow:
1. git push → Cloudflare Pages deploy
2. 等待 2 分鐘（deploy 完成）
3. 執行 crawler:
   python3 scripts/fun1399-crawler/fun1399_crawler.py https://fun1399.com --ci
4. 若 exit code 0:
   → 通過，記錄報告
5. 若 exit code 1:
   → 讀取報告
   → 若 Critical: 通知 Hans，評估 rollback
   → 若 Warning: 記錄待修
6. 同時執行:
   @internal-linker analyze /path/to/site --orphan-pages
   （補強連結結構分析）
```

---

## 十二、風險與緩解

| 風險 | 可能性 | 影響 | 緩解 |
|------|--------|------|------|
| Cloudflare block | 低 | 高 | rate limit 3 req/sec，模擬 Googlebot |
| HTML 結構變更 | 中 | 中 | 用 BeautifulSoup 彈性解析 |
| 執行時間過長 | 低 | 低 | 並行 3 req/sec，98 頁 ~35 秒 |
| 記憶體不足 | 極低 | 低 | 98 頁 HTML < 10MB |
| 套件維護停止 | 低 | 中 | 選擇主流套件（requests, BeautifulSoup）|
| 誤報（false positive）| 中 | 低 | 設定 severity 分級，手動確認 Critical |

---

## 十三、最終建議

### 強烈建議建立

| 理由 | 說明 |
|------|------|
| **現有技能無法覆蓋** | seo-audit 是知識型，internal-linker 是連結型，均無全站自動化技術檢查 |
| **ROI 極高** | 8 小時開發，永久使用，每次 deploy 節省 25 分鐘 |
| **預防勝於治療** | 在 Google 發現問題前先自行發現 |
| **遷移保護** | Cloudflare 剛遷移，需要持續監控 |
| **規模化基礎** | 未來若網站擴大到 500+ 頁，crawler 直接適用 |

### 實施順序

| 順序 | 任務 | 時間 | 產出 |
|------|------|------|------|
| 1 | Phase 1: 核心爬蟲 | 2h | 可執行基礎版 |
| 2 | Phase 2: SEO 檢查器 | 2h | 可檢查 meta/canonical/OG/schema |
| 3 | **暫停評估** | — | Hans 確認是否繼續 |
| 4 | Phase 3: 進階分析 | 2h | 連結圖 + redirect + image |
| 5 | Phase 4: Diff 引擎 | 1h | Preview vs Production |
| 6 | Phase 5: 整合測試 | 1h | 穩定版 v1.0 |

**建議**: 先完成 Phase 1+2（4 小時），產出可用版本，Hans 確認後再完成 Phase 3-5。

---

## 十四、附錄：現有技能無法替代的原因

| 現有技能 | 為何無法替代 Custom Crawler |
|----------|---------------------------|
| **seo-audit** | 知識型技能，告訴你「怎麼檢查」，不會自動爬全站 98 頁 |
| **internal-linker** | 專精連結，但無 status code、redirect、canonical、schema 檢查 |
| **seo-geo / seo_audit.py** | 單頁檢查，無全站爬取、無連結分析、無 diff |
| **google-search-console** | 分析 GSC 數據，但無法在 deploy 後立即檢查 |

**唯一可行的替代**: 用大量 curl + grep 手動組合腳本，但維護成本遠高於建立專用 crawler。

---

*規劃完成時間: 2026-05-20 21:45 CST*  
*等待 Hans 指示是否開始 Phase 1 實作*
