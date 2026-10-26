#!/usr/bin/env python3
"""Read-only measurements: collect codec/source comparisons without changing gates."""
import importlib.util
import json
import time
from pathlib import Path
import numpy as np
from scipy import signal

P = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location('assembly170', P/'assemble-170.py')
A = importlib.util.module_from_spec(s)
s.loader.exec_module(A)

def db(x):
    return float(20*np.log10(max(float(np.sqrt(np.mean(np.asarray(x, float)**2))), 1e-30)))

def correlation(x, y):
    x=np.asarray(x, float).ravel(); y=np.asarray(y, float).ravel()
    return float(np.dot(x,y)/max(np.linalg.norm(x)*np.linalg.norm(y),1e-30))

def lag(x,y):
    x=np.asarray(x,float).mean(axis=1);y=np.asarray(y,float).mean(axis=1)
    cc=signal.correlate(y,x,mode='full',method='fft'); c=len(x)-1
    return int(np.argmax(cc[c-96:c+97])-96)

def reference(plan,audio,start):
    out=np.zeros((A.SR,2),float)
    for ek,e in enumerate(plan['entries']):
        left=max(start,e['mix_start_sample']);right=min(start+A.SR,e['mix_end_sample'])
        if right<=left:continue
        loc=np.arange(left-e['mix_start_sample'],right-e['mix_start_sample']);w=np.ones(len(loc))
        if ek:
            ln=plan['transitions'][ek-1]['overlap_samples']
            w*=np.sin(np.clip(loc/(ln-1),0,1)*np.pi/2)
        if ek<39:
            ln=plan['transitions'][ek]['overlap_samples']
            w*=np.cos(np.clip((loc-(e['samples']-ln))/(ln-1),0,1)*np.pi/2)
        out[left-start:right-start]+=np.asarray(audio[e['order']][loc[0]:loc[-1]+1])*w[:,None]*10**(e['source_gain_db']/20)
    return out

def main():
    started=time.monotonic()
    plan=json.loads((P/'mix-plan.json').read_text());enc=json.loads((P/'encode-record.json').read_text())
    _,audio=A.load();wav=A.ROOT/enc['wav_path'];aac=A.ROOT/enc['aac_path']
    assert A.sha(wav)==enc['wav_sha256'] and A.sha(aac)==enc['aac_sha256']
    locations=[('body',e['entry'],(e['mix_start_sample']+e['mix_end_sample'])//2-A.SR//2) for e in plan['entries']]
    locations += [('transition',t['number'],(t['start_sample']+t['end_sample'])//2-A.SR//2) for t in plan['transitions']]
    bands={'low_40_250':(40,250),'mid_250_3000':(250,3000),'high_3000_16000':(3000,16000)}
    filters={name:signal.butter(4,edges,btype='bandpass',fs=A.SR,output='sos') for name,edges in bands.items()}
    checks=[]
    for kind,n,start in locations:
        x,cw=A.decode_window(wav,start);y,ca=A.decode_window(aac,start)
        ref=reference(plan,audio,start);mx=x.astype(float).mean(axis=1);my=y.astype(float).mean(axis=1)
        rm=ref.mean(axis=1);energy=np.sqrt(np.mean(mx*mx))
        bands_result={}
        for name,filt in filters.items():
            bx=signal.sosfiltfilt(filt,x.astype(float),axis=0)[512:-512]
            by=signal.sosfiltfilt(filt,y.astype(float),axis=0)[512:-512]
            bands_result[name]={'stereo_correlation':correlation(bx,by),'wav_rms_dbfs':db(bx),
                'aac_rms_dbfs':db(by),'difference_rms_dbfs':db(by-bx),'error_snr_db':db(bx)-db(by-bx)}
        c=correlation(mx,my) if energy>=1e-6 else None
        bestlag=lag(x,y) if c is not None else None
        identity=correlation(rm,mx) if np.linalg.norm(rm)>1e-6 else None
        ilag=lag(ref,x) if identity is not None else None
        row={'kind':kind,'number':n,'start_sample':start,'frames':A.SR,
             'mono_correlation':c,'stereo_correlation':correlation(x,y),'left_correlation':correlation(x[:,0],y[:,0]),
             'right_correlation':correlation(x[:,1],y[:,1]),'best_lag_samples':bestlag,
             'wav_rms_dbfs':db(x),'aac_rms_dbfs':db(y),'mono_wav_rms_dbfs':db(mx),
             'difference_rms_dbfs':db(y-x),'error_snr_db':db(x)-db(y-x),
             'maximum_absolute_difference':float(np.max(abs(y-x))),
             'declared_source_mono_correlation':identity,'declared_source_lag_samples':ilag,
             'existing_mono_gate_pass':(float(np.max(abs(y-x)))<1e-4 if c is None else c>.95 and abs(bestlag)<=2),
             'existing_source_gate_pass':identity is None or identity>.98 and abs(ilag)<=2,
             'bands':bands_result,'commands':[cw,ca]}
        checks.append(row)
        print(json.dumps({k:row[k] for k in ['kind','number','mono_correlation','stereo_correlation','best_lag_samples','existing_mono_gate_pass','existing_source_gate_pass']}),flush=True)
    result={'schema':'wavvy.final_codec_window_audit.v1','read_only':True,'audio_modified':False,
            'does_not_override_existing_gate':True,'wav_sha256':enc['wav_sha256'],'aac_sha256':enc['aac_sha256'],
            'window_count':len(checks),'existing_mono_gate_failures':[{'kind':c['kind'],'number':c['number']} for c in checks if not c['existing_mono_gate_pass']],
            'existing_source_gate_failures':[{'kind':c['kind'],'number':c['number']} for c in checks if not c['existing_source_gate_pass']],
            'checks':checks,'elapsed_seconds':time.monotonic()-started}
    A.save(P/'final-window-audit.json',result)
    print(json.dumps({k:result[k] for k in ['window_count','existing_mono_gate_failures','existing_source_gate_failures','elapsed_seconds']}),flush=True)

if __name__=='__main__':main()
