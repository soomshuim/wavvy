#!/usr/bin/env python3
"""Stream two beat-aligned cycles to AAC; never write a two-hour WAV."""
import argparse,hashlib,json,math,re,subprocess,warnings
from pathlib import Path
import numpy as np
from scipy import signal
from scipy.io import wavfile
ROOT=Path(__file__).resolve().parents[3];SERIES=ROOT/'SERIES/07-00';SR=48000
PLAN=SERIES/'production/continuous-180-20261024/plan.json'
OUT=SERIES/'output/continuous-180-20261024';RECORD=SERIES/'production/continuous-180-20261024'
L=16*16000;CONTEXT=L

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def save(p,v):
 assert not p.exists(),p
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

def read(p):
 with warnings.catch_warnings():
  warnings.simplefilter('ignore',wavfile.WavFileWarning);rate,a=wavfile.read(p,mmap=True)
 assert rate==SR and a.ndim==2 and a.shape[1]==2 and a.dtype==np.float32
 return a

def measure(path):
 cmd=['ffmpeg','-hide_banner','-nostdin','-i',str(path),'-af','loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json','-f','null','-']
 r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0
 data,_=json.JSONDecoder().raw_decode(r.stderr[r.stderr.rfind('{'):])
 return {'integrated_lufs':float(data['input_i']),'true_peak_dbtp':float(data['input_tp']),'loudness_range_lu':float(data['input_lra']),'command':cmd}

def load():
 c=json.loads(PLAN.read_text());assert not c['failures'] and len(c['sources'])==len(c['pairs'])==20
 assert c['repeat_count']==2 and c['additional_repeats']==0
 sources={s['order']:s for s in c['sources']};audio={}
 for i,s in sources.items():
  p=ROOT/s['path'];assert sha(p)==s['sha256'];audio[i]=read(p)
 return c,sources,audio

def preview(pair,sources,audio):
 o=pair['outgoing'];i=pair['incoming'];out=audio[o['order']];inc=audio[i['order']]
 t=o['start_sample'];h=i['start_sample'];assert t>=CONTEXT and h+L+CONTEXT<=len(inc)
 go=10**(sources[o['order']]['gain_db']/20);gi=10**(sources[i['order']]['gain_db']/20)
 f=np.linspace(0,math.pi/2,L);fo=np.cos(f);fi=np.sin(f)
 mixed=np.asarray(out[t:t+L])*go*fo[:,None]+np.asarray(inc[h:h+L])*gi*fi[:,None]
 p=np.concatenate([np.asarray(out[t-CONTEXT:t])*go,mixed,np.asarray(inc[h+L:h+L+CONTEXT])*gi]).astype(np.float32)
 assert len(p)==3*L and np.isfinite(p).all() and max(abs(p.ravel()))<1
 path=OUT/'transitions'/f'{pair["label"]}.wav';assert not path.exists();wavfile.write(path,SR,p)
 bins=p[L:2*L][:L//4800*4800].reshape(-1,4800,2)
 rms=np.sqrt(np.mean(bins.astype(float)**2,axis=(1,2)))
 assert float(min(rms))>10**(-40/20),(pair['label'],'low overlap RMS',min(rms))
 r={'label':pair['label'],'path':str(path.relative_to(ROOT)),'sha256':sha(path),'samples':len(p),'overlap_preview_samples':[L,2*L],'minimum_overlap_100ms_rms_dbfs':float(20*np.log10(min(rms))),'peak_abs':float(np.max(abs(p))),'shared_observed_quarters':pair['shared_observed_quarters'],'cross_source_quarter_phase':pair['cross_source_quarter_phase'],'equal_power_fade':{'out':'cos(0..pi/2)','in':'sin(0..pi/2)','squared_gains_sum':1},'source_body_before_and_after_preserved_at_constant_gain':True,'loudness':measure(path),'technical_gate_pass':True,'listener_approved':False}
 return r

def prepare(selected=None):
 c,sources,audio=load();(OUT/'transitions').mkdir(parents=True,exist_ok=True)
 results=[]
 for pair in c['pairs']:
  if selected and pair['label'] not in selected:continue
  record=RECORD/f'preview-{pair["label"]}.json'
  if record.exists():
   r=json.loads(record.read_text());assert sha(ROOT/r['path'])==r['sha256']
  else:r=preview(pair,sources,audio);save(record,r)
  results.append(r);print(json.dumps({'pair':r['label'],'phase_p90_ms':r['cross_source_quarter_phase']['p90_abs_ms'],'peak':r['peak_abs'],'minimum_overlap_rms_dbfs':r['minimum_overlap_100ms_rms_dbfs']},ensure_ascii=False),flush=True)
 return results

def make_timeline(c,audio,previews):
 by_out={p['outgoing']['order']:p for p in c['pairs']};by_in={p['incoming']['order']:p for p in c['pairs']}
 chunks=[];entries=[];cursor=0
 def add(part):
  nonlocal cursor
  part['mix_start_sample']=cursor;cursor+=part['samples'];part['mix_end_sample']=cursor;chunks.append(part)
 for cycle in (1,2):
  for order in range(1,21):
   if cycle==1 and order==1:entries.append({'cycle':1,'order':1,'mix_entry_sample':0})
   start=0 if cycle==1 and order==1 else by_in[order]['incoming']['start_sample']+L
   end=len(audio[20]) if cycle==2 and order==20 else by_out[order]['outgoing']['start_sample']
   assert end-start>20*SR,(cycle,order,start,end)
   add({'kind':'body','cycle':cycle,'order':order,'source_start_sample':start,'source_end_sample':end,'samples':end-start})
   if cycle==2 and order==20:continue
   incoming=order%20+1;next_cycle=cycle+(order==20);p=by_out[order];r=previews[p['label']]
   entries.append({'cycle':next_cycle,'order':incoming,'mix_entry_sample':cursor})
   add({'kind':'transition','cycle':cycle,'label':p['label'],'incoming_cycle':next_cycle,'incoming_order':incoming,'preview_path':r['path'],'preview_sha256':r['sha256'],'preview_start_sample':L,'preview_end_sample':2*L,'samples':L})
 assert len(chunks)==79 and len(entries)==40 and sum(x['kind']=='transition' for x in chunks)==39
 assert [(e['cycle'],e['order']) for e in entries]==[(c,i) for c in (1,2) for i in range(1,21)]
 for e in entries:
  s=c['sources'][e['order']-1];e.update({'title':s['title'],'mix_entry_seconds':e['mix_entry_sample']/SR,'meaning':'incoming fade and aligned four-bar start; gain starts at zero, not certified first audible sample'})
 return {'expected_samples':cursor,'expected_seconds':cursor/SR,'chunks':chunks,'track_entries':entries}

def reference(chunk,sources,audio):
 if chunk['kind']=='body':return audio[chunk['order']],chunk['source_start_sample'],10**(sources[chunk['order']]['gain_db']/20)
 p=ROOT/chunk['preview_path'];assert sha(p)==chunk['preview_sha256'];return read(p),chunk['preview_start_sample'],1.

def verify_aac(path,timeline,sources,audio,master_gain):
 checks=[]
 for chunk in timeline['chunks']:
  if chunk['kind']=='body' and chunk['cycle']==2:continue
  local=chunk['samples']//2-SR//2
  start=chunk['mix_start_sample']+local
  src,offset,gain=reference(chunk,sources,audio)
  ref=np.asarray(src[offset+local:offset+local+SR],float)*gain*master_gain
  cmd=['ffmpeg','-v','error','-nostdin','-ss',f'{start/SR:.12f}','-i',str(path),'-t','1','-c:a','pcm_f32le','-f','f32le','-']
  actual=np.frombuffer(subprocess.check_output(cmd),dtype='<f4').reshape(-1,2).astype(float)
  assert actual.shape==ref.shape
  x=ref.mean(axis=1);y=actual.mean(axis=1);corr=float(np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y)))
  cc=signal.correlate(y,x,mode='full',method='fft');center=len(x)-1;lag=int(np.argmax(cc[center-96:center+97])-96)
  assert corr>=.95 and abs(lag)<=2,('AAC content/timing mismatch',chunk,corr,lag)
  checks.append({'kind':chunk['kind'],'order':chunk.get('order'),'cycle':chunk['cycle'],'label':chunk.get('label'),'mix_start_sample':start,'compared_samples':SR,'zero_lag_waveform_correlation':corr,'best_lag_samples_plus_minus_2ms':lag,'command':cmd})
 assert sum(r['kind']=='transition' for r in checks)==39 and sum(r['kind']=='body' for r in checks)==20
 return checks

def render():
 c,sources,audio=load();rs=prepare();assert len(rs)==20
 previews={r['label']:r for r in rs}
 timeline=make_timeline(c,audio,previews)
 loudest=max([s['loudness']['true_peak_dbtp']+s['gain_db'] for s in c['sources']]+[r['loudness']['true_peak_dbtp'] for r in rs])
 master_db=min(0,-2.5-loudest);master_gain=10**(master_db/20)
 path=OUT/'continuous-mix-0700-repeat2.m4a';assert not path.exists()
 cmd=['ffmpeg','-hide_banner','-v','error','-nostdin','-n','-f','f32le','-ar',str(SR),'-ac','2','-i','pipe:0','-c:a','aac','-b:a','320k','-movflags','+faststart',str(path)]
 digest=hashlib.sha256();checks=[];peak=0.;total=0
 with (OUT/'encode.log').open('wb') as log:
  proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=log)
  try:
   for chunk in timeline['chunks']:
    src,start,gain=reference(chunk,sources,audio);h=hashlib.sha256()
    for k in range(0,chunk['samples'],10*SR):
     count=min(10*SR,chunk['samples']-k)
     part=(np.asarray(src[start+k:start+k+count],float)*gain*master_gain).astype('<f4')
     assert len(part)==count and np.isfinite(part).all()
     peak=max(peak,float(np.max(abs(part))));assert peak<1
     raw=part.tobytes();digest.update(raw);h.update(raw);proc.stdin.write(raw);total+=count
    checks.append({'kind':chunk['kind'],'cycle':chunk['cycle'],'order':chunk.get('order'),'label':chunk.get('label'),'samples':chunk['samples'],'pcm_sha256':h.hexdigest(),'source_gain_db':sources[chunk['order']]['gain_db'] if chunk['kind']=='body' else None})
   proc.stdin.close();assert proc.wait()==0
  finally:
   if proc.poll() is None:proc.terminate();proc.wait()
 assert total==timeline['expected_samples']
 before=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(path)],text=True))
 assert abs(float(before['format']['duration'])-total/SR)<.1
 codec_cmd=['ffprobe','-v','error','-select_streams','a:0','-show_frames','-show_entries','frame=nb_samples','-of','csv=p=0',str(path)]
 decoded=sum(int(line.split(',')[0]) for line in subprocess.check_output(codec_cmd,text=True).splitlines() if line.strip())
 assert 0<=decoded-total<1024,(decoded,total)
 content=verify_aac(path,timeline,sources,audio,master_gain)
 loud=measure(path);assert loud['true_peak_dbtp']<=-1.,loud
 result={'schema':'wavvy.continuous_mix.repeat2.v1','series':'07-00','status':'rendered_technical_checks_pass_listening_pending','listening_approved':False,'plan_path':str(PLAN.relative_to(ROOT)),'plan_sha256':sha(PLAN),'producer_script_path':str(Path(__file__).relative_to(ROOT)),'producer_script_sha256':sha(Path(__file__)),'sources':c['sources'],'repeat_count':2,'additional_repeats':0,'sample_rate':SR,'overlap_quarter_beats':16,'overlap_seconds':L/SR,'timeline':timeline,'transition_results':rs,'track_gain_target_lufs':-16,'master_gain_db':master_db,'master_gain_reason':'constant headroom against measured source and transition true peaks; no limiter or extra tempo change','pcm_stream_encoding':'float32 little-endian stereo 48000 Hz','pcm_stream_sha256':digest.hexdigest(),'pcm_stream_samples':total,'pcm_stream_peak':peak,'all79_chunk_hashes':checks,'no_repeat_wav_written':True,'audio_path':str(path.relative_to(ROOT)),'audio_sha256':sha(path),'encode_command':cmd,'probe':before,'decoded_samples':decoded,'codec_tail_padding_samples':decoded-total,'codec_sample_count_command':codec_cmd,'aac_content_timing_checks':content,'final_loudness':loud,'native_song_quiet_passages_not_removed':True,'limitations':['No automated measurement constitutes listening approval.','Track entries identify incoming fade starts, not first audible samples.','Model-supported bar phase and observed attack alignment are measured estimates, not performer annotations.']}
 save(RECORD/'manifest.json',result)
 print(json.dumps({'audio':result['audio_path'],'seconds':total/SR,'samples':total,'transitions':39,'entries':40,'minimum_aac_waveform_correlation':min(r['zero_lag_waveform_correlation'] for r in content),'maximum_aac_lag_samples':max(abs(r['best_lag_samples_plus_minus_2ms']) for r in content),'loudness':loud,'master_gain_db':master_db},ensure_ascii=False),flush=True)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['preview','render']);p.add_argument('--pairs',nargs='*');args=p.parse_args()
 if args.action=='preview':prepare(args.pairs)
 else:render()
