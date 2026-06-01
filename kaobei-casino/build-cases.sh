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

# Helper: build case page
case_schema() {
  cat <<EOF
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "$1",
  "description": "$2",
  "url": "$3",
  "datePublished": "$4",
  "dateModified": "$5",
  "publisher": {
    "@type": "Organization",
    "name": "靠北娛樂城",
    "url": "https://kaobei-casino.example.com/"
  }
}
</script>
EOF
}

# ========== /case/demo-case-001/index.html ==========
common_head "Demo Casino A 出金延遲爭議整理 | 靠北娛樂城" "玩家反映 Demo Casino A 出金處理時間異常延長，客服回覆不一致。本頁為示範資料，非真實平台爭議紀錄。" "article" "https://kaobei-casino.example.com/case/demo-case-001/" "https://kaobei-casino.example.com/case/demo-case-001/" "$(case_schema "Demo Casino A 出金延遲爭議整理" "玩家反映出金處理時間異常延長" "https://kaobei-casino.example.com/case/demo-case-001/" "2025-04-20" "2025-05-15")" > "$BASE/case/demo-case-001/index.html"
common_header >> "$BASE/case/demo-case-001/index.html"
cat >> "$BASE/case/demo-case-001/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <a href="/cases/">爭議案件</a> · <span>DEMO-CASE-001</span></nav>
    <h1>Demo Casino A 出金延遲爭議</h1>
    <p>案件編號 DEMO-CASE-001 · 2025-04-20 · <span class="badge badge-demo">示範資料</span> <span class="badge badge-pending">審核中</span></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-content">
EOF
echo "$demo_banner" >> "$BASE/case/demo-case-001/index.html"
echo "$search_terms_disclaimer" >> "$BASE/case/demo-case-001/index.html"
cat >> "$BASE/case/demo-case-001/index.html" <<'EOF'

      <h2>事件摘要</h2>
      <p>示範資料：Demo Casino A 被玩家反映提款申請後超過預期處理時間仍未到帳，且客服回覆存在不一致情況。</p>

      <h2>玩家反映內容（示範）</h2>
      <ul>
        <li>提款申請提交後超過 72 小時未處理</li>
        <li>客服先表示「正在審核」，後改稱「系統維護中」</li>
        <li>未收到任何書面通知說明延遲原因</li>
      </ul>

      <h2>平台回應</h2>
      <p>目前無公開回應（示範資料）。</p>

      <h2>相關資料</h2>
      <div class="card" style="margin-bottom:16px;">
        <table class="data-table" style="min-width:auto;">
          <tbody>
            <tr><td style="font-weight:600; width:120px;">案件編號</td><td>DEMO-CASE-001</td></tr>
            <tr><td style="font-weight:600;">相關平台</td><td><a href="/casino/demo-casino-a/">Demo Casino A</a></td></tr>
            <tr><td style="font-weight:600;">爭議類型</td><td>出金延遲</td></tr>
            <tr><td style="font-weight:600;">事件日期</td><td>2025-04-20</td></tr>
            <tr><td style="font-weight:600;">查證狀態</td><td><span class="badge badge-review">審核中</span></td></tr>
            <tr><td style="font-weight:600;">平台回應</td><td><span class="badge badge-pending">無回應</span></td></tr>
          </tbody>
        </table>
      </div>

      <h2>相關案件</h2>
      <div class="card-grid card-grid-2" style="margin-bottom:16px;">
        <article class="card">
          <span class="badge badge-demo">示範</span>
          <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-002/">Demo Casino B 客服態度爭議</a></h3>
          <p class="card-meta">客服糾紛 · 2025-04-28</p>
        </article>
        <article class="card">
          <span class="badge badge-demo">示範</span>
          <h3 class="card-title" style="margin-top:8px;"><a href="/case/demo-case-003/">Demo Casino A 優惠條款爭議</a></h3>
          <p class="card-meta">優惠條款 · 2025-05-08</p>
        </article>
      </div>

      <div class="alert alert-demo">
        <span class="alert-icon">⚠️</span>
        <div>本頁為測試資料／示範頁面，非真實平台爭議紀錄。所有內容均為虛構，僅供系統展示與功能測試使用。</div>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/case/demo-case-001/index.html"

# ========== /case/demo-case-002/index.html ==========
common_head "Demo Casino B 客服態度爭議整理 | 靠北娛樂城" "玩家反映 Demo Casino B 客服回覆態度不佳、解決問題效率低。本頁為示範資料，非真實平台爭議紀錄。" "article" "https://kaobei-casino.example.com/case/demo-case-002/" "https://kaobei-casino.example.com/case/demo-case-002/" "$(case_schema "Demo Casino B 客服態度爭議整理" "玩家反映客服回覆態度不佳" "https://kaobei-casino.example.com/case/demo-case-002/" "2025-04-28" "2025-05-10")" > "$BASE/case/demo-case-002/index.html"
common_header >> "$BASE/case/demo-case-002/index.html"
cat >> "$BASE/case/demo-case-002/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <a href="/cases/">爭議案件</a> · <span>DEMO-CASE-002</span></nav>
    <h1>Demo Casino B 客服態度爭議</h1>
    <p>案件編號 DEMO-CASE-002 · 2025-04-28 · <span class="badge badge-demo">示範資料</span> <span class="badge badge-pending">審核中</span></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-content">
EOF
echo "$demo_banner" >> "$BASE/case/demo-case-002/index.html"
echo "$search_terms_disclaimer" >> "$BASE/case/demo-case-002/index.html"
cat >> "$BASE/case/demo-case-002/index.html" <<'EOF'

      <h2>事件摘要</h2>
      <p>示範資料：多位玩家反映 Demo Casino B 的客服窗口回覆延遲、態度冷淡，且對帳戶異常問題未能提供有效協助。</p>

      <h2>玩家反映內容（示範）</h2>
      <ul>
        <li>在線客服平均等待時間超過 15 分鐘</li>
        <li>客服人員對規則解釋前後不一致</li>
        <li>問題升級後未收到後續跟進</li>
      </ul>

      <h2>平台回應</h2>
      <p>目前無公開回應（示範資料）。</p>

      <h2>相關資料</h2>
      <div class="card" style="margin-bottom:16px;">
        <table class="data-table" style="min-width:auto;">
          <tbody>
            <tr><td style="font-weight:600; width:120px;">案件編號</td><td>DEMO-CASE-002</td></tr>
            <tr><td style="font-weight:600;">相關平台</td><td><a href="/casino/demo-casino-b/">Demo Casino B</a></td></tr>
            <tr><td style="font-weight:600;">爭議類型</td><td>客服糾紛</td></tr>
            <tr><td style="font-weight:600;">事件日期</td><td>2025-04-28</td></tr>
            <tr><td style="font-weight:600;">查證狀態</td><td><span class="badge badge-review">審核中</span></td></tr>
          </tbody>
        </table>
      </div>

      <div class="alert alert-demo">
        <span class="alert-icon">⚠️</span>
        <div>本頁為測試資料／示範頁面，非真實平台爭議紀錄。所有內容均為虛構，僅供系統展示與功能測試使用。</div>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/case/demo-case-002/index.html"

# ========== /case/demo-case-003/index.html ==========
common_head "Demo Casino A 優惠條款爭議整理 | 靠北娛樂城" "玩家反映 Demo Casino A 首存優惠的洗碼倍率與宣傳說明不符。本頁為示範資料，非真實平台爭議紀錄。" "article" "https://kaobei-casino.example.com/case/demo-case-003/" "https://kaobei-casino.example.com/case/demo-case-003/" "$(case_schema "Demo Casino A 優惠條款爭議整理" "首存優惠洗碼倍率與宣傳說明不符" "https://kaobei-casino.example.com/case/demo-case-003/" "2025-05-08" "2025-05-15")" > "$BASE/case/demo-case-003/index.html"
common_header >> "$BASE/case/demo-case-003/index.html"
cat >> "$BASE/case/demo-case-003/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <a href="/cases/">爭議案件</a> · <span>DEMO-CASE-003</span></nav>
    <h1>Demo Casino A 優惠條款爭議</h1>
    <p>案件編號 DEMO-CASE-003 · 2025-05-08 · <span class="badge badge-demo">示範資料</span> <span class="badge badge-pending">審核中</span></p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-content">
EOF
echo "$demo_banner" >> "$BASE/case/demo-case-003/index.html"
echo "$search_terms_disclaimer" >> "$BASE/case/demo-case-003/index.html"
cat >> "$BASE/case/demo-case-003/index.html" <<'EOF'

      <h2>事件摘要</h2>
      <p>示範資料：玩家參與 Demo Casino A 首存優惠活動後，發現實際洗碼倍率與活動頁面說明存在落差。</p>

      <h2>玩家反映內容（示範）</h2>
      <ul>
        <li>活動頁面標示「洗碼 10 倍」，實際要求為「洗碼 20 倍」</li>
        <li>申請優惠時未收到條款變更通知</li>
        <li>嘗試聯繫客服確認時回覆緩慢</li>
      </ul>

      <h2>平台回應</h2>
      <p>目前無公開回應（示範資料）。</p>

      <h2>相關資料</h2>
      <div class="card" style="margin-bottom:16px;">
        <table class="data-table" style="min-width:auto;">
          <tbody>
            <tr><td style="font-weight:600; width:120px;">案件編號</td><td>DEMO-CASE-003</td></tr>
            <tr><td style="font-weight:600;">相關平台</td><td><a href="/casino/demo-casino-a/">Demo Casino A</a></td></tr>
            <tr><td style="font-weight:600;">爭議類型</td><td>優惠條款</td></tr>
            <tr><td style="font-weight:600;">事件日期</td><td>2025-05-08</td></tr>
            <tr><td style="font-weight:600;">查證狀態</td><td><span class="badge badge-review">審核中</span></td></tr>
          </tbody>
        </table>
      </div>

      <div class="alert alert-demo">
        <span class="alert-icon">⚠️</span>
        <div>本頁為測試資料／示範頁面，非真實平台爭議紀錄。所有內容均為虛構，僅供系統展示與功能測試使用。</div>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/case/demo-case-003/index.html"

echo "Case pages done."
