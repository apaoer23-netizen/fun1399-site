#!/bin/bash
# 批量為文章添加 hero image 的腳本

ARTICLES_DIR="/root/.openclaw/workspace/fun1399-site/build/articles"

cd "$ARTICLES_DIR"

# 定義文章與對應的圖片
declare -A ARTICLE_IMAGES=(
    ["baccarat-rules.html"]="baccarat-chips.webp"
    ["baccarat-strategy.html"]="baccarat-chips.webp"
    ["cashback-guide.html"]="baccarat-chips.webp"
    ["casino-agent-guide.html"]="baccarat-chips.webp"
    ["casino-comparison-guide.html"]="baccarat-chips.webp"
    ["casino-customer-service.html"]="baccarat-chips.webp"
    ["casino-free-trial-bonus.html"]="baccarat-chips.webp"
    ["casino-no-withdrawal-scam.html"]="warning-shield.webp"
    ["casino-ranking-2026.html"]="baccarat-chips.webp"
    ["casino-recommendation-2026.html"]="baccarat-chips.webp"
    ["casino-registration-guide.html"]="baccarat-chips.webp"
    ["casino-safety-check.html"]="casino-security.webp"
    ["casino-scam-methods.html"]="warning-shield.webp"
    ["deposit-guide.html"]="baccarat-chips.webp"
    ["fast-withdrawal.html"]="baccarat-chips.webp"
    ["free-credit-guide.html"]="baccarat-chips.webp"
    ["high-cashback-casino.html"]="baccarat-chips.webp"
    ["high-rtp-slots.html"]="baccarat-chips.webp"
    ["how-to-check-casino-scam-record.html"]="warning-shield.webp"
    ["mlb-betting.html"]="sports-betting.webp"
    ["nba-betting.html"]="basketball-court.webp"
    ["newbie-friendly.html"]="baccarat-chips.webp"
    ["rtp-compare.html"]="baccarat-chips.webp"
    ["safety-guide.html"]="casino-security.webp"
    ["slots-beginner.html"]="baccarat-chips.webp"
    ["slots-guide.html"]="baccarat-chips.webp"
    ["slots-myths.html"]="baccarat-chips.webp"
    ["soccer-betting.html"]="sports-betting.webp"
    ["sports-betting-tips.html"]="sports-betting.webp"
    ["usdt-casino.html"]="baccarat-chips.webp"
    ["vip-guide.html"]="baccarat-chips.webp"
    ["wagering-guide.html"]="baccarat-chips.webp"
    ["withdrawal-ranking.html"]="baccarat-chips.webp"
    ["withdrawal-risks.html"]="warning-shield.webp"
    ["world-cup-2026-guide.html"]="sports-betting.webp"
    ["world-cup-betting-guide.html"]="sports-betting.webp"
    ["world-cup-betting-tips.html"]="sports-betting.webp"
    ["world-cup-favorites.html"]="sports-betting.webp"
    ["world-cup-live-betting.html"]="sports-betting.webp"
    ["world-cup-schedule.html"]="sports-betting.webp"
)

declare -A ARTICLE_ALTS=(
    ["baccarat-rules.html"]="百家樂規則教學，牌桌與籌碼示意圖"
    ["baccarat-strategy.html"]="百家樂策略攻略，馬丁格爾技巧"
    ["cashback-guide.html"]="娛樂城返水優惠概念圖"
    ["casino-agent-guide.html"]="娛樂城代理分潤機制圖示"
    ["casino-comparison-guide.html"]="娛樂城比較評比圖表"
    ["casino-customer-service.html"]="娛樂城客服支援示意圖"
    ["casino-free-trial-bonus.html"]="娛樂城免費體驗金示意圖"
    ["casino-no-withdrawal-scam.html"]="娛樂城不出金詐騙警示"
    ["casino-ranking-2026.html"]="2026年娛樂城排名圖表"
    ["casino-recommendation-2026.html"]="2026年娛樂城推薦平台"
    ["casino-registration-guide.html"]="娛樂城註冊開戶教學"
    ["casino-safety-check.html"]="娛樂城安全檢查認證"
    ["casino-scam-methods.html"]="娛樂城詐騙手法警示"
    ["deposit-guide.html"]="娛樂城儲值入金教學"
    ["fast-withdrawal.html"]="娛樂城快速出金提款"
    ["free-credit-guide.html"]="娛樂城免費體驗金攻略"
    ["high-cashback-casino.html"]="高返水娛樂城推薦"
    ["high-rtp-slots.html"]="高RTP老虎機推薦"
    ["how-to-check-casino-scam-record.html"]="查詢娛樂城詐騙紀錄教學"
    ["mlb-betting.html"]="MLB棒球賽事投注"
    ["nba-betting.html"]="NBA籃球賽事投注"
    ["newbie-friendly.html"]="新手友善娛樂城推薦"
    ["rtp-compare.html"]="娛樂城RTP回報率比較"
    ["safety-guide.html"]="娛樂城安全指南"
    ["slots-beginner.html"]="老虎機入門教學"
    ["slots-guide.html"]="老虎機玩法攻略"
    ["slots-myths.html"]="老虎機迷思破解"
    ["soccer-betting.html"]="足球賽事投注教學"
    ["sports-betting-tips.html"]="體育投注技巧策略"
    ["usdt-casino.html"]="USDT加密貨幣娛樂城"
    ["vip-guide.html"]="娛樂城VIP會員制度"
    ["wagering-guide.html"]="洗碼量流水計算教學"
    ["withdrawal-ranking.html"]="娛樂城出金速度排名"
    ["withdrawal-risks.html"]="娛樂城提款風險警示"
    ["world-cup-2026-guide.html"]="2026世界盃足球賽"
    ["world-cup-betting-guide.html"]="世界盃投注教學"
    ["world-cup-betting-tips.html"]="世界盃投注技巧"
    ["world-cup-favorites.html"]="世界盃奪冠熱門隊伍"
    ["world-cup-live-betting.html"]="世界盃滾球投注"
    ["world-cup-schedule.html"]="世界盃賽程表"
)

# 為每篇文章添加 hero image (如果還沒有的話)
for article in "${!ARTICLE_IMAGES[@]}"; do
    image="${ARTICLE_IMAGES[$article]}"
    alt="${ARTICLE_ALTS[$article]}"
    
    # 檢查是否已經有 hero image
    if ! grep -q "article-hero-image" "$article"; then
        echo "添加 hero image 到 $article"
        
        # 創建 hero image HTML
        hero_html="            <div class=\"article-hero-image\">\n                <img src=\"/static/images/$image\" \n                     alt=\"$alt\" \n                     loading=\"lazy\"\n                     width=\"1200\" height=\"630\">\n                <p class=\"image-caption\">$alt</p>\n            </div>\n\n"
        
        # 在 article-meta 之前插入 hero image
        sed -i "/<div class=\"article-meta\">/i\\$hero_html" "$article"
    fi
done

echo "Hero image 添加完成！"
