import re

# ============================================================
# 1. CSS 修改：卡片圖片加圓角
# ============================================================
with open('/root/.openclaw/workspace/fun1399-clean/static/css/style.css', 'r') as f:
    css = f.read()

# 在 .card-image 區塊添加 border-radius
old_card_image = """/* 圖片區 */
.card-image {
    position: relative;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
}"""

new_card_image = """/* 圖片區 */
.card-image {
    position: relative;
    aspect-ratio: 16 / 9;
    overflow: hidden;
    background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
    border-radius: 8px 8px 0 0;
}

/* Featured 卡片圖片左側圓角 */
.article-card.featured .card-image {
    border-radius: 16px 0 0 16px;
}

/* 手機版 Featured 卡片圖片頂部圓角 */
@media (max-width: 768px) {
    .article-card.featured .card-image {
        border-radius: 16px 16px 0 0;
    }
}"""

css = css.replace(old_card_image, new_card_image)

with open('/root/.openclaw/workspace/fun1399-clean/static/css/style.css', 'w') as f:
    f.write(css)

print("✅ CSS updated: card-image border-radius added")

# ============================================================
# 2. index.html：詐騙調查區塊背景改為白底
# ============================================================
with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'r') as f:
    html = f.read()

# 移除詐騙調查區塊的特殊背景色，改為純白底
html = html.replace(
    'style="padding-top: 48px; padding-bottom: 48px; margin-top: 24px; margin-bottom: 24px; background: linear-gradient(135deg, #faf5f5 0%, #f8f0f0 100%); border-top: 1px solid #f0e0e0; border-bottom: 1px solid #f0e0e0;"',
    'style="padding-top: 48px; padding-bottom: 48px; margin-top: 24px; margin-bottom: 24px;"'
)

# 標題顏色從深紅改回一般顏色（但保留警示感用 badge 呈現）
html = html.replace(
    '<h2 style="color: #8b1a1a;">🔥 娛樂城詐騙熱門調查</h2>',
    '<h2>🔥 娛樂城詐騙熱門調查</h2>'
)

with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'w') as f:
    f.write(html)

print("✅ index.html updated: scam section background unified")

# ============================================================
# 3. articles/index.html：移除底部 CTA 和 sidebar 小工具
# ============================================================
with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    articles = f.read()

# 找到 footer 開始的位置
footer_start = articles.find('<footer class="footer">')
if footer_start == -1:
    print("❌ Footer not found")
    exit(1)

# 找到 body 結束的位置
body_end = articles.find('</body>')
if body_end == -1:
    print("❌ </body> not found")
    exit(1)

# 保留 footer 之前的所有內容 + footer 本身（只保留品牌信息和版权）
# 然後跳到 </body> 之前加入浮動按鈕

# 構建新的 footer 區塊（乾淨簡潔）
new_footer = """    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-brand">
                    <h4>娛樂城玩家俱樂部</h4>
                    <p>台灣最專業的娛樂城玩家互助平台</p>
                </div>
                <div class="footer-links">
                    <a href="/recommend/2026">2026推薦</a>
                    <a href="/reviews/">平台評測</a>
                    <a href="/articles/">攻略文章</a>
                    <a href="/about">關於我們</a>
                    <a href="/author">作者介紹</a>
                    <a href="/contact">聯絡我們</a>
                    <a href="/responsible-gaming">理性博彩</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>© 2026 娛樂城玩家俱樂部. 僅供參考，理性遊戲.</p>
            </div>
        </div>
    </footer>

    <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">立即遊玩</a>
    <a href="https://lin.ee/Mc1pb7z" class="float-line" target="_blank">LINE@</a>
</body>
</html>"""

# 從 footer 開始到文件結尾替換為新的乾淨 footer
articles = articles[:footer_start] + new_footer

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(articles)

print(f"✅ articles/index.html updated: removed sidebar widgets and bottom CTA")
print(f"   New size: {len(articles)} bytes")

# 驗證 div 標籤平衡
open_div = articles.count('<div')
close_div = articles.count('</div>')
print(f"   div tags: open={open_div}, close={close_div}")

print("\n🎉 All modifications completed!")
