#!/usr/bin/env python3
"""
Google Search Console API 測試腳本
讀取 fun1399.com 的搜尋成效數據
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# 設定
CREDENTIALS_FILE = '/root/.openclaw/workspace/config/gsc-credentials.json'
SITE_URL = 'https://fun1399.com/'

def get_gsc_service():
    """建立 GSC API 服務"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    service = build('webmasters', 'v3', credentials=credentials)
    return service

def test_api_connection(service):
    """測試 API 連線並取得網站列表"""
    try:
        sites = service.sites().list().execute()
        print("✅ API 連線成功！")
        print(f"可存取的網站：")
        for site in sites.get('siteEntry', []):
            print(f"  - {site['siteUrl']} ({site['permissionLevel']})")
        return True
    except Exception as e:
        print(f"❌ API 連線失敗：{e}")
        return False

def get_search_analytics(service, days=28):
    """取得搜尋成效數據"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    print(f"\n📊 查詢期間：{start_date} 至 {end_date}（過去 {days} 天）")
    
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['query'],
        'rowLimit': 25
    }
    
    try:
        response = service.searchanalytics().query(
            siteUrl=SITE_URL, 
            body=request
        ).execute()
        
        return response
    except Exception as e:
        print(f"❌ 查詢失敗：{e}")
        return None

def format_results(response):
    """格式化輸出結果"""
    if not response or 'rows' not in response:
        print("⚠️ 沒有數據（可能網站還沒有搜尋流量）")
        return
    
    print("\n🔍 熱門搜尋查詢（Top 25）：")
    print("-" * 80)
    print(f"{'排名':<4} {'關鍵字':<40} {'點擊':<8} {'曝光':<8} {'CTR':<8} {'排名':<6}")
    print("-" * 80)
    
    for i, row in enumerate(response['rows'], 1):
        query = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0) * 100
        position = row.get('position', 0)
        
        print(f"{i:<4} {query[:38]:<40} {clicks:<8} {impressions:<8} {ctr:<7.1f}% {position:<6.1f}")
    
    # 總計
    total_clicks = sum(r.get('clicks', 0) for r in response['rows'])
    total_impressions = sum(r.get('impressions', 0) for r in response['rows'])
    avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
    
    print("-" * 80)
    print(f"總計：{total_clicks} 點擊 / {total_impressions} 曝光 / {avg_ctr:.1f}% CTR")

if __name__ == '__main__':
    print("=" * 80)
    print("Google Search Console API - fun1399.com 數據讀取")
    print("=" * 80)
    
    try:
        # 建立服務
        service = get_gsc_service()
        
        # 測試連線
        if test_api_connection(service):
            # 取得搜尋數據
            response = get_search_analytics(service, days=28)
            if response:
                format_results(response)
        
    except Exception as e:
        print(f"\n❌ 錯誤：{e}")
        print("\n可能原因：")
        print("1. 服務帳號尚未加入 GSC 使用者（請到 GSC → 設定 → 使用者與權限新增）")
        print("2. 憑證檔案路徑錯誤")
        print("3. API 尚未啟用")
