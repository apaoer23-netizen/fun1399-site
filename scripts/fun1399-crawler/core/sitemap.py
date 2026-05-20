"""
Sitemap parser module for FUN1399 SEO Crawler
Parses sitemap.xml and validates URL consistency
"""
import xml.etree.ElementTree as ET
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse
import aiohttp


class SitemapParser:
    """Parse sitemap.xml and provide URL lists"""
    
    NS = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
    
    async def parse(self, sitemap_url: str) -> Dict[str, any]:
        """
        Fetch and parse sitemap.xml
        Returns dict with urls, count, and errors
        """
        result = {
            "sitemap_url": sitemap_url,
            "urls": [],
            "count": 0,
            "error": None,
            "lastmod_dates": [],
        }
        
        try:
            async with self.session.get(sitemap_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
                if resp.status != 200:
                    result["error"] = f"HTTP {resp.status}"
                    return result
                
                content = await resp.text()
                
                # Check if it's a sitemap index
                if '<sitemapindex' in content:
                    result["error"] = "Sitemap index not yet supported"
                    return result
                
                root = ET.fromstring(content)
                
                # Handle both namespaced and non-namespaced
                urls = root.findall('.//ns:loc', self.NS) or root.findall('.//loc')
                lastmods = root.findall('.//ns:lastmod', self.NS) or root.findall('.//lastmod')
                
                for i, loc in enumerate(urls):
                    url = loc.text.strip() if loc.text else ""
                    if url:
                        result["urls"].append(url)
                        
                        if i < len(lastmods) and lastmods[i].text:
                            result["lastmod_dates"].append(lastmods[i].text.strip())
                
                result["count"] = len(result["urls"])
                
        except ET.ParseError as e:
            result["error"] = f"XML parse error: {str(e)}"
        except Exception as e:
            result["error"] = f"Fetch error: {str(e)}"
        
        return result
    
    def find_orphans(self, sitemap_urls: Set[str], crawled_urls: Set[str]) -> Dict[str, List[str]]:
        """
        Find URL inconsistencies between sitemap and crawl
        """
        sitemap_set = set(sitemap_urls)
        crawled_set = set(crawled_urls)
        
        return {
            "in_sitemap_not_crawled": list(sitemap_set - crawled_set),
            "crawled_not_in_sitemap": list(crawled_set - sitemap_set),
            "total_sitemap": len(sitemap_set),
            "total_crawled": len(crawled_set),
            "matched": len(sitemap_set & crawled_set),
        }