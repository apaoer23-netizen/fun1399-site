# FUN1399 Redirect 驗證檢查清單

**觸發時機**: 每次 deploy 後 + DNS 變更後 + 新增 redirect 規則後  
**執行時間**: ~3 分鐘  
**工具**: curl + 自訂腳本  

---

## 1. 重要舊網址 Redirect

### 1.1 已知舊網址（來自 _redirects 檔案）
```bash
# 讀取 _redirects 並測試前 10 條
cat /root/.openclaw/workspace/fun1399-clean/_redirects | head -20
```

| # | 舊網址 | 預期狀態 | 預期目標 | 實際結果 |
|---|--------|---------|---------|---------|
| 1 | /old-path | 301 | /new-path | ___ |
| 2 | /legacy-page | 301 | /articles/legacy | ___ |
| 3 | /wp-admin | 301 | / | ___ |
| ... | ... | ... | ... | ... |

- [ ] 所有已知舊網址返回 301/308
- [ ] Location header 正確
- [ ] 無 redirect loop

### 1.2 高流量舊網址（優先保護）
```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/wp-login.php"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/wp-admin"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/xmlrpc.php"
```
- [ ] WordPress 路徑 → 首頁或 404
- [ ] 無暴露 CMS 類型

---

## 2. .html Redirect 驗證

### 2.1 一致性檢查
```bash
# 測試：無 .html 是否 redirect 到 .html
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles/mbm-review"

# 測試：有 .html 是否 200
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review.html"
```
- [ ] 無 `.html` URL 返回 301/308 → `.html`
- [ ] 或反向：`.html` → 無 `.html`（一致性即可）
- [ ] 無 404 或 200 重複內容

### 2.2 全站掃描
```bash
# 掃描 _redirects 中的 .html 規則
grep "\.html" /root/.openclaw/workspace/fun1399-clean/_redirects | head -10
```
- [ ] `.html` redirect 規則正確運作
- [ ] 無 double redirect（301 → 301）

---

## 3. Trailing Slash 驗證

### 3.1 目錄頁
```bash
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles"
curl -sI -o /dev/null -w "%{http_code} → %{redirect_url}" "https://fun1399.com/articles/"
```
- [ ] `/articles` → 301 → `/articles/`（或反向，一致性即可）
- [ ] `/reviews` → 301 → `/reviews/`（或反向）

### 3.2 檔案頁面
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review.html/"
```
- [ ] `.html/` 返回 301 或 404（不應 200）

---

## 4. 301 vs 302 狀態

### 4.1 必須是 301（永久）的 redirect
- [ ] HTTP → HTTPS: 301
- [ ] www → apex: 301
- [ ] 舊網址 → 新網址: 301/308
- [ ] trailing slash 統一: 301/308

### 4.2 禁止 302（臨時）的情況
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com"
curl -sI -o /dev/null -w "%{http_code}" "http://fun1399.com"
```
- [ ] 無 302 redirect（會稀釋 SEO 權重）
- [ ] 所有 SEO-relevant redirect 均為 301/308

---

## 5. Redirect Chain 檢查

### 5.1 Chain 深度
```bash
# 測試 redirect chain
curl -sIL -o /dev/null -w "%{http_code}\n" "http://www.fun1399.com/old-path"
```
- [ ] Chain depth ≤ 2（A → B → C）
- [ ] 無 loop（A → B → A）
- [ ] 最終 URL 200 OK

### 5.2 常見 Chain 風險
```
風險範例：
http://www.fun1399.com/old → https://www.fun1399.com/old → https://fun1399.com/old → https://fun1399.com/new
（4 跳！）
```
- [ ] HTTP + www + old path → 直接到最終 HTTPS apex new path

---

## 6. Cloudflare Pages Redirect 特點

### 6.1 已知行為
| 情況 | Cloudflare Pages | Netlify |
|------|-----------------|---------|
| `.html` redirect | 308（預設）| 301 |
| trailing slash | 308 | 301 |
| 行為差異 | 等同 301（Google 視為 permanent）| 301 |

### 6.2 驗證
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/articles/mbm-review"
```
- [ ] 返回 308（Cloudflare 正常）或 301
- [ ] 非 302

---

## 7. _redirects 檔案驗證

### 7.1 檔案存在
```bash
curl -sI -o /dev/null -w "%{http_code}" "https://fun1399.com/_redirects"
```
- [ ] 返回 200（開發用）或 404（生產應阻擋）

### 7.2 規則數量
```bash
cat /root/.openclaw/workspace/fun1399-clean/_redirects | wc -l
```
- [ ] 規則數: ___（基準: 75 行）
- [ ] 無新增/遺漏

---

## 8. 批量測試腳本

```bash
#!/bin/bash
# redirect-test.sh

URLS=(
  "http://fun1399.com"
  "https://www.fun1399.com"
  "https://fun1399.com/articles/mbm-review"
  "https://fun1399.com/articles/"
  "https://fun1399.com/team"
)

for url in "${URLS[@]}"; do
  code=$(curl -sI -o /dev/null -w "%{http_code}" "$url")
  final=$(curl -sIL -o /dev/null -w "%{url_effective}" "$url")
  echo "$code | $url → $final"
done
```

---

## ✅ 通過標準

| 檢查項 | 通過條件 |
|--------|---------|
| 舊網址 | 100% 返回 301/308，無 404 |
| .html | 一致性（全有或全無），無重複內容 |
| Trailing slash | 統一策略，無 200 重複 |
| 狀態碼 | 無 302，SEO-relevant 均為 301/308 |
| Chain | 深度 ≤ 2，無 loop |
| _redirects | 規則數穩定，無異常新增 |

---

*最後更新: 2026-05-20*
