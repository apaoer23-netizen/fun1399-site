import re

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    content = f.read()

# Known articles with covers
covers = {
    'usdt-casino-scam-2026': '/static/images/articles/scam/usdt-casino-scam-2026-cover.webp',
    'casino-license-verification-2026': '/static/images/articles/scam/casino-license-verification-2026-cover.webp',
    'fake-line-official-account': '/static/images/articles/scam/fake-line-official-account-cover.webp',
    'biwin-casino-no-withdrawal': '/static/images/articles/scam/biwin-casino-no-withdrawal-cover.webp',
    'wealth-god-casino-scam-review': '/static/images/articles/scam/wealth-god-casino-scam-review-cover-v2.webp',
    '3a-casino-scam-review': '/static/images/articles/scam/3a-casino-scam-review-cover.webp',
    'gm1688-casino-scam-review': '/static/images/articles/reviews/gm1688-casino-scam-review-cover.webp',
    'casino-investment-scam': '/static/images/casino-investment-scam-cover.png',
    'jucity-casino-review-may-2026': '/static/images/articles/reviews/jucity-casino-review-may-2026-cover.webp',
    'hg-casino-promotions-may-2026': '/static/images/articles/promo/hg-promo-may-2026-cover.webp',
    'casino-scam-alert': '/static/images/articles/scam/casino-scam-alert-cover-2026.png',
    'casino-romance-scam': '/static/images/articles/scam/casino-romance-scam-cover.webp',
    'casino-account-freeze-scam': '/static/images/articles/scam/casino-account-freeze-scam-cover.webp',
    'casino-no-withdrawal-scam': '/static/images/articles/scam/casino-no-withdrawal-scam-cover.webp',
    'fast-withdrawal': '/static/images/articles/tech/fast-withdrawal-cover.webp',
}

# Category config: (badge_text, badge_class, card_class, gradient, emoji)
categories = {
    'baccarat': ('百家樂', 'guide', '', 'linear-gradient(135deg, #0a4a3a 0%, #00a884 100%)', '🎴'),
    'slots': ('老虎機', 'hot', '', 'linear-gradient(135deg, #5a3a0a 0%, #ff6b35 100%)', '🎰'),
    'sports': ('體育投注', 'guide', '', 'linear-gradient(135deg, #0a2a5a 0%, #3498db 100%)', '⚽'),
    'worldcup': ('世界盃', 'hot', '', 'linear-gradient(135deg, #0a4a2a 0%, #28a745 100%)', '🏆'),
    'safety': ('安全防詐', 'scam', 'scam-alert', 'linear-gradient(135deg, #4a0a0a 0%, #dc3545 100%)', '🛡️'),
    'bonus': ('優惠指南', 'promo', '', 'linear-gradient(135deg, #5a4a0a 0%, #ffd700 100%)', '🎁'),
    'guide': ('新手指南', 'guide', '', 'linear-gradient(135deg, #2a0a4a 0%, #9b59b6 100%)', '📖'),
    'casino': ('娛樂城類型', 'guide', '', 'linear-gradient(135deg, #1a1a2e 0%, #6c757d 100%)', '🎮'),
    'ranking': ('排名代理', 'review', '', 'linear-gradient(135deg, #1a1a2e 0%, #495057 100%)', '🏆'),
    'reviews': ('品牌評價', 'review', 'review-card', 'linear-gradient(135deg, #1a1a2e 0%, #495057 100%)', '🔍'),
}


def get_category_for_pos(content, pos):
    """Find which category section an article at position `pos` belongs to."""
    # Look backwards for the nearest <div id="..." class="category-section"
    preceding = content[:pos]
    # Find all category section ids before this position
    matches = list(re.finditer(r'<div id="([^"]+)" class="category-section"', preceding))
    if matches:
        return matches[-1].group(1)
    return None


def slug_from_url(url):
    """Extract slug from /articles/slug or /pillars/slug"""
    parts = url.rstrip('/').split('/')
    if len(parts) >= 2:
        return parts[-1]
    return ''


# Pattern to match article cards (flexible for various HTML formatting)
article_pattern = re.compile(
    r'<article class="article-card">\s*'
    r'<h3><a href="([^"]+)">([^<]+)</a></h3>\s*'
    r'<p>([^<]+)</p>\s*'
    r'<a href="[^"]+" class="read-more">閱讀全文 →</a>\s*'
    r'</article>',
    re.DOTALL
)

count = 0
last_end = 0
new_content = ''

for match in article_pattern.finditer(content):
    url = match.group(1)
    title = match.group(2).strip()
    excerpt = match.group(3).strip()
    
    slug = slug_from_url(url)
    category_id = get_category_for_pos(content, match.start())
    
    cat_config = categories.get(category_id, ('文章', 'guide', '', 'linear-gradient(135deg, #1a1a2e 0%, #495057 100%)', '📄'))
    badge_text, badge_class, card_class, gradient, emoji = cat_config
    
    # Check if article has a cover image
    cover_path = covers.get(slug)
    
    if cover_path:
        image_html = f'<img src="{cover_path}" alt="{title}" loading="lazy">'
    else:
        image_html = f'<div style="position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 2.5rem; font-weight: 700;">{emoji}</div>'
    
    card_classes = f'article-card {card_class}'.strip()
    
    new_card = f'''                <a href="{url}" class="{card_classes}">
                    <div class="card-image" style="background: {gradient};">
                        {image_html}
                    </div>
                    <div class="card-content">
                        <div class="card-meta">
                            <span class="card-badge {badge_class}">{badge_text}</span>
                        </div>
                        <h3 class="card-title">{title}</h3>
                        <p class="card-excerpt">{excerpt}</p>
                        <span class="card-readmore">閱讀全文 →</span>
                    </div>
                </a>'''
    
    new_content += content[last_end:match.start()] + new_card
    last_end = match.end()
    count += 1

new_content += content[last_end:]

# Also update article-grid to article-grid-v2 in the category sections
new_content = new_content.replace('<div class="article-grid">', '<div class="article-grid-v2">')

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(new_content)

print(f'Replaced {count} article cards')
print(f'New file size: {len(new_content)} bytes')
