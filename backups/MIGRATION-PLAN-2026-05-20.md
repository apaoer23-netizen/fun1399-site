# FUN1399 專案備份報告 + Cloudflare Pages 遷移規劃

**日期**: 2026-05-20
**專案**: fun1399.com
**執行人**: 助手

---

## 第一階段：備份完成狀態

### 備份檔案清單

| 檔案 | 大小 | 內容 |
|------|------|------|
| `fun1399-source-2026-05-20.tar.gz` | 39 MB | **完整網站原始碼**（288 個檔案）|
| `fun1399-netlify-config-2026-05-20.toml` | 14 KB | Netlify 設定（redirects + build config）|
| `fun1399-netlify-state-2026-05-20.json` | 53 B | Netlify site state |
| `fun1399-robots-2026-05-20.txt` | 99 B | robots.txt |
| `fun1399-sitemap-2026-05-20.xml` | 11 KB | sitemap.xml（93 URLs）|
| `fun1399-deploy-history-2026-05-20.md` | 741 B | Deploy 記錄 |
| `fun1399-backup-manifest-2026-05-20.txt` | 491 B | 備查清單 |

**備份位置**: `/root/.openclaw/workspace/backups/`
**總大小**: 39 MB

---

### 專案結構統計

| 項目 | 數量/大小 |
|------|----------|
| 總檔案數 | 288 個 |
| HTML 檔案 | 98 個 |
| CSS 檔案 | 2 個 |
| 圖片檔案 | 151 個 |
| 網站原始碼總大小 | 42 MB |
| static/（圖片為主）| 39 MB |
| articles/ | 2.0 MB |
| reviews/ | 196 KB |
| pillars/ | 104 KB |

---

### 目前 DNS / 網域狀態

| 項目 | 值 |
|------|-----|
| **域名** | fun1399.com |
| **域名註冊商** | GoDaddy (ns27/ns28.domaincontrol.com) |
| **目前 DNS 解析** | GoDaddy DNS |
| **A Records** | 75.2.60.5, 99.83.190.102 (Netlify edge) |
| **目前 Hosting** | Netlify |
| **Netlify Site ID** | 7232c8ac-d01c-454d-867b-f0eb8f4c7f94 |
| **Netlify Site Name** | statuesque-pithivier-bc9060 |
| **SSL** | Let's Encrypt（Netlify 自動管理）|
| **是否 Git repo** | ❌ 否（純本地檔案 + Netlify CLI deploy）|

---

### Netlify 專屬功能分析

#### ✅ 已使用功能

| 功能 | 用途 | Cloudflare Pages 替代方案 |
|------|------|------------------------|
| `netlify.toml` redirects | 88 個 .html → 無尾斜線 301 重導向 | `_redirects` 檔案 |
| Netlify CLI deploy | 直接上傳靜態檔案 | Git-based deploy 或 Wrangler CLI |
| Let's Encrypt SSL | 自動 HTTPS | Cloudflare 自動 SSL（更強）|
| Netlify Edge CDN | 全球 CDN | Cloudflare CDN（更強）|
| Netlify DNS（未使用）| — | Cloudflare DNS |

#### ⚠️ 需要特別注意

1. **88 個 redirects** 必須轉移到 Cloudflare Pages
2. **不是 Git repo** → Cloudflare Pages 需要 Git 才能 deploy
3. **純靜態網站** → 無 build process，直接上傳

---

## 第二階段：Cloudflare Pages 遷移規劃

---

### 步驟 1：建立 Git Repo

**原因**: Cloudflare Pages 只支援 Git-based deploy（GitHub/GitLab）

**操作**:
```bash
# 1. 初始化 Git repo
cd /root/.openclaw/workspace/fun1399-clean
git init
git add .
git commit -m "Initial commit - fun1399 static site"

# 2. 建立 GitHub repo（Hans 手動或我協助）
# 建議 repo 名稱: fun1399-site 或 fun1399-static

# 3. Push 到 GitHub
git remote add origin https://github.com/[USERNAME]/fun1399-site.git
git push -u origin main
```

**注意**:
- 目前不是 Git repo，這是必要步驟
- `.netlify/` 目錄不需要進入 repo（Cloudflare 不需要）
- 考慮加 `.gitignore` 排除 `.netlify/`

---

### 步驟 2：轉移 Redirects

**Netlify 目前設定**:
- 88 個 `[[redirects]]` 在 `netlify.toml`
- 全部為 `.html` → 無 `.html` 的 301 重導向
- 例如: `/articles/hg-casino-review.html` → `/articles/hg-casino-review`

**Cloudflare Pages 替代**: `_redirects` 檔案

**建立方式**:
```
# 在 fun1399-clean 根目錄建立 _redirects
/articles/hg-casino-review.html /articles/hg-casino-review 301
/articles/gm1688-casino-scam-review.html /articles/gm1688-casino-scam-review 301
# ...（88 條）
```

**快速產生腳本**:
```bash
# 從 netlify.toml 提取並轉換
grep -A3 '\[\[redirects\]\]' netlify.toml | \
  grep -E 'from|to|status' | \
  paste - - - | \
  sed 's/from = "\(.*\)".*to = "\(.*\)".*status = \(.*\)/\1 \2 \3/'
```

---

### 步驟 3：Cloudflare Pages 專案設定

**建立流程**:
1. 登入 Cloudflare Dashboard
2. 左側選單 → **Pages**
3. **Create a project** → Connect to Git
4. 選擇 GitHub → 授權 → 選擇 `fun1399-site` repo
5. **Build settings**:

| 設定 | 值 |
|------|-----|
| **Framework preset** | None（純靜態）|
| **Build command** | （留空，或 `echo "Static site"`）|
| **Build output directory** | `/`（根目錄）|
| **Root directory** | `/` |

6. **Save and Deploy** → 首次 deploy 完成

---

### 步驟 4：自訂網域綁定

**Cloudflare Pages 綁定流程**:
1. Cloudflare Pages → 專案 → **Custom domains**
2. 點 **Set up a custom domain**
3. 輸入 `fun1399.com`
4. Cloudflare 會檢查 DNS 設定

**DNS 設定方式（二選一）**:

#### 方案 A：Cloudflare DNS 接管（推薦 ⭐）

1. 將 fun1399.com 的 **Nameservers** 改為 Cloudflare:
   - 在 GoDaddy 將 NS 改為 Cloudflare 提供的 NS
   - 例如: `brett.ns.cloudflare.com`, `jocelyn.ns.cloudflare.com`
2. Cloudflare 自動管理 DNS + SSL + CDN
3. Pages 綁定自動完成

#### 方案 B：CNAME + GoDaddy DNS（保守）

1. 保持 GoDaddy DNS
2. 新增 **CNAME record**:
   - `www` → `[project-name].pages.dev`
   - `fun1399.com`（apex）→ 需要 ALIAS/ANAME（GoDaddy 不支援）
   - 或使用 Cloudflare DNS 處理 apex

**⚠️ 注意**: Apex domain（無 www）需要 Cloudflare DNS 或 ALIAS record

---

### 步驟 5：SSL 遷移

| 目前 (Netlify) | 遷移後 (Cloudflare) |
|----------------|---------------------|
| Let's Encrypt | Cloudflare Universal SSL（自動）|
| 由 Netlify 管理 | 由 Cloudflare 管理 |
| 需等待憑證簽發 | 即時生效 |
| 偶發 SSL 錯誤 | Cloudflare SSL 更穩定 |

**操作**: 無需手動操作，Cloudflare 自動處理

---

### 步驟 6：DNS 切換流程

**建議：零停機切換**

| 步驟 | 操作 | 停機時間 |
|------|------|----------|
| 1 | Cloudflare Pages deploy 完成 | 0 |
| 2 | 在 Cloudflare 新增 fun1399.com 為 custom domain | 0 |
| 3 | 測試 `.pages.dev` 版本是否正常 | 0 |
| 4 | 將 GoDaddy NS 改為 Cloudflare NS | **<5 分鐘** |
| 5 | 等待 DNS propagation（24-48h）| 0（並行）|
| 6 | 確認 SSL + DNS 正常 | 0 |
| 7 | 停用 Netlify site（保留不刪除）| 0 |

**Rollback 方案**:
- 若出問題，將 NS 改回 GoDaddy (`ns27/ns28.domaincontrol.com`)
- 或將 A records 改回 Netlify edge IPs
- Netlify site 保持不刪除，隨時可切回

---

### 步驟 7：Sitemap / Robots 調整

| 檔案 | 是否需要調整 | 說明 |
|------|-------------|------|
| `sitemap.xml` | ⚠️ 需要 | canonical URL 需更新為 `https://fun1399.com`（已正確，無需改）|
| `robots.txt` | ⚠️ 需要 | Sitemap URL 確認正確 |

**檢查項目**:
- sitemap.xml 中所有 `<loc>` 是否為 `https://fun1399.com/...` ✅ 已正確
- robots.txt 中 `Sitemap:` URL 是否正確 ✅ 已正確

---

### 步驟 8：Headers 轉移

**目前 Netlify headers**: `netlify.toml` 中 `headers = []`（無自訂 headers）

**Cloudflare Pages 替代**:
- 如需自訂 headers，使用 `_headers` 檔案
- 目前無需建立（網站無特殊 header 需求）

**建議加上的 headers**:
```
# _headers（可選，提升安全性）
/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
```

---

### 步驟 9：SEO 風險分析

| 風險 | 等級 | 說明 |
|------|------|------|
| **301 redirects 遺失** | 🔴 高 | 88 個 .html 重導向若遺失，Google 索引大量 404 |
| **URL 結構改變** | 🟡 中 | Cloudflare Pages 預設帶 trailing slash，需確認 |
| **SSL 中斷** | 🟡 中 | DNS 切換期間可能短暫無 SSL |
| **DNS propagation** | 🟢 低 | 全球 DNS 快取需 24-48h |
| **CDN 效能變化** | 🟢 低 | Cloudflare CDN 通常比 Netlify 快 |

**降低風險措施**:
1. ✅ 確保 `_redirects` 檔案完整轉移 88 條規則
2. ✅ 使用 Cloudflare DNS 接管（SSL 不會中斷）
3. ✅ 切換前用 `curl` 測試 `.pages.dev` 版本
4. ✅ 保留 Netlify site 不刪除（rollback 保險）

---

### 步驟 10：Cloudflare Cache 建議

| 設定 | 建議值 | 說明 |
|------|--------|------|
| **Caching Level** | Standard | 正常快取 |
| **Browser Cache TTL** | 4 hours | HTML 頁面 |
| **Edge Cache TTL** | 1 month | 靜態資源（CSS/JS/圖片）|
| **Always Online** | On | 源站故障時顯示快取版本 |
| **Auto Minify** | On (CSS/JS/HTML) | 壓縮檔案 |
| **Brotli** | On | 更好的壓縮 |

---

### 步驟 11：Netlify → Cloudflare 功能對照

| 功能 | Netlify | Cloudflare Pages | 是否需要調整 |
|------|---------|-----------------|-------------|
| 靜態網站 hosting | ✅ | ✅ | 否 |
| 全球 CDN | ✅ | ✅（更強）| 否 |
| 自動 SSL | ✅ Let's Encrypt | ✅ Universal SSL | 否 |
| Custom domain | ✅ | ✅ | DNS 切換 |
| Redirects | `netlify.toml` | `_redirects` | ✅ 需要轉移 |
| Headers | `netlify.toml` | `_headers` | 目前無需 |
| Functions/Workers | ✅ | ✅ Cloudflare Workers | 目前無需 |
| Git-based deploy | ✅ | ✅ | 需要建立 Git repo |
| CLI deploy | `netlify deploy` | `wrangler pages deploy` | 需要學習 |
| Branch deploys | ✅ | ✅ | 否 |
| Form handling | ✅ | ❌ 無原生 | 目前無需 |
| Identity/Auth | ✅ | ❌ 無原生 | 目前無需 |
| Analytics | ✅ | ✅（更強）| 否 |

---

### 步驟 12：Deploy Workflow 建議

**遷移後的工作流程**:

```
1. 修改文章/內容
   ↓
2. git add + git commit
   ↓
3. git push origin main
   ↓
4. Cloudflare Pages 自動 build + deploy（~30秒）
   ↓
5. 驗證 https://fun1399.com（production）
```

**替代方案（不用 Git）**:
- Cloudflare Pages 支援 **Direct Upload**（Wrangler CLI）
- `wrangler pages deploy /path/to/fun1399-clean`
- 但推薦 Git-based（版本控制 + 自動化）

---

## 遺漏檔案檢查

| 檔案類型 | 狀態 |
|----------|------|
| 所有 HTML | ✅ 已備份 |
| 所有 CSS | ✅ 已備份 |
| 所有圖片 | ✅ 已備份 |
| sitemap.xml | ✅ 已備份 |
| robots.txt | ✅ 已備份 |
| netlify.toml | ✅ 已備份 |
| .netlify/ | ✅ 已備份 |
| 無其他 config 檔案 | — |

**確認**: 無遺漏檔案

---

## 執行建議

### 優先順序

| 優先 | 任務 | 估計時間 |
|------|------|----------|
| 1 | 建立 Git repo + push GitHub | 10 分鐘 |
| 2 | 轉移 88 條 redirects → `_redirects` | 15 分鐘 |
| 3 | Cloudflare Pages 建立 + deploy | 10 分鐘 |
| 4 | 測試 `.pages.dev` 版本 | 15 分鐘 |
| 5 | DNS 切換（GoDaddy NS → Cloudflare）| 10 分鐘 + 24h propagation |
| 6 | 驗證 SSL + 全站功能 | 30 分鐘 |
| 7 | 保留 Netlify（不刪除）| 0 分鐘 |

**總計**: ~1.5 小時操作 + 24-48 小時 DNS propagation

---

## 準備好開始遷移

等待 Hans 確認後執行。目前：
- ✅ 備份完成
- ✅ 規劃完成
- ❌ 未修改 DNS
- ❌ 未切換 hosting
