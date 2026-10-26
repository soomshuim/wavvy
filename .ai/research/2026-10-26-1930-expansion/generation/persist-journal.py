import json,re,shutil
from pathlib import Path
from datetime import datetime,timezone
root=Path('/Users/zenkim_office/Project/wavvy')
out=root/'.ai/research/2026-10-26-1930-expansion/generation'
src=Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_LVWBD7MtjzT9B8wW/artifacts/1930-expansion-generation')
raw=out/'raw';raw.mkdir(parents=True,exist_ok=True)
for f in src.iterdir():
 if f.is_file():shutil.copy2(f,raw/f.name)
j=json.loads((src/'journal.json').read_text());entries=[]
for x in j:
 candidates=[]
 for c in x.get('candidates',[]):
  txt=c['row_text'];m=re.match(r'^(\d+:\d+)\n',txt);duration=m.group(1) if m else None
  lines=txt.split('\n');style=next((s for i,s in enumerate(lines) if i>0 and len(s)>100),'')
  candidates.append({'id':c['href'].rsplit('/',1)[1],'title':x['title'],'url':'https://suno.com'+c['href'],'status':c.get('status','duration_displayed' if duration else 'generating_duration_not_yet_displayed'),'duration_ui':c.get('duration_ui',duration),'observed_style_description':style,'raw_row_text':txt})
 entries.append({'order':x['order'],'title':x['title'],'source_txt':x['source_txt'],'source_sha256':x['source_sha256'],'workspace':{'name':'[19:30]','id':'ee623e57-912e-4645-aa02-b1775f6930b2'},'actualsettings':x['settings'],'submitted_fields':x.get('readback',{'style':x['style'],'exclude':x['exclude'],'lyrics':x['lyrics'],'title':x['title']}),'submitted_at_utc':x['submitted_at_utc'],'submissionstatus':x['phase'],'credits_before':x['credits_before'],'credits_after':x.get('credits_after'),'form_exact_match':x['form_exact_match'],'candidates':candidates,'decision':{'status':'pending','chosen_candidate_id':None},'rawref':'.ai/research/2026-10-26-1930-expansion/generation/raw/'+str(x['order']).zfill(2)+'-before.txt'})
p=root/'SERIES/19-30/input/suno-candidates.json'
d=json.loads(p.read_text()) if p.exists() else {'schema_version':1,'scope':'19:30 expansion candidates; not final selected sources','tracks':[],'existing_reference_tracks':json.loads((root/'.ai/research/2026-10-26-1930-six-tracks/refresh-01/refresh.json').read_text())['tracks']}
old={x['order']:x for x in d['tracks']}
for e in entries:
 if e['order'] in old and old[e['order']].get('decision',{}).get('status')!='pending':e['decision']=old[e['order']]['decision']
 old[e['order']]=e
d['tracks']=[old[k] for k in sorted(old)];p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
manifest={'user_authorization':{'quote':'생성해.','scope':'14 independent designs, one initial Create submission each, both candidates preserved; no final candidate selection'},'updated_at_utc':datetime.now(timezone.utc).isoformat(),'workspace':{'name':'[19:30]','id':'ee623e57-912e-4645-aa02-b1775f6930b2'},'create_clicks':sum(x['phase']!='ready' for x in j),'credits_initial':1506,'credits_latest':j[-1].get('credits_after') if j else 1506,'submissions':entries,'original_source_files_untouched':True,'final_selection':'pending','download_attempts':0,'playback_actions':0,'personalize_button_clicks':0}
(root/'SERIES/19-30/production/suno-expansion-20261026.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'submitted':manifest['create_clicks'],'candidates':sum(len(x['candidates']) for x in entries),'credits':manifest['credits_latest']},ensure_ascii=False))
