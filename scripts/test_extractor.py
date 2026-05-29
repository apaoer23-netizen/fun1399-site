import trafilatura
import os

# 確保下載目錄存在
os.makedirs("/root/.openclaw/workspace/downloads", exist_ok=True)

url = "https://gamelife543.com/at99-scam-recovery-guide-2025/"
print(f"正在抓取網址: {url}")

downloaded = trafilatura.fetch_url(url)
if downloaded:
    # 萃取內文，並嘗試保留圖片的 alt 資訊
    text = trafilatura.extract(downloaded, include_images=True)
    if text:
        save_path = "/root/.openclaw/workspace/downloads/test_extracted.txt"
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"✅ 萃取成功！檔案已儲存至: {save_path}")
        print("\n--- 內文預覽 (前 300 字) ---")
        print(text[:300])
        print("----------------------------")
    else:
        print("❌ 抓取成功，但無法萃取內文（可能是防爬蟲或全圖片網頁）")
else:
    print("❌ 無法連線至該網頁")
