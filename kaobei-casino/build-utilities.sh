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

# ========== /report/index.html ==========
common_head "我要回報 | 靠北娛樂城" "透過表單回報線上娛樂城爭議事件，協助建立公開觀察資料。本站不提供博弈服務，所有資料僅供參考。" "website" "https://kaobei-casino.example.com/report/" "https://kaobei-casino.example.com/report/" > "$BASE/report/index.html"
common_header >> "$BASE/report/index.html"
cat >> "$BASE/report/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>我要回報</span></nav>
    <h1>爭議事件回報</h1>
    <p>協助我們建立更完整的線上娛樂城觀察資料</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div style="max-width:640px; margin:0 auto;">
      <div class="alert alert-info" style="margin-bottom:24px;">
        <span class="alert-icon">ℹ️</span>
        <div>目前本站處於建置階段，回報功能為示範表單。實際回報系統將於正式上線後啟用。你可以先將資料寄送至 <a href="mailto:[待 Hans 提供]">[待 Hans 提供]</a>。</div>
      </div>

      <div class="card">
        <form action="#" method="post" onsubmit="event.preventDefault(); alert('目前為示範模式，表單尚未連結實際收件系統。');">
          <div class="form-group">
            <label class="form-label" for="platform">涉及的娛樂城平台名稱 *</label>
            <input class="form-input" type="text" id="platform" name="platform" placeholder="例如：XX娛樂城" required>
            <p class="form-hint">請填寫平台官方名稱或網域名稱</p>
          </div>

          <div class="form-group">
            <label class="form-label" for="case_type">爭議類型 *</label>
            <select class="form-select" id="case_type" name="case_type" required>
              <option value="">請選擇...</option>
              <option value="withdrawal_delay">出金延遲</option>
              <option value="withdrawal_denied">出金被拒</option>
              <option value="customer_service">客服糾紛</option>
              <option value="bonus_terms">優惠條款爭議</option>
              <option value="account_frozen">帳戶凍結</option>
              <option value="fraud_suspected">疑似詐騙</option>
              <option value="other">其他</option>
            </select>
          </div>

          <div class="form-group">
            <label class="form-label" for="incident_date">事件發生日期（約略）</label>
            <input class="form-input" type="date" id="incident_date" name="incident_date">
          </div>

          <div class="form-group">
            <label class="form-label" for="description">事件描述 *</label>
            <textarea class="form-textarea" id="description" name="description" placeholder="請描述你遇到的問題，包含時間、經過、與平台的溝通情況等..." required></textarea>
            <p class="form-hint">請盡量客觀描述事實，避免情緒性用語。我們會將資訊整理歸檔。</p>
          </div>

          <div class="form-group">
            <label class="form-label" for="amount">涉及金額（可選）</label>
            <input class="form-input" type="text" id="amount" name="amount" placeholder="例如：NT$ 50,000">
          </div>

          <div class="form-group">
            <label class="form-label" for="contact">聯絡方式（可選，方便後續確認）</label>
            <input class="form-input" type="text" id="contact" name="contact" placeholder="Email 或 LINE ID">
          </div>

          <div class="form-group">
            <label style="display:flex; align-items:flex-start; gap:8px; cursor:pointer;">
              <input type="checkbox" required style="margin-top:4px;">
              <span style="font-size:0.85rem; color:var(--text-secondary);">我確認以上資訊為我親身經歷或經核實的資料，並同意本站將資訊整理為觀察紀錄公開（個人身份資訊將匿名處理）。</span>
            </label>
          </div>

          <button type="submit" class="btn btn-primary" style="width:100%;">提交回報（示範模式）</button>
        </form>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/report/index.html"

# ========== /about/index.html ==========
common_head "關於本站 | 靠北娛樂城" "靠北娛樂城是專注於線上娛樂城爭議紀錄與風險觀察的資料庫平台。本站為觀察與紀錄用途，不提供任何博弈服務。" "website" "https://kaobei-casino.example.com/about/" "https://kaobei-casino.example.com/about/" > "$BASE/about/index.html"
common_header >> "$BASE/about/index.html"
cat >> "$BASE/about/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>關於本站</span></nav>
    <h1>關於靠北娛樂城</h1>
    <p>我們在做什麼、為什麼做、以及我們不做什麼</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-content">
      <h2>本站宗旨</h2>
      <p>靠北娛樂城是一個專注於<strong>線上娛樂城爭議事件紀錄與風險觀察</strong>的資料庫平台。我們整理玩家反映、出金爭議、客服糾紛、優惠條款爭議等公開資訊，協助提升線上博弈領域的資訊透明度與玩家風險意識。</p>

      <h2>我們不做的事</h2>
      <ul>
        <li>本站<strong>不提供任何博弈服務</strong>，也不推薦任何娛樂城平台。</li>
        <li>我們不對任何平台做出「就是詐騙」的單方面指控。所有紀錄均標示來源與查證狀態。</li>
        <li>我們不介入玩家與平台之間的爭議調解。如有需要，請聯繫主管機關或法律途徑。</li>
        <li>我們不處理金錢或帳戶相關事務。所有金流請直接與平台處理。</li>
      </ul>

      <h2>資料來源與查證</h2>
      <p>本站資料來自公開管道整理，包括玩家回報、社群討論、新聞報導等。每筆紀錄均標示：</p>
      <ul>
        <li><strong>來源類型</strong>：玩家回報 / 新聞 / 論壇討論 / 其他</li>
        <li><strong>查證狀態</strong>：待審核 / 初步查證 / 多方確認 / 無法查證</li>
        <li><strong>平台回應狀態</strong>：無回應 / 已回應 / 處理中 / 已解決</li>
      </ul>

      <h2>與 fun1399 的關係</h2>
      <p>靠北娛樂城由 fun1399 團隊延伸建置，作為獨立的爭議觀察資料庫運作。fun1399 提供娛樂城評測與安全知識內容，而靠北娛樂城專注於爭議事件的客觀紀錄與資料整理。</p>
      <p>如需了解更多線上博弈安全資訊，請前往 <a href="https://fun1399.com/" target="_blank" rel="noopener">fun1399</a>。</p>

      <h2>聯絡我們</h2>
      <p>LINE：[待 Hans 提供]<br>
      Email：<a href="mailto:[待 Hans 提供]">[待 Hans 提供]</a></p>

      <div class="alert alert-info">
        <span class="alert-icon">ℹ️</span>
        <div>本站為建置中階段，部分功能尚未上線。如有任何問題或建議，歡迎透過上述管道聯繫。</div>
      </div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/about/index.html"

# ========== /disclaimer/index.html ==========
common_head "免責聲明 | 靠北娛樂城" "靠北娛樂城免責聲明。本站為觀察與紀錄平台，所有資料僅供參考，不構成任何投資、法律或博弈建議。" "website" "https://kaobei-casino.example.com/disclaimer/" "https://kaobei-casino.example.com/disclaimer/" > "$BASE/disclaimer/index.html"
common_header >> "$BASE/disclaimer/index.html"
cat >> "$BASE/disclaimer/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>免責聲明</span></nav>
    <h1>免責聲明</h1>
    <p>使用本站前，請詳閱以下聲明</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="article-content">
      <h2>一、本站定位</h2>
      <p>靠北娛樂城（以下稱「本站」）是一個<strong>線上娛樂城爭議事件的觀察與紀錄平台</strong>。本站僅就公開資訊進行整理與歸檔，不提供任何博弈服務、投資建議或法律意見。</p>

      <h2>二、資料性質</h2>
      <ul>
        <li>本站所有紀錄均標示來源與查證狀態，部分資料處於「待審核」或「資料整理中」狀態。</li>
        <li>本站不對任何平台做出確定性指控。紀錄中的描述為「玩家反映」或「觀察紀錄」，不代表本站立場。</li>
        <li>「詐騙」「黑網」「不出金」等詞彙僅為網路搜尋常見關鍵字，不代表本站對任何特定平台之認定。</li>
      </ul>

      <h2>三、資訊準確性</h2>
      <p>本站致力於確保資訊準確性，但不保證所有內容的完整、即時或正確。使用者應自行判斷資訊可信度，並就重要事項向相關平台或專業人士查證。</p>

      <h2>四、風險自負</h2>
      <p>線上博弈存在固有風險。本站提供的資訊僅供參考，使用者應自行承擔參與線上博弈活動的所有風險與後果。本站不對任何損失負責。</p>

      <h2>五、版權與轉載</h2>
      <p>本站內容的版權歸屬依各來源標示。未經授權，請勿複製、轉載或改作本站內容用於商業用途。</p>

      <h2>六、聯絡與申訴</h2>
      <p>如認為本站內容有誤、侵害權益，或希望提出更正要求，請透過 <a href="/contact/">聯絡頁面</a> 與我們聯繫。我們將在合理時間內審查並回應。</p>

      <p style="margin-top:32px; color:var(--text-muted); font-size:0.85rem;">最後更新：2025-05-30</p>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/disclaimer/index.html"

# ========== /contact/index.html ==========
common_head "聯絡與申訴 | 靠北娛樂城" "聯絡靠北娛樂城團隊、提出內容更正要求或申訴。本站為觀察與紀錄平台，不提供博弈服務。" "website" "https://kaobei-casino.example.com/contact/" "https://kaobei-casino.example.com/contact/" > "$BASE/contact/index.html"
common_header >> "$BASE/contact/index.html"
cat >> "$BASE/contact/index.html" <<'EOF'
<main>
<section class="page-header">
  <div class="container">
    <nav class="breadcrumb"><a href="/">首頁</a> · <span>聯絡與申訴</span></nav>
    <h1>聯絡與申訴</h1>
    <p>內容更正、申訴、合作或其他聯繫需求</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="card-grid card-grid-2">
      <div class="card">
        <h2 style="font-size:1.1rem; margin-bottom:12px;">📧 聯絡我們</h2>
        <p style="color:var(--text-secondary); margin-bottom:16px;">如有任何問題、建議或合作需求，歡迎透過以下管道聯繫：</p>
        <ul style="color:var(--text-secondary); font-size:0.9rem; line-height:2;">
          <li>LINE：[待 Hans 提供]</li>
          <li>Email：<a href="mailto:[待 Hans 提供]">[待 Hans 提供]</a></li>
        </ul>
        <p style="color:var(--text-muted); font-size:0.8rem; margin-top:12px;">回覆時間約 1–3 個工作天</p>
      </div>

      <div class="card">
        <h2 style="font-size:1.1rem; margin-bottom:12px;">📝 內容更正申訴</h2>
        <p style="color:var(--text-secondary); margin-bottom:16px;">如認為本站某篇紀錄內容有誤、需要更新，或認為內容侵害您的權益，請提供以下資訊：</p>
        <ul style="color:var(--text-secondary); font-size:0.9rem; line-height:2;">
          <li>涉及的頁面網址或案件編號</li>
          <li>具體需要更正的內容</li>
          <li>您的理由或佐證資料</li>
          <li>聯絡方式（方便我們回覆）</li>
        </ul>
        <p style="color:var(--text-muted); font-size:0.8rem; margin-top:12px;">我們會在收到後審查，並於合理時間內回應</p>
      </div>
    </div>

    <div class="alert alert-info" style="margin-top:24px;">
      <span class="alert-icon">ℹ️</span>
      <div>本站不提供博弈服務、不處理金錢爭議、不做法律諮詢。如需這些協助，請聯繫相關平台客服或專業人士。</div>
    </div>
  </div>
</section>
</main>
EOF
common_footer >> "$BASE/contact/index.html"

echo "Utility pages done."
