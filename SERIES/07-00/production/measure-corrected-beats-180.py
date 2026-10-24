#!/usr/bin/env python3
"""Independent Beat This measurements of corrected audio; no audio mutation."""
import argparse,hashlib,json,subprocess,time
from pathlib import Path
import numpy as np
import torch
from beat_this.inference import Audio2Frames
from beat_this.model.postprocessor import Postprocessor
ROOT=Path(__file__).resolve().parents[3]
SERIES=ROOT/'SERIES/07-00'
WORK=ROOT/'work/0700-remaster-20261024'
CHECKPOINT=WORK/'beat-model/checkpoints/beat_this-final0.ckpt'
EXPECTED='8c328b45f59d8dd3dff219253ff6a8d6482be57d0133a29140e2febbf8eb8331'

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def main(orders):
 assert sha(CHECKPOINT)==EXPECTED
 torch.set_num_threads(4)
 model=Audio2Frames(checkpoint_path=str(CHECKPOINT),device='mps',float16=False)
 post=Postprocessor(type='minimal')
 folder=SERIES/'production/corrected-beats-20261024';folder.mkdir(exist_ok=True)
 cache=WORK/'beat-measurements';cache.mkdir(exist_ok=True)
 for order in orders:
  out=folder/f'{order:02d}.json';assert not out.exists(),out
  t=time.monotonic()
  correction=SERIES/'production/tempo-corrected-20261024'/f'{order:02d}.json'
  a=json.loads(correction.read_text());p=ROOT/a['output_path']
  assert sha(p)==a['output_sha256']
  cmd=['ffmpeg','-hide_banner','-v','error','-nostdin','-i',str(p),'-ac','1','-ar','22050','-f','f32le','-']
  x=np.frombuffer(subprocess.check_output(cmd),dtype='<f4').copy()
  logits_b,logits_d=model(x,22050)
  beats,downbeats=post(logits_b,logits_d)
  bp=logits_b.sigmoid().cpu().numpy();dp=logits_d.sigmoid().cpu().numpy()
  npz=cache/f'{order:02d}.npz';np.savez_compressed(npz,beat_probability=bp,downbeat_probability=dp)
  b0=a['first_grid_beat_output_seconds'];n=a['grid_beat_count']
  grid=b0+np.arange(n)/3
  frame=np.clip(np.rint(grid*50).astype(int),0,len(bp)-1)
  b_near=np.array([np.max(bp[max(0,i-2):min(len(bp),i+3)]) for i in frame])
  d_near=np.array([np.max(dp[max(0,i-2):min(len(dp),i+3)]) for i in frame])
  regions={}
  for label,lower,upper in [('head',max(1,b0),min(35,len(x)/22050-10)),('body',10,len(x)/22050-10),('tail',max(10,len(x)/22050-40),len(x)/22050-2)]:
   mask=(grid>=lower)&(grid<=upper)
   phase=[]
   for q in range(4):
    ids=np.flatnonzero(mask & (np.arange(n)%4==q))
    phase.append(float(np.mean(d_near[ids])) if len(ids) else 0.)
   winners=[]
   for k in np.flatnonzero(mask):
    nearest=beats[np.argmin(abs(beats-grid[k]))] if len(beats) else float('inf')
    if abs(nearest-grid[k])<.09:winners.append(float(nearest-grid[k]))
   regions[label]={'seconds':[lower,upper],'downbeat_phase_mean_probabilities':phase,'best_downbeat_index_mod4':int(np.argmax(phase)),'nearest_model_beat_count_within_90ms':len(winners),'grid_quarter_count':int(sum(mask)),'model_minus_grid_ms_p10_p50_p90':(np.quantile(winners,[.1,.5,.9])*1000).tolist() if winners else None}
  result={'schema':'wavvy.independent_corrected_beats.v1','order':order,'title':a['title'],'audio_path':a['output_path'],'audio_sha256':sha(p),'correction_record_sha256':sha(correction),'model':'CPJKU Beat This 1.1.0 final0','model_source':'https://github.com/CPJKU/beat_this','model_sha256':EXPECTED,'torch_version':torch.__version__,'device':'mps','postprocessor':'minimal, no DBN','frame_rate':50,'audio_decode_command':cmd,'beat_seconds':beats.tolist(),'downbeat_seconds':downbeats.tolist(),'first_corrected_grid_beat_seconds':b0,'corrected_grid_beat_count':n,'regions':regions,'frame_cache':str(npz.relative_to(ROOT)),'frame_cache_sha256':sha(npz),'elapsed_seconds':time.monotonic()-t,'limitations':['Model peaks are estimates at 20 ms frame spacing; they are not listener approval.','Syncopation or half/double pulses can cause extra or missing model beats.','The correction grid comes from the separate multiband source analysis; this model did not drive the tempo correction.']}
  out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
  print(json.dumps({'order':order,'elapsed_seconds':result['elapsed_seconds'],'regions':regions},ensure_ascii=False),flush=True)
  torch.mps.empty_cache()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--orders',nargs='+',type=int,required=True);main(p.parse_args().orders)
