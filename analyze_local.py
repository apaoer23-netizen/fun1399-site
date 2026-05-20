#!/usr/bin/env python3
import os, re, glob
from collections import defaultdict

BASE_DIR = "/root/.openclaw/workspace/fun1399-clean"

# Get all HTML files
html_files = glob.glob(f"{BASE_DIR}/**/*.html", recursive=True)

results = {}
for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    rel_path = filepath.replace(BASE_DIR, "").lstrip("/")
    
    # Title
    title_match = re.search(r'<title>(.*?)</title>', content, re.I|re.S)
    title = title_match.group(1).strip() if title_match else "NO TITLE"
    
    # Meta description
    desc_match = re.search(r'<meta[^\u003e]*name=["\']description["\'][^\u003e]*content=["\']([^"\']+)', content, re.I|re.S)
    if not desc_match:
        desc_match = re.search(r'<meta[^\u003e]*content=["\']([^"\']+)["\'][^\u003e]*name=["\']description["\']', content, re.I|re.S)
    description = desc_match.group(1) if desc_match else "NO META DESCRIPTION"
    
    # Canonical
    canon_match = re.search(r'<link[^\u003e]*rel=["\']canonical["\'][^\u003e]*href=["\']([^"\']+)', content, re.I|re.S)
    canonical = canon_match.group(1) if canon_match else "NONE"
    
    # Check robots noindex
    robots_match = re.search(r'<meta[^\u003e]*name=["\']robots["\'][^\u003e]*content=["\']([^"\']+)', content, re.I|re.S)
    robots = robots_match.group(1) if robots_match else "NONE"
    
    # OG title
    og_title_match = re.search(r'<meta[^\u003e]*property=["\']og:title["\'][^\u003e]*content=["\']([^"\']+)', content, re.I|re.S)
    og_title = og_title_match.group(1) if og_title_match else "NO OG:TITLE"
    
    # OG image
    og_img_match = re.search(r'<meta[^\u003e]*property=["\']og:image["\'][^\u003e]*content=["\']([^"\']+)', content, re.I|re.S)
    og_image = og_img_match.group(1) if og_img_match else "NO OG:IMAGE"
    
    # Schema.org
    has_schema = 'application/ld+json' in content or 'schema.org' in content
    
    # Internal links count (href="/...")
    links = re.findall(r'href=["\'](/[^"\']+)["\']', content)
    unique_links = len(set(links))
    
    # Word count (strip HTML)
    text = re.sub(r'<[^\u003e]+>', ' ', content)
    text = re.sub(r'\s+', ' ', text).strip()
    word_count = len(text.split())
    
    # H1 count
    h1_count = len(re.findall(r'<h1[>\s]', content, re.I))
    
    # H2 count
    h2_count = len(re.findall(r'<h2[>\s]', content, re.I))
    
    results[rel_path] = {
        'title': title,
        'description': description[:120],
        'canonical': canonical,
        'robots': robots,
        'og_title': og_title,
        'og_image': og_image,
        'has_schema': has_schema,
        'internal_links': unique_links,
        'word_count': word_count,
        'h1_count': h1_count,
        'h2_count': h2_count
    }

# Print report
print("=" * 90)
print("FUN1399 LOCAL HTML AUDIT")
print("=" * 90)
print(f"\nTotal HTML files: {len(results)}\n")

# Articles directory only
articles = {k:v for k,v in results.items() if k.startswith('articles/') and k != 'articles/index.html'}
print(f"Article pages: {len(articles)}\n")

# Issues analysis
print("=" * 90)
print("ISSUES BY PAGE")
print("=" * 90)

for path, data in sorted(articles.items()):
    issues = []
    if data['title'] == "NO TITLE":
        issues.append("NO TITLE")
    if data['description'] == "NO META DESCRIPTION":
        issues.append("NO META DESC")
    if 'noindex' in data['robots'].lower():
        issues.append("NOINDEX")
    if data['canonical'] == "NONE":
        issues.append("NO CANONICAL")
    if data['og_title'] == "NO OG:TITLE":
        issues.append("NO OG:TITLE")
    if data['og_image'] == "NO OG:IMAGE":
        issues.append("NO OG:IMAGE")
    if not data['has_schema']:
        issues.append("NO SCHEMA")
    if data['word_count'] < 800:
        issues.append(f"LOW CONTENT ({data['word_count']} words)")
    if data['h1_count'] == 0:
        issues.append("NO H1")
    if data['h1_count'] > 1:
        issues.append(f"MULTIPLE H1 ({data['h1_count']})")
    if data['h2_count'] < 3:
        issues.append(f"FEW H2 ({data['h2_count']})")
    if data['internal_links'] < 3:
        issues.append(f"LOW INTERNAL LINKS ({data['internal_links']})")
    
    if issues:
        print(f"\n{path}")
        for i in issues:
            print(f"  ⚠️ {i}")

# Content quality summary
print("\n" + "=" * 90)
print("CONTENT QUALITY SUMMARY")
print("=" * 90)

low_content = [(p, d['word_count']) for p, d in articles.items() if d['word_count'] < 1000]
print(f"\nArticles with < 1000 words: {len(low_content)}")
for p, w in sorted(low_content, key=lambda x: x[1])[:10]:
    print(f"  {w:5d} words: {p}")

no_schema = [p for p, d in articles.items() if not d['has_schema']]
print(f"\nArticles without Schema.org: {len(no_schema)}")

no_og = [p for p, d in articles.items() if d['og_image'] == "NO OG:IMAGE"]
print(f"Articles without OG image: {len(no_og)}")

low_links = [(p, d['internal_links']) for p, d in articles.items() if d['internal_links'] < 5]
print(f"\nArticles with < 5 internal links: {len(low_links)}")
for p, l in sorted(low_links, key=lambda x: x[1])[:10]:
    print(f"  {l:3d} links: {p}")

# Check for duplicate titles
titles = defaultdict(list)
for path, data in articles.items():
    titles[data['title']].append(path)
dupes = {t: u for t, u in titles.items() if len(u) > 1}
if dupes:
    print("\n" + "=" * 90)
    print("DUPLICATE TITLES")
    print("=" * 90)
    for t, paths in dupes.items():
        print(f"\n'{t}'")
        for p in paths:
            print(f"  - {p}")

print("\n" + "=" * 90)
print("AUDIT COMPLETE")
print("=" * 90)
