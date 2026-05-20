# FUN1399 SEO Workflow

**版本**: 1.0  
**日期**: 2026-05-20  
**適用**: fun1399.com（Cloudflare Pages）  
**原則**: 穩定 > 擴張，Technical SEO > Content Volume  

---

## 一、啟用技能與使用時機

| 技能 | 用途 | 觸發時機 | 執行時間 |
|------|------|---------|---------|
| **seo-audit** | Technical SEO 全面檢查（canonical、sitemap、schema、redirect、robots、status code、OG、noindex、404） | 每次 deploy 後 | ~3 分鐘 |
| **internal-linker** | 內部連結結構分析、orphan pages 檢測、權重分配 | 每次 deploy + 每週 | ~2 分鐘 |
| **google-search-console** | GSC 數據與索引監控、Core Web Vitals、coverage | 每週 | ~3 分鐘 |
| **ai-seo** | AI 搜尋可見度（ChatGPT/Perplexity）、GEO 優化、EEAT | 每週 | ~2 分鐘 |

---

## 二、每次 Deploy 後 SEO 檢查清單

**觸發時機**: Git push → Cloudflare Pages deploy 完成後  
**執行時間**: ~5 分鐘  
**工具**: seo-audit + internal-linker + curl + 自訂腳本  

### 2.1 Canonical 檢查

```bash
# 首頁
curl -sL "https://fun1399.com" | grep -o 'rel="canonical"[^>]*'
# 文章頁
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -o 'rel="canonical"[^>]*'
# 分類頁
curl -sL "https://fun1399.com/articles/" | grep -o 'rel="canonical"[^>]*'
```

- [ ] 所有頁面有 `rel="canonical"`
- [ ] 指向 `https://fun1399.com/`（HTTPS + apex，無 www）
- [ ] 文章頁為 self-referencing
- [ ] 無多餘 trailing slash（`.html` 頁面）

### 2.2 Sitemap 檢查

```bash
curl -sI "https://fun1399.com/sitemap.xml" | grep -i "HTTP/"
curl -s "https://fun1399.com/sitemap.xml" | grep -c "<loc>"
curl -s "https://fun1399.com/robots.txt" | grep -i "sitemap"
```

- [ ] Status: 200 OK
- [ ] URL 總數: ~91-98（符合實際頁面數）
- [ ] 包含 `/team`
- [ ] 無 `.bak`、無測試頁面
- [ ] robots.txt 引用 sitemap

### 2.3 Schema 檢查

```bash
curl -sL "https://fun1399.com" | grep -A 30 'application/ld+json'
curl -sL "https://fun1399.com/team.html" | grep -A 50 'application/ld+json'
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -A 50 'application/ld+json'
```

- [ ] 首頁: Organization / WebSite schema
- [ ] 文章頁: Article schema（author、datePublished）
- [ ] /team: Organization + Person schema
- [ ] `name` 為「娛樂城玩家俱樂部」

### 2.4 Redirect 檢查

```bash
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
curl -sI -o /dev/null -w "%{http_code}" "https://www.fun1399.com"
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review"
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/team"
```

- [ ] HTTP → HTTPS: 301
- [ ] www → apex: 301
- [ ] 無 `.html` → `.html`: 308（Cloudflare 正常）或 301
- [ ] 無 302

### 2.5 robots.txt 檢查

```bash
curl -s "https://fun1399.com/robots.txt"
```

- [ ] `User-agent: *` + `Allow: /`
- [ ] `Disallow: /admin/`、`/api/`
- [ ] `Sitemap:` 引用正確
- [ ] 未阻擋 `GPTBot`、`ChatGPT-User`、`PerplexityBot`、`ClaudeBot`

### 2.6 Status Code 檢查

```bash
for page in / /articles/mbm-review.html /team.html /articles/ /reviews/ /sitemap.xml /robots.txt /og-image.jpg; do
  echo -n "$page: "
  curl -sI -o /dev/null -w "%{http_code}\n" "https://fun1399.com$page"
done
```

- [ ] 首頁: 200
- [ ] 文章頁: 200
- [ ] /team: 200
- [ ] /sitemap.xml: 200
- [ ] /robots.txt: 200
- [ ] /og-image.jpg: 200
- [ ] 不存在 URL: 404（有 404.html）

### 2.7 OG / Meta 檢查

```bash
curl -sL "https://fun1399.com" | grep -E '<title>|<meta name="description"'
curl -sL "https://fun1399.com" | grep -E '<meta property="og:'
curl -sL "https://fun1399.com" | grep -E '<meta name="twitter:'
```

- [ ] Title: 50-60 字元
- [ ] Description: 150-160 字元
- [ ] og:title、og:description、og:image、og:url
- [ ] twitter:card = summary_large_image

### 2.8 Noindex 檢查

```bash
curl -sL "https://fun1399.com" | grep -i 'noindex'
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -i 'noindex'
curl -sL "https://fun1399.com/team.html" | grep -i 'noindex'
```

- [ ] 重要頁面無 noindex
- [ ] 測試頁面如有應有 `noindex, nofollow`

### 2.9 Mobile 基本檢查

```bash
curl -sL "https://fun1399.com" | grep -o 'viewport[^>]*'
curl -sL "https://fun1399.com" | grep -o 'theme-color[^>]*'
curl -sI -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)" -o /dev/null -w "%{http_code}" "https://fun1399.com"
```

- [ ] `width=device-width, initial-scale=1`
- [ ] theme-color 存在
- [ ] Mobile User-Agent 返回 200

### 2.10 Content Integrity

```bash
curl -sL "https://fun1399.com" | grep -c '<h1'
curl -sL "https://fun1399.com" | grep '娛樂城玩家俱樂部'
curl -sL "https://fun1399.com/team.html" | grep 'Diana\|Molly\|Ethan'
```

- [ ] 每頁有且僅有 1 個 `<h1>`
- [ ] 品牌名稱「娛樂城玩家俱樂部」存在
- [ ] /team 分析師人名存在
- [ ] GA4 追蹤碼存在

### 2.11 Internal Link 檢查

```bash
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --orphan-pages --broken-links
```

- [ ] 無 broken internal links
- [ ] Orphan pages < 5
- [ ] 重要頁面有足夠內鏈

### 2.12 Diff 檢查（Production vs Preview）

```bash
bash /tmp/seo_diff.sh
```

- [ ] Canonical 一致
- [ ] Sitemap URL 數一致
- [ ] robots.txt 一致
- [ ] 無新增 noindex
- [ ] OG 結構一致

---

## 三、每週 SEO 檢查清單

**觸發時機**: 每週一次（建議週一 10:00）  
**執行時間**: ~10 分鐘  
**工具**: google-search-console + ai-seo + internal-linker  

### 3.1 Google Search Console

- [ ] **Coverage**: Valid > 90，Error = 0
- [ ] **Performance**: impressions、clicks、CTR、position
- [ ] **熱門查詢**: 前 10 穩定，品牌詞有 impression
- [ ] **Core Web Vitals**: LCP/INP/CLS = Good 或 Need Improvement
- [ ] **Crawl Stats**: 無大量 404 crawl

### 3.2 AI SEO 分析

```bash
curl -s "https://fun1399.com/robots.txt" | grep -E "GPTBot|ChatGPT-User|PerplexityBot|ClaudeBot"
curl -sL "https://fun1399.com/team.html" | grep -A 5 'FAQPage'
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -E 'author|datePublished'
```

- [ ] 4 大 AI bot 均 Allow
- [ ] /team 有 FAQPage Schema（5-8 題）
- [ ] 文章有 author + datePublished
- [ ] 段落 2-3 句話，結論前置

### 3.3 Internal Link Audit

```bash
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --link-depth --distribution
```

| 頁面 | 連入目標 | 實際連入 |
|------|---------|---------|
| 首頁 | — | — |
| /team | 全站導航 + 5+ 文章 | ___ |
| /about | 3+ | ___ |
| /contact | 3+ | ___ |

- [ ] Orphan < 5
- [ ] /team 連入 > 5
- [ ] Pillar/cluster 結構完整

### 3.4 Content Freshness

```bash
cd /root/.openclaw/workspace/fun1399-clean && git log --since="1 week ago" --name-only --oneline
```

- [ ] 上週更新文章: ___ 篇
- [ ] 無過期內容（如「2025 最佳」）
- [ ] 最新文章有正確 datePublished

### 3.5 競爭對手監控

- [ ] 對手是否有新頁面（site:qttheluxe.com 等）
- [ ] 品牌詞「娛樂城玩家俱樂部」是否 #1

---

## 四、Redirect 驗證檢查清單

**觸發時機**: 每次 deploy + DNS 變更 + 新增 redirect 規則後  
**執行時間**: ~3 分鐘  

### 4.1 重要舊網址

```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/wp-login.php"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/wp-admin"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/xmlrpc.php"
```

- [ ] 所有已知舊網址返回 301/308
- [ ] Location header 正確
- [ ] 無 redirect loop

### 4.2 .html Redirect

```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles/mbm-review"
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review.html"
```

- [ ] 一致性（全有或全無 `.html`）
- [ ] 無 200 重複內容
- [ ] 無 double redirect

### 4.3 Trailing Slash

```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles/"
```

- [ ] `/articles` → `/articles/`（或反向，一致性即可）
- [ ] `.html/` 返回 301 或 404（不應 200）

### 4.4 301 vs 302

```bash
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
curl -sI -o /dev/null -w "%{http_code}" "https://www.fun1399.com"
```

- [ ] HTTP→HTTPS: 301
- [ ] www→apex: 301
- [ ] 舊網址→新網址: 301/308
- [ ] **無 302**

### 4.5 Redirect Chain

```bash
curl -sIL -o /dev/null -w "%{http_code}\n" "http://www.fun1399.com/old-path"
```

- [ ] Chain depth ≤ 2
- [ ] 無 loop
- [ ] 最終 URL 200 OK

### 4.6 Cloudflare Pages 特點

| 情況 | Cloudflare Pages | Netlify |
|------|-----------------|---------|
| `.html` redirect | 308 | 301 |
| trailing slash | 308 | 301 |

- [ ] 返回 308（等同 301，Google 視為 permanent）
- [ ] 非 302

### 4.7 _redirects 檔案驗證

```bash
cat /root/.openclaw/workspace/fun1399-clean/_redirects | wc -l
```

- [ ] 規則數穩定（基準: ~75 行）
- [ ] 無新增/遺漏

---

## 五、Cloudflare Migration SEO 檢查清單

**狀態**: ✅ 遷移已完成（2026-05-20）  
**用途**: 驗證遷移後 SEO 完整性 + 未來 rollback 參考  

### 5.1 DNS 驗證

```bash
dig NS fun1399.com +short
dig A fun1399.com +short
dig A www.fun1399.com +short
```

- [ ] NS 為 Cloudflare（`*.cloudflare.com`）
- [ ] A 紀錄指向 Cloudflare Pages IPs
- [ ] 無 MX/TXT 異常

### 5.2 SSL/TLS

```bash
echo | openssl s_client -servername fun1399.com -connect fun1399.com:443 2>/dev/null | openssl x509 -noout -issuer -subject -dates
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
```

- [ ] Issuer: Cloudflare Inc
- [ ] CN=fun1399.com
- [ ] HTTP → 301 → HTTPS
- [ ] 未過期

### 5.3 Cloudflare Pages 設定

- [ ] Production branch: `main`
- [ ] Custom Domain: fun1399.com Active
- [ ] www → apex redirect Active
- [ ] 無 Cloudflare Functions（純靜態）

### 5.4 SEO 元素遷移驗證

```bash
curl -sL "https://fun1399.com" | grep -E '<title>|<meta name="description"'
curl -sL "https://fun1399.com" | grep 'rel="canonical"'
curl -sL "https://fun1399.com" | grep -A 20 'application/ld+json'
curl -s "https://fun1399.com/robots.txt"
curl -s "https://fun1399.com/sitemap.xml" | grep -c '<loc>'
```

- [ ] Title、Description 與遷移前一致
- [ ] Canonical 正確
- [ ] OG 完整，og:image 200
- [ ] Schema 存在
- [ ] robots.txt 一致
- [ ] Sitemap URL 數一致（~93）

### 5.5 Redirect 驗證

- [ ] HTTP→HTTPS: 301
- [ ] www→apex: 301
- [ ] `.html` redirect: 308
- [ ] 無 302

### 5.6 性能驗證

```bash
curl -sI -o /dev/null -w "%{time_total}" "https://fun1399.com"
curl -sI "https://fun1399.com" | grep -E "CF-Cache-Status|cache-control"
```

- [ ] TTFB < 500ms
- [ ] `CF-Cache-Status: HIT`（第二次請求）

### 5.7 Rollback 準備

- [ ] Netlify site 未刪除（備用）
- [ ] GoDaddy 帳號可登入
- [ ] 原 NS 值已記錄（ns27/ns28.domaincontrol.com）
- [ ] 回滾步驟清晰

### 5.8 遷移後監控

**遷移後 1 週內每日檢查**:
- [ ] 首頁 200
- [ ] /articles 200
- [ ] /team 200
- [ ] sitemap.xml 200
- [ ] 不存在 URL 404

**遷移後 1 個月內每週檢查**:
- [ ] GSC Coverage 無異常 drop
- [ ] 排名無大幅波動
- [ ] Impressions 穩定

---

## 六、補強項目評估

### 評估總表

| 項目 | 實際幫助 | 實施難度 | 時間 | ROI | 優先順序 |
|------|---------|---------|------|-----|---------|
| **Googlebot Crawl Simulation** | ⭐⭐⭐⭐⭐ | 低 | 3h | 最高 | **#1** |
| **Internal Link Graph** | ⭐⭐⭐⭐ | 中 | 3h | 高 | **#2** |
| **Lighthouse CI** | ⭐⭐⭐ | 低 | 1h | 中 | **#3** |

### #1 優先：Googlebot Crawl Simulation（Custom Crawler）

**為什麼最值得優先：**
- 直接影響 indexing：確保 Googlebot 能爬取所有重要頁面
- Deploy 後立即價值：每次 deploy 執行，立即發現隱藏 404
- 預防性：在 Google 發現問題前先自行發現
- 低成本高回報：Python + requests，3 小時建立，永久使用

**實施方案：**
```python
# scripts/fun1399_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Fun1399Crawler:
    BASE = "https://fun1399.com"
    HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}
    
    def crawl_sitemap(self):
        """從 sitemap 取得所有 URL 並檢查"""
        pass
    
    def check_page(self, url):
        """檢查單頁 SEO 元素（status、canonical、title、h1、schema）"""
        pass
    
    def check_redirects(self, old_urls):
        """檢查舊網址 redirect（status、chain、loop）"""
        pass
    
    def generate_report(self):
        """產生 Markdown 報告"""
        pass
```

**預估時間：**
| 階段 | 時間 |
|------|------|
| 基礎 crawler（sitemap + status） | 1h |
| SEO 元素檢查（canonical、title、h1、schema） | 1h |
| Redirect 測試（chain、loop） | 0.5h |
| 報告輸出（Markdown） | 0.5h |
| **總計** | **3h** |

### #2 優先：Internal Link Graph

**為什麼值得：**
- 發現 orphan pages：視覺化顯示哪些頁面無內鏈
- 權重分配分析：發現重要頁面內鏈不足
- Cluster 結構驗證：確認 pillar/cluster 架構完整
- 每月執行即可

**實施方案：**
```python
# scripts/link_graph.py
import networkx as nx
from pyvis.network import Network

G = nx.DiGraph()
# 爬全站 → 建立有向圖 → 計算 PageRank → 標註 orphan
# 輸出互動式 HTML（綠色=充足、黃色=中等、紅色=orphan）
```

**預估時間：**
| 階段 | 時間 |
|------|------|
| 爬蟲 + 圖建立 | 1h |
| 視覺化（pyvis） | 1h |
| 指標計算（PageRank） | 1h |
| **總計** | **3h** |

### #3 優先：Lighthouse CI

**為什麼較低優先：**
- Cloudflare 已優化：CDN + Polish 處理 80% 性能問題
- CWV 影響非決定性：內容品質 > 性能（對 fun1399 而言）
- GSC 已有 CWV 報告
- 每月檢查即可

**實施方案：**
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm install -g @lhci/cli
      - run: lhci autorun --url=https://fun1399.com
```

**預估時間：** 1h（GitHub Action 設定）

---

## 七、執行計畫

| 順序 | 任務 | 時間 | 預期成果 |
|------|------|------|---------|
| 1 | 建立 `scripts/fun1399_crawler.py` | 3h | 每次 deploy 自動執行全站爬蟲 |
| 2 | 整合到 deploy checklist | 0.5h | Deploy 後自動觸發 |
| 3 | 建立 `scripts/link_graph.py` | 3h | 每月內鏈可視化 |
| 4 | Lighthouse CI（可選） | 1h | GitHub Action |

### 最快提升 indexing 穩定性的方法

**結論：#1 Custom Crawler**
- 預防勝於治療：在 Google 發現前修復
- 每次 deploy 保護：立即驗證，無延遲
- 全站覆蓋：98 頁全部檢查，不遺漏
- 自動化：建立後無需手動操作

---

## 八、禁止清單（堅守）

- ❌ 不安裝新 content SEO skills
- ❌ 不追求文章數暴增
- ❌ 不做 keyword stuffing
- ❌ 不修改正式 DNS（除非明確授權）
- ❌ 不刪除 Netlify site（rollback 保險）

---

## 九、文件位置

| 文件 | 路徑 |
|------|------|
| 本 workflow | `/root/.openclaw/workspace/FUN1399-SEO-WORKFLOW.md` |
| SEO 技能分析 | `/root/.openclaw/workspace/FUN1399-SEO-SKILL-ANALYSIS.md` |
| SEO Diff 腳本 | `/tmp/seo_diff.sh` |
| Production Audit | `/tmp/cloudflare_production_audit.sh` |

---

*最後更新: 2026-05-20*
*版本: 1.0*
