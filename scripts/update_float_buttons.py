#!/usr/bin/env python3
"""
Update floating buttons across all HTML pages
"""
import os
import glob

OLD_SINGLE = '''    <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">立即遊玩</a>
    <a href="https://lin.ee/Mc1pb7z" class="float-line" target="_blank">LINE@</a>'''

OLD_CONTAINER = '''    <div class="float-btn-container">
        <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">🎮 立即遊玩</a>
        <a href="https://lin.ee/Mc1pb7z" class="float-service" target="_blank">💬 專人服務</a>
    </div>'''

NEW = '''    <div class="float-btn-container">
        <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">🎮 立即遊玩</a>
        <a href="https://lin.ee/Mc1pb7z" class="float-service" target="_blank">💬 專人服務</a>
    </div>'''

OLD_PATTERNS = [
    '    <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">立即遊玩</a>\n    <a href="https://lin.ee/Mc1pb7z" class="float-line" target="_blank">LINE@</a>',
    '    <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">立即遊玩</a>\n    <a href="https://lin.ee/Mc1pb7z" class="float-line" target="_blank">LINE@</a>',
    '<a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">立即遊玩</a>\n    <a href="https://lin.ee/Mc1pb7z" class="float-line" target="_blank">LINE@</a>',
]

files = glob.glob('/root/.openclaw/workspace/fun1399-clean/**/*.html', recursive=True)
updated = 0

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Replace old patterns
    for pattern in OLD_PATTERNS:
        content = content.replace(pattern, NEW)
    
    # Also replace if already in container format but wrong class
    content = content.replace('class="float-line"', 'class="float-service"')
    content = content.replace('>LINE@<', '>💬 專人服務<')
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        updated += 1
        print(f'Updated: {filepath}')

print(f'\nTotal files updated: {updated}')
