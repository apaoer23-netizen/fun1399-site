# Fun1399.com 文章模板規範（2026年3月15日更新）

## 📋 模板總覽

### 文章類型分類

| 類型 | 說明 | 平台比較位置 |
|------|------|-------------|
| **推薦/比較類** | 出金排行、RTP比較、平台推薦 | 文章內文自然呈現 |
| **攻略教學類** | 百家樂技巧、老虎機攻略、投注教學 | 不需要平台比較 |
| **新聞分析類** | 產業新聞、賽事分析 | 視內容需要 |

---

## 📝 統一文章結構

### 1. HTML 基本架構

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章標題 - 娛樂城玩家俱樂部</title>
    <meta name="description" content="文章描述，150字以內">
    <link rel="stylesheet" href="/static/css/style.css">
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-1V53J5D71S"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', 'G-1V53J5D71S');
    </script>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <div class="logo"><a href="/">娛樂城玩家俱樂部</a></div>
            <nav class="nav">
                <a href="/">首頁</a>
                <!-- 其他導航連結 -->
                <a href="https://fun1399.ofa177.net/" class="play-btn" target="_blank" rel="noopener">立即遊玩</a>
                <a href="https://lin.ee/Mc1pb7z" class="line-btn" target="_blank">加入LINE</a>
            </nav>
        </div>
    </header>

    <!-- 文章內容 -->
    <article class="content">
        <div class="container content-with-sidebar">
            <div class="content-main">
                
                <!-- 麵包屑 -->
                <nav class="breadcrumb">
                    <a href="/">首頁</a> > 
                    <a href="/articles/">攻略文章</a> > 
                    <span>文章標題</span>
                </nav>

                <!-- H1 標題 -->
                <h1>文章標題</h1>
                
                <!-- 作者資訊 -->
                <div class="article-meta">
                    <div class="author-info">
                        <span class="author-name">
                            👤 作者：<a href="/author.html#作者ID">作者名稱</a>（作者頭銜）
                        </span>
                        <span class="publish-date">📅 發布日期：2026年MM月DD日</span>
                        <span class="update-date">🔄 最後更新：2026年MM月DD日</span>
                    </div>
                </div>

                <!-- 文章引言 -->
                <div class="intro">
                    <p><strong>關鍵字</strong>是文章主題...</p>
                </div>

                <!-- 目錄（選用） -->
                <div class="toc">
                    <h3>目錄</h3>
                    <ol>
                        <li><a href="#section1">第一節標題</a></li>
                        <li><a href="#section2">第二節標題</a></li>
                    </ol>
                </div>

                <!-- 文章內容 -->
                <h2 id="section1">第一節標題</h2>
                <p>內容...</p>

                <!-- 平台比較（如需要）-->
                <!-- 在相關段落下方自然插入，非固定區塊 -->
                
            </div>

            <!-- Sidebar -->
            <aside class="sidebar">
                <!-- 推薦娛樂城 -->
                <div class="sidebar-widget">
                    <h4>🔥 推薦娛樂城</h4>
                    <ul class="sidebar-list">
                        <li>
                            <a href="/reviews/jucity.html" class="sidebar-link">
                                <span class="sidebar-rank">#1</span>
                                <span>鉅城娛樂城</span>
                                <span class="sidebar-rating">★4.9</span>
                            </a>
                        </li>
                        <li>
                            <a href="/reviews/mbm.html" class="sidebar-link">
                                <span class="sidebar-rank">#2</span>
                                <span>MBM娛樂城</span>
                                <span class="sidebar-rating">★4.7</span>
                            </a>
                        </li>
                        <li>
                            <a href="/reviews/utown.html" class="sidebar-link">
                                <span class="sidebar-rank">#3</span>
                                <span>優塔娛樂城</span>
                                <span class="sidebar-rating">★4.6</span>
                            </a>
                        </li>
                    </ul>
                </div>

                <!-- 熱門攻略 -->
                <div class="sidebar-widget">
                    <h4>📚 熱門攻略</h4>
                    <ul class="sidebar-list">
                        <li><a href="/articles/baccarat-guide.html">百家樂技巧攻略</a></li>
                        <li><a href="/articles/slots-guide.html">老虎機RTP攻略</a></li>
                        <li><a href="/articles/sports-betting-guide.html">體育投注教學</a></li>
                    </ul>
                </div>

                <!-- LINE CTA -->
                <div class="sidebar-widget sidebar-cta">
                    <h4>💬 加入 LINE@</h4>
                    <p>獲取最新優惠情報與專業攻略</p>
                    <a href="https://lin.ee/Mc1pb7z" class="btn btn-line" target="_blank">加入好友</a>
                </div>
            </aside>
        </div>

        <!-- 底部CTA（所有文章統一）-->
        <div class="cta-box bottom-cta">
            <h3>🚀 準備開始你的娛樂城之旅？</h3>
            <p>立即加入我們推薦的平台，領取專屬優惠！</p>
            <div class="cta-buttons">
                <a href="https://fun1399.ofa177.net/" target="_blank" rel="noopener" class="btn btn-primary btn-large">🎮 立即遊玩</a>
                <a href="https://lin.ee/Mc1pb7z" target="_blank" class="btn btn-line btn-large">💬 加入LINE@獲取優惠</a>
            </div>
        </div>

        <!-- 相關文章推薦 -->
        <div class="related-articles">
            <h3>📚 相關文章推薦</h3>
            <ul class="related-list">
                <li>👉 <a href="/articles/文章1.html">相關文章標題1</a></li>
                <li>👉 <a href="/articles/文章2.html">相關文章標題2</a></li>
                <li>👉 <a href="/articles/文章3.html">相關文章標題3</a></li>
                <li>👉 <a href="/recommend/2026.html">2026最新娛樂城推薦</a></li>
                <li>👉 <a href="/articles/safety-guide.html">娛樂城安全指南</a></li>
            </ul>
        </div>
    </article>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <p>© 2026 娛樂城玩家俱樂部</p>
        </div>
    </footer>
</body>
</html>
```

---

## 👤 作者資訊規範

### 可用作者

| 作者ID | 姓名 | 頭銜 | 專長領域 |
|--------|------|------|----------|
| kevin | Kevin Lin | 資深娛樂城分析師 / 百家樂策略專家 | 百家樂、策略分析 |
| jason | Jason Chen | 博弈產業研究員 / 數據分析師 | 產業分析、數據研究 |
| vivian | Vivian Wu | 資深玩家顧問 / 優惠活動專家 | 優惠攻略、新手教學 |

### 作者連結格式
```html
<a href="/author.html#kevin">Kevin Lin</a>
<a href="/author.html#jason">Jason Chen</a>
<a href="/author.html#vivian">Vivian Wu</a>
```

---

## 🏢 平台比較寫作規範

### ⚠️ 重要原則

**平台比較應融入文章內文，不要固定區塊！**

### 正確寫法範例

#### 範例1：出金排行文章

```html
<p>目前出金速度較快的娛樂城主要有以下幾家：</p>

<table class="data-table">
    <thead>
        <tr>
            <th>平台</th>
            <th>出金速度</th>
            <th>特色</th>
            <th>連結</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>MBM娛樂城</td>
            <td>2分鐘</td>
            <td>極速出金</td>
            <td><a href="https://fun1399.mbm88.net/" target="_blank">立即註冊</a></td>
        </tr>
        <tr>
            <td>鉅城娛樂城</td>
            <td>15分鐘</td>
            <td>穩定快速</td>
            <td><a href="https://fun1399.ofa177.net/" target="_blank">立即註冊</a></td>
        </tr>
    </tbody>
</table>
```

#### 範例2：RTP比較文章

```html
<p>各平台高RTP老虎機比較：</p>

<h3>鉅城娛樂城</h3>
<p>平均RTP 96.2%，推薦遊戲：</p>
<ul>
    <li>血戰到底 - RTP 97.5%</li>
    <li>五福臨門 - RTP 97.2%</li>
</ul>
<a href="https://fun1399.ofa177.net/" target="_blank" class="btn btn-primary">立即註冊鉅城</a>

<h3>MBM娛樂城</h3>
<p>平均RTP 96.0%，推薦遊戲...</p>
<a href="https://fun1399.mbm88.net/" target="_blank" class="btn btn-primary">立即註冊MBM</a>
```

### 平台連結對照表

| 平台 | 連結 | 特色標語 |
|------|------|----------|
| 鉅城娛樂城 | https://fun1399.ofa177.net/ | 首儲1000送1000 |
| MBM娛樂城 | https://fun1399.mbm88.net/ | 2分鐘極速出金 |
| 優塔娛樂城 | https://u.town/3006 | USDT專精 1%返水 |
| HG娛樂城 | https://www.leyo.tw/r?p=685e99859c687 | 體驗金388免費試玩 |
| 大老爺娛樂城 | https://fun1399.gm1688.net/ | 遊戲種類最豐富 |
| 3A娛樂城 | https://fun1399.3a1788.bet/ | 新手友善平台 |

---

## ⚠️ 寫作注意事項

### ✅ 應該做的事

1. **字數要求**：核心內容至少 2000 字以上
2. **作者資訊**：必須包含作者連結到 /author.html#作者ID
3. **日期標示**：發布日期與更新日期
4. **內部連結**：至少 3 個網站內部連結
5. **底部CTA**：保留「立即遊玩 + 加入LINE」
6. **Sidebar**：保留推薦平台與熱門攻略
7. **相關文章**：至少 3-5 篇相關文章連結

### ❌ 不應該做的事

1. **不要固定平台推薦區塊**：不要在文章底部固定插入5家平台推薦
2. **不要過度商業化**：一般攻略文章不要在內文插入過多平台推薦
3. **不要重複內容**：平台比較應與文章主題相關
4. **不要使用占位符**：[聯盟連結] 等占位符必須替換為真實連結

---

## 📝 文章品質檢查清單

發布前請確認：

- [ ] 字數達 2000 字以上
- [ ] 有作者資訊且連結正確
- [ ] 有發布日期與更新日期
- [ ] 有麵包屑導航
- [ ] 底部CTA正確（立即遊玩 + 加入LINE）
- [ ] Sidebar 完整
- [ ] 有相關文章推薦
- [ ] 無 [占位符] 未替換
- [ ] 所有連結可正常點擊
- [ ] 平台比較自然融入內文（如需要）

---

## 🔄 更新記錄

| 日期 | 更新內容 |
|------|----------|
| 2026-03-15 | 移除固定平台推薦區塊，改為內文自然呈現 |
| 2026-03-15 | 統一底部CTA格式 |
| 2026-03-15 | 建立作者連結規範 |

---

**文件版本：v1.0**
**適用日期：2026年3月15日起**
