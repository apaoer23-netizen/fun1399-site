# P3 MBM 2026年9月評價｜匿名對話擴充版（三圖）完成報告（Preview Only）

- **日期**：2026-09-22
- **基準（親自重新核對）**：origin/main＝`bf946077e6689729d396df124fbfc7a10bf08f67` 未變；正式頁 HTTP 200 與 repo 一致
- **交付 Commit**：`f177caf`（三圖擴充＋文案）＋`b9909bb`（FAQ JSON-LD 逐字修正）；分支 `preview/mbm-2026-09-review`；main 未動
- **公開 Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026（HTTP 200）

## 本包變更（`_1` 包：取代先前各版）

1. **玩家心得段改三圖結構**（依更新後 ARTICLE_DRAFT_V4）：
   - 截圖一｜出金體感：`anonymous-feedback-2.webp`（原對話組資訊較完整者，依指令僅展示此張）
   - 截圖二｜出金與客服感受：新增 `anonymous-feedback-3.webp`（592×1280，「你們MBM出金好快」「客服小姐姐服務態度很好」，含「來到MBM還沒輸過」個人說法）
   - 截圖三｜賽特遊戲畫面：新增 `anonymous-feedback-4.webp`（592×1280，「我今天打賽特一直贏」＋兩張遊戲獎金畫面）
   - 每圖上方有可見來源與限制圖說（依草稿逐字）；三段引導文字依草稿落稿
2. **遮蔽檢查**：四張原始截圖頭像、聊天對象名稱皆已像素遮蔽，無可辨識個資；新圖無需再加工，原圖未動
3. **文案同步**（依草稿）：開場看法段、概況表「玩家回饋」列、優缺點段、總結段（新增「遊戲畫面也不能證明長期勝率」）、FAQ 3 答案（可見與 JSON-LD 已逐字一致）
4. **Description 更新**：`MBM娛樂城2026年9月評價：首儲、返水與出金值得注意什麼？看使用者提供的匿名對話與遊戲畫面，整理台幣、USDT活動條件及MBM的優缺點。`（meta/OG/Article 同步）
5. **H2 改標**：「玩家最新心得：匿名對話怎麼看？」（目錄同步）
6. **dateModified** `2026-09-22T17:50:00+08:00`；封面四處引用維持 1280×800 新圖不變
7. 新圖 webp q90（53,000B／69,314B）；width/height/描述性 alt/lazy 齊全
8. 舊 `anonymous-feedback-1.webp` 仍存 repo 但本篇已不引用

## 驗證（Playwright 320/375/390/430/1440，滾動載入後五寬度結果一致）

- 頁面 200；四張頁面圖片（封面＋回饋 2/3/4）皆 HTTP 200 且實載成功
- 三張回饋圖：寬度屬性正確（590/592/592×1280）、lazy、遮蔽完整、圖說緊貼圖片
- 封面 naturalWidth=1280；無 lazy；og/twitter/Article image 一致
- FAQ 3 題逐字一致（mm=0）；H1=1；無橫向溢位；手機單欄圖片未撐破文章寬
- JSON-LD：Article＋BreadcrumbList＋FAQPage；無 Review/Rating/Product

## 邊界落實

- 未以「來到MBM還沒輸過」暗示勝率；未以遊戲獎金數字作實得／提款證據；未稱 PTT/Dcard 趨勢；綠色客服回覆未作玩家證言；三圖未稱三位不同玩家
- 未加入任何 AI 生成示意圖作為真實回饋
- 未動 main、未部署 Production、未提交 GSC、未改 Cloudflare／其他文章／共用樣式

## 未確認項目

1. 最低託售額度（不寫死）
2. GSC 無存取憑證 → 未查到
3. 三則對話皆無完整可核日期

## 待使用者

驗收本 Preview；如需正式發布請明確指示。
