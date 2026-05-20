#!/usr/bin/env python3
"""
Remove hardcoded floating CTA buttons from ALL HTML pages,
then add global floating-cta.js reference.
"""
import glob, re

files = glob.glob('/root/.openclaw/workspace/fun1399-clean/**/*.html', recursive=True)
removed_total = 0
added_total = 0

for filepath in files:
    if 'netlify' in filepath:
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # ---- Remove various hardcoded floating button patterns ----
    
    # Pattern A: full container div
    content = re.sub(
        r'\s*<div class="float-btn-container">\s*'
        r'<a href="https://fun1399\.ofa177\.net/"[^>]*class="float-play"[^>]*>.*?</a>\s*'
        r'<a href="https://lin\.ee/Mc1pb7z"[^>]*class="float-(?:service|line)"[^>]*>.*?</a>\s*'
        r'</div>',
        '', content, flags=re.DOTALL
    )
    
    # Pattern B: comment + single anchors (homepage style)
    content = re.sub(
        r'\s*<!--\s*Floating\s+(?:Play\s+)?Button\s*-->\s*'
        r'<a href="https://fun1399\.ofa177\.net/"[^>]*class="float-play"[^>]*>.*?</a>',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'\s*<!--\s*Floating\s+(?:Line\s+)?Button\s*-->\s*'
        r'<a href="https://lin\.ee/Mc1pb7z"[^>]*class="float-(?:service|line)"[^>]*>.*?</a>',
        '', content, flags=re.DOTALL
    )
    
    # Pattern C: loose single anchors
    content = re.sub(
        r'\s*<a href="https://fun1399\.ofa177\.net/"[^>]*class="float-play"[^>]*>.*?</a>',
        '', content, flags=re.DOTALL
    )
    content = re.sub(
        r'\s*<a href="https://lin\.ee/Mc1pb7z"[^>]*class="float-(?:service|line)"[^>]*>.*?</a>',
        '', content, flags=re.DOTALL
    )
    
    # Pattern D: trailing whitespace cleanup
    content = re.sub(r'(\s*)\n\s*\n\s*\n', r'\1\n\n', content)
    
    changed = content != original
    
    # ---- Add floating-cta.js if not present ----
    if 'floating-cta.js' not in content:
        # Insert before closing body tag
        content = content.replace(
            '</body>',
            '    <script src="/static/js/floating-cta.js"></script>\n</body>'
        )
        added_total += 1
    
    if changed or 'floating-cta.js' not in original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        if changed:
            removed_total += 1
            print(f'Removed hardcoded: {filepath}')
        elif 'floating-cta.js' not in original:
            print(f'Added script: {filepath}')

print(f'\nRemoved hardcoded buttons from: {removed_total} files')
print(f'Added floating-cta.js to: {added_total} files')
