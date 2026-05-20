#!/bin/bash
# 為重要文章添加 Schema.org Article 標記

cd /root/.openclaw/workspace/fun1399-site/build/articles

# 定義文章資訊 (檔名|標題|描述|日期)
declare -a ARTICLES=(
  "withdrawal-ranking.html|娛樂城出金速度排行｜6大平台實測比較|實測6大娛樂城出金速度！鉅城、MBM、優塔等平台出金時間比較，找出出金最快的娛樂城。|2026-03-14"
  "casino-safe.html|如何判斷娛樂城是否安全？7個關鍵指標完整解析|娛樂城安全攻略！7個判斷指標、3大驗證方法、5個危險信號，教你如何避開黑網詐騙平台。|2026-03-14"
  "cashback-guide.html|娛樂城返水是什麼？返水比例計算攻略|娛樂城返水完整教學！返水是什麼、如何計算、0.3%-1.0%返水差異分析，幫你最大化返水收益。|2026-03-14"
  "deposit-guide.html|娛樂城儲值教學｜四大儲值方式完整攻略|娛樂城儲值完整教學！超商儲值、銀行轉帳、虛擬貨幣、第三方支付比較，最低儲值金額與手續費分析。|2026-03-14"
  "casino-scam-methods.html|娛樂城詐騙手法大公開｜5大常見詐騙套路解析|娛樂城詐騙手法完整解析！假冒客服、愛情詐騙、高額獲利、帳號凍結、不出金等5大詐騙套路。|2026-03-14"
  "sports-betting-guide.html|體育投注完整教學｜賠率計算與投注策略|體育投注入門攻略！賠率計算、讓分/大小球玩法、場中投注技巧，從新手到專業投注教學。|2026-03-14"
  "baccarat-rules.html|百家樂規則完整教學｜新手必讀入門指南|百家樂基礎規則完整教學！牌型計算、補牌規則、賠率說明，5分鐘搞懂百家樂怎麼玩。|2026-03-14"
  "baccarat-strategy.html|百家樂必勝策略解析｜馬丁格爾與其他投注法|百家樂進階策略！馬丁格爾、費波那契、帕羅利等投注法分析，資金管理與風險控制技巧。|2026-03-14"
  "slots-guide.html|老虎機攻略｜RTP、波動度與中獎機率解析|老虎機完整攻略！RTP是什麼、高低波動度差異、中獎機率計算，選台技巧與資金管理。|2026-03-14"
  "casino-bonus-guide.html|娛樂城優惠攻略｜首儲、體驗金、返水怎麼領|娛樂城優惠完整教學！首儲優惠、體驗金、返水、VIP特權，如何領取最划算，流水要求解析。|2026-03-14"
  "wagering-guide.html|洗碼量是什麼？流水要求計算完整教學|娛樂城洗碼量完整教學！流水要求是什麼、如何計算、優惠與出金的洗碼差異，快速達標技巧。|2026-03-14"
  "casino-scam-alert.html|娛樂城詐騙警示｜最新詐騙手法與防範方法|2026最新娛樂城詐騙警示！假冒平台、愛情詐騙、投資詐騙等最新手法，如何保護自己不受騙。|2026-03-14"
  "safety-guide.html|娛樂城安全指南｜如何選擇安全的平台|娛樂城安全完整指南！5大安全指標、3步驟驗證法、常見危險信號，教你選擇安全可靠的娛樂城。|2026-03-14"
  "usdt-casino.html|USDT娛樂城完整教學｜加密貨幣儲值提款攻略|USDT娛樂城攻略！加密貨幣儲值教學、USDT娛樂城推薦、優缺點分析、安全注意事項。|2026-03-14"
)

for item in "${ARTICLES[@]}"; do
  IFS='|' read -r filename title description date <<< "$item"
  
  if [ -f "$filename" ]; then
    # 檢查是否已有 Schema
    if ! grep -q "@type.*Article" "$filename"; then
      echo "處理: $filename"
      
      # 使用 Python 插入 Schema（避免 sed 特殊字符問題）
      python3 << EOF
import re

with open('$filename', 'r', encoding='utf-8') as f:
    content = f.read()

schema = '''    <!-- Schema.org Article 標記 -->
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "$title",
      "description": "$description",
      "author": {
        "@type": "Person",
        "name": "Kevin Lin",
        "url": "https://fun1399.com/author.html#kevin"
      },
      "publisher": {
        "@type": "Organization",
        "name": "娛樂城玩家俱樂部"
      },
      "datePublished": "$date",
      "dateModified": "$date"
    }
    </script>'''

# 在 canonical 後面插入 Schema
content = content.replace(
    '<link rel="canonical" href="https://fun1399.com/articles/$filename"\u003e',
    '<link rel="canonical" href="https://fun1399.com/articles/$filename"\u003e\n' + schema
)

with open('$filename', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✓ Added Schema: $filename")
EOF
    else
      echo "○ Already has Schema: $filename"
    fi
  else
    echo "✗ File not found: $filename"
  fi
done

echo ""
echo "Schema 添加完成！"
