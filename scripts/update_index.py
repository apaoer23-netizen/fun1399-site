import re

with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'r') as f:
    content = f.read()

# ========== 1. Replace Latest Articles section ==========
latest_start = content.find('    <!-- Latest Articles -->')
latest_end = content.find('    <!-- Scam Authority Cluster -->')

new_latest = '''    <!-- Latest Articles -->
    <section class="latest-articles">
        <div class="container">
            <h2>📚 最新攻略文章</h2>
            <!-- Featured 頭條 -->
            <a href="/articles/casino-scam-alert" class="article-card featured" style="margin-bottom: 24px; text-decoration: none; color: inherit;">
                <div class="card-image">
                    <img src="/static/images/articles/scam/casino-scam-alert-cover-2026.png" alt="娛樂城詐騙警示｜2026最新詐騙手法與防範完整指南" loading="lazy">
                </div>
                <div class="card-content">
                    <div class="card-meta">
                        <span class="card-badge scam">⚠️ 詐騙警示</span>
                        <span>2026年5月15日</span>
                    </div>
                    <h3 class="card-title">娛樂城詐騙警示｜2026最新詐騙手法與防範完整指南</h3>
                    <p class="card-excerpt">揭露7大最新娛樂城詐騙手法：不出金、假客服、代操投資、愛情詐騙、帳號凍結、USDT詐騙。完整防詐自保指南、查證平台方法與被騙後應變步驟。7大類型一次掌握，遠離詐騙陷阱。</p>
                    <span class="card-readmore">閱讀完整指南 →</span>
                </div>
            </a>
            <!-- 一般文章網格 -->
            <div class="article-grid-v2">
                <a href="/articles/usdt-casino-scam-2026" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/usdt-casino-scam-2026-cover.webp" alt="娛樂城USDT詐騙" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">詐騙</span>
                            <span>2026年5月15日</span>
                        </div>
                        <h3 class="card-title">娛樂城USDT詐騙：虛擬貨幣儲值陷阱與防範教學</h3>
                        <p class="card-excerpt">2026最新USDT詐騙手法全解析！虛擬貨幣儲值陷阱、不出金黑網特徵與自保教學...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/hg-casino-promotions-may-2026" class="article-card promo-card">
                    <div class="card-image">
                        <img src="/static/images/articles/promo/hg-promo-may-2026-cover.webp" alt="HG娛樂城5月優惠" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge promo">優惠</span>
                            <span>2026年5月13日</span>
                        </div>
                        <h3 class="card-title">HG娛樂城2026年5月優惠整理：首儲與返水活動實測</h3>
                        <p class="card-excerpt">HG娛樂城5月最新優惠整理！首儲活動、返水比例、每日加碼優惠完整實測...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/casino-license-verification-2026" class="article-card">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/casino-license-verification-2026-cover.webp" alt="娛樂城牌照查證" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge guide">教學</span>
                            <span>2026年5月11日</span>
                        </div>
                        <h3 class="card-title">如何查詢娛樂城牌照與合法性：官方認證3步驟驗證法</h3>
                        <p class="card-excerpt">3步驟驗證平台合法性，從官方監管機構查詢、牌照真偽辨識到黑網資料庫比對...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/fake-line-official-account" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/fake-line-official-account-cover.webp" alt="假LINE官方帳號辨識" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">詐騙</span>
                            <span>2026年5月8日</span>
                        </div>
                        <h3 class="card-title">娛樂城假客服詐騙升級版：LINE官方帳號辨識全攻略</h3>
                        <p class="card-excerpt">2026年假客服詐騙已全面升級！詐騙集團偽造官方認證、搭建仿冒客服系統...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/jucity-casino-review-may-2026" class="article-card review-card">
                    <div class="card-image">
                        <img src="/static/images/articles/reviews/jucity-casino-review-may-2026-cover.webp" alt="鉅城娛樂城評價" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge review">評測</span>
                            <span>2026年5月6日</span>
                        </div>
                        <h3 class="card-title">鉅城娛樂城2026年5月評價更新：出金速度與客服實測</h3>
                        <p class="card-excerpt">實測出金平均2分41秒、客服17秒回應，PTT/Dcard玩家真實心得整理...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/biwin-casino-no-withdrawal" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/biwin-casino-no-withdrawal-cover.webp" alt="必贏娛樂城不出金" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">不出金</span>
                            <span>2026年5月4日</span>
                        </div>
                        <h3 class="card-title">必贏娛樂城不出金怎麼辦？受害者投訴與自救方法實測</h3>
                        <p class="card-excerpt">整理PTT受害者投訴、不出金詐騙手法拆解與5步驟自救方法...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
            </div>
        </div>
    </section>

'''

content = content[:latest_start] + new_latest + content[latest_end:]

# ========== 2. Replace Scam Authority Cluster section ==========
scam_start = content.find('    <!-- Scam Authority Cluster -->')
scam_end = content.find('    <!-- Popular Guides -->')

new_scam = '''    <!-- Scam Authority Cluster -->
    <section class="latest-articles dark-section" style="background: linear-gradient(135deg, #1a0a0a 0%, #0d1a0d 100%);">
        <div class="container">
            <h2 style="color: #ff4757;">🔥 娛樂城詐騙熱門調查</h2>
            <p style="color: #888; margin-bottom: 25px;">持續追蹤的詐騙與爭議調查，幫你避開黑網陷阱</p>
            <div class="article-grid-v2">
                <a href="/articles/3a-casino-scam-review" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/3a-casino-scam-review-cover.webp" alt="3A娛樂城詐騙調查" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">品牌調查</span>
                        </div>
                        <h3 class="card-title">3A娛樂城詐騙是真的嗎？PTT不出金投訴與黑網疑慮</h3>
                        <p class="card-excerpt">PTT/Dcard玩家真實評價、出金實測與爭議解析...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/gm1688-casino-scam-review" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/reviews/gm1688-casino-scam-review-cover.webp" alt="GM1688黑網調查" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">品牌調查</span>
                        </div>
                        <h3 class="card-title">GM1688娛樂城是黑網嗎？不出金投訴與玩家被騙經驗</h3>
                        <p class="card-excerpt">玩家投訴整理、出金問題與黑網疑慮調查...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/casino-investment-scam" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/casino-investment-scam-cover.png" alt="投資代操詐騙" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">投資詐騙</span>
                        </div>
                        <h3 class="card-title">娛樂城投資詐騙手法：代操保證獲利是真的嗎？</h3>
                        <p class="card-excerpt">5大陷阱解析、4步驟詐騙流程與真實受害案例...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/biwin-casino-no-withdrawal" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/biwin-casino-no-withdrawal-cover.webp" alt="必贏不出金" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">不出金</span>
                        </div>
                        <h3 class="card-title">必贏娛樂城不出金怎麼辦？受害者投訴實測</h3>
                        <p class="card-excerpt">不出金詐騙手法拆解與5步驟自救方法...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/wealth-god-casino-scam-review" class="article-card scam-alert">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/wealth-god-casino-scam-review-cover-v2.webp" alt="財神娛樂城詐騙" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">品牌調查</span>
                        </div>
                        <h3 class="card-title">財神娛樂城是詐騙嗎？PTT網友被騙經驗與評價</h3>
                        <p class="card-excerpt">不出金投訴、黑網疑慮與真實評價整理...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/pillars/casino-scam-complete-guide" class="article-card">
                    <div class="card-image">
                        <img src="/static/images/articles/scam/casino-scam-complete-guide-cover-2026.png" alt="2026詐騙完整指南" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge hot">完整指南</span>
                        </div>
                        <h3 class="card-title">2026娛樂城詐騙完整指南：8大類型與受害案例</h3>
                        <p class="card-excerpt">從不出金、假客服到PTT真實案例的完整防護手冊...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
            </div>
        </div>
    </section>

'''

content = content[:scam_start] + new_scam + content[scam_end:]

# ========== 3. Replace Popular Guides article cards ==========
# Find the article-grid within Popular Guides
pg_start = content.find('    <!-- Popular Guides -->')
pg_grid_start = content.find('<div class="article-grid">', pg_start)
pg_grid_end = content.find('</section>', pg_grid_start) + len('</section>')

# Actually let's find the end of the article-grid div more precisely
pg_grid_end = content.find('            </div>\n        </div>\n    </section>', pg_grid_start)

new_popular = '''    <!-- Popular Guides -->

    <section class="popular-guides">
        <div class="container">
            <h2>🔥 熱門攻略推薦</h2>
            <div class="article-grid-v2">
                <a href="/articles/2026-casino-recommendation" class="article-card">
                    <div class="card-image" style="background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);">
                        <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #ffd700; font-size: 3rem; font-weight: 700;">🏆</div>
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge hot">推薦</span>
                        </div>
                        <h3 class="card-title">2026娛樂城推薦完整指南</h3>
                        <p class="card-excerpt">最新娛樂城評測，嚴選5大值得信賴平台...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/withdrawal-ranking" class="article-card">
                    <div class="card-image" style="background: linear-gradient(135deg, #0a4a3a 0%, #00a884 100%);">
                        <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 3rem; font-weight: 700;">💰</div>
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge guide">排行</span>
                        </div>
                        <h3 class="card-title">娛樂城出金速度排行</h3>
                        <p class="card-excerpt">實測6大平台出金速度，15分鐘內到帳...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
                <a href="/articles/safety-guide" class="article-card">
                    <div class="card-image" style="background: linear-gradient(135deg, #1a0a0a 0%, #4a1a1a 100%);">
                        <div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #ff6b6b; font-size: 3rem; font-weight: 700;">🛡️</div>
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">安全</span>
                        </div>
                        <h3 class="card-title">娛樂城安全指南</h3>
                        <p class="card-excerpt">如何判斷平台是否安全，避開詐騙陷阱...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>
            </div>
        </div>
    </section>'''

# Find the full section from <!-- Popular Guides --> to the end of </section>
pg_full_start = content.find('    <!-- Popular Guides -->')
# Find the next <!-- after this section
next_comment = content.find('    <!-- ', pg_full_start + 1)
if next_comment == -1:
    next_comment = len(content)

# But we need to be more precise - find where the Popular Guides section ends
# Look for pattern: </div>\n        </div>\n    </section> after article-grid
pg_section_end_marker = '        </div>\n    </section>'
pg_section_end = content.find(pg_section_end_marker, pg_grid_start)
if pg_section_end != -1:
    pg_section_end += len(pg_section_end_marker)

content = content[:pg_full_start] + new_popular + content[pg_section_end:]

with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'w') as f:
    f.write(content)

print('index.html updated successfully')
print('New file size:', len(content))
