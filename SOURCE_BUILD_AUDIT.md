# Source 與 Build 檔案對照檢查

## 問題發現
Build 目錄中有以下檔案在 Source 中找不到對應：
- casino-no-withdrawal-scam.html
- casino-registration-guide.html
- hg-casino-review.html（build 在 articles/，source 在 reviews/hg.html）

## 處理方案
1. 對於 source 存在的檔案：直接修改 source
2. 對於 build 獨有的檔案：需要建立 source 版本或確認生成方式
3. 重新 build 後驗證

## 已修改 Source 檔案
- ✅ fun1399-fixed/articles/free-credit-guide.html（Title 重寫）
- ✅ fun1399-fixed/articles/baccarat-guide.html（Title 重寫）

## 待處理
- [ ] casino-no-withdrawal-scam.html（無 source，需確認）
- [ ] casino-registration-guide.html（無 source，需確認）
- [ ] reviews/hg.html（需新增3專區）
- [ ] reviews/mbm.html（需新增內鏈）
- [ ] reviews/gm1688.html（需新增內鏈）
- [ ] reviews/utown.html（需新增內鏈）
- [ ] articles/deposit-guide.html（需新增內鏈）
- [ ] articles/fast-withdrawal.html（需新增內鏈）
