網站部署說明
===========

檔案結構
------
- index.html: 首頁
- articles/: 攻略文章（52篇）
- reviews/: 平台評測（7篇）
- static/: 資源檔案（CSS/圖片/JS）
- sitemap.xml: 站點地圖
- robots.txt: 搜尋引擎設定

部署方式
--------
1. 登入 Netlify (https://www.netlify.com)
2. 點擊 "Add new site" → "Deploy manually"
3. 將所有檔案拖拉到上傳區域
4. 等待部署完成
5. 設定自訂域名 fun1399.com

DNS設定
-------
將域名Nameservers改為：
  dns1.p01.nsone.net
  dns2.p01.nsone.net
  dns3.p01.nsone.net
  dns4.p01.nsone.net

或參考 DEPLOY-GUIDE.md 完整說明。

技術支援
--------
如有問題，請聯絡開發團隊。
