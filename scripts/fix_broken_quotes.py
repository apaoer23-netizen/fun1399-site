#!/usr/bin/env python3
import glob

files = glob.glob('/root/.openclaw/workspace/fun1399-clean/**/*.html', recursive=True)
fixed = 0

for f in files:
    if 'netlify' in f:
        continue
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    # Fix broken quotes from sed
    content = content.replace(
        "<script src=\"/static/js/floating-cta.js'></script>\n    <script src=\"/static/js/mobile-menu.js\"\"\u003e\u003c/script\u003e",
        "<script src=\"/static/js/floating-cta.js\"\u003e\u003c/script\u003e\n    <script src=\"/static/js/mobile-menu.js\"\u003e\u003c/script\u003e"
    )
    
    # Also fix if the quotes are slightly different
    content = content.replace(
        "floating-cta.js'></script>",
        "floating-cta.js\"\u003e\u003c/script\u003e"
    )
    content = content.replace(
        'mobile-menu.js"\u003e\u003c/script\u003e',
        'mobile-menu.js\"\u003e\u003c/script\u003e'
    )
    content = content.replace(
        'mobile-menu.js""\u003e\u003c/script\u003e',
        'mobile-menu.js\"\u003e\u003c/script\u003e'
    )
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        fixed += 1

print(f'Fixed {fixed} files')
