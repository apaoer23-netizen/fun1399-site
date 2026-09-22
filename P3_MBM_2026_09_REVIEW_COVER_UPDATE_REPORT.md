# P3 MBM 2026年9月評價（may-2026 篇）封面更新完成報告（Preview Only）

- **日期**：2026-09-22
- **基準（親自重新核對）**：origin/main＝`bf946077e6689729d396df124fbfc7a10bf08f67` 未變；正式頁 HTTP 200 與 repo 基準一致
- **交付 Commit**：`471cab7`（分支 `preview/mbm-2026-09-review`；main 未動）
- **公開 Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026（HTTP 200）
- **封面圖公開 URL（Preview）**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/static/images/articles/reviews/mbm-casino-review-sep-2026-cover.png（HTTP 200）

## 封面處理

1. 使用者原圖 `assets/MBM-2026-09-user-cover.png` 1586×992，SHA-256 核對＝`2d7a24cb3e823a28840828ee1a7e5fef328397e38424f134f1485b689623f1e9`（與指令包記載一致）
2. 目視確認內容：「MBM 娛樂城／2026年9月評價：玩家最新心得與出金回饋／玩家心得、出金回饋、真實評價、優惠資訊」；無 4.7/5、85%、出金實測、安全可靠/資金保障等宣稱
3. 依指令僅做尺寸輸出：**1280×800 PNG**（LANCZOS 等比縮放，比例 1.599:1→1.6:1 無裁切），存於本篇專用新路徑 `static/images/articles/reviews/mbm-casino-review-sep-2026-cover.png`（1.6MB）；**未覆寫**舊 5 月圖檔，舊檔保留 repo 未動未引用
4. HTML 四處引用同一新圖，均為 1280×800：
   - 正文 `<img>`（原位置原容器樣式、alt「MBM娛樂城2026年9月評價封面：玩家最新心得與出金回饋」、width/height 1280×800、`fetchpriority="high"`、**無 lazy**）
   - `og:image`＝`https://fun1399.com/static/images/articles/reviews/mbm-casino-review-sep-2026-cover.png`
   - `twitter:image` 同上
   - Article JSON-LD `image` 同上
5. dateModified/可見更新同步 `2026-09-22T17:00:00+08:00` / 2026年9月22日

## 驗證（Playwright：320/375/390/430/1440 五寬度，結果一致）

- 頁面 200、圖片 200；封面實載 naturalWidth=1280 ✅
- 四處引用逐字一致 ✅；無 lazy 首屏延遲設定 ✅
- FAQ 3 題逐字一致（mm=0）；H1=1；無橫向溢位
- JSON-LD：Article＋BreadcrumbList＋FAQPage；無 Review/Rating/Product
- 舊封面路徑於本篇 HTML 已零引用

## 其餘

- 正文維持 V4 定稿（本包草稿與證據圖與 V4 逐位元相同，已比對確認）
- 未確認：最低託售額度（不寫死）；GSC 無憑證未查到
- 未動 main、未部署 Production、未提交 GSC、未改 Cloudflare/其他文章/共用樣式

## 待使用者

- 驗收本 Preview；如需正式發布請明確指示「正式發布／部署」（屆時才動 main）
