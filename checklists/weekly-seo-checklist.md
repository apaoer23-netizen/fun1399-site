# FUN1399 每週 SEO 檢查清單

**觸發時機**: 每週一次（建議週一 10:00）  
**執行時間**: ~10 分鐘  
**工具**: google-search-console + ai-seo + internal-linker  

---

## 1. Google Search Console 分析

### 1.1 收錄狀況
```bash
# 手動檢查：site:fun1399.com
curl -s "https://www.google.com/search?q=site:fun1399.com" | grep -c "fun1399.com"
```
- [ ] Indexed pages: ___（目標: 90+）
- [ ] 檢查是否有大量 drop

### 1.2 Coverage Report（GSC 後台）
- [ ] Valid: ___
- [ ] Valid with warnings: ___
- [ ] Excluded: ___
- [ ] Error: ___（目標: 0）

### 1.3 Performance（Query）
- [ ] Total impressions: ___
- [ ] Total clicks: ___
- [ ] Average CTR: ___
- [ ] Average position: ___

### 1.4 熱門查詢
- [ ] 前 10 查詢是否穩定
- [ ] 是否有新查詢進入前 20
- [ ] 品牌詞「娛樂城玩家俱樂部」是否有 impression

### 1.5 Core Web Vitals（GSC）
- [ ] LCP: Good / Need Improvement / Poor
- [ ] INP: Good / Need Improvement / Poor
- [ ] CLS: Good / Need Improvement / Poor
- [ ] 行動裝置 CWV 通過率: ___%

### 1.6 Crawl Stats（GSC）
- [ ] Crawl requests: ___
- [ ] Average response time: ___ ms
- [ ] 是否有大量 404 crawl

---

## 2. AI SEO 分析（ai-seo）

### 2.1 品牌詞 AI 可見度
```
手動檢查：
- ChatGPT: "娛樂城玩家俱樂部 是什麼"
- Perplexity: "娛樂城玩家俱樂部 評價"
- Google AI Overview: "娛樂城推薦"
```
- [ ] fun1399.com 是否被引用
- [ ] 競爭對手是否被引用（比較）

### 2.2 AI Bot robots.txt 狀態
```bash
curl -s "https://fun1399.com/robots.txt" | grep -E "GPTBot|ChatGPT-User|PerplexityBot|ClaudeBot|anthropic-ai"
```
- [ ] GPTBot: Allow
- [ ] ChatGPT-User: Allow
- [ ] PerplexityBot: Allow
- [ ] ClaudeBot: Allow
- [ ] CCBot: 可選 Disallow（防止訓練）

### 2.3 FAQ 結構品質
```bash
curl -sL "https://fun1399.com/team.html" | grep -A 5 'FAQPage'
curl -sL "https://fun1399.com" | grep -A 5 'FAQPage'
```
- [ ] /team 有 FAQPage Schema
- [ ] FAQ 數量: ___（建議 5-8 題）
- [ ] 問題為自然語言（非關鍵字堆砌）

### 2.4 Comparison 格式
```bash
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -iE '比較|vs|對比|差異'
```
- [ ] 有 comparison table（如有比較內容）
- [ ] 格式為 AI 可提取的表格或列表

### 2.5 EEAT 結構
```bash
curl -sL "https://fun1399.com/team.html" | grep -E 'author|expert|經驗|資歷'
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -E 'author|datePublished|dateModified'
```
- [ ] /team 有作者資訊
- [ ] 文章有 author + datePublished
- [ ] 內容有 first-hand experience 描述

### 2.6 AI Readable Content
- [ ] 段落 2-3 句話
- [ ] 關鍵結論前置（首段直接回答）
- [ ] 有統計數據 + 來源引用
- [ ] 有專家引言（如有）

---

## 3. Internal Link Audit（internal-linker）

```bash
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --link-depth --distribution --orphan-pages
```

### 3.1 Orphan Pages
- [ ] Orphan pages 數量: ___
- [ ] 新產生的 orphan pages: ___
- [ ] 目標: < 5

### 3.2 重要頁面權重
- [ ] 首頁: 連入 ___ 個 / 連出 ___ 個
- [ ] /team: 連入 ___ 個（目標: 全站導航 + 5+ 文章內鏈）
- [ ] /about: 連入 ___ 個
- [ ] /contact: 連入 ___ 個

### 3.3 Pillar / Cluster 結構
| Pillar | Support Pages | 狀態 |
|--------|--------------|------|
| 首頁 | /articles, /reviews, /team | ___ |
| /articles（文章列表）| 各文章頁 | ___ |
| /reviews（評價列表）| 各評價頁 | ___ |
| /team | — | ___ |

- [ ] 每個 pillar 有足夠 support（3+ 頁面）
- [ ] Cluster 間有 cross-linking

### 3.4 /team 內鏈狀況
- [ ] 全站導航有 /team 連結
- [ ] 有 ___ 篇文章內文連到 /team
- [ ] /team 有 ___ 個連出到文章頁

---

## 4. Content Freshness

### 4.1 文章更新檢查
```bash
# 檢查最近修改的文章（透過 git log）
cd /root/.openclaw/workspace/fun1399-clean && git log --since="1 week ago" --name-only --oneline
```
- [ ] 上週更新文章: ___ 篇
- [ ] 最舊文章更新時間: ___（建議每季更新）

### 4.2 日期檢查
```bash
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -o 'datePublished[^"]*"[^"]*"'
```
- [ ] 最新文章有正確 datePublished
- [ ] 無過期內容（如「2025 最佳」等）

---

## 5. Cloudflare Analytics（如可存取）

### 5.1 Traffic
- [ ] Requests: ___
- [ ] Bandwidth: ___
- [ ] Unique visitors: ___

### 5.2 Performance
- [ ] Cache hit rate: ___%（目標: > 80%）
- [ ] Edge response time: ___ ms
- [ ] Error rate: ___%（目標: < 1%）

---

## 6. 競爭對手監控

### 6.1 同行站點
```
檢查對象：
- qttheluxe.com
- qttowerrush.com
- inoutchickenroad2.com
- pandasportsevents.com
```
- [ ] 對手是否有新頁面（site:domain.com）
- [ ] 對手是否更新 content
- [ ] 對手是否有新的 SEO 策略

### 6.2 品牌詞競爭
```
搜尋："娛樂城玩家俱樂部"
```
- [ ] fun1399.com 是否 #1
- [ ] 是否有負面內容出現

---

## 7. 行動項目記錄

| 發現 | 嚴重性 | 行動 | 負責人 | 期限 |
|------|--------|------|--------|------|
| | | | | |

---

## ✅ 通過標準

| 檢查項 | 通過條件 |
|--------|---------|
| GSC Coverage | Error = 0，Valid > 90 |
| CWV | 全部 Good 或 Need Improvement |
| AI Bot | 4 大 AI bot 均 Allow |
| Orphan | < 5 |
| /team 內鏈 | > 5 個連入 |
| Cache | Hit rate > 80% |

---

*最後更新: 2026-05-20*
