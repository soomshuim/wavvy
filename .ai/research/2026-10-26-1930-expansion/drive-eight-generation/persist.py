import json,hashlib,shutil
from pathlib import Path
R=Path('/Users/zenkim_office/Project/wavvy');D=R/'.ai/research/2026-10-26-1930-expansion/drive-eight-generation';S=Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_2u1vlhJp4vPzHQil/artifacts/1930-drive-eight-generation');raw=D/'raw';raw.mkdir(exist_ok=True)
for p in S.glob('*'):
 if p.is_file():shutil.copy2(p,raw/p.name)
j=json.loads((raw/'journal.json').read_text());base=json.loads((D/'baseline.json').read_text());sources=json.loads((D/'source-fields.json').read_text())
for p,h in base['immutable_sha256'].items():assert hashlib.sha256((R/p).read_bytes()).hexdigest()==h,p
for s in sources:assert hashlib.sha256((R/s['source_txt']).read_bytes()).hexdigest()==s['source_sha256']
P=R/'SERIES/19-30/input/suno-candidates.json';ledger=json.loads(P.read_text());orders={s['number'] for s in sources}
for old in base['ledger']['tracks']:
 t=next(t for t in ledger['tracks'] if t['order']==old['order'])
 if old['order'] not in orders:assert t==old,old['order']
 for c in old['candidates']:assert next(x for x in t['candidates'] if x['id']==c['id'])==c,c['id']
 assert t['source_sha256']==old['source_sha256'] and t['source_txt']==old['source_txt']
for a in j['attempts']:
 t=next(t for t in ledger['tracks'] if t['order']==a['order']); attempts=t.setdefault('regeneration_attempts',[]); ids={c['id'] for c in a.get('candidates',[])}
 record=dict(a,production_json='production/suno-drive-eight-20261026.json',source_txt=a['source_txt'].removeprefix('SERIES/19-30/'))
 attempts[:]=[x for x in attempts if x.get('attempt_id')!=a['attempt_id']];attempts.append(record)
 for c in a.get('candidates',[]):
  obj=dict(c,regeneration_attempt_id=a['attempt_id'],source_sha256=a['source_sha256'],source_txt=a['source_txt'].removeprefix('SERIES/19-30/'))
  existing=next((x for x in t['candidates'] if x['id']==c['id']),None)
  if existing:existing.update(obj)
  else:t['candidates'].append(obj)
 assert t['decision']['chosen_candidate_id'] is None
if j.get('final_ui_verification'):ledger['latest_drive_ui_verification']=j['final_ui_verification']
ledger['candidate_history_note']='Cumulative candidate history: original and earlier regeneration candidates are preserved. Each Drive/Night Steps attempt binds its own source and settings. No final candidate has been chosen.'
P.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');(R/'SERIES/19-30/production/suno-drive-eight-20261026.json').write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'attempts':len(j['attempts']),'create_clicks':sum(a.get('create_clicks',0) for a in j['attempts']),'new_candidates':sum(len(a.get('candidates',[])) for a in j['attempts']),'host_raw':str(raw),'production':'SERIES/19-30/production/suno-drive-eight-20261026.json'}))
