"""Manual local publishing helper: curated YAML -> exports and Markdown. No network or imports."""
from pathlib import Path
from html import escape
import csv,json,shutil
import yaml
from validate import validate, ROOT

records=validate(); by_id={r['id']:r for r in records}
topics=sum([yaml.safe_load((ROOT/f'taxonomy/{f}.yml').read_text(encoding='utf-8')) for f in ['country','microdata']],[])
topic_map={t['id']:t for t in topics}
geo=yaml.safe_load((ROOT/'taxonomy/geography.yml').read_text(encoding='utf-8'))
def write(path,text):
    p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
def link(id): return f'[{by_id[id]["name"]}]({id}.md)'
def table(rows):return '| Field | Value |\n| --- | --- |\n'+''.join(f'| {k} | {str(v).replace(chr(10)," ").replace("|"," / ")} |\n' for k,v in rows)
def cards(items,prefix='../records/'):
    return '\n'.join(f'- [{r["name"]}]({prefix}{r["id"]}.md) — {r["kind"].title()}; **{r.get("access",{}).get("status",r.get("un_relation",""))}**. {r["description"]}' for r in items)+'\n'

for r in records:
    out=f'# {r["name"]}\n\n{r["description"]}\n\n'
    if r['kind']=='organization':
        out+=f'**Source card · {r["un_relation"]}**\n\n{r["relation_note"]}\n\n[Official website]({r["website"]})\n\n## Catalogs, programmes and data\n\n'
        out+=cards([x for x in records if x.get('organization_id')==r['id']],prefix='')
    else:
        a=r['access'];g=r['geography'];out+=f'**{r["kind"].title()} card · {a["status"]} · {"Free data route documented" if a["free_data_available"] else "Reference only — data access not established"}**\n\n'
        out+='[Open original source]('+r['links'][0]['url']+')\n\n'
        rows=[('Stable ID',r['id']),('Organization',link(r['organization_id'])),('Original producer',r['original_producer']),('Collector',r['collector']),('Publisher',r['publisher']),('Data level',', '.join(r['data_levels'])),('Observation units',', '.join(r['observation_units'])),('Coverage',', '.join(g['regions'])),('Confirmed country examples',', '.join(g['country_codes']) or 'Not enumerated'),('Time coverage',r['time_coverage']),('Release',r['release'] or 'Select the current series or release at the source')]
        if r['parent_id']:rows.append(('Parent catalogue or programme',link(r['parent_id'])))
        if r['catalog_ids']:rows.append(('Indexed by',', '.join(link(c) for c in r['catalog_ids'])))
        out+=table(rows)+'\n'+g['notes']+'\n\n## Access and reuse\n\n'+a['notes']+'\n\n'
        out+=table([('Methods',', '.join(a['methods'])),('Formats',', '.join(a['formats']) or 'See source'),('License',a['license_name']),('Terms / access evidence',f'[Provider documentation]({a["license_url"]})')])
        out+='\n## Topics\n\n'+''.join(f'- [{t} · {topic_map[t]["name"]}](../topics/{t}.md)\n' for t in r['topics'])
        if r['survey']:
            out+='\n## Survey design and comparison\n\n'+table([(k.replace('_',' ').title(),v) for k,v in r['survey'].items()])
        out+='\n## Original links\n\n'+''.join(f'- [{x["rel"].replace("_"," ").title()}]({x["url"]})\n' for x in r['links'])
        children=[x for x in records if x.get('parent_id')==r['id']]
        if children:out+='\n## Linked records\n\n'+cards(children,prefix='')
    v=r['verification'];out+=f'\n## Verification and evidence\n\nChecked **{v["checked_on"]}**, status **{v["status"]}**, method **{v["method"]}**. {v["scope"]}\n\n'
    out+=''.join(f'- [{x["claim"]}]({x["url"]})\n' for x in v['evidence'])
    out+='\n[Return to the finder](../index.md) · [Browse by source](../sources.md) · [Browse by topic](../topics/index.md)\n'
    write(f'wiki/records/{r["id"]}.md',out)

orgs=[r for r in records if r['kind']=='organization']
write('wiki/sources.md','# Browse by organization and source\n\nFollow source → catalog → programme → dataset. These are linked entities, not four different copies of the same data.\n\n'+''.join(f'## {r["name"]}\n\n[Open source card](records/{r["id"]}.md) · {r["un_relation"]}\n\n'+cards([x for x in records if x.get('organization_id')==r['id']],prefix='records/')+'\n' for r in orgs))
write('wiki/catalogs.md','# Catalogs and meta-catalogs\n\nDiscovery portals can include restricted or unavailable studies. A METADATA_ONLY entry is never a confirmed free dataset.\n\n'+cards([r for r in records if r['kind']=='catalog'],prefix='records/'))
write('wiki/programs.md','# Survey programmes\n\nDistinguish individual respondent records from household files, diaries and published country summaries. Programme-wide descriptions do not guarantee every module in every country.\n\n'+cards([r for r in records if r['kind']=='program'],prefix='records/'))
write('wiki/datasets.md','# Datasets and statistical databases\n\nThis is a curated seed, including some broad statistical database families and selected fixed survey releases. It is not an exhaustive study or variable inventory.\n\n'+cards([r for r in records if r['kind']=='dataset'],prefix='records/'))
write('wiki/topics/index.md','# Browse by topic\n\nTopics are multi-label discovery categories. Units of observation and published data levels are separate fields. SDGs have their own [crosswalk](../sdg.md).\n\n'+''.join(('## Country and regional data\n\n' if i==0 else '## Individual and household microdata\n\n' if i==6 else '')+f'- [{t["id"]} · {t["name"]}]({t["id"]}.md) — {t["description"]}\n' for i,t in enumerate(topics)))
for t in topics:
    write(f'wiki/topics/{t["id"]}.md',f'# {t["id"]} · {t["name"]}\n\n{t["description"]}\n\nCoverage is a seed: the topic definition is broader than the sources currently listed.\n\n'+cards([r for r in records if t['id'] in r['topics']])+'\n[All topics](index.md)\n')
with (ROOT/'crosswalks/sdg-indicators.csv').open(encoding='utf-8',newline='') as f:crosswalk=list(csv.DictReader(f))
sdg='# SDG crosswalk\n\nSDGs are a policy framework, separate from the 14 discovery topics. The framework is not a mutually exclusive or exhaustive taxonomy of all UN data: goals overlap, indicators may repeat across targets, and many statistical series lie outside the framework. Do not sum unlike indicators into a single score.\n\nThe mappings below are curated examples. **Official series**, **related measure** and **potential input** mean different things. Potential inputs require a compatible population, definition, denominator and calculation. No mapping alone establishes statistical equivalence or custodianship.\n\n[Official framework](https://unstats.un.org/sdgs/indicators/indicators-list/) · [Official definitions](https://unstats.un.org/sdgs/metadata/) · [Download crosswalk CSV](downloads/sdg-indicators.csv)\n\n| Record | Topic | Indicator | Mapping | Note / evidence |\n| --- | --- | --- | --- | --- |\n'
for row in crosswalk:sdg+=f'| [{by_id[row["record_id"]]["name"]}](records/{row["record_id"]}.md) | {row["topic_id"]} | {row["indicator"]} | {row["mapping_type"]} | [{row["note"]}]({row["evidence_url"]}) |\n'
write('wiki/sdg.md',sdg)

export_dir=ROOT/'exports';export_dir.mkdir(exist_ok=True)
write('exports/catalog.jsonl',''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in records))
columns=sorted(set().union(*(r.keys() for r in records)))
with (export_dir/'catalog.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=columns);w.writeheader()
    for r in records:w.writerow({k:json.dumps(v,ensure_ascii=False,separators=(',',':')) if isinstance(v,(dict,list)) else ('null' if v is None else v) for k,v in r.items()})
for r in records:
    if r['kind']=='organization':continue
    r['organization_name']=by_id[r['organization_id']]['name']
    r['un_relation']=by_id[r['organization_id']]['un_relation']
    r['topic_labels']=[topic_map[t]['name'] for t in r['topics']]
    r['country_labels']=[next(c['name'] for c in geo['countries'] if c['code']==k) for k in r['geography']['country_codes']]
    r['card_url']=f'records/{r["id"]}/'
write('wiki/assets/catalog.json',json.dumps({'records':[r for r in records if r['kind']!='organization'],'topics':topics,'geography':geo},ensure_ascii=False,indent=2)+'\n')
for src,name in [('exports/catalog.jsonl','catalog.jsonl'),('exports/catalog.csv','catalog.csv'),('schemas/catalog.schema.json','catalog.schema.json'),('crosswalks/sdg-indicators.csv','sdg-indicators.csv')]:
    dst=ROOT/'wiki/downloads'/name;dst.parent.mkdir(exist_ok=True);shutil.copyfile(ROOT/src,dst)
write('wiki/.nojekyll','')
print('Rendered source cards, topic pages, SDG crosswalk, CSV, JSONL and the local search index.')
