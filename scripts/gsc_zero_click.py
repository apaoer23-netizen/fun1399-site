#!/usr/bin/env python3
"""
GSC 分析 - 找出有曝光但0點擊的頁面
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

CREDENTIALS_FILE = '/root/.openclaw/workspace/config/gsc-credentials.json'
SITE_URL = 'https://fun1399.com/'

def get_gsc_service():
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    return build('webmasters', 'v3', credentials=credentials)

def get_pages_with_impressions(service, days=28):
    """取得有曝光但0點擊的頁面"""
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page'],
        'rowLimit': 100
    }
    
    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    
    zero_click_pages = []
    for row in response.get('rows', []):
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        page = row['keys'][0]
        
        # 有曝光但0點擊
        if impressions > 0 and clicks == 0:
            zero_click_pages.append({
                'page': page,
                'impressions': impressions,
                'position': row.get('position', 0)
            })
    
    # 按曝光量排序
    zero_click_pages.sort(key=lambda x: x['impressions'], reverse=True)
    return zero_click_pages

if __name__ == '__main__':
    service = get_gsc_service()
    pages = get_pages_with_impressions(service)
    
    print("🔍 有曝光但0點擊的頁面（Top 10）：")
    print("-" * 80)
    for i, p in enumerate(pages[:10], 1):
        print(f"{i}. {p['page']}")
        print(f"   曝光: {p['impressions']} | 平均排名: {p['position']:.1f}")
        print()
