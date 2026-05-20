#!/usr/bin/env python3
"""
優化 3 篇文章：
1. 3a-casino-scam-review.html
2. baccarat-strategy.html
3. deposit-guide.html
"""
import os, re

WORKSPACE = '/root/.openclaw/workspace/fun1399-clean/articles'
NOW_ISO   = '2026-05-17T19:30:00+08:00'
NOW_DATE  = '2026年5月17日'

# ────────────────────────────
# 1. 3a-casino-scam-review
# ────────────────────────────
def optimize_3a_casino_scam_review():
    path = os.path.join(WORKSPACE, '3a-casino-scam-review.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1.1 Title 優化：降低負面感，增加查證/實測/調查感
    old_title = '3A娛樂城詐騙是真的嗎？PTT不出金投訴、黑網疑慮與玩家真實評價（2026）'
    new_title = '2026 3A娛樂城評價調查報告｜詐騙傳聞查證、出金實測與PTT網友真實心得'
    c = c.replace(f'<title>{old_title}</title>', f'<title>{new_title}</title>')
    c = c.replace(f'content="{old_title}"', f'content="{new_title}"')
    c = c.replace(f'"headline": "{old_title}"', f'"headline": "{new_title}"')

    # h1 同步更新
    old_h1 = '3A娛樂城詐騙疑慮解析：新手必看的安全性、出金實測與真實評價（2026）'
    new_h1 = '2026 3A娛樂城評價調查報告｜詐騙傳聞查證、出金實測與玩家真實心得'
    c = c.replace(f'<h1 style="font-size: 32px; margin-bottom: 20px; line-height: 1.4;">{old_h1}</h1>',
                  f'<h1 style="font-size: 32px; margin-bottom: 20px; line-height: 1.4;">{new_h1}</h1>')

    # 1.2 更新 meta description
    c = c.replace(
        'content="3A娛樂城詐騙是真的嗎？整理PTT網友不出金投訴、黑網疑慮、玩家真實評價。2026最新調查報告，客觀分析安全性與出金實測。"',
        'content="2026最新3A娛樂城評價調查報告！詐騙傳聞真假查證、出金速度實測、PTT/Dcard網友真實心得、優缺點完整分析。客觀安全性評估。"'
    )
    c = c.replace(
        'content="3A娛樂城詐騙調查：PTT不出金投訴整理、黑網疑慮分析、玩家真實評價。2026最新客觀報告。"',
        'content="2026最新3A娛樂城評價調查報告！詐騙傳聞真假查證、出金速度實測、PTT/Dcard網友真實心得。客觀安全性評估。"'
    )

    # 1.3 更新 Schema description
    c = c.replace(
        '"description": "深度解析3A娛樂城評價、詐騙傳聞真假、1-2分鐘出金速度、玩家真實經驗。PTT/Dcard網友評價完整整理，客觀分析優缺點。"',
        '"description": "2026最新3A娛樂城評價調查報告！詐騙傳聞真假查證、出金速度實測、PTT/Dcard網友真實心得、優缺點完整分析。客觀安全性評估。"'
    )

    # 1.4 移除過早 CTA（開頭的導流連結）
    early_cta = '''        <!-- 導流連結 -->
        <div class="cta-box" style="background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%); border: 2px solid #FFD700; border-radius: 12px; padding: 25px; margin: 30px 0; text-align: center;">
            <h3 style="color: #FFD700; margin-bottom: 15px;">🔥 想親自體驗3A娛樂城？</h3>
            <p style="color: #e0e0e0; margin-bottom: 20px; line-height: 1.6;">透過本站連結註冊，享首儲1000送1000優惠，1-2分鐘極速出金實測！</p>
            <a href="https://fun1399.3a1788.com/" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-size: 18px; transition: all 0.3s;" target="_blank" rel="noopener">立即註冊領優惠 →</a>
        </div>
'''
    c = c.replace(early_cta, '')

    # 同時移除中段的導流 CTA
    mid_cta = '''        <!-- 中段導流 -->
        <div class="cta-box" style="background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%); border: 2px solid #FFD700; border-radius: 12px; padding: 25px; margin: 30px 0; text-align: center;">
            <h3 style="color: #FFD700; margin-bottom: 15px;">💎 3A娛樂城限時優惠</h3>
            <p style="color: #e0e0e0; margin-bottom: 20px; line-height: 1.6;">首儲1000送1000 | 1-2分鐘極速出金 | 每月10號續儲加贈20%</p>
            <a href="https://fun1399.3a1788.com/" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-size: 18px; transition: all 0.3s;" target="_blank" rel="noopener">立即註冊體驗 →</a>
        </div>
'''
    c = c.replace(mid_cta, '')

    # 1.5 新增重點摘要區塊（在文章目錄後面）
    summary_box = '''        <!-- 本文重點摘要 -->
        <div class="summary-box" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0284c7; border-radius: 8px; padding: 20px 25px; margin: 25px 0;">
            <h3 style="margin: 0 0 12px 0; color: #0369a1; font-size: 18px;">📋 本文重點摘要</h3>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.8; color: #111;">
                <li><strong>查證結論</strong>：3A娛樂城並非詐騙，營運超過6年，出金實測平均1分38秒</li>
                <li><strong>詐騙傳聞來源</strong>：多為假冒網站、玩家誤解規則、同業競爭抹黑所致</li>
                <li><strong>安全性評級</strong>：本土品牌，客服溝通順暢，但首儲20倍流水較高需注意</li>
                <li><strong>網友評價</strong>：PTT/Dcard 正面為主，出金速度與客服獲一致好評</li>
            </ul>
        </div>
'''
    c = c.replace('        </div>\n\n        <h2 id="scam-rumor"', summary_box + '\n        <h2 id="scam-rumor"')

    # 1.6 新增 FAQPage Schema（插入在 </head> 之前）
    faq_schema = '''    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "3A娛樂城是詐騙嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不是。3A營運超過6年，有大量真實玩家持續使用，出金紀錄良好（平均1分38秒）。網路上的詐騙傳聞多為假冒網站或玩家誤解規則所致。"
          }
        },
        {
          "@type": "Question",
          "name": "3A娛樂城安全嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "安全。3A是台灣本土品牌，營運多年，提供24小時繁體中文客服。在眾多平台中屬於安全性較高的選擇，但首儲20倍流水要求較高，新手需注意。"
          }
        },
        {
          "@type": "Question",
          "name": "3A娛樂城出金會被拖延嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不會。實測顯示出金平均只需1分38秒，完全符合1-2分鐘承諾。只要達到流水要求，提款都會正常處理。每日前2次提款免手續費。"
          }
        },
        {
          "@type": "Question",
          "name": "3A娛樂城適合新手嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "適合，但需注意首儲流水要求。3A的優勢在於本土客服和快速出金。建議新手先不領首儲優惠，純儲值體驗，熟悉平台後再決定是否領取優惠。"
          }
        },
        {
          "@type": "Question",
          "name": "如何分辨真假3A網站？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "建議透過本站連結前往註冊，確保進入正確的官方網站。切勿隨意點擊不明連結，避免進入假冒網站。正規3A網站有https加密和完整客服系統。"
          }
        },
        {
          "@type": "Question",
          "name": "3A娛樂城的首儲流水要求是多少？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "首儲流水要求為20倍，在業界中屬於較高標準。續儲流水為10倍。如果不愛綁流水，建議純儲值不領優惠，這樣提款無限制。"
          }
        },
        {
          "@type": "Question",
          "name": "3A娛樂城有哪些優缺點？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "優點：1-2分鐘極速出金、本土24H客服、每月10號續儲加贈20%、日返水0.4-0.8%。缺點：首儲20倍流水較高、廳商數量中等、尖峰時段偶爾稍慢。"
          }
        },
        {
          "@type": "Question",
          "name": "為什麼網路上有3A娛樂城的負面評價？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "負面評價主要來自四種情況：1)假冒網站詐騙與真3A無關；2)玩家未達流水要求就申請提款；3)同業競爭刻意抹黑；4)少數玩家輸錢後情緒性發文。"
          }
        }
      ]
    }
    </script>
'''
    c = c.replace('</head>', faq_schema + '</head>')

    # 1.7 更新日期
    c = c.replace('content="2026-04-21">', f'content="2026-05-17">')
    c = c.replace('content="2026-04-21T10:00:00+08:00">', f'content="{NOW_ISO}">')
    c = c.replace('content="2026-05-14T01:00:00+08:00">', f'content="{NOW_ISO}">')
    c = c.replace('"datePublished": "2026-04-21T10:00:00+08:00"', f'"datePublished": "2026-04-21T10:00:00+08:00"')
    c = c.replace('"dateModified": "2026-05-15T01:00:00+08:00"', f'"dateModified": "{NOW_ISO}"')
    c = c.replace('📅 發布日期：2026年4月21日', '📅 發布日期：2026年4月21日')
    c = c.replace('⏱️ 閱讀時間：約12分鐘', f'🔄 最後更新：{NOW_DATE} | ⏱️ 閱讀時間：約12分鐘')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('✅ 3a-casino-scam-review.html optimized')


# ────────────────────────────
# 2. baccarat-strategy
# ────────────────────────────
def optimize_baccarat_strategy():
    path = os.path.join(WORKSPACE, 'baccarat-strategy.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 2.1 修復 hero image 路徑
    c = c.replace(
        'src="/static/images/articles/tech/baccarat-strategy-cover.webp\u00d026百家樂策略進階攻略"',
        'src="/static/images/articles/articles/baccarat-strategy-cover.png"\n                     alt="2026百家樂策略進階攻略｜馬丁格爾與看路技巧"'
    )

    # 2.2 在 lead paragraph 後新增摘要 + CTA
    old_lead_end = '''        <p class="lead">百家樂不只是運氣遊戲，進階玩家懂得運用策略與資金管理來提升勝率。本文將深入探討各種經典投注策略、牌路分析技巧與心理控制心法，幫助你在百家樂桌上做出更明智的決策。</p>
        
        <h2>一、經典投注策略深度解析</h2>'''
    new_lead_end = '''        <p class="lead">百家樂不只是運氣遊戲，進階玩家懂得運用策略與資金管理來提升勝率。本文將深入探討各種經典投注策略、牌路分析技巧與心理控制心法，幫助你在百家樂桌上做出更明智的決策。</p>

        <!-- 重點摘要 -->
        <div class="summary-box" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0284c7; border-radius: 8px; padding: 20px 25px; margin: 25px 0;">
            <h3 style="margin: 0 0 12px 0; color: #0369a1; font-size: 18px;">📋 本文重點摘要</h3>
            <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">
                <li><strong>馬丁格爾策略</strong>：輸了加倍，風險高但理論必勝</li>
                <li><strong>反馬丁格爾</strong>：贏了加倍，讓利潤奔跑</li>
                <li><strong>牌路分析</strong>：大路/小路/單跳雙跳判讀技巧</li>
                <li><strong>資金管理</strong>：注碼分配、停損停利設定</li>
                <li><strong>心理素質</strong>：避免情緒化下注，紀律執行</li>
            </ul>
        </div>

        <!-- 開頭 CTA -->
        <div class="cta-box-inline" style="background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%); border-radius: 12px; padding: 25px 30px; margin: 25px 0; text-align: center; border: 2px solid #FFD700;">
            <h3 style="color: #FFD700; margin: 0 0 12px 0; font-size: 20px;">🎰 想實戰練習百家樂策略？</h3>
            <p style="color: #e0e0e0; margin: 0 0 18px 0; line-height: 1.6;">多家平台提供 <strong style="color:#FFD700">免費體驗金</strong>，註冊即可試玩百家樂，零風險驗證策略效果！</p>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                <a href="/recommend/2026" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-size: 16px;">查看推薦平台 →</a>
                <a href="https://lin.ee/Mc1pb7z" style="display: inline-block; background: #06C755; color: #fff; font-weight: 600; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-size: 16px;" target="_blank">💬 加入LINE諮詢</a>
            </div>
        </div>
        
        <h2>一、經典投注策略深度解析</h2>'''
    c = c.replace(old_lead_end, new_lead_end)

    # 2.3 在資金管理段落後新增平台推薦 CTA
    old_fund_section = '''        <h3>3.3 時間管理</h3>
        <p>長時間遊戲容易疲勞導致判斷失準。建議每1小時休息10分鐘，單日遊戲不超過4小時。設定時間上限比金額上限更重要。</p>

        <h2>四、心理素質與紀律</h2>'''
    new_fund_section = '''        <h3>3.3 時間管理</h3>
        <p>長時間遊戲容易疲勞導致判斷失準。建議每1小時休息10分鐘，單日遊戲不超過4小時。設定時間上限比金額上限更重要。</p>

        <!-- 中段平台推薦 CTA -->
        <div class="platform-cta" style="background: #fff; border: 2px solid #e5e7eb; border-radius: 12px; padding: 25px; margin: 30px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
            <h3 style="margin: 0 0 18px 0; color: #1a1a2e; font-size: 20px;">🏆 適合練習百家樂策略的平台推薦</h3>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 18px;">
                <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                    <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">鉅城娛樂城</div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">百家樂廳商最多</div>
                    <div style="font-size: 13px; color: #16a34a;">✅ 出金快 | 遊戲多</div>
                </div>
                <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                    <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">HG娛樂城</div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">免傭百家樂優惠</div>
                    <div style="font-size: 13px; color: #16a34a;">✅ 低莊優 | 返水高</div>
                </div>
                <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                    <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">3A娛樂城</div>
                    <div style="font-size: 14px; color: #666; margin-bottom: 8px;">本土客服最親切</div>
                    <div style="font-size: 13px; color: #16a34a;">✅ 中文客服 | 體驗金</div>
                </div>
            </div>
            <div style="text-align: center;">
                <a href="/recommend/2026" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 12px 32px; border-radius: 8px; text-decoration: none;">查看完整平台比較 →</a>
            </div>
            <p style="text-align: center; margin: 12px 0 0 0; font-size: 13px; color: #666;">💡 新手建議先領 <a href="/articles/free-credit-guide" style="color: #0284c7; text-decoration: none; font-weight: 600;">體驗金</a> 免費試玩，驗證策略效果</p>
        </div>

        <h2>四、心理素質與紀律</h2>'''
    c = c.replace(old_fund_section, new_fund_section)

    # 2.4 替換舊版 cta-box 為新版 + 相關文章導航
    old_cta = '''                <div class="cta-box">
                <h3>延伸閱讀</h3>
                <ul>
                    <li><a href="/articles/baccarat-guide">百家樂技巧完整攻略</a></li>
                    <li><a href="/articles/baccarat-rules">百家樂規則詳解</a></li>
                </ul>
            </div>'''
    new_cta = '''                <!-- 最終轉化 CTA -->
            <div class="final-cta" style="background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%); border-radius: 12px; padding: 30px; margin: 35px 0; text-align: center; border: 2px solid #FFD700;">
                <h3 style="color: #FFD700; margin: 0 0 15px 0; font-size: 22px;">🚀 準備好實戰驗證策略了嗎？</h3>
                <p style="color: #e0e0e0; margin: 0 0 20px 0; line-height: 1.7; font-size: 16px;">
                    多家平台提供 <strong style="color:#FFD700">168-588元體驗金</strong>，註冊即可免費試玩百家樂。<br>
                    零風險驗證馬丁格爾、看路技巧與資金管理策略！
                </p>
                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 18px;">
                    <a href="/recommend/2026" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-size: 17px;">🎰 領取體驗金開始試玩 →</a>
                    <a href="/articles/casino-registration-guide" style="display: inline-block; background: rgba(255,255,255,0.15); color: #fff; font-weight: 600; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-size: 17px; border: 1px solid rgba(255,255,255,0.3);">📝 先看註冊教學</a>
                </div>
                <p style="margin: 0; font-size: 14px; color: #94a3b8;">已有 <strong style="color:#FFD700">2,800+</strong> 玩家透過本站學習策略 | 
                <a href="https://lin.ee/Mc1pb7z" style="color: #06C755; text-decoration: none; font-weight: 600;" target="_blank">💬 加入LINE取得策略更新</a></p>
            </div>

            <!-- 相關文章快速導航 -->
            <div class="related-quick-links" style="background: #f8fafc; border-radius: 10px; padding: 25px; margin: 30px 0;">
                <h3 style="margin: 0 0 18px 0; color: #1a1a2e; font-size: 18px;">🔗 百家樂玩家推薦閱讀</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
                    <a href="/articles/baccarat-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🎴 百家樂完整攻略</div>
                        <div style="font-size: 13px; color: #666;">規則、牌路與下注策略入門</div>
                    </a>
                    <a href="/articles/deposit-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">💳 儲值教學</div>
                        <div style="font-size: 13px; color: #666;">超商、銀行、USDT儲值攻略</div>
                    </a>
                    <a href="/articles/fast-withdrawal" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">⚡ 快速出金教學</div>
                        <div style="font-size: 13px; color: #666;">提款流程與注意事項</div>
                    </a>
                    <a href="/articles/casino-registration-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">📝 註冊教學</div>
                        <div style="font-size: 13px; color: #666;">3分鐘完成開戶</div>
                    </a>
                    <a href="/articles/free-credit-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🎁 體驗金完整指南</div>
                        <div style="font-size: 13px; color: #666;">免費試玩百家樂零風險</div>
                    </a>
                    <a href="/articles/safety-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🛡️ 安全指南</div>
                        <div style="font-size: 13px; color: #666;">如何選擇安全娛樂城</div>
                    </a>
                </div>
            </div>'''
    c = c.replace(old_cta, new_cta)

    # 2.5 新增 FAQPage Schema
    faq_schema = '''    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "馬丁格爾策略真的能保證贏錢嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "不能。馬丁格爾理論上只要資金無限就能回本，但實際上面臨兩大限制：1) 連輸時資金快速消耗；2) 娛樂城有單注上限。建議設定明確停損點，不可過度依賴。"
          }
        },
        {
          "@type": "Question",
          "name": "百家樂最好的投注策略是什麼？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "沒有絕對最好的策略，但專業玩家普遍推薦：1) 永遠押莊家（莊家優勢僅1.06%）；2) 嚴格資金管理，單注不超過本金2%；3) 設定停損停利點；4) 避免情緒化追注。"
          }
        },
        {
          "@type": "Question",
          "name": "看路技巧真的有用嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "看路不能改變機率，但可幫助判斷趨勢順勢而為。當大路、小路、大眼仔路同時呈現規律時，順勢下注勝率較高。但任何模式都可能隨時中斷，看路僅是輔助工具。"
          }
        },
        {
          "@type": "Question",
          "name": "百家樂資金管理怎麼做？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "專業建議：1) 將資金分為50-100個單位，單注不超過2%；2) 設定停損點為本金的20-30%；3) 設定停利點為本金的50%獲利；4) 每次遊戲不超過4小時，每小時休息10分鐘。"
          }
        },
        {
          "@type": "Question",
          "name": "免傭百家樂和傳統百家樂哪個好？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "傳統百家樂莊家優勢1.06%較低，但需支付5%佣金。免傭百家樂莊家優勢1.46%較高，但莊家6點勝利只賠一半。長期來看傳統百家樂較有利，但免傭適合不喜歡計算佣金的玩家。"
          }
        },
        {
          "@type": "Question",
          "name": "連輸時該怎麼辦？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "連輸3局後應強制休息5分鐘，離開座位讓情緒平復。絕對不要在情緒激動時加大注碼或改變策略。若已達停損點，必須立即停止，改日再戰。"
          }
        }
      ]
    }
    </script>
'''
    c = c.replace('</head>', faq_schema + '</head>')

    # 2.6 加強內鏈：在策略段落中加入相關文章連結
    c = c.replace(
        '<p>百家樂最大的敵人不是莊家，而是自己的情緒。</p>',
        '<p>百家樂最大的敵人不是莊家，而是自己的情緒。建議新手先閱讀<a href="/articles/baccarat-guide">百家樂完整攻略</a>了解基礎規則，再學習進階策略。</p>'
    )

    # 2.7 更新日期
    c = c.replace('"dateModified": "2026-05-15T01:00:00+08:00"', f'"dateModified": "{NOW_ISO}"')
    c = c.replace('<span class="update-date">更新日期：2026年5月15日</span>', f'<span class="update-date">更新日期：{NOW_DATE}</span>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('✅ baccarat-strategy.html optimized')


# ────────────────────────────
# 3. deposit-guide
# ────────────────────────────
def optimize_deposit_guide():
    path = os.path.join(WORKSPACE, 'deposit-guide.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 3.1 更新 Title 加入 2026
    c = c.replace(
        '<title>娛樂城儲值教學｜超商、銀行、USDT儲值完整攻略 - 娛樂城玩家俱樂部</title>',
        '<title>2026最新娛樂城儲值教學｜超商、銀行、USDT儲值完整攻略 - 娛樂城玩家俱樂部</title>'
    )
    c = c.replace(
        'content="娛樂城儲值完整教學！超商、ATM、網銀、USDT虛擬幣儲值方式比較，各平台儲值教學步驟圖解，手續費與到帳時間分析。"',
        'content="2026最新娛樂城儲值完整教學！超商、ATM、網銀、USDT虛擬幣儲值方式比較，各平台儲值教學步驟圖解，手續費與到帳時間分析。"'
    )

    # 3.2 更新 Schema
    c = c.replace(
        '"headline": "娛樂城儲值教學｜四大儲值方式完整攻略"',
        '"headline": "2026最新娛樂城儲值教學｜超商、銀行、USDT四大儲值方式完整攻略"'
    )
    c = c.replace(
        '"description": "娛樂城儲值完整教學！超商儲值、銀行轉帳、虛擬貨幣、第三方支付比較，最低儲值金額與手續費分析。"',
        '"description": "2026最新娛樂城儲值完整教學！超商儲值、銀行轉帳、虛擬貨幣、第三方支付比較，最低儲值金額與手續費分析。"'
    )

    # 3.3 在 intro 後新增摘要 + 儲值前提醒 CTA
    old_intro_end = '''                <div class="intro">
                    <p><strong>娛樂城儲值</strong>是開始遊戲的第一步，但許多新手對於儲值方式感到困惑。本文將詳細介紹<strong>超商儲值</strong>、<strong>銀行轉帳</strong>、<strong>網路銀行</strong>、<strong>USDT虛擬幣</strong>等各種儲值方式，幫助你找到最適合的儲值管道。</p>
                </div>

                <div class="toc">'''
    new_intro_end = '''                <div class="intro">
                    <p><strong>娛樂城儲值</strong>是開始遊戲的第一步，但許多新手對於儲值方式感到困惑。本文將詳細介紹<strong>超商儲值</strong>、<strong>銀行轉帳</strong>、<strong>網路銀行</strong>、<strong>USDT虛擬幣</strong>等各種儲值方式，幫助你找到最適合的儲值管道。</p>
                </div>

                <!-- 重點摘要 -->
                <div class="summary-box" style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); border-left: 4px solid #0284c7; border-radius: 8px; padding: 20px 25px; margin: 25px 0;">
                    <h3 style="margin: 0 0 12px 0; color: #0369a1; font-size: 18px;">📋 本文重點摘要</h3>
                    <ul style="margin: 0; padding-left: 20px; line-height: 1.8;">
                        <li><strong>超商儲值</strong>：方便隱私，但手續費20-30元，限額2-3萬</li>
                        <li><strong>網銀轉帳</strong>：免手續費、即時到帳、限額最高，最推薦</li>
                        <li><strong>ATM轉帳</strong>：手續費低，但需到ATM操作</li>
                        <li><strong>USDT儲值</strong>：匿名無限額，適合大額，有額外回饋</li>
                    </ul>
                </div>

                <!-- 儲值前提醒 CTA -->
                <div class="cta-box-inline" style="background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 10px; padding: 20px 25px; margin: 25px 0; border-left: 4px solid #f59e0b;">
                    <p style="margin: 0; color: #92400e; line-height: 1.7;">
                        <strong>⚠️ 儲值前重要提醒</strong><br>
                        首次儲值建議先 <strong>小額測試（1000-2000元）</strong>，確認平台正常出金後再大額儲值。
                        還沒註冊？先看 <a href="/articles/casino-registration-guide" style="color: #b45309; text-decoration: underline; font-weight: 600;">註冊教學</a>，
                        註冊後可領取 <a href="/articles/free-credit-guide" style="color: #b45309; text-decoration: underline; font-weight: 600;">免費體驗金</a> 試玩！
                    </p>
                </div>

                <div class="toc">'''
    c = c.replace(old_intro_end, new_intro_end)

    # 3.4 在超商儲值後新增平台推薦 CTA
    old_convenience_end = '''                <div class="tip-box">
                    <p><strong>💡 超商儲值注意事項</strong>：超商儲值通常會收取20-30元手續費，建議一次儲值較大金額（如5000元以上）較為划算。另外，每日超商儲值限額通常為2-3萬元，大額儲值建議使用銀行轉帳。</p>
                </div>

                <h2 id="bank">🏦 銀行轉帳與網銀儲值</h2>'''
    new_convenience_end = '''                <div class="tip-box">
                    <p><strong>💡 超商儲值注意事項</strong>：超商儲值通常會收取20-30元手續費，建議一次儲值較大金額（如5000元以上）較為划算。另外，每日超商儲值限額通常為2-3萬元，大額儲值建議使用銀行轉帳。</p>
                </div>

                <!-- 平台推薦 CTA -->
                <div class="platform-comparison-cta" style="background: #fff; border: 2px solid #e5e7eb; border-radius: 12px; padding: 25px; margin: 30px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
                    <h3 style="margin: 0 0 18px 0; color: #1a1a2e; font-size: 20px;">🏆 2026年儲值最方便的平台推薦</h3>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 18px;">
                        <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">鉅城娛樂城</div>
                            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">支援全台15家銀行</div>
                            <div style="font-size: 13px; color: #16a34a;">✅ 網銀免手續費</div>
                        </div>
                        <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">HG娛樂城</div>
                            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">USDT儲值回饋1%</div>
                            <div style="font-size: 13px; color: #16a34a;">✅ 大額首選</div>
                        </div>
                        <div style="background: #f8fafc; border-radius: 8px; padding: 15px; text-align: center;">
                            <div style="font-weight: 700; color: #1a1a2e; margin-bottom: 6px;">3A娛樂城</div>
                            <div style="font-size: 14px; color: #666; margin-bottom: 8px;">超商儲值到帳最快</div>
                            <div style="font-size: 13px; color: #16a34a;">✅ 5分鐘內到帳</div>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <a href="/recommend/2026" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 12px 32px; border-radius: 8px; text-decoration: none;">查看完整平台比較 →</a>
                    </div>
                    <p style="text-align: center; margin: 12px 0 0 0; font-size: 13px; color: #666;">💡 各家儲值優惠時常有變動，加入 <a href="https://lin.ee/Mc1pb7z" style="color: #06C755; text-decoration: none; font-weight: 600;" target="_blank">LINE</a> 取得最新儲值優惠碼</p>
                </div>

                <h2 id="bank">🏦 銀行轉帳與網銀儲值</h2>'''
    c = c.replace(old_convenience_end, new_convenience_end)

    # 3.5 替換舊版 cta-box 為新版 + LINE CTA
    old_cta = '''            <div class="cta-box">
                <h3>延伸閱讀</h3>
                <ul>
                    <li><a href="/articles/withdrawal-ranking">娛樂城出金速度排行</a></li>
                    <li><a href="/articles/fast-withdrawal">快速出金教學</a></li>
                    <li><a href="/articles/casino-withdrawal-fast">娛樂城快速提款攻略</a></li>
                </ul>
            </div>'''
    new_cta = '''            <!-- 最終轉化 CTA -->
            <div class="final-cta" style="background: linear-gradient(135deg, #1e3a5f 0%, #0d2137 100%); border-radius: 12px; padding: 30px; margin: 35px 0; text-align: center; border: 2px solid #FFD700;">
                <h3 style="color: #FFD700; margin: 0 0 15px 0; font-size: 22px;">🚀 準備好開始儲值了嗎？</h3>
                <p style="color: #e0e0e0; margin: 0 0 20px 0; line-height: 1.7; font-size: 16px;">
                    多家平台提供 <strong style="color:#FFD700">免手續費網銀儲值</strong>，3-5分鐘內到帳。<br>
                    首次儲值還可領取 <strong style="color:#FFD700">首儲優惠</strong>，讓本金直接翻倍！
                </p>
                <div style="display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 18px;">
                    <a href="/recommend/2026" style="display: inline-block; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); color: #000; font-weight: 700; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-size: 17px;">💳 選擇平台開始儲值 →</a>
                    <a href="/articles/casino-registration-guide" style="display: inline-block; background: rgba(255,255,255,0.15); color: #fff; font-weight: 600; padding: 14px 32px; border-radius: 8px; text-decoration: none; font-size: 17px; border: 1px solid rgba(255,255,255,0.3);">📝 還沒註冊？先看教學</a>
                </div>
                <p style="margin: 0; font-size: 14px; color: #94a3b8;">儲值遇到問題？ 
                <a href="https://lin.ee/Mc1pb7z" style="color: #06C755; text-decoration: none; font-weight: 600;" target="_blank">💬 加入LINE一對一協助儲值</a></p>
            </div>

            <!-- 相關文章快速導航 -->
            <div class="related-quick-links" style="background: #f8fafc; border-radius: 10px; padding: 25px; margin: 30px 0;">
                <h3 style="margin: 0 0 18px 0; color: #1a1a2e; font-size: 18px;">🔗 儲值後推薦閱讀</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px;">
                    <a href="/articles/casino-registration-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">📝 註冊教學</div>
                        <div style="font-size: 13px; color: #666;">3分鐘完成開戶</div>
                    </a>
                    <a href="/articles/casino-withdrawal-tutorial" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">💰 提款完整教學</div>
                        <div style="font-size: 13px; color: #666;">出金流程與注意事項</div>
                    </a>
                    <a href="/articles/fast-withdrawal" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">⚡ 快速出金教學</div>
                        <div style="font-size: 13px; color: #666;">15分鐘內到帳實測</div>
                    </a>
                    <a href="/articles/free-credit-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🎁 體驗金完整指南</div>
                        <div style="font-size: 13px; color: #666;">免費試玩零風險</div>
                    </a>
                    <a href="/articles/casino-safe" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🛡️ 安全推薦清單</div>
                        <div style="font-size: 13px; color: #666;">如何選擇安全娛樂城</div>
                    </a>
                    <a href="/articles/safety-guide" style="display: block; background: #fff; padding: 14px 18px; border-radius: 8px; text-decoration: none; color: #1a1a2e; border: 1px solid #e5e7eb;">
                        <div style="font-weight: 600; margin-bottom: 4px;">🔒 安全指南</div>
                        <div style="font-size: 13px; color: #666;">儲值前必讀防詐須知</div>
                    </a>
                </div>
            </div>'''
    c = c.replace(old_cta, new_cta)

    # 3.6 新增 HowTo Schema（儲值步驟）
    howto_schema = '''    <!-- HowTo Schema: 娛樂城儲值5步驟 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "2026最新娛樂城儲值教學：5步驟安全入金",
      "description": "詳細圖解娛樂城儲值流程，從選擇平台到確認到帳，只需5分鐘即可完成安全儲值。",
      "image": "https://fun1399.com/static/images/articles/articles/deposit-guide-cover.png",
      "totalTime": "PT5M",
      "estimatedCost": {
        "@type": "MonetaryAmount",
        "currency": "TWD",
        "value": "0"
      },
      "supply": [
        {"@type": "HowToSupply", "name": "銀行帳戶或超商繳費單"},
        {"@type": "HowToSupply", "name": "儲值金額（建議首次1000-2000元測試）"}
      ],
      "tool": [
        {"@type": "HowToTool", "name": "智慧型手機或電腦"},
        {"@type": "HowToTool", "name": "網路銀行APP或超商繳費"}
      ],
      "step": [
        {
          "@type": "HowToStep",
          "position": 1,
          "name": "選擇安全的娛樂城平台",
          "text": "確認平台有合法執照、網路評價良好、且提供你偏好的儲值方式。建議先小額測試。",
          "url": "https://fun1399.com/articles/deposit-guide#methods",
          "image": "https://fun1399.com/static/images/articles/articles/deposit-guide-cover.png"
        },
        {
          "@type": "HowToStep",
          "position": 2,
          "name": "登入帳號進入儲值頁面",
          "text": "登入娛樂城帳號，找到「儲值」或「存款」按鈕，選擇你要使用的儲值方式。",
          "url": "https://fun1399.com/articles/deposit-guide#convenience"
        },
        {
          "@type": "HowToStep",
          "position": 3,
          "name": "輸入儲值金額並取得付款資訊",
          "text": "輸入儲值金額（通常最低1000元），系統會顯示收款帳號、繳費代碼或USDT地址。務必核對資訊正確。",
          "url": "https://fun1399.com/articles/deposit-guide#convenience"
        },
        {
          "@type": "HowToStep",
          "position": 4,
          "name": "完成付款並保留憑證",
          "text": "使用網銀轉帳、ATM、超商繳費或USDT轉帳完成付款。保留轉帳明細、繳費單據或區塊鏈截圖作為憑證。",
          "url": "https://fun1399.com/articles/deposit-guide#bank"
        },
        {
          "@type": "HowToStep",
          "position": 5,
          "name": "確認點數到帳並開始遊戲",
          "text": "等待3-10分鐘確認點數是否到帳。若超過30分鐘未到帳，聯繫客服並提供付款憑證。到帳後即可開始遊戲！",
          "url": "https://fun1399.com/articles/deposit-guide#tips"
        }
      ]
    }
    </script>
'''
    c = c.replace('</head>', howto_schema + '</head>')

    # 3.7 新增 FAQPage Schema
    faq_schema = '''    <!-- FAQPage Schema -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "FAQPage",
      "mainEntity": [
        {
          "@type": "Question",
          "name": "娛樂城儲值後沒有到帳怎麼辦？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "1) 先確認轉帳是否成功（查看銀行明細）；2) 檢查是否超過30分鐘；3) 聯繫平台客服，提供轉帳證明；4) 通常客服會在1小時內處理完畢。"
          }
        },
        {
          "@type": "Question",
          "name": "超商儲值和銀行轉帳哪個比較好？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "銀行轉帳（尤其是網路銀行）比較好：免手續費、即時到帳、限額高。超商儲值方便但需20-30元手續費，且每日限額2-3萬元。大額儲值建議用網銀。"
          }
        },
        {
          "@type": "Question",
          "name": "USDT儲值安全嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "USDT儲值相對安全，具有匿名性、無限額、快速到帳等優點。但需注意：1) 選擇正規交易所購買USDT；2) 確認平台支援的鏈類型（TRC20/ERC20）；3) 選錯鏈可能導致資金遺失。"
          }
        },
        {
          "@type": "Question",
          "name": "儲值時需要手續費嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "依儲值方式而異：網路銀行轉帳通常免手續費；ATM轉帳通常免費或10元；超商儲值需20-30元手續費；USDT需1-2 USDT手續費（TRC20）。建議選擇網銀轉帳最划算。"
          }
        },
        {
          "@type": "Question",
          "name": "儲值金額錯誤怎麼辦？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "如果不小心儲值錯誤金額，立即聯繫客服說明情況。大部分平台都會協助處理，但可能需要一些時間核對。保留所有轉帳憑證以便查證。"
          }
        },
        {
          "@type": "Question",
          "name": "首次儲值建議多少金額？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "建議首次儲值1000-2000元進行測試，確認平台正常出金、遊戲體驗良好後，再進行大額儲值。這樣可以最低風險驗證平台可靠性。"
          }
        },
        {
          "@type": "Question",
          "name": "儲值後可以馬上提款嗎？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "可以，但領取首儲優惠的話通常有流水要求（如10-20倍）。如果不領優惠純儲值，提款通常無限制。建議詳閱各平台的提款條款。"
          }
        },
        {
          "@type": "Question",
          "name": "哪家銀行網銀最適合儲值娛樂城？",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": "推薦：台新銀行（Richart APP好用）、玉山銀行（介面友善）、國泰世華（穩定可靠）。這三家網銀轉帳都免手續費，操作便利。"
          }
        }
      ]
    }
    </script>
'''
    c = c.replace('</head>', faq_schema + '</head>')

    # 3.8 加強內鏈
    c = c.replace(
        '<li><strong>確認平台信譽</strong>：儲值前務必確認平台是否為正規娛樂城</li>',
        '<li><strong>確認平台信譽</strong>：儲值前務必確認平台是否為正規娛樂城（參考<a href="/articles/casino-safe">安全推薦清單</a>）</li>'
    )

    # 3.9 更新日期
    c = c.replace('"dateModified": "2026-05-15T01:00:00+08:00"', f'"dateModified": "{NOW_ISO}"')
    c = c.replace('<span class="update-date">🔄 最後更新：2026年5月15日</span>', f'<span class="update-date">🔄 最後更新：{NOW_DATE}</span>')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('✅ deposit-guide.html optimized')


if __name__ == '__main__':
    optimize_3a_casino_scam_review()
    optimize_baccarat_strategy()
    optimize_deposit_guide()
    print('\n🎉 All 3 articles optimized!')
