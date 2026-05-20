#!/usr/bin/env python3
"""
Scam Authority Cluster 強化腳本
修改 7 篇文章的延伸閱讀區塊、2 篇文章標題、首頁結構
"""

import os
import re

BASE = "/root/.openclaw/workspace/fun1399-clean"

# 每篇文章的延伸閱讀連結映射（至少 5 篇互連）
RELATED_MAP = {
    "3a-casino-scam-review": [
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/casino-investment-scam", "娛樂城投資詐騙手法", "代操保證獲利？5大陷阱解析"),
        ("/articles/casino-no-withdrawal-scam", "不出金詐騙解析", "為什麼贏了錢卻領不出來？"),
        ("/articles/casino-romance-scam", "娛樂城愛情詐騙揭秘", "交友軟體假帳號識別指南"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/wealth-god-casino-scam-review", "財神娛樂城評價", "PTT網友被騙經驗實測"),
        ("/articles/biwin-casino-no-withdrawal", "必贏娛樂城不出金", "受害者投訴與自救方法"),
    ],
    "gm1688-casino-scam-review": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/casino-investment-scam", "娛樂城投資詐騙手法", "代操保證獲利？5大陷阱解析"),
        ("/articles/casino-no-withdrawal-scam", "不出金詐騙解析", "為什麼贏了錢卻領不出來？"),
        ("/articles/casino-romance-scam", "娛樂城愛情詐騙揭秘", "交友軟體假帳號識別指南"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/wealth-god-casino-scam-review", "財神娛樂城評價", "PTT網友被騙經驗實測"),
        ("/articles/biwin-casino-no-withdrawal", "必贏娛樂城不出金", "受害者投訴與自救方法"),
    ],
    "casino-investment-scam": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/casino-no-withdrawal-scam", "不出金詐騙解析", "為什麼贏了錢卻領不出來？"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/casino-scam-alert", "娛樂城詐騙警示", "2026最新詐騙手法與防範"),
        ("/articles/casino-account-freeze-scam", "帳號凍結詐騙", "要求儲值解凍全是騙局"),
        ("/articles/casino-fake-customer-service", "假客服詐騙升級版", "LINE官方帳號辨識全攻略"),
    ],
    "casino-no-withdrawal-scam": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/casino-investment-scam", "娛樂城投資詐騙手法", "代操保證獲利？5大陷阱解析"),
        ("/articles/biwin-casino-no-withdrawal", "必贏娛樂城不出金", "受害者投訴與自救方法"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/casino-scam-alert", "娛樂城詐騙警示", "2026最新詐騙手法與防範"),
        ("/articles/how-to-check-casino-scam-record", "查詢詐騙紀錄", "3步驟驗證法完整教學"),
    ],
    "casino-romance-scam": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/casino-investment-scam", "娛樂城投資詐騙手法", "代操保證獲利？5大陷阱解析"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/casino-scam-alert", "娛樂城詐騙警示", "2026最新詐騙手法與防範"),
        ("/articles/casino-fake-customer-service", "假客服詐騙升級版", "LINE官方帳號辨識全攻略"),
        ("/articles/casino-account-freeze-scam", "帳號凍結詐騙", "要求儲值解凍全是騙局"),
    ],
    "wealth-god-casino-scam-review": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/biwin-casino-no-withdrawal", "必贏娛樂城不出金", "受害者投訴與自救方法"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/casino-scam-alert", "娛樂城詐騙警示", "2026最新詐騙手法與防範"),
        ("/articles/casino-no-withdrawal-scam", "不出金詐騙解析", "為什麼贏了錢卻領不出來？"),
    ],
    "biwin-casino-no-withdrawal": [
        ("/articles/3a-casino-scam-review", "3A娛樂城詐騙疑慮", "PTT真實評價與出金實測"),
        ("/articles/gm1688-casino-scam-review", "GM1688黑網調查", "玩家投訴與出金問題整理"),
        ("/articles/wealth-god-casino-scam-review", "財神娛樂城評價", "PTT網友被騙經驗實測"),
        ("/articles/casino-no-withdrawal-scam", "不出金詐騙解析", "為什麼贏了錢卻領不出來？"),
        ("/pillars/casino-scam-complete-guide", "娛樂城詐騙完整指南", "8大類型與PTT受害案例整理"),
        ("/articles/casino-scam-alert", "娛樂城詐騙警示", "2026最新詐騙手法與防範"),
        ("/articles/how-to-check-casino-scam-record", "查詢詐騙紀錄", "3步驟驗證法完整教學"),
    ],
}

def build_related_section(links):
    """生成統一格式的延伸閱讀 HTML"""
    cards = ""
    for url, title, desc in links:
        cards += f'''                <a href="{url}" style="background: rgba(255,255,255,0.05); border-radius: 8px; padding: 15px; text-decoration: none; color: #111; display: block; transition: background 0.3s;">
                    <div style="color: #00d4aa; font-weight: 600; margin-bottom: 5px;">{title}</div>
                    <div style="font-size: 14px; color: #555;">{desc}</div>
                </a>\n'''
    
    return f'''        <!-- 延伸閱讀：娛樂城詐騙調查 -->
        <div style="margin-top: 50px; padding-top: 30px; border-top: 1px solid rgba(255,255,255,0.1);">
            <h3 style="color: #FFD700; margin-bottom: 20px;">📚 延伸閱讀：娛樂城詐騙調查</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
{cards}            </div>
        </div>
'''

def modify_article(filename, links):
    """修改單篇文章，替換或新增延伸閱讀區塊"""
    path = os.path.join(BASE, "articles", filename)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    related_html = build_related_section(links)
    
    # 嘗試替換現有的延伸閱讀區塊
    patterns = [
        r'<!-- 延伸閱讀 -->.*?<!-- Footer -->',
        r'<!-- 延伸閱讀 -->.*?<footer class="footer">',
        r'<div class="related-articles">.*?</div>\s*</article>',
        r'<div class="cta-box">\s*<h3>延伸閱讀</h3>.*?</div>\s*</article>',
    ]
    
    replaced = False
    for pattern in patterns:
        if re.search(pattern, content, re.DOTALL):
            # 找到延伸閱讀，替換掉
            content = re.sub(
                pattern,
                related_html + "\n    </article>\n\n    <!-- Footer -->",
                content,
                flags=re.DOTALL,
                count=1
            )
            replaced = True
            break
    
    if not replaced:
        # 沒找到現有延伸閱讀，在 </article> 前插入
        content = content.replace(
            "    </article>",
            related_html + "    </article>",
            1
        )
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ 已修改: {filename}")

def update_titles():
    """優化 2 篇高曝光文章的 title 和 meta"""
    # 3a-casino-scam-review
    path_3a = os.path.join(BASE, "articles", "3a-casino-scam-review.html")
    with open(path_3a, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_title = "3A娛樂城詐騙疑慮解析：新手必看的安全性、出金實測與真實評價（2026）"
    new_title = "3A娛樂城詐騙是真的嗎？PTT不出金投訴、黑網疑慮與玩家真實評價（2026）"
    
    content = content.replace(old_title, new_title, 3)  # title tag, og:title
    content = content.replace(
        'content="3A娛樂城是詐騙嗎？深度解析3A娛樂城安全性、1-2分鐘出金實測速度、PTT/Dcard真實評價。客觀分析優缺點與詐騙傳聞真假，2026最新指南。"',
        'content="3A娛樂城詐騙是真的嗎？整理PTT網友不出金投訴、黑網疑慮、玩家真實評價。2026最新調查報告，客觀分析安全性與出金實測。"'
    )
    content = content.replace(
        'content="深度解析3A娛樂城評價、詐騙傳聞真假、1-2分鐘出金速度、玩家真實經驗。客觀分析優缺點。"',
        'content="3A娛樂城詐騙調查：PTT不出金投訴整理、黑網疑慮分析、玩家真實評價。2026最新客觀報告。"'
    )
    
    with open(path_3a, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已更新 title: 3a-casino-scam-review → {new_title}")
    
    # gm1688-casino-scam-review
    path_gm = os.path.join(BASE, "articles", "gm1688-casino-scam-review.html")
    with open(path_gm, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_title_gm = "GM1688娛樂城評價爭議：出金問題、玩家投訴與黑網疑慮深度調查（2026）"
    new_title_gm = "GM1688娛樂城是黑網嗎？不出金投訴、玩家被騙經驗與PTT評價整理（2026）"
    
    content = content.replace(old_title_gm, new_title_gm, 3)
    
    with open(path_gm, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 已更新 title: gm1688-casino-scam-review → {new_title_gm}")

def add_homepage_section():
    """在首頁 Latest Articles 下方新增熱門調查區"""
    path = os.path.join(BASE, "index.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 找到 Latest Articles section 結束後的 Popular Guides section
    # 在 Latest Articles 和 Popular Guides 之間插入新區塊
    
    new_section = '''    <!-- Scam Authority Cluster -->
    <section class="latest-articles" style="background: linear-gradient(135deg, #1a0a0a 0%, #0d1a0d 100%);">
        <div class="container">
            <h2 style="color: #ff4757;">🔥 娛樂城詐騙熱門調查</h2>
            <p style="color: #888; margin-bottom: 25px;">持續追蹤的詐騙與爭議調查，幫你避開黑網陷阱</p>
            <div class="article-grid">
                <article class="article-card">
                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">品牌調查</span>
                    <h3><a href="/articles/3a-casino-scam-review">3A娛樂城詐騙是真的嗎？PTT不出金投訴與黑網疑慮</a></h3>
                    <p>PTT/Dcard玩家真實評價、出金實測與爭議解析...</p>
                    <a href="/articles/3a-casino-scam-review" class="read-more">閱讀全文 →</a>
                </article>
                <article class="article-card">
                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">品牌調查</span>
                    <h3><a href="/articles/gm1688-casino-scam-review">GM1688娛樂城是黑網嗎？不出金投訴與玩家被騙經驗</a></h3>
                    <p>玩家投訴整理、出金問題與黑網疑慮調查...</p>
                    <a href="/articles/gm1688-casino-scam-review" class="read-more">閱讀全文 →</a>
                </article>
                <article class="article-card">
                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">投資詐騙</span>
                    <h3><a href="/articles/casino-investment-scam">娛樂城投資詐騙手法：代操保證獲利是真的嗎？</a></h3>
                    <p>5大陷阱解析、4步驟詐騙流程與真實受害案例...</p>
                    <a href="/articles/casino-investment-scam" class="read-more">閱讀全文 →</a>
                </article>
                <article class="article-card">
                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">不出金</span>
                    <h3><a href="/articles/biwin-casino-no-withdrawal">必贏娛樂城不出金怎麼辦？受害者投訴實測</a></h3>
                    <p>不出金詐騙手法拆解與5步驟自救方法...</p>
                    <a href="/articles/biwin-casino-no-withdrawal" class="read-more">閱讀全文 →</a>
                </article>
                <article class="article-card">
                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">品牌調查</span>
                    <h3><a href="/articles/wealth-god-casino-scam-review">財神娛樂城是詐騙嗎？PTT網友被騙經驗與評價</a></h3>
                    <p>不出金投訴、黑網疑慮與真實評價整理...</p>
                    <a href="/articles/wealth-god-casino-scam-review" class="read-more">閱讀全文 →</a>
                </article>
                <article class="article-card">
                    <span class="article-tag" style="background: #00d4aa; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">完整指南</span>
                    <h3><a href="/pillars/casino-scam-complete-guide">2026娛樂城詐騙完整指南：8大類型與受害案例</a></h3>
                    <p>從不出金、假客服到PTT真實案例的完整防護手冊...</p>
                    <a href="/pillars/casino-scam-complete-guide" class="read-more">閱讀全文 →</a>
                </article>
            </div>
        </div>
    </section>

    <!-- Popular Guides -->
'''
    
    # 替換 Popular Guides section 的開始標記
    content = content.replace(
        '    <!-- Popular Guides -->',
        new_section
    )
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ 已新增首頁「🔥 娛樂城詐騙熱門調查」區塊")

if __name__ == '__main__':
    print("=" * 60)
    print("Scam Authority Cluster 強化腳本")
    print("=" * 60)
    
    # 1. 修改 7 篇文章
    for filename, links in RELATED_MAP.items():
        modify_article(f"{filename}.html", links)
    
    # 2. 更新 2 篇文章 title
    update_titles()
    
    # 3. 新增首頁區塊
    add_homepage_section()
    
    print("=" * 60)
    print("✅ 全部完成！")
    print("=" * 60)
