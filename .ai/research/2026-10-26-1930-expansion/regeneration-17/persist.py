import hashlib,json,shutil
from pathlib import Path
from datetime import datetime,timezone
r=Path('/Users/zenkim_office/Project/wavvy')
o=r/'.ai/research/2026-10-26-1930-expansion/regeneration-17'
s=Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_2u1vlhJp4vPzHQil/artifacts/1930-regeneration-17')
raw=o/'raw';raw.mkdir(exist_ok=True)
for p in s.iterdir():
 if p.is_file():shutil.copy2(p,raw/p.name)
j=json.loads((raw/'journal.json').read_text());b=json.loads((o/'baseline.json').read_text())
assert hashlib.sha256((r/'SERIES/19-30/production/suno-expansion-20261026.json').read_bytes()).hexdigest()==b['original_expansion_manifest_sha256']
assert hashlib.sha256((r/'SERIES/19-30/input/tracks/17_small-satellites.txt').read_bytes()).hexdigest()==b['source_sha256']
p=r/'SERIES/19-30/input/suno-candidates.json';d=json.loads(p.read_text())
other=[t for t in d['tracks'] if t['order']!=17]
assert hashlib.sha256(json.dumps(other,sort_keys=True,ensure_ascii=False).encode()).hexdigest()==b['other13_entries_sha256']
t=next(t for t in d['tracks'] if t['order']==17)
old={c['id']:c for c in t['candidates']}
for c in b['entry17_before']['candidates']:assert old[c['id']]==c
rel='production/suno-small-satellites-regeneration-20261026.json'
j['updated_at_utc']=datetime.now(timezone.utc).isoformat();j['rawref']='.ai/research/2026-10-26-1930-expansion/regeneration-17/raw/'
(r/'SERIES/19-30'/rel).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
for c in j['candidates']:
 row=dict(c);row['regeneration_attempt_id']=j['attempt_id'];old[row['id']]=row
# The original two remain first; the two regeneration candidates accumulate afterward.
t['candidates']=list(old.values())
a={'attempt_id':j['attempt_id'],'production_json':rel,'source_sha256':j['source_sha256'],'status':j['status'],'create_clicks':j['create_clicks'],'submitted_at_utc':j.get('submitted_at_utc'),'credits_before':j['credits_before'],'credits_after':j['credits_after'],'actualsettings':j['actualsettings'],'new_candidate_ids':[c['id'] for c in j['candidates']],'prior_candidate_ids':[c['id'] for c in b['entry17_before']['candidates']]}
attempts={x['attempt_id']:x for x in t.get('regeneration_attempts',[])};attempts[a['attempt_id']]=a;t['regeneration_attempts']=list(attempts.values())
d['candidate_history_note']='Cumulative candidate history: original candidates are preserved; authorized regeneration candidates are appended to their track. No final candidate has been chosen.'
if 'final_ui_verification' in j:d['latest_regeneration_ui_verification']=j['final_ui_verification']
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':j['status'],'create_clicks':j['create_clicks'],'new_candidates':len(j['candidates']),'credits_after':j['credits_after']}))
