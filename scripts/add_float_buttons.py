#!/usr/bin/env python3
"""
Add floating buttons to all HTML pages that don't have them
"""
import glob

FLOAT_BUTTONS = '''    <div class="float-btn-container">
        <a href="https://fun1399.ofa177.net/" class="float-play" target="_blank" rel="noopener">🎮 立即遊玩</a>
        <a href="https://lin.ee/Mc1pb7z" class="float-service" target="_blank">💬 專人服務</a>
    </div>
'''

files = glob.glob('/root/.openclaw/workspace/fun1399-clean/**/*.html', recursive=True)
added = 0

for filepath in files:
    # Skip netlify files
    if 'netlify' in filepath:
        continue
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Skip if already has float buttons
    if 'float-play' in content or 'float-btn-container' in content:
        continue
    
    # Add before </body>
    if '</body>' in content:
        content = content.replace('</body>', FLOAT_BUTTONS + '</body>')
        with open(filepath, 'w') as f:
            f.write(content)
        added += 1

print(f'Added floating buttons to {added} files')
