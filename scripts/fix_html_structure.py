import re

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'r') as f:
    html = f.read()

# Fix 1: Remove stray </div> after card-image closing tag
# Pattern: </div>\s*</div>\s*<div class="card-content">
# The first </div> is the img closing, second is stray — wait no
# Actually: <div class="card-image"><img ...></div>\n\s*</div>\n\s*<div class="card-content">
# The extra </div> needs to be removed
html = re.sub(
    r'(</div>)\s*</div>\s*(<div class="card-content">)',
    r'\1\n                    \2',
    html
)

# Fix 2: Fix corrupted img src attributes
# Pattern: src="...webpGARBAGE" alt="..."
# The garbage is the text that was inside the old emoji div
html = re.sub(
    r'src="([^"]+\.webp)[^"]*"',
    r'src="\1"',
    html
)

# Count fixes
fixes = html.count('</div>\n                    </div>\n                    <div class="card-content">')
print(f'Stray </div> occurrences: {fixes}')

with open('/root/.openclaw/workspace/fun1399-clean/articles/index.html', 'w') as f:
    f.write(html)

print(f'Fixed HTML saved. Size: {len(html)} bytes')
