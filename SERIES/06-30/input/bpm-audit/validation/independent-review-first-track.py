import pathlib,json,hashlib
import numpy as np
from scipy import signal,ndimage
from scipy.io import wavfile
b=pathlib.Path("SERIES/06-30/input/bpm-audit/audio")
settings=[
("a3af370c-b53f-4ecb-baa5-56bacc466599-30s.wav",178.7),
("a3af370c-b53f-4ecb-baa5-56bacc466599-front-30s.wav",179.5),
("6ee02826-a14c-48e9-bf63-5671bae1008c-resume20261023-30s.wav",192.0),
("63595bb8-89b5-403c-8ded-0f0adf8934f2-resume20261023-30s.wav",187.5),
("3d7dd056-493e-4952-8236-506934affdff-resume20261023-30s.wav",187.7)]
for name,bpm in settings:
 pth=b/name
 sr,a=wavfile.read(pth)
 rms=np.sqrt(np.mean(a.reshape(30,sr,2)**2,axis=(1,2)))
 meta={"file":name,"sha256":hashlib.sha256(pth.read_bytes()).hexdigest(),
       "duration_s":len(a)/sr,"sample_rate_hz":sr,"channels":a.shape[1],
       "all_finite":bool(np.isfinite(a).all()),
       "nonzero_samples":int(np.count_nonzero(a)),
       "per_second_rms_min":float(min(rms))}
 a=signal.resample_poly(a.mean(axis=1),1,3);sr=sr/3
 acrows=[];timestamps=None
 for lo,hi in [(35,90),(90,220),(220,800),(3000,7500)]:
  z=signal.sosfiltfilt(signal.butter(3,[lo,hi],fs=sr,btype="bandpass",output="sos"),a)
  e=ndimage.gaussian_filter1d(np.sqrt(ndimage.uniform_filter1d(z*z,size=round(sr*.012)))[::16],5)
  onset=np.maximum(np.diff(e),0)
  if lo==35:
   pk,prop=signal.find_peaks(onset,distance=80,prominence=np.percentile(onset,99)*.2)
   ts=pk/1000;strength=prop["prominences"]
   keep=(ts>=10)&(ts<=30);ts=ts[keep];strength=strength[keep]
   timestamps=(ts,strength)
  for start,stop in [(0,30),(0,10),(10,20),(20,30)]:
   x=onset[round(start*1000):round(stop*1000)];x=x-x.mean();n=len(x)
   ac=signal.correlate(x,x,method="fft")[n-1:]/np.arange(n,0,-1);ac/=ac[0]
   peaks,_=signal.find_peaks(ac);peaks=peaks[(peaks>=250)&(peaks<3000)]
   peaks=peaks[np.argsort(ac[peaks])[::-1]][:5]
   pp=[]
   for i in peaks:
    d=.5*(ac[i-1]-ac[i+1])/(ac[i-1]-2*ac[i]+ac[i+1])
    pp.append({"lag_s":round((i+d)/1000,6),"ac":round(float(ac[i]),4)})
   acrows.append({"band":[lo,hi],"window":[start,stop],"top5_peaks":pp})
 ts,strength=timestamps;period=30/bpm;best=None
 for t0 in ts:
  ns=np.rint((ts-t0)/period);res=ts-t0-ns*period;m=abs(res)<.025
  valid=True
  for iteration in range(2):
   if sum(m)<4 or np.ptp(ns[m])<4:
    valid=False;break
   slope,offset=np.polyfit(ns[m],ts[m],1)
   res=ts-(offset+slope*ns);m=abs(res)<.025
  if not valid or sum(m)<4 or np.ptp(ns[m])<4:continue
  score=(float(sum(strength[m])),int(sum(m)))
  if best is None or score>best[0]:best=(score,slope,offset,ns,m,res)
 score,slope,offset,ns,m,res=best
 # 0.005 BPM spacing and 256 phases introduce less than 0.8ms over 30s.
 target_best=(0.0,None)
 for target in np.linspace(175,177,401):
  per=30/target
  phases=np.linspace(0,per,256,endpoint=False)
  err=(ts[None,:]-phases[:,None]+per/2)%per-per/2
  scores=(abs(err)<.026)@strength/sum(strength)
  scoremax=float(max(scores))
  if scoremax>target_best[0]:target_best=(scoremax,float(target))
 targets={"bpm_band":[175,177],"tempo_step":.005,"phase_count":256,
          "conservative_tolerance_ms":26,
          "best_weighted_match_fraction":target_best[0],
          "best_bpm_grid_point":target_best[1]}
 grid={"seed_bpm_from_previous_unconstrained_autocorrelation":bpm,
       "observed_window_s":[10,30],"subdivision_s":float(slope),
       "bpm_for_2_3_4_subdivisions":[30/slope,20/slope,15/slope],
       "matched_attacks":int(sum(m)),"total_attacks":len(ts),
       "weighted_match_fraction":score[0]/sum(strength),
       "max_abs_residual_ms":float(max(abs(res[m]))*1000),
       "p95_abs_residual_ms":float(np.percentile(abs(res[m]),95)*1000),
       "matched_timestamp_and_grid_index":list(zip(ts[m].tolist(),ns[m].astype(int).tolist())),
       "target_comparison":targets}
 print(json.dumps({"metadata":meta,"acf":acrows,"onset_grid":grid}))
