import re

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    html = f.read()

# Fix: Remove the extra </div> between card-image closing and card-content opening
# Pattern: </div>
#                    </div>
#                    <div class="card-content">
# The first </div> is from <img...></div>, the second </div> is stray

html = re.sub(
    r'(</div>)\s*</div>\s*<div class="card-content">',
    r'\1\n                    <div class="card-content">',
    html
)

# Also fix any remaining cases where the indentation might differ
html = re.sub(
    r'(</div>)\s*\n\s*</div>\s*\n\s*<div class="card-content">',
    r'\1\n                    <div class="card-content">',
    html
)

# Fix corrupted img src
# baccarat-strategy-cover.webpÐ26百家樂策略進階攻略
html = re.sub(
    r'src="([^"]+\.webp)[^"]*"',
    r'src="\1"',
    html
)

# Verify by checking div balance in a sample card
sample = re.search(r'<a href="/articles/baccarat-guide".*?</a>', html, re.DOTALL)
if sample:
    card = sample.group(0)
    open_div = card.count('<div')
    close_div = card.count('</div>')
    print(f'Sample card div balance: open={open_div}, close={close_div}')

# Count all cards
cards = re.findall(r'<a href="/articles/[^"]+" class="article-card[^"]*".*?</a>', html, re.DOTALL)
broken = 0
for card in cards:
    open_div = card.count('<div')
    close_div = card.count('</div>')
    if open_div != close_div:
        broken += 1
        # Find the slug
        slug = re.search(r'href="/articles/([^"]+)"', card)
        if slug:
            print(f'BROKEN: {slug.group(1)} - open={open_div}, close={close_div}')

print(f'Total cards: {len(cards)}, Broken: {broken}')

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(html)

print(f'Saved. Size: {len(html)} bytes')
