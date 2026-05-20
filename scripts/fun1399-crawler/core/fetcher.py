"""
Core fetcher module for FUN1399 SEO Crawler
Handles HTTP requests with asyncio, rate limiting, and retry logic
"""
import asyncio
import aiohttp
import time
from typing import Optional, Tuple, Dict, Any
from urllib.parse import urljoin, urlparse


class Fetcher:
    """Async HTTP fetcher with rate limiting and Googlebot UA"""
    
    GOOGLEBOT_UA = (
        "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    )
    
    def __init__(self, rate_limit: float = 0.33, timeout: int = 30, max_retries: int = 2):
        """
        rate_limit: minimum seconds between requests (0.33 = ~3 req/sec)
        timeout: request timeout in seconds
        max_retries: number of retries on failure
        """
        self.rate_limit = rate_limit
        self.timeout = timeout
        self.max_retries = max_retries
        self.last_request_time = 0
        self.session: Optional[aiohttp.ClientSession] = None
        self._semaphore = asyncio.Semaphore(5)  # max concurrent requests
    
    async def __aenter__(self):
        connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": self.GOOGLEBOT_UA}
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _rate_limited_request(self, url: str, allow_redirects: bool = True) -> Tuple[Optional[aiohttp.ClientResponse], Optional[str], float]:
        """Execute rate-limited request"""
        async with self._semaphore:
            # Rate limiting
            now = time.time()
            elapsed = now - self.last_request_time
            if elapsed < self.rate_limit:
                await asyncio.sleep(self.rate_limit - elapsed)
            
            self.last_request_time = time.time()
            
            for attempt in range(self.max_retries + 1):
                try:
                    start = time.time()
                    async with self.session.get(url, allow_redirects=allow_redirects) as resp:
                        load_time = time.time() - start
                        
                        # Read content for non-redirect responses
                        if resp.status < 300 or resp.status >= 400:
                            try:
                                content = await resp.text()
                            except:
                                content = None
                        else:
                            content = None
                        
                        return resp, content, load_time
                        
                except asyncio.TimeoutError:
                    if attempt < self.max_retries:
                        await asyncio.sleep(1 * (attempt + 1))
                        continue
                    return None, None, 0.0
                except Exception as e:
                    if attempt < self.max_retries:
                        await asyncio.sleep(1 * (attempt + 1))
                        continue
                    return None, None, 0.0
            
            return None, None, 0.0
    
    async def fetch(self, url: str, allow_redirects: bool = True) -> Dict[str, Any]:
        """
        Fetch URL and return structured result
        """
        result = {
            "url": url,
            "status": None,
            "headers": {},
            "content": None,
            "load_time": 0.0,
            "error": None,
            "redirect_chain": [],
            "final_url": url,
        }
        
        resp, content, load_time = await self._rate_limited_request(url, allow_redirects)
        
        if resp is None:
            result["error"] = "Failed to fetch after retries"
            return result
        
        result["status"] = resp.status
        result["load_time"] = load_time
        result["headers"] = dict(resp.headers)
        result["content"] = content
        result["final_url"] = str(resp.url)
        
        # Trace redirect chain
        if hasattr(resp, 'history') and resp.history:
            result["redirect_chain"] = [
                {"url": str(r.url), "status": r.status} 
                for r in resp.history
            ]
            result["redirect_chain"].append({"url": str(resp.url), "status": resp.status})
        
        return result
    
    async def fetch_head(self, url: str) -> Dict[str, Any]:
        """Fetch HEAD request for redirect tracing"""
        result = {
            "url": url,
            "status": None,
            "headers": {},
            "redirect_chain": [],
            "error": None,
        }
        
        async with self._semaphore:
            now = time.time()
            elapsed = now - self.last_request_time
            if elapsed < self.rate_limit:
                await asyncio.sleep(self.rate_limit - elapsed)
            
            self.last_request_time = time.time()
            
            try:
                async with self.session.head(url, allow_redirects=False) as resp:
                    result["status"] = resp.status
                    result["headers"] = dict(resp.headers)
                    
                    # Follow redirects manually to trace chain
                    if resp.status in (301, 302, 303, 307, 308):
                        location = resp.headers.get("Location")
                        if location:
                            result["redirect_chain"].append({
                                "from": url,
                                "to": urljoin(url, location),
                                "status": resp.status
                            })
            except Exception as e:
                result["error"] = str(e)
        
        return result
