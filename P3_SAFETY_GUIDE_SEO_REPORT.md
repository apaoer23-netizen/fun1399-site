# P3 safety-guide｜SEO/AEO/GEO 優化完成報告（Preview Only）

- **日期**：2026-09-23
- **Repository Remote**：git@github.com:apaoer23-netizen/fun1399-site.git
- **分支**：`preview/safety-guide-seo`（新建，自 origin/main）
- **基準 Commit**：`bf94607`（origin/main，未動）
- **新 Commit**：`f564571`
- **修改檔案**：僅 `articles/safety-guide.html`
- **Preview URL**：https://preview-safety-guide-seo.fun1399-site.pages.dev/articles/safety-guide（HTTP 200）

## 三、Title／H1／Canonical
- Title 不變：娛樂城安全指南｜如何選擇安全平台與保護個人資料 - 娛樂城玩家俱樂部
- H1 不變（同上文不含站名）
- Canonical：https://fun1399.com/articles/safety-guide（無 UTM）

## 四、作者與日期
- 可見作者：Kevin Lin（連結 /author#kevin）；meta author、Article Schema author.name=Kevin Lin、author.url=https://fun1399.com/author#kevin
- 已清除 Jason Chen、/author.html#kevin、「博弈產業研究員／安全專家」職稱
- datePublished 2026-03-15、dateModified 2026-09-23（可見與 Schema 一致；visible 更新日 2026年9月23日）

## 五、Meta Description（統一於 meta/OG/Twitter/Article Schema）
- 前：「娛樂城安全完整指南！教你如何辨識安全平台…確保遊戲過程安心無慮。2026年最新安全攻略。」
- 後：「想知道娛樂城安全怎麼判斷？本文整理平台網址、海外執照、提款條件、個資與帳號安全檢查方法，並說明代操、假客服及無法出金時的處理步驟。」（無確保/安心無慮/保證出金等字）

## 六、開頭
- 前：籠統的「本文將從…教你如何辨識安全可靠的娛樂城…確保…安心。」
- 後：直接回答版（逐項核對＋保證獲利/代操帶牌/再繳一筆才提款→先停止交易再向165或警方查證）＋FUN1399 定位聲明（娛樂資訊與評測網站，不是娛樂城平台，不作合法/安全/必定出金保證）

## 七～十二、段落修改摘要
- 「如何選擇安全的娛樂城」→「娛樂城安全怎麼判斷？先核對這些地方」：首句直接回答；執照段删除「合法合規…以下認證」、改為官方名冊核對＋PAGCOR 冒用警示；HTTPS 段改為僅代表連線加密；新增平台規則（8 項查核＋口頭條款建議暫停付款）；評價客服段去除 24H=安全與秒數；小額測試段删除「1000-2000元」、改為可承受損失預算＋小額成功不保證未來
- 高風險表：改 4 欄（危險訊號／為什麼要注意／建議立即怎麼做／資料來源），8 項訊號，來源連 165/CIB/PAGCOR，無「百分之百詐騙」斷言
- KYC 段：删除一律遮蔽/一律浮水印/拒收浮水印=危險平台；改為書面規則為準、官方管道、不給私人帳號、不給密碼驗證碼、說明不了用途就暫停
- 資金段：删除贏利目標/達標收手/先提款後遊戲/定期提領；改為 5 項原則＋「前幾局的輸贏不能保證下一局結果；輸錢後加碼，不會讓損失自動回來」
- 密碼段：删除「每 3～6 個月定期更換」；改 NIST 方向 6 點並連官方來源

## 十三～十五、官方案例／處理步驟／法規
- 「官方案例常見的操作流程」區塊（CIB 來源＋「不是 FUN1399 自行統計」聲明，無 42%/多數案件）
- 受騙後 6 步驟 ordered list（止付、保存、銀行、165/報案、改密碼），加註「165 不代表一定能追回款項」
- 所在地法規提醒（刑法 266 條連法務部來源，不延伸法律結論）

## 八、GEO 查核表
- 「娛樂城安全資訊要怎麼查？」標準 <table>（thead/tbody/th/td），4 列：海外執照／HTTPS／提款與優惠規則／玩家評價，各列「怎麼核對／能確認什麼／不能證明什麼」；無 Table Schema

## 十六、FAQ
- 可見 FAQ 6 題（details/summary，與 JSON-LD 逐字 mm=0）：執照=安全？HTTPS=放心？KYC=詐騙？再繳稅金保證金？小額提款成功=長期安全？被騙先做什麼？每題首句直接回答
- FAQPage JSON-LD 可解析、無頁面外問答；不保證複合式結果顯示

## 十七、Article Schema
- @graph：Article＋BreadcrumbList＋FAQPage；headline=H1、description=新版 meta、image 絕對網址、author Kevin Lin(/author#kevin)、datePublished 2026-03-15、dateModified 2026-09-23T00:00:00+08:00、publisher Organization 娛樂城玩家俱樂部；無重複欄位/錯誤逗號；已清「5大指標、3步驟驗證法」

## 十八、來源連結
- 官方來源均 target=_blank rel="nofollow noopener noreferrer"（165、CIB、PAGCOR 警示/監管、MGA、Curaçao、NIST、法務部）；無商業連結故無 sponsored

## 十九、CTA 移除
- 已移除頁首「立即遊玩」「加入 LINE」、floating-cta.js 與 mobile-menu.js 引用（後者經查內含 ofa177/lin.ee 導流選單）；共用 JS 檔案本身未修改
- 殘留數：fun1399.ofa177.net＝0、lin.ee＝0、floating-cta.js＝0、立即遊玩＝0、專人服務＝0（原始碼與渲染文字雙查）

## 二十、延伸閱讀
- 保留兩篇：常見娛樂城詐騙手法整理（/articles/casino-scam-methods）、娛樂城安全檢查清單（/articles/casino-safety-check）；已刪 /articles/casino-safe 卡片

## 二十一、頁尾
- 「台灣最專業的娛樂城玩家互助平台」→「提供娛樂資訊、平台規則與風險整理」（僅本頁）

## 二十二、HTML 修復
- 已修「分開資金」<strong> 未閉合、<div class="final-tips" 缺 >；python html.parser 全文件檢查：無標籤錯誤、無未閉合；表格標準 HTML；五寬度容器內不超出文章寬度，手機可橫滑

## 二十三、文字風格
- 全篇「你」為主、先答後補、無排名無推薦清單；強宣稱掃描（台灣最專業/全台第一/絕對安全/安全可靠的平台/保證出金/永久安全/穩定獲利/必勝/穩賺不賠/一定能追回）僅存於否定或詐騙話術脈絡

## 二十四、驗收
- Preview 200；H1 未更換；Canonical 無 UTM；作者/日期可見與 Schema 一致；Article/Breadcrumb/FAQPage 解析正常；FAQ mm=0；HTML 標籤完整；桌機與手機表格正常；本頁無商業導流按鈕、無 floating 腳本；無 42% 等無來源統計；無「首次儲值控制在 1000～2000 元」；無固定週期換密碼；未把海外牌照寫成台灣合法或安全保證；未把 HTTPS 寫成安全證明；Production 未部署
- 五寬度（320/375/390/430/1440）核心結構一致；兩表格容器內可讀、手機橫滾未撐破
- 截圖：桌機首屏/GEO 表/FAQ、手機首屏/表/FAQ 共 6 張

## 揭露
- Hero 封面圖為既有素材，圖中文字（如「安全、公平、可靠」「安心娛樂有保障」）屬圖片內容，非本文文字，本輪未更換圖片；如需要可另案換圖
- 同目錄另有 casino-safe、casino-safety-check 等高度相似文章，依指示未修改

Production：未部署；GSC：未送出。
