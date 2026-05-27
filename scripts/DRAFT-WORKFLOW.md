# Fun1399 半自動發文流程 - 操作手冊

## 流程架構

```
[週一/三/五 9AM] ──→ [cron 觸發] ──→ [生成草稿到 build/]
                                              │
                                              ▼
                                    [發送 Telegram 通知給 Hans]
                                              │
                                              ▼
                                    [Hans 確認封面圖 + 內容]
                                              │
                                              ▼
                                    [AI 補上封面圖 + 最終檢查]
                                              │
                                              ▼
                                    [git commit + push main]
                                              │
                                              ▼
                                    [Cloudflare Pages auto deploy]
```

## 目錄規則

| 目錄 | 用途 | Deploy？ |
|------|------|----------|
| `build/articles/` | 草稿區，等 Hans 確認 | ❌ 否 |
| `articles/` (root) | 正式區，已確認文章 | ✅ 是 |
| `build/draft-generation.log` | 生成日誌 | ❌ 否 |

## Cron 設定

```
0 9 * * 1,3,5 /root/.openclaw/workspace/scripts/auto-draft-trigger.sh
```

- 執行日：週一、三、五
- 執行時間：上午 9:00 (Asia/Taipei)
- 觸發方式：執行 shell 腳本，透過 `openclaw agent` 觸發 AI 生成

## 禁止事項

❌ 自動 deploy 到 production
❌ 自動 push 到 GitHub main
❌ 使用 `fun1399/` 舊目錄
❌ Netlify deploy
❌ preview deploy 當正式成功
❌ 正式站 404 還回報成功

## 允許事項

✅ 生成草稿到 `build/articles/`
✅ 更新 `build/articles/index.html`
✅ 輸出封面圖需求規格
✅ 等 Hans 確認後手動 deploy
✅ 使用 `build/`、GitHub main、Cloudflare Pages

## 文章生成規範（v7）

1. **風險提醒語氣**：使用「部分玩家反映」「網路討論指出」
2. **非武斷定罪**：避免「黑網」「詐騙確定」等詞
3. **免責聲明**：文末標註「僅供參考，不代表官方立場」
4. **CTA 導向**：引導至安全平台（鉅城、MBM 等）
5. **差異化**：與現有品牌查證文保持不同角度

## 確認清單（Hans 確認後執行）

- [ ] 文章標題確認
- [ ] 封面圖提供（1200×630 PNG）
- [ ] 內鏈配置確認
- [ ] CTA 確認
- [ ] 免責聲明確認
- [ ] Permalink 確認

## Deploy 步驟（確認後）

1. `cp build/articles/NEW-ARTICLE.html articles/`
2. 更新 `articles/index.html`
3. 更新 `index.html`（最新文章區）
4. 更新 `sitemap.xml`
5. `git add -A`
6. `git commit -m "feat: add ARTICLE-NAME"`
7. `git push origin main`
8. 驗證 Cloudflare Pages deploy
9. 驗證正式站 200
