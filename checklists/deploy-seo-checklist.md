# FUN1399 Deploy 後 SEO 檢查清單

**觸發時機**: 每次 Git push → Cloudflare Pages deploy 完成後  
**執行時間**: ~5 分鐘  
**工具**: seo-audit + internal-linker + curl + 自訂腳本  

---

## 1. Canonical 檢查

### 1.1 首頁 Canonical
```bash
curl -sL "https://fun1399.com" | grep -o 'rel="canonical"[^>]*'
```
- [ ] 存在 `rel="canonical"`
- [ ] 指向 `https://fun1399.com/`
- [ ] 非 `http://`（必須是 HTTPS）
- [ ] 無 `www.`（必須是 apex domain）

### 1.2 文章頁 Canonical
```bash
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -o 'rel="canonical"[^>]*'
curl -sL "https://fun1399.com/articles/nba-betting.html" | grep -o 'rel="canonical"[^>]*'
```
- [ ] 文章頁有 self-referencing canonical
- [ ] 無多餘 trailing slash（`.html` 頁面）

### 1.3 分類頁 Canonical
```bash
curl -sL "https://fun1399.com/articles/" | grep -o 'rel="canonical"[^>]*'
curl -sL "https://fun1399.com/reviews/" | grep -o 'rel="canonical"[^>]*'
```
- [ ] 分類頁有 canonical

---

## 2. Sitemap 檢查

### 2.1 Sitemap 可存取
```bash
curl -sI "https://fun1399.com/sitemap.xml" | grep -i "HTTP/"
```
- [ ] Status: 200 OK
- [ ] Content-Type: application/xml

### 2.2 Sitemap 內容
```bash
curl -s "https://fun1399.com/sitemap.xml" | grep -c "<loc>"
```
- [ ] URL 總數: ~91-98（符合實際頁面數）
- [ ] 包含 `/team`
- [ ] 無 `.bak`、無測試頁面

### 2.3 robots.txt 引用
```bash
curl -s "https://fun1399.com/robots.txt" | grep -i "sitemap"
```
- [ ] `Sitemap: https://fun1399.com/sitemap.xml`

---

## 3. Schema 檢查

### 3.1 首頁 Schema
```bash
curl -sL "https://fun1399.com" | grep -A 30 'application/ld+json'
```
- [ ] 存在 JSON-LD
- [ ] `@type` 正確（Organization / WebSite）
- [ ] `name` 為「娛樂城玩家俱樂部」

### 3.2 文章頁 Schema
```bash
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -A 50 'application/ld+json'
```
- [ ] Article schema 存在
- [ ] author 正確
- [ ] datePublished 存在

### 3.3 /team Schema
```bash
curl -sL "https://fun1399.com/team.html" | grep -A 50 'application/ld+json'
```
- [ ] Organization + Person schema 存在
- [ ] sameAs 連結正確

---

## 4. Redirect 檢查

### 4.1 HTTP → HTTPS
```bash
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
```
- [ ] 返回 301
- [ ] Location: https://fun1399.com/

### 4.2 www → apex
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://www.fun1399.com"
```
- [ ] 返回 301
- [ ] Location: https://fun1399.com/

### 4.3 .html Redirect
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review"
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/team"
```
- [ ] 無 `.html` 的 URL 返回 301 → `.html`
- [ ] 或 `.html` → 無 `.html`（一致性即可）

---

## 5. robots.txt 檢查

### 5.1 基本規則
```bash
curl -s "https://fun1399.com/robots.txt"
```
- [ ] `User-agent: *`
- [ ] `Allow: /`
- [ ] `Disallow: /admin/`
- [ ] `Disallow: /api/`
- [ ] `Disallow: /test/`（如有測試頁）
- [ ] `Sitemap:` 引用正確

### 5.2 AI Bot 存取
- [ ] 未阻擋 `GPTBot`
- [ ] 未阻擋 `ChatGPT-User`
- [ ] 未阻擋 `PerplexityBot`
- [ ] 未阻擋 `ClaudeBot`

---

## 6. Status Code 檢查

### 6.1 核心頁面
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

### 6.2 不存在頁面
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/nonexistent-page-12345"
```
- [ ] 返回 404（非 200 或 301）
- [ ] 有 404.html 內容

---

## 7. OG / Meta 檢查

### 7.1 基本 Meta
```bash
curl -sL "https://fun1399.com" | grep -E '<title>|<meta name="description"'
```
- [ ] `<title>` 存在且 50-60 字元
- [ ] `<meta name="description">` 存在且 150-160 字元

### 7.2 Open Graph
```bash
curl -sL "https://fun1399.com" | grep -E '<meta property="og:'
```
- [ ] `og:title` 存在
- [ ] `og:description` 存在
- [ ] `og:image` 存在（`https://fun1399.com/og-image.jpg`）
- [ ] `og:url` 存在

### 7.3 Twitter Card
```bash
curl -sL "https://fun1399.com" | grep -E '<meta name="twitter:'
```
- [ ] `twitter:card` = summary_large_image
- [ ] `twitter:title` 存在
- [ ] `twitter:image` 存在

---

## 8. Noindex 檢查

### 8.1 重要頁面不得有 noindex
```bash
curl -sL "https://fun1399.com" | grep -i 'noindex'
curl -sL "https://fun1399.com/articles/mbm-review.html" | grep -i 'noindex'
curl -sL "https://fun1399.com/team.html" | grep -i 'noindex'
```
- [ ] 首頁無 noindex
- [ ] 文章頁無 noindex
- [ ] /team 無 noindex
- [ ] /articles 無 noindex
- [ ] /reviews 無 noindex

### 8.2 測試頁面應有 noindex（如有）
- [ ] 測試頁面有 `noindex, nofollow`

---

## 9. Mobile 基本檢查

### 9.1 Viewport
```bash
curl -sL "https://fun1399.com" | grep -o 'viewport[^>]*'
```
- [ ] `width=device-width, initial-scale=1`

### 9.2 Theme Color
```bash
curl -sL "https://fun1399.com" | grep -o 'theme-color[^>]*'
```
- [ ] 存在 theme-color

### 9.3 Mobile User-Agent
```bash
curl -sI -A "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)" -o /dev/null -w "%{http_code}" "https://fun1399.com"
```
- [ ] Mobile 返回 200

---

## 10. Content Integrity

### 10.1 首頁內容
```bash
curl -sL "https://fun1399.com" | grep -c '<h1'
curl -sL "https://fun1399.com" | grep '娛樂城玩家俱樂部'
```
- [ ] 有且僅有 1 個 `<h1>`
- [ ] 品牌名稱「娛樂城玩家俱樂部」存在
- [ ] GA4 追蹤碼存在（gtag）

### 10.2 /team 頁面
```bash
curl -sL "https://fun1399.com/team.html" | grep -c '<h1'
curl -sL "https://fun1399.com/team.html" | grep 'Diana\|Molly\|Ethan'
```
- [ ] 有且僅有 1 個 `<h1>`
- [ ] 分析師人名存在

---

## 11. Internal Link 檢查（internal-linker）

```bash
@internal-linker analyze /root/.openclaw/workspace/fun1399-clean --orphan-pages --broken-links --link-depth
```
- [ ] 無 broken internal links
- [ ] Orphan pages 數量: ___（目標: 0-5）
- [ ] 重要頁面（/team, /about, /contact）有足夠內鏈

---

## 12. Diff 檢查（Production vs Preview）

```bash
bash /tmp/seo_diff.sh
```
- [ ] Canonical 一致
- [ ] Sitemap URL 數一致
- [ ] robots.txt 一致
- [ ] 無新增 noindex
- [ ] OG 結構一致

---

## ✅ 通過標準

| 檢查項 | 通過條件 |
|--------|---------|
| Canonical | 100% 頁面有正確 canonical |
| Sitemap | 200 OK，URL 數正確 |
| Schema | 首頁 + 文章 + /team 有 JSON-LD |
| Redirect | HTTP→HTTPS 301，www→apex 301 |
| robots.txt | Allow: /，引用 sitemap |
| Status Code | 核心頁面 200，不存在頁面 404 |
| OG | 所有頁面有基本 OG 標籤 |
| Noindex | 重要頁面無 noindex |
| Mobile | Viewport + Theme Color 存在 |
| Internal Link | Orphan < 5，無 broken links |
| Diff | Production ≡ Preview（結構） |

---

## 🚨 失敗處理

若任一檢查失敗：
1. 立即記錄 `memory/YYYY-MM-DD.md`
2. 不回報 Hans？**必須回報**（部署相關）
3. 不自行修復（除非明確授權）
4. 評估是否 rollback（Netlify 備用）

---

*最後更新: 2026-05-20*
