# P3 MBM 2026年9月評價（may-2026 篇）V3 PREVIEW REPORT

- **日期**：2026-09-22
- **基準 Commit（重新核對）**：`bf946077e6689729d396df124fbfc7a10bf08f67`（origin/main 未變；正式頁 HTTP 200 且與 repo 基準檔一致）
- **交付 Commit**：`2ab0679`（分支 `preview/mbm-2026-09-review`；v3 內容自 `preview/mbm-2026-09-review-v3` 的 `5a8bb1f` 移植——該分支 Pages 預覽建置逾 25 分鐘未生效（404），為交付公開預覽改推至可運作之預覽分支，main 全程未動）
- **公開 Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026（HTTP 200，實測為 V3 內容）

## V3 相對 V1 的主要變更（依 CHANGELOG_V3）

| 項目 | V1 | V3（現行） |
|---|---|---|
| Title/H1 | 匿名回饋與出金規則 | 玩家最新心得與出金回饋（沿用原題，月份 5→9） |
| 開頭 | 「先說結論」查核框 | 兩段讀者提問，無聲明框 |
| 主軸 | 出金規則教學式 | 優惠→概況→出金→返水→心得→比較→優缺點→總結（原閱讀順序） |
| 目錄/延伸閱讀/防詐提醒 | 有 | 保留並更新指向 |
| 會員轉移、老會員回歸 | 無 | 依平台活動頁補回（今日已重新核實） |
| 鉅城/HG 比較 | 無 | 保留比較問題＋站內延伸閱讀，無速度排名/星等 |
| FAQ | 4 題 | 3 題（首存流水／0.8% 返水／每日託售次數） |

## Title / Description / H1 / Canonical / 日期

- Title：`MBM娛樂城2026年9月評價：玩家最新心得與出金回饋 - 娛樂城玩家俱樂部`
- Description：`MBM娛樂城2026年9月評價：整理首儲、返水與託售條件，看看一則匿名玩家怎麼說出金；台幣、USDT 的活動流水有何不同？`
- H1 全頁 1 個，與 Title 一致；OG/Article headline 同步
- Canonical：`https://fun1399.com/articles/mbm-casino-review-may-2026`（無 .html）；mainEntityOfPage 已修正一致
- datePublished `2026-05-20T10:00:00+08:00` 保留；dateModified/可見更新 `2026-09-22T15:55:00+08:00` / `2026年9月22日`
- 作者 Kevin Lin（無資歷宣稱；https://fun1399.com/author HTTP 200）

## 平台條款重新驗證（2026-09-22 下午，唯讀渲染頁面）

| 條款 | 結果 |
|---|---|
| 首存 1,000 送 1,000：台幣（本金+贈金）×1、USDT ×10、先儲值後投注前向客服申請 | ✅ 活動頁確認 |
| 9 月儲值加碼 9/1–9/30、門檻 2,000、3%～10%、週一~四 ×8／週五~日 ×10 | ✅ 活動頁確認 |
| 王者回歸：VIP2 以上、超過一個月無有效投注、8%～15%、贈金上限 3,000、（本金+回饋）×10、僅一次 | ✅ 活動頁確認 |
| 會員轉移：原平台儲值額對應 VIP2–VIP6、需提供原平台會員資料、暫定永久 | ✅ 活動頁確認 |
| VIP 返水：電子/真人百家 VIP1 0.4%→VIP6 0.8%（0.4/0.4/0.5/0.6/0.7/0.8）、體育均 0.8%、當日託售額度各級 100 萬 | ✅ 活動頁 VIP 表確認 |
| 託售：每日一次、單筆上限 100 萬點、首次綁定審核、同名收款、一般儲值 ×1 有效投注 | ✅ 託售教學頁確認 |
| 最低託售 1,000 點 | ⚠️ 今日公開頁仍查不到 → 已依規則自出金表移除數字，改寫「最低額度以平台當下託售頁面為準」 |

## 驗證（Playwright，320/375/390/430/1440 五寬度實測公開 Preview）

- JSON-LD 可解析：Article＋BreadcrumbList＋FAQPage；無 Review/Rating/Product
- FAQ 可見 3 題與 JSON-LD 逐字一致（mm=0）
- H1=1；H2 依序：promotions / overview / withdrawal / rebate / feedback / compare / pros-cons / conclusion / faq
- 五寬度無橫向溢位；兩張表格皆容器內捲動；圖片含 width/height/alt/lazy，實載正常
- 禁用語全文搜尋（含可見文字）：2分鐘、兩分鐘、1分54秒、4.7、85%、1688、30秒客服、每日2次、無門檻0.8%、先說結論、原文曾、這版先不放、依本次查核、能核對的是、資深娛樂城分析師、最低 1,000 點 → **0 命中**
- 三處 MBM 商業外連均 `rel="sponsored nofollow noopener noreferrer"`
- 封面：顯示與 og:image/twitter:image/Article.image 引用全數移除，原圖檔未動

## 未確認項目

1. 最低託售額度（已移除數字，列未確認）
2. GSC 無存取憑證 → 未查到（不阻擋 Preview）
3. 新封面 1280×800 待使用者提供

## 聲明

- 未動 main、未做 Production 部署、未提交 GSC、未更動 Cloudflare/DNS/其他文章/全站樣式
- `_1`、`_2` 包與原始包逐位元相同（已另行回報）；本版依 `v3` 包（ARTICLE_DRAFT_V3）交付
