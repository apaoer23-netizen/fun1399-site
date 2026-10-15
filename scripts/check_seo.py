#!/usr/bin/env python3
"""Dependency-free release checks. Local output verification, not Google indexing."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,urljoin,unquote
from collections import Counter
import json,re,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://fun1399.com'
class Page(HTMLParser):
    def __init__(self,source):
        super().__init__();self.tags=[];self.feed(source)
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
def target(path):
    path=unquote(path)
    if path=='/':return ROOT/'index.html'
    exact=ROOT/path.lstrip('/')
    if exact.is_file():return exact
    if (exact/'index.html').is_file():return exact/'index.html'
    return ROOT/(path.lstrip('/').rstrip('/')+'.html')
def commercial(host):return bool(host and (host.startswith('fun1399.') and host!='fun1399.com' or host in ['u.town','www.leyo.tw']))
def main():
    errors=[];warnings=[];stats=Counter();pages={}
    for p in sorted(ROOT.rglob('*.html')):
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith(('kaobei-casino/','downloads/')) or p.name.startswith('google'):continue
        source=p.read_text();tags=Page(source).tags;meta={a.get('name','').lower():a.get('content','') for t,a in tags if t=='meta'}
        canonical=[a.get('href','') for t,a in tags if t=='link' and a.get('rel')=='canonical']
        pages[p]=(source,meta,canonical);stats['pages']+=1
        if 'noindex' in meta.get('robots','').lower() and rel!='404.html':errors.append(f'{rel}: unexpected noindex')
        if len(canonical)!=1:errors.append(f'{rel}: expected one canonical')
        if not meta.get('description'):errors.append(f'{rel}: missing description')
        if sum(t=='h1' for t,a in tags)!=1:errors.append(f'{rel}: expected one H1')
        for raw in re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',source,re.S|re.I):
            try:json.loads(raw);stats['jsonld']+=1
            except ValueError:errors.append(f'{rel}: invalid JSON-LD')
        for tag,a in tags:
            href=a.get('href','')
            if tag=='a' and href:
                dest=urlsplit(urljoin(canonical[0] if canonical else DOMAIN+'/'+rel,href));host=dest.hostname or ''
                if dest.scheme in ['http','https'] and host=='fun1399.com':
                    f=target(dest.path)
                    if not f.exists():errors.append(f'{rel}: missing internal link {href}')
                    elif dest.fragment and f.suffix=='.html':
                        ids={a.get('id') for _,a in Page(f.read_text()).tags}
                        if unquote(dest.fragment) not in ids:warnings.append(f'{rel}: missing fragment {href}')
                if commercial(host):
                    stats['commercial_links']+=1
                    if 'sponsored' not in a.get('rel','').split() and 'nofollow' not in a.get('rel','').split():errors.append(f'{rel}: unqualified commercial link {href}')
            src=a.get('src') if tag in ['img','script'] else a.get('href') if tag=='link' and a.get('rel') in ['stylesheet','icon','apple-touch-icon','manifest'] else None
            if src and src.startswith('/') and not (ROOT/urlsplit(src).path.lstrip('/')).is_file():errors.append(f'{rel}: missing asset {src}')
    ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'};urls=[]
    for item in ET.parse(ROOT/'sitemap.xml').getroot():
        loc=item.find('s:loc',ns).text;urls.append(loc);f=target(urlsplit(loc).path)
        if not f.exists():errors.append(f'sitemap: missing {loc}')
        elif 'noindex' in dict((a.get('name',''),a.get('content','')) for t,a in Page(f.read_text()).tags if t=='meta').get('robots','').lower():errors.append(f'sitemap: noindex {loc}')
    if len(urls)!=len(set(urls)):errors.append('sitemap: duplicate URLs')
    stats['sitemap_urls']=len(urls)
    test=(ROOT/'downloads/test_preview.html').read_text()
    if not any(t=='meta' and a.get('name')=='robots' and 'noindex' in a.get('content','') for t,a in Page(test).tags):errors.append('test_preview: must stay noindex')
    for special in ['index.html','recommend/2026.html']:
        text=(ROOT/special).read_text()
        for claim in ['12,458','台灣最大','業界最快','出金保證']:
            if claim in text:errors.append(f'{special}: unsupported claim {claim}')
        if 'href="/disclosure"' not in text or 'href="/review-methodology"' not in text:errors.append(f'{special}: policy navigation missing')
    about=(ROOT/'about.html').read_text()
    for claim in ['10K+','24小時內回覆','24 小時內完成修正','所有評測都經過實際測試','台灣最專業']:
        if claim in about:errors.append(f'about.html: unsupported site-wide claim {claim}')
    directory=(ROOT/'reviews/index.html').read_text()
    if re.search(r'class="(?:overall-rating|review-scores|rank-badge)"',directory):errors.append('reviews/index.html: unsupported ranking UI returned')
    for raw in re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',directory,re.S|re.I):
        data=json.loads(raw)
        for node in data.get('@graph',[]):
            if node.get('@type')=='CollectionPage':
                listing=node.get('mainEntity',{});items=listing.get('itemListElement',[])
                if listing.get('numberOfItems')!=len(items) or len(items)!=6:errors.append('reviews/index.html: collection count mismatch')
                for item in items:
                    if f'href="{urlsplit(item.get("url", "")).path}"' not in directory:errors.append('reviews/index.html: schema entry not linked in visible page')
    result={'checks':dict(stats),'errors':errors,'warnings':list(dict.fromkeys(warnings))}
    print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if errors else 0
if __name__=='__main__':raise SystemExit(main())
