import re

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    content = f.read()

markers = [
    'article-grid-v2',
    'article-card scam-alert',
    'card-image',
    'card-badge',
    'card-title',
    'card-excerpt',
    'card-readmore',
    'casino-scam-complete-guide-cover-2026.png',
]
for m in markers:
    count = content.count(m)
    print(f'{count}x {m}')

# Check for broken tags
open_a = content.count('<a href=')
close_a = content.count('</a>')
open_div = content.count('<div')
close_div = content.count('</div>')
print(f'\na tags: open={open_a}, close={close_a}')
print(f'div tags: open={open_div}, close={close_div}')

first_cards = re.findall(r'class="(article-card[^"]*)"', content)[:10]
print(f'\nFirst 10 card classes: {first_cards}')
