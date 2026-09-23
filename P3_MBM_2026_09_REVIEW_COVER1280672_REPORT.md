# P3 MBM 2026年9月評價｜新封面（1280×672）替換完成報告（Preview Only）

- **日期**：2026-09-23
- **基準（親自重新核對）**：origin/main＝`bf946077e6689729d396df124fbfc7a10bf08f67` 未變；正式頁 HTTP 200（仍顯示舊 1280×672 封面，符合預期——本版僅 Preview）
- **交付 Commit**：`06fa23f`（分支 `preview/mbm-2026-09-review`；main 未動）
- **公開 Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026（HTTP 200）
- **封面圖直鏈（Preview）**：…/static/images/articles/reviews/mbm-casino-review-sep-2026-cover.png（HTTP 200）

## 封面處理（依本包指令）

1. 附件原圖 SHA-256 核對＝`cf9a4ac4c261bfe76c2b66914d4bee4c842695de15102cc000faeff5ba699b8b`（與指令記載一致），實測 1280×672 RGBA
2. **直接使用原圖，不縮放、不裁切、不補邊、不改字**；複製至本篇專用路徑 `mbm-casino-review-sep-2026-cover.png`（覆蓋前版 1280×800 輸出檔；舊 5 月封面圖檔仍未動、未引用）
3. 內容目視：「MBM 娛樂城／2026年9月評價：玩家最新心得與出金回饋」，四標籤為**出金快速／遊戲多元／安全可靠／玩家好評**，右下「真實玩家分享 帶你看見更完整的MBM!」；無月份錯誤、無評分或成功率數字
4. HTML：正文 img `width="1280" height="672"`、`fetchpriority="high"` 無 lazy、描述性 alt；og:image／twitter:image／Article.image 三處同圖絕對 URL（fun1399.com）
5. dateModified／可見更新日改為實際修改日 `2026-09-23T09:35:00+08:00`／2026年9月23日

## 驗證（Playwright 320/375/390/430/1440，五寬度結果一致）

- 頁面 200、封面圖 200，伺服器端實測 1280×672
- 封面實載 naturalWidth=1280、naturalHeight=672；四處引用一致
- 三張回饋圖皆實載；FAQ 3 題逐字一致（mm=0）；H1=1；無橫向溢位
- JSON-LD：Article＋BreadcrumbList＋FAQPage；無 Review/Rating/Product
- 封面在手機/桌面構圖清晰、文字可讀、無裁切

## 未確認項目（含本包特別指示）

1. **封面圖文案「出金快速／安全可靠／玩家好評」屬圖片內容，現有附件不足以獨立證明**——依指令未延伸為正文結論、評分、Review Schema 或安全保證；正文維持「無完整入帳紀錄、不能算出金速度、無法提供安全保證」的表述。Production 前依使用者證據或最終決定處理
2. 最低託售額度（不寫死）
3. GSC 無存取憑證 → 未查到
4. 三則對話皆無完整可核日期

## 聲明

- 草稿與證據圖與上一包逐位元相同，正文無需更動；本次僅替換封面資產與尺寸/日期
- 未動 main、未部署 Production、未提交 GSC、未改 Cloudflare／其他文章／共用樣式；舊封面圖檔保留未刪

## 待使用者

驗收本 Preview；如需正式發布請明確指示（Production 前請先決定封面文案之證據或接受現況）。
