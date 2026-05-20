"""
Markdown Report Generator for FUN1399 SEO Crawler
"""
from typing import Dict, List, Any
from datetime import datetime


class MarkdownReporter:
    """Generate human-readable Markdown SEO reports"""
    
    def generate(self, crawl_result: Dict[str, Any]) -> str:
        """Generate full Markdown report from crawl results"""
        lines = []
        
        # Header
        lines.extend(self._header(crawl_result))
        lines.append("")
        
        # Summary
        lines.extend(self._summary(crawl_result))
        lines.append("")
        
        # Critical Issues
        critical = self._get_issues_by_severity(crawl_result, "critical")
        if critical:
            lines.extend(self._issues_section("🚨 Critical Issues", critical))
            lines.append("")
        
        # Warnings
        warnings = self._get_issues_by_severity(crawl_result, "warning")
        if warnings:
            lines.extend(self._issues_section("⚠️ Warnings", warnings))
            lines.append("")
        
        # Info
        infos = self._get_issues_by_severity(crawl_result, "info")
        if infos:
            lines.extend(self._issues_section("ℹ️ Info", infos))
            lines.append("")
        
        # Statistics
        lines.extend(self._statistics(crawl_result))
        lines.append("")
        
        # Orphan Pages
        orphans = crawl_result.get("orphan_pages", [])
        if orphans:
            lines.extend(self._orphan_pages(orphans))
            lines.append("")
        
        # Redirect Summary
        redirect_summary = crawl_result.get("redirect_summary", {})
        if redirect_summary:
            lines.extend(self._redirect_summary(redirect_summary))
            lines.append("")
        
        # Link Stats
        link_stats = crawl_result.get("link_stats", {})
        if link_stats:
            lines.extend(self._link_stats(link_stats))
            lines.append("")
        
        # Sitemap Consistency
        sitemap_audit = crawl_result.get("sitemap_audit", {})
        if sitemap_audit:
            lines.extend(self._sitemap_consistency(sitemap_audit))
            lines.append("")
        
        # Footer
        lines.extend(self._footer())
        
        return "\n".join(lines)
    
    def _header(self, result: Dict[str, Any]) -> List[str]:
        return [
            "# FUN1399 SEO Crawl Report",
            "",
            f"**Date**: {result.get('date', datetime.now().strftime('%Y-%m-%d %H:%M'))} CST",
            f"**Target**: {result.get('base_url', 'Unknown')}",
            f"**Pages Crawled**: {result.get('pages_crawled', 0)}",
            f"**Duration**: {result.get('duration', 0):.1f}s",
        ]
    
    def _summary(self, result: Dict[str, Any]) -> List[str]:
        counts = result.get("issue_counts", {})
        return [
            "## 📊 Summary",
            "",
            f"| Severity | Count |",
            f"|----------|-------|",
            f"| 🚨 Critical | {counts.get('critical', 0)} |",
            f"| ⚠️ Warning | {counts.get('warning', 0)} |",
            f"| ℹ️ Info | {counts.get('info', 0)} |",
            f"| ✅ Pass | {counts.get('pass', 0)} |",
        ]
    
    def _get_issues_by_severity(self, result: Dict[str, Any], severity: str) -> List[Dict[str, Any]]:
        all_issues = result.get("all_issues", [])
        return [i for i in all_issues if i.get("severity") == severity]
    
    def _issues_section(self, title: str, issues: List[Dict[str, Any]]) -> List[str]:
        lines = [f"## {title} ({len(issues)})", ""]
        
        for i, issue in enumerate(issues, 1):
            lines.extend([
                f"### {i}. {issue.get('type', 'Unknown')} — {issue.get('url', 'Unknown')[-60:]}",
                f"- **Message**: {issue.get('message', 'No details')}",
            ])
            if issue.get("fix"):
                lines.append(f"- **Fix**: {issue['fix']}")
            lines.append("")
        
        return lines
    
    def _statistics(self, result: Dict[str, Any]) -> List[str]:
        stats = result.get("statistics", {})
        return [
            "## 📈 Statistics",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Avg Load Time | {stats.get('avg_load_time', 0):.2f}s |",
            f"| Max Load Time | {stats.get('max_load_time', 0):.2f}s |",
            f"| Avg HTML Size | {stats.get('avg_html_size', 0):.1f} KB |",
            f"| Total Images | {stats.get('total_images', 0)} |",
            f"| Images w/o Alt | {stats.get('images_without_alt', 0)} |",
            f"| Total Internal Links | {stats.get('total_internal_links', 0)} |",
            f"| Broken Links | {stats.get('broken_links', 0)} |",
            f"| Pages with Schema | {stats.get('pages_with_schema', 0)} |",
            f"| Pages with OG | {stats.get('pages_with_og', 0)} |",
        ]
    
    def _orphan_pages(self, orphans: List[Dict[str, Any]]) -> List[str]:
        lines = ["## 🔗 Orphan Pages", ""]
        lines.append("| # | URL | Issue |")
        lines.append("|---|-----|-------|")
        
        for i, orphan in enumerate(orphans[:20], 1):  # Limit to 20
            url = orphan.get("url", "")[-70:]
            lines.append(f"| {i} | {url} | {orphan.get('issue', '')} |")
        
        if len(orphans) > 20:
            lines.append(f"| ... | ... | +{len(orphans) - 20} more |")
        
        return lines
    
    def _redirect_summary(self, summary: Dict[str, Any]) -> List[str]:
        lines = ["## 🔀 Redirect Summary", ""]
        lines.append("| Type | Count |")
        lines.append("|------|-------|")
        
        by_status = summary.get("by_status", {})
        for status, count in sorted(by_status.items()):
            lines.append(f"| {status} | {count} |")
        
        lines.append(f"| Chains > 2 hops | {summary.get('chains_found', 0)} |")
        lines.append(f"| Loops | {summary.get('loops_found', 0)} |")
        lines.append(f"| Bad 302s | {summary.get('bad_302_count', 0)} |")
        
        return lines
    
    def _link_stats(self, stats: Dict[str, Any]) -> List[str]:
        return [
            "## 🔗 Link Statistics",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Total Pages | {stats.get('total_pages', 0)} |",
            f"| Total Links | {stats.get('total_links', 0)} |",
            f"| Avg Out Degree | {stats.get('avg_out_degree', 0):.1f} |",
            f"| Avg In Degree | {stats.get('avg_in_degree', 0):.1f} |",
        ]
    
    def _sitemap_consistency(self, audit: Dict[str, Any]) -> List[str]:
        lines = [
            "## 📋 Sitemap Consistency",
            "",
            "| Metric | Value |",
            "|--------|-------|",
            f"| Sitemap URLs | {audit.get('total_sitemap', 0)} |",
            f"| Crawled URLs | {audit.get('total_crawled', 0)} |",
            f"| Matched | {audit.get('matched', 0)} |",
        ]
        
        not_crawled = audit.get("in_sitemap_not_crawled", [])
        if not_crawled:
            lines.append(f"| In Sitemap but Not Crawled | {len(not_crawled)} |")
            lines.append("")
            lines.append("### In Sitemap but Not Crawled")
            for url in not_crawled[:10]:
                lines.append(f"- {url}")
        
        not_in_sitemap = audit.get("crawled_not_in_sitemap", [])
        if not_in_sitemap:
            lines.append(f"| Crawled but Not in Sitemap | {len(not_in_sitemap)} |")
            lines.append("")
            lines.append("### Crawled but Not in Sitemap")
            for url in not_in_sitemap[:10]:
                lines.append(f"- {url}")
        
        return lines
    
    def _footer(self) -> List[str]:
        return [
            "---",
            "",
            f"*Generated by FUN1399 SEO Crawler v1.0*",
            f"*Report time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CST*",
        ]