#!/usr/bin/env python3
"""
Google Search Console Page Performance Analysis
讀取 fun1399.com 過去 28 天的 page-level 數據
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

def get_page_performance(service, days=28, limit=5000):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    request = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['page'],
        'rowLimit': limit
    }
    
    response = service.searchanalytics().query(siteUrl=SITE_URL, body=request).execute()
    return response.get('rows', [])

def get_sitemap_urls():
    import xml.etree.ElementTree as ET
    tree = ET.parse('/root/.openclaw/workspace/fun1399-clean/sitemap.xml')
    root = tree.getroot()
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for url in root.findall('ns:url', ns):
        loc = url.find('ns:loc', ns)
        if loc is not None:
            urls.append(loc.text)
    return urls

if __name__ == '__main__':
    service = get_gsc_service()
    
    # 讀取 page performance
    rows = get_page_performance(service, days=28, limit=5000)
    
    # 讀取 sitemap
    sitemap_urls = get_sitemap_urls()
    
    print(f"📊 過去 28 天 Page Performance 數據")
    print(f"   總共 {len(rows)} 個 URL 有數據")
    print(f"   sitemap 共有 {len(sitemap_urls)} 個 URL")
    print()
    
    # 分類
    with_impressions = []
    zero_impressions = []
    
    for row in rows:
        page = row['keys'][0]
        clicks = row.get('clicks', 0)
        impressions = row.get('impressions', 0)
        ctr = row.get('ctr', 0)
        position = row.get('position', 0)
        
        data = {
            'page': page,
            'clicks': clicks,
            'impressions': impressions,
            'ctr': ctr,
            'position': position
        }
        
        if impressions > 0:
            with_impressions.append(data)
        else:
            zero_impressions.append(data)
    
    # 排序
    with_impressions.sort(key=lambda x: x['impressions'], reverse=True)
    zero_impressions.sort(key=lambda x: x['page'])
    
    print("=" * 100)
    print("【有曝光的頁面】依 impressions 排序")
    print("=" * 100)
    print(f"{'URL':<65} {'Impressions':<12} {'Clicks':<8} {'CTR':<8} {'Position'}")
    print("-" * 100)
    
    for item in with_impressions:
        url_short = item['page'].replace('https://fun1399.com', '')
        if len(url_short) > 60:
            url_short = url_short[:57] + '...'
        print(f"{url_short:<65} {item['impressions']:<12} {item['clicks']:<8} {item['ctr']*100:<7.1f}% {item['position']:<6.1f}")
    
    print()
    print("=" * 100)
    print("【零曝光但已索引的頁面】")
    print("=" * 100)
    
    # 找出 sitemap 中有但在 performance 中沒有 impressions 的 URL
    perf_pages = {r['keys'][0] for r in rows}
    no_data_urls = [u for u in sitemap_urls if u not in perf_pages]
    
    print(f"sitemap 中無 performance 數據的 URL: {len(no_data_urls)} 個")
    print()
    for url in no_data_urls[:30]:
        print(f"  - {url.replace('https://fun1399.com', '')}")
    if len(no_data_urls) > 30:
        print(f"  ... 還有 {len(no_data_urls) - 30} 個")
    
    # 儲存完整數據到 JSON 供分析
    output = {
        'with_impressions': with_impressions,
        'zero_impressions': zero_impressions,
        'no_data_urls': no_data_urls,
        'total_sitemap': len(sitemap_urls),
        'total_performance': len(rows)
    }
    
    with open('/tmp/fun1399-gsc-analysis.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print()
    print(f"✅ 完整數據已儲存到 /tmp/fun1399-gsc-analysis.json")
