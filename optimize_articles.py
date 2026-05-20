#!/usr/bin/env python3
"""
優化 free-credit-guide.html 與 casino-registration-guide.html
"""
import os

WORKSPACE = '/root/.openclaw/workspace/fun1399-clean/articles'

def fix_free_credit_guide():
    path = os.path.join(WORKSPACE, 'free-credit-guide.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. 修復 OG/Twitter description
    c = c.replace(
        'content="娛樂城體驗金完整教學！什麼是體驗金？如何領取？提款條件是什麼？推薦有體驗金的平台一次看！">',
        'content="2026最新娛樂城體驗金完整教學！各平台體驗金金額比較、領取步驟、提款條件與流水計算，推薦有體驗金的平台一次看！">'
    )

    # 2. 更新 Schema headline/description
    c = c.replace(
        '"headline": "娛樂城體驗金完整指南：免費試玩與提款條件解析 - 娛樂城玩家俱樂部"',
        '"headline": "2026最新娛樂城體驗金完整指南｜免費試玩與提款條件解析"'
    )
    c = c.replace(
        '"description": "娛樂城體驗金完整教學！什麼是體驗金？如何領取？提款條件是什麼？推薦有體驗金的平台一次看！"',
        '"description": "2026最新娛樂城體驗金完整教學！各平台體驗金金額比較、領取步驟、提款條件與流水計算，推薦有體驗金的平台一次看！"'
    )

    # 3. 新增 HowTo Schema（插入在 </head> 之前）
    howto_schema = '''    <!-- HowTo Schema: 娛樂城體驗金領取5步驟 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "HowTo",
      "name": "2026最新娛樂城體驗金領取教學：5步驟免費試玩",
      "description": "詳細圖解娛樂城體驗金領取流程，從註冊到開始遊戲，只需5分鐘即可免費試玩。",
      "image": "https://fun1399.com/static/images/articles/articles/free-credit-guide-cover.jpg",
      "totalTime": "PT5M",
      "estimatedCost": {
        "@type": "MonetaryAmount",
        "currency": "TWD",
        "value": "0"
      },
      "supply": [
        {"@type": "HowToSupply", "name": "有效的電子郵件地址"},
        {"@type": "HowToSupply", "name": "可接收簡訊的手機號碼"},
        {"@type": "HowToSupply", "name": "身分證字號（部分平台）"}
      ],
      "tool": [
        {"@type": "HowToTool", "name": "智慧型手機或電腦"},
        {"@type": "HowToTool", "name": "穩定網路連線"}
      ],
      "step": [
        {
          "@type": "HowToStep",
          "position": 1,
          "name": "選擇信譽良好的娛樂城平台",
          "text": "研究並選擇有合法執照、網路評價良好的娛樂城。確認平台提供體驗金，並了解其流水倍數與提款條件。",
          "url": "https://fun1399.com/articles/free-credit-guide#section3",
          "image": "https://fun1399.com/static/images/articles/articles/free-credit-guide-cover.jpg"
        },
        {
          "@type": "HowToStep",
          "position": 2,
          "name": "完成會員註冊與驗證",
          "text": "進入官網點擊註冊，填寫真實個人資料（帳號、密碼、姓名、手機、Email）。完成手機驗證與郵件確認。",
          "url": "https://fun1399.com/articles/free-credit-guide#section3"
        },
        {
          "@type": "HowToStep",
          "position": 3,
          "name": "申請領取體驗金",
          "text": "註冊完成後，依平台規定領取體驗金：自動入帳型（直接到帳）、手動申請型（聯繫客服）、或綁定銀行型（綁定後發放）。",
          "url": "https://fun1399.com/articles/free-credit-guide#section3"
        },
        {
          "@type": "HowToStep",
          "position": 4,
          "name": "確認體驗金與流水條件",
          "text": "檢查體驗金是否已加入遊戲帳戶，並確認平台的流水倍數要求（通常10-30倍）與使用期限（通常7-30天）。",
          "url": "https://fun1399.com/articles/free-credit-guide#section4"
        },
        {
          "@type": "HowToStep",
          "position": 5,
          "name": "開始遊戲累計流水",
          "text": "選擇適合的遊戲開始投注。老虎機通常100%計入流水，百家樂與體育投注可能按比例計算。達成流水要求後即可申請提款。",
          "url": "https://fun1399.com/articles/free-credit-guide#section5"
        }
      ]
    }
    </script>
'''
    c = c.replace('</head>', howto_schema + '</head>')

    # 4. 修復重複結構問題 - 移除末尾多餘的 </div></article>footer... 區塊
    # 找到第一個正確的結尾，後面的都是重複
    # 正確結尾應該是：footer → related-articles → scripts → </body></html>
    # 後面多了一整段：cta-box + </div></article> + footer + related-articles + scripts
    
    duplicate_block = '''                    <div class="cta-box">
                <h3>延伸閱讀</h3>
                <ul>
                    <li><a href="/articles/withdrawal-ranking">娛樂城出金速度排行</a></li>
                    <li><a href="/articles/fast-withdrawal">快速出金教學</a></li>
                    <li><a href="/articles/casino-withdrawal-fast">娛樂城快速提款攻略</a></li>
                </ul>
            </div>

        </div>
    </article>

    <footer class="footer">
        <div class="container">
            <p>© 2026 娛樂城玩家俱樂部</p>
        </div>
    </footer>

<!-- Related Articles -->
<div class="related-articles" style="margin-top: 60px; padding: 30px; background: #f8f9fa; border-radius: 12px; border-left: 4px solid #00d4aa;">
  <h3 style="font-size: 22px; margin-bottom: 20px; color: #1a1a2e;">📚 你可能還想看</h3>
  <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px;">
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/casino-bonus-guide" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 娛樂城優惠攻略：返水、體驗金與首儲怎麼領</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/casino-free-trial-bonus" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 體驗金詐騙：領取優惠前必看的陷阱</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/vip-guide" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 娛樂城VIP制度解析</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/high-cashback-casino" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 高返水娛樂城推薦：哪家返水最優惠</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/casino-registration-guide" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 娛樂城註冊教學：新手開戶完整流程</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/articles/baccarat-guide" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 百家樂完整攻略：規則、牌路與下注策略</a></div>
    <div style="padding: 12px 15px; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);"><a href="/reviews/jucity" style="color: #1a1a2e; text-decoration: none; font-weight: 500;">→ 鉅城娛樂城評測</a></div>
  </div>
</div>
<!-- End Related Articles -->
    <script src="/static/js/floating-cta.js"></script>
'''
    c = c.replace(duplicate_block, '')

    # 5. 加強內鏈 - 在「選擇安全的註冊平台」段落添加 deposit-guide 內鏈
    c = c.replace(
        '推薦閱讀我們的<a href="/articles/safety-guide">娛樂城安全指南</a>',
        '推薦閱讀我們的<a href="/articles/safety-guide">娛樂城安全指南</a>，以及<a href="/articles/deposit-guide">儲值教學</a>與<a href="/articles/fast-withdrawal">提款攻略</a>'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('✅ free-credit-guide.html fixed')


def fix_casino_registration_guide():
    path = os.path.join(WORKSPACE, 'casino-registration-guide.html')
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. 更新 OG title
    c = c.replace(
        'content="娛樂城註冊教學｜3分鐘完成開戶，領取體驗金完整攻略 - 娛樂城玩家俱樂部">',
        'content="2026最新娛樂城註冊教學｜3分鐘完成開戶，領取體驗金完整攻略 - 娛樂城玩家俱樂部">'
    )
    # OG 和 Twitter 各出現兩次（title + description），只更新 title
    
    # 2. 更新 Article schema description
    c = c.replace(
        '"description": "娛樂城註冊完整教學！3分鐘快速開戶、身分驗證流程、體驗金領取步驟，註冊注意事項一次看。"',
        '"description": "2026最新娛樂城註冊完整教學！3分鐘快速開戶、身分驗證KYC流程、體驗金領取步驟、註冊常見問題一次看。新手開戶必讀攻略！"'
    )

    # 3. 更新 Twitter title
    c = c.replace(
        '<meta name="twitter:title" content="娛樂城註冊教學｜3分鐘完成開戶，領取體驗金完整攻略 - 娛樂城玩家俱樂部">',
        '<meta name="twitter:title" content="2026最新娛樂城註冊教學｜3分鐘完成開戶，領取體驗金完整攻略 - 娛樂城玩家俱樂部">'
    )

    # 4. 加強內鏈 - 在「註冊前準備事項」添加更多相關文章
    c = c.replace(
        '推薦閱讀我們的<a href="/articles/safety-guide">娛樂城安全指南</a>',
        '推薦閱讀我們的<a href="/articles/safety-guide">娛樂城安全指南</a>，註冊完成後可參考<a href="/articles/deposit-guide">儲值教學</a>與<a href="/articles/fast-withdrawal">提款攻略</a>'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print('✅ casino-registration-guide.html fixed')


if __name__ == '__main__':
    fix_free_credit_guide()
    fix_casino_registration_guide()
    print('\n🎉 All fixes applied!')
