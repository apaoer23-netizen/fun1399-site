# P3 MBM 2026年9月評價｜FAQ 模板補丁完成報告（Preview Only）

- **日期**：2026-09-23
- **基準 Commit（親自重新核對）**：origin/main＝`bf946077e6689729d396df124fbfc7a10bf08f67`（未變）；Preview 分支前版 `4c2b6ab`
- **本輪 Preview Commit**：`1f4e742`（分支 `preview/mbm-2026-09-review`；main 未動、未 Merge、未部署 Production）
- **公開 Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026（HTTP 200）

## 修改檔案清單

1. `articles/mbm-casino-review-may-2026.html`（僅本篇；大老爺文章與其他文章未動，`git status` 乾淨僅本篇）

## FAQ 可見模板（已依大老爺版型）

- 外層 `.faq-section`；每題 `<details class="faq-item">` 淺灰背景 `#f8f9fa`、淡灰邊 `#e9ecef`、12px 圓角、卡片間距 12px
- 問題 `<summary>`（flex/gap 12px/list-style none/18px/600）、答案 `<div class="faq-answer"><p>…</p></div>`
- 第一題 `open` 預設展開；第二、三題預設收合；H2 `id="faq"` 標題「常見問題 FAQ」，目錄錨點 `#faq` 實測可跳轉（目錄標籤同步為「常見問題 FAQ」）
- 未複製大老爺的任何問題、答案、平台名稱或數據；未引入共用 CSS
- 本篇局部手機樣式：`<style>@media (max-width:480px){ .faq-section .faq-answer{padding:0 18px 18px 18px !important} }</style>`（僅本篇作用域）
- 純原生 `<details>`，無任何 JavaScript

## 三題可見 FAQ 完整文字（逐字）

**Q1：MBM首存1,000送1,000，USDT也只要1倍流水嗎？**
不是。MBM活動頁把台幣和USDT分開：台幣是「本金＋贈金」1倍流水，USDT是10倍；申請資格與時點也要一併確認。

**Q2：MBM新會員就有0.8%返水嗎？**
不能這樣算。電子與真人百家樂依VIP等級給返水，VIP1、VIP2表列0.4%，VIP6才列0.8%。

**Q3：MBM出金真的幾分鐘就會到帳嗎？**
目前沒有完整申請和入帳紀錄可計時。使用者提供的匿名對話有人覺得快，但不能拿來保證其他人的到帳時間。

## 落稿前平台條款重新核對（今日 Playwright 渲染，唯讀）

- 首儲「王牌登場，首存1000送1000」：台幣（本金＋優惠禮金）×1 倍流水、USDT ×10 倍；申請方式「儲值點數成功後未投注前聯繫LINE客服提出申請」→ 與 Q1 一致 ✓（活動期間現示 2026/8/18–2026/12/31）
- VIP 表（`promos?id=VIP` 今日重抓）：電子遊戲返水 VIP1 0.4%／VIP2 0.4%／VIP3 0.5%／VIP4 0.6%／VIP5 0.7%／VIP6 0.8%；真人百家同表；體育 0.8% 全級 → 與 Q2 一致 ✓
- 規則無變更，無需降低表述

## FAQPage JSON-LD 完整內容

```json
{
  "@type": "FAQPage",
  "mainEntity": [
    { "@type": "Question", "name": "MBM首存1,000送1,000，USDT也只要1倍流水嗎？", "acceptedAnswer": { "@type": "Answer", "text": "不是。MBM活動頁把台幣和USDT分開：台幣是「本金＋贈金」1倍流水，USDT是10倍；申請資格與時點也要一併確認。" } },
    { "@type": "Question", "name": "MBM新會員就有0.8%返水嗎？", "acceptedAnswer": { "@type": "Answer", "text": "不能這樣算。電子與真人百家樂依VIP等級給返水，VIP1、VIP2表列0.4%，VIP6才列0.8%。" } },
    { "@type": "Question", "name": "MBM出金真的幾分鐘就會到帳嗎？", "acceptedAnswer": { "@type": "Answer", "text": "目前沒有完整申請和入帳紀錄可計時。使用者提供的匿名對話有人覺得快，但不能拿來保證其他人的到帳時間。" } }
  ]
}
```

- 僅含頁面實際可見三題；無額外說明、無評分/Review/Product/出金速度；不重複 FAQPage、無尾逗號

## 驗證結果

**JSON-LD 解析**：全部 script 區塊 `JSON.parse` 通過（僅 1 個 FAQPage）。
**可見 vs Schema 逐字比對**：3 題 name 與 acceptedAnswer.text 全部逐字一致（mm=0，五寬度一致）。
**五寬度驗收（320/375/390/430/1440，結果一致）**：
- 問題文字自然換行 ✓；箭頭與文字不重疊 ✓
- 卡片不超出文章寬度、答案無橫向溢位、無頁面橫向溢位 ✓
- 320px 下 `.faq-answer` 套用局部手機留白（0 18px 18px 18px）✓
- 點擊整個 `<summary>` 可展開/收合（原生 details，實測 toggle）✓
- 真實鍵盤：Tab 可聚焦 summary、Enter 展開、Space 收合 ✓
- 未使用任何破壞原生可用性的 JS ✓

**其他段落**：Title/Description/H1/Canonical/作者/封面/三張回饋圖/CTA/延伸閱讀/免責聲明均未改動（dateModified 依實際修改日更新為 `2026-09-23T10:10:00+08:00`）。
**大老爺文章**：`git diff` 無變更；其他文章未動。

## 未確認 / 規則變更項目

- 無規則變更（首儲流水與 VIP 返水表今日重核一致）
- 最低託售額度仍查不到（維持不寫死）
- GSC 無存取憑證 → 未查到
- 封面文案「出金快速／安全可靠／玩家好評」仍列未確認（同前次回報）

## 聲明

本輪僅交付 Preview。未收到「正式發布／部署」指示前不進 Production。
