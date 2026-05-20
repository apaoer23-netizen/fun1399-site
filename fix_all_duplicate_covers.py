import os, re, glob

print('='*80)
print('修復同時有 article-cover 和 article-hero-image 的重複封面')
print('='*80)

# Find all articles with both article-cover and article-hero-image
for html in glob.glob('articles/*.html'):
    with open(html, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_cover = 'class="article-cover"' in content
    has_hero = 'class="article-hero-image"' in content
    
    if has_cover and has_hero:
        # Remove article-cover div, keep article-hero-image
        # Pattern: optional whitespace + <div class="article-cover" ...>...</div> + optional whitespace
        pattern = r'\s*<div class="article-cover"[^>]*>.*?</div>\s*'
        content = re.sub(pattern, '', content, flags=re.DOTALL, count=1)
        
        with open(html, 'w', encoding='utf-8') as f:
            f.write(content)
        
        slug = os.path.basename(html).replace('.html', '')
        print(f'  ✅ {slug}: removed article-cover, kept article-hero-image')

print('Done!')
