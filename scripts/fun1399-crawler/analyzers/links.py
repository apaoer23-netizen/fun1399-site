"""
Link and Redirect Analyzers for FUN1399 SEO Crawler
Handles internal links, orphan pages, redirect chains
"""
from typing import Dict, List, Set, Any, Optional
from urllib.parse import urlparse, urljoin
import networkx as nx


class LinkAnalyzer:
    """Analyze internal link structure and find issues"""
    
    def __init__(self, base_domain: str):
        self.base_domain = base_domain
        self.link_graph = nx.DiGraph()
        self.pages_data = {}  # url -> page data
    
    def add_page(self, url: str, links: List[Dict[str, Any]], page_data: Dict[str, Any]):
        """Add a page and its links to the graph"""
        self.pages_data[url] = page_data
        self.link_graph.add_node(url)
        
        for link in links:
            if link.get("is_internal"):
                target = link["absolute"]
                # Normalize target URL
                target = self._normalize_url(target)
                self.link_graph.add_edge(url, target)
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for comparison"""
        url = url.rstrip('/')
        if url.endswith('.html'):
            url = url[:-5]
        return url
    
    def find_orphan_pages(self, all_crawled_urls: Set[str]) -> List[Dict[str, Any]]:
        """Find pages with no incoming internal links"""
        orphans = []
        
        for url in all_crawled_urls:
            normalized = self._normalize_url(url)
            in_degree = self.link_graph.in_degree(normalized) if normalized in self.link_graph else 0
            
            if in_degree == 0 and url != f"https://{self.base_domain}/":
                orphans.append({
                    "url": url,
                    "issue": "No internal links point to this page",
                    "severity": "warning",
                })
        
        return orphans
    
    def find_broken_links(self, all_urls_status: Dict[str, int]) -> List[Dict[str, Any]]:
        """Find internal links that return 404 or 500"""
        broken = []
        
        for edge in self.link_graph.edges():
            target = edge[1]
            status = all_urls_status.get(target)
            
            if status and status >= 400:
                broken.append({
                    "source": edge[0],
                    "target": target,
                    "status": status,
                    "severity": "critical" if status == 404 else "warning",
                })
        
        return broken
    
    def get_link_stats(self) -> Dict[str, Any]:
        """Get overall link statistics"""
        return {
            "total_pages": self.link_graph.number_of_nodes(),
            "total_links": self.link_graph.number_of_edges(),
            "avg_out_degree": sum(dict(self.link_graph.out_degree()).values()) / max(self.link_graph.number_of_nodes(), 1),
            "avg_in_degree": sum(dict(self.link_graph.in_degree()).values()) / max(self.link_graph.number_of_nodes(), 1),
        }
    
    def check_team_links(self) -> Dict[str, Any]:
        """Check /team page internal links"""
        team_url = f"https://{self.base_domain}/team.html"
        team_normalized = self._normalize_url(team_url)
        
        in_degree = self.link_graph.in_degree(team_normalized) if team_normalized in self.link_graph else 0
        
        return {
            "team_url": team_url,
            "incoming_links": in_degree,
            "status": "good" if in_degree >= 3 else "warning" if in_degree >= 1 else "critical",
            "message": f"/team has {in_degree} incoming internal links",
        }


class RedirectAnalyzer:
    """Analyze redirect chains and loops"""
    
    def __init__(self):
        self.redirects = {}  # url -> redirect info
    
    def add_redirect(self, url: str, status: int, location: Optional[str] = None, chain: Optional[List[Dict]] = None):
        """Record redirect information"""
        self.redirects[url] = {
            "status": status,
            "location": location,
            "chain": chain or [],
        }
    
    def find_chains(self) -> List[Dict[str, Any]]:
        """Find redirect chains longer than 2 hops"""
        chains = []
        
        for url, info in self.redirects.items():
            chain = info.get("chain", [])
            if len(chain) > 2:
                chains.append({
                    "source": url,
                    "hops": len(chain),
                    "chain": [c.get("url", c.get("from", "unknown")) for c in chain],
                    "severity": "warning",
                    "message": f"Redirect chain has {len(chain)} hops (recommended <= 2)",
                })
        
        return chains
    
    def find_loops(self) -> List[Dict[str, Any]]:
        """Find redirect loops (A -> B -> A)"""
        loops = []
        
        for url, info in self.redirects.items():
            chain = info.get("chain", [])
            urls_in_chain = [c.get("url", c.get("from", "")) for c in chain]
            
            # Check for duplicates in chain
            seen = set()
            for u in urls_in_chain:
                if u in seen:
                    loops.append({
                        "source": url,
                        "loop_at": u,
                        "severity": "critical",
                        "message": f"Redirect loop detected at {u}",
                    })
                    break
                seen.add(u)
        
        return loops
    
    def check_302_redirects(self) -> List[Dict[str, Any]]:
        """Find 302 redirects (should be 301 for SEO)"""
        bad_redirects = []
        
        for url, info in self.redirects.items():
            if info["status"] == 302:
                bad_redirects.append({
                    "source": url,
                    "status": 302,
                    "severity": "warning",
                    "message": "302 redirect found (should be 301 for permanent redirects)",
                })
        
        return bad_redirects
    
    def get_summary(self) -> Dict[str, Any]:
        """Get redirect summary statistics"""
        status_counts = {}
        for info in self.redirects.values():
            status = info["status"]
            status_counts[status] = status_counts.get(status, 0) + 1
        
        return {
            "total_redirects": len(self.redirects),
            "by_status": status_counts,
            "chains_found": len(self.find_chains()),
            "loops_found": len(self.find_loops()),
            "bad_302_count": len(self.check_302_redirects()),
        }
