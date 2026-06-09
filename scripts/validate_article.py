#!/usr/bin/env python3
"""
Fun1399 文章模板驗證腳本
用途：檢查生成的文章是否符合 gm1688 標準模板
檢查項目：
  - Header 存在
  - Footer 存在
  - Hero Image 存在
  - CTA 區塊存在（至少3個）
  - FAQ 區塊存在（至少6組）
  - FAQ Schema 存在
  - Article Schema 存在
用法：
  python3 scripts/validate_article.py <article_html_path>
  python3 scripts/validate_article.py build/articles/swag-casino-scam-discussion.html
"""

import sys
import re
from pathlib import Path
from html.parser import HTMLParser


class ArticleValidator:
    def __init__(self, html_path: str):
        self.path = Path(html_path)
        self.html = ""
        self.errors = []
        self.warnings = []
        self.results = {}

    def load(self) -> bool:
        if not self.path.exists():
            self.errors.append(f"❌ 檔案不存在: {self.path}")
            return False
        self.html = self.path.read_text(encoding='utf-8')
        self.results['file_size'] = len(self.html)
        return True

    def check_header(self) -> bool:
        """檢查 Header 是否存在"""
        has_header = '<header class="header"' in self.html or '<header>' in self.html
        if has_header:
            self.results['header'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 Header 區塊")
            self.results['header'] = "❌ 缺失"
        return has_header

    def check_footer(self) -> bool:
        """檢查 Footer 是否存在"""
        has_footer = '<footer class="footer"' in self.html or '<footer>' in self.html
        if has_footer:
            self.results['footer'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 Footer 區塊")
            self.results['footer'] = "❌ 缺失"
        return has_footer

    def check_hero_image(self) -> bool:
        """檢查 Hero 封面圖是否存在"""
        has_hero = 'class="article-hero-image"' in self.html or 'class="hero-image"' in self.html
        if has_hero:
            self.results['hero_image'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 Hero 封面圖")
            self.results['hero_image'] = "❌ 缺失"
        return has_hero

    def check_cta(self) -> bool:
        """檢查 CTA 區塊（至少3個）"""
        cta_count = self.html.count('class="cta-box"')
        self.results['cta_count'] = cta_count
        if cta_count >= 3:
            self.results['cta'] = f"✅ {cta_count} 個"
        elif cta_count >= 1:
            self.warnings.append(f"⚠️ 只有 {cta_count} 個 CTA，建議至少3個")
            self.results['cta'] = f"⚠️ {cta_count} 個"
        else:
            self.errors.append("❌ 缺少 CTA 區塊")
            self.results['cta'] = "❌ 缺失"
        return cta_count >= 1

    def check_faq(self) -> bool:
        """檢查 FAQ 區塊（至少6組）"""
        # 計算 FAQ 問題數量（Q1, Q2... 或 FAQ 標題）
        faq_patterns = [
            r'Q\d+:',  # Q1:, Q2: ...
            r'<h3[^>]*>.*?FAQ.*?</h3>',
            r'常見問題',
        ]
        faq_count = len(re.findall(r'Q\d+:', self.html))
        self.results['faq_count'] = faq_count
        if faq_count >= 6:
            self.results['faq'] = f"✅ {faq_count} 組"
        elif faq_count >= 1:
            self.warnings.append(f"⚠️ 只有 {faq_count} 組 FAQ，建議至少6組")
            self.results['faq'] = f"⚠️ {faq_count} 組"
        else:
            self.errors.append("❌ 缺少 FAQ 區塊")
            self.results['faq'] = "❌ 缺失"
        return faq_count >= 1

    def check_faq_schema(self) -> bool:
        """檢查 FAQPage Schema 是否存在"""
        has_faq_schema = 'FAQPage' in self.html and '"@type": "FAQPage"' in self.html
        if has_faq_schema:
            self.results['faq_schema'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 FAQPage Schema")
            self.results['faq_schema'] = "❌ 缺失"
        return has_faq_schema

    def check_article_schema(self) -> bool:
        """檢查 Article Schema 是否存在"""
        has_article_schema = '"@type": "Article"' in self.html or '"@type":"Article"' in self.html
        if has_article_schema:
            self.results['article_schema'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 Article Schema")
            self.results['article_schema'] = "❌ 缺失"
        return has_article_schema

    def check_css(self) -> bool:
        """檢查 CSS 是否載入"""
        has_css = 'style.css' in self.html or '<style>' in self.html
        if has_css:
            self.results['css'] = "✅ 存在"
        else:
            self.errors.append("❌ 缺少 CSS 載入")
            self.results['css'] = "❌ 缺失"
        return has_css

    def check_breadcrumb(self) -> bool:
        """檢查 Breadcrumb 是否存在"""
        has_breadcrumb = 'BreadcrumbList' in self.html or 'breadcrumb' in self.html.lower()
        if has_breadcrumb:
            self.results['breadcrumb'] = "✅ 存在"
        else:
            self.warnings.append("⚠️ 缺少 Breadcrumb")
            self.results['breadcrumb'] = "⚠️ 缺失"
        return has_breadcrumb

    def check_toc(self) -> bool:
        """檢查目錄 (TOC) 是否存在"""
        has_toc = 'class="toc"' in self.html or '文章目錄' in self.html
        if has_toc:
            self.results['toc'] = "✅ 存在"
        else:
            self.warnings.append("⚠️ 缺少文章目錄")
            self.results['toc'] = "⚠️ 缺失"
        return has_toc

    def check_word_count(self) -> bool:
        """檢查中文字數（至少2500字）"""
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', self.html))
        self.results['chinese_chars'] = chinese_chars
        if chinese_chars >= 2500:
            self.results['word_count'] = f"✅ {chinese_chars} 字"
        elif chinese_chars >= 1000:
            self.warnings.append(f"⚠️ 只有 {chinese_chars} 中文字，建議2500字以上")
            self.results['word_count'] = f"⚠️ {chinese_chars} 字"
        else:
            self.errors.append(f"❌ 內容過少：只有 {chinese_chars} 中文字")
            self.results['word_count'] = f"❌ {chinese_chars} 字"
        return chinese_chars >= 1000

    def check_h2_sections(self) -> bool:
        """檢查 H2 章節數量（至少10個）"""
        h2_count = len(re.findall(r'<h2[^>]*>', self.html))
        self.results['h2_count'] = h2_count
        if h2_count >= 10:
            self.results['h2_sections'] = f"✅ {h2_count} 個 H2"
        elif h2_count >= 5:
            self.warnings.append(f"⚠️ 只有 {h2_count} 個 H2，建議10個")
            self.results['h2_sections'] = f"⚠️ {h2_count} 個 H2"
        else:
            self.errors.append(f"❌ H2 章節過少：只有 {h2_count} 個")
            self.results['h2_sections'] = f"❌ {h2_count} 個 H2"
        return h2_count >= 5

    def check_related_reading(self) -> bool:
        """檢查延伸閱讀區塊"""
        has_related = '延伸閱讀' in self.html or 'related' in self.html.lower()
        if has_related:
            self.results['related_reading'] = "✅ 存在"
        else:
            self.warnings.append("⚠️ 缺少延伸閱讀區塊")
            self.results['related_reading'] = "⚠️ 缺失"
        return has_related

    def validate(self) -> dict:
        """執行所有驗證並回傳結果"""
        if not self.load():
            return {'valid': False, 'errors': self.errors, 'results': self.results}

        self.check_header()
        self.check_footer()
        self.check_css()
        self.check_breadcrumb()
        self.check_hero_image()
        self.check_toc()
        self.check_cta()
        self.check_faq()
        self.check_faq_schema()
        self.check_article_schema()
        self.check_word_count()
        self.check_h2_sections()
        self.check_related_reading()

        is_valid = len(self.errors) == 0
        return {
            'valid': is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'results': self.results
        }

    def print_report(self, result: dict) -> str:
        """印出驗證報告，回傳報告文字"""
        lines = []
        lines.append("=" * 50)
        lines.append(f"📋 文章驗證報告: {self.path.name}")
        lines.append("=" * 50)
        lines.append("")
        
        for key, value in result['results'].items():
            lines.append(f"  {key:<20} {value}")
        
        lines.append("")
        
        if result['errors']:
            lines.append("❌ 錯誤:")
            for err in result['errors']:
                lines.append(f"   {err}")
            lines.append("")
        
        if result['warnings']:
            lines.append("⚠️ 警告:")
            for warn in result['warnings']:
                lines.append(f"   {warn}")
            lines.append("")
        
        if result['valid']:
            lines.append("✅ 驗證通過！文章符合標準模板。")
        else:
            lines.append("❌ 驗證失敗！文章不符合標準模板，請修正後再部署。")
        
        lines.append("=" * 50)
        
        return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_article.py <article_html_path>")
        print("Example: python3 validate_article.py build/articles/swag-casino-scam-discussion.html")
        sys.exit(1)

    path = sys.argv[1]
    validator = ArticleValidator(path)
    result = validator.validate()
    report = validator.print_report(result)
    print(report)

    # 回傳 exit code: 0 = 通過, 1 = 失敗
    sys.exit(0 if result['valid'] else 1)


if __name__ == "__main__":
    main()
