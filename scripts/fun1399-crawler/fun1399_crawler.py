#!/usr/bin/env python3
"""
FUN1399 SEO Crawler - Main Entry Point
Crawls website, checks SEO elements, and generates reports

Usage:
    python3 fun1399_crawler.py https://fun1399.com
    python3 fun1399_crawler.py https://fun1399.com --mode=fast
    python3 fun1399_crawler.py https://fun1399.com --sitemap-only
    python3 fun1399_crawler.py https://fun1399.com --output=report.md
"""
import asyncio
import argparse
import sys
import time
from typing import Dict, List, Set, Any, Optional
from urllib.parse import urlparse, urljoin
from datetime import datetime
import aiohttp

# Add project path
sys.path.insert(0, '/root/.openclaw/workspace/scripts/fun1399-crawler')

from core.fetcher import Fetcher
from core.parser import HTMLParser
from core.sitemap import SitemapParser
from inspectors.seo import SEOInspector
from analyzers.links import LinkAnalyzer, RedirectAnalyzer
from reporters.markdown import MarkdownReporter


class Fun1399Crawler:
    """Main crawler orchestrator"""
    
    def __init__(self, base_url: str, rate_limit: float = 0.33, max_pages: int = 200):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.rate_limit = rate_limit
        self.max_pages = max_pages
        self.results = {}  # url -> page data
        self.all_urls = set()
        self.sitemap_urls = set()
        self.link_analyzer = LinkAnalyzer(self.domain)
        self.redirect_analyzer = RedirectAnalyzer()
    
    async def crawl(self, mode: str = "full") -> Dict[str, Any]:
        """
        Main crawl method
        mode: "fast" (sitemap only), "full" (sitemap + recursive), "single" (just base URL)
        """
        start_time = time.time()
        
        async with Fetcher(rate_limit=self.rate_limit) as fetcher:
            self.fetcher = fetcher
            
            # Step 1: Parse sitemap
            await self._parse_sitemap()
            
            # Step 2: Determine URLs to crawl
            urls_to_crawl = set()
            
            if mode == "single":
                urls_to_crawl = {self.base_url}
            elif mode == "fast":
                urls_to_crawl = self.sitemap_urls.copy()
            else:  # full mode
                urls_to_crawl = self.sitemap_urls.copy()
                # Add recursive discovery
                discovered = await self._discover_urls()
                urls_to_crawl.update(discovered)
            
            # Limit max pages
            urls_to_crawl = set(list(urls_to_crawl)[:self.max_pages])
            self.all_urls = urls_to_crawl
            
            print(f"[*] Crawling {len(urls_to_crawl)} pages...")
            
            # Step 3: Fetch all pages
            await self._fetch_all_pages(urls_to_crawl)
            
            # Step 4: Check redirects for key URLs
            await self._check_redirects()
            
            # Step 5: Check images (HEAD requests)
            if mode == "full":
                await self._check_images()
        
        duration = time.time() - start_time
        
        # Generate report
        return self._generate_result(duration)
    
    async def _parse_sitemap(self):
        """Parse sitemap.xml"""
        sitemap_url = f"{self.base_url}/sitemap.xml"
        
        async with aiohttp.ClientSession() as session:
            parser = SitemapParser(session)
            result = await parser.parse(sitemap_url)
            
            if result["urls"]:
                self.sitemap_urls = set(result["urls"])
                print(f"[+] Sitemap: {result['count']} URLs found")
            else:
                print(f"[-] Sitemap error: {result.get('error', 'Unknown')}")
    
    async def _discover_urls(self) -> Set[str]:
        """Recursively discover internal URLs from already fetched pages"""
        discovered = set()
        
        # Start with sitemap URLs and discover from each
        to_check = list(self.sitemap_urls)[:20]  # Limit discovery to first 20
        
        for url in to_check:
            result = self.results.get(url)
            if result and result.get("internal_links"):
                for link in result["internal_links"]:
                    if link.get("is_internal"):
                        abs_url = link["absolute"]
                        # Normalize
                        if abs_url.endswith('/'):
                            abs_url = abs_url[:-1]
                        # Only add HTML pages and root
                        if abs_url.endswith('.html') or abs_url == self.base_url:
                            discovered.add(abs_url)
        
        return discovered
    
    async def _fetch_all_pages(self, urls: Set[str]):
        """Fetch all pages concurrently with rate limiting"""
        tasks = [self._fetch_single(url) for url in urls]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _fetch_single(self, url: str):
        """Fetch and parse a single page"""
        try:
            result = await self.fetcher.fetch(url)
            
            page_data = {
                "url": url,
                "status": result.get("status"),
                "load_time": result.get("load_time", 0),
                "error": result.get("error"),
                "redirect_chain": result.get("redirect_chain", []),
                "final_url": result.get("final_url", url),
            }
            
            if result.get("content") and result.get("status") == 200:
                parser = HTMLParser(result["content"], url)
                
                page_data.update({
                    "meta": parser.extract_meta(),
                    "og": parser.extract_og(),
                    "twitter": parser.extract_twitter(),
                    "canonical": parser.extract_canonical(),
                    "headings": parser.extract_headings(),
                    "schema": parser.extract_schema(),
                    "internal_links": parser.extract_internal_links(),
                    "images": parser.extract_images(),
                    "html_size": parser.get_page_size(),
                })
                
                # Add to link analyzer
                self.link_analyzer.add_page(
                    url,
                    page_data.get("internal_links", []),
                    page_data
                )
            
            self.results[url] = page_data
            
            # Record redirect info
            if result.get("redirect_chain"):
                self.redirect_analyzer.add_redirect(
                    url,
                    result.get("status", 0),
                    chain=result["redirect_chain"]
                )
            
        except Exception as e:
            self.results[url] = {
                "url": url,
                "status": None,
                "error": str(e),
            }
    
    async def _check_redirects(self):
        """Check redirects for common patterns"""
        test_urls = [
            f"{self.base_url}/team",
            f"{self.base_url}/articles/mbm-review",
            f"http://{self.domain}",
            f"https://www.{self.domain}",
        ]
        
        for url in test_urls:
            try:
                result = await self.fetcher.fetch_head(url)
                if result.get("status") in (301, 302, 307, 308):
                    self.redirect_analyzer.add_redirect(
                        url,
                        result["status"],
                        result["headers"].get("Location"),
                        result.get("redirect_chain", [])
                    )
            except:
                pass
    
    async def _check_images(self):
        """Check image URLs return 200"""
        image_urls = set()
        for page in self.results.values():
            for img in page.get("images", []):
                src = img.get("src")
                if src and src.startswith("http"):
                    image_urls.add(src)
        
        # Limit to first 50 images
        image_urls = set(list(image_urls)[:50])
        
        image_status = {}
        for img_url in image_urls:
            try:
                result = await self.fetcher.fetch_head(img_url)
                image_status[img_url] = result.get("status", 0)
            except:
                image_status[img_url] = 0
        
        # Store image status in results
        for page in self.results.values():
            for img in page.get("images", []):
                src = img.get("src")
                if src in image_status:
                    img["http_status"] = image_status[src]
    
    def _generate_result(self, duration: float) -> Dict[str, Any]:
        """Generate final crawl result with all analysis"""
        
        # Run SEO checks on all pages
        all_issues = []
        page_checks = []
        
        for url, page_data in self.results.items():
            if page_data.get("status") == 200:
                inspector = SEOInspector(page_data)
                checks = inspector.run_all_checks()
                page_checks.append(checks)
                
                # Collect issues
                for check_name, check_data in checks.items():
                    if isinstance(check_data, dict) and "issues" in check_data:
                        for issue in check_data["issues"]:
                            issue["url"] = url
                            issue["check"] = check_name
                            all_issues.append(issue)
        
        # Calculate statistics
        total_pages = len(self.results)
        successful_pages = sum(1 for p in self.results.values() if p.get("status") == 200)
        
        load_times = [p.get("load_time", 0) for p in self.results.values() if p.get("status") == 200]
        html_sizes = [p.get("html_size", 0) for p in self.results.values() if p.get("status") == 200]
        
        total_images = sum(len(p.get("images", [])) for p in self.results.values())
        images_without_alt = sum(
            sum(1 for img in p.get("images", []) if not img.get("has_alt", False))
            for p in self.results.values()
        )
        
        pages_with_schema = sum(1 for p in page_checks if p.get("schema", {}).get("schema_count", 0) > 0)
        pages_with_og = sum(1 for p in page_checks if p.get("og", {}).get("has_og_image", False))
        
        # Count issues
        issue_counts = {
            "critical": sum(1 for i in all_issues if i.get("severity") == "critical"),
            "warning": sum(1 for i in all_issues if i.get("severity") == "warning"),
            "info": sum(1 for i in all_issues if i.get("severity") == "info"),
            "pass": successful_pages - len(all_issues),
        }
        
        # Sitemap audit
        sitemap_audit = {}
        if self.sitemap_urls:
            from core.sitemap import SitemapParser
            sitemap_audit = SitemapParser(None).find_orphans(
                self.sitemap_urls,
                set(self.results.keys())
            )
        
        # Orphan pages
        orphan_pages = []
        if self.all_urls:
            orphan_pages = self.link_analyzer.find_orphan_pages(self.all_urls)
        
        # Link stats
        link_stats = self.link_analyzer.get_link_stats()
        
        # Team links check
        team_check = self.link_analyzer.check_team_links()
        
        # Redirect summary
        redirect_summary = self.redirect_analyzer.get_summary()
        
        # Broken links
        url_status = {url: data.get("status", 0) for url, data in self.results.items()}
        broken_links = self.link_analyzer.find_broken_links(url_status)
        
        return {
            "base_url": self.base_url,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "pages_crawled": total_pages,
            "successful_pages": successful_pages,
            "duration": duration,
            "issue_counts": issue_counts,
            "all_issues": all_issues,
            "statistics": {
                "avg_load_time": sum(load_times) / max(len(load_times), 1),
                "max_load_time": max(load_times) if load_times else 0,
                "avg_html_size": sum(html_sizes) / max(len(html_sizes), 1) / 1024,
                "total_images": total_images,
                "images_without_alt": images_without_alt,
                "total_internal_links": link_stats.get("total_links", 0),
                "broken_links": len(broken_links),
                "pages_with_schema": pages_with_schema,
                "pages_with_og": pages_with_og,
            },
            "orphan_pages": orphan_pages,
            "redirect_summary": redirect_summary,
            "link_stats": link_stats,
            "sitemap_audit": sitemap_audit,
            "team_links": team_check,
            "page_details": page_checks[:5],  # First 5 pages for detail
        }


def main():
    parser = argparse.ArgumentParser(description="FUN1399 SEO Crawler")
    parser.add_argument("url", help="Base URL to crawl")
    parser.add_argument("--mode", choices=["fast", "full", "single"], default="full",
                       help="Crawl mode: fast (sitemap only), full (sitemap + discovery), single (just one page)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--rate-limit", type=float, default=0.33,
                       help="Seconds between requests (default: 0.33 = ~3 req/sec)")
    parser.add_argument("--max-pages", type=int, default=200,
                       help="Maximum pages to crawl")
    
    args = parser.parse_args()
    
    # Ensure URL has scheme
    url = args.url
    if not url.startswith("http"):
        url = f"https://{url}"
    
    print(f"[*] FUN1399 SEO Crawler v1.0")
    print(f"[*] Target: {url}")
    print(f"[*] Mode: {args.mode}")
    print(f"[*] Rate limit: {args.rate_limit}s between requests")
    print()
    
    # Run crawl
    crawler = Fun1399Crawler(url, rate_limit=args.rate_limit, max_pages=args.max_pages)
    result = asyncio.run(crawler.crawl(mode=args.mode))
    
    # Generate report
    reporter = MarkdownReporter()
    report = reporter.generate(result)
    
    # Output
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n[+] Report saved to: {args.output}")
    else:
        print("\n" + "=" * 60)
        print(report)
        print("=" * 60)
    
    # Print summary
    counts = result.get("issue_counts", {})
    print(f"\n[*] Summary:")
    print(f"    Pages crawled: {result['pages_crawled']}")
    print(f"    Duration: {result['duration']:.1f}s")
    print(f"    Critical: {counts.get('critical', 0)}")
    print(f"    Warnings: {counts.get('warning', 0)}")
    print(f"    Info: {counts.get('info', 0)}")
    
    # Exit code
    critical_count = counts.get('critical', 0)
    if critical_count > 0:
        print(f"\n[!] Found {critical_count} critical issues")
        sys.exit(1)
    else:
        print(f"\n[+] No critical issues found")
        sys.exit(0)


if __name__ == "__main__":
    main()
