#!/usr/bin/env python3
"""
Batch cover image updater for fun1399.com
Usage: python3 update_cover.py <slug> <image_path>
"""
import sys, os, re, shutil

BASE = '/root/.openclaw/workspace/fun1399-clean'
IMAGES_DIR = f'{BASE}/static/images/articles'

def find_file(slug):
    """Find HTML file by slug."""
    # Try common patterns
    patterns = [
        f'{BASE}/articles/{slug}.html',
        f'{BASE}/pillars/{slug}.html',
        f'{BASE}/guides/{slug}.html',
        f'{BASE}/reviews/{slug}.html',
    ]
    for p in patterns:
        if os.path.exists(p):
            return p
    # Fallback: search
    for root, dirs, files in os.walk(BASE):
        if 'netlify' in root:
            continue
        for f in files:
            if f == f'{slug}.html':
                return os.path.join(root, f)
    return None

def get_category(file_path):
    """Extract category from path for image directory."""
    rel = os.path.relpath(file_path, BASE)
    parts = rel.split('/')
    if len(parts) >= 2:
        cat = parts[0]
        if cat in ['articles', 'pillars', 'guides', 'reviews']:
            return cat
    return 'articles'

def update_cover(slug, image_path):
    html_path = find_file(slug)
    if not html_path:
        return f"❌ 找不到文章: {slug}"
    
    # Read file
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Determine image type
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp']:
        return f"❌ 不支援的圖片格式: {ext}"
    
    # Determine target directory and filename
    cat = get_category(html_path)
    target_dir = f'{IMAGES_DIR}/{cat}'
    os.makedirs(target_dir, exist_ok=True)
    
    cover_name = f'{slug}-cover{ext}'
    target_path = f'{target_dir}/{cover_name}'
    web_path = f'/static/images/articles/{cat}/{cover_name}'
    full_web_url = f'https://fun1399.com{web_path}'
    
    # Copy image
    shutil.copy2(image_path, target_path)
    
    # Extract title from HTML
    title_match = re.search(r'<title>(.*?)</title>', html)
    title = title_match.group(1) if title_match else slug
    # Clean title suffix
    title = re.sub(r' - 娛樂城玩家俱樂部$', '', title)
    
    modified = False
    
    # 1. Update og:image (create or replace)
    if 'property="og:image"' in html:
        html = re.sub(r'<meta property="og:image" content="[^"]*">', 
                      f'<meta property="og:image" content="{full_web_url}">', html)
    else:
        # Insert after description or keywords
        html = re.sub(r'(<meta name="description"[^>]*>)',
                      f'\\1\n    <meta property="og:image" content="{full_web_url}">', html, count=1)
    modified = True
    
    # 2. Update twitter:image
    if 'name="twitter:image"' in html:
        html = re.sub(r'<meta name="twitter:image" content="[^"]*">',
                      f'<meta name="twitter:image" content="{full_web_url}">', html)
    else:
        # Insert after og:image
        html = re.sub(r'(<meta property="og:image"[^>]*>)',
                      f'\\1\n    <meta name="twitter:image" content="{full_web_url}">', html, count=1)
    
    # 3. Ensure twitter:card exists
    if 'name="twitter:card"' not in html:
        html = re.sub(r'(<meta name="twitter:image"[^>]*>)',
                      f'\\1\n    <meta name="twitter:card" content="summary_large_image">', html, count=1)
    
    # 4. Update Schema image
    if '"image"' in html and '"@type": "Article"' in html:
        # Replace existing image in schema
        html = re.sub(r'"image":\s*"[^"]*"', f'"image": "{full_web_url}"', html)
    elif '"@type": "Article"' in html:
        # Add image field before closing brace
        html = re.sub(r'("dateModified":\s*"[^"]*")', f'\\1,\n      "image": "{full_web_url}"', html)
    elif '"@type": "FAQPage"' in html:
        if '"image"' in html:
            html = re.sub(r'"image":\s*"[^"]*"', f'"image": "{full_web_url}"', html)
        else:
            html = re.sub(r'("description":\s*"[^"]*")', f'\\1,\n      "image": "{full_web_url}"', html, count=1)
    
    # 5. Update or create article-hero-image
    if 'class="article-hero-image"' in html:
        # Replace existing hero image
        html = re.sub(
            r'<div class="article-hero-image">.*?</div>',
            f'<div class="article-hero-image">\n                <img src="{web_path}"\n                     alt="{title}"\n                     loading="lazy" width="1200" height="630">\n                <p class="image-caption">{title}</p>\n            </div>',
            html, flags=re.DOTALL, count=1)
    else:
        # Insert after h1
        h1_match = re.search(r'(<h1[^>]*>.*?</h1>)', html, re.DOTALL)
        if h1_match:
            h1 = h1_match.group(1)
            hero = f'{h1}\n            <div class="article-hero-image">\n                <img src="{web_path}"\n                     alt="{title}"\n                     loading="lazy" width="1200" height="630">\n                <p class="image-caption">{title}</p>\n            </div>'
            html = html.replace(h1, hero, 1)
        else:
            # Insert after breadcrumb or intro
            html = re.sub(
                r'(<nav class="breadcrumb">.*?</nav>)',
                f'\\1\n            <h1>{title}</h1>\n            <div class="article-hero-image">\n                <img src="{web_path}" alt="{title}" loading="lazy" width="1200" height="630">\n                <p class="image-caption">{title}</p>\n            </div>',
                html, flags=re.DOTALL, count=1)
    
    # Write back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return f"✅ {slug} → {web_path}"

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 update_cover.py <slug> <image_path>")
        sys.exit(1)
    
    slug = sys.argv[1]
    image_path = sys.argv[2]
    result = update_cover(slug, image_path)
    print(result)
