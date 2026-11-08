"""Manually verify export integrity and all local links in the compiled site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,csv
from validate import validate,ROOT

records=validate()
expected={r['id']:r for r in records}
exported=[json.loads(line) for line in (ROOT/'exports/catalog.jsonl').read_text(encoding='utf-8').splitlines()]
assert {r['id']:r for r in exported}==expected,'JSONL differs from YAML'
with (ROOT/'exports/catalog.csv').open(encoding='utf-8',newline='') as f:
    for row in csv.DictReader(f):
        source=expected[row['id']]
        for key,value in row.items():
            if key not in source: assert value=='';continue
            original=source[key]
            parsed=json.loads(value) if isinstance(original,(dict,list)) or original is None else value
            assert parsed==original,f'CSV differs: {row["id"]}.{key}'
assert {p.stem for p in (ROOT/'wiki/records').glob('*.md')}==set(expected),'Missing or stale generated cards'
index=json.loads((ROOT/'wiki/assets/catalog.json').read_text(encoding='utf-8'))
assert {r['id'] for r in index['records']}=={r['id'] for r in records if r['kind']!='organization'}
for r in index['records']:
    for k,v in expected[r['id']].items():assert r[k]==v

class Page(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.ids=set();self.lang=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        if tag=='html':self.lang=a.get('lang')
        for key in ['href','src']:
            if key in a:self.links.append(a[key])
site=(ROOT/'docs').resolve();pages={}
for path in site.rglob('*.html'):
    parsed=Page();parsed.feed(path.read_text(encoding='utf-8'));pages[path]=parsed
assert pages,'Build the MkDocs site before checking it'
broken=[];count=0
for path,page in pages.items():
    assert page.lang=='en',f'Non-English page setting: {path}'
    for raw in page.links:
        u=urlsplit(raw)
        if u.scheme or u.netloc or raw.startswith('/') or not u.path:continue
        target=(path.parent/unquote(u.path)).resolve()
        if target.is_dir():target=target/'index.html'
        count+=1
        if not target.is_relative_to(site) or not target.exists():broken.append((str(path.relative_to(site)),raw))
assert not broken,f'Broken local links: {broken[:20]}'
assert (site/'.nojekyll').exists()
home=pages[site/'index.html']
for id in ['atlas-form','atlas-q','atlas-topic','atlas-geo','atlas-level','atlas-access','atlas-kind','atlas-free','atlas-status','atlas-results','atlas-clear']:
    assert id in home.ids,f'Missing finder control: {id}'
assert (site/'search/search_index.json').exists(),'Missing full-text search index'
assert (site/'assets/catalog.json').read_bytes()==(ROOT/'wiki/assets/catalog.json').read_bytes()
print(f'Passed export equivalence, generated-card consistency, English HTML settings, {len(pages)} HTML pages, {count} local links, finder controls and both search indexes.')
