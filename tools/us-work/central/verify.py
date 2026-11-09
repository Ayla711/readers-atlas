import json,re
from pathlib import Path
from collections import Counter
r=Path(__file__).resolve().parent
load=lambda p:json.loads(p.read_text())
b,p,l=[load(r/f'{x}.json') for x in ['books','places','lines']]
assert (len(b),len(p),len(l))==(10,23,20)
ids={x['id'] for x in p};books={x['id']:x for x in b}
for f in [r.parents[2]/'packs/existing-ids.json',r.parent/'shared/current-ids.json']:
 old=load(f)
 for new,used in [(b,{x['id'] for x in old['books']}),(p,{x['id'] if isinstance(x,dict) else x for x in old['places']}),(l,set(old['line_ids']))]:
  assert not ({x['id'] for x in new}&used),f'collision {f}'
for x in p:
 assert set(['id','name','name_zh','lat','lon','place_type','note','note_en','coord_checked','fact_source'])<=x.keys()
 assert 'https://' in x['coord_checked'] and 'state' not in x
 if x['place_type']=='prototype':assert x['prototype_of'] and x['prototype_of_en']
for x in l:
 assert x['status']=='draft' and x['text_zh'] and x['location_zh']
 assert set(x['place_ids'])<=ids and x['book_id'] in books
 assert all(h in x['text_en'] for h in x.get('highlight_en',[]))
 if books[x['book_id']]['public_domain']:
  raw=(r/'cache'/f"pg{x['source']['id']}.txt").read_bytes().decode('utf8')
  assert x['text_en'] in raw
 else:assert x['kind']=='scene' and x['fact_source']
 assert not re.search('[\u4e00-\u9fff]',x['text_en'])
assert all(1<=sum(x['book_id']==y['id'] for x in l)<=10 for y in b)
print('PASS: counts, references, collisions against both snapshots, bilingual fields, draft status, copyright scene split, all 10 exact raw-source quotations')
