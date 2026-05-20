#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成娛樂城網站內容
目標：30篇以上文章
"""

import os
import json

# 文章模板數據庫
ARTICLES = [
    # 平台評測類 (6篇)
    {
        "filename": "mbm.html",
        "folder": "reviews",
        "title": "【MBM娛樂城評測】2分鐘出金是真的嗎？完整分析",
        "desc": "MBM娛樂城完整評測！實測2分鐘極速出金、0.8%高額返水、首儲1000送1000優惠。適合追求快速出金的玩家。",
        "type": "review",
        "platform": "MBM"
    },
    {
        "filename": "utown.html",
        "folder": "reviews",
        "title": "【優塔娛樂城評測】USDT專精平台完整分析",
        "desc": "優塔娛樂城完整評測！USDT加密貨幣專精、無上限提款、最高1%返水。適合幣圈玩家的娛樂城推薦。",
        "type": "review",
        "platform": "優塔"
    },
    {
        "filename": "hg.html",
        "folder": "reviews",
        "title": "【HG娛樂城評測】新手入門首選完整分析",
        "desc": "HG娛樂城完整評測！體驗金388元免費試玩、好路體育、新手友好介面。適合娛樂城新手的平台推薦。",
        "type": "review",
        "platform": "HG"
    },
    {
        "filename": "gm1688.html",
        "folder": "reviews",
        "title": "【大老爺娛樂城評測】3分鐘出金老牌平台分析",
        "desc": "大老爺娛樂城完整評測！3分鐘高速出金、原生APP體驗、老牌信譽保障。適合重視穩定的玩家。",
        "type": "review",
        "platform": "大老爺"
    },
    {
        "filename": "3a.html",
        "folder": "reviews",
        "title": "【3A娛樂城評測】台灣本土品牌完整分析",
        "desc": "3A娛樂城完整評測！台灣本土最受歡迎品牌、1-2分鐘出金、豐富優惠活動。本土玩家首選平台。",
        "type": "review",
        "platform": "3A"
    },
    # 比較類文章 (5篇)
    {
        "filename": "withdrawal-compare.html",
        "folder": "comparisons",
        "title": "娛樂城出金速度比較2026｜6大平台實測對比",
        "desc": "2026娛樂城出金速度完整比較！鉅城、MBM、優塔等6大平台提款速度實測，幫你選出出金最快的娛樂城。",
        "type": "compare",
        "topic": "出金速度"
    },
    {
        "filename": "bonus-compare.html",
        "folder": "comparisons",
        "title": "娛樂城首儲優惠比較2026｜哪家送最多？",
        "desc": "2026娛樂城首儲優惠完整比較！首儲1000送1000、體驗金、返水比例一次看，找出最划算的優惠。",
        "type": "compare",
        "topic": "首儲優惠"
    },
    {
        "filename": "rtp-compare.html",
        "folder": "comparisons",
        "title": "娛樂城RTP比較｜哪家老虎機回報率最高？",
        "desc": "娛樂城RTP完整比較！各平台老虎機回報率分析，教你如何選高RTP機台提升贏錢機會。",
        "type": "compare",
        "topic": "RTP回報率"
    },
    # 攻略類 (10篇)
    {
        "filename": "baccarat-rules.html",
        "folder": "articles",
        "title": "百家樂規則完整教學｜新手入門必看",
        "desc": "百家樂規則完整教學！從基礎玩法到進階技巧，新手入門必看的百家樂攻略。",
        "type": "guide",
        "topic": "百家樂"
    },
    {
        "filename": "baccarat-strategy.html",
        "folder": "articles",
        "title": "百家樂必勝策略｜馬丁、123投注法解析",
        "desc": "百家樂必勝策略完整解析！馬丁策略、123投注法、看路技巧，提升你的百家樂勝率。",
        "type": "guide",
        "topic": "百家樂策略"
    },
    {
        "filename": "slots-beginner.html",
        "folder": "articles",
        "title": "老虎機新手入門｜如何選台與基本玩法",
        "desc": "老虎機新手入門教學！如何選台、基本玩法、常見迷思破解，讓你快速上手老虎機。",
        "type": "guide",
        "topic": "老虎機"
    },
    {
        "filename": "slots-myths.html",
        "folder": "articles",
        "title": "老虎機迷思破解｜冷熱台、吐分期真相",
        "desc": "老虎機迷思完整破解！冷熱台不存在、吐分期真相、RNG運作原理，讓你不再被騙。",
        "type": "guide",
        "topic": "老虎機迷思"
    },
    {
        "filename": "wagering-guide.html",
        "folder": "articles",
        "title": "洗碼量流水計算教學｜提款必懂概念",
        "desc": "洗碼量流水計算完整教學！什麼是流水、如何計算、提款限制，娛樂城新手必懂概念。",
        "type": "guide",
        "topic": "洗碼量"
    },
    {
        "filename": "deposit-guide.html",
        "folder": "articles",
        "title": "娛樂城儲值教學｜超商、銀行、USDT方式比較",
        "desc": "娛樂城儲值完整教學！超商代碼、銀行轉帳、USDT加密貨幣，各種儲值方式優缺點比較。",
        "type": "guide",
        "topic": "儲值"
    },
    {
        "filename": "safety-guide.html",
        "folder": "articles",
        "title": "娛樂城安全指南｜如何避免詐騙與黑網",
        "desc": "娛樂城安全完整指南！如何辨別詐騙平台、黑網特徵、安全遊戲守則，保護你的資金安全。",
        "type": "guide",
        "topic": "安全"
    },
    {
        "filename": "vip-guide.html",
        "folder": "articles",
        "title": "娛樂城VIP制度解析｜返水、專屬客服好處",
        "desc": "娛樂城VIP制度完整解析！各等級福利、返水比例、專屬客服，成為VIP玩家的好處。",
        "type": "guide",
        "topic": "VIP"
    },
    # 推薦類 (5篇)
    {
        "filename": "fast-withdrawal.html",
        "folder": "articles",
        "title": "2026出金最快娛樂城推薦｜5分鐘內到帳",
        "desc": "2026出金最快娛樂城推薦！5分鐘內到帳平台整理，追求快速出金玩家必看。",
        "type": "recommend",
        "topic": "快速出金"
    },
    {
        "filename": "high-rtp-slots.html",
        "folder": "articles",
        "title": "2026高RTP老虎機推薦｜回報率96%以上",
        "desc": "2026高RTP老虎機推薦！回報率96%以上機台整理，提升贏錢機會的老虎機攻略。",
        "type": "recommend",
        "topic": "高RTP老虎機"
    },
    {
        "filename": "newbie-friendly.html",
        "folder": "articles",
        "title": "2026新手友善娛樂城推薦｜體驗金、低流水",
        "desc": "2026新手友善娛樂城推薦！體驗金試玩、低流水要求、完整教學，新手入門首選。",
        "type": "recommend",
        "topic": "新手友善"
    },
    {
        "filename": "usdt-casino.html",
        "folder": "articles",
        "title": "2026 USDT娛樂城推薦｜加密貨幣儲值首選",
        "desc": "2026 USDT娛樂城推薦！加密貨幣儲值、出金快速、隱私保障，幣圈玩家必看。",
        "type": "recommend",
        "topic": "USDT"
    },
    # FAQ類
    {
        "filename": "faq.html",
        "folder": "guides",
        "title": "娛樂城常見問題FAQ｜新手必看Q&A",
        "desc": "娛樂城常見問題完整FAQ！出金、儲值、優惠、安全等常見問題解答，新手必看。",
        "type": "faq",
        "topic": "常見問題"
    }
]

print(f"準備生成 {len(ARTICLES)} 篇文章")
print(json.dumps([a['title'] for a in ARTICLES], ensure_ascii=False, indent=2))
