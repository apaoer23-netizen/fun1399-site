"""
HTML Parser module for FUN1399 SEO Crawler
Extracts SEO-relevant elements from HTML content
"""
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse
import json
import re


class HTMLParser:
    """Parse HTML and extract SEO elements"""
    
    def __init__(self, html: str, base_url: str):
        self.soup = BeautifulSoup(html, 'lxml')
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
    
    def extract_meta(self) -> Dict[str, Any]:
        """Extract all meta tags"""
        result = {
            "title": None,
            "description": None,
            "viewport": None,
            "robots": None,
            "charset": None,
        }
        
        # Title
        title_tag = self.soup.find('title')
        if title_tag:
            result["title"] = title_tag.get_text(strip=True)
        
        # Meta tags
        for meta in self.soup.find_all('meta'):
            name = meta.get('name', '').lower()
            prop = meta.get('property', '').lower()
            content = meta.get('content', '')
            
            if name == 'description':
                result["description"] = content
            elif name == 'viewport':
                result["viewport"] = content
            elif name == 'robots':
                result["robots"] = content
            elif name == 'charset' or meta.get('http-equiv', '').lower() == 'content-type':
                charset = meta.get('charset') or content
                if charset:
                    result["charset"] = charset
        
        return result
    
    def extract_og(self) -> Dict[str, Optional[str]]:
        """Extract Open Graph tags"""
        result = {}
        og_tags = ['title', 'description', 'image', 'url', 'type', 'site_name']
        
        for tag in og_tags:
            elem = self.soup.find('meta', property=f'og:{tag}')
            if elem:
                result[tag] = elem.get('content')
        
        return result
    
    def extract_twitter(self) -> Dict[str, Optional[str]]:
        """Extract Twitter Card tags"""
        result = {}
        twitter_tags = ['card', 'title', 'description', 'image']
        
        for tag in twitter_tags:
            elem = self.soup.find('meta', attrs={'name': f'twitter:{tag}'})
            if elem:
                result[tag] = elem.get('content')
        
        return result
    
    def extract_canonical(self) -> Optional[str]:
        """Extract canonical URL"""
        link = self.soup.find('link', rel='canonical')
        if link:
            href = link.get('href')
            if href:
                return urljoin(self.base_url, href)
        return None
    
    def extract_headings(self) -> Dict[str, List[str]]:
        """Extract all headings"""
        result = {}
        for level in range(1, 7):
            tags = self.soup.find_all(f'h{level}')
            result[f'h{level}'] = [tag.get_text(strip=True) for tag in tags]
        return result
    
    def extract_schema(self) -> List[Dict[str, Any]]:
        """Extract JSON-LD schema markup"""
        schemas = []
        scripts = self.soup.find_all('script', type='application/ld+json')
        
        for script in scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, list):
                    schemas.extend(data)
                else:
                    schemas.append(data)
            except (json.JSONDecodeError, TypeError):
                schemas.append({"_error": "Invalid JSON-LD", "_raw": str(script.string)[:200]})
        
        return schemas
    
    def extract_internal_links(self) -> List[Dict[str, Any]]:
        """Extract all internal links"""
        links = []
        
        for a in self.soup.find_all('a', href=True):
            href = a['href']
            absolute = urljoin(self.base_url, href)
            parsed = urlparse(absolute)
            
            # Skip non-HTTP, anchors, mailto, tel
            if parsed.scheme not in ('http', 'https'):
                continue
            if href.startswith('#') or href.startswith('javascript:'):
                continue
            
            is_internal = parsed.netloc == self.domain
            
            links.append({
                "href": href,
                "absolute": absolute,
                "text": a.get_text(strip=True),
                "title": a.get('title'),
                "is_internal": is_internal,
                "is_nofollow": 'nofollow' in a.get('rel', []),
            })
        
        return links
    
    def extract_images(self) -> List[Dict[str, Any]]:
        """Extract all images"""
        images = []
        
        for img in self.soup.find_all('img'):
            src = img.get('src')
            if not src:
                continue
            
            absolute = urljoin(self.base_url, src)
            
            images.append({
                "src": absolute,
                "alt": img.get('alt', ''),
                "width": img.get('width'),
                "height": img.get('height'),
                "has_alt": bool(img.get('alt')),
            })
        
        return images
    
    def get_page_size(self) -> int:
        """Get approximate HTML size in bytes"""
        return len(str(self.soup))
