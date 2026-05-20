# MEMORY.md - 長期記憶

## 用戶偏好設定

### SEO 預設配置
- **目標市場**：台灣
- **語言**：繁體中文
- **地區代碼**：TW
- **搜尋引擎**：Google Taiwan (google.com.tw)

### 執行準則
當用戶要求 SEO 相關任務時，自動應用以下設定：
1. 關鍵字研究 → 繁體中文關鍵字
2. 內容生成 → 繁體中文撰寫
3. 網站架構 → 台灣使用者習慣
4. 競爭分析 → 台灣競爭對手
5. 搜尋意圖 → 台灣使用者行為

### 產業背景
- 主要領域：線上娛樂城/博弈資訊
- 內容類型：評測、攻略、優惠整理
- 變現模式：聯盟行銷

## 部署規則（2026-05-18 確立）
- **Preview-only → 等待 Hans 確認 → Production deploy**
- 未經 Hans 明確確認，禁止 production deploy
- 所有 deploy 必須先建立 Preview，驗證通過後才正式上線

## 最近 Production Deploy
- Deploy ID: 6a0b1a566bf6a10b5a511156
- URL: https://fun1399.com
- 日期：2026-05-18
- 內容：SEO 修正（orphan links, canonical, OG URL, World Cup internal linking）

## GSC 分析結果（2026-05-18）
- Sitemap 總 URL: 89
- 已索引（有曝光）: 25（28%）
- 未索引/無曝光: 68
- 優先提交頁面：world-cup-2026-guide, usdt-casino-scam-2026, casino-agent-scam-2026, world-cup-betting-tips, jucity-casino-review-may-2026
- Orphan pages 已修復內鏈
- 5 個 orphan pages：world-cup-live-betting, world-cup-betting-tips, utown-casino-scam-review, cashback-guide, casino-agent-guide

## 未來項目規劃（待執行）

### 🚀 第二網站策略：單頁深度優化（Single Product Landing Page）

**背景**：
分析同行（qttheluxe.com, qttowerrush.com, inoutchickenroad2.com, pandasportsevents.com, dglivevideo.com）發現他們採用「單一產品深度優化」策略，與fun1399的「大量文章覆蓋」策略形成互補。

**策略對比**：
| 維度 | 單頁深度優化 | 大量文章覆蓋（fun1399） |
|------|--------------|------------------------|
| SEO目標 | 品牌詞/產品名稱排名 | 長尾關鍵字資訊型排名 |
| 流量特性 | 精準高轉化 | 廣泛低轉化 |
| 內容成本 | 低（1-5頁） | 高（60+文章持續更新） |
| 見效時間 | 快（2-4週） | 慢（2-4月） |
| 維護成本 | 低 | 高 |

**適用時機**：
當用戶問「有什麼項目可以做」時，提出此策略。

**執行時機建議**：
- fun1399達穩定流量（日均300+ UV）後
- 找到高轉化產品/遊戲時
- 預算允許多站點運營時

**執行步驟**：
1. 選擇產品（如：特定老虎機/體育品牌）
2. 註冊含關鍵詞域名（如：mbmgame.com, 3acasino.tw）
3. 設計高轉化單頁（Hero區+特色+FAQ+CTA）
4. 優化品牌詞SEO
5. 投放精準廣告導流

---

## 從同行學習的優化元素（應用於fun1399）

### 1. 著陸頁轉化優化
- ✅ **Hero區域**：大標題+副標+立即行動按鈕
- ✅ **社交證明**：實時玩家數、獲獎排行榜、獎金金額
- ✅ **特色卡片**：圖標+標題+簡短說明（3-4個特色）
- ✅ **FAQ摺疊**：直接解答用戶疑慮
- ✅ **多CTA分佈**：頁面各處都有行動按鈕

### 2. 文章頁可借鑑元素
- **即時數據展示**：「目前有XXX位玩家在線」
- **浮動/固定CTA**：側邊欄或底部固定導流按鈕
- **視覺化特色**：用圖標代替純文字列表
- **簡潔FAQ**：摺疊式常見問題，提升頁面互動

### 3. 域名策略（未來參考）
- 同行使用 `品牌名+產品名` 組合域名
- 如：qt + theluxe, qt + towerrush
- 可考慮為高價值產品註冊獨立域名

---

*最後更新：2026年5月18日*

## ✅ Cloudflare Pages 遷移完成（2026-05-20）

### 遷移時間軸
- GitHub Repo 建立：2026-05-20 17:21
- Git push 完成：2026-05-20 17:26
- Cloudflare Pages 部署：2026-05-20 17:33
- DNS NS 切換：~18:00
- Production Audit 完成：18:45

### 新架構
| 層級 | 服務 | 功能 |
|------|------|------|
| 版控 | GitHub (apaoer23-netizen/fun1399-site) | main branch auto-deploy |
| Hosting | Cloudflare Pages | CDN + SSL + 全球節點 |
| DNS | Cloudflare NS | NS 管理 + CNAME flattening |
| Domain | fun1399.com | apex domain + www redirect |

### 遷移前準備
- 完整備份（source/Netlify config/SEO/deploy log）
- Git init + .gitignore（排除 .netlify/ netlify.toml *.bak）
- 清理 .bak 檔案（5 個已移除）
- 敏感資訊掃描（無 API key/token 外洩）

### 遷移後修復
- og-image.jpg（1280×673）上傳到 static/images/
- 404.html 建立（修復 Soft 404）
- www → apex 301 redirect

### 觀察期（2026-05-20 ~ 05-22）
- 穩定優先，不大幅修改設定
- 每次 git push 驗證 deploy
- 監控 GSC 抓取狀態
- 暫不加 CSP / HSTS preload
- 可選加 X-Content-Type-Options + X-Frame-Options

### 報告檔案
- `CLOUDFLARE-PRODUCTION-AUDIT.md`
- `backups/MIGRATION-PLAN-2026-05-20.md`
- `backups/CLOUDFLARE-SEO-DIFF-2026-05-20.md`

---

*最後更新：2026年5月20日*

## SEO Workflow（2026-05-20 建立）
- **技能啟用**: seo-audit, internal-linker, google-search-console, ai-seo
- **Deploy 後**: deploy-seo-checklist.md（12 項檢查）
- **每週**: weekly-seo-checklist.md（GSC + AI + 內鏈）
- **Redirect**: redirect-verification-checklist.md（8 項驗證）
- **遷移**: cloudflare-migration-seo-checklist.md（9 項驗證）
- **補強評估**: #1 Custom Crawler → #2 Link Graph → #3 Lighthouse CI
- **原則**: 穩定 > 擴張，Technical SEO > Content Volume
