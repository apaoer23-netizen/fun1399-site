import re

with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'r') as f:
    content = f.read()

# ========== 1. Fix Section Spacing ==========
# Add spacing between major sections by modifying section styles

# Top casinos section - add margin-bottom
content = content.replace(
    '<section class="top-casinos">',
    '<section class="top-casinos" style="margin-bottom: 48px;">'
)

# Latest articles section - add margin-top and margin-bottom
content = content.replace(
    '<section class="latest-articles">',
    '<section class="latest-articles" style="padding-top: 32px; padding-bottom: 32px;">'
)

# Scam section - remove dark background, add light border and spacing
content = content.replace(
    '<section class="latest-articles dark-section" style="background: linear-gradient(135deg, #1a0a0a 0%, #0d1a0d 100%);">',
    '<section class="latest-articles" style="padding-top: 48px; padding-bottom: 48px; margin-top: 24px; margin-bottom: 24px; background: linear-gradient(135deg, #faf5f5 0%, #f8f0f0 100%); border-top: 1px solid #f0e0e0; border-bottom: 1px solid #f0e0e0;">'
)

# Update scam section heading style (remove inline red color)
content = content.replace(
    '<h2 style="color: #ff4757;">🔥 娛樂城詐騙熱門調查</h2>',
    '<h2 style="color: #8b1a1a;">🔥 娛樂城詐騙熱門調查</h2>'
)
content = content.replace(
    '<p style="color: #888; margin-bottom: 25px;">持續追蹤的詐騙與爭議調查，幫你避開黑網陷阱</p>',
    '<p style="color: #666; margin-bottom: 25px;">持續追蹤的詐騙與爭議調查，幫你避開黑網陷阱</p>'
)

# Popular guides section - add spacing
content = content.replace(
    '<section class="popular-guides">',
    '<section class="popular-guides" style="padding-top: 48px; padding-bottom: 48px; margin-top: 24px; margin-bottom: 24px;">'
)

# Featured navigation section - add spacing and remove dark background
content = content.replace(
    '<section class="popular-guides" style="background: linear-gradient(135deg, #0a1a0a 0%, #0d0d1a 100%);">',
    '<section class="popular-guides" style="padding-top: 48px; padding-bottom: 48px; margin-top: 24px; margin-bottom: 24px; background: linear-gradient(135deg, #f8f9fa 0%, #f0f2f5 100%); border-top: 1px solid #e8e8e8; border-bottom: 1px solid #e8e8e8;">'
)

# Update featured nav heading style
content = content.replace(
    '<h2>📌 精選攻略導航</h2>\n            <p style="color: #888; margin-bottom: 25px;">熱門主題快速連結，幫你找到需要的資訊</p>',
    '<h2>📌 精選攻略導航</h2>\n            <p style="color: #666; margin-bottom: 25px;">熱門主題快速連結，幫你找到需要的資訊</p>'
)

# ========== 2. Fix Popular Guides - Replace emoji placeholders with real covers ==========

# 2026-casino-recommendation
content = content.replace(
    '''<a href="/articles/2026-casino-recommendation" class="article-card">
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
                </a>''',
    '''<a href="/articles/2026-casino-recommendation" class="article-card">
                    <div class="card-image">
                        <img src="/static/images/articles/tech/2026-casino-recommendation-cover.webp" alt="2026娛樂城推薦完整指南" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge hot">推薦</span>
                        </div>
                        <h3 class="card-title">2026娛樂城推薦完整指南</h3>
                        <p class="card-excerpt">最新娛樂城評測，嚴選5大值得信賴平台...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>'''
)

# withdrawal-ranking
content = content.replace(
    '''<a href="/articles/withdrawal-ranking" class="article-card">
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
                </a>''',
    '''<a href="/articles/withdrawal-ranking" class="article-card">
                    <div class="card-image">
                        <img src="/static/images/articles/tech/withdrawal-ranking-cover.webp" alt="娛樂城出金速度排行" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge guide">排行</span>
                        </div>
                        <h3 class="card-title">娛樂城出金速度排行</h3>
                        <p class="card-excerpt">實測6大平台出金速度，15分鐘內到帳...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>'''
)

# safety-guide
content = content.replace(
    '''<a href="/articles/safety-guide" class="article-card">
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
                </a>''',
    '''<a href="/articles/safety-guide" class="article-card">
                    <div class="card-image">
                        <img src="/static/images/articles/tech/safety-guide-cover.webp" alt="娛樂城安全指南" loading="lazy">
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge scam">安全</span>
                        </div>
                        <h3 class="card-title">娛樂城安全指南</h3>
                        <p class="card-excerpt">如何判斷平台是否安全，避開詐騙陷阱...</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>'''
)

# ========== 3. Fix Featured Navigation - Convert to image cards ==========
# First, replace the opening of featured nav article grid
content = content.replace(
    '<div class="article-grid">\n                <article class="article-card">\n                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">防詐必讀</span>\n                    <h3><a href="/articles/casino-scam-methods">娛樂城詐騙手法大全：2026最新騙術拆解</a></h3>\n                    <p>整理所有常見詐騙手法，讓你一眼識破黑網陷阱...</p>\n                    <a href="/articles/casino-scam-methods" class="read-more">閱讀全文 →</a>\n                </article>',
    '<div class="article-grid-v2">\n                <a href="/articles/casino-scam-methods" class="article-card scam-alert">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/casino-scam-methods-cover.webp" alt="娛樂城詐騙手法大全" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge scam">防詐必讀</span>\n                        </div>\n                        <h3 class="card-title">娛樂城詐騙手法大全：2026最新騙術拆解</h3>\n                        <p class="card-excerpt">整理所有常見詐騙手法，讓你一眼識破黑網陷阱...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-no-withdrawal-scam
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">防詐必讀</span>\n                    <h3><a href="/articles/casino-no-withdrawal-scam">娛樂城不出金詐騙：如何識別與自保</a></h3>\n                    <p>不出金是最常見的詐騙徵兆，教你提前辨識與應對...</p>\n                    <a href="/articles/casino-no-withdrawal-scam" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-no-withdrawal-scam" class="article-card scam-alert">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/casino-no-withdrawal-scam-cover.webp" alt="娛樂城不出金詐騙" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge scam">防詐必讀</span>\n                        </div>\n                        <h3 class="card-title">娛樂城不出金詐騙：如何識別與自保</h3>\n                        <p class="card-excerpt">不出金是最常見的詐騙徵兆，教你提前辨識與應對...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-fake-customer-service
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #ff4757; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">防詐必讀</span>\n                    <h3><a href="/articles/casino-fake-customer-service">假客服詐騙：LINE官方帳號辨識攻略</a></h3>\n                    <p>詐騙集團偽造官方客服的四步驟辨識法...</p>\n                    <a href="/articles/casino-fake-customer-service" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-fake-customer-service" class="article-card scam-alert">\n                    <div class="card-image">\n                        <img src="/static/images/articles/scam/casino-fake-customer-service-cover.webp" alt="假客服詐騙" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge scam">防詐必讀</span>\n                        </div>\n                        <h3 class="card-title">假客服詐騙：LINE官方帳號辨識攻略</h3>\n                        <p class="card-excerpt">詐騙集團偽造官方客服的四步驟辨識法...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-withdrawal-tutorial (no cover image - use baccarat-chips as fallback)
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #00d4aa; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">出金教學</span>\n                    <h3><a href="/articles/casino-withdrawal-tutorial">娛樂城提款完整教學：出金流程與注意事項</a></h3>\n                    <p>從申請到入帳的完整流程，避免被拖延或拒絕...</p>\n                    <a href="/articles/casino-withdrawal-tutorial" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-withdrawal-tutorial" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/baccarat-chips.webp" alt="娛樂城提款教學" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">出金教學</span>\n                        </div>\n                        <h3 class="card-title">娛樂城提款完整教學：出金流程與注意事項</h3>\n                        <p class="card-excerpt">從申請到入帳的完整流程，避免被拖延或拒絕...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# fast-withdrawal
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #00d4aa; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">出金教學</span>\n                    <h3><a href="/articles/fast-withdrawal">快速出金娛樂城推薦：15分鐘內到帳實測</a></h3>\n                    <p>實測各平台出金速度，整理最快到帳的優質平台...</p>\n                    <a href="/articles/fast-withdrawal" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/fast-withdrawal" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/fast-withdrawal-cover.webp" alt="快速出金娛樂城推薦" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">出金教學</span>\n                        </div>\n                        <h3 class="card-title">快速出金娛樂城推薦：15分鐘內到帳實測</h3>\n                        <p class="card-excerpt">實測各平台出金速度，整理最快到帳的優質平台...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# deposit-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #00d4aa; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">入金教學</span>\n                    <h3><a href="/articles/deposit-guide">娛樂城儲值教學：安全入金方式比較</a></h3>\n                    <p>銀行轉帳、超商繳款、USDT虛擬貨幣各種方式優缺點...</p>\n                    <a href="/articles/deposit-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/deposit-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/deposit-guide-cover.webp" alt="娛樂城儲值教學" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">入金教學</span>\n                        </div>\n                        <h3 class="card-title">娛樂城儲值教學：安全入金方式比較</h3>\n                        <p class="card-excerpt">銀行轉帳、超商繳款、USDT虛擬貨幣各種方式優缺點...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# baccarat-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #f39c12; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">遊戲攻略</span>\n                    <h3><a href="/articles/baccarat-guide">百家樂完整攻略：規則、牌路與下注策略</a></h3>\n                    <p>從基礎規則到進階牌路分析，提升勝率的完整教學...</p>\n                    <a href="/articles/baccarat-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/baccarat-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/baccarat-guide-cover.webp" alt="百家樂完整攻略" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge hot">遊戲攻略</span>\n                        </div>\n                        <h3 class="card-title">百家樂完整攻略：規則、牌路與下注策略</h3>\n                        <p class="card-excerpt">從基礎規則到進階牌路分析，提升勝率的完整教學...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# slots-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #f39c12; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">遊戲攻略</span>\n                    <h3><a href="/articles/slots-guide">老虎機攻略：RTP、波動度與選台技巧</a></h3>\n                    <p>看懂老虎機核心機制，選對台子提高中獎機率...</p>\n                    <a href="/articles/slots-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/slots-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/slots-guide-cover.webp" alt="老虎機攻略" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge hot">遊戲攻略</span>\n                        </div>\n                        <h3 class="card-title">老虎機攻略：RTP、波動度與選台技巧</h3>\n                        <p class="card-excerpt">看懂老虎機核心機制，選對台子提高中獎機率...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# sports-betting-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #f39c12; color: #000; padding: 3px 10px; border-radius: 4px; font-size: 12px;">遊戲攻略</span>\n                    <h3><a href="/articles/sports-betting-guide">體育投注完整教學：賠率計算與投注策略</a></h3>\n                    <p>足球、籃球、棒球各種玩法與賠率解讀...</p>\n                    <a href="/articles/sports-betting-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/sports-betting-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/sports-betting-guide-cover.webp" alt="體育投注完整教學" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge hot">遊戲攻略</span>\n                        </div>\n                        <h3 class="card-title">體育投注完整教學：賠率計算與投注策略</h3>\n                        <p class="card-excerpt">足球、籃球、棒球各種玩法與賠率解讀...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-bonus-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #9b59b6; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">優惠教學</span>\n                    <h3><a href="/articles/casino-bonus-guide">娛樂城優惠攻略：返水、體驗金與首儲怎麼領</a></h3>\n                    <p>各種優惠活動的比較與領取注意事項...</p>\n                    <a href="/articles/casino-bonus-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-bonus-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/casino-bonus-guide-cover.webp" alt="娛樂城優惠攻略" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge promo">優惠教學</span>\n                        </div>\n                        <h3 class="card-title">娛樂城優惠攻略：返水、體驗金與首儲怎麼領</h3>\n                        <p class="card-excerpt">各種優惠活動的比較與領取注意事項...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# vip-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #9b59b6; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">優惠教學</span>\n                    <h3><a href="/articles/vip-guide">娛樂城VIP制度解析：等級福利與晉升條件</a></h3>\n                    <p>各平台VIP制度比較，如何最大化專屬福利...</p>\n                    <a href="/articles/vip-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/vip-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/vip-guide-cover.webp" alt="娛樂城VIP制度解析" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge promo">優惠教學</span>\n                        </div>\n                        <h3 class="card-title">娛樂城VIP制度解析：等級福利與晉升條件</h3>\n                        <p class="card-excerpt">各平台VIP制度比較，如何最大化專屬福利...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-registration-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #3498db; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">新手入門</span>\n                    <h3><a href="/articles/casino-registration-guide">娛樂城註冊教學：新手開戶完整流程</a></h3>\n                    <p>從選平台到驗證身分，第一次註冊的完整步驟...</p>\n                    <a href="/articles/casino-registration-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-registration-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/casino-registration-guide-cover.webp" alt="娛樂城註冊教學" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">新手入門</span>\n                        </div>\n                        <h3 class="card-title">娛樂城註冊教學：新手開戶完整流程</h3>\n                        <p class="card-excerpt">從選平台到驗證身分，第一次註冊的完整步驟...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# mobile-casino-guide (no cover - use baccarat-chips fallback)
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #3498db; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">新手入門</span>\n                    <h3><a href="/articles/mobile-casino-guide">手機娛樂城推薦：APP與網頁版實測比較</a></h3>\n                    <p>iOS與Android實測，哪個平台手機體驗最好...</p>\n                    <a href="/articles/mobile-casino-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/mobile-casino-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/baccarat-chips.webp" alt="手機娛樂城推薦" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">新手入門</span>\n                        </div>\n                        <h3 class="card-title">手機娛樂城推薦：APP與網頁版實測比較</h3>\n                        <p class="card-excerpt">iOS與Android實測，哪個平台手機體驗最好...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# newbie-friendly
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #3498db; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">新手入門</span>\n                    <h3><a href="/articles/newbie-friendly">新手友善娛樂城推薦：低門檻平台比較</a></h3>\n                    <p>首儲低、操作簡單、客服回應快的平台整理...</p>\n                    <a href="/articles/newbie-friendly" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/newbie-friendly" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/newbie-friendly-cover.webp" alt="新手友善娛樂城推薦" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge guide">新手入門</span>\n                        </div>\n                        <h3 class="card-title">新手友善娛樂城推薦：低門檻平台比較</h3>\n                        <p class="card-excerpt">首儲低、操作簡單、客服回應快的平台整理...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-ptt-discussion (no cover - use baccarat-chips fallback)
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #e74c3c; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">熱門話題</span>\n                    <h3><a href="/articles/casino-ptt-discussion">PTT娛樂城討論整理：網友真實評價與推薦</a></h3>\n                    <p>整理PTT八卦版與博弈版的熱門討論與玩家心得...</p>\n                    <a href="/articles/casino-ptt-discussion" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-ptt-discussion" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/baccarat-chips.webp" alt="PTT娛樂城討論整理" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge review">熱門話題</span>\n                        </div>\n                        <h3 class="card-title">PTT娛樂城討論整理：網友真實評價與推薦</h3>\n                        <p class="card-excerpt">整理PTT八卦版與博弈版的熱門討論與玩家心得...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# casino-dcard-2026
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #e74c3c; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">熱門話題</span>\n                    <h3><a href="/articles/casino-dcard-2026">Dcard娛樂城討論：2026年網友真實經驗分享</a></h3>\n                    <p>整理Dcard上的娛樂城心得、抱怨與推薦...</p>\n                    <a href="/articles/casino-dcard-2026" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/casino-dcard-2026" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/casino-dcard-2026-cover.webp" alt="Dcard娛樂城討論" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge review">熱門話題</span>\n                        </div>\n                        <h3 class="card-title">Dcard娛樂城討論：2026年網友真實經驗分享</h3>\n                        <p class="card-excerpt">整理Dcard上的娛樂城心得、抱怨與推薦...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# usdt-casino
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #e74c3c; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">熱門話題</span>\n                    <h3><a href="/articles/usdt-casino">USDT娛樂城教學：虛擬貨幣儲值與出金攻略</a></h3>\n                    <p>泰達幣儲值的好處、風險與操作教學...</p>\n                    <a href="/articles/usdt-casino" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/usdt-casino" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/usdt-casino-cover.webp" alt="USDT娛樂城教學" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge review">熱門話題</span>\n                        </div>\n                        <h3 class="card-title">USDT娛樂城教學：虛擬貨幣儲值與出金攻略</h3>\n                        <p class="card-excerpt">泰達幣儲值的好處、風險與操作教學...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

# world-cup-2026-guide
content = content.replace(
    '<article class="article-card">\n                    <span class="article-tag" style="background: #e74c3c; color: #fff; padding: 3px 10px; border-radius: 4px; font-size: 12px;">熱門話題</span>\n                    <h3><a href="/articles/world-cup-2026-guide">2026世界盃投注攻略：賽程、賠率與玩法</a></h3>\n                    <p>世界盃賽制、熱門球隊與投注技巧一次看...</p>\n                    <a href="/articles/world-cup-2026-guide" class="read-more">閱讀全文 →</a>\n                </article>',
    '<a href="/articles/world-cup-2026-guide" class="article-card">\n                    <div class="card-image">\n                        <img src="/static/images/articles/tech/world-cup-2026-guide-cover.webp" alt="2026世界盃投注攻略" loading="lazy">\n                    </div>\n                    <div class="card-content">\n                        <div class="card-meta">\n                            <span class="card-badge review">熱門話題</span>\n                        </div>\n                        <h3 class="card-title">2026世界盃投注攻略：賽程、賠率與玩法</h3>\n                        <p class="card-excerpt">世界盃賽制、熱門球隊與投注技巧一次看...</p>\n                        <span class="card-readmore">閱讀全文 →</span>\n                    </div>\n                </a>'
)

with open('/root/.openclaw/workspace/fun1399-clean/index.html', 'w') as f:
    f.write(content)

print(f"Updated index.html: {len(content)} bytes")
print("Changes made:")
print("1. Section spacing added")
print("2. Scam section background changed to light")
print("3. Popular Guides now use real cover images")
print("4. Featured Navigation converted to image cards")
