# SEO 維護與發布驗收

本文件新增可重複執行的技術檢查，不代表已部署、Google 已收錄或成效已提升。

## 本機檢查

在儲存庫根目錄執行：

```sh
python3 scripts/sync_sitemap.py
python3 scripts/check_seo.py
git diff --check
```

`sync_sitemap.py` 預設只檢查，有待同步項目時以非零狀態結束。確認文章原有日期可保留後，再執行 `python3 scripts/sync_sitemap.py --write`。它沿用內容中已宣告的實質更新日期，不以檔案修改時間或今日日期全面刷新。

`check_seo.py` 檢查主站 HTML 的 H1、description、canonical 數量、JSON-LD 語法與本站圖片／logo 引用、站內目標與錨點、引用資產、指定推薦網域的連結關係標示，以及 sitemap 重複與 noindex。它允許 404 頁保留 noindex，排除原型區、測試頁與驗證檔，另確認測試頁維持 noindex。

這些檢查無法取代來源查核、完整結構化資料資格測試或瀏覽器驗收。未命中錯誤不代表頁面內容真實、所有商業關係已辨識，或未經同意的新測試檔可直接加入正式輸出。

## 發布前人工確認

- 數字、案例、評分及引用有可追溯資料；否則移除或清楚標示限制。
- 頁面標題、摘要、正文、FAQ 與 JSON-LD 結論一致。
- 桌面與手機檢查文章、表格、按鈕、選單及圖片。
- 核對待發布 branch、commit 與已接受內容，不能直接覆蓋其他預覽文章。

## 發布後確認

核對 Cloudflare Production 的 branch、commit SHA 與輸出目錄。抽查線上 HTML 與 HTTP headers，確認目標頁 200、索引指令、canonical、301／404 及素材載入，再用 Search Console URL 檢查驗證。只有本機結果不能回報正式站修復成功。

## 成效追蹤

使用 GSC 的查詢、頁面、日期、裝置、國家資料衡量非品牌曝光與點擊；使用 GA4 驗證自然搜尋進站的有效事件。缺資料時不推估排名提升比例、不保證收錄時間。FAQ、Schema、字數與 CTA 的數量不作為 SEO 成效門檻。
