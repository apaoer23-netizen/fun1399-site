#!/usr/bin/env python3
"""Align existing sitemap entries with declared content dates; --write applies changes.

No historic date is independently certified by this script. It preserves published
date declarations and never substitutes filesystem mtime or today's date.
"""
import argparse
from datetime import datetime
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
NS='http://www.sitemaps.org/schemas/sitemap/0.9'
ET.register_namespace('',NS)
class Meta(HTMLParser):
    def __init__(self,source):
        super().__init__();self.meta={};self.canonical='';self.feed(source)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='meta':self.meta[a.get('name','').lower()]=a.get('content','')
        if tag=='link' and a.get('rel')=='canonical':self.canonical=a.get('href','')
def content_date(source):
    import re
    dates=[]
    def walk(x):
        if isinstance(x,dict):
            if isinstance(x.get('dateModified'),str):dates.append(x['dateModified'])
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    for raw in re.findall(r'<script\b[^>]*type=[\"\']application/ld\+json[\"\'][^>]*>(.*?)</script>',source,re.S|re.I):walk(json.loads(raw))
    if not dates:
        value=Meta(source).meta.get('update')
        if value:dates.append(value)
    for value in dates:datetime.fromisoformat(value.replace('Z','+00:00'))
    return max(dates,key=lambda d:d[:10]) if dates else None
def resolve(url):
    p=urlsplit(url).path
    if p=='/':return ROOT/'index.html'
    if p.endswith('/'):return ROOT/p.lstrip('/')/'index.html'
    f=ROOT/(p.lstrip('/')+'.html')
    return f if f.exists() else ROOT/p.lstrip('/')/'index.html'
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
    tree=ET.parse(ROOT/'sitemap.xml');root=tree.getroot();changes=[];seen=set()
    for item in list(root):
        loc=item.find(f'{{{NS}}}loc').text
        if loc in seen:root.remove(item);changes.append(f'Remove duplicate {loc}');continue
        seen.add(loc);p=resolve(loc)
        if not p.exists():raise ValueError(f'Missing sitemap file: {loc}')
        source=p.read_text();meta=Meta(source)
        if 'noindex' in meta.meta.get('robots','').lower():root.remove(item);changes.append(f'Remove noindex {loc}');continue
        date=content_date(source);last=item.find(f'{{{NS}}}lastmod')
        if date and (last is None or last.text!=date):
            if last is None:last=ET.SubElement(item,f'{{{NS}}}lastmod')
            last.text=date;changes.append(f'Date {loc}: {date}')
    urls={e.find(f'{{{NS}}}loc').text for e in root}
    # Only explicitly selected navigational and policy pages are added.
    for path in ['articles/index.html','reviews/index.html','responsible-gaming.html','disclosure.html','review-methodology.html']:
        p=ROOT/path;source=p.read_text();meta=Meta(source);loc=meta.canonical
        if not loc or 'noindex' in meta.meta.get('robots','').lower():raise ValueError(f'Ineligible page: {path}')
        if loc not in urls:
            item=ET.SubElement(root,f'{{{NS}}}url');ET.SubElement(item,f'{{{NS}}}loc').text=loc
            date=content_date(source)
            if date:ET.SubElement(item,f'{{{NS}}}lastmod').text=date
            urls.add(loc);changes.append(f'Add {loc}')
    print(f'{len(changes)} sitemap changes; {len(root)} URLs')
    for change in changes:print(change)
    if args.write:
        ET.indent(tree,space='  ');tree.write(ROOT/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    return 1 if changes and not args.write else 0
if __name__=='__main__':raise SystemExit(main())
