# Cloudflare Pages SEO Diff 報告

**日期**: 2026-05-20
**Preview URL**: https://fun1399-site.pages.dev
**Production URL**: https://fun1399.com

---

## 檢查方法

使用 curl 同時抓取 Netlify Production 和 Cloudflare Preview 的相同頁面，對比：
- HTTP status code
- Response content
- Canonical URL
- OG tags
- Schema JSON-LD
- robots.txt / sitemap
- Redirect behavior

---

## ✅ 完全一致項目（12 項）

| # | 檢查項目 | Preview | Production | 結果 |
|---|---------|---------|-----------|------|
| 1 | Homepage status | 200 | 200 | ✅ |
| 2 | Canonical | https://fun1399.com/ | https://fun1399.com/ | ✅ |
| 3 | robots.txt | User-agent: * Allow: / | User-agent: * Allow: / | ✅ |
| 4 | sitemap.xml | 93 URLs | 93 URLs | ✅ |
| 5 | Title | 2026娛樂城推薦｜線上娛樂城比較與百家樂攻略... | 相同 | ✅ |
| 6 | Meta Description | 2026最新娛樂城推薦... | 相同 | ✅ |
| 7 | OG title | 2026娛樂城推薦｜線上娛樂城比較與百家樂攻略 | 相同 | ✅ |
| 8 | OG image path | https://fun1399.com/static/images/og-image.jpg | 相同 | ✅ |
| 9 | OG locale | zh_TW | zh_TW | ✅ |
| 10 | Content size | 36,270 bytes | 36,270 bytes | ✅ |
| 11 | /team page | 200, ProfilePage schema | 相同 | ✅ |
| 12 | /articles/mbm | 200, Article schema | 相同 | ✅ |

---

## ⚠️ 差異項目

### 1. .html → Clean URL Redirect Status Code

| 環境 | .html URL | Status | Final URL |
|------|-----------|--------|-----------|
| Netlify | /articles/hg-casino-review.html | 301 | /articles/hg-casino-review |
| Cloudflare | /articles/hg-casino-review.html | **308** | /articles/hg-casino-review |

**分析**:
- 308 = Permanent Redirect（RFC 7538）
- Google 對 308 的處理與 301 相同（link equity 傳遞）
- 308 要求 request method 不變（POST→POST）
- **SEO 影響**: 無負面影響 ✅

### 2. Trailing Slash 行為

| 環境 | URL | Status | Final URL |
|------|-----|--------|-----------|
| Netlify | /articles/mbm... | 200 | 無 trailing slash |
| Cloudflare | /articles/mbm... | 200 | 無 trailing slash |
| Cloudflare | /articles/mbm.../ | **308** | 移除 trailing slash |

**分析**:
- Cloudflare Pages 預設對 trailing slash 返回 308 redirect 到 non-slash 版本
- **SEO 影響**: 無負面影響，符合 Google 建議 ✅

### 3. 404 頁面處理 🔴

| 環境 | 不存在 URL | Status | 內容 |
|------|-----------|--------|------|
| Netlify | /articles/nonexistent.html | 404 | 404 頁面 |
| Cloudflare | /articles/nonexistent.html | **200** | **首頁內容** |

**分析**:
- Cloudflare Pages 預設對不存在路徑返回 200 + 首頁 HTML
- 這是 **Soft 404**，對 SEO 有害
- Google Search Console 會報告「已提交但未索引」

**解決方案**:
1. 建立 `404.html`（Cloudflare Pages 會自動識別）
2. 或在 `_redirects` 加入 catch-all: `/* /404.html 404`

---

## 🔴 發現的 Production 問題

### og-image.jpg 不存在

**問題**: 首頁和所有頁面 OG image 指向 `/static/images/og-image.jpg`，但檔案不存在。

**驗證**:
```bash
curl -I https://fun1399.com/static/images/og-image.jpg
# HTTP/2 404
```

**影響**:
- Facebook/Threads/X 分享時無預覽圖片
- OG debugger 報錯
- 品牌曝光下降

**解決**: 建立 `static/images/og-image.jpg`（1200×630 px）

---

## _redirects 數量不一致

| 來源 | 數量 | 說明 |
|------|------|------|
| netlify.toml | 88 | 原始 Netlify 設定 |
| _redirects | 72 | 目前檔案 |

**差異**: 16 條 redirect 規則遺漏

**可能原因**:
- _redirects 檔案產生時遺漏
- netlify.toml 有些規則是後來加的，沒同步到 _redirects

**建議**: 重新從 netlify.toml 產生完整的 `_redirects`

---

## Cloudflare Pages 相容性總結

| 功能 | 相容性 | 備註 |
|------|--------|------|
| 靜態檔案 | ✅ 完美 | 200 OK |
| Custom domain | ⏳ 待測試 | 尚未綁定 |
| SSL | ✅ 自動 | Cloudflare Universal SSL |
| Redirects | ⚠️ 可接受 | 308 非 301，功能正常 |
| Trailing slash | ✅ 正常 | 自動 308 到 non-slash |
| 404 處理 | ❌ 需修正 | Soft 404 問題 |
| Headers | ✅ 可透過 _headers | 目前無需求 |
| Cache | ✅ 自動 | Cloudflare CDN |
| Functions | ⏳ 未測試 | 目前無需 |

---

## 遷移建議

### 現階段（不遷移）
- [ ] 建立 og-image.jpg
- [ ] 修復 Soft 404（建立 404.html）
- [ ] 補齊 _redirects（88 條）

### 驗證階段
- [ ] 綁定 fun1399.com 到 Cloudflare Pages 測試
- [ ] 確認 SSL 正常
- [ ] 確認所有 redirects 運作

### 切換階段
- [ ] DNS NS 改為 Cloudflare
- [ ] 保留 Netlify site（rollback 保險）
- [ ] 監控 48 小時

---

## 結論

Cloudflare Pages Preview 與 Netlify Production **內容 100% 一致**，SEO 結構正確。

主要問題：
1. 🔴 **Soft 404**（需建立 404.html）
2. 🔴 **og-image.jpg 不存在**（需製作圖片）
3. ⚠️ **_redirects 數量不足**（需補齊）

**建議先修復以上問題，再進行 DNS 切換。**
