"""
SEO Inspectors module for FUN1399 SEO Crawler
Checks meta tags, canonical, schema, OG, Twitter Card
"""
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


class SEOInspector:
    """Inspect SEO elements from parsed page data"""
    
    def __init__(self, page_data: Dict[str, Any]):
        self.page = page_data
        self.url = page_data.get("url", "")
        self.domain = urlparse(self.url).netloc
        self.issues = []
    
    def check_meta(self) -> Dict[str, Any]:
        """Check title, description, viewport, robots meta"""
        meta = self.page.get("meta", {})
        result = {
            "title": meta.get("title"),
            "title_length": len(meta.get("title", "")) if meta.get("title") else 0,
            "description": meta.get("description"),
            "description_length": len(meta.get("description", "")) if meta.get("description") else 0,
            "viewport": meta.get("viewport"),
            "robots_meta": meta.get("robots"),
            "issues": [],
        }
        
        # Title checks
        title = meta.get("title", "")
        if not title:
            result["issues"].append({"severity": "critical", "type": "missing_title", "message": "Title tag is missing"})
        elif len(title) > 60:
            result["issues"].append({"severity": "warning", "type": "title_too_long", "message": f"Title is {len(title)} chars (recommended <= 60)"})
        elif len(title) < 10:
            result["issues"].append({"severity": "warning", "type": "title_too_short", "message": f"Title is only {len(title)} chars"})
        
        # Description checks
        desc = meta.get("description", "")
        if not desc:
            result["issues"].append({"severity": "warning", "type": "missing_description", "message": "Meta description is missing"})
        elif len(desc) > 160:
            result["issues"].append({"severity": "warning", "type": "description_too_long", "message": f"Description is {len(desc)} chars (recommended <= 160)"})
        
        # Viewport check
        if not meta.get("viewport"):
            result["issues"].append({"severity": "critical", "type": "missing_viewport", "message": "Viewport meta tag is missing (mobile issue)"})
        
        # Robots meta check
        robots = meta.get("robots", "")
        if robots:
            if "noindex" in robots.lower():
                result["issues"].append({"severity": "info", "type": "noindex_set", "message": f"Page has noindex: {robots}"})
            if "nofollow" in robots.lower():
                result["issues"].append({"severity": "info", "type": "nofollow_set", "message": f"Page has nofollow: {robots}"})
        
        return result
    
    def check_og(self) -> Dict[str, Any]:
        """Check Open Graph tags"""
        og = self.page.get("og", {})
        result = {
            "tags_present": og,
            "has_og_title": bool(og.get("title")),
            "has_og_description": bool(og.get("description")),
            "has_og_image": bool(og.get("image")),
            "has_og_url": bool(og.get("url")),
            "issues": [],
        }
        
        required = ["title", "description", "image", "url"]
        for tag in required:
            if not og.get(tag):
                result["issues"].append({"severity": "warning", "type": f"missing_og_{tag}", "message": f"Missing og:{tag}"})
        
        return result
    
    def check_twitter(self) -> Dict[str, Any]:
        """Check Twitter Card tags"""
        twitter = self.page.get("twitter", {})
        result = {
            "tags_present": twitter,
            "has_card": bool(twitter.get("card")),
            "has_title": bool(twitter.get("title")),
            "has_image": bool(twitter.get("image")),
            "issues": [],
        }
        
        if not twitter.get("card"):
            result["issues"].append({"severity": "warning", "type": "missing_twitter_card", "message": "Missing twitter:card"})
        
        return result
    
    def check_canonical(self) -> Dict[str, Any]:
        """Check canonical URL"""
        canonical = self.page.get("canonical")
        result = {
            "canonical": canonical,
            "is_self_referencing": False,
            "issues": [],
        }
        
        if not canonical:
            result["issues"].append({"severity": "critical", "type": "missing_canonical", "message": "Canonical URL is missing"})
            return result
        
        # Self-referencing check
        # Normalize URLs for comparison
        def normalize(url):
            url = url.rstrip('/')
            if url.endswith('.html'):
                url = url[:-5]
            return url
        
        if normalize(canonical) == normalize(self.url):
            result["is_self_referencing"] = True
        else:
            result["issues"].append({"severity": "warning", "type": "canonical_mismatch", "message": f"Canonical ({canonical}) doesn't match URL ({self.url})"})
        
        # HTTPS check
        if canonical and not canonical.startswith("https://"):
            result["issues"].append({"severity": "warning", "type": "canonical_not_https", "message": "Canonical URL is not HTTPS"})
        
        # WWW vs apex check
        parsed_canonical = urlparse(canonical)
        if parsed_canonical.netloc.startswith("www."):
            result["issues"].append({"severity": "info", "type": "canonical_has_www", "message": "Canonical uses www (verify this is intended)"})
        
        return result
    
    def check_headings(self) -> Dict[str, Any]:
        """Check heading structure"""
        headings = self.page.get("headings", {})
        h1s = headings.get("h1", [])
        
        result = {
            "h1_count": len(h1s),
            "h1_texts": h1s,
            "h2_count": len(headings.get("h2", [])),
            "issues": [],
        }
        
        if len(h1s) == 0:
            result["issues"].append({"severity": "critical", "type": "missing_h1", "message": "No H1 tag found"})
        elif len(h1s) > 1:
            result["issues"].append({"severity": "warning", "type": "multiple_h1", "message": f"Found {len(h1s)} H1 tags (recommended: 1)"})
        
        return result
    
    def check_schema(self) -> Dict[str, Any]:
        """Check JSON-LD schema markup"""
        schemas = self.page.get("schema", [])
        result = {
            "schema_count": len(schemas),
            "schema_types": [],
            "has_article": False,
            "has_organization": False,
            "has_website": False,
            "has_faq": False,
            "issues": [],
        }
        
        if not schemas:
            result["issues"].append({"severity": "warning", "type": "missing_schema", "message": "No JSON-LD schema found"})
            return result
        
        for schema in schemas:
            if isinstance(schema, dict):
                schema_type = schema.get("@type", "Unknown")
                if isinstance(schema_type, list):
                    schema_type = schema_type[0]
                result["schema_types"].append(schema_type)
                
                if schema_type == "Article":
                    result["has_article"] = True
                elif schema_type == "Organization":
                    result["has_organization"] = True
                elif schema_type == "WebSite":
                    result["has_website"] = True
                elif schema_type == "FAQPage":
                    result["has_faq"] = True
                
                # Check for errors
                if "_error" in schema:
                    result["issues"].append({"severity": "warning", "type": "invalid_schema", "message": schema.get("_error", "Invalid JSON-LD")})
        
        return result
    
    def check_images(self) -> Dict[str, Any]:
        """Check image alt tags"""
        images = self.page.get("images", [])
        result = {
            "total_images": len(images),
            "images_without_alt": 0,
            "images_list": [],
            "issues": [],
        }
        
        for img in images[:20]:  # Limit to first 20 for brevity
            result["images_list"].append({
                "src": img.get("src", "")[-80:],  # Truncate for brevity
                "has_alt": img.get("has_alt", False),
                "alt": img.get("alt", "")[:50],
            })
            
            if not img.get("has_alt", False):
                result["images_without_alt"] += 1
        
        if result["images_without_alt"] > 0:
            result["issues"].append({"severity": "warning", "type": "images_without_alt", "message": f"{result['images_without_alt']} images missing alt text"})
        
        return result
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all SEO checks and return combined results"""
        return {
            "url": self.url,
            "status": self.page.get("status"),
            "meta": self.check_meta(),
            "og": self.check_og(),
            "twitter": self.check_twitter(),
            "canonical": self.check_canonical(),
            "headings": self.check_headings(),
            "schema": self.check_schema(),
            "images": self.check_images(),
            "load_time": self.page.get("load_time", 0),
            "html_size": self.page.get("html_size", 0),
        }
