"""Manually run, offline validation. Never contacts a provider."""
from pathlib import Path
from datetime import date
import csv, json
import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
def load_records():
    return [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'catalog').glob('*/*.yml'))]

def validate():
    schema=json.loads((ROOT/'schemas/catalog.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema,format_checker=FormatChecker())
    records=load_records(); by_id={r['id']:r for r in records}
    assert len(records)==len(by_id),'Duplicate record IDs'
    for p in (ROOT/'catalog').glob('*/*.yml'):
        assert p.stem==yaml.safe_load(p.read_text(encoding='utf-8'))['id'],'Record filename must match ID'
    topics=sum([yaml.safe_load((ROOT/f'taxonomy/{f}.yml').read_text(encoding='utf-8')) for f in ['country','microdata']],[])
    assert len(topics)==14 and len({t['id'] for t in topics})==14
    topic_ids={t['id'] for t in topics}
    geography=yaml.safe_load((ROOT/'taxonomy/geography.yml').read_text(encoding='utf-8'))
    codes={c['code'] for c in geography['countries']}
    for r in records:
        errors=list(validator.iter_errors(r))
        assert not errors, f'{r["id"]}: '+ '; '.join(e.message for e in errors)
        assert set(r['topics'])<=topic_ids,r['id']+' has unknown topics'
        assert date.fromisoformat(r['verification']['checked_on'])<=date.today()
        if r['kind']=='organization': continue
        assert by_id[r['organization_id']]['kind']=='organization'
        if r['parent_id']:
            assert r['parent_id']!=r['id']
            assert by_id[r['parent_id']]['kind'] in ['program','catalog']
        for c in r['catalog_ids']: assert by_id[c]['kind']=='catalog'
        assert set(r['geography']['country_codes'])<=codes
        assert set(r['geography']['regions'])<=set(geography['regions'])
        assert r['access']['free_data_available']==(r['access']['status'] in ['OPEN','REGISTER','APPLY','REQUEST'])
        if 'microdata' in r['data_levels'] and r['kind'] in ['program','dataset']:
            assert r['survey'],r['id']+' needs survey methodology'
        visited={r['id']}; parent=r['parent_id']
        while parent:
            assert parent not in visited,'Cyclic parent relationship'
            visited.add(parent);parent=by_id[parent].get('parent_id')
    with (ROOT/'crosswalks/sdg-indicators.csv').open(encoding='utf-8',newline='') as f:
        for row in csv.DictReader(f):
            assert row['record_id'] in by_id
            assert row['topic_id'] in topic_ids
            assert 1<=int(row['goal'])<=17
            assert row['target'].startswith(row['goal']+'.')
            assert row['indicator'].startswith(row['target']+'.')
            assert row['mapping_type'] in ['official_series','related_measure','potential_input']
    assert not (ROOT/'.github/workflows').exists(),'No automated workflows are permitted in this release'
    print(f'Validated {len(records)} records, 14 topics, foreign keys, access rules and SDG references.')
    return records

if __name__=='__main__': validate()
