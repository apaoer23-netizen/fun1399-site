#!/bin/bash
# 批量添加 Schema.org Article 標記到重要文章

ARTICLES=(
  "casino-customer-service.html|娛樂城客服比較｜24小時LINE客服與問題解決完整攻略|娛樂城客服完整攻略！LINE客服、24小時線上支援、常見問題解決方法。出金問題、帳號異常、優惠諮詢，找到最有效的聯繫管道。|2026-03-20"
  "casino-registration-guide.html|娛樂城註冊教學｜3分鐘完成開戶，領取體驗金完整攻略|娛樂城註冊完整教學！3分鐘快速開戶、身分驗證流程、體驗金領取步驟，註冊注意事項一次看。|2026-03-18"
  "casino-free-trial-bonus.html|娛樂城體驗金｜2026最新免費體驗金領取攻略與注意事項|2026最新娛樂城體驗金攻略！如何領取免費體驗金、體驗金使用規則、流水要求解析。|2026-03-17"
  "baccarat-guide.html|百家樂技巧：從入門到高手的完整攻略|百家樂完整攻略！從基礎規則到進階看路技巧，掌握長龍、單跳、雙跳等牌路。|2026-03-14"
  "withdrawal-ranking.html|娛樂城出金速度排行｜6大平台實測比較|實測6大娛樂城出金速度！鉅城、MBM、優塔等平台出金時間比較，找出出金最快的娛樂城。|2026-03-14"
  "casino-safe.html|如何判斷娛樂城是否安全？7個關鍵指標完整解析|娛樂城安全攻略！7個判斷指標、3大驗證方法、5個危險信號，教你如何避開黑網詐騙平台。|2026-03-14"
  "cashback-guide.html|娛樂城返水是什麼？返水比例計算攻略|娛樂城返水完整教學！返水是什麼、如何計算、0.3%-1.0%返水差異分析，幫你最大化返水收益。|2026-03-14"
  "deposit-guide.html|娛樂城儲值教學｜四大儲值方式完整攻略|娛樂城儲值完整教學！超商儲值、銀行轉帳、虛擬貨幣、第三方支付比較，最低儲值金額與手續費分析。|2026-03-14"
  "casino-scam-methods.html|娛樂城詐騙手法大公開｜5大常見詐騙套路解析|娛樂城詐騙手法完整解析！假冒客服、愛情詐騙、高額獲利、帳號凍結、不出金等5大詐騙套路。|2026-03-14"
  "sports-betting-guide.html|體育投注完整教學｜賠率計算與投注策略|體育投注入門攻略！賠率計算、讓分/大小球玩法、場中投注技巧，從新手到專業投注教學。|2026-03-14"
)

cd /root/.openclaw/workspace/fun1399-site/build/articles

for item in "${ARTICLES[@]}"; do
  IFS='|' read -r filename title description date <<< "$item"
  
  if [ -f "$filename" ]; then
    # 檢查是否已有 Schema
    if ! grep -q "application/ld+json" "$filename"; then
      # 創建 Schema JSON
      schema='    <!-- Schema.org Article 標記 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "'"$title"'",
      "description": "'"$description"'",
      "author": {
        "@type": "Person",
        "name": "Kevin Lin",
        "url": "https://fun1399.com/author.html#kevin"
      },
      "publisher": {
        "@type": "Organization",
        "name": "娛樂城玩家俱樂部"
      },
      "datePublished": "'"$date"'",
      "dateModified": "'"$date"'"
    }
    </script>'
      
      # 插入到 canonical 後面
      sed -i "/canonical/a\\$schema" "$filename"
      echo "✓ Added Schema: $filename"
    else
      echo "○ Already has Schema: $filename"
    fi
  else
    echo "✗ File not found: $filename"
  fi
done

echo ""
echo "Schema 添加完成！"
