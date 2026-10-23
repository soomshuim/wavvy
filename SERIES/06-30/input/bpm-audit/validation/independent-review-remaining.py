import sys,json,hashlib
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy import signal,ndimage,optimize
ids=set(sys.argv[1:])
ledger=json.loads(Path('SERIES/06-30/input/bpm-audit/results/2026-10-23-30s-batch-ledger.json').read_text())
rows=[{k:s.get(k) for k in ['candidate_id','sample_path','sample_sha256','evidence_path']} for s in ledger['samples'] if s['candidate_id'] in ids]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def norm(x):
 if x.dtype.kind in 'iu': x=x.astype(float)/np.iinfo(x.dtype).max
 return np.asarray(x,float)
def acpeaks(z,rate):
 z=z-z.mean(); ac=signal.correlate(z,z,mode='full',method='fft')[len(z)-1:]
 ac=ac/(np.arange(len(z),0,-1)*np.var(z));lo,hi=int(rate*.17),min(int(rate*1.5),len(z)-1)
 idx,_=signal.find_peaks(ac[lo:hi],distance=max(1,int(rate*.025)))
 idx=sorted(idx+lo,key=lambda k:ac[k],reverse=True)[:7];ans=[]
 for k in idx:
  den=ac[k-1]-2*ac[k]+ac[k+1];frac=.5*(ac[k-1]-ac[k+1])/den if den else 0
  ans.append([round(60*rate/(k+frac),3),round(float(ac[k]),4)])
 return ans
def spectrum(z,rate):
 z=z-z.mean();nfft=131072;p=abs(np.fft.rfft(z*np.hanning(len(z)),n=nfft))**2
 f=np.fft.rfftfreq(nfft,1/rate);ix,_=signal.find_peaks(p)
 ix=sorted([i for i in ix if .7<=f[i]<=8],key=lambda i:p[i],reverse=True)[:5]
 return [[round(f[i]*60,3),round(float(p[i]/p.max()),4)] for i in ix]
for s in rows:
 cid=s['candidate_id'];ev=json.loads(Path(s['evidence_path']).read_text())
 sr,a=wavfile.read(s['sample_path']);a=norm(a);x=a.mean(axis=1) if a.ndim>1 else a
 rr,raw=wavfile.read(ev['raw']['path']);raw=norm(raw);lo,hi=ev['sample_raw_interval_s'];part=raw[round(lo*rr):round(hi*rr)]
 checks={'id':cid,'sha256':sha(s['sample_path']),'sample_sha_ok':sha(s['sample_path'])==s['sample_sha256']==ev['sample']['sha256'],'raw_sha_ok':sha(ev['raw']['path'])==ev['raw']['sha256'],'log_sha_ok':sha(ev['capture']['log_path'])==ev['capture']['log_sha256'],'duration_s':len(a)/sr,'raw_slice_equal':bool(rr==sr and a.shape==part.shape and np.array_equal(a,part)),'min_1s_rms':min(float(np.sqrt(np.mean(a[i*sr:(i+1)*sr]**2))) for i in range(30))}
 xd=signal.resample_poly(x,16000,sr);out={}
 for name,band in [('low',[30,180]),('mid',[180,1800]),('high',[1800,7000])]:
  y=signal.sosfiltfilt(signal.butter(4,band,btype='bandpass',fs=16000,output='sos'),xd)
  env=np.sqrt(np.mean(y[:len(y)//32*32].reshape(-1,32)**2,axis=1));env=ndimage.gaussian_filter1d(env,1.5)
  onset=np.maximum(env-np.roll(env,3),0);onset[:3]=0;onset/=np.percentile(onset,99)+1e-12;onset=np.minimum(onset,3)
  pp,_=signal.find_peaks(onset,distance=60,prominence=.15)
  out[name]={'ac_full':acpeaks(onset,500),'ac_parts':[acpeaks(z,500)[:3] for z in np.array_split(onset,3)],'spectrum_full':spectrum(onset,500),'events_s':np.round(pp/500,3).tolist(),'event_strengths':np.round(onset[pp],2).tolist()}
 seeds=[]
 for name in ['high','mid','low']:
  v=out[name]
  for b,a0 in v['ac_full'][:4]+v['spectrum_full'][:1]:
   if not any(abs(b/q-1)<.012 for q in seeds):seeds.append(b)
 fits=[]
 for seed in sorted(seeds):
  for name,v in out.items():
   t=np.array(v['events_s']);w=np.minimum(np.array(v['event_strengths']),1.5);freq=seed/60
   def coh(f):return abs(np.sum(w*np.exp(2j*np.pi*f*t)))/sum(w)
   grid=np.linspace(freq*.985,freq*1.015,101);f0=grid[np.argmax([coh(f) for f in grid])]
   opt=optimize.minimize_scalar(lambda f:-coh(f),bounds=(f0-freq*.0005,f0+freq*.0005),method='bounded');f=opt.x;p=1/f
   phase=np.angle(np.sum(w*np.exp(2j*np.pi*f*t)))/(2*np.pi*f);n=np.round((t-phase)/p)
   good=abs(t-(phase+n*p))<min(.035,p*.12);tt=t[good];nn=n[good];ww=w[good]
   if len(tt)<10:continue
   sl,it=np.polyfit(nn,tt,1,w=np.sqrt(ww));chunks=[]
   for a0,b0 in [(0,10),(10,20),(20,30)]:
    ok=(tt>=a0)&(tt<b0)
    if sum(ok)>6 and np.ptp(nn[ok])>3:
     ss,ii=np.polyfit(nn[ok],tt[ok],1,w=np.sqrt(ww[ok]));chunks.append(round(60/ss,3))
   if coh(f)>.23:fits.append({'seed':seed,'band':name,'bpm_fit':round(60/sl,3),'coherence':round(coh(f),3),'inlier_count':len(tt),'span_s':round(float(np.ptp(tt)),3),'observed_10s_estimates':chunks,'residual_p90_ms':round(float(np.quantile(abs(tt-(it+sl*nn)),.9)*1000),2),'first_actual_events_s':tt[:8].tolist(),'last_actual_events_s':tt[-5:].tolist()})
 print(json.dumps({'checks':checks,'measurements':out,'lattice_fits':fits},ensure_ascii=False),flush=True)
