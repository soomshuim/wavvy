#!/usr/bin/env python3
"""Independent output model measurements; raw half-rate observations stay raw."""
import argparse,importlib.util,json,subprocess,time
from pathlib import Path
import numpy as np
import torch
from beat_this.inference import Audio2Frames
from beat_this.model.postprocessor import Postprocessor
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('r170',P/'render-170.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
ROOT=R.ROOT;WORK=R.WORK;SR=R.SR
CK=ROOT/'work/0700-remaster-20261024/beat-model/checkpoints/beat_this-final0.ckpt'
EXPECTED='8c328b45f59d8dd3dff219253ff6a8d6482be57d0133a29140e2febbf8eb8331'

def main(orders):
    assert R.sha(CK)==EXPECTED
    torch.set_num_threads(4);model=Audio2Frames(checkpoint_path=str(CK),device='mps',float16=False);post=Postprocessor(type='minimal')
    for order in orders:
        dest=P/'independent-beats'/f'{order:02d}.json'
        if dest.exists():continue
        start=time.monotonic();j=json.loads((P/'corrected'/f'{order:02d}.json').read_text());audio=ROOT/j['output_path'];assert R.sha(audio)==j['output_sha256']
        cmd=['ffmpeg','-v','error','-nostdin','-i',str(audio),'-ar','22050','-ac','1','-f','f32le','-']
        x=np.frombuffer(subprocess.check_output(cmd),'<f4').copy();lb,ld=model(x,22050);beats,downbeats=post(lb,ld)
        bp=lb.sigmoid().cpu().numpy();dp=ld.sigmoid().cpu().numpy();cache=WORK/'beat-measurements'/f'{order:02d}.npz';cache.parent.mkdir(exist_ok=True);np.savez_compressed(cache,beat_probability=bp,downbeat_probability=dp)
        first=j['first_grid_beat_sample']/SR;n=j['grid_beat_count'];grid=(j['first_grid_beat_sample']+np.array([R.quarter_sample(k) for k in range(n)]))/SR
        b=beats[(beats>=grid[0])&(beats<=grid[-1])]
        long=(60*16/(b[16:]-b[:-16])).tolist() if len(b)>16 else []
        median=float(np.median(long)) if long else None
        family='full~170' if median and abs(median-170)<5 else 'half~85' if median and abs(median-85)<3 else 'mixed/uncertain'
        offsets=[]
        for g in grid:
            if len(beats):
                near=beats[np.argmin(abs(beats-g))]
                if abs(near-g)<.09:offsets.append(float((near-g)*1000))
        result={'schema':'wavvy.rubberband_independent_output_beats.v1','order':order,'song_id':j['song_id'],'title':j['title'],
          'audio_path':j['output_path'],'audio_sha256':R.sha(audio),'model':'CPJKU Beat This1.1.0 final0',
          'checkpoint_sha256':EXPECTED,'device':'mps','frame_rate':50,'postprocessor':'minimal/noDBN',
          'raw_beat_seconds':beats.tolist(),'raw_downbeat_seconds':downbeats.tolist(),
          'body_raw_model_16_interval_bpm_median':median,'body_raw_model_pulse_family':family,
          'body_raw_model_bpm_p10_p50_p90':np.quantile(long,[.1,.5,.9]).tolist() if long else None,
          'expected_body_quarters':n,'near_model_peak_count_within90ms':len(offsets),
          'model_minus_grid_ms_p10_p50_p90':np.quantile(offsets,[.1,.5,.9]).tolist() if offsets else None,
          'cache_path':R.relative(cache),'cache_sha256':R.sha(cache),'decode_command':cmd,
          'elapsed_seconds':time.monotonic()-start,'direct_listening':False,
          'limitations':['Raw model pulse is not doubled or halved to manufacture170.',
             'Model spacing20ms; syncopation, meter aliases, missed beats and sparse music limit confidence.',
             'Full~170 and half~85 are separately reported; ambiguous output is not automatic proof of wrong time stretching.',
             'Model did not drive the input time map or the Rubber Band transformation.']}
        R.save(dest,result);print(json.dumps({'order':order,'title':j['title'],'raw_model_bpm':median,'family':family,'offsets_ms':result['model_minus_grid_ms_p10_p50_p90'],'elapsed':result['elapsed_seconds']},ensure_ascii=False),flush=True);torch.mps.empty_cache()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--orders',type=int,nargs='+');a=p.parse_args();main(a.orders or range(1,21))
