#!/usr/bin/env python3
"""Explain output model aliases with interval, phase, independent AC and FFT evidence."""
import importlib.util,json
from pathlib import Path
import numpy as np
from scipy import signal
P=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('r170',P/'render-170.py');R=importlib.util.module_from_spec(s);s.loader.exec_module(R)

def main():
    for p in sorted((P/'independent-beats').glob('[0-9][0-9].json')):
        m=json.loads(p.read_text());order=m['order'];c=json.loads((P/'corrected'/f'{order:02d}.json').read_text());qa=json.loads((P/'rubberband-qa'/f'{order:02d}.json').read_text())
        b=np.array(m['raw_beat_seconds']);q=60/170;first=c['first_grid_beat_sample']/48000;last=first+(c['grid_beat_count']-1)*q
        inside=b[(b>=first)&(b<=last)];dt=np.diff(inside)
        residual=((inside-first+q/2)%q-q/2)*1000
        types={'full_quarter~170':abs(dt-q)<.035,'half_rate~85':abs(dt-2*q)<.05,'subdivision~340':abs(dt-q/2)<.025}
        classified=np.zeros(len(dt),bool)
        for v in types.values():classified|=v
        envs=R.MEASURE.envelopes(R.ROOT/c['output_path']);windows=[]
        for center in np.arange(first+10,last-9,10):
            lo,hi=center-10,center+10;bb=inside[(inside>=lo)&(inside<hi)];dd=np.diff(bb)
            rr=((bb-first+q/2)%q-q/2)*1000
            rates=60*16/(bb[16:]-bb[:-16]) if len(bb)>16 else []
            ac=min(qa['independent_output_tempo_windows'],key=lambda w:abs(w['center_seconds']-center))
            fft={}
            for name in ['mid','high']:
                e=envs[name][round(lo*500):round(hi*500)];e=e-np.mean(e);w=np.hanning(len(e))
                spec=np.abs(np.fft.rfft(e*w,n=2**int(np.ceil(np.log2(len(e)*8)))))**2;freq=np.fft.rfftfreq(2*(len(spec)-1),1/500)
                ids,_=signal.find_peaks(spec);ids=ids[(freq[ids]>=50/60)&(freq[ids]<=220/60)];ids=sorted(ids,key=lambda k:spec[k],reverse=True)[:8]
                fft[name]=[{'bpm':float(freq[k]*60),'relative_power':float(spec[k]/max(np.max(spec),1e-30))} for k in ids]
            windows.append({'seconds':[float(lo),float(hi)],'model_beat_count':len(bb),
                'model_interval_seconds_p10_p50_p90':np.quantile(dd,[.1,.5,.9]).tolist() if len(dd) else None,
                'model_16_interval_bpm_median':float(np.median(rates)) if len(rates) else None,
                'model_phase_residual_ms_p10_p50_p90':np.quantile(rr,[.1,.5,.9]).tolist() if len(rr) else None,
                'model_peak_fraction_within40ms_of170_grid':float(np.mean(abs(rr)<=40)) if len(rr) else None,
                'independent_mid_high_ac_bpm':{k:ac['band_bpm'][k] for k in ['mid','high']},
                'independent_attack_fft_peaks_50_to220_bpm':fft})
        result={'schema':'wavvy.output_model_alias_diagnosis.v1','order':order,'song_id':m['song_id'],'title':m['title'],
            'raw_model_bpm':m['body_raw_model_16_interval_bpm_median'],'raw_model_family':m['body_raw_model_pulse_family'],
            'model_interval_counts':{k:int(np.sum(v)) for k,v in types.items()},'other_interval_count':int(np.sum(~classified)),
            'model_interval_seconds_p05_p50_p95':np.quantile(dt,[.05,.5,.95]).tolist(),
            'raw_model_phase_residual_ms_p10_p50_p90':np.quantile(residual,[.1,.5,.9]).tolist(),
            'model_peak_fraction_within40ms_of170_grid':float(np.mean(abs(residual)<=40)),
            'source_output_attack_lag_p90_ms':qa['attack_abs_lag_p90_ms'],
            'independent_mid_high_ac_bpm_median':qa['mid_high_output_bpm_median'],
            'windows_20s':windows,'direct_listening':False,
            'interpretation_rule':'Raw model BPM remains raw. Extra/subdivision peaks and missed/half intervals can change16-interval BPM while independent AC/FFT and corresponding attack locations still support170. Mixed evidence stays uncertain; no automatic re-render or forced doubling.',
            'limitations':['FFT peaks can be harmonics or subdivisions, not certified beats.',
              'Phase residual refers to the inferred source quarter grid, not confirmed first downbeats.']}
        R.save(P/'model-alias-diagnosis'/f'{order:02d}.json',result)
        print(json.dumps({k:result[k] for k in ['order','title','raw_model_bpm','model_interval_counts','other_interval_count','model_peak_fraction_within40ms_of170_grid','independent_mid_high_ac_bpm_median']},ensure_ascii=False),flush=True)
if __name__=='__main__':main()
