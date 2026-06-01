BASE="/root/.openclaw/workspace/kaobei-casino"

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
<body>
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

# ========== /casino/demo-casino-a/index.html ==========
common_head "Demo Casino A 風險觀察資料 | 靠北娛樂城" "Demo Casino A 的綜合風險觀察紀錄，包含玩家反映與出金爭議整理。本頁為示範資料，非真實平台。" "website" "https://kaobei-casino.example.com/casino/demo-casino-a/" "https://kaobei-casino.example.com/casino/demo-casino-a/" > "$BASE/casino/demo-casino-a/index.html"
common_header >> "$BASE/casino/demo-casino-a/index.html"
cat >> "$BASE/casino/demo-casino-a/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <a href="/casinos/">平台紀錄</a> · <span>Demo Casino A</span></nav>
    <h1>Demo Casino A <span class="badge badge-demo">示範資料</span></h1>
    <p>綜合娛樂城平台 · 風險觀察紀錄</p>
  </div>
</section>

<section class="section">
  <div class="container">
EOF
echo "$demo_banner" >> "$BASE/casino/demo-casino-a/index.html"
echo "$search_terms_disclaimer" >> "$BASE/casino/demo-casino-a/index.html"
cat >> "$BASE/casino/demo-casino-a/index.html" <<'EOF'

    <div class="card" style="margin-bottom:24px;">
      <h2 style="font-size:1.1rem; margin-bottom:12px;">風險評估</h2>
      <div class="risk-meter">
        <div class="risk-bar"><div class="risk-bar-fill" style="width:72%;"></div></div>
        <span class="risk-score" style="color:var(--warning-red);">72 / 100</span>
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">風險分數為系統綜合評估，僅供參考。示範資料。</p>
    </div>

    <h2 style="font-size:1.1rem; margin:24px 0 12px;">平台資訊（示範）</h2>
    <div class="card" style="margin-bottom:24px;">
      <table class="data-table" style="min-width:auto;">
        <tbody>
          <tr><td style="font-weight:600; width:140px;">平台名稱</td><td>Demo Casino A</td></tr>
          <tr><td style="font-weight:600;">宣稱執照</td><td>Curaçao（待查證）</td></tr>
          <tr><td style="font-weight:600;">成立年份</td><td>2023（示範）</td></tr>
          <tr><td style="font-weight:600;">平台類型</td><td>綜合娛樂城</td></tr>
          <tr><td style="font-weight:600;">觀察狀態</td><td><span class="badge badge-pending">持續觀察中</span></td></tr>
        </tbody>
      </table>
    </div>

    <h2 style="font-size:1.1rem; margin:24px 0 12px;">相關爭議案件</h2>
    <div class="card-grid card-grid-2">
      <article class="card">
        <span class="badge badge-demo">示範</span>
        <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-001/">出金延遲爭議</a></h3>
        <p class="card-meta">2025-04-20 · 審核中</p>
        <p class="card-body">提款申請後超過預期處理時間仍未到帳。</p>
      </article>
      <article class="card">
        <span class="badge badge-demo">示範</span>
        <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-003/">優惠條款爭議</a></h3>
        <p class="card-meta">2025-05-08 · 審核中</p>
        <p class="card-body">首存優惠洗碼倍率與活動說明存在落差。</p>
      </article>
    </div>

    <div class="alert alert-demo" style="margin-top:24px;">
      <span class="alert-icon">⚠️</span>
      <div>本頁所有內容為示範資料，用於系統功能測試與介面展示。不構成對任何真實平台的評價或指控。</div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/casino/demo-casino-a/index.html"

# ========== /casino/demo-casino-b/index.html ==========
common_head "Demo Casino B 風險觀察資料 | 靠北娛樂城" "Demo Casino B 的綜合風險觀察紀錄，包含客服爭議整理。本頁為示範資料，非真實平台。" "website" "https://kaobei-casino.example.com/casino/demo-casino-b/" "https://kaobei-casino.example.com/casino/demo-casino-b/" > "$BASE/casino/demo-casino-b/index.html"
common_header >> "$BASE/casino/demo-casino-b/index.html"
cat >> "$BASE/casino/demo-casino-b/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <a href="/casinos/">平台紀錄</a> · <span>Demo Casino B</span></nav>
    <h1>Demo Casino B <span class="badge badge-demo">示範資料</span></h1>
    <p>體育博彩為主 · 風險觀察紀錄</p>
  </div>
</section>

<section class="section">
  <div class="container">
EOF
echo "$demo_banner" >> "$BASE/casino/demo-casino-b/index.html"
echo "$search_terms_disclaimer" >> "$BASE/casino/demo-casino-b/index.html"
cat >> "$BASE/casino/demo-casino-b/index.html" <<'EOF'

    <div class="card" style="margin-bottom:24px;">
      <h2 style="font-size:1.1rem; margin-bottom:12px;">風險評估</h2>
      <div class="risk-meter">
        <div class="risk-bar"><div class="risk-bar-fill" style="width:58%;"></div></div>
        <span class="risk-score" style="color:var(--warning-orange);">58 / 100</span>
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted); margin-top:4px;">風險分數為系統綜合評估，僅供參考。示範資料。</p>
    </div>

    <h2 style="font-size:1.1rem; margin:24px 0 12px;">平台資訊（示範）</h2>
    <div class="card" style="margin-bottom:24px;">
      <table class="data-table" style="min-width:auto;">
        <tbody>
          <tr><td style="font-weight:600; width:140px;">平台名稱</td><td>Demo Casino B</td></tr>
          <tr><td style="font-weight:600;">宣稱執照</td><td>MGA（待查證）</td></tr>
          <tr><td style="font-weight:600;">成立年份</td><td>2022（示範）</td></tr>
          <tr><td style="font-weight:600;">平台類型</td><td>體育博彩為主</td></tr>
          <tr><td style="font-weight:600;">觀察狀態</td><td><span class="badge badge-pending">持續觀察中</span></td></tr>
        </tbody>
      </table>
    </div>

    <h2 style="font-size:1.1rem; margin:24px 0 12px;">相關爭議案件</h2>
    <div class="card-grid card-grid-2">
      <article class="card">
        <span class="badge badge-demo">示範</span>
        <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-002/">客服態度爭議</a></h3>
        <p class="card-meta">2025-04-28 · 審核中</p>
        <p class="card-body">多位玩家反映客服回覆品質不佳、解決問題效率低。</p>
      </article>
    </div>

    <div class="alert alert-demo" style="margin-top:24px;">
      <span class="alert-icon">⚠️</span>
      <div>本頁所有內容為示範資料，用於系統功能測試與介面展示。不構成對任何真實平台的評價或指控。</div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/casino/demo-casino-b/index.html"

echo "Casino pages done."
