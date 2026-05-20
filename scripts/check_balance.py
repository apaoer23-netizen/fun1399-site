with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    content = f.read()

# Check tag balance
open_a = content.count('<a href=')
close_a = content.count('</a>')
open_div = content.count('<div')
close_div = content.count('</div>')

print(f'<a href=> tags: {open_a}')
print(f'</a> tags: {close_a}')
print(f'<div tags: {open_div}')
print(f'</div> tags: {close_div}')

# Check for any remaining old-style article cards
old_patterns = [
    '<article class="article-card">',
    'class="read-more"',
    "<h3><a href='",
    '</a></h3>',
]
for p in old_patterns:
    count = content.count(p)
    print(f'{count}x {p}')
