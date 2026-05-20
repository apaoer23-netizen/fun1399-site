#!/usr/bin/env python3
"""
Google Search Console URL Inspection API (v1)
檢查 fun1399.com 指定 URL 的索引狀態
"""

import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# 設定
CREDENTIALS_FILE = '/root/.openclaw/workspace/config/gsc-credentials.json'
SITE_URL = 'https://fun1399.com/'

# 用戶要求檢查的 URL
URLS_TO_CHECK = [
    '/articles/deposit-guide',
    '/articles/casino-registration-guide',
    '/articles/casino-investment-scam',
    '/articles/3a-casino-scam-review',
    '/articles/free-credit-guide',
    '/articles/biwin-casino-no-withdrawal',
    '/articles/baccarat-strategy',
]

def get_gsc_service_v1():
    """建立 GSC API v1 服務（支持 urlInspection）"""
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/webmasters.readonly']
    )
    # 嘗試使用 searchconsole v1
    try:
        service = build('searchconsole', 'v1', credentials=credentials)
        return service
    except:
        # 如果 searchconsole 不可用，回退到 webmasters
        service = build('webmasters', 'v3', credentials=credentials)
        return service

def inspect_url(service, url_path):
    """檢查單個 URL 的索引狀態"""
    full_url = f"{SITE_URL.rstrip('/')}{url_path}"
    
    try:
        # 嘗試 searchconsole v1 API
        request = {
            'inspectionUrl': full_url,
            'siteUrl': SITE_URL
        }
        
        response = service.urlInspection().index().inspect(body=request).execute()
        
        result = {
            'url': url_path,
            'full_url': full_url,
            'status': 'unknown',
            'index_status': 'unknown',
            'last_crawl': None,
            'coverage_state': None,
            'reason': None,
            'google_canonical': None,
            'user_canonical': None,
            'sitemap': None,
            'error': None
        }
        
        inspection = response.get('inspectionResult', {})
        
        # 索引狀態
        index_status = inspection.get('indexStatusResult', {})
        if index_status:
            result['index_status'] = index_status.get('verdict', 'unknown')
            result['coverage_state'] = index_status.get('coverageState', 'unknown')
            result['last_crawl'] = index_status.get('lastCrawlTime', 'N/A')
            result['google_canonical'] = index_status.get('googleCanonical', 'N/A')
            result['user_canonical'] = index_status.get('userCanonical', 'N/A')
            
            verdict = result['index_status']
            coverage = result['coverage_state']
            
            # 根據 coverage state 判斷
            if coverage == 'Submitted and indexed':
                result['status'] = 'indexed'
            elif coverage == 'URL is unknown to Google':
                result['status'] = 'not_indexed'
                result['reason'] = 'Google 尚未發現此 URL（需提交 sitemap 或手動要求索引）'
            elif 'Crawled' in coverage and 'not indexed' in coverage:
                result['status'] = 'not_indexed'
                result['reason'] = 'Google 已抓取但未編入索引（內容品質或重複內容問題）'
            elif 'Duplicate' in coverage:
                result['status'] = 'not_indexed'
                result['reason'] = '重複內容，canonical 指向其他頁面'
            else:
                result['status'] = 'unknown'
        
        sitemap_info = inspection.get('sitemapResult', {})
        if sitemap_info:
            result['sitemap'] = sitemap_info.get('sitemap', 'N/A')
        
        return result
        
    except Exception as e:
        return {
            'url': url_path,
            'full_url': full_url,
            'status': 'error',
            'error': str(e)
        }

def print_results(results):
    """格式化輸出結果"""
    print("=" * 100)
    print(f"{'URL':<45} {'索引狀態':<12} {'Coverage State':<25} {'原因/說明'}")
    print("=" * 100)
    
    for r in results:
        url = r['url']
        status = r['status']
        coverage = r.get('coverage_state', 'N/A')
        reason = r.get('reason', '')
        error = r.get('error', '')
        
        if status == 'indexed':
            status_icon = '✅ 已索引'
            reason_text = 'Google 已收錄'
        elif status == 'not_indexed':
            status_icon = '❌ 未索引'
            reason_text = reason or '等待 Google 處理'
        elif status == 'error':
            status_icon = '⚠️ 錯誤'
            reason_text = error[:50]
        else:
            status_icon = '❓ 未知'
            reason_text = coverage
        
        print(f"{url:<45} {status_icon:<12} {coverage:<25} {reason_text}")
    
    print("=" * 100)
    
    indexed = sum(1 for r in results if r['status'] == 'indexed')
    not_indexed = sum(1 for r in results if r['status'] == 'not_indexed')
    errors = sum(1 for r in results if r['status'] == 'error')
    
    print(f"\n📊 統計：已索引 {indexed} / 未索引 {not_indexed} / 錯誤 {errors}")
    
    print("\n📝 建議手動提交建立索引的 URL（未索引且無錯誤）：")
    to_submit = [r for r in results if r['status'] == 'not_indexed']
    if to_submit:
        for r in to_submit:
            print(f"  - {r['full_url']}")
    else:
        print("  （無）")

if __name__ == '__main__':
    print("=" * 100)
    print("Google Search Console URL Inspection v1 - fun1399.com")
    print("=" * 100)
    
    service = get_gsc_service_v1()
    print(f"API 類型: {type(service).__name__}")
    
    results = []
    for url_path in URLS_TO_CHECK:
        print(f"檢查中: {url_path} ...")
        result = inspect_url(service, url_path)
        results.append(result)
    
    print_results(results)
