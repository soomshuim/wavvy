#!/usr/bin/env python3
"""Choose observed, model-supported four-bar mix cues from corrected sources."""
import hashlib,importlib.util,json,subprocess
from pathlib import Path
import numpy as np
from scipy import signal
ROOT=Path(__file__).resolve().parents[3];SERIES=ROOT/'SERIES/07-00';SR=48000;PERIOD=1/3;N=16
spec=importlib.util.spec_from_file_location('measure',SERIES/'production/analyze-180bpm.py');measure=importlib.util.module_from_spec(spec);spec.loader.exec_module(measure)

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def summary(values):
 v=np.asarray(values)
 return {'count':len(v),'median_ms':float(np.median(v)*1000),'p90_abs_ms':float(np.quantile(abs(v),.9)*1000),'max_abs_ms':float(max(abs(v))*1000)}

def loudness(path):
 cmd=['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']
 r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0
 j,_=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])
 return {'integrated_lufs':float(j['input_i']),'true_peak_dbtp':float(j['input_tp']),'lra':float(j['input_lra']),'measurement_command':cmd}

def candidates(a,b,envs,kind):
 b0=a['first_grid_beat_output_seconds'];count=a['grid_beat_count'];duration=a['output_duration_seconds']
 cache=ROOT/b['frame_cache'];assert sha(cache)==b['frame_cache_sha256'];dp=np.load(cache)['downbeat_probability']
 region='head' if kind=='in' else 'tail'
 phase=b['regions'][region]['best_downbeat_index_mod4']
 scores=b['regions'][region]['downbeat_phase_mean_probabilities']
 if max(scores)<.4:phase=b['regions']['body']['best_downbeat_index_mod4']
 peaks={}
 for name,e in envs.items():
  p,_=signal.find_peaks(e,distance=45,prominence=.11*np.percentile(e,99));peaks[name]=p/500
 result=[]
 origins=[(b0+k*PERIOD,k,'corrected-source-grid') for k in range(phase,count-N-1,4)]
 # Source-grid phase may follow an offbeat in a sparse introduction. The
 # independent model's observed downbeats supply a second, corroborated origin.
 origins += [(float(t),None,'independent-model-downbeat') for t in b['downbeat_seconds']]
 for t,k,origin in origins:
  if kind=='in' and not 0<=t<=min(60,duration*.3):continue
  if kind=='out' and not max(0,duration-45)<=t<=duration-N*PERIOD:continue
  for name,events in peaks.items():
   initial=[]
   for q in range(N):
    v=events[np.argmin(abs(events-(t+q*PERIOD)))]
    if abs(v-t-q*PERIOD)<=.04:initial.append(float(v-t-q*PERIOD))
   if len(initial)<8:continue
   shift=float(np.median(initial));start=round((t+shift)*SR)/SR
   if start<0 or start+N*PERIOD>duration:continue
   observations={}
   for q in range(N):
    v=events[np.argmin(abs(events-(start+q*PERIOD)))]
    if abs(v-start-q*PERIOD)<=.035:observations[str(q)]=float(v-start-q*PERIOD)
   if len(observations)<8:continue
   residual=summary(list(observations.values()))
   if residual['p90_abs_ms']>20 or residual['max_abs_ms']>30:continue
   bar_times=start+np.arange(5)*4*PERIOD
   f=np.clip(np.rint(bar_times*50).astype(int),0,len(dp)-1)
   model_probs=[float(max(dp[max(0,i-2):min(len(dp),i+3)])) for i in f]
   if sum(p>=.5 for p in model_probs)<2:continue
   result.append({'kind':kind,'order':a['order'],'grid_quarter_index':k,'grid_start_seconds':t,'cue_origin':origin,'start_sample':round(start*SR),'start_seconds':start,'end_sample':round(start*SR)+N*16000,'end_seconds':start+N*PERIOD,'band':name,'refinement_from_grid_ms':(start-t)*1000,'observed_quarter_residual_seconds':observations,'attack_residual':residual,'bar_model_probabilities':model_probs,'bar_phase_index_mod4':phase,'trimmed_seconds':start if kind=='in' else duration-start-N*PERIOD})
 return result

def main():
 analyses=[];sources=[];cue_candidates={}
 folder=SERIES/'production/continuous-180-20261024';folder.mkdir(exist_ok=True)
 for order in range(1,21):
  cp=SERIES/'production/tempo-corrected-20261024'/f'{order:02d}.json';bp=SERIES/'production/corrected-beats-20261024'/f'{order:02d}.json'
  a=json.loads(cp.read_text());b=json.loads(bp.read_text());path=ROOT/a['output_path'];assert sha(path)==a['output_sha256']==b['audio_sha256']
  envs=measure.envelopes(path)
  inc=candidates(a,b,envs,'in');out=candidates(a,b,envs,'out')
  row={'order':order,'title':a['title'],'candidate_id':a['candidate_id'],'path':a['output_path'],'sha256':a['output_sha256'],'duration_seconds':a['output_duration_seconds'],'correction_record':str(cp.relative_to(ROOT)),'correction_record_sha256':sha(cp),'beat_record':str(bp.relative_to(ROOT)),'beat_record_sha256':sha(bp),'loudness':loudness(path)}
  row['gain_db']=-16-row['loudness']['integrated_lufs']
  sources.append(row);cue_candidates[order]={'in':inc,'out':out}
  print(json.dumps({'order':order,'in_candidates':len(inc),'out_candidates':len(out),'integrated_lufs':row['loudness']['integrated_lufs']},ensure_ascii=False),flush=True)
 Path(folder/'cue-candidates.json').write_text(json.dumps(cue_candidates,ensure_ascii=False,indent=2)+'\n')
 pairs=[];failures=[]
 for order in range(1,21):
  incoming=order%20+1;valid=[]
  for out in cue_candidates[order]['out']:
   for inc in cue_candidates[incoming]['in']:
    ids=sorted(set(out['observed_quarter_residual_seconds'])&set(inc['observed_quarter_residual_seconds']),key=int)
    if len(ids)<8:continue
    residual=summary([out['observed_quarter_residual_seconds'][q]-inc['observed_quarter_residual_seconds'][q] for q in ids])
    if residual['p90_abs_ms']>20 or residual['max_abs_ms']>35:continue
    score=out['trimmed_seconds']+inc['trimmed_seconds']+residual['p90_abs_ms']*.15
    # Prefer evidence across more quarters if trims are within about a beat.
    score+=(16-len(ids))*.05
    valid.append((score,out,inc,ids,residual))
  if not valid:
   failures.append({'out':order,'in':incoming});continue
  _,out,inc,ids,residual=min(valid,key=lambda v:v[0])
  pairs.append({'label':f'{order:02d}-{incoming:02d}','outgoing':out,'incoming':inc,'shared_observed_quarters':list(map(int,ids)),'cross_source_quarter_phase':residual,'overlap_samples':N*16000,'overlap_seconds':N*PERIOD})
 result={'schema':'wavvy.continuous_180_plan.v1','series':'07-00','sample_rate':SR,'target_bpm':180,'quarter_samples':16000,'overlap_quarter_beats':N,'repeat_count':2,'additional_repeats':0,'sources':sources,'pairs':pairs,'failures':failures,'status':'cue_plan_requires_preview_and_output_validation','listening_approved':False,'selection_method':'minimum intro/outro removal among 16-quarter, waveform-onset and independent bar-model supported cues; no inherited listening exceptions','gates':{'min_shared_observed_quarters':8,'cross_source_quarter_p90_abs_ms_max':20,'cross_source_quarter_max_abs_ms_max':35},'script_sha256':sha(Path(__file__))}
 dest=folder/'plan.json';assert not dest.exists();dest.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'pairs':len(pairs),'failures':failures,'cuts':[{'pair':p['label'],'out_tail_removed':p['outgoing']['trimmed_seconds'],'in_head_removed':p['incoming']['trimmed_seconds'],'phase':p['cross_source_quarter_phase']} for p in pairs]},ensure_ascii=False),flush=True)
 assert not failures,failures

if __name__=='__main__':main()
