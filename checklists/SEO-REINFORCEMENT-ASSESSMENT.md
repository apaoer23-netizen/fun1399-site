# FUN1399 SEO 補強項目評估報告

**日期**: 2026-05-20  
**評估項目**: lighthouse-ci, Googlebot crawl simulation, custom crawler, internal link graph  
**評估標準**: 對 fun1399 實際幫助、實施難度、ROI、indexing 影響  

---

## 評估總表

| 項目 | 實際幫助 | 實施難度 | 時間 | ROI | 優先順序 |
|------|---------|---------|------|-----|---------|
| **Googlebot Crawl Simulation** | ⭐⭐⭐⭐⭐ | 低 | 2h | 最高 | **#1** |
| **Internal Link Graph** | ⭐⭐⭐⭐ | 中 | 3h | 高 | **#2** |
| **Lighthouse CI** | ⭐⭐⭐ | 低 | 1h | 中 | **#3** |
| **Custom Crawler（全站）** | ⭐⭐⭐⭐ | 中 | 4h | 高 | #1 的延伸 |

---

## #1 優先：Googlebot Crawl Simulation（Custom Crawler）

### 為什麼最值得優先

| 面向 | 說明 |
|------|------|
| **直接影響 indexing** | 確保 Googlebot 能爬取所有重要頁面，發現隱藏 404 |
| **deploy 後立即價值** | 每次 deploy 執行，立即發現問題 |
| **預防性** | 在 Google 發現問題前，先自行發現 |
| **低成本高回報** | Python + requests，2 小時建立，永久使用 |

### 實際應用場景

```
情境：deploy 新文章後
→ Crawler 掃全站 98 頁
→ 發現 /articles/new-post.html 返回 404（檔名錯誤）
→ 立即修復，而非等 GSC 報告（可能需要數天）
```

```
情境：新增 redirect 規則後
→ Crawler 測試舊網址
→ 發現 redirect chain A→B→C（3 跳）
→ 優化為 A→C（1 跳）
```

### 實施方案

```python
# fun1399_crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Fun1399Crawler:
    BASE = "https://fun1399.com"
    SITEMAP_URLS = []
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"
        })
    
    def crawl_from_sitemap(self):
        """從 sitemap 取得所有 URL"""
        r = self.session.get(f"{self.BASE}/sitemap.xml")
        # 解析 <loc>...
    
    def check_page(self, url):
        """檢查單頁 SEO 元素"""
        r = self.session.get(url)
        return {
            "status": r.status_code,
            "canonical": self.extract_canonical(r.text),
            "title": self.extract_title(r.text),
            "h1_count": self.count_h1(r.text),
            "schema": self.has_schema(r.text),
            "og_image": self.extract_og_image(r.text),
        }
    
    def check_redirects(self, old_urls):
        """檢查舊網址 redirect"""
        for url in old_urls:
            r = self.session.head(url, allow_redirects=True)
            # 記錄 status + chain
```

### 預估時間

| 階段 | 時間 | 說明 |
|------|------|------|
| 基礎 crawler | 1h | 爬 sitemap + 檢查 status |
| SEO 元素檢查 | 1h | canonical, title, h1, schema |
| Redirect 測試 | 0.5h | 舊網址 redirect chain |
| 報告輸出 | 0.5h | Markdown 報告 |
| **總計** | **3h** | |

---

## #2 優先：Internal Link Graph（可視化）

### 為什麼值得

| 面向 | 說明 |
|------|------|
| **發現 orphan pages** | 視覺化顯示哪些頁面無內鏈 |
| **權重分配分析** | 發現重要頁面內鏈不足 |
| **cluster 結構驗證** | 確認 pillar/cluster 架構完整 |
| **每月執行即可** | 不需要每次 deploy 執行 |

### 實際應用

```
輸出：internal-link-graph.html
→ 節點 = 每個頁面
→ 邊 = 內部連結
→ 顏色：
   - 綠色 = 內鏈充足（5+）
   - 黃色 = 內鏈中等（2-4）
   - 紅色 = orphan（0-1）
→ 大小 = 頁面重要性（基於內鏈數）
```

### 實施方案

```python
# link_graph.py
import networkx as nx
from pyvis.network import Network

# 爬全站 → 建立有向圖
G = nx.DiGraph()
for page in all_pages:
    for link in page.internal_links:
        G.add_edge(page.url, link.url)

# 計算指標
pagerank = nx.pagerank(G)
orphan_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]

# 產生互動式圖表
net = Network()
# ...
net.show("link-graph.html")
```

### 預估時間

| 階段 | 時間 |
|------|------|
| 爬蟲 + 圖建立 | 1h |
| 視覺化（pyvis） | 1h |
| 指標計算（PageRank） | 1h |
| **總計** | **3h** |

---

## #3 優先：Lighthouse CI

### 為什麼較低優先

| 面向 | 說明 |
|------|------|
| **Cloudflare 已優化** | CDN + Polish 處理 80% 性能問題 |
| **CWV 影響非決定性** | 內容品質 > 性能（對 fun1399 而言）|
| **GSC 已有 CWV 報告** | 不需要額外工具 |
| **低頻率需求** | 每月檢查即可 |

### 何時有用

- 發現 GSC CWV 報告有 Poor 頁面時
- 新增大量圖片或 JS 後
- 收到 Core Update 影響通知時

### 實施方案

```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push]
jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Lighthouse
        run: |
          npm install -g @lhci/cli
          lhci autorun --url=https://fun1399.com
```

### 預估時間

| 階段 | 時間 |
|------|------|
| GitHub Action 設定 | 0.5h |
| Lighthouse CI 設定 | 0.5h |
| **總計** | **1h** |

---

## 最快提升 indexing 與 SEO 穩定性的方法

### 結論：#1 Custom Crawler

| 原因 | 說明 |
|------|------|
| **預防勝於治療** | 在 Google 發現前修復 |
| **每次 deploy 保護** | 立即驗證，無延遲 |
| **全站覆蓋** | 98 頁全部檢查，不遺漏 |
| **自動化** | 建立後無需手動操作 |
| **低成本** | 3 小時建立，永久使用 |

### 執行計畫

| 順序 | 任務 | 時間 | 預期成果 |
|------|------|------|---------|
| 1 | 建立 `scripts/fun1399_crawler.py` | 3h | 每次 deploy 自動執行 |
| 2 | 整合到 deploy checklist | 0.5h | deploy 後自動爬蟲 |
| 3 | 建立 `scripts/link_graph.py` | 3h | 每月內鏈可視化 |
| 4 | Lighthouse CI（可選） | 1h | GitHub Action |

---

## 建議

### 立即執行（本週）
- [ ] 建立 Googlebot Crawl Simulation 腳本
- [ ] 整合到 deploy checklist

### 1 週後
- [ ] 建立 Internal Link Graph
- [ ] 首次執行並分析 orphan pages

### 2 週後（可選）
- [ ] Lighthouse CI GitHub Action

---

*最後更新: 2026-05-20*
