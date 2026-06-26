# fun1399 GSC 曝光歸零深度排查報告

**日期：** 2026-06-26
**排查範圍：** fun1399.com 2026/5/25 - 2026/6/26 GSC 曝光異常
**排查人：** FUN1399 Bot
**限制：** 僅讀取型排查，未修改任何檔案

---

## 一、目前已排除的主因

| 項目 | 狀態 | 證據 |
|------|------|------|
| robots.txt 阻擋 | ✅ 排除 | 已簡化為乾淨版本，User-agent: * Allow: / |
| sitemap 缺失 | ✅ 排除 | 已補首頁 URL，109 頁 GSC 成功收錄 |
| 首頁 noindex | ✅ 排除 | 首頁無 noindex，canonical 正確 |
| 文章頁 noindex | ✅ 排除 | 抽查 10 篇皆無 noindex |
| canonical 錯誤 | ✅ 排除 | 抽查 10 篇皆指向自己 |
| HTTP 404/500 | ✅ 排除 | 抽查 10 篇皆 200，Googlebot 200 |
| URL duplicate (.html vs 無 .html) | ✅ 排除 | 19 個 slug 皆 .html 308 轉向無 .html，無 duplicate |
| 內鏈大量消失 | ✅ 排除 | 首頁維持 32 篇連結，/articles/ 列表從 78 增至 84 |
| 6/8 前曝光文章被移除 | ✅ 排除 | 移除的 6 篇首頁連結中，無 6/8 前主要曝光文章 |
| 單篇 schema 錯誤 | ✅ 排除 | 已修復 casino-scam-methods 和 gm1688，但這是局部問題 |

---

## 二、最可疑問題排序 TOP 5

### TOP 1: Google 演算法對娛樂城/賭博類內容的整體性調整

- **原因：** 6/8 是精確的時間分界點，非常像 Google 演算法更新（如 Helpful Content Update、Spam Update）
- **支持證據：**
  - 6/8 前 30 頁有曝光，6/8 後幾乎整批消失，只剩首頁和 /about
  - 這種「斷崖式」下降更符合演算法更新特徵
  - 娛樂城/賭博是 Google 明確標記的高風險 YMYL 類別
- **反證：** 無法直接確認 6/8 是否有 Google 演算法更新
- **建議修法：** 加強 E-E-A-T（經驗、專業、權威、信任），增加原創實測內容
- **風險等級：** 🔴 高（無法直接控制）

### TOP 2: 內容品質被判定為低品質或模板化

- **原因：** Google Helpful Content System 可能判定網站內容「由 AI 批量產生」「缺乏原創價值」
- **支持證據：**
  - 多篇 title 高度模板化（「2026最新」「完整攻略」「娛樂城」重複出現）
  - 多篇 description 結構相似（「2026最新...完整教學/攻略！...」）
  - 大量「評價」類文章可能只是換平台名稱，內容架構相同
  - 多篇 description 過短（39-44 字）
- **反證：** 6/8 前這些文章有曝光，代表 Google 之前沒有判定為低品質
- **建議修法：** 重寫 title/description，增加原創比較表、實測數據、獨特觀點
- **風險等級：** 🟡 中（可改善）

### TOP 3: 首頁內鏈替換導致 PageRank 重新分配

- **原因：** 97dca4b（6/9 15:36）移除了首頁 6 篇文章連結，替換為新文章
- **支持證據：**
  - 移除的文章包括 casino-experience-bonus-scam-2026（6/8 前有曝光的重要文章）
  - 雖然首頁總連結數不變，但 PageRank 分配改變
- **反證：** 移除的 6 篇文章中，僅 casino-experience-bonus-scam-2026 是較重要的，其他多為舊文章
- **建議修法：** 在首頁保留重要文章的連結，不要只放最新文章
- **風險等級：** 🟡 中（可修復）

### TOP 4: 網站被標記為 spam / 過度優化

- **原因：** 大量文章主題相似（娛樂城評價、詐騙、排名），內鏈錨文字可能過度優化
- **支持證據：**
  - 網站有 90+ 篇 articles，大量為「評價」「詐騙」「排名」類
  - 這類內容容易觸發 Google 的 spam 檢測
- **反證：** 6/8 前正常曝光，未被封鎖
- **建議修法：** 減少同質化文章，增加教學/攻略類多樣內容
- **風險等級：** 🟡 中（需長期調整）

### TOP 5: JSON-LD 結構化資料大規模錯誤

- **原因：** 34 抽樣中發現 3 個 JSON-LD 錯誤（約 9%），推估全站 8-10 篇有問題
- **支持證據：**
  - casino-black-site-methods 重複 image
  - how-to-check-casino-scam-record 重複 image + 相對 URL
  - hg-casino-promotions-may-2026 JSON parse 錯誤
- **反證：** 結構化資料錯誤通常不影響索引，只影響 Rich Snippet
- **建議修法：** 批次修復全站 JSON-LD 錯誤
- **風險等級：** 🟢 低（不直接影響索引）

---

## 三、最可疑 commit

| commit | 時間 | 修改檔案 | 影響範圍 | 可疑程度 | 理由 |
|--------|------|----------|---------|---------|------|
| 97dca4b | 6/9 15:36 | index.html, articles/index.html, swag-casino-scam-discussion.html | 首頁 7 篇文章替換 | **🔴 高** | 移除 6 篇首頁連結，包括 casino-experience-bonus-scam-2026；雖然不是主因，但時間點最接近 6/8 |
| d508f23 | 6/9 17:13 | swag-casino-scam-discussion.html | 單篇文章重寫 | 🟡 中 | 改變文章模板結構，但只影響一篇 |
| d5efc44 | 6/9 17:24 | scripts/validate_article.py | 無 | 🟢 低 | 未改網站內容 |

**結論：** 97dca4b 是時間點最接近 6/8 的 commit，但技術上無法證明它導致整批曝光歸零。

---

## 四、低風險可立即修復項目

| 項目 | 原因 | 修法 |
|------|------|------|
| 修復 5 篇孤兒頁 | sitemap 有但列表/首頁無內鏈 | 在 articles/index 和首頁添加連結 |
| 補 sitemap 缺失 | swag-casino-scam-discussion 不在 sitemap | 添加 URL 到 sitemap.xml |
| 修復 JSON-LD 錯誤 | 3 篇有 parse 錯誤或重複 image | 逐篇修復（參考 casino-scam-methods 修復方式） |
| 補 description | 2 篇 description 過短 | 擴充到 120-160 字 |
| 減少 title 模板化 | 2 篇 title 高度模板化 | 改寫為更獨特的標題 |

---

## 五、中風險需 Preview 項目

| 項目 | 原因 | 修法 |
|------|------|------|
| 首頁內鏈策略調整 | 目前只放最新文章，重要文章可能被移除 | 設計「常駐文章」區塊，保留高曝光文章連結 |
| 文章模板優化 | 新模板可能存在過度 SEO 風險 | 審查 gm1688 模板，減少固定詞組和 CTA 重複 |
| 內容多樣化 | 大量文章為評價/詐騙/排名類 | 增加教學、攻略、新聞類多樣內容 |

---

## 六、高風險需人工確認項目

| 項目 | 原因 | 確認方式 |
|------|------|---------|
| 是否繼續做娛樂城內容 | Google 可能對此類內容持續降權 | 觀察 1-2 週，若無回升需考慮轉型 |
| 大量文章重寫 | 模板化內容可能需全面重寫 | 逐篇審查，優先重寫 6/8 前有曝光的文章 |
| 域名/品牌策略 | 長期來看，fun1399 是否適合做內容站 | 評估是否需獨立內容子域名 |

---

## 七、是否建議 rollback

### 1. 是否建議 rollback？
**不建議。**

### 2. 如果建議，應 rollback 到哪個 commit？
不建議 rollback，但如果強制測試：
- 目標 commit：`cbbb04d`（6/7 前最後正常版本）
- 必須先建立 Preview 測試，不可直接 rollback Production

### 3. 如果不建議，原因是什麼？

**原因一：無明確技術錯誤可 rollback 修復**
已排查確認：robots、sitemap、noindex、canonical、404、duplicate URL、內鏈結構皆正常。rollback 無法修復「演算法調整」或「內容品質判定」問題。

**原因二：97dca4b 的影響範圍不足以解釋整批消失**
- 97dca4b 移除的 6 篇首頁連結中，僅 casino-experience-bonus-scam-2026 是較重要的文章
- 其他 5 篇（3a-casino-investigation-may-2026、biwin-casino-scam-review、casino-scam-prevention-checklist、casino-scam-update-may-2026、dragon-boat-casino-scam-alert-jun-2026）多為舊文章或季節性內容
- 6/8 前主要曝光文章（3a-casino-scam-review、casino-registration-guide、casino-bonus-guide、gm1688-casino-scam-review、free-credit-guide 等）**皆不在移除名單中**
- 若 97dca4b 是主因，應只看到「被移除的 6 篇文章」失去曝光，而非「整批 30 篇文章」消失

**原因三：rollback 的副作用**
- rollback 會移除 6/9 後新增的所有文章（SWAG、皇家不出金、黑網解析、排名、推薦、高風險觀察等）
- 這些新文章可能已獲得部分內鏈和曝光，rollback 會造成二次傷害
- 6/9 後的修復（sitemap 補首頁、robots 簡化、JSON-LD 修復）也會被 rollback 還原

**原因四：時間點不符**
- 97dca4b 是 6/9 15:36，而曝光歸零是 6/8 開始
- 雖然時區可能導致 1 天差異，但 GSC 數據顯示 6/8 當天已無曝光
- 若 97dca4b 是原因，應該是 6/9 後才出現問題，而非 6/8

### 4. 97dca4b 是否需要 rollback？
**不需要。**
- 97dca4b 只改了一篇文章的 Featured 位置和 6 篇一般卡片的替換
- 這類首頁內容更新是正常操作，不應導致整批曝光歸零
- 即使 rollback，也不會恢復 6/8 前失去的曝光

### 5. d508f23 是否需要 rollback？
**不需要。**
- d508f23 只修改 swag-casino-scam-discussion.html 單篇文章
- 這是一篇新文章，6/8 前不存在，不可能是 6/8 曝光歸零的原因

### 6. d5efc44 是否需要 rollback？
**不需要。**
- d5efc44 只新增 scripts/validate_article.py 和修改 scripts/auto-draft-trigger.sh
- 未修改任何網站檔案，完全不影響 Production

### 7. 如果不 rollback，應該優先修哪些項目？

**第一優先（低風險，可立即修）：**
1. 修復 5 篇孤兒頁（sitemap 有但列表/首頁無內鏈）
2. 補 sitemap 缺失（swag-casino-scam-discussion 不在 sitemap）
3. 修復 3 篇 JSON-LD 錯誤（casino-black-site-methods、how-to-check-casino-scam-record、hg-casino-promotions-may-2026）
4. 擴充 2 篇 description 過短文章

**第二優先（中風險，需 Preview）：**
5. 調整首頁「最新攻略文章」策略：保留高曝光文章連結，設計「常駐文章」區塊
6. 重寫 2 篇 title 模板化文章
7. 審查 gm1688 模板，減少固定詞組和 CTA 重複

**第三優先（高風險，需人工確認）：**
8. 觀察 1-2 週 GSC 數據變化
9. 若無回升，考慮內容策略調整（減少評價類，增加教學/攻略類多樣內容）
10. 評估是否需要獨立內容子域名或品牌轉型

### 8. 哪些修復屬於低風險？
- 修復孤兒頁（添加內鏈）
- 補 sitemap
- 修復 JSON-LD 錯誤（單篇修復）
- 擴充 description
- 更新 meta update 日期

### 9. 哪些修復需要 Preview？
- 首頁內鏈策略調整（改變 Featured + 6 卡片結構）
- 重寫 title（可能影響排名）
- 修改文章模板（影響所有新文章）
- 批量修復 JSON-LD（多篇文章同時修改）

### 10. 哪些修復需要人工確認？
- 內容策略轉型（減少評價類，增加教學類）
- 是否繼續做娛樂城內容（若 Google 持續降權）
- 域名/品牌策略調整
- 大量文章重寫（成本評估）
- 是否投資付費 SEO 工具或顧問

### 結論
不建議 rollback。技術層面已排除所有明確錯誤，曝光歸零最可能是 Google 演算法對娛樂城/賭博類內容的調整，或內容品質被判定為低品質。rollback 無法解決這些問題，反而會移除 6/9 後的新文章和修復。

建議明天先執行低風險修復（孤兒頁、sitemap、JSON-LD），觀察 1-2 週 GSC 數據變化，再決定是否需要內容策略調整。

---

## 八、優先修復建議（明天執行）

### 第一優先（低風險，可立即修）
1. 修復 5 篇孤兒頁：在 articles/index 添加連結
2. 補 sitemap：添加 swag-casino-scam-discussion
3. 修復 3 篇 JSON-LD 錯誤（casino-black-site-methods, how-to-check-casino-scam-record, hg-casino-promotions-may-2026）

### 第二優先（中風險，需 Preview）
4. 調整首頁「最新攻略文章」策略：保留高曝光文章連結
5. 重寫 2 篇 title 模板化文章
6. 擴充 2 篇 description 過短文章

### 第三優先（高風險，需人工確認）
7. 觀察 1-2 週 GSC 數據變化
8. 若無回升，考慮內容策略調整（減少評價類，增加教學類）

---

## 九、排查方法論說明

本次排查遵循「由外到內、由技術到內容」的順序：
1. 先排除最明顯的技術問題（robots、sitemap、noindex、404）
2. 檢查 URL 結構和 canonical
3. 檢查內鏈結構和孤兒頁
4. 檢查 commit 差異
5. 檢查 JSON-LD 結構化資料
6. 最後檢查內容品質

結論：技術層面已排除所有明顯問題，最可能原因是 Google 演算法對娛樂城/賭博類內容的調整，或內容品質被判定為低品質。

---

*報告產出時間：2026-06-26*
*檔案名稱：fun1399-gsc-drop-investigation-2026-06-26.md*
