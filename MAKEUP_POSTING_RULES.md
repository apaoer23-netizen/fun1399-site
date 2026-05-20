# fun1399.com 補發機制（強制規則）
## Makeup Posting Mechanism

---

## 📋 規則說明

### 執行流程（每次發文前必須執行）

```python
import datetime
import os

# 1. 取得真實今天日期
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
weekday = today.weekday()

# 2. 僅週一/三/五發文
if weekday not in [0, 2, 4]:
    exit(0)

# 3. 檢查上一個發文日是否已完成
# weekday: 0=週一, 2=週三, 4=週五
# 上一個發文日：
#   週三 → 週一（-2天）
#   週五 → 週三（-2天）
#   週一 → 上週五（-3天）

prev_days = {0: 3, 2: 2, 4: 2}  # 週一/三/五對應的上一個發文日間隔
prev_date = today - datetime.timedelta(days=prev_days[weekday])

# 4. 檢查上一篇是否已存在（根據排程文件中的標題）
#    若不存在 → 優先補發
#    若存在 → 執行今天文章

# 5. 若有多篇未完成（連續錯過），按日期順序補發
#    不可跳過任何未完成文章
```

---

## 📊 補發檢核報告

### 系統時間
| 項目 | 數值 |
|------|------|
| 系統日期 | 2026-05-05 |
| 系統時間 | 15:55 CST (Asia/Taipei, UTC+08:00) |
| 計算星期 | weekday() = 1 → **週二** |
| 是否發文日 | ❌ 否（僅週一/三/五發文） |

### 文章完成狀態檢查

| 排程日期 | 正確星期 | 文章標題 | 檔案是否存在 | 狀態 |
|----------|---------|----------|-------------|------|
| 5/1 | 週五 | 財神娛樂城是詐騙嗎？PTT網友被騙經驗與評價實測 | ❌ 不存在 | 🔴 **未完成** |
| 5/4 | 週一 | 必贏娛樂城不出金怎麼辦？受害者投訴與自救方法實測 | ❌ 不存在 | 🔴 **未完成** |
| 5/6 | 週三 | 鉅城娛樂城2026年5月評價：出金速度與遊戲體驗實測 | ❌ 不存在 | ⏳ 待執行 |
| 5/8 | 週五 | 炫海娛樂城黑網傳聞是真的嗎？網友評價與爭議調查 | ❌ 不存在 | ⏳ 待執行 |

### 檢查方法

```bash
# 檢查最新文章修改時間
ls -lt /root/.openclaw/workspace/fun1399-clean/articles/*.html | head -5

# 結果：
# 2026-04-30 02:08:05 index.html
# 2026-04-30 02:06:59 casino-account-freeze-scam.html
# 2026-04-27 18:20:47 casino-scam-emergency-response.html
# → 最近一篇為 4/30，5月無任何文章
```

---

## 🔴 補發清單（按日期順序，不可跳過）

| 優先順序 | 原定日期 | 文章標題 | 補發原因 |
|----------|---------|----------|----------|
| 1 | 5/1（週五） | 財神娛樂城是詐騙嗎？PTT網友被騙經驗與評價實測 | 429 rate limit 導致未完成 |
| 2 | 5/4（週一） | 必贏娛樂城不出金怎麼辦？受害者投訴與自救方法實測 | 非發文日錯過 |

**補發順序**：必須先寫 5/1 → 再寫 5/4 → 最後寫當天（5/6 鉅城）

---

## 📋 補發機制實作（嵌入 CRON_TASK.md）

### 執行順序

```
Step 1: 取得今天日期與星期
Step 2: 確認是週一/三/五（否則 exit）
Step 3: 計算上一個發文日
Step 4: 檢查上一個發文日的文章是否已存在
        ↓
        若不存在：進入補發流程
        ↓
        Step 4a: 找出所有「已過期但未完成」的文章
        Step 4b: 按日期順序排序（最早優先）
        Step 4c: 逐一補發（每篇獨立生成）
        ↓
        若存在：執行今天文章
```

### 檢查邏輯

```python
def check_missed_posts():
    """檢查所有已過期但未完成的文章"""
    today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    
    # 讀取排程文件
    schedule = load_schedule("2MONTH-CONTENT-PLAN-May-Jun-2026-v5.md")
    
    missed = []
    for entry in schedule:
        if entry.date < today.date():
            # 檢查該日期文章是否存在
            if not article_exists(entry.title):
                missed.append(entry)
    
    return sorted(missed, key=lambda x: x.date)  # 最早優先

def execute_with_makeup():
    """執行發文（含補發）"""
    missed = check_missed_posts()
    
    if missed:
        # 有未完成文章，優先補發
        for post in missed:
            print(f"🔴 補發 {post.date} 文章：{post.title}")
            write_article(post)
            report_to_user(post, is_makeup=True)
    
    # 執行今天文章（若今天也是發文日）
    if is_publish_day():
        today_post = get_today_post()
        print(f"✅ 執行今天文章：{today_post.title}")
        write_article(today_post)
        report_to_user(today_post, is_makeup=False)
```

---

## 📋 回報格式（強制）

每次執行後必須回報：

```
━━━━━━━━━━━━━━━
【發文執行報告】
━━━━━━━━━━━━━━━

系統日期：YYYY-MM-DD HH:MM CST (Asia/Taipei)
計算星期：週X（weekday=X）
是否發文日：是/否

【補發檢查】
- 未完成文章數：N篇
- 補發清單：
  1. YYYY-MM-DD（原定日期）：文章標題
  2. ...

【執行結果】
- 補發：N篇（列出標題）
- 今日：1篇（標題）
- 總計：N+1篇

【檔案路徑】
- /articles/xxx.html
- /articles/yyy.html
```

---

## ⚠️ 禁止事項

| 禁止行為 | 後果 |
|----------|------|
| ❌ 跳過未完成文章直接寫新文章 | 排程永久性遺失 |
| ❌ 手動判斷是否補發 | 必須用程式檢查 |
| ❌ 用記憶推測文章是否存在 | 必須檢查檔案系統 |
| ❌ 同一天補發多篇卻只回報一篇 | 必須逐篇回報 |

---

*建立日期：2026-05-05*
*生效日期：2026-05-05*
*此補發機制為強制規則，不可省略*
