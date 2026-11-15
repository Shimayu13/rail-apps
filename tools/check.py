#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify deployment paths, page metadata, anchor targets and publication scope."""
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'dist'
config=json.loads((ROOT/'content/site.json').read_text())
base=config['base_path'].rstrip('/')
class Document(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.refs=[];self.h1=0;self.title=False;self.lang=False;self.description=False;self.scripts=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('href','src'):
            if key in attrs:self.refs.append(attrs[key])
        self.h1+=tag=='h1';self.title|=tag=='title';self.scripts+=tag=='script'
        self.lang|=tag=='html' and attrs.get('lang')=='ja'
        self.description|=tag=='meta' and attrs.get('name')=='description' and bool(attrs.get('content'))

docs={p:Document(p.read_text()) for p in OUT.rglob('*.html')}
assert len(docs)==10, f'Expected 10 pages, found {len(docs)}'
count=0
for path,doc in docs.items():
    assert doc.h1==1 and doc.title and doc.lang and doc.description, f'Incomplete metadata: {path}'
    assert doc.scripts==0, 'This site must work without scripts or trackers'
    for ref in doc.refs:
        parsed=urlsplit(ref)
        assert ref and ref!='#',f'Empty link in {path}'
        if parsed.scheme in ('https','mailto'):continue
        assert not parsed.scheme and not parsed.netloc, f'Unexpected remote asset: {ref}'
        if parsed.path:
            assert parsed.path.startswith(base+'/'),f'Incorrect Pages base path: {ref}'
            target=OUT/unquote(parsed.path[len(base)+1:])
            if target.is_dir():target=target/'index.html'
        else:target=path
        assert target.is_file(),f'Broken link: {path} → {ref}'
        if parsed.fragment:
            assert target in docs and unquote(parsed.fragment) in docs[target].ids,f'Broken anchor: {ref}'
        count+=1
assert (OUT/'.nojekyll').exists()
ET.parse(OUT/'sitemap.xml')
registry=json.loads((OUT/'app-store-urls.json').read_text())
for app in ('jre','yokohama'):
    assert len(registry[app])==3
    for target in registry[app].values():assert target.startswith(config['origin']+base+'/')
for path in OUT.rglob('*'):
    assert path.suffix not in ('.swift','.toml','.pem','.key'),f'Unexpected app/secret file: {path}'
    if path.is_file():
        text=path.read_text()
        assert not re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|-----BEGIN .*PRIVATE KEY|acl:consumerKey=|X-RapidAPI-Key)',text),f'Credential marker: {path}'
print(f'PASS: {len(docs)} pages, {count} local links/assets/anchors, App Store URL registry, sitemap and publication scope.')
