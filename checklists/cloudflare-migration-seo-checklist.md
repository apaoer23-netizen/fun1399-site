# FUN1399 Cloudflare Migration SEO 檢查清單

**狀態**: ✅ 遷移已完成  
**日期**: 2026-05-20  
**用途**: 驗證遷移後 SEO 完整性 + 未來 rollback 參考  

---

## 遷移歷史

| 時間 | 事件 | 狀態 |
|------|------|------|
| 2026-05-20 | DNS NS 切換至 Cloudflare | ✅ |
| 2026-05-20 | Cloudflare Pages deploy | ✅ |
| 2026-05-20 | SSL 憑證啟用 | ✅ |
| 2026-05-20 | www → apex 301 | ✅ |
| 2026-05-20 | og-image 修復 | ✅ |
| 2026-05-20 | 404.html 建立 | ✅ |

---

## 1. DNS 驗證

### 1.1 NS 紀錄
```bash
dig NS fun1399.com +short
```
- [ ] NS 為 Cloudflare（`*.cloudflare.com`）
- [ ] 非 GoDaddy NS

### 1.2 A 紀錄
```bash
dig A fun1399.com +short
dig A www.fun1399.com +short
```
- [ ] fun1399.com → Cloudflare Pages IPs
- [ ] www → Cloudflare Pages IPs

### 1.3 無 MX/TXT 異常
```bash
dig MX fun1399.com +short
dig TXT fun1399.com +short
```
- [ ] MX: 無或正確
- [ ] TXT: 無異常 SPF/DKIM

---

## 2. SSL/TLS 驗證

### 2.1 憑證資訊
```bash
echo | openssl s_client -servername fun1399.com -connect fun1399.com:443 2>/dev/null | openssl x509 -noout -issuer -subject -dates
```
- [ ] Issuer: Cloudflare Inc
- [ ] Subject: CN=fun1399.com
- [ ] 未過期

### 2.2 HTTPS 強制
```bash
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
```
- [ ] HTTP → 301 → HTTPS

### 2.3 HSTS（如啟用）
```bash
curl -sI "https://fun1399.com" | grep -i "strict-transport-security"
```
- [ ] 有 `Strict-Transport-Security` header（加分項）

---

## 3. Cloudflare Pages 設定驗證

### 3.1 基本設定
- [ ] Production branch: `main`
- [ ] Build command: 無（靜態站）
- [ ] Output directory: `/`

### 3.2 Custom Domain
- [ ] fun1399.com → Active
- [ ] www.fun1399.com → Active + redirect to apex

### 3.3 Functions（應無）
- [ ] 無 Cloudflare Functions（純靜態）

---

## 4. SEO 元素遷移驗證

### 4.1 標題與 Meta
```bash
curl -sL "https://fun1399.com" | grep -E '<title>|<meta name="description"'
```
- [ ] Title 與遷移前一致
- [ ] Description 與遷移前一致

### 4.2 Canonical
```bash
curl -sL "https://fun1399.com" | grep 'rel="canonical"'
```
- [ ] Canonical 指向 https://fun1399.com/
- [ ] 無 www，無 http

### 4.3 OG / Twitter Card
```bash
curl -sL "https://fun1399.com" | grep -E '<meta property="og:|<meta name="twitter:'
```
- [ ] OG 完整
- [ ] og:image 可存取（200）

### 4.4 Schema
```bash
curl -sL "https://fun1399.com" | grep -A 20 'application/ld+json'
```
- [ ] JSON-LD 存在
- [ ] 結構與遷移前一致

### 4.5 robots.txt
```bash
curl -s "https://fun1399.com/robots.txt"
```
- [ ] 內容與遷移前一致
- [ ] Sitemap 引用正確

### 4.6 Sitemap
```bash
curl -s "https://fun1399.com/sitemap.xml" | grep -c '<loc>'
```
- [ ] URL 數量一致（~93）
- [ ] 所有 URL 為 https://fun1399.com

---

## 5. Redirect 驗證（遷移後）

### 5.1 基本 Redirect
```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "http://fun1399.com"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://www.fun1399.com"
```
- [ ] HTTP → HTTPS: 301
- [ ] www → apex: 301

### 5.2 Cloudflare Pages Redirect
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review"
```
- [ ] `.html` redirect: 308（Cloudflare 正常）
- [ ] 無 302

---

## 6. 性能驗證

### 6.1 Response Time
```bash
curl -sI -o /dev/null -w "%{time_total}" "https://fun1399.com"
```
- [ ] TTFB < 500ms

### 6.2 Cache Header
```bash
curl -sI "https://fun1399.com" | grep -i "cache-control\|cf-cache-status"
```
- [ ] `CF-Cache-Status: HIT`（第二次請求）
- [ ] Cache-Control 合理

---

## 7. 安全性驗證

### 7.1 Security Headers
```bash
curl -sI "https://fun1399.com" | grep -E "X-Content-Type-Options|X-Frame-Options|Referrer-Policy"
```
- [ ] 基本安全 headers 存在（Cloudflare 預設）

### 7.2 無敏感資訊洩漏
```bash
curl -sL "https://fun1399.com" | grep -i "api_key\|token\|password"
```
- [ ] 無敏感資訊在 HTML 中

---

## 8. Rollback 準備

### 8.1 Netlify 備份
- [ ] Netlify site 未刪除
- [ ] Netlify site 仍可存取（備用 URL）
- [ ] 可隨時切換 DNS 回 Netlify

### 8.2 DNS 回滾步驟
```
1. GoDaddy DNS → NS 改回 ns27.domaincontrol.com + ns28.domaincontrol.com
2. 等待 propagation（5-48 小時）
3. 驗證 SSL 正常
4. 驗證 redirect 正常
```

### 8.3 檢查清單
- [ ] GoDaddy 帳號可登入
- [ ] 知道如何修改 NS
- [ ] 已記錄原 NS 值

---

## 9. 監控項目

### 9.1 遷移後 1 週內每日檢查
- [ ] 首頁 200
- [ ] /articles 200
- [ ] /team 200
- [ ] sitemap.xml 200
- [ ] robots.txt 200
- [ ] 不存在 URL 404

### 9.2 遷移後 1 個月內每週檢查
- [ ] GSC Coverage 無異常 drop
- [ ] 排名無大幅波動
- [ ] Impressions 穩定

---

## ✅ 通過標準

| 檢查項 | 通過條件 |
|--------|---------|
| DNS | Cloudflare NS active |
| SSL | Cloudflare-issued, valid |
| SEO 元素 | 100% 與遷移前一致 |
| Redirect | HTTP→HTTPS 301, www→apex 301 |
| 404 | 不存在 URL 返回 404 |
| 性能 | TTFB < 500ms, Cache HIT |
| Rollback | Netlify 備份可用 |

---

## 🚨 異常處理

若發現遷移後 SEO 異常：
1. 立即記錄 `memory/YYYY-MM-DD.md`
2. 評估嚴重性（流量 drop %）
3. 輕微: 修復並觀察
4. 嚴重: 啟動 rollback（切換 DNS 回 Netlify）
5. 通知 Hans

---

*最後更新: 2026-05-20*
*遷移狀態: ✅ 已完成*
