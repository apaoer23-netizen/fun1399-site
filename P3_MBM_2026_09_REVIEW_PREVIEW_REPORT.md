# P3 MBM 2026年9月評價（may-2026 文章）PREVIEW REPORT

- **日期**：2026-09-22
- **基準 Commit**：`bf946077e6689729d396df124fbfc7a10bf08f67`（origin/main，已重新核對）
- **新 Commit**：`aecede0`（分支 `preview/mbm-2026-09-review`）
- **Preview URL**：https://preview-mbm-2026-09-review.fun1399-site.pages.dev/articles/mbm-casino-review-may-2026
- **Production 基準查核**：正式頁 HTTP 200，HTML 與本地基準檔位元一致（sha1 相同）

## 變更檔案清單

| 檔案 | 變更 |
|---|---|
| `articles/mbm-casino-review-may-2026.html` | 全文改寫（第一版） |
| `static/images/articles/reviews/mbm-anonymous-feedback-1.webp` | 新增（54,556B，590×1280，q90） |
| `static/images/articles/reviews/mbm-anonymous-feedback-2.webp` | 新增（54,328B，590×1280，q90） |

## Title / Description / H1 / Canonical

| 項目 | 內容 |
|---|---|
| Title | `MBM娛樂城2026年9月評價：匿名回饋與出金規則 - 娛樂城玩家俱樂部` |
| Description | `整理 MBM 娛樂城 2026 年 9 月的首儲優惠、返水級距與提款規則，並說明一則匿名回饋能證明什麼、不能證明什麼。優惠條件以平台當下公告為準。` |
| H1（全頁 1 個） | `MBM娛樂城2026年9月評價：匿名回饋與出金規則` |
| Canonical | `https://fun1399.com/articles/mbm-casino-review-may-2026`（無 .html，維持原路徑） |
| mainEntityOfPage | 已修正為無 `.html` 的 canonical |
| datePublished | `2026-05-20T10:00:00+08:00`（保留） |
| dateModified / 最後更新 | `2026-09-22T14:40:00+08:00` / `2026年9月22日`（實際修改日） |
| 作者 | Kevin Lin（可見與 Article.author 一致；已移除「資深娛樂城分析師」資歷宣稱；作者連結 https://fun1399.com/author HTTP 200） |

## JSON-LD 驗證（Playwright，320/375/390/430/1440 五寬度）

- 圖型：`Article` + `BreadcrumbList` + `FAQPage`（可解析）
- Review / Rating 結構：已完全刪除
- FAQ 可見 4 題與 JSON-LD 逐字一致（mm=0）
- 五寬度 H1 數量 = 1、無整頁橫向溢位

## 無證據宣稱清理清單（全文搜尋含 Title/Description/OG/表格/CTA/alt/JSON-LD）

| 項目 | 狀態 |
|---|---|
| 2分鐘/兩分鐘/極速出金、平均1分54秒、5筆精確到秒提款表 | 已刪除 |
| 每日前2次免手續費、30秒客服、返水自動入帳實測 | 已刪除 |
| 無門檻0.8%、4.7/5、85%成功率、星級表格 | 已刪除（含 Review schema） |
| 雙幣加碼日、回歸送1688、轉移專屬優惠 | 已刪除 |
| PTT/Dcard 五則無連結引言、虛構帳號 | 已刪除 |
| 跨平台比較（鉅城、HG 誰更快） | 已刪除 |
| 封面引用（og:image / twitter:image / Article.image / 可見 cover） | 已全部移除（原圖檔保留未動） |

## 平台條款重新驗證（2026-09-22，唯讀）

| 條款 | 重新查核結果 |
|---|---|
| 首存 1,000 送 1,000：台幣（本金+贈金）×1、USDT ×10 | ✅ 活動頁實際載入確認 |
| 9月儲值加碼 9/1–9/30、門檻 2,000、3%–10%、週一~四 ×8、週五~日 ×10 | ✅ 活動頁實際載入確認（週五~日最高檔 10%） |
| 每日託售 1 次、單筆上限 100 萬點、免手續費 | ✅ 託售教學頁確認 |
| 首次託售需客服綁定審核、收款姓名須與註冊一致、一般儲值 1 倍有效投注 | ✅ 託售教學頁確認 |
| 電子/真人百家樂返水 VIP1-2 0.4%→VIP6 0.8%、體育 0.8% | ⚠️ 今日 /vip 路由未載入表格；依 2026-09-22 查核資訊與本站已發布同系列文章一致，標為平台公布規則 |
| 最低託售 1,000 點 | ⚠️ 今日公開頁重新查不到（SPA/需登入）→ 已從正文與 FAQ 移除該數字，改寫為「最低額度依平台當下託售頁面為準」 |

## 匿名回饋圖片

- 兩張截圖頭像、名稱、帳號均已馬賽克遮蔽（人工檢視確認）→ 可展示
- 圖說逐字：`使用者提供的匿名回饋（對話日期未確認）`
- 未計算速度、未納入對話方回覆與「比 R 平台好」比較

## 版面驗收

| 寬度 | 結果 |
|---|---|
| 320 | 無橫向溢位、表格容器內捲動 ✅ |
| 375 | 同上 ✅ |
| 390 | 同上 ✅（表格截圖存證） |
| 430 | 同上 ✅ |
| 1440 | 同上 ✅ |

## 未確認項目

1. 最低託售額度（今日重新查不到，已移除數字）
2. VIP 返水級距今日未能從公開路由重新載入（依 9/22 查核資訊，發布前建議再核）
3. GSC：skill 存在但無存取憑證 → 未查到本篇查詢/索引資料（不阻擋 Preview）
4. 新封面：待使用者提供 1280×800 合規圖；本輪已完全移除舊封面顯示與 image metadata

## 聲明

- 本次僅建立 Preview，**未動 main、未做 Production 部署、未提交 GSC 索引**
- 未修改全站共用 CSS/JS、其他文章、Cloudflare/DNS 設定
- 舊封面檔 `mbm-casino-review-may-2026-cover.png` 保留於 repo 未刪除
