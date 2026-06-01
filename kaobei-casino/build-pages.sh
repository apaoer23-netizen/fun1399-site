#!/bin/bash
set -e

BASE="/root/.openclaw/workspace/kaobei-casino"

# Common head template function
common_head() {
  local title="$1"
  local desc="$2"
  local og_type="${3:-website}"
  local og_url="${4:-https://kaobei-casino.example.com/}"
  local canonical="${5:-https://kaobei-casino.example.com/}"
  local schema="${6:-}"

  cat <<EOF
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="$desc">
<meta property="og:title" content="$title">
<meta property="og:description" content="$desc">
<meta property="og:type" content="$og_type">
<meta property="og:url" content="$og_url">
<meta property="og:site_name" content="靠北娛樂城">
<link rel="canonical" href="$canonical">
<link rel="stylesheet" href="/static/styles.css">
<title>$title</title>
${schema:+$schema}
</head>
EOF
}

common_header() {
  cat <<'EOF'
<header class="site-header">
  <div class="header-inner">
    <a href="/" class="site-logo">
      <span class="logo-icon">KB</span>
      <span class="logo-text">
        <span>靠北娛樂城</span>
        <small>爭議紀錄與風險觀察</small>
      </span>
    </a>
    <nav class="main-nav">
      <a href="/cases/">爭議案件</a>
      <a href="/withdrawal-issues/">出金問題</a>
      <a href="/casinos/">平台紀錄</a>
      <a href="/about/">關於本站</a>
      <a href="/report/" class="nav-cta">我要回報</a>
    </nav>
    <button class="mobile-menu-btn" aria-label="開啟選單" onclick="document.querySelector('.main-nav').classList.toggle('mobile-open')">
      <span></span><span></span><span></span>
    </button>
  </div>
</header>
EOF
}

common_footer() {
  cat <<'EOF'
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <span class="logo-icon">KB</span>
        <strong>靠北娛樂城</strong>
        <p style="margin-top:8px; line-height:1.6;">
          線上娛樂城爭議紀錄與風險觀察資料庫。<br>
          所有資料僅供參考，不構成任何投資或博弈建議。
        </p>
      </div>
      <div class="footer-links">
        <h4>導覽</h4>
        <a href="/cases/">爭議案件</a>
        <a href="/withdrawal-issues/">出金問題</a>
        <a href="/casinos/">平台紀錄</a>
        <a href="/report/">我要回報</a>
      </div>
      <div class="footer-links">
        <h4>關於</h4>
        <a href="/about/">關於本站</a>
        <a href="/disclaimer/">免責聲明</a>
        <a href="/contact/">聯絡與申訴</a>
        <a href="https://fun1399.com/" target="_blank" rel="noopener">fun1399</a>
      </div>
    </div>
    <div class="footer-bottom">
      <p>© 2025 靠北娛樂城 · 本站為觀察與紀錄平台，不提供任何博弈服務 · <a href="/disclaimer/">免責聲明</a></p>
      <p style="margin-top:4px; font-size:0.7rem;">「詐騙」「黑網」「不出金」等詞彙僅為搜尋常用詞彙，不代表本站對任何平台之指控。</p>
    </div>
  </div>
</footer>
</body></html>
EOF
}

search_terms_disclaimer='<div class="search-terms-disclaimer">
<strong>關於搜尋用詞聲明：</strong> 本站使用「詐騙」「黑網」「不出金」等詞彙僅因這些是網路搜尋中常見的查詢關鍵字，並不代表本站對任何特定平台做出直接指控。所有紀錄均標示來源與查證狀態，僅供參考。
</div>'

demo_banner='<div class="demo-banner">
  ⚠️ 測試資料／示範頁面，非真實平台爭議紀錄
</div>'

# ========== /cases/index.html ==========
common_head "爭議案件列表 | 靠北娛樂城" "靠北娛樂城爭議案件資料庫，整理線上娛樂城出金延遲、客服糾紛、優惠條款等爭議事件。所有資料僅供參考。" "website" "https://kaobei-casino.example.com/cases/" "https://kaobei-casino.example.com/cases/" > "$BASE/cases/index.html"
cat >> "$BASE/cases/index.html" <<'EOF'
<body>
EOF
common_header >> "$BASE/cases/index.html"
cat >> "$BASE/cases/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>爭議案件</span></nav>
    <h1>爭議案件資料庫</h1>
    <p>整理中的線上娛樂城爭議事件紀錄（目前僅展示示範資料）</p>
  </div>
</section>

<section class="section">
  <div class="container">
EOF
echo "$search_terms_disclaimer" >> "$BASE/cases/index.html"
cat >> "$BASE/cases/index.html" <<'EOF'

    <div class="data-table-wrap">
      <table class="data-table">
        <thead>
          <tr>
            <th>案件編號</th>
            <th>平台</th>
            <th>爭議類型</th>
            <th>事件日期</th>
            <th>狀態</th>
            <th>查證</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><a href="/case/demo-case-001/">DEMO-CASE-001</a> <span class="badge badge-demo">示範</span></td>
            <td><a href="/casino/demo-casino-a/">Demo Casino A</a></td>
            <td>出金延遲</td>
            <td class="timestamp">2025-04-20</td>
            <td><span class="badge badge-pending">資料整理中</span></td>
            <td><span class="badge badge-review">審核中</span></td>
          </tr>
          <tr>
            <td><a href="/case/demo-case-002/">DEMO-CASE-002</a> <span class="badge badge-demo">示範</span></td>
            <td><a href="/casino/demo-casino-b/">Demo Casino B</a></td>
            <td>客服糾紛</td>
            <td class="timestamp">2025-04-28</td>
            <td><span class="badge badge-pending">資料整理中</span></td>
            <td><span class="badge badge-review">審核中</span></td>
          </tr>
          <tr>
            <td><a href="/case/demo-case-003/">DEMO-CASE-003</a> <span class="badge badge-demo">示範</span></td>
            <td><a href="/casino/demo-casino-a/">Demo Casino A</a></td>
            <td>優惠條款</td>
            <td class="timestamp">2025-05-08</td>
            <td><span class="badge badge-pending">資料整理中</span></td>
            <td><span class="badge badge-review">審核中</span></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/cases/index.html"

# ========== /withdrawal-issues/index.html ==========
common_head "出金問題資料庫 | 靠北娛樂城" "整理線上娛樂城出金延遲、拒付、審核卡關等問題的觀察紀錄。所有資料僅供參考，不構成投資建議。" "website" "https://kaobei-casino.example.com/withdrawal-issues/" "https://kaobei-casino.example.com/withdrawal-issues/" > "$BASE/withdrawal-issues/index.html"
cat >> "$BASE/withdrawal-issues/index.html" <<'EOF'
<body>
EOF
common_header >> "$BASE/withdrawal-issues/index.html"
cat >> "$BASE/withdrawal-issues/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>出金問題</span></nav>
    <h1>出金問題資料庫</h1>
    <p>線上娛樂城提款延遲、拒付、審核異常等問題的觀察紀錄</p>
  </div>
</section>

<section class="section">
  <div class="container">
EOF
echo "$search_terms_disclaimer" >> "$BASE/withdrawal-issues/index.html"
cat >> "$BASE/withdrawal-issues/index.html" <<'EOF'

    <div class="alert alert-info">
      <span class="alert-icon">ℹ️</span>
      <div>目前本站處於建置階段，以下僅展示示範資料。實際公開紀錄將於正式上線後逐步整理發布。</div>
    </div>

    <h2 style="font-size:1.1rem; margin:24px 0 12px;">相關爭議案件</h2>
    <div class="card-grid card-grid-3">
      <article class="card">
        <span class="badge badge-demo">示範</span>
        <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-001/">Demo Casino A 出金延遲爭議</a></h3>
        <p class="card-meta">2025-04-20 · 審核中</p>
        <p class="card-body">提款申請後超過 72 小時未處理，客服回覆前後不一致。</p>
      </article>
    </div>

    <h2 style="font-size:1.1rem; margin:32px 0 12px;">常見出金問題類型</h2>
    <div class="card-grid card-grid-2 card-grid-4" style="gap:12px;">
      <div class="card">
        <h3 style="font-size:1rem; margin-bottom:4px;">⏱️ 處理延遲</h3>
        <p style="font-size:0.82rem; color:var(--text-muted);">超過宣稱的處理時間仍未到帳</p>
      </div>
      <div class="card">
        <h3 style="font-size:1rem; margin-bottom:4px;">❌ 無故拒付</h3>
        <p style="font-size:0.82rem; color:var(--text-muted);">提款被拒但理由不明確</p>
      </div>
      <div class="card">
        <h3 style="font-size:1rem; margin-bottom:4px;">🔍 反覆審核</h3>
        <p style="font-size:0.82rem; color:var(--text-muted);">被要求重複提交證件或資料</p>
      </div>
      <div class="card">
        <h3 style="font-size:1rem; margin-bottom:4px;">📉 帳戶凍結</h3>
        <p style="font-size:0.82rem; color:var(--text-muted);">出金前帳戶被限制或凍結</p>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/withdrawal-issues/index.html"

# ========== /casinos/index.html ==========
common_head "平台風險紀錄 | 靠北娛樂城" "線上娛樂城平台風險觀察資料庫，包含爭議統計、玩家反映整理與風險分數。所有資料僅供參考。" "website" "https://kaobei-casino.example.com/casinos/" "https://kaobei-casino.example.com/casinos/" > "$BASE/casinos/index.html"
cat >> "$BASE/casinos/index.html" <<'EOF'
<body>
EOF
common_header >> "$BASE/casinos/index.html"
cat >> "$BASE/casinos/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>平台紀錄</span></nav>
    <h1>平台風險紀錄</h1>
    <p>各線上娛樂城的觀察摘要、爭議統計與風險分數</p>
  </div>
</section>

<section class="section">
  <div class="container">
EOF
echo "$search_terms_disclaimer" >> "$BASE/casinos/index.html"
cat >> "$BASE/casinos/index.html" <<'EOF'

    <div class="alert alert-info">
      <span class="alert-icon">ℹ️</span>
      <div>目前本站處於建置階段，以下僅展示示範資料。實際平台紀錄將於正式上線後逐步整理發布。</div>
    </div>

    <div class="card-grid card-grid-2" style="margin-top:24px;">
      <article class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
          <div>
            <h3 class="card-title"><a href="/casino/demo-casino-a/">Demo Casino A</a></h3>
            <span class="badge badge-demo">示範資料</span>
          </div>
          <div style="text-align:right;">
            <div style="font-size:1.6rem; font-weight:700; color:var(--warning-red);">72</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">風險分數</div>
          </div>
        </div>
        <p class="card-body">綜合娛樂城平台 · 示範資料中有 2 筆爭議紀錄（出金延遲、優惠條款）</p>
        <div class="card-footer">
          <span class="badge badge-pending">持續觀察</span>
          <span class="timestamp">更新：2025-05-15</span>
        </div>
      </article>
      <article class="card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
          <div>
            <h3 class="card-title"><a href="/casino/demo-casino-b/">Demo Casino B</a></h3>
            <span class="badge badge-demo">示範資料</span>
          </div>
          <div style="text-align:right;">
            <div style="font-size:1.6rem; font-weight:700; color:var(--warning-orange);">58</div>
            <div style="font-size:0.75rem; color:var(--text-muted);">風險分數</div>
          </div>
        </div>
        <p class="card-body">體育博彩為主 · 示範資料中有 1 筆爭議紀錄（客服糾紛）</p>
        <div class="card-footer">
          <span class="badge badge-pending">持續觀察</span>
          <span class="timestamp">更新：2025-05-10</span>
        </div>
      </article>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/casinos/index.html"

echo "Pages 2-4 created."
